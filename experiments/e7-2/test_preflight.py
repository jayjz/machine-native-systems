"""Development-only tests for E7.2; they never import an evaluation corpus."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
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

    def test_runtime_blocks_fitting_when_pins_do_not_match(self) -> None:
        report = e72.validate_runtime()
        self.assertFalse(report["fitting_allowed"])
        with self.assertRaisesRegex(RuntimeError, "pinned-runtime mismatch"):
            e72.fit_producers()

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
                "expanded_id": f"x-{index}", "clear": bool(index % 2), "producer": "linear",
                "rendering": "rich", "duplicate_slot": 0, "wire": wire,
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
            for index in range(2):
                for clear in (True, False):
                    for regime in e72.REGIMES:
                        for input_name in ("P+", "P-", "M", "N"):
                            rows.append(
                                {
                                    "pair": f"synthetic-{stratum}-{index}",
                                    "stratum": stratum,
                                    "regime": regime,
                                    "input": input_name,
                                    "clear": clear,
                                    "release": clear if input_name != "P+" else regime == "reliable",
                                    "useful_completion": clear and input_name != "P-",
                                }
                            )
        result = analysis.analyze(rows, draws=25, seed=72009)
        self.assertEqual(result["unit"], "source-pair cluster")
        self.assertEqual(result["draws"], 25)
        duplicate = copy.deepcopy(rows)
        duplicate.append(copy.deepcopy(rows[0]))
        with self.assertRaisesRegex(ValueError, "duplicate analysis intervention key"):
            analysis.analyze(duplicate, draws=1)
        invalid = copy.deepcopy(rows)
        invalid[0].pop("release")
        with self.assertRaisesRegex(ValueError, "missing required"):
            analysis.analyze(invalid, draws=1)


@unittest.skipUnless(importlib.util.find_spec("sklearn"), "requires installed scikit-learn for non-fitting wire preflight")
class WirePreflightChecks(unittest.TestCase):
    class _Producer:
        classes_ = [0, 1]

        def predict_proba(self, texts: list[str]) -> list[list[float]]:
            return [[0.1, 0.9] for _ in texts]

    def test_training_contingencies_wires_and_token_audit(self) -> None:
        # Stub producers exercise serialization only; no model is fitted.
        expanded = e72.make_development()
        producers = {family: self._Producer() for family in e72.FAMILIES}
        training = e72.make_training(expanded, producers)
        audit = e72.audit_training(training)
        transform = e72.audit_transform(training)
        self.assertTrue(audit["present_bundle_marginals_match"])
        self.assertTrue(all(value == 0.0 for value in audit["fallible_complete_bundle_mutual_information_bits"].values()))
        self.assertTrue(all(value == 0.5 for value in audit["fallible_bundle_only_lookup_accuracy"].values()))
        self.assertGreater(transform["masked_neutral_identity_groups"], 0)
        corrupted = copy.deepcopy(training)
        corrupted["fallible-complete-cross"][0]["wire"] += ' "clear_oracle":true'
        with self.assertRaisesRegex(AssertionError, "forbidden metadata"):
            e72.audit_training(corrupted)


if __name__ == "__main__":
    unittest.main()
