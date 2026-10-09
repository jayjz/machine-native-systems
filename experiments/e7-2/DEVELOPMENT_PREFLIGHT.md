# E7.2 development/preflight implementation

Implementation hypothesis: with the frozen E7 source corpus expanded to equal
clear/blocked mass, complete fallible assessment bundles can be made exactly
nonidentifying of development truth while reliable and fallible regimes retain
the same present-bundle marginals and exposure. This is an implementation
property, not a result about semantic trust, an internal mediator, deployment,
or the E7.2 estimand.

This implementation is development-only. It has no evaluation generator,
evaluation loader, case fixture, oracle, or inference command. The frozen
`EVALUATION_PLAN.json` remains byte-identical to registration and retains
`registration_commit: null`; the resolved registration SHA is recorded by
`registration_checks` and separate implementation artifacts instead.

## Commands

Run source/preflight tests without fitting:

```sh
python -m unittest discover -s experiments/e7-2 -p 'test_*.py' -v
python -m compileall -q experiments/e7-2
```

For the Windows x64 Python-3.12.14 runtime, resolve and install the checked-in
hash lock into an isolated virtual environment. Do not install into a system
Python and do not replace this lock with an un-hashed requirements file:

```sh
uv pip sync --python <isolated-python-3.12.14> --require-hashes --only-binary :all: \
  experiments/e7-2/requirements-3.12.14-windows-x86_64.lock
```

Record a no-fit environment preflight:

```sh
python experiments/e7-2/run_development.py --preflight-only --output <new-directory>
```

Only after the report says `fitting_allowed: true`, run the development fit:

```sh
python experiments/e7-2/run_development.py --output <new-empty-directory>
python experiments/e7-2/verify.py <directory>
```

The runner requires Python 3.12.14 and scikit-learn 1.8.0, NumPy 2.3.5,
SciPy 1.17.0, joblib 1.5.3, and threadpoolctl 3.6.0. It records actual
threadpools and forces the declared one-thread environment. It refuses to fit
on any mismatch rather than treating a local run as a reproduction.

## Implemented contract checks

| Contract area | Status before a pinned fit |
|---|---|
| Registration ancestry and frozen registration blobs | Implemented and tested |
| Historical E7/E7.1 archive checksum reconstruction | Implemented and tested read-only |
| 216 to 1,560 development expansion and 13/5 multiplicities | Implemented and tested |
| 24,960-row mixed regimes / 24,960-row rich reference | Implemented; exercised only when scikit-learn is available |
| R/F full-bundle marginals, exposure, F mutual information and lookup accuracy | Implemented; exercised only when scikit-learn is available |
| Consumer-wire isolation, transform identity, tokenizer checks | Implemented; tokenizer execution requires pinned scikit-learn |
| Fitted producer reproduction and consumer/reference fitting | Runtime established; **blocked** because the linear historical producer state differs in 32 floating-point coefficients (Bayes matches exactly) |
| Synthetic paired-cluster analysis and negative fixtures | Implemented and tested without evaluation templates |
| Evaluation loading | Deliberately absent; `validate_freeze` fails closed on missing pins and authorization |

The analysis treats R/F as effects of the stipulated complete training regimes.
It cannot separate reliability from every induced feature-weight, IDF, or
normalization change, and it does not identify semantic trust or any internal
mechanism. Independent curation, sealed oracle/evaluation hashes, an
implementation/evaluation freeze, and separate execution authorization remain
required before any evaluation can be considered.

No development corpus, consumer, or rich-reference artifact may be generated
until the historical linear producer-state discrepancy is resolved under the
registered exact-state requirement. The recorded mismatch is a reproducibility
blocker, not a result or a basis to relax equality tolerances.
