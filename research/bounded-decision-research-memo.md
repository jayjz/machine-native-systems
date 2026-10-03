# Bounded Decision Systems — Research Memo
Research date: October 2, 2026 (America/New_York)

## Assessment
The hypothesis is plausible for recurring decisions whose state, action space, and success criteria can be specified. The repositories support separating intelligence from authority more strongly than replacing general-purpose models. They do not establish industry-wide overuse or end-to-end superiority of specialist systems.

From first principles, a decision needs relevant information, an objective/loss, constraints, and a policy. Conversation is one way to compute that policy. Typed output, specialist cognition, independent enforcement, and reliable evidence are separate design choices. An LLM can operate inside this architecture; a deterministic component can violate it.

The difficult assumption is that the typed state preserves decision-relevant information. A bounded action space does not imply an easy decision problem. Evidence must span the process: preserve input provenance and commit intent before external effects, then reconcile outcomes.

## 1. Questions and closest traditions

| Research question inferred from artifacts | Repository evidence | Closest established traditions |
| --- | --- | --- |
| Can a capable proposer be interchangeable while authority remains independently enforced? | SHAD0W strategies propose; risk gates grant; durable journal and broker reconciliation establish operational state. AetherForge gates strategy requests using resource measurements. | Runtime assurance / Simplex; reference monitors; capability security; policy decision/enforcement separation; assume-guarantee contracts. |
| When can recurring semantic decisions move to a specialist without increasing total loss or cost? | TEMPER explicitly investigates specialist + calibration + verification + escalation and cost per verified correct decision. | Selective classification; learning to defer; cascades; distillation; decision-focused learning. |
| What can establish correctness independently of a convincing explanation? | CipherLoop AST-backed findings; TraceForge independently ingests evidence and checks integrity. | Static analysis; proof-carrying results; provenance; assurance cases; independent evaluation. |
| What was actually known, and what changed, at each consequential decision? | SHAD0W availability semantics, journal-before-dispatch, explicit unresolved state; CipherLoop trajectory ledger. | Event sourcing; write-ahead logging; state-machine replication; causal/temporal semantics; partial observability. |
| Which control structures recover under corruption rather than merely look organized? | Fracture compares failure injections, graph topologies, and verifier strategies. | Fault injection; chaos engineering; resilience engineering; runtime verification; controlled intervention. |

These are converging design questions across artifacts by one author, not independent experimental replications.

## 2. Evidence for and against

Supporting:
- TEMPER's September 17 result record reports frozen BERT baseline mean validation macro F1 0.9539 versus B1 0.8864. This supports specialist feasibility on one fixed intent task. Raw artifacts are external and were not independently recomputed in this investigation.
- SHAD0W and AetherForge encode permissions, resource limits, and lifecycle constraints directly. These decisions do not intrinsically require prose generation.
- Neural Simplex provides established precedent for a learned controller under independently checked runtime authority.
- FrugalGPT and RouteLLM report benchmark-specific gains from cascades and learned routing. They support selective computation, not universal replacement of generative models.
- Anthropic's engineering guidance explicitly permits traditional classifiers for routing. OPA separates policy evaluation from application enforcement. Temporal reconstructs workflow state from event history. This architecture already has substantial precedent.

Contradicting or limiting:
- TEMPER has no demonstrated specialist-plus-escalation superiority under shift and full lifecycle cost.
- TraceForge's baseline has two scripted cases; production ingestion checks evidence integrity, not general task success. Fracture's inspected core runtime still raises NotImplementedError. These are research infrastructure, not comparative results.
- CipherLoop's inspected AST validator assigns confidence 0.9 as a constant. An AST trace is evidence within its limited analysis semantics, not calibrated confidence or proof of exploitability.
- ReAct (ICLR 2023) demonstrates benefits from interleaving language reasoning and interaction on particular tasks. Removing language-mediated deliberation can remove useful computation.
- Turpin et al. show misleading reasoning explanations; ACL 2026 work by Zaman and Srivastava challenges treating omitted hints alone as proof of unfaithfulness. Explanation can be useful without being sufficient evidence.
- Calibration and conformal risk guarantees require assumptions; arbitrary shift, subgroup failure, verifier omissions, and correlated model/verifier errors can break deployment expectations.
- No inspected evidence establishes what fraction of production agent decisions is unnecessarily delegated to LLMs.

## 3. Replacement boundaries

| Function | Candidate machinery |
| --- | --- |
| Freshness, permissions, budgets, admissible actions | Predicates, policy engines, capabilities, atomic reservations |
| Known retries, tool scheduling, lifecycle transitions | State machines and durable workflows |
| Fixed semantic labels and escalation routing | Classifiers/encoders, calibrated selective prediction |
| Planning with explicit goals, transitions, and constraints | Search, constraint solving, optimization |
| Hidden-state estimation and sequential uncertainty | Bayesian filters, probabilistic programs, POMDPs |
| Resource adaptation | Feedback controllers, admission control, optimization |
| Correctness claims | Tests, static analysis, formal verifiers, external observations |

This is an architectural assessment, not a result from the repositories. General-purpose models retain their strongest case when relevant state must be discovered: unfamiliar code, open-ended investigation, ambiguous requirements, new concepts, changing tasks, and synthesis. They may generate a specification or program which subsequently runs without repeated model calls. Necessity must be demonstrated against alternatives; neither open-endedness nor a JSON interface proves it.

Official Structured Outputs documentation explicitly says structured responses can contain mistakes. OpenAI Agents SDK documents per-tool guards; final-output checks happen after execution and cannot substitute for pre-effect authorization.

## 4. Terminology

- Sufficient state representation / state abstraction: a schema must retain the information needed for a decision; types alone do not do that.
- Selective risk and coverage: error among accepted predictions, and fraction accepted.
- Calibration versus discrimination: honest probabilities and good ranking of difficult cases are different properties.
- Learning to defer / value of information: choose escalation according to expected downstream benefit and cost.
- Decision-focused learning / regret: optimize consequences, not only label accuracy.
- Reference monitor / complete mediation: every consequential action crosses an enforced authority boundary.
- TOCTOU: authorization can become stale between checking and acting.
- Epistemic uncertainty versus operational unknown state: prediction uncertainty differs from not knowing whether an external action completed.
- Verifier soundness and completeness: false acceptance and false rejection are separate limitations.
- Trusted computing base: the components whose failure invalidates claimed guarantees.

## 5. Three falsifiable experiments

All thresholds below are proposed preregistration choices, not measured results. Freeze data, policies, loss functions, thresholds, model versions, and evaluation rules before final testing. Use paired cases and confidence intervals; record labels/oracles and their limitations.

A. Is prose deliberation necessary for a fixed semantic task?
Extend TEMPER with B1/B2, a general model producing constrained labels directly, the same model with a deliberative protocol, and specialist-plus-escalation. Hold downstream authority/evidence constant. Fit routing only on reserved calibration data; evaluate untouched in-scope data plus independently specified OOS and label-preserving perturbations. Suggested success criterion: at least 30% lower full-system cost per verified correct decision, at least 70% specialist coverage, and no more than one percentage point increase in task error, with uncertainty bounds. Charge training, calibration, verification, escalation, monitoring, and maintenance under declared traffic scenarios. Failure: savings vanish, coverage collapses, or risk rises under shift. This tests specialization and deliberation separately.

B. Does authority separation help independently of model intelligence?
Use a fake-broker SHAD0W/Fracture harness and a 2×2 design: rule versus model proposer; advisory versus enforced pre-effect gate. Inject stale state, duplicate requests, contradictory observations, crashes, lost acknowledgements, and persuasive permission-bypass prose. Apply identical rules and record authorized useful completions as well as violations and unresolved outcomes. The enforced arms must reject every specified illegal action, preserve declared legal completions, and require no model-specific bypass. Failure: invalid effects cross the gate or useful completion collapses. A gain shared by both proposer types supports enforcement architecture, not LLM replacement. Zero observed failures is bounded test evidence, not a universal guarantee.

C. Is typed state actually sufficient?
Build paired CipherLoop/security triage cases: same proposed typed state but different omitted source context requiring different correct decisions. Include out-of-scope program constructs. Compare typed-state-only decisions, access to full source/context, and typed-state decisions with evidence-triggered escalation. Use executable fixture oracles or independently adjudicated labels; measure decision regret, false verification, abstention, and total cost. If full context consistently resolves distinctions the schema collapses and escalation cannot recover them economically, reject that state abstraction. If a richer bounded representation preserves decisions at lower cost on held-out variants, support that boundary. Freeze abstraction revisions before evaluation; do not redesign on held-out cases.

## 6. Most important unresolved question

Can a compact, maintainable state representation and independently valid success criterion capture enough of a real evolving task that bounded decisions remain useful under novelty—without shifting the cost and intelligence into extraction, verification, escalation, and maintenance?

## Provenance and scope

Inspected README files, sampled commit history from August–September inside the roughly July 5–October 2 window, selected contracts/results and implementation files. This is a targeted artifact review, not an exhaustive 90-day commit audit or test execution.

- SHAD0W default revision: 8e5e6f9e94dd47a7ca2a209e73d6019d51ac201f. Also inspected feat/btc-paper-learning-loop and its canonical docs/STATUS.md. That status distinguishes strict bounded sessions from separate operational PAPER_SOAK; README status is older.
- TEMPER: 0747730d18cdb692142d9c2b50f9e8bc1ff0c45f. Result record supersedes stale B2-next README paragraphs.
- CipherLoop: f03a1e186e491cf24aa0f0e0671cac766c1fa8ab. Inspected src/cipherloop/executor/validator.py.
- TraceForge: 51af0f4ed2e9fb0416bffcb3f0bc8140bc1c38bd. README and production ingestion distinguish capture integrity from task-success evaluation.
- AetherForge: 265c26769eba257ac40540a7e1da5378d7515532. Inspected src/server.py; real hardware fast-swap remains outside verified mock claims.
- Fracture: 300ef83a0ee999857189542bd836f215490da116. README plus src/fracture/core/runtime.py; do not infer completed comparative experiments from commit descriptions.
- No undocumented Jev internal mechanism was assumed.

## Primary sources

Repository sources:
- https://github.com/jayjz/SHAD0W/blob/feat/btc-paper-learning-loop/docs/STATUS.md
- https://github.com/jayjz/SHAD0W/blob/8e5e6f9e94dd47a7ca2a209e73d6019d51ac201f/src/shadow/risk/gate.py
- https://github.com/jayjz/TEMPER/blob/0747730d18cdb692142d9c2b50f9e8bc1ff0c45f/docs/results/EXP-0001-B2-validation-2026-09-17.md
- https://github.com/jayjz/CipherLoop/blob/f03a1e186e491cf24aa0f0e0671cac766c1fa8ab/src/cipherloop/executor/validator.py
- https://github.com/jayjz/TraceForge/blob/51af0f4ed2e9fb0416bffcb3f0bc8140bc1c38bd/README.md
- https://github.com/jayjz/aetherforge/blob/265c26769eba257ac40540a7e1da5378d7515532/src/server.py
- https://github.com/jayjz/fracture/blob/300ef83a0ee999857189542bd836f215490da116/src/fracture/core/runtime.py

Research:
- Neural Simplex Architecture (NFM 2020): https://arxiv.org/abs/1908.00528
- Selective Classification for Deep Neural Networks (NeurIPS 2017): https://arxiv.org/abs/1705.08500
- Conformal Risk Control (2022; revised 2025): https://arxiv.org/abs/2208.02814
- FrugalGPT (2023): https://arxiv.org/abs/2305.05176
- RouteLLM (2024; revised 2025): https://arxiv.org/abs/2406.18665
- LLM-Modulo (ICML 2024 position paper): https://arxiv.org/abs/2402.01817
- ReAct (ICLR 2023): https://arxiv.org/abs/2210.03629
- Unfaithful Explanations in Chain-of-Thought Prompting (2023): https://arxiv.org/abs/2305.04388
- Chain-of-Thought Can Be Faithful without Hint Verbalization (ACL 2026): https://arxiv.org/abs/2512.23032
- Decision-Focused Learning: Through the Lens of Learning to Rank (ICML 2022): https://proceedings.mlr.press/v162/mandi22a.html
- Authorization Architectures for Tool-Using AI Agents (September 14, 2026 preprint; review, not deployment proof): https://arxiv.org/abs/2609.15906

Official documentation, accessed October 2–3 UTC, 2026:
- https://www.anthropic.com/engineering/building-effective-agents
- https://openai.github.io/openai-agents-python/guardrails/
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://www.openpolicyagent.org/docs
- https://docs.temporal.io/tasks

