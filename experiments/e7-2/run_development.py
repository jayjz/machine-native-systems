"""Run the E7.2 development-only fit after the exact pinned environment is present.

There is intentionally no evaluation import, loader, or CLI option in this
file.  A successful run prepares auditable development artifacts only.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import subprocess
from pathlib import Path

import development as e72


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def _write_jsonl_gz(path: Path, rows: list[dict]) -> None:
    payload = "".join(e72.canonical(row) + "\n" for row in rows).encode()
    path.write_bytes(gzip.compress(payload, mtime=0))


def _archive(folder: Path) -> None:
    entries: list[str] = []
    for path in sorted(folder.iterdir()):
        if path.name == "SHA256SUMS":
            continue
        entries.append(f"{e72.sha256_bytes(path.read_bytes())}  {path.name}")
        if path.suffix == ".gz":
            entries.append(f"{e72.sha256_bytes(gzip.decompress(path.read_bytes()))}  {path.stem} (decompressed)")
    (folder / "SHA256SUMS").write_text("\n".join(entries) + "\n")


def preflight(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    report = e72.environment_manifest()
    _write_json(output / "environment.json", report)
    _write_json(output / "registration.json", e72.registration_checks())
    _archive(output)
    return report


def run(output: Path) -> None:
    report = e72.validate_runtime()
    if not report["fitting_allowed"]:
        raise RuntimeError(f"refusing development fit: {report['mismatches']}")
    # These process-level limits are set before fitting and recorded below.
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name] = "1"
    import threadpoolctl

    output.mkdir(parents=True, exist_ok=False)
    with threadpoolctl.threadpool_limits(limits=1):
        e7, producers = e72.fit_producers()
        expanded = e72.make_development()
        training = e72.make_training(expanded, producers)
        rich_reference = e72.make_rich_reference(expanded, producers)
        training_audit = e72.audit_training(training)
        transform_audit = e72.audit_transform(training)
        consumers = {regime: e72.fit_consumers(rows) for regime, rows in training.items()}
        rich_models = e72.fit_rich_reference(rich_reference)
        states = {
            "producer": {family: e7.state(model) for family, model in producers.items()},
            "consumer": {
                regime: {family: e7.state(model) for family, model in models.items()}
                for regime, models in consumers.items()
            },
            "rich_reference": {family: e7.state(model) for family, model in rich_models.items()},
        }
        threadpools = threadpoolctl.threadpool_info()
    _write_json(output / "development.json", expanded)
    for regime, rows in training.items():
        _write_jsonl_gz(output / f"training-{regime}.jsonl.gz", rows)
    _write_jsonl_gz(output / "training-rich-reference.jsonl.gz", rich_reference)
    _write_json(output / "model-state.json", states)
    _write_json(output / "training-audit.json", training_audit)
    _write_json(output / "transform-audit.json", transform_audit)
    commit = subprocess.check_output(["git", "-C", str(e72.REPO), "rev-parse", "HEAD"], text=True).strip()
    _write_json(output / "registration.json", e72.registration_checks(implementation_commit=commit))
    environment = e72.environment_manifest()
    environment.update(threadpool_environment={name: os.environ[name] for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")}, threadpools=threadpools)
    _write_json(output / "environment.json", environment)
    _archive(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        result = preflight(args.output)
        print(json.dumps({"fitting_allowed": result["fitting_allowed"], "mismatches": result["mismatches"]}, sort_keys=True))
        return
    run(args.output)


if __name__ == "__main__":
    main()
