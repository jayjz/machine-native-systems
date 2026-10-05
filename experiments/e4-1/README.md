# E4.1 reproduction

Read PROTOCOL.md then RESULTS.md. Python 3.12.14, standard library; no models/network/cost.

```sh
python3 -m unittest discover -s experiments/e4-1 -p test_harness.py -v
python3 -m unittest discover -s experiments/e4-boundary -p test_harness.py -v
python3 experiments/e4-1/run.py --output experiments/e4-1/results/reproduction-001
```

Output must be new. Timing/platform may differ; semantic results are deterministic. configuration.json pins reused E4 source/fixtures and new source/protocol hashes; SHA256SUMS covers files and decompressed raw rows. checks.txt is the actual adapter test capture. Missing attempt's reserved sentinel is adapter state, never an actual receipt identifier. Full prior reports/raw files are preserved unchanged.
