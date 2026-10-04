"""Small finite boundary experiment. Standard library only; no model/API calls."""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import platform
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ("version", "target", "digest", "revision", "evidence", "alternatives",
          "attempt", "status", "receipt", "grant")
CONTEXT = ("alternatives", "attempt", "status", "receipt")
LABELS = {name: name.replace("_", " ") for name in FIELDS}
ARMS = ("prose-full", "typed-full", "hybrid-full", "typed-compact")
PRODUCERS = ("predicates", "graph")
CONSUMERS = ("v1-only", "compatible")


def producer(case: dict, kind: str) -> dict:
    """Adapters emit public meaning; private data structures are never transmitted."""
    defaults = dict(version=case.get("wire_version", 1), target="artifact-A",
                    digest="sha256:A", revision=7, evidence=["e-good"],
                    alternatives=[], attempt=None, status="proposed", receipt=None,
                    grant="g-good")
    if kind == "predicates":
        private = {key: case.get(key, value) for key, value in defaults.items()}
        private["internal_predicate_cache"] = {"could_release": True}
        return {key: copy.deepcopy(private[key]) for key in FIELDS}
    if kind == "graph":
        private = [("handoff", key, copy.deepcopy(case.get(key, value)))
                   for key, value in defaults.items()]
        private.append(("private", "attention", [0.2, 0.8]))
        return {key: value for node, key, value in private if node == "handoff"}
    raise ValueError(kind)


def prose(values: dict, style: str) -> str:
    keys = list(values)
    if style == "reordered":
        keys.reverse()
    return "\n".join(f"The {LABELS[key]} is {json.dumps(values[key])}." for key in keys)


def parse_prose(text: str) -> dict:
    result = {}
    for line in text.splitlines():
        for key, label in LABELS.items():
            prefix = f"The {label} is "
            if line.startswith(prefix) and line.endswith("."):
                if key in result:
                    raise ValueError("duplicate semantic field")
                result[key] = json.loads(line[len(prefix):-1])
                break
        else:
            raise ValueError("unrecognized controlled-language clause")
    return result


def encode(public: dict, arm: str, style: str, case: dict) -> str:
    values = copy.deepcopy(public)
    rationale = case.get("rationale", "Candidate proposed; no authority is asserted.")
    if style == "reordered":
        rationale += " Independent consumers may disagree."
    if arm == "prose-full":
        return json.dumps({"clauses": prose(values, style), "explanation": rationale})
    if arm == "typed-compact":
        for key in CONTEXT:
            values.pop(key)
    if values["version"] == 2:
        values["artifact_id"] = values.pop("target")
        values["content_hash"] = {"value": values.pop("digest")}
    if case.get("extension"):
        values["display_hint"] = "cosmetic addition"
    if arm == "hybrid-full":
        context = {key: values.pop(key) for key in CONTEXT}
        return json.dumps({"envelope": values, "context": prose(context, style),
                           "explanation": rationale})
    keys = list(values)
    if style == "reordered":
        keys.reverse()
    return json.dumps({"record": {key: values[key] for key in keys},
                       "explanation": rationale})


def decode(wire: str, arm: str, consumer: str) -> dict:
    message = json.loads(wire)
    if arm == "prose-full":
        values = parse_prose(message["clauses"])
    elif arm == "hybrid-full":
        values = dict(message["envelope"])
        values.update(parse_prose(message["context"]))
    else:
        values = dict(message["record"])
    version = values.get("version")
    if version not in (1, 2) or (version == 2 and consumer == "v1-only"):
        raise ValueError("unsupported schema version")
    if version == 2 and arm != "prose-full":
        values["target"] = values.pop("artifact_id")
        values["digest"] = values.pop("content_hash")["value"]
    if arm == "typed-compact":
        # Declared compression defaults, not recovery of omitted knowledge.
        values.update(alternatives=[], attempt=None, status="proposed", receipt=None)
    if not all(key in values for key in FIELDS):
        raise ValueError("missing semantic field")
    return {key: values[key] for key in FIELDS}


class World:
    def __init__(self, case: dict):
        self.case_id = case["id"]
        self.artifact = dict(target="artifact-A", digest="sha256:A", revision=7)
        self.evidence = {
            "e-good": dict(self.artifact),
            "e-conflict": dict(self.artifact, digest="sha256:other"),
        }
        self.grants = {
            "g-good": dict(target="artifact-A", operation="release", expires=101),
            "g-expired": dict(target="artifact-A", operation="release", expires=99),
            "g-wrong-scope": dict(target="artifact-A", operation="delete", expires=101),
        }
        self.effects = []
        self.receipts = {}
        self.reads = 0
        if case.get("initial_effect"):
            self.effects.append(dict(attempt="old-attempt", **self.artifact))
        if case.get("initial_receipt"):
            self.receipts["old-attempt"] = dict(id="r-old", attempt="old-attempt", **self.artifact)
        self.receipts["other-attempt"] = dict(id="r-foreign", attempt="other-attempt",
                                               target="artifact-B", digest="sha256:B", revision=7)

    def allowed(self, grant_id, target) -> bool:
        self.reads += 1
        grant = self.grants.get(grant_id, {})
        return (grant.get("target") == target and grant.get("operation") == "release"
                and grant.get("expires", 0) >= 100)

    def observe(self, evidence_ids):
        self.reads += len(evidence_ids)
        return [self.evidence.get(key) for key in evidence_ids]

    def lookup(self, attempt):
        self.reads += 1
        return self.receipts.get(attempt)

    def execute(self, grant_id, target, digest, attempt):
        # Complete mediation is independent of decoder and decision producer.
        if not self.allowed(grant_id, target):
            raise PermissionError("effect denied")
        if attempt in self.receipts:
            return self.receipts[attempt]
        effect = dict(attempt=attempt, target=target, digest=digest, revision=7)
        self.effects.append(effect)
        receipt = dict(id="receipt-" + attempt, **effect)
        self.receipts[attempt] = receipt
        return receipt


def receipt_matches(receipt, values):
    return (receipt is not None and all(receipt.get(key) == values[key]
                                       for key in ("target", "digest", "revision")))


def consume(values: dict | None, world: World) -> dict:
    if values is None:
        return dict(outcome="abstained", reason="unsupported_or_invalid_protocol", verified=False)
    if values["alternatives"] is None or values["alternatives"]:
        return dict(outcome="abstained", reason="unknown_or_ambiguous_intent", verified=False)
    if not values["target"] or values["revision"] != world.artifact["revision"]:
        return dict(outcome="abstained", reason="missing_or_stale_state", verified=False)
    facts = world.observe(values["evidence"])
    if not facts or any(fact != {key: values[key] for key in ("target", "digest", "revision")}
                        for fact in facts):
        return dict(outcome="abstained", reason="missing_or_conflicting_evidence", verified=False)
    if values["attempt"]:
        receipt = world.lookup(values["attempt"])
        valid = receipt_matches(receipt, values)
        if values["receipt"] and (receipt is None or receipt["id"] != values["receipt"]):
            valid = False
        return dict(outcome="confirmed" if valid else "unresolved",
                    reason="receipt_match" if valid else "no_matching_receipt",
                    verified=valid)
    if values["status"] != "proposed":
        return dict(outcome="abstained", reason="unsupported_completion_claim", verified=False)
    if not world.allowed(values["grant"], values["target"]):
        return dict(outcome="abstained", reason="no_authority", verified=False)
    attempt = "new-" + world.case_id
    receipt = world.execute(values["grant"], values["target"], values["digest"], attempt)
    return dict(outcome="completed", reason="executed_or_idempotently_replayed",
                verified=receipt_matches(receipt, values))


def independently_verified(world: World, values: dict | None) -> bool:
    if values is None:
        return False
    # Read-only audit does not trust consumer's flag or producer's receipt claim.
    artifact_matches = all(world.artifact[key] == values[key]
                           for key in ("target", "digest", "revision"))
    return artifact_matches and any(receipt_matches(receipt, values)
                                    for receipt in world.receipts.values())


def run_case(case, arm, producer_kind, consumer_kind, style):
    public = producer(case, producer_kind)
    started = time.perf_counter_ns()
    wire = encode(public, arm, style, case)
    encode_ns = time.perf_counter_ns() - started
    started = time.perf_counter_ns()
    try:
        decoded = decode(wire, arm, consumer_kind)
        decode_error = None
    except (ValueError, KeyError, TypeError) as error:
        decoded, decode_error = None, str(error)
    decode_ns = time.perf_counter_ns() - started
    world = World(case)
    initial_count = len(world.effects)
    started = time.perf_counter_ns()
    result = consume(decoded, world)
    # Replacement consumer starts with no private context. Same world, same wire.
    replay_values = None if decoded is None else decode(wire, arm, consumer_kind)
    replay = consume(replay_values, world)
    consumer_ns = time.perf_counter_ns() - started
    expected = case["expected"]
    if public["version"] == 2 and consumer_kind == "v1-only":
        expected = "abstained"
    loss = [key for key in FIELDS if decoded is None or decoded[key] != public[key]]
    # Independent audit compares new effects with the policy registry, not the decoder.
    authority_violations = sum(not (world.grants.get(public["grant"], {}).get("target") == e["target"]
                                   and world.grants.get(public["grant"], {}).get("operation") == "release"
                                   and world.grants.get(public["grant"], {}).get("expires", 0) >= 100)
                               for e in world.effects[initial_count:])
    false_verification = result["verified"] and not independently_verified(world, decoded)
    duplicate_effects = max(0, len(world.effects) - 1)
    return dict(case=case["id"], arm=arm, producer=producer_kind, consumer=consumer_kind,
                style=style, public=public, wire=wire, decoded=decoded,
                decode_error=decode_error, expected=expected, result=result, replay=replay,
                oracle_agreement=result["outcome"] == expected,
                useful_completion=expected in ("completed", "confirmed") and result["outcome"] == expected,
                recovery_case=case.get("recovery", False),
                recovered=case.get("recovery", False) and replay["outcome"] == expected,
                semantic_loss_fields=loss, authority_violations=authority_violations,
                false_verification=int(false_verification), duplicate_effects=duplicate_effects,
                registry_reads=world.reads, new_effects=len(world.effects)-initial_count,
                payload_bytes=len(wire.encode()), encode_ns=encode_ns, decode_ns=decode_ns,
                consumer_ns=consumer_ns, model_calls=0, final_effects=world.effects,
                final_receipts=world.receipts)


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["arm"], row["consumer"])].append(row)
    summaries = []
    for (arm, consumer), group in sorted(groups.items()):
        eligible = [r for r in group if r["expected"] in ("completed", "confirmed")]
        recovery = [r for r in group if r["recovery_case"]]
        paired = defaultdict(set)
        for row in group:
            paired[row["case"]].add((row["result"]["outcome"], row["result"]["verified"]))
        summaries.append(dict(arm=arm, consumer=consumer, n=len(group),
            agreement=sum(r["oracle_agreement"] for r in group),
            useful=sum(r["useful_completion"] for r in eligible), eligible=len(eligible),
            recovered=sum(r["recovered"] for r in recovery), recovery_n=len(recovery),
            field_loss=sum(len(r["semantic_loss_fields"]) for r in group),
            authority_violations=sum(r["authority_violations"] for r in group),
            false_verifications=sum(r["false_verification"] for r in group),
            duplicate_rows=sum(r["duplicate_effects"] > 0 for r in group),
            replacement_disagreement_cases=sum(len(v) > 1 for v in paired.values()),
            replay_disagreement_rows=sum(r["result"] != r["replay"] for r in group),
            mean_payload_bytes=statistics.mean(r["payload_bytes"] for r in group),
            total_registry_reads=sum(r["registry_reads"] for r in group),
            median_encode_ns=statistics.median(r["encode_ns"] for r in group),
            median_decode_ns=statistics.median(r["decode_ns"] for r in group),
            median_consumer_ns=statistics.median(r["consumer_ns"] for r in group)))
    return summaries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "run-001")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((ROOT / "fixtures.json").read_text())["cases"]
    rows = [run_case(case, arm, p, c, style)
            for case, arm, p, c, style in itertools.product(cases, ARMS, PRODUCERS,
                                                          CONSUMERS, ("ordered", "reordered"))]
    (args.output / "raw.jsonl").write_text("".join(json.dumps(r, sort_keys=True)+"\n" for r in rows))
    summary = summarize(rows)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    config = dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
                  cases=len(cases), rows=len(rows), arms=ARMS, producers=PRODUCERS,
                  consumers=CONSUMERS, model_calls=0, external_calls=0,
                  clocks="perf_counter_ns; encode/decode and two consumer calls",
                  input_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                for name in ("run.py", "fixtures.json", "PROTOCOL.md")})
    (args.output / "configuration.json").write_text(json.dumps(config, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
