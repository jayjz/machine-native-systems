"""Independent reconstruction of development-only E7.2 artifacts.

This module intentionally does not call the generator's audit functions and
does not contain an evaluation loader. It recomputes counts and statistical
properties from serialized records using separately defined constants.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

REGIMES = ("reliable", "fallible-complete-cross")
RENDERINGS = ("rich", "hybrid-present", "hybrid-masked", "hybrid-neutral")
FAMILIES = ("linear", "bayes")
FORBIDDEN_KEYS = {
    "id", "case", "source_id", "expanded_id", "original_id", "regime", "orientation",
    "clear", "clear_oracle", "semantic_oracle", "truth", "label", "producer_probability",
    "original_producer_probability", "assessment_correct", "assessment_present",
}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_checksums(folder: Path) -> None:
    manifest = folder / "SHA256SUMS"
    if not manifest.exists():
        raise FileNotFoundError("missing content-address manifest")
    seen: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        try:
            expected, name = line.split("  ", 1)
        except ValueError as error:
            raise AssertionError("malformed content-address manifest") from error
        if name in seen or len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            raise AssertionError("duplicate or invalid content-address manifest entry")
        seen.add(name)
        if name.endswith(" (decompressed)"):
            filename = name[: -len(" (decompressed)")] + ".gz"
            content = gzip.decompress((folder / filename).read_bytes())
        else:
            content = (folder / name).read_bytes()
        if _sha256(content) != expected:
            raise AssertionError(f"content-address mismatch: {name}")


def _read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]


def _wire_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(_wire_keys(item) for item in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(_wire_keys(item) for item in value)) if value else set()
    return set()


def _mutual_information(contingency: Counter[tuple[str, bool]]) -> float:
    total = sum(contingency.values())
    if total == 0:
        raise AssertionError("empty complete-bundle contingency")
    bundle_count = Counter({bundle: sum(value for (candidate, _), value in contingency.items() if candidate == bundle) for bundle, _ in contingency})
    truth_count = Counter({truth: sum(value for (_, candidate), value in contingency.items() if candidate == truth) for _, truth in contingency})
    return sum((value / total) * math.log2((value * total) / (bundle_count[bundle] * truth_count[truth])) for (bundle, truth), value in contingency.items() if value)


def _lookup_accuracy(contingency: Counter[tuple[str, bool]]) -> float:
    total = sum(contingency.values())
    return sum(max(contingency[(bundle, True)], contingency[(bundle, False)]) for bundle in {bundle for bundle, _ in contingency}) / total


def verify_training_structure(regime: str, rows: list[dict[str, Any]]) -> None:
    if regime not in REGIMES or len(rows) != 24960:
        raise AssertionError(f"{regime}: expected 24,960 training rows")
    required = {"expanded_id", "original_id", "clear", "producer", "rendering", "duplicate_slot", "bundle_name", "wire", "wire_sha256"}
    if any(not required.issubset(row) for row in rows):
        raise AssertionError(f"{regime}: invalid training record")
    keys = [(row["expanded_id"], row["producer"], row["rendering"], row["duplicate_slot"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError(f"{regime}: duplicate training identifier")
    labels = Counter(bool(row["clear"]) for row in rows)
    exposure = Counter(row["rendering"] for row in rows)
    source_exposure = Counter(row["expanded_id"] for row in rows)
    if labels != Counter({True: 12480, False: 12480}) or exposure != Counter({rendering: 6240 for rendering in RENDERINGS}) or set(source_exposure.values()) != {16}:
        raise AssertionError(f"{regime}: label, rendering, or source exposure invariant failed")
    for row in rows:
        wire = row["wire"].encode()
        if _sha256(wire) != row["wire_sha256"]:
            raise AssertionError(f"{regime}: mismatched wire hash")
        decoded = json.loads(row["wire"])
        leaked = FORBIDDEN_KEYS & _wire_keys(decoded)
        if leaked:
            raise AssertionError(f"{regime}: wire metadata leakage: {sorted(leaked)}")


def independent_training_audit(training: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    if set(training) != set(REGIMES):
        raise AssertionError("independent audit requires exactly two frozen regimes")
    for regime, rows in training.items():
        verify_training_structure(regime, rows)
    present = {regime: [row for row in rows if row["rendering"] == "hybrid-present"] for regime, rows in training.items()}
    histograms = {regime: Counter(tuple(row["bundle"] or ()) for row in rows) for regime, rows in present.items()}
    if histograms["reliable"] != histograms["fallible-complete-cross"]:
        raise AssertionError("independent audit: R/F present bundle marginals differ")
    mi: dict[str, float] = {}
    lookup: dict[str, float] = {}
    for producer in FAMILIES:
        rows = [row for row in present["fallible-complete-cross"] if row["producer"] == producer]
        contingency = Counter((row["bundle_name"], bool(row["clear"])) for row in rows)
        key = f"producer={producer};rendering=hybrid-present"
        mi[key] = _mutual_information(contingency)
        lookup[key] = _lookup_accuracy(contingency)
        if abs(mi[key]) > 1e-15 or abs(lookup[key] - 0.5) > 1e-15:
            raise AssertionError(f"independent audit: F nonidentifiability failed in {key}")
    for producer in FAMILIES:
        for original_id in {row["original_id"] for row in present["fallible-complete-cross"]}:
            group = [row for row in present["fallible-complete-cross"] if row["producer"] == producer and row["original_id"] == original_id]
            if Counter(row["bundle_name"] for row in group) != Counter({"positive": len(group) // 2, "negative": len(group) // 2}):
                raise AssertionError(f"independent audit: source crossing failed for {original_id}/{producer}")
    return {"present_bundle_marginals_match": True, "fallible_complete_bundle_mutual_information_bits": mi, "fallible_bundle_only_lookup_accuracy": lookup}


def verify(folder: Path) -> dict[str, Any]:
    verify_checksums(folder)
    environment = json.loads((folder / "environment.json").read_text())
    if not environment.get("fitting_allowed"):
        raise AssertionError("development artifact was produced without the pinned environment")
    training = {regime: _read_jsonl_gz(folder / f"training-{regime}.jsonl.gz") for regime in REGIMES}
    rich = _read_jsonl_gz(folder / "training-rich-reference.jsonl.gz")
    if len(rich) != 24960 or len({(row["expanded_id"], row["duplicate_slot"]) for row in rich}) != 24960:
        raise AssertionError("rich reference has invalid weighting or duplicate identifiers")
    audit = independent_training_audit(training)
    saved = json.loads((folder / "training-audit.json").read_text())
    for name, value in audit.items():
        if saved.get(name) != value:
            raise AssertionError(f"saved aggregate differs from independent reconstruction: {name}")
    return {"independent_training_audit": audit}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    print(json.dumps(verify(parser.parse_args().folder), sort_keys=True))
