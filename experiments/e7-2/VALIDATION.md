# E7.2 baseline and documentation validation

Inspected October 8, 2026 via GitHub public repository endpoints and a fetched local checkout. Existing worktree was clean. Applicable instructions: root AGENTS.md; no nested AGENTS.md in the inspected tree. Open PRs: 0; open issues: 0. Repository collections fit within the requested 100-entry pages.

| Existing branch | Verified remote tip |
|---|---|
| main | `393a2ceb7c8372e4e020c81c782af1c12ade96bb` |
| research/e4-boundary-handoff-20261004 | `dffa582a3fe7f2445617e22a87d4c7ed2c0ea480` |
| research/e4-1-e7-semantic-sufficiency | `bf1003f3fdde28c3d518f661ce45aa8a42c08cdd` |
| research/e7-1-belief-shortcut | `2b9a04cf0920b54f7b994e2e2b67b5707d5192e6` |
| research/public-program-integration | `cb3b637eeae3aa599373cdfbad0e269f70976ba3` |

All three experiment branch tips are ancestors of current main. Recent main history integrates the existing E7.1 results through public-program PR #1; no newer experimental implementation was found. Every fetched remote branch tree has no E7.2 artifact path. RESEARCH_INDEX.md, experiments/README.md and E7.1 RESULTS.md agree on confidence/presence-controlled E7.2 as the proposed next step. E7.2 is not a context-recovery architecture experiment.

Read E7/E7.1 protocols, run/development/evaluation source, results, postrun audits, publication mapping, validation, configuration/manifests and representative historical raw records, plus research index, hypotheses, questions and worklog. No new holdout case/label was created or read. Raw historical records are already published evidence, not E7.2 heldout.

Read-only baseline checks passed:

```text
python3 experiments/verify_results.py
e4-boundary integrity/aggregate checks OK 640 rows
e4-1 integrity/aggregate checks OK 5280 rows
e7 integrity/aggregate checks OK 640 rows

python3 experiments/e7-1/verify.py
E7.1 archive/source integrity, 7680 unique crossed rows and all aggregates/causal criteria reconstructed; verdict D
```

These reconstruct existing archives; they do not refit models, reproduce new predictions or execute E7.2. Documentation checks verify JSON parsing, declared sample/training/row arithmetic, relative links, whitespace and restricted changed paths. Historical experiment/research artifacts remain byte-identical to baseline; only new E7.2 files and additive navigation/worklog entries are allowed.

Registration publication must record its actual Git commit externally; self-referential SHA fields remain null in the frozen plan with an explicit resolution rule. No implementation/evaluation freeze, independent-curator attestation, or evaluation authorization exists yet. No claimed result, model test, power calculation or independent evaluation has been fabricated.

Future staged work: development/preflight/analysis implementation after reviewing this design, then independent case curation under the committed plan. Experimental evaluation requires separate authorization after both freezes; it is outside this task.
