# E7.2 implementation-ready contract

This file specifies future code; it is not executable implementation. PROTOCOL.md is authoritative if a discrepancy is found: stop and issue a pre-evaluation amendment rather than choose a favorable interpretation.

## Reuse and dependency boundary

Import E7's model, public/boundary rendering, state, execute and expected helpers under unique module names. Reuse E4 gate/world/receipt verification without edits. Reuse only E7's development sources, not E7/E7.1 evaluation as training. Historical evaluation hashes may be checked by the curator for duplicates. Use the published E7.1 configuration's Python/package pins: Python 3.12.14, scikit-learn 1.8.0, NumPy 2.3.5, SciPy 1.17.0, joblib 1.5.3, threadpoolctl 3.6.0. A runtime mismatch must be resolved and recorded before fitting; it cannot be silently waived.

Maintain TF-IDF word (1,2)/LogisticRegression(C=10,max_iter=1000,random_state=704) and unigram CountVectorizer/MultinomialNB(alpha=1). Single-thread BLAS/OpenMP for future E7.2 runs; record OS, Python executable, versions and actual threadpool state. No model APIs/network inference. Preserve E7's release>=0.6, withhold<=0.4, otherwise escalate, and version guard. Producer known-scope probabilities determine only its original orientation; transmitted experimental values come from fixed literals. Consumer never sees the semantic oracle.

## Required functions and invariants

| Future function | Inputs / outputs | Required invariant |
|---|---|---|
| make_development | E7 development → balanced expanded sources | 216 originals; 780 clear and 780 blocked; multiplicities 13/5; no heldout imports |
| fit_producers | original 216 source review texts → two pipelines | Parameter states match archived E7 producer states; consumer refitting is intentionally different |
| assessment_transform | copied E7 contract, P+/P-/M/N → copied contract | Only five preregistered paths change; no floating complement or extra correctness/presence flag |
| make_training | balanced sources, regimes, producers, renderings, copy slot → wires/labels/metadata | 24,960 rows per regime; deterministic source/prod/render/copy order; equal exposure and source multiplicities |
| audit_training | complete training records → contingency/histograms/check status | F bundles independent per source and balanced by truth; R/F full-bundle marginals match; metadata never enters wires |
| fit_consumers | one regime's frozen training → two pipelines | Fit vocabulary/IDF/classifier on development only; no heldout-dependent calibration, selection or adapters |
| fit_rich_reference | same source multiplicities and total rows → two pipelines | Rich-only wires repeated 16 times per expanded source; identical between regimes |
| audit_transform | all development wires → tokens/norms/hash checks | P/N eligible word-count match at manipulated fields for both tokenizers; supporting/world/nonbundle equality; M/N orientation identity |
| validate_freeze | registration, implementation, data/label/curator manifests → pass/fail | Verify ancestry/hashes/attestation; cannot query predictions or repair heldout |
| evaluate | frozen pipelines and sealed corpus → lossless rows | New output directory; fixed cells once; no fitting; save full wires/probabilities/effects before aggregation |
| analyze | lossless rows → contrasts/criteria/cluster sensitivity | Separate B/U; exact pair index; no row-level independence; fixed bootstrap plan; no composite verdict |
| verify | saved files + manifests → independent reconstruction | SHA256 of compressed/decompressed data, row-key uniqueness, all expected cells, gates, every aggregate/criterion recomputed |

Metadata rows must contain experiment/registration/implementation/evaluation commit identifiers, pair/case/family, training regime, producer/consumer, rendering/access/orientation, source/world/support hashes, original producer probability, exact transformed bundle, complete wire, consumer probability/decision, semantic and operational expected outcomes, effects/receipts/replay, useful completion, unsafe proposal, abstention/escalation, resource counts and timings. Identifiers and labels stay out of model wire text.

## Evaluation shape and no redundant evidence

For 144 cases, mixed models cross 2 regimes × 2 producers × 2 consumers × 5 unique inputs (P+, P-, M, N, rich) = 5,760 rows. The two rich-only references add 144 × 2 = 288 rows, for 6,048 total. Primary 128-case subset: 5,120 mixed rows plus 256 capacity-reference rows. No redundant orientation rows for M/N/rich. Producer duplication after confidence normalization is recorded; rows never become independent observations. No model randomness replication is claimed.

Novel pairs differ only in the extra directive; orientation pairs differ only in assessment bundle. These are different interventions and must have separate hashes and contrast keys. Known/state controls have declared eligibility and are reported outside primary means. Curator makes labels; models receive only frozen source or hybrid wire.

## Artifact and validation requirements

Future output: configuration.json, source/environment/freeze/curator manifests, development/training/evaluation datasets, fitted model states, raw.jsonl.gz, summary.json, analysis.json, validation logs and SHA256SUMS covering files and decompressed bytes. Include deviations and failed controls even when no conclusion is possible. Exact semantic refit/replay is targeted in the pinned runtime; timing is not reproducible and cross-platform floats require explicit comparison limits frozen before evaluation.

Before receiving evaluation: tests for class/bundle/exposure contingencies, no leakage, unchanged support/authority, token counts, orientation identities, fixed thresholds, deduplication, synthetic analysis arithmetic and paired-cluster resampling. Synthetic analysis rows must not use future evaluation templates. Baseline archive checks are read-only and do not execute E7.2.

Guard evaluation loading separately from fitting. It requires registration commit, implementation freeze, curator attestation, evaluation freeze, all SHA256 pins and a separately recorded evaluation authorization. No current field contains an invented future SHA. Missing field means stop. A CLI flag alone does not establish authorization or independence.

No fitting, generator, evaluation loader or new model code is created by the preregistration task. Next work may implement development/preflight/analysis after review; evaluation remains a later separately authorized step.
