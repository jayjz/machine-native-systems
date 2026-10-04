# Research experiments

Consolidated from the preserved reports. **The initial synthesis did not execute these proposals. E4 now has a finite scripted boundary run; E1–E3/E5–E6 remain unexecuted.** Preserve the original formulations and proposed thresholds in the reports; values below are not measured results.

## E1. Bounded semantic decisions and total cost

- **Tests:** H3; whether deliberative prose is necessary for a fixed semantic task.
- **Existing proposal:** Bounded-decision experiment A, motivating repository TEMPER.
- **Comparison:** B1/B2 specialist, constrained-label general model, same model with deliberation, specialist-plus-escalation. Hold authority/evidence constant; reserve calibration data; use untouched in-scope, OOS, and label-preserving perturbations.
- **Metrics:** Task error, selective risk, coverage, calibration, latency, and full lifecycle cost per verified correct decision including training, monitoring, verification, escalation, and maintenance.
- **Falsification:** Savings disappear, coverage collapses, or risk rises under shift. Original suggested preregistration: ≥30% cost reduction, ≥70% specialist coverage, ≤1 percentage point error increase with uncertainty bounds; justify or revise before testing, not afterward.

## E2. Authority separation independent of intelligence

- **Tests:** H2; separates an enforcement effect from a cognition effect.
- **Existing proposal:** Bounded-decision experiment B, SHAD0W/Fracture fake-broker harness.
- **Comparison:** Rule versus model proposer × advisory versus enforced pre-effect gate. Identical policy and task set.
- **Faults:** Stale state, duplicates, contradictions, crashes, lost acknowledgments, persuasive bypass requests.
- **Metrics:** Prohibited effects, useful authorized completion, unresolved effects, audit reconstruction, model-specific bypasses.
- **Falsification:** Prohibited effects cross enforcement, a proposer requires special permission exceptions, or safety mainly comes from blocking useful work. A gain in both proposer arms supports authority architecture, not LLM replacement. Zero observed violations is bounded test evidence.

## E3. State sufficiency and evidence-triggered escalation

- **Tests:** H1/H3/H5; whether a bounded representation preserves consequential distinctions.
- **Existing proposal:** Bounded-decision experiment C, CipherLoop/security triage.
- **Comparison:** Paired cases with identical typed summaries but omitted source context requiring different correct decisions; typed-only, full-context, and evidence-triggered escalation arms. Include out-of-scope constructs.
- **Metrics:** Regret, false verification, abstention, cost; executable fixture or independently adjudicated oracles with stated limitations.
- **Falsification:** Full context consistently resolves collapsed distinctions while escalation cannot recover them economically. Freeze schema revisions before held-out evaluation.

## E4. Communication representation at matched authority

- **Tests:** H1/H5 independently of gate quality.
- **Existing proposal:** Communication-map boundary representation experiment.
- **Comparison:** Same models, tools, authority, budgets, and tasks; prose, typed domain records, hybrid messages.
- **Stressors:** Ambiguity, stale evidence, schema evolution, replacement components.
- **Metrics:** Semantic errors, substitutions requiring undocumented knowledge, preserved decision quality, integration effort, latency.
- **Falsification:** Contracts provide no material improvement, or information loss and adaptation cost outweigh benefits. Do not attribute authority-gate gains to message syntax.

## E5. Coordination and recovery under faults

- **Tests:** H1/H4; explicit coordination compared with conversational agreement.
- **Existing proposal:** Communication-map coordination-under-faults experiment.
- **Comparison:** Identical candidate proposals/evidence; conversational coordination versus owned state machine/durable workflow.
- **Faults:** Duplicate/reordered delivery, crashes around effects, missing acknowledgments, conflicting grants.
- **Metrics:** Invariant violations, duplicate effects, useful recovery, unresolved outcomes, overhead.
- **Falsification:** No material recovery/invariant improvement at matched overhead, or useful progress is lost. E2 tests authority; E5 tests coordination—retain this distinction.

## E6. Rich communication versus independent audit

- **Tests:** Limits of H1/H5 and an exclusively symbolic substrate.
- **Existing proposal:** Communication-map rich-communication experiment.
- **Comparison:** Text, typed beliefs, compatible-model latent sharing on bounded and open-ended tasks.
- **Metrics:** Quality, latency, calibration, replacement/transfer to new components, and independent reconstruction of consequential decisions.
- **Falsification:** Symbolic contracts cannot preserve necessary information economically while richer channels achieve equivalent practical assurance. Conversely, latent speed gains alone do not establish interchangeable or auditable components.

## Common protocol

Pre-register losses, effect sizes, noninferiority margins, datasets, model/tool versions, failure assumptions, budgets, and oracle limitations. Use paired cases and uncertainty intervals. Report performance, risk, authority violations, recovery, and cost separately. Account for correlated proposer/verifier errors. Do not redesign interfaces on held-out evaluation cases.

The largest actual gap is executed controlled comparisons, not another general literature memo.

## Executed boundary exploration

[E4 artifact-release handoff](e4-boundary/README.md): protocol and confound review written before implementation; run-001 compares full controlled prose/JSON/hybrid and compact JSON. Full formats tie; compact loses semantics/recovery under optimistic defaults. Raw results, exact configuration, limitations, and next-test falsification are preserved. This is not a model benchmark or framework.

[E4.1 defaults × semantic subsets](e4-1/README.md), executed: conservative compact prevents duplicates but loses useful work; alternatives + attempt + status matches full in this finite world, receipt reference redundant. All 32 subsets/default policies and reference retained. Next is E7 novelty with a development-frozen interface and learned components.
