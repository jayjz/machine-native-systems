# E4.1/E7 final validation — October 4, 2026

Canonical ancestry: main `760697b40d2946647a5a69301f4ad34bfc07e2e8` → prior E4 → `dffa582a3fe7f2445617e22a87d4c7ed2c0ea480` → new research work. Remote compare to E4 reports ahead=4, behind=0 before this validation commit. Main remains at its original SHA. GitHub connector publishes exact local trees with every changed blob SHA verified. Actual remote commit objects were imported with SHA verification to align the local branch; prepublication local snapshots retained separately. No main merge.

| Local prepublication snapshot | Canonical GitHub commit |
|---|---|
| E4.1 protocol `7ea4dc42e7f8411db3d4f25ba4396d7a49d1d1b4` | `c7001883785f36700f4f54d92575b7e9938c2881` |
| E4.1 results `5cbca6cc5e48313dc171c9ba913c5de7c5156d0f` | `cb8f31b3cdf22d1a10f65bd378386f6d3ab20a43` |
| E7 interface/development freeze `99120495fcf8118d98b106c9be3315cb3ff035a8` | `3f71d3af894231431ba369053d609aea943e3e4c` |
| E7 code/results `8d70c51e1e484d90382475702b2cf892fe3bfce5` | `b3eea1701c4b922515f2cfecd6b9a0e00bb2df7d` |

Protocols were committed locally before execution. GitHub publication follows execution; do not call these externally timestamped preregistrations. Frozen protocol hashes remain in configuration files. No original reports or E4 files revised.

## Passed checks

- E4 five trust/fixture checks; E4.1 three adapter/default checks.
- E7 four boundary/budget checks plus full deterministic reproduction: refit models, compare fitted parameters and development/heldout datasets, regenerate all 640 wires/requests, reproduce probabilities/actions and final effects/receipts. Actual output: e7/reproduction-checks.txt.
- Compressed/decompressed hashes and recomputed aggregates: E4 640 rows, E4.1 5280, E7 640; unique factorial keys and new source hashes verified by verify_results.py.
- Git ancestry, complete object integrity, original E4/research/AGENTS/README preservation, whitespace and new-artifact credential-pattern checks. Pattern scanning is not universal secret detection. New data/model states are synthetic; no credentials/private prompt/memory payloads used.

E4.1 minor implementation-order annotation: defaults are inserted before E4's shared decoder validates versions, rather than after validation as protocol wording says. Rejected messages cannot reach the consumer; no authority/effect or accepted-state change. Preserve the protocol rather than silently edit it. E7's substantive inventory-before-first-inference deviation is documented in RESULTS; no learned clarification policy tested.

## Reproduce checks from root

```sh
python3 experiments/verify_results.py
python3 -m unittest discover -s experiments/e4-boundary -p test_harness.py -v
python3 -m unittest discover -s experiments/e4-1 -p test_harness.py -v
python3 -m unittest discover -s experiments/e7 -p 'test_*.py' -v
```

Pinned E7 requirements and separate README run commands/configuration limits are committed. Reproduction does not tune on failures. Research branch only, no product framework or external literature retrieval.

## E7.1 additive validation — October 4, 2026

Prior validation above is preserved unchanged. New branch starts from exact canonical E7 tip bf1003f3fdde28c3d518f661ce45aa8a42c08cdd. Protocol89970c2c8dc9e2374b056d33d7b47a394af5e7c8 published before evaluation creation/execution. [E7.1 validation](e7-1/VALIDATION.md) records full7,680-output reproduction, unchanged prior evidence, raw integrity, test-discovery correction and publication mappings. No PR/main merge or prior commit/artifact modification.
