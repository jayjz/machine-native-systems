# E4 boundary experiment

Read [PROTOCOL.md](PROTOCOL.md) before [RESULTS.md](RESULTS.md). This is a finite synthetic artifact-release experiment, not an agent framework. Existing literature/provenance remains in the root research index.

Python 3.12.14, standard library only. No package installation, model key, GPU, network, or paid inference is needed.

From the repository root:

```sh
python3 -m unittest discover -s experiments/e4-boundary -p 'test_harness.py' -v
python3 experiments/e4-boundary/run.py --output experiments/e4-boundary/results/reproduction-001
```

The output directory must not already exist, preventing accidental overwrite of raw results. Decisions and outcomes are deterministic; timestamps/latencies and platform configuration vary. Each row contains the full public snapshot, wire message, decoded state, result, replay, final effects/receipts, and measures.

The original run's `raw.jsonl` is archived losslessly as `results/run-001/raw.jsonl.gz`; `SHA256SUMS` records the compressed file and original decompressed byte hash. Inspect it with:

```sh
python3 -c "import gzip; print(gzip.open('experiments/e4-boundary/results/run-001/raw.jsonl.gz', 'rt').read())"
```

Exact source/fixture/protocol hashes and environment are in `configuration.json`; aggregate outcomes are in `summary.json`. No data from run-001 was overwritten. The test log is preserved alongside the results. See RESULTS for limitations, counterevidence and the single next experiment.
