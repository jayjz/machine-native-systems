# E7.1 validation/provenance

Exact base: remote E7 tip `bf1003f3fdde28c3d518f661ce45aa8a42c08cdd`. Protocol: `89970c2c8dc9e2374b056d33d7b47a394af5e7c8`, parent is that exact tip. It was published BEFORE implementation/evaluation creation. Local prepublication protocol snapshot `40657741f93a1fbbbad55aba020d24ba5fa5745f` retained; canonical protocol tree identical. Implementation/evaluation freeze local `ab1378ec9f51885504d09e8a031f9dfd1083bb7b` directly descends from canonical protocol. configuration.json records evaluated commit and source hashes before/after. Evaluation creation happened after protocol; not independently blind design.

Passed: 5 preflight checks, full refit/replay of 7,680 outputs with exact fitted/training states and all non-timing fields, read-only checksum/source/aggregate/causal reconstruction. Original E4 five checks, E4.1 three checks, E7 five checks and all original archive checks passed. Prior experiment directories/imported research remain byte-identical. No schema/model/threshold/oracle/case repair after execution. No external research.

An initial NEW reproduction test discovery failed due to E7 reuse inserting its path and shadowing the filename; actual traceback preserved in reproduction-discovery-failure.txt. Renamed only the new postrun test to test_e71_reproduction.py and restored discovery path. Evaluated source/data stayed unchanged; actual passing output preserved in reproduction-checks.txt. README's planned test_reproduction.py refers to this uniquely named new test. This is a validation-tool correction, not a model/experiment deviation.

```sh
python3 experiments/e7-1/verify.py
python3 -m unittest discover -s experiments/e7-1 -p 'test_*.py' -v
python3 experiments/verify_results.py
python3 -m unittest discover -s experiments/e4-boundary -p test_harness.py -v
python3 -m unittest discover -s experiments/e4-1 -p test_harness.py -v
python3 -m unittest discover -s experiments/e7 -p 'test_*.py' -v
```

New-artifact credential-pattern scan includes decompressed raw/model/training archives; only synthetic data, model parameters and nonsecret execution-version metadata. Pattern scanning is not universal secret detection. Git object/tree identity, protocol/results ancestry, clean state, unchanged remote main/E4/E7 tips and pushed research branch are checked at publication. No PR or merge. Remote publication mappings are recorded in a later additive PUBLICATION.json; prior protocol/results files remain frozen.
