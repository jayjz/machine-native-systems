# E7.1 reproduction

Read PROTOCOL.md before RESULTS.md (added after execution). Frozen E7 schema/components and pinned environment; no keys/GPU/network/paid inference. Python 3.12.14; scikit-learn 1.8.0, NumPy 2.3.5, SciPy 1.17.0, joblib 1.5.3, threadpoolctl 3.6.0. Reuse `experiments/e7/requirements.txt` if packages are absent.

```sh
python3 -m unittest discover -s experiments/e7-1 -p test_harness.py -v
python3 experiments/e7-1/run.py --output experiments/e7-1/results/reproduction-001
```

Output must be new; never overwrite run-001. Reliable consumer fitting must exactly match preserved E7 fitted parameters before new evaluation loads. Two fixed noise allocations and new evaluation generator seed are in protocol/configuration; consumer/classifier hyperparameters/thresholds are unchanged. Null masks remove all assessment proxies but retain independently available facts/state. No masking-training augmentation or new retrieval implementation.

Raw evaluation/training rows and fitted parameters are archived losslessly in gzip; datasets/configuration/aggregate causal contrasts are plain JSON. SHA256SUMS covers files and decompressed archive bytes. Same-runtime semantic reproduction is intended; cross-platform floating arithmetic and latency may differ. Statistical class probabilities remain uncalibrated. New test_reproduction.py and verify.py are added with result validation; original E4/E4.1/E7 checks remain runnable separately.
