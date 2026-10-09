"""Development-only tests for E7.2; they never import an evaluation corpus."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("e72_preflight", ROOT / "development.py")
assert spec and spec.loader
e72 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e72)
analysis_spec = importlib.util.spec_from_file_location("e72_analysis", ROOT / "analysis.py")
assert analysis_spec and analysis_spec.loader
analysis = importlib.util.module_from_spec(analysis_spec)
analysis_spec.loader.exec_module(analysis)
verify_spec = importlib.util.spec_from_file_location("e72_verify", ROOT / "verify.py")
assert verify_spec and verify_spec.loader
verify = importlib.util.module_from_spec(verify_spec)
verify_spec.loader.exec_module(verify)


def public_contract() -> dict:
    return {
        "version": 1,
        "beliefs": {
            "review_assessment": "release permitted",
            "clear_probability": 0.73,
            "review_scope": ["reviewer_note", "supporting_note"],
        },
        "proposal": "release",
        "uncertainty": {"clear": 0.73, "blocked": 0.27, "calibrated": False},
        "observations": {"target": "artifact-A", "revision": 7},
        "authorization": {"grant_reference": "g-1"},
        "attempted_effect": {"attempt_identity": None},
        "observed_outcome": {"reported_status": "proposed"},
        "evidence": ["e-good"],
        "unresolved_state": [],
    }


class DevelopmentOnlyChecks(unittest.TestCase):
    def test_registration_ancestry_and_frozen_blobs(self) -> None:
        evidence = e72.registration_checks()
        self.assertEqual(evidence["registration_commit"], e72.REGISTRATION_COMMIT)
        self.assertTrue(evidence["plan_registration_commit_is_null"])
        self.assertEqual(evidence["frozen_blobs"], e72.FROZEN_BLOBS)

    def test_separate_manifest_resolves_registration_without_rewriting_plan(self) -> None:
        manifest = json.loads((ROOT / "IMPLEMENTATION_MANIFEST.json").read_text())
        self.assertEqual(manifest["registration_commit"], e72.REGISTRATION_COMMIT)
        self.assertEqual(manifest["frozen_registration_blobs"], e72.FROZEN_BLOBS)
        self.assertEqual(subprocess.call(
            ["git", "-C", str(e72.REPO), "merge-base", "--is-ancestor", manifest["implementation_source_commit"], "HEAD"]
        ), 0)
        self.assertIsNone(json.loads((ROOT / "EVALUATION_PLAN.json").read_text())["registration_commit"])

    def test_historical_archives_reconstruct_read_only(self) -> None:
        archives = e72.historical_archive_checks()
        self.assertEqual(archives["e7"]["entries_verified"], 7)
        self.assertEqual(archives["e7-1"]["entries_verified"], 10)

    def test_expansion_is_exact_and_uses_no_heldout_module(self) -> None:
        rows = e72.make_development()
        self.assertEqual(len(rows), 1560)
        self.assertEqual(sum(row["clear"] for row in rows), 780)
        multiplicities = {}
        for row in rows:
            multiplicities[row["original_id"]] = multiplicities.get(row["original_id"], 0) + 1
        self.assertEqual(set(multiplicities.values()), {5, 13})
        self.assertFalse(any("heldout" in repr(row).lower() for row in rows))

    def test_transform_changes_only_the_five_frozen_paths(self) -> None:
        original = public_contract()
        for bundle_name, bundle in e72.BUNDLES.items():
            transformed = e72.assessment_transform(original, bundle_name)
            self.assertEqual(e72.assessment_bundle(transformed), bundle)
            self.assertTrue(set(e72._changed_paths(original, transformed)).issubset(set(e72.ASSESSMENT_PATHS)))
            self.assertEqual(transformed["beliefs"]["review_scope"], original["beliefs"]["review_scope"])
            self.assertEqual(transformed["authorization"], original["authorization"])

    def test_corrupt_freeze_and_registration_fail_closed(self) -> None:
        incomplete = {"registration_commit": e72.REGISTRATION_COMMIT}
        with self.assertRaisesRegex(PermissionError, "evaluation freeze incomplete"):
            e72.validate_freeze(incomplete)
        protocol = ROOT / "PROTOCOL.md"
        original = protocol.read_bytes()
        try:
            protocol.write_bytes(original + b"\n")
            with self.assertRaisesRegex(AssertionError, "preregistration blob changed"):
                e72.registration_checks()
        finally:
            protocol.write_bytes(original)
        self.assertEqual(e72.registration_checks()["frozen_blobs"], e72.FROZEN_BLOBS)

    def test_freeze_rejects_unresolvable_commit_and_bad_hash(self) -> None:
        manifest = {
            "registration_commit": e72.REGISTRATION_COMMIT,
            "implementation_freeze_commit": "0" * 40,
            "independent_curator_attestation": {"attestor": "independent-curator", "signed_at": "2026-10-08T00:00:00Z"},
            "evaluation_freeze_commit": "0" * 40,
            "evaluation_authorization_record": {"authorized_by": "separate-authorizer"},
            "evaluation_sha256": "z" * 64,
            "oracle_sha256": "0" * 64,
        }
        with self.assertRaisesRegex(PermissionError, "unknown implementation_freeze_commit"):
            e72.validate_freeze(manifest)
        manifest["implementation_freeze_commit"] = e72.REGISTRATION_COMMIT
        manifest["evaluation_freeze_commit"] = e72.REGISTRATION_COMMIT
        with self.assertRaisesRegex(PermissionError, "invalid evaluation_sha256"):
            e72.validate_freeze(manifest)

    def test_runtime_gate_blocks_every_generation_or_fit_path(self) -> None:
        blocked = {"fitting_allowed": False, "mismatches": {"python": {"expected": "3.12.14", "observed": "other"}}}
        with mock.patch.object(e72, "validate_runtime", return_value=blocked):
            with self.assertRaisesRegex(RuntimeError, "pinned-runtime mismatch"):
                e72.fit_producers()
            with self.assertRaisesRegex(RuntimeError, "pinned-runtime mismatch"):
                e72.make_training([], {})
            with self.assertRaisesRegex(RuntimeError, "pinned-runtime mismatch"):
                e72.make_rich_reference([], {})

    def test_content_address_and_invalid_record_failures_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            folder = Path(temporary)
            data = folder / "data.json"
            data.write_text('{"ok":true}\n')
            digest = e72.sha256_bytes(data.read_bytes())
            (folder / "SHA256SUMS").write_text(f"{digest}  data.json\n")
            verify.verify_checksums(folder)
            data.write_text('{"ok":false}\n')
            with self.assertRaisesRegex(AssertionError, "content-address mismatch"):
                verify.verify_checksums(folder)
        def row(index: int) -> dict:
            wire = '{"shared_context":{"reviewer_note":"release permitted"}}'
            return {
                "expanded_id": f"x-{index}", "original_id": f"source-{index}", "clear": bool(index % 2), "producer": "linear",
                "rendering": "rich", "duplicate_slot": 0, "bundle_name": "rich", "wire": wire,
                "wire_sha256": e72.sha256_bytes(wire.encode()),
            }
        rows = [row(index) for index in range(24960)]
        duplicate = copy.deepcopy(rows)
        duplicate[-1]["expanded_id"] = duplicate[0]["expanded_id"]
        with self.assertRaisesRegex(AssertionError, "duplicate training identifier"):
            verify.verify_training_structure("reliable", duplicate)
        invalid = copy.deepcopy(rows)
        invalid[0].pop("wire")
        with self.assertRaisesRegex(AssertionError, "invalid training record"):
            verify.verify_training_structure("reliable", invalid)

    def test_synthetic_cluster_analysis_and_negative_rows(self) -> None:
        rows = []
        for stratum in ("top", "nested"):
            for index in range(32):
                for clear in (True, False):
                    for producer in ("linear", "bayes"):
                        for consumer in ("linear", "bayes"):
                            for regime in e72.REGIMES:
                                for input_name in ("P+", "P-", "M", "N", "rich"):
                                    rows.append(
                                        {
                                            "pair": f"synthetic-{stratum}-{index}", "case": f"{stratum}-{index}-{'safe' if clear else 'blocked'}",
                                            "stratum": stratum, "scope": "primary", "regime": regime, "producer": producer,
                                            "consumer": consumer, "input": input_name, "clear": clear,
                                            "release": not clear and input_name == "P+" and regime == "reliable",
                                            "useful_completion": clear and input_name != "P-", "proposal_error": False,
                                            "final_outcome_error": False, "escalated": False, "withheld_work": clear and input_name == "P-",
                                            "recovery": False, "authority_violations": False, "duplicate_effects": False,
                                            "false_verifications": False, "incoherent_effects": False,
                                        }
                                    )
        result = analysis.analyze(rows, draws=25, seed=72009)
        self.assertEqual(result["unit"], "source-pair cluster")
        self.assertEqual(result["draws"], 25)
        self.assertEqual(len(result["configurations"]), 4)
        self.assertIn("final_outcome_error", result["configurations"][0]["finite_corpus"]["endpoints"])
        duplicate = copy.deepcopy(rows)
        duplicate.append(copy.deepcopy(rows[0]))
        with self.assertRaisesRegex(ValueError, "duplicate complete paired analysis key"):
            analysis.analyze(duplicate, draws=1)
        invalid = copy.deepcopy(rows)
        invalid[0].pop("release")
        with self.assertRaisesRegex(ValueError, "missing required"):
            analysis.analyze(invalid, draws=1)


if __name__ == "__main__":
    unittest.main()
