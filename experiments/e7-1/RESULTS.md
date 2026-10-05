# E7.1 — assessment interference established; pooled causal attribution inconclusive

October 4, 2026. Canonical preregistration `89970c2c8dc9e2374b056d33d7b47a394af5e7c8` was published before implementation and evaluation creation. Evaluated implementation/evaluation freeze: local `ab1378ec9f51885504d09e8a031f9dfd1083bb7b`, parent is that canonical protocol. No E7/E4/E4.1 artifact changed. Source hashes recorded before/after execution; no model, schema, threshold, fixture or analysis criterion repair.

40 new cases, 24 primary novelty cases (12 safe/blocking pairs), 8 known controls and 8 state controls. 7,680 crossed executions are correlated repetitions, not 7,680 independent samples. Three consumer training regimes: E7-exact reliable, 50%-within-class assessment flips with seeds 9101/9102. Two learned producers × two consumers, four existing E7 boundaries, present/masked assessment and actual/complement input orientation. No new context-recovery mechanism or literature retrieval.

## Observations: primary full-support hybrid condition

Actual-orientation novelty outcomes (n=24, 12 useful safe cases) below. Supporting source is identical within each paired intervention. Both producer configurations yield the stated values except the noted seed9102 difference.

| Consumer / training | Assessment present: correct, safe useful | Assessment masked: correct, safe useful |
|---|---|---|
| Linear / reliable | 12/24, 12/12 | 24/24, 12/12 |
| Linear / decor9101 | 12/24, 12/12 | 24/24, 12/12 |
| Linear / decor9102, linear producer | 21/24, 12/12 | 24/24, 12/12 |
| Linear / decor9102, NB producer | 12/24, 12/12 | 24/24, 12/12 |
| NB / reliable | 12/24, 12/12 | 21/24, 12/12 |
| NB / either decorrelation seed | 12/24, 12/12 | 12/24, 0/12 |

Masking the reliable consumer's complete assessment bundle fixes all twelve blocked novelty errors for linear and nine for NB without sacrificing ANY of twelve safe novelty completions. The same frozen model/schema/renderer/support and gate remain in use. Thus at least these supporting facts CAN affect useful decisions through the current hybrid boundary; hard inability to transport/use context is contradicted.

At fixed source facts, reversing assessment orientation changes all 24 novelty decisions for either producer feeding the reliable linear consumer. It changes nine for linear producer→NB consumer. NB producer→NB consumer changes zero decisions and mean absolute probability only .0535; it remains saturated toward release despite opposite assessments. Masking this last pairing still fixes nine blocked errors. Null removal therefore cannot be equated with semantic trust in the assessment's direction for every configuration.

Training decorrelation reduces orientation sensitivity but generally does not restore correct present-assessment novelty behavior. Linear seed9102 recovers nine blocked cases only with the linear producer; seed9101 and the NB producer do not. NB under either decorrelation seed plus masking loses ALL safe novelty completions. Its rich-context control also collapses to 12/24 novelty decisions with zero safe novelty completion; changed training caused a broader fitting/threshold/generalization problem, not evidence that the hybrid boundary alone blocked information. Reliable rich on the new novelty set is 21/24 for both consumer families; that does not meet the protocol's <=1-error integration control. Counts and differences-in-differences (0 or9, depending configuration/seed) are preserved in summary.json, not pooled as independent samples.

Across ALL 40 cases, reliable actual hybrid masking improves linear from 27/40 to30/40 but useful completion falls 15/16→12/16; NB improves27/40→35/40 but useful falls15/16→14/16. Linear masking generates ten escalations versus one; NB remains one. The perfect linear novelty subset is NOT a deployment-wide fix. Explicit/adaptive masked arms lose all useful completion; in these arms masking can erase the only known-review signal and is not a valid full-context integration test. All secondary/complement conditions and their separate completion/escalation/recovery/cost values are in the raw rows and grouped summary.

## Preregistered verdict, without changing thresholds

- Linear producer→linear consumer: **A** (S criterion met, I not met).
- NB producer→linear consumer: **A**.
- Linear producer→NB consumer: **A**.
- NB producer→NB consumer: **D** (orientation effect below preregistered threshold despite useful masking).
- **Pooled: D**, because the protocol requires the shortcut pattern across all configurations and mixed conclusions remain inconclusive. No configuration establishes I under the required competent-rich and persistent-hybrid-failure controls. B/C are not supported by these operational criteria.

The specific observed causal effect is **assessment-bundle presence interferes with contradictory-context decisions**, demonstrated by same-fitted-model counterfactual masking with equal supporting facts. Strong evidence of assessment dependence exists in three configurations. This is insufficient to identify reliable-training shortcut learning as the sole mechanism across all configurations, or distinguish it cleanly from lexical duplication, normalization, residual confidence signals and mixed-format fitting. Do not rename D to an architecture success or a universal shortcut result.

## Manipulation checks and postrun audit

Reliable fitted producer/consumer states exactly match preserved E7. Training flips: 108/216 records per noise seed, exactly 30/60 clear and 78/156 blocked; explicit binary assessment contingencies are 50/50 within truth classes. Supporting artifact hashes, requests and operational-state hashes match across conditions. Masked actual/complement wires are identical, with zero remaining assessment-proxy mismatch. Known-scope producer classification errors: zero. No source/oracle label is passed to consumer inference.

Postrun descriptive audit (POSTRUN_AUDIT.json, not another intervention): complete assessment bundles, INCLUDING decimal probabilities, remain label-identifying by lookup in the development corpus even after binary label decorrelation. No exact bundle has opposite truth labels: 80 unique linear bundles per noisy regime,36/37 unique NB bundles. This establishes residual empirical information, NOT that the fitted models memorized numeric tokens. It weakens interpretation of binary flips as independent full-assessment noise. The protocol anticipated confidence/marginal residuals; this audit documents the concrete gap rather than quietly repairing it.

## Authority, evidence, cost and recovery remain separate

All 7,680 rows have zero enforced credential violations, duplicate effects and narrow false receipt verification. Many present-assessment arms still make semantically incoherent releases; reliable actual hybrid has12 per configuration, reliable masked linear 0/NB 3. Shared mediation/audit creates safety invariants; those zeros are mechanism checks, not semantic success. Prior-effect replay/recovery, unsupported-release proxy, registry reads, request/payload bytes, timing and replacement disagreement are separately recorded in summary/POSTRUN_AUDIT and raw outputs. In particular, consumer withholding can prevent attempted recovery and lose useful confirmation; no safe-count substitute for recovery.

No API/network/paid inference. Exact Python/library/git versions, seeds, BLAS thread configuration, training time and 15,360 evaluation prediction calls are recorded. Tiny local latency/byte counts are not lifecycle economics. Probabilities remain uncalibrated. Producer containers and consumers are real fitted statistical models, much less heterogeneous than general LLM/planner/robotic intelligence.

## Interpretation limits and negative findings

Masking is an OOD input perturbation and removes repeated predictive words and probability tokens together. It proves an input-interference effect but cannot by itself establish psychological trust or a learned causal mediator. The reliable NB producer→NB consumer saturation contradicts a universal assessment-direction account. Decorrelated training can damage even the assessment-free rich control; that is an important negative result, not a contract win. Different confidence distributions across replaceable producers matter despite the same schema. Independent complete facts are available in hybrid; explicit omission and adaptive partial coverage remain distinct unresolved causes. Familiar generated vocabulary, same-author cases and trusted exact simulated effects limit all generalization.

No experimental deviation from the frozen manipulations/analysis is needed to explain the result. Initial postrun reproduction discovery failed because reused E7's path shadowed the new test filename; retained failure log, then gave the new reproduction test a unique name/restored its discovery path. Evaluated implementation, cases, data, criteria and original artifacts were unchanged. Full refit reproduces all 7,680 wires/probabilities/decisions/effects and saved training/model state. Validation records this testing correction, not an experimental repair.

## Hypotheses and single justified next experiment

H1 remains weakened for economical frozen/adaptive semantic sufficiency; categorical boundary-blockage interpretations of E7 are now weakened because masking restores context use without changing the boundary. H5 gains no general semantic-substitutability claim: different producer confidences/consumer families give different causal patterns. H2/H3/H4 unchanged; authority zeros do not establish useful intelligence or architectural advantage.

**E7.2: confidence-matched shortcut diagnostic.** Repeat the smallest full-support hybrid factorial with new untouched safe/blocking pairs, same schema/models/gate/thresholds, but normalize assessed confidence to the SAME fixed .9/.1 values in both reliable and stratified50%-fallible training. Require each complete fallible assessment bundle to occur with both truth labels, preventing decimal-probability identifiers. Include masked and neutral assessment-presence controls exposed during development to distinguish semantic assessment direction from token presence/OOD removal, plus rich control; report selective errors and safe completion separately. Predeclare that context use must survive fallible PRESENT assessments without sacrificing safe work or collapsing the rich control. If it does not, shortcut-learning correction remains unsupported. No retrieval/escape-hatch implementation is experimentally justified yet: resolve this identified manipulation confound and available-context-use failure first.
