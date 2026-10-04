# E7 — semantic sufficiency under bounded learned novelty

October 4, 2026. Preregistered after E4.1, before held-out creation or execution. No external retrieval. A concrete availability check found scikit-learn 1.8.0; no exposed language-model inference tool or installed neural model runtime. Use real locally fitted statistical text classifiers rather than scripted producers. This is NOT evidence about general-purpose language-model intelligence or unrestricted novel semantics.

## Frozen design and roles

Producer learns whether development review text permits release; internals unrestricted. Consumer learns release/withhold from boundary text. Two different learning families for each: word-bigram TF-IDF + discriminative logistic regression versus unigram count + generative multinomial naive Bayes. Cross both producers with both consumers (four configurations), without replacement-specific adapters/prompts/memory. The two inductive biases are genuine learned components, but much less heterogeneous than a planner/robotics/LLM system. No prompts, temperature or inference sampling; seeds/versions/hyperparameters recorded. No paid inference/network. Train from a deterministic development corpus; consumer training includes all boundary renderings at matched labels to avoid format-exposure imbalance.

Known development review fields: reviewer_note and supporting_note. freeze contract.json and development.py before authoring heldout.py. Models and decision threshold fixed before evaluation: consumer releases at P(clear) >=0.60, withholds at <=0.40, otherwise escalates. Producer transmits full two-class distribution and scope, never calibrated certainty. No evaluation tuning or schema repair.

Authority/effects/outcome observation remain outside models: reuse E4 registry, complete mediator and receipt matcher. Observed artifact facts and permission references are independently checked. Fresh proposals cannot prove a prior outcome. Unknown attempts require reconciliation, not a second action. A report of completion grants no rights and proves no effect. All arms receive identical task inputs/effect authority; rich baseline gets source context, explicit gets the frozen projection. No component receives the oracle.

## Four conditions

1. Rich: full source dossier, a strong information-preserving baseline. No schema restriction on interpreting supporting notes.
2. Explicit: only contract observations, scoped learned review belief/distribution, advisory proposal, evidence/grant references, attempt/status and unresolved field names.
3. Hybrid: same explicit contract plus entire source dossier as a nonauthoritative supporting artifact.
4. Adaptive: explicit; request each named unresolved top-level field (up to two / 1000 bytes), attach returned values as nonauthoritative support and rerun the same consumer. Each request/response/existence/bytes recorded. Generic discovery of deeper hidden context is deliberately not supplied. If a limit is exceeded, escalate. No schema redesign.

Development set includes single/combined permitted/blocked review notes, contradictory notes, paraphrases, irrelevant decoration. Rich, explicit and hybrid training samples derive from the same development sources. Frozen classifiers cannot be presumed to understand novel facts outside trained vocabulary.

## Held-out generation after freeze

Create deterministic evaluation cases AFTER protocol/contract/development commit. Include new task variables at unknown top-level keys (safe and blocking contrast pairs), consequential context buried within a known nested observation object, conflicting reviewer notes, changed task meanings expressed by known vocabulary in unseen locations, absent/stale evidence, schema evolution, unknown prior effects and replaced components. Content/context combinations are held out; source vocabulary may overlap development. Known stressor categories were predeclared; same-author fixture construction is not blind adversarial evaluation. Unseen locations/variables do not equal entirely unforeseen world knowledge. Preserve all held-out cases and source/model input/output losslessly.

## Measures, separate (never a combined score)

- Model proposal correctness versus semantic oracle; final decision correctness versus original E4 policy augmented with fixture review condition. Useful completed/confirmed outcomes over eligible cases.
- Semantic loss: consequential review facts unavailable in boundary to the consumer (request availability measured separately); contract-collision pairs documented. This is field availability, not a universal mutual-information metric.
- Abstention/escalation and withheld eligible work; unsupported belief propagation: confident release when full review is blocking, distinguish producer scope mistakes from consumer overreach.
- Enforced authority violations; duplicate effects; semantically incoherent fresh effects despite valid grants; false independent verification; replay/recovery after ambiguous effects. Audit property is artifact receipt match, not satisfied human intent.
- Replacement disagreement across the four configurations, outputs and recoveries; no private model weights crossed.
- Novel-family outcomes separately; requests/response availability/bytes, full dossier and boundary bytes, wall inference/tool time, request/read counts, zero paid inference, training time, source LOC/schema fields/adapters as limited complexity proxies (not lifecycle labor estimates).
- Record uncalibrated distributions and wrong high confidence; no claim that they are calibrated uncertainty.

## Expectations and predeclared falsification

Expect known-task performance to be competitive across arms; explicit projection may collapse cases whose omitted new variable reverses the decision. Adaptive should recover top-level missing variables cheaply but may miss nested state and schema changes. Hybrid/rich should retain more context, but model scope/contradiction handling may still fail. These predictions must not become conclusions if models fail development.

Evaluate economic comparison descriptively: adaptive competitive only if it has at most one additional error over rich per configuration, <=1/2 full source bytes retrieved on average, <=2 requests/case, no new authority/false-verification/duplicate violations, and no redesign or private-memory dependence. Report all criteria individually, no composite win. If rich is better by >=2 cases in both matched consumer families and adaptation cannot meet the above limits, weaken cheap fixed-contract sufficiency here. If adaptive needs >=80% of full context or repeated redesign, weaken economy. If replacement requires private adapters/memory or explicit adds overhead without coherence/recovery benefit, weaken H5/H1. Any useful action requiring bypass of gate/evidence semantics weakens separation. If all models fail the review task, treat novelty comparison as uninformative, not a contract victory. If syntax alone changes outputs, it is an integration effect, not sufficient semantics.

## Confound review before implementation

Learned classifiers are bounded intelligences and cannot infer arbitrary new concepts; novel variables are tested through familiar decision vocabulary. Generated language/oracle may favor keyword learners; mixed consumer training favors familiar contract tokens. Producer compression may omit relevant facts by design: collision demonstrates information loss, not prevalence in real agents. Adaptive field inventory helps discover new top-level variables and is a substantive interface capability, not syntax. It may miss nested omissions; rich/hybrid have more information but the same model/tool authority. Hybrid redundant beliefs may bias decisions. Shared enforcement/reliable receipt store may manufacture equal safety and recovery; report zero as mechanism checks. No independent fixture designer or true hidden-world semantics. Fixed order and tiny local inference timings are not production costs. No model-family benchmark inference, calibrated confidence, general-framework claim or broad scholarly survey.
