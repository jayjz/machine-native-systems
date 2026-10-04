# E7 reproduction

Read PROTOCOL.md, frozen contract.json, then RESULTS.md including the implementation deviation. Python 3.12.14; scikit-learn 1.8.0, NumPy 2.3.5, SciPy 1.17.0. Local CPU, no keys/GPU/network/paid inference. Exact development and held-out sets, fitted coefficients/vocabularies and every raw prediction/request/effect are preserved. Models fit before heldout import; development/contract freeze precedes heldout source creation in git history.

```sh
python3 -m pip install -r experiments/e7/requirements.txt
python3 -m unittest discover -s experiments/e7 -p test_harness.py -v
python3 experiments/e7/run.py --output experiments/e7/results/reproduction-001
```

Output must be new. Seeds, classifier hyperparameters, thresholds, inputs and source hashes are in configuration.json. Deterministic semantic reproduction is intended; hardware/library threads may change floating arithmetic near thresholds and latency. Inspect raw probabilities rather than assuming bitwise cross-platform identity. No prompts, temperatures or inference sampling exist for these statistical models. Resubstitution scores are not independent validation. Original tests are captured in checks.txt. POSTRUN_ANALYSIS.json audits collisions and trust/effect measures without altering run-001.

SHA256SUMS covers compressed results, datasets, fitted model state, summaries/configuration and original decompressed raw bytes. Verify all experiment archives with `python3 experiments/verify_results.py`. No pickle deserialization is required; model-state.json preserves fitted parameters as plain data.
