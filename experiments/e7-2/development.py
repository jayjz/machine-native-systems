"""E7.2 development-only construction and preflight checks.

This module deliberately contains no evaluation-case generator or loader.  It
only expands the published E7 development corpus, constructs the stipulated
training wires, and provides checks which can be independently recomputed.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
REGISTRATION_COMMIT = "3420834c6a447b4fead476858c2f9fbb1c60dcbf"
FROZEN_BLOBS = {
    "experiments/e7-2/EVALUATION_PLAN.json": "dccf3fb6f778f6fed85b3340a08c7c32a7d7bc75",
    "experiments/e7-2/IMPLEMENTATION_CONTRACT.md": "b65929e66d098cef3977f90de99389311185ffad",
    "experiments/e7-2/METHODOLOGY.md": "0a89356120b18357ce1dcac1b28185f46308baec",
    "experiments/e7-2/PROTOCOL.md": "443771f2101339a16fcc35108dc2b33faa292b0f",
    "experiments/e7-2/README.md": "2981dce39e39926751a019ede31761470ceea793",
    "experiments/e7-2/VALIDATION.md": "7ad50f5b1cbeefda002af58b913bafc42af8c39e",
}
ASSESSMENT_PATHS = (
    ("beliefs", "review_assessment"),
    ("beliefs", "clear_probability"),
    ("proposal",),
    ("uncertainty", "clear"),
    ("uncertainty", "blocked"),
)
BUNDLES: dict[str, tuple[Any, ...]] = {
    "positive": ("release permitted", 0.9, "release", 0.9, 0.1),
    "negative": ("release blocked", 0.1, "withhold", 0.1, 0.9),
    "masked": (None, None, None, None, None),
    "neutral": ("neutral neutral", 0.5, "neutral", 0.5, 0.5),
}
REGIMES = ("reliable", "fallible-complete-cross")
RENDERINGS = ("rich", "hybrid-present", "hybrid-masked", "hybrid-neutral")
FAMILIES = ("linear", "bayes")
FORBIDDEN_WIRE_TERMS = (
    "expanded_id",
    "original_id",
    "source_id",
    "regime",
    "orientation",
    "clear_oracle",
    "semantic_oracle",
    "producer_probability",
    "truth",
    "label",
)
PINNED_VERSIONS = {
    "python": "3.12.14",
    "sklearn": "1.8.0",
    "numpy": "2.3.5",
    "scipy": "1.17.0",
    "joblib": "1.5.3",
    "threadpoolctl": "3.6.0",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import frozen dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def e7_development_module() -> Any:
    """Load only the old development-source definition, never heldout.py."""
    return _load_module("e72_e7_development", ROOT.parent / "e7" / "development.py")


def e7_runtime_module() -> Any:
    """Load E7 under a unique name only when model/rendering helpers are needed."""
    e7_root = str(ROOT.parent / "e7")
    if e7_root not in sys.path:
        sys.path.insert(0, e7_root)
    return _load_module("e72_e7_runtime", ROOT.parent / "e7" / "run.py")


def _get_path(value: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = value
    for key in path:
        current = current[key]
    return current


def _set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def assessment_bundle(contract: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(_get_path(contract, path) for path in ASSESSMENT_PATHS)


def assessment_transform(contract: dict[str, Any], bundle_name: str) -> dict[str, Any]:
    """Copy a public E7 contract and replace exactly the five frozen fields."""
    if bundle_name not in BUNDLES:
        raise ValueError(f"unknown E7.2 bundle: {bundle_name}")
    result = copy.deepcopy(contract)
    for path, replacement in zip(ASSESSMENT_PATHS, BUNDLES[bundle_name], strict=True):
        _set_path(result, path, replacement)
    changed = _changed_paths(contract, result)
    if not set(changed).issubset(set(ASSESSMENT_PATHS)):
        raise AssertionError(f"assessment transform modified non-frozen paths: {changed}")
    if assessment_bundle(result) != BUNDLES[bundle_name]:
        raise AssertionError("assessment transform did not serialize fixed literals")
    return result


def _changed_paths(before: Any, after: Any, prefix: tuple[str, ...] = ()) -> list[tuple[str, ...]]:
    if isinstance(before, dict) and isinstance(after, dict):
        paths: list[tuple[str, ...]] = []
        if set(before) != set(after):
            return [prefix]
        for key in before:
            paths.extend(_changed_paths(before[key], after[key], prefix + (key,)))
        return paths
    return [] if before == after else [prefix]


def make_development() -> list[dict[str, Any]]:
    """Expand the 216 E7 source records to the stipulated balanced corpus."""
    original = e7_development_module().development()
    if len(original) != 216 or sum(bool(row["clear"]) for row in original) != 60:
        raise AssertionError("E7 original development corpus no longer has 216 rows / 60 clear")
    expanded: list[dict[str, Any]] = []
    for row in sorted(original, key=lambda item: item["id"]):
        repeats = 13 if row["clear"] else 5
        for copy_slot in range(repeats):
            expanded.append(
                {
                    "expanded_id": f"{row['id']}-w{copy_slot:02d}",
                    "original_id": row["id"],
                    "copy_slot": copy_slot,
                    "clear": bool(row["clear"]),
                    "source": copy.deepcopy(row["source"]),
                }
            )
    if len(expanded) != 1560 or sum(row["clear"] for row in expanded) != 780:
        raise AssertionError("E7.2 expansion must contain 780 clear and 780 blocked rows")
    counts = Counter(row["original_id"] for row in expanded)
    expected = {row["id"]: 13 if row["clear"] else 5 for row in original}
    if counts != expected:
        raise AssertionError("E7.2 expansion multiplicities drifted")
    return expanded


def validate_runtime() -> dict[str, Any]:
    """Return a strict pin report; callers must not fit when it is not allowed."""
    observed: dict[str, str] = {"python": platform.python_version()}
    try:
        import joblib
        import numpy
        import scipy
        import sklearn
        import threadpoolctl

        observed.update(
            sklearn=sklearn.__version__,
            numpy=numpy.__version__,
            scipy=scipy.__version__,
            joblib=joblib.__version__,
            threadpoolctl=threadpoolctl.__version__,
        )
    except ImportError as error:
        observed["import_error"] = str(error)
    mismatches = {
        name: {"expected": version, "observed": observed.get(name)}
        for name, version in PINNED_VERSIONS.items()
        if observed.get(name) != version
    }
    return {
        "pinned": PINNED_VERSIONS,
        "observed": observed,
        # A basename preserves reproducibility-relevant executable identity
        # without publishing a local user-directory path in this public repo.
        "python_executable": Path(sys.executable).name,
        "fitting_allowed": not mismatches,
        "mismatches": mismatches,
    }


def _require_pinned_runtime() -> Any:
    report = validate_runtime()
    if not report["fitting_allowed"]:
        raise RuntimeError(f"E7.2 fitting blocked by pinned-runtime mismatch: {report['mismatches']}")
    return e7_runtime_module()


def fit_producers() -> tuple[Any, dict[str, Any]]:
    """Fit original E7 producers and reject any state that differs from the archive."""
    e7 = _require_pinned_runtime()
    original = e7_development_module().development()
    texts = [e7.review(row["source"]) for row in original]
    labels = [int(row["clear"]) for row in original]
    producers = {family: e7.model(family).fit(texts, labels) for family in FAMILIES}
    states = {family: e7.state(model) for family, model in producers.items()}
    archived = json.loads((ROOT.parent / "e7" / "results" / "run-001" / "model-state.json").read_text())
    if states != archived["producer"]:
        raise AssertionError("E7.2 producer state does not byte-semantically reproduce archived E7 producer")
    return e7, producers


def _render_training_row(
    e7: Any,
    record: dict[str, Any],
    regime: str,
    producer: str,
    rendering: str,
    duplicate_slot: int,
    producers: dict[str, Any],
) -> dict[str, Any]:
    case = {"id": record["original_id"], "source": record["source"], "world": {}}
    _, original_contract, producer_probability = e7.public(case, producers[producer])
    if rendering == "rich":
        transformed = original_contract
        wire, requests, exceeded = e7.boundary(case, transformed, "rich")
        bundle_name = "rich"
        orientation = "none"
    else:
        if rendering == "hybrid-masked":
            bundle_name, orientation = "masked", "none"
        elif rendering == "hybrid-neutral":
            bundle_name, orientation = "neutral", "none"
        elif regime == "reliable":
            # Historical E7 producer scores establish the original orientation;
            # only the transmitted value is replaced by a frozen literal.
            bundle_name = "positive" if producer_probability >= 0.5 else "negative"
            orientation = "actual"
            if (bundle_name == "positive") != bool(record["clear"]):
                raise AssertionError("historical E7 producer cannot supply a reliable development orientation")
        elif regime == "fallible-complete-cross":
            bundle_name = "positive" if duplicate_slot == 0 else "negative"
            orientation = bundle_name
        else:
            raise ValueError(f"unknown regime: {regime}")
        transformed = assessment_transform(original_contract, bundle_name)
        wire, requests, exceeded = e7.boundary(case, transformed, "hybrid")
    if requests or exceeded:
        raise AssertionError("E7.2 development render unexpectedly requested context")
    _assert_wire_isolated(wire)
    return {
        "expanded_id": record["expanded_id"],
        "original_id": record["original_id"],
        "source_copy_slot": record["copy_slot"],
        "clear": record["clear"],
        "regime": regime,
        "producer": producer,
        "rendering": rendering,
        "duplicate_slot": duplicate_slot,
        "orientation": orientation,
        "bundle_name": bundle_name,
        "bundle": list(assessment_bundle(transformed)) if bundle_name != "rich" else None,
        "source_sha256": sha256_bytes(canonical(record["source"]).encode()),
        "original_producer_probability": producer_probability,
        "wire": wire,
        "wire_sha256": sha256_bytes(wire.encode()),
    }


def _assert_wire_isolated(wire: str) -> None:
    try:
        decoded = json.loads(wire)
    except json.JSONDecodeError as error:
        raise AssertionError("consumer wire is not canonical JSON") from error

    def keys(value: Any) -> set[str]:
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(item) for item in value.values())) if value else set()
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value)) if value else set()
        return set()

    forbidden_keys = {
        "id", "case", "source_id", "expanded_id", "original_id", "regime", "orientation",
        "clear", "clear_oracle", "semantic_oracle", "truth", "label", "producer_probability",
        "original_producer_probability", "assessment_correct", "assessment_present",
    }
    observed_keys = keys(decoded)
    if forbidden_keys & observed_keys:
        raise AssertionError(f"consumer wire contains forbidden metadata keys: {sorted(forbidden_keys & observed_keys)}")
    lowered = wire.lower()
    leaked = [term for term in FORBIDDEN_WIRE_TERMS if term in lowered]
    if leaked:
        raise AssertionError(f"consumer wire contains forbidden metadata: {leaked}")


def make_training(expanded: list[dict[str, Any]], producers: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Produce deterministic 24,960-row training datasets for R and F."""
    e7 = e7_runtime_module()
    rows: dict[str, list[dict[str, Any]]] = {regime: [] for regime in REGIMES}
    for regime in REGIMES:
        for record in expanded:
            for producer in FAMILIES:
                for rendering in RENDERINGS:
                    for duplicate_slot in range(2):
                        rows[regime].append(
                            _render_training_row(
                                e7, record, regime, producer, rendering, duplicate_slot, producers
                            )
                        )
        if len(rows[regime]) != 24960:
            raise AssertionError(f"{regime} has {len(rows[regime])}, expected 24960")
    return rows


def make_rich_reference(expanded: list[dict[str, Any]], producers: dict[str, Any]) -> list[dict[str, Any]]:
    """Create the one rich-only, 16-times-weighted capacity reference corpus."""
    e7 = e7_runtime_module()
    rows: list[dict[str, Any]] = []
    for record in expanded:
        case = {"id": record["original_id"], "source": record["source"], "world": {}}
        # E7 rich rendering ignores the contract.  Keep its producer field out of the fit rows.
        _, contract, _ = e7.public(case, producers["linear"])
        wire, requests, exceeded = e7.boundary(case, contract, "rich")
        if requests or exceeded:
            raise AssertionError("rich capacity reference unexpectedly requested context")
        _assert_wire_isolated(wire)
        for duplicate_slot in range(16):
            rows.append(
                {
                    "expanded_id": record["expanded_id"],
                    "original_id": record["original_id"],
                    "source_copy_slot": record["copy_slot"],
                    "clear": record["clear"],
                    "rendering": "rich-reference",
                    "duplicate_slot": duplicate_slot,
                    "source_sha256": sha256_bytes(canonical(record["source"]).encode()),
                    "wire": wire,
                    "wire_sha256": sha256_bytes(wire.encode()),
                }
            )
    if len(rows) != 24960:
        raise AssertionError("rich reference must contain exactly 24,960 rows")
    return rows


def fit_consumers(training: Iterable[dict[str, Any]]) -> dict[str, Any]:
    e7 = _require_pinned_runtime()
    rows = list(training)
    if len(rows) != 24960:
        raise ValueError("consumer fitting requires exactly one complete E7.2 mixed regime")
    return {family: e7.model(family).fit([r["wire"] for r in rows], [int(r["clear"]) for r in rows]) for family in FAMILIES}


def fit_rich_reference(training: Iterable[dict[str, Any]]) -> dict[str, Any]:
    e7 = _require_pinned_runtime()
    rows = list(training)
    if len(rows) != 24960:
        raise ValueError("rich reference fitting requires exactly 24,960 rows")
    return {family: e7.model(family).fit([r["wire"] for r in rows], [int(r["clear"]) for r in rows]) for family in FAMILIES}


def _mutual_information(contingency: Counter[tuple[str, bool]]) -> float:
    total = sum(contingency.values())
    if not total:
        raise ValueError("empty contingency")
    bundles = Counter({bundle: sum(v for (b, _), v in contingency.items() if b == bundle) for bundle, _ in contingency})
    truths = Counter({truth: sum(v for (_, t), v in contingency.items() if t == truth) for _, truth in contingency})
    information = 0.0
    for (bundle, truth), observed in contingency.items():
        if observed:
            probability = observed / total
            information += probability * math.log2((observed * total) / (bundles[bundle] * truths[truth]))
    return information


def _bundle_lookup_accuracy(contingency: Counter[tuple[str, bool]]) -> float:
    total = sum(contingency.values())
    return sum(max(contingency[(bundle, True)], contingency[(bundle, False)]) for bundle in {key[0] for key in contingency}) / total


def audit_training(training_by_regime: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Mechanically audit the exact balance, isolation and nonidentifiability contract."""
    if set(training_by_regime) != set(REGIMES):
        raise ValueError("audit requires the reliable and fallible-complete-cross regimes")
    report: dict[str, Any] = {"regimes": {}}
    present_histograms: dict[str, Counter[Any]] = {}
    field_histograms: dict[str, list[Counter[Any]]] = {}
    for regime, rows in training_by_regime.items():
        if len(rows) != 24960:
            raise AssertionError(f"{regime}: row count is not 24,960")
        labels = Counter(bool(row["clear"]) for row in rows)
        exposure = Counter(row["rendering"] for row in rows)
        source_exposure = Counter(row["expanded_id"] for row in rows)
        present = [row for row in rows if row["rendering"] == "hybrid-present"]
        contingency = Counter((row["bundle_name"], bool(row["clear"])) for row in present)
        present_histograms[regime] = Counter(tuple(row["bundle"] or ()) for row in present)
        field_histograms[regime] = [Counter((row["bundle"] or [])[index] for row in present) for index in range(5)]
        if labels != Counter({True: 12480, False: 12480}):
            raise AssertionError(f"{regime}: training labels are not balanced")
        if exposure != Counter({rendering: 6240 for rendering in RENDERINGS}):
            raise AssertionError(f"{regime}: rendering exposure is not equal")
        if set(source_exposure.values()) != {16}:
            raise AssertionError(f"{regime}: source multiplicity is not exactly sixteen wires")
        report["regimes"][regime] = {
            "rows": len(rows),
            "labels": {str(key): value for key, value in sorted(labels.items())},
            "rendering_exposure": dict(sorted(exposure.items())),
            "source_wire_multiplicity": sorted(set(source_exposure.values())),
            "present_bundle_truth": {f"{bundle}|{truth}": count for (bundle, truth), count in sorted(contingency.items())},
        }
        for row in rows:
            _assert_wire_isolated(row["wire"])
    if present_histograms["reliable"] != present_histograms["fallible-complete-cross"]:
        raise AssertionError("R/F complete present-bundle marginals differ")
    if field_histograms["reliable"] != field_histograms["fallible-complete-cross"]:
        raise AssertionError("R/F present confidence or field marginals differ")
    fallible = training_by_regime["fallible-complete-cross"]
    fallible_present = [row for row in fallible if row["rendering"] == "hybrid-present"]
    strata: dict[str, float] = {}
    accuracies: dict[str, float] = {}
    for producer in FAMILIES:
        for rendering in ("hybrid-present",):
            group = [row for row in fallible_present if row["producer"] == producer and row["rendering"] == rendering]
            contingency = Counter((row["bundle_name"], bool(row["clear"])) for row in group)
            key = f"producer={producer};rendering={rendering}"
            strata[key] = _mutual_information(contingency)
            accuracies[key] = _bundle_lookup_accuracy(contingency)
            if abs(strata[key]) > 1e-15 or abs(accuracies[key] - 0.5) > 1e-15:
                raise AssertionError(f"F bundle nonidentifiability failed in {key}")
    for original_id in {row["original_id"] for row in fallible_present}:
        for producer in FAMILIES:
            group = [row for row in fallible_present if row["original_id"] == original_id and row["producer"] == producer]
            if Counter(row["bundle_name"] for row in group) != Counter({"positive": len(group) // 2, "negative": len(group) // 2}):
                raise AssertionError(f"F did not exactly cross bundles for {original_id}/{producer}")
    report["fallible_complete_bundle_mutual_information_bits"] = strata
    report["fallible_bundle_only_lookup_accuracy"] = accuracies
    report["present_bundle_marginals_match"] = True
    report["present_field_marginals_match"] = True
    return report


def audit_transform(training_by_regime: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Check token eligibility, nonbundle equality and masked/neutral orientation identity."""
    try:
        from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    except ImportError as error:
        raise RuntimeError("tokenizer audit requires the pinned scikit-learn environment") from error
    analyzers = {
        "linear": TfidfVectorizer(ngram_range=(1, 2)).build_analyzer(),
        "bayes": CountVectorizer(ngram_range=(1, 1)).build_analyzer(),
    }
    token_counts: dict[str, dict[str, int]] = {}
    for family, analyzer in analyzers.items():
        token_counts[family] = {
            name: sum(len(analyzer(str(value))) for value in bundle[:3] if isinstance(value, str))
            for name, bundle in BUNDLES.items()
            if name in ("positive", "negative", "neutral")
        }
        if token_counts[family]["positive"] != token_counts[family]["neutral"] or token_counts[family]["negative"] != token_counts[family]["neutral"]:
            raise AssertionError(f"P/N token eligibility mismatch for {family}")
    identities = 0
    for regime, rows in training_by_regime.items():
        grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            if row["rendering"] in ("hybrid-masked", "hybrid-neutral"):
                grouped[(regime, row["expanded_id"], row["producer"], row["rendering"])].append(row)
        for key, group in grouped.items():
            if len({row["wire_sha256"] for row in group}) != 1:
                raise AssertionError(f"M/N wires vary by duplicate/orientation: {key}")
            identities += 1
    return {"eligible_word_tokens": token_counts, "masked_neutral_identity_groups": identities}


def registration_checks(repo: Path = REPO, implementation_commit: str | None = None) -> dict[str, Any]:
    """Check immutable registration ancestry and byte-identical preregistration blobs."""
    def git(*arguments: str) -> str:
        return subprocess.check_output(["git", "-C", str(repo), *arguments], text=True).strip()

    git("cat-file", "-e", REGISTRATION_COMMIT)
    if subprocess.call(["git", "-C", str(repo), "merge-base", "--is-ancestor", REGISTRATION_COMMIT, "HEAD"]) != 0:
        raise AssertionError("registration commit is not an ancestor of implementation HEAD")
    current_blobs: dict[str, str] = {}
    for relative, expected_blob in FROZEN_BLOBS.items():
        registration_blob = git("rev-parse", f"{REGISTRATION_COMMIT}:{relative}")
        working_blob = git("hash-object", relative)
        if registration_blob != expected_blob or working_blob != expected_blob:
            raise AssertionError(f"preregistration blob changed: {relative}")
        current_blobs[relative] = working_blob
    plan = json.loads((repo / "experiments" / "e7-2" / "EVALUATION_PLAN.json").read_text())
    if plan["registration_commit"] is not None:
        raise AssertionError("frozen EVALUATION_PLAN registration_commit must remain null")
    return {
        "registration_commit": REGISTRATION_COMMIT,
        "implementation_commit": implementation_commit,
        "frozen_blobs": current_blobs,
        "plan_registration_commit_is_null": True,
    }


def historical_archive_checks() -> dict[str, Any]:
    """Read-only checksum reconstruction for the E7 and E7.1 published archives."""
    result: dict[str, Any] = {}
    for experiment in ("e7", "e7-1"):
        relative_folder = f"experiments/{experiment}/results/run-001"
        manifest_relative = f"{relative_folder}/SHA256SUMS"
        manifest = subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{REGISTRATION_COMMIT}:{manifest_relative}"]
        )
        verified = 0
        for line in manifest.decode().splitlines():
            expected, name = line.split("  ", 1)
            if name.endswith(" (decompressed)"):
                compressed = subprocess.check_output(
                    ["git", "-C", str(REPO), "show", f"{REGISTRATION_COMMIT}:{relative_folder}/{name[: -len(' (decompressed)')]}.gz"]
                )
                content = __import__("gzip").decompress(compressed)
            else:
                content = subprocess.check_output(
                    ["git", "-C", str(REPO), "show", f"{REGISTRATION_COMMIT}:{relative_folder}/{name}"]
                )
            if sha256_bytes(content) != expected:
                raise AssertionError(f"historical {experiment} archive hash mismatch: {name}")
            registered_blob = subprocess.check_output(
                ["git", "-C", str(REPO), "rev-parse", f"{REGISTRATION_COMMIT}:{relative_folder}/{name if not name.endswith(' (decompressed)') else name[: -len(' (decompressed)')] + '.gz'}"], text=True
            ).strip()
            head_blob = subprocess.check_output(
                ["git", "-C", str(REPO), "rev-parse", f"HEAD:{relative_folder}/{name if not name.endswith(' (decompressed)') else name[: -len(' (decompressed)')] + '.gz'}"], text=True
            ).strip()
            if registered_blob != head_blob:
                raise AssertionError(f"historical {experiment} artifact changed in implementation tree: {name}")
            verified += 1
        result[experiment] = {"manifest_sha256": sha256_bytes(manifest), "entries_verified": verified}
    return result


def validate_freeze(manifest: dict[str, Any]) -> None:
    """Fail closed; this verifies pins only and never opens an evaluation corpus."""
    required = (
        "registration_commit",
        "implementation_freeze_commit",
        "independent_curator_attestation",
        "evaluation_freeze_commit",
        "evaluation_authorization_record",
        "evaluation_sha256",
        "oracle_sha256",
    )
    missing = [field for field in required if not manifest.get(field)]
    if missing:
        raise PermissionError(f"evaluation freeze incomplete; refusing to load evaluation: {', '.join(missing)}")
    if manifest["registration_commit"] != REGISTRATION_COMMIT:
        raise PermissionError("evaluation manifest does not cite the immutable E7.2 registration")


def environment_manifest() -> dict[str, Any]:
    """Serializable environment evidence; it does not authorize fitting on mismatch."""
    report = validate_runtime()
    report.update(
        os=platform.platform(),
        registration_commit=REGISTRATION_COMMIT,
        source_sha256={
            str(path.relative_to(REPO)): sha256_bytes(path.read_bytes())
            for path in (ROOT / "development.py", ROOT / "analysis.py", ROOT / "verify.py", ROOT / "run_development.py")
            if path.exists()
        },
    )
    return report
