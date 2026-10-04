"""Checks trust boundaries and fixture integrity, not thesis success."""
import copy
import json
import unittest

import run


class BoundaryChecks(unittest.TestCase):
    def test_effect_gate_cannot_be_bypassed_by_consumer(self):
        world = run.World({"id": "gate-test"})
        with self.assertRaises(PermissionError):
            world.execute("g-forged", "artifact-A", "sha256:A", "attack")
        self.assertEqual(world.effects, [])

    def test_execution_idempotency_survives_consumer_replacement(self):
        world = run.World({"id": "repeat"})
        public = run.producer({"id": "repeat"}, "predicates")
        first = run.consume(copy.deepcopy(public), world)
        second = run.consume(copy.deepcopy(public), world)
        self.assertEqual(first, second)
        self.assertEqual(len(world.effects), 1)

    def test_claim_alone_cannot_be_verified(self):
        world = run.World({"id": "claim"})
        public = run.producer({"id": "claim", "status": "completed"}, "graph")
        result = run.consume(public, world)
        self.assertFalse(result["verified"])
        self.assertFalse(run.independently_verified(world, public))
        self.assertEqual(world.effects, [])

    def test_receipt_for_another_artifact_is_not_proof(self):
        public = run.producer({"id": "foreign", "attempt": "other-attempt",
                               "receipt": "r-foreign", "status": "completed"}, "graph")
        result = run.consume(public, run.World({"id": "foreign"}))
        self.assertEqual(result["outcome"], "unresolved")
        self.assertFalse(result["verified"])

    def test_fixture_ids_unique_and_producer_private_state_not_transmitted(self):
        cases = json.loads((run.ROOT / "fixtures.json").read_text())["cases"]
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        for case in cases:
            a, b = (run.producer(case, kind) for kind in run.PRODUCERS)
            self.assertEqual(a, b)
            self.assertEqual(set(a), set(run.FIELDS))


if __name__ == "__main__":
    unittest.main()
