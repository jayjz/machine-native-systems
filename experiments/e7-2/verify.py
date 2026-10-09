"""Independent reconstruction of development-only E7.2 artifacts.

This verifier does not know how to load a heldout corpus and refuses to infer
or repair any missing artifact.  It consumes saved development records only.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

import development as e72


def verify_checksums(folder: Path) -> None:
    manifest = folder / "SHA256SUMS"
    if not manifest.exists():
        raise FileNotFoundError("missing content-address manifest")
    for line in manifest.read_text().splitlines():
        expected, name = line.split("  ", 1)
        if name.endswith(" (decompressed)"):
            filename = name[: -len(" (decompressed)")] + ".gz"
            content = gzip.decompress((folder / filename).read_bytes())
        else:
            content = (folder / name).read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        if actual != expected:
            raise AssertionError(f"content-address mismatch: {name}")


def _read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]


def verify_training_structure(regime: str, rows: list[dict[str, Any]]) -> None:
    if len(rows) != 24960:
        raise AssertionError(f"{regime}: expected 24,960 training rows")
    required = {"expanded_id", "clear", "producer", "rendering", "duplicate_slot", "wire", "wire_sha256"}
    if any(not required.issubset(row) for row in rows):
        raise AssertionError(f"{regime}: invalid training record")
    keys = [(row["expanded_id"], row["producer"], row["rendering"], row["duplicate_slot"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError(f"{regime}: duplicate training identifier")
    for row in rows:
        if e72.sha256_bytes(row["wire"].encode()) != row["wire_sha256"]:
            raise AssertionError(f"{regime}: mismatched wire hash")
        e72._assert_wire_isolated(row["wire"])


def verify(folder: Path) -> dict[str, Any]:
    verify_checksums(folder)
    registration = json.loads((folder / "registration.json").read_text())
    e72.registration_checks(implementation_commit=registration.get("implementation_commit"))
    environment = json.loads((folder / "environment.json").read_text())
    if not environment.get("fitting_allowed"):
        raise AssertionError("development artifact was produced without the pinned environment")
    training = {
        regime: _read_jsonl_gz(folder / f"training-{regime}.jsonl.gz") for regime in e72.REGIMES
    }
    for regime, rows in training.items():
        verify_training_structure(regime, rows)
    rich = _read_jsonl_gz(folder / "training-rich-reference.jsonl.gz")
    if len(rich) != 24960 or len({(row["expanded_id"], row["duplicate_slot"]) for row in rich}) != 24960:
        raise AssertionError("rich reference has invalid weighting or duplicate identifiers")
    audit = e72.audit_training(training)
    transform = e72.audit_transform(training)
    saved_audit = json.loads((folder / "training-audit.json").read_text())
    saved_transform = json.loads((folder / "transform-audit.json").read_text())
    if audit != saved_audit or transform != saved_transform:
        raise AssertionError("saved aggregate differs from independent reconstruction")
    return {"training_audit": audit, "transform_audit": transform}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    print(json.dumps(verify(parser.parse_args().folder), sort_keys=True))
