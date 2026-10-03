# Composing heterogeneous intelligence: a research map

Research cutoff: October 2, 2026, with sources available at the beginning of October. Later October publications cannot be included. This is a critical synthesis of selected primary literature and official documentation, not an exhaustive systematic review. Architectural recommendations below are inferences; papers establish narrower results under their own assumptions.

## Finding

The strongest supported direction is **explicit semantic contracts at consequential component boundaries, with freedom of representation inside components**. There is no evidence for one universally best message format, nor for eliminating language from machine communication. Typed records, prose, probability distributions, latent vectors, events, credentials, and proofs solve different problems.

The research question is therefore larger than “JSON versus conversation”: what must a receiver know, preserve, check, and be authorized to do when it receives something? Transport interoperability, shared meaning, successful reasoning, coordinated execution, and permission are separate achievements.

## 1. The questions motivating this investigation

The repositories inspected in the preceding investigation mostly fall within the roughly July–October 2026 window. Their convergence is an interpretation of one author's artifacts, not independent replication or evidence that this architecture wins.

| Artifact | Architectural question it raises | What it does not establish |
|---|---|---|
| SHAD0W | Can uncertain strategies propose while a separate gate owns risk and a broker-observation reducer owns execution state? How should unknown external outcomes affect retries? | A local atomic grant does not establish persistent, distributed, or broker-side exclusivity. The BTC branch's strict fee-finality proof remains incomplete. |
| TEMPER | Can a specialist emit bounded decisions and earn the right to answer through validation, calibration, and escalation? | The inspected classifier validation does not demonstrate the complete calibrated, out-of-scope-aware decision pipeline or superiority over general-purpose models. |
| CipherLoop | Can proposed security findings be checked against source-level structure rather than accepted because an explanation sounds persuasive? | Its inspected AST validator is a limited local taint check, not proof of exploitability; a fixed confidence value is not calibration. |
| TraceForge | Can execution evidence be ingested and checked independently of the producer and its success narrative? | Integrity checks and scripted cases do not establish general task correctness; a successful production audit was not demonstrated in the inspected artifacts. |
| AetherForge | Can admission, resource scheduling, and thermal feedback use explicit measurements and bounded control rules? | Mock safety tests do not establish real-hardware switching performance or stability across operating conditions. |
| Fracture | Does coordination topology affect recovery from failures, corrupted state, and goal drift? | The inspected runtime still raises `NotImplementedError`; proposed experiments are not completed empirical comparisons. |

These suggest five deep questions: **Who owns truth and transitions? What evidence permits action? How much state is sufficient for a decision? How should uncertainty change behavior? Which coordination topology survives faults without losing the goal?**

Repository snapshots: SHAD0W `8e5e6f9e94dd47a7ca2a209e73d6019d51ac201f`; TEMPER `0747730d18cdb692142d9c2b50f9e8bc1ff0c45f`; CipherLoop `f03a1e186e491cf24aa0f0e0671cac766c1fa8ab`; TraceForge `51af0f4ed2e9fb0416bffcb3f0bc8140bc1c38bd`; AetherForge `265c26769eba257ac40540a7e1da5378d7515532`; Fracture `300ef83a0ee999857189542bd836f215490da116`. SHAD0W's BTC branch was read separately; its status document supersedes some README claims. See repository links in the source register.

## 2. Distinctions that must survive an interface

| Role | What crosses its boundary | Common category error |
|---|---|---|
| Communication | Information and its interpretation rules | Delivering a message implies understanding it. |
| Reasoning | Hypotheses, estimates, predictions, plans | A plausible answer is an established fact. |
| Coordination | Commitments, ownership, ordering, cancellation, resource allocation | Agreement in conversation is an atomic reservation. |
| Authority | Authenticated rights bounded by policy, resource, action, and time | Competence, confidence, or another agent's request grants permission. |
| Verification | A check result identifying a property, inputs, assumptions, and checker | Passing a schema or an LLM critique establishes correctness. |
| Execution | Commands, attempt identities, acknowledgments, observed outcomes | A sent command or successful local return establishes the external effect. |
| Memory | Stored observations, derived beliefs, decisions, and versions | Everything in shared context has equal epistemic status. |
| Explanation | Human-readable accounts of reasoning or behavior | An explanation is independently reproducible evidence. |

These are logical roles. They need not be separate services. Independence requires an appropriate trust boundary: a policy checker sharing unrestricted credentials and mutable state with a proposer may provide little protection against compromise.

## 3. The established research map

The following mechanisms are composable layers, not mutually exclusive architectures.

| Mechanism | Strongest prior art / tradition | Appropriate information and coordination role | Principal limitation |
|---|---|---|---|
| Natural-language messages | Speech-act multi-agent systems; AutoGen [1, 19] | Unspecified concepts, interpretation, negotiation, research hypotheses, synthesis | Meaning, commitment, and confidence need interpretation; fluent agreement is not enforcement. |
| Typed state / structured outputs | Type systems, abstract data types, domain modeling; MCP schemas [20] | Stable identifiers, units, observations, decisions, explicit error variants | Correct shape does not establish correct values or a sufficient abstraction. |
| Event streams / event sourcing | Causal ordering; event histories and durable computation [6, 21] | Facts that occurred, attempts, causal lineage, audit and reconstruction | A log records what a producer emitted; omissions and external reality still need checking. |
| State machines / durable workflows | Automata, temporal specifications; Temporal [21] | Legal transitions, timers, pending work, recovery, compensation | Replay is not universal exactly-once execution; external activities require effect-aware retries. |
| Blackboard architectures | HEARSAY-II [2] | Heterogeneous knowledge sources contribute competing hypotheses to shared structured space; scheduler directs attention | Shared vocabulary, focus of control, contention, and hypothesis provenance remain design obligations. |
| Actor / message-passing systems | Actor model; Akka; Ray [22, 23] | Isolated ownership, asynchronous work, supervision, local state | Isolation does not supply global invariants, semantic agreement, or reversal of external effects. |
| Shared memory / object stores | Parallel computing; Ray; latent working memory [23, 27] | Large tensors, immutable artifacts, tightly coupled high-bandwidth computation | Aliasing, races, representation compatibility, and hidden dependencies reduce substitutability. |
| Belief / state representations | POMDPs, state estimation, abstraction theory; Agent-BRACE [9, 28] | Multiple possible worlds, partial observability, compact decision-relevant history | A compact state is sufficient only relative to the model and decisions; compression can destroy optimality. |
| Probabilistic messages | Factor graphs, sum-product, distributed sensor fusion, probabilistic programming [7, 8, 10] | Likelihoods, factors, posteriors, covariance, samples, predictive distributions | Shared evidence produces correlation; naive fusion can count the same information twice. Approximate inference has limits. |
| Constraints / capabilities | Reference monitors, least privilege, Macaroons [11, 12] | Admissible actions and delegated resource-specific rights | A constraint is not automatically enforced; credentials need binding, validation, expiration, and revocation semantics. |
| Contracts / protocol types | Design by contract, refinement, multiparty session types, IronFleet [13, 14] | Preconditions, postconditions, participant sequencing, invariants | Proofs depend on models, checked participants, and environmental assumptions. |
| Planners / search | Classical planning, optimization, constraint solving, LLM-Modulo [15] | Goals, actions, transition models, costs, proposed plans, counterexamples | Search cannot compensate for incorrect world models or missing goals. |
| Verifier / proposer systems | Proof-carrying code; runtime assurance; LLM-Modulo [15–17] | Candidate artifacts separated from bounded property checks and authorization | Checking can be as hard as solving; informal goals may lack complete independent verifiers. |
| Control / robotics | Subsumption, behavior trees, control barrier functions, ROS 2 [16, 18, 24, 25] | Sensor estimates, setpoints, envelopes, modes, deadlines, feedback | Timing and stability matter; safety guarantees are model- and disturbance-dependent. |
| Multi-agent protocols | Contract Net, joint intentions, FIPA; A2A [1, 3, 4, 26] | Task allocation, commitments, lifecycle, discovery, artifacts | Protocol compliance does not establish shared domain meaning, task success, or appropriate delegated authority. |

### Which established architectures come closest?

**HEARSAY-II** already composes heterogeneous intelligence around hypotheses and explicit control of attention rather than a conversation transcript. Its contribution is not merely shared storage: different knowledge sources can operate at different abstraction levels while control decides which hypothesis to develop [2].

**Robotics** is the closest tradition for partial observability plus consequential action. Estimation, planning, behavior selection, and feedback control operate at different rates. Subsumption provides layered reactive behaviors; behavior trees expose task status and switching; runtime assurance and barrier methods constrain an advanced controller [16, 18, 24]. These mechanisms solve different problems and should not be collapsed into one purported standard robotics architecture.

**Durable workflows and actors** are the closest production substrates for owned state and long-running work. Temporal records execution history and replays workflow logic while activities handle effects. Akka isolates actor state and supervises failures. Ray combines tasks, actors, and object references for heterogeneous computation. None guarantees that the intelligent component's conclusions are true [21–23].

**Session types and verified distributed systems** come closest to specifying interaction correctness. Multiparty session types relate global protocols to local participants; IronFleet combines distributed-system reasoning with implementation verification. These provide useful guarantees under assumptions, not universal resilience to arbitrary unmodeled failures [13, 14].

**Probabilistic graphical models** come closest when communication is itself distributed inference: local factors exchange mathematical messages with defined update rules. This is stronger than attaching an uninterpreted confidence number to prose, but requires compatible variables and factorization [7].

No single architecture combines all these guarantees. The gap is composition across their assumptions.

## 4. What actually needs to cross boundaries?

My synthesis is a small family of distinct message meanings, with domain-specific payloads:

| Meaning | Minimum consequential content |
|---|---|
| Observation | Source, subject, value and units/frame, observation time, availability time, evidence reference, quality limitations |
| Claim / belief | Proposition or state variables, alternatives or distribution where useful, evidence lineage, model/version, scope, freshness |
| Proposal / plan | Intended change, objective, preconditions, predicted effects, cost/risk estimates, state version used |
| Verification report | Exact property checked, artifact/input digest, checker/version, assumptions, result, counterexample or proof reference |
| Authorization grant | Issuer, principal/audience, resource, permitted operation, limits, expiry, policy version, delegation restrictions |
| Command / attempt | Authorized operation, attempt identity, idempotency semantics, expected state version, deadline/cancellation behavior |
| Outcome | Acknowledgment versus observed completion, actual resulting state, evidence, unresolved effects, reconciliation status |

Not every message needs every field. Apply detail in proportion to consequences. Content-addressed references can replace copying whole artifacts. Schemas must specify units, reference frames, domain definitions, and absent/unknown/null semantics. A field named `risk` or `done` is not a semantic contract.

Use prose for interpretation that cannot yet be represented adequately, preserving the source material. Use typed values for established domain facts and interfaces. Use events for history, distributions for decision-relevant uncertainty, constraints for admissibility, credentials for permission, and evidence references for checkability. A free-text rationale may accompany any of these; it should not silently change their meaning.

The key abstraction test is: **could two histories producing the same transmitted state require different correct next decisions?** If yes, the interface is missing decision-relevant information. Abstraction theory shows that preserving some policies does not necessarily preserve values, learning convergence, or planning quality [9].

## 5. Communicating uncertainty

Uncertainty should answer “uncertain about what, conditional on what, and relevant to which action?” A universal confidence field is inadequate.

Distinguish measurement noise, uncertainty about latent state, model uncertainty, distribution shift, incomplete evidence, stale data, conflicting reports, and unknown execution outcomes. Distinguish a posterior probability from a likelihood, similarity score, classifier margin, ordinal certainty label, confidence interval, or conformal prediction set. Each has different interpretation rules.

For bounded decisions, communicate the alternative labels or outcomes, calibrated probabilities or a set/interval when justified, calibration domain and version, and a typed abstention reason. Report measured calibration and selective risk, rather than making the message itself claim that it is calibrated. A decision to defer should consider error costs, escalation costs, and whether further information is obtainable.

For distributed estimation, communicate covariance or joint dependence information where available. Evidence identifiers and derivation lineage help identify repeated information. Covariance intersection offers conservative fusion under unknown correlations in its applicable estimation setting; it is not a universal rule for combining arbitrary agents' beliefs [8].

A POMDP belief represents a distribution over possible states; practical interfaces may use particles, factors, intervals, or selected hypotheses rather than an infeasible full distribution. Agent-BRACE is an instructive 2026 counterpoint: it separates belief from policy using structured natural-language claims and ordinal certainty labels. This supports role separation while weakening the claim that uncertainty must always be numerical [28].

Unknown execution outcome deserves special treatment. A timeout may mean the effect occurred but its acknowledgment was lost. Retrying is a coordination decision requiring reconciliation or an external idempotency guarantee, not a generic response to low confidence [21].

## 6. Authority and coherent coordination

Authority should follow explicit delegation rules rather than spread with context. Knowledge of a task, a high-confidence recommendation, possession of a model-generated plan, and discovery of an advertised agent skill confer no right to execute.

Least privilege and complete mediation are old security principles [11]. Macaroons demonstrate delegated credentials with contextual caveats [12]. For intelligent systems the useful pattern is narrowing delegation: resource, permitted operation, budget, time, audience, and further-delegation restrictions. One-time grants require atomic consumption; expiration alone does not prevent concurrent reuse. Authentication proves a principal or origin, not a claim's truth.

Coherence does not require every component to share identical internal beliefs. It requires agreement on the meaning of exchanged objects, ownership of state transitions, the commitments outstanding, relevant objectives, and how incompatibility is detected. A planner, classifier, controller, solver, and language model can use different internal representations if adapters preserve the properties their consumers require.

Use coordination where an invariant demands it. CALM relates coordination-free consistency to monotonic computation; invariant confluence characterizes when independently valid database changes can merge safely in its model [5]. Accumulating observations can often be decentralized. Exclusive spending, absence-based decisions, and conflicting ownership generally require additional coordination or carefully partitioned rights. A global total order for everything is unnecessarily expensive; causal order and local authoritative domains often suffice [6].

There is also no protocol that guarantees deterministic consensus termination in a fully asynchronous system with even one crash under the FLP assumptions [30]. Reliable design must make timing, failure-detector, quorum, or availability tradeoffs explicit.

## 7. Shared context: useful substrate, dangerous implicit contract

Shared context helps when components need the same source artifacts, large tensor data, common hypotheses, or coordinated exploration. A blackboard is useful when independent methods incrementally refine a shared problem. Shared latent memory can avoid repeated decoding and encoding [2, 23, 27].

Hidden coupling arises when consumers depend on undocumented prompt order, mutable shared notes, unknown update timing, another component's summary omissions, architecture-specific embeddings, or beliefs recursively derived from each other. A shared transcript can blur observation, inference, instruction, and permission. Two agents repeating one source are not two independent witnesses.

Prefer named artifacts and versioned snapshots over an ever-growing universal context. Separate authoritative records from derived belief views and exploratory scratch space. Specify who can write each namespace, which snapshot a decision used, invalidation/freshness rules, and how disagreements are represented. Preserve competing hypotheses when premature consensus would discard useful uncertainty.

Latent sharing is reasonable within compatible, tightly coupled model groups. Crossing independently governed or interchangeable components calls for an explicit external contract even if the payload contains vectors. LatentMAS's inspected extension discussion assumes compatible layer shapes and proposes adapters for heterogeneous models; its benchmark gains do not demonstrate arbitrary cross-model interoperability [27].

## 8. Properties a consequential protocol should have

1. **Semantic precision:** distinct observations, beliefs, proposals, grants, commands, and outcomes; units and domain vocabulary; versioned compatibility rules.
2. **Epistemic precision:** provenance, freshness, evidence dependencies, uncertainty meaning, explicit unknown and abstention states.
3. **Interaction precision:** permitted transitions, ownership, preconditions, commitments, deadlines, cancellation and acknowledgment semantics.
4. **Authority precision:** authenticated scoped rights, controlled delegation, enforcement at effects, policy versions, revocation strategy.
5. **Recovery precision:** attempt identities, duplicate/reorder handling, durable state where needed, replay boundaries, reconciliation of ambiguous effects.
6. **Verification precision:** property-specific checks tied to immutable inputs, explicit assumptions, counterexamples, reproducible artifacts.
7. **Operational precision:** backpressure, bounded resource use, real-time deadlines where applicable, observable failure modes.

Auditability requires reconstructing what was known, proposed, permitted, attempted, and observed. Recoverability requires knowing which work may safely resume. Composability requires substituting a component without relying on its private prompt or memory. Independent verification requires a checker able to evaluate the relevant property without merely trusting the producer's narrative. These goals can conflict with privacy, retention costs, latency, and opaque learned communication.

Signed logs establish provenance and tamper detection under a trust model; they do not prove complete recording or accurate world observation. Workflow replay reconstructs recorded decisions; it does not reproduce an uncontrolled external environment. A verifier can be statistically fallible, incomplete, or based on the wrong specification. The assurance claim must say which of these remains.

## 9. What recent agent systems rediscover—and change

AutoGen's conversations are a flexible reasoning substrate [19]. MetaGPT's standard operating procedures and artifacts move toward explicit software-process coordination [29]. A2A's inspected specification already defines task lifecycles, structured parts, artifacts, streaming, versioning, and authentication/authorization responsibilities. MCP's July 28, 2026 specification supplies tool schemas and structured results [20, 26]. It is inaccurate to describe all contemporary agents as unstructured chat loops.

These standards solve substantial interoperability problems. They do not, by themselves, establish that an artifact satisfies a domain goal, that two parties attach identical meaning to a field, or that a proposed effect has the required independent evidence. Capability advertisements must also be distinguished from security capabilities.

The 2026 semantic-protocol survey explicitly identifies this syntactic/semantic gap [31]. The MAST failure study identifies system design, inter-agent misalignment, and verification failures in collected agent traces [32]. Neither proves that prose causes the failures or that replacing it with types eliminates them. A September 2026 security systematization highlights emergent multi-agent risks; it remains a preprint synthesis, not a controlled comparison of substrates [33].

LLMs genuinely change the cost of interpreting novel instructions, translating representations, extracting tentative models, generating candidate plans and code, and explaining results. They can bridge a domain before a schema is established. They also make a message simultaneously an input datum and a potential instruction to a receiver, complicating trust boundaries. Their stochastic behavior, broad competence, context-dependent interpretation, and semantic flexibility increase the importance of explicit admission and execution contracts.

They do not abolish distributed-systems failures, the need for state estimation, resource constraints, or the difference between a proposal and a commitment.

## 10. Contradictions and limits of the hypothesis

**Language can be the best available semantic interface.** Open-ended research and changing task ontologies may lose essential meaning when forced into premature schemas. Conversation architectures demonstrate task-specific usefulness [19]. Agent-BRACE shows that a structured belief need not abandon natural language [28].

**Machine-native can mean learned rather than symbolic.** RIAL/DIAL learn communication for cooperative reinforcement learning [34]. ICML 2026 LatentMAS reports benchmark gains and lower communication/inference overhead using latent collaboration [27]. These weaken any universal typed-symbolic prescription, while leaving cross-model compatibility, governance, and audit questions open. The May 2026 HyLaT preprint explores a hybrid latent/text approach; its reported small-model evaluation does not settle large-scale deployment [35].

**Determinism is not correctness.** A wrong schema, missing state variable, invalid transition model, or incorrect invariant can fail consistently. State-abstraction results provide concrete negative examples, not merely philosophical objections [9].

**Modularity has a tax.** Translation, serialization, validation, orchestration, and extra network boundaries cost time and can discard useful information. End-to-end learned coordination or shared representations can outperform an overly rigid decomposition. Separate logical roles only where their benefits exceed these costs.

**Verification has limits.** Proof-carrying code checks defined safety policies; runtime assurance assumes a usable safety model and backup strategy [16, 17]. General factual, creative, and preference-sensitive goals may lack complete mechanical verifiers. Another general-purpose model can be useful as a critic without becoming an independent correctness oracle.

**Logs and protocols do not defeat physics or distributed uncertainty.** Durable histories cannot atomically couple every external effect to a local record. Real-time loops cannot tolerate arbitrary latency. Consensus cannot guarantee unconditional progress under the FLP assumptions [21, 25, 30].

The broad premise—“all intelligence should be separated into deterministic roles with nonlinguistic messages”—is unsupported. The narrower claim—“consequential coordination should not depend solely on interpreting unconstrained model prose”—has substantial theoretical and engineering support, but still needs controlled end-to-end evaluations in agent settings.

## 11. Unresolved research gaps and decisive comparisons

The central unresolved question is **how to discover and evolve an interface that preserves decision-relevant meaning while remaining checkable and substitutable**. Encoding a sufficient state is much harder than enforcing its schema.

Other gaps are calibrated uncertainty under interaction and shift; evidence dependence across agents; semantic contract negotiation; delegation tied to evolving plans; composition of statistical, formal, and real-time guarantees; auditable latent communication; recovery from partially observed external effects; and benchmarks measuring actual invariants and recovery rather than answer quality alone.

Three compact experiments would separate architecture from aesthetic preference:

| Experiment | Controlled comparison | What would weaken the direction? |
|---|---|---|
| Boundary representation | Same models, tools, authority checks, budget, and tasks; randomized prose versus typed domain records versus hybrid payloads. Inject ambiguity, stale evidence, schema evolution, and component replacement. | Typed boundaries fail to improve semantic errors or substitutability, or their information loss and adaptation cost dominate. |
| Coordination under faults | Same candidate proposals and evidence; conversational coordination versus owned state machine/durable workflow. Inject duplicate delivery, crashes around effects, missing acknowledgments, and conflicting grants. | Explicit coordination gives no material improvement in invariant violations, duplicate effects, unresolved outcomes, or recovery at matched overhead. |
| Rich communication versus audit | Text, typed beliefs, and compatible-model latent sharing on open-ended and bounded tasks; measure quality, latency, transfer to new components, calibration, and independent reconstruction. | Symbolic contracts cannot retain needed information economically, while richer channels preserve quality and equivalent practical assurance. |

Pre-register effect sizes, error costs, assurance properties, and noninferiority margins. Report quality, safety, calibration, recovery, latency, integration effort, and authority violations separately. Do not credit an authority gate's benefit to a change in message syntax.

## 12. Answer: architecture without the chatbot inheritance

I would use **domain-specific, versioned contracts over multiple communication mechanisms**. Components may be language models, classifiers, solvers, estimators, controllers, or learned latent collaborators. They exchange explicit observations, beliefs, proposals, check results, rights, commands, and outcomes at consequential boundaries. They retain rich local cognition and can use prose where interpretation is the task.

Owned state machines or durable workflows coordinate long-running effects; real-time feedback remains in timing-appropriate control loops; blackboards support collaborative search; probabilistic factors support estimation; immutable artifact references support large shared data. Scoped credentials constrain action independently of intellectual competence. Recorded attempts and independently observed outcomes support recovery and audit, with an explicit unresolved state when the world is uncertain.

The evidence supports this **plural, contract-centered architecture**, not a universal new wire format: blackboards demonstrate heterogeneous inference; graphical models formalize probabilistic messaging; protocol types and distributed verification establish conditional interaction guarantees; security capabilities bound delegation; workflows demonstrate durable coordination; robotics separates time-sensitive control from deliberation; recent latent results establish that efficient cognition can need richer channels [2, 7, 12–14, 16, 21, 27]. What remains unproven is the general agent-level performance advantage of combining them, and how cheaply their semantic contracts can evolve.

## Primary source register

1. Smith, **The Contract Net Protocol**, IEEE Transactions on Computers, 1980 ([paper](https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/smith80contract.pdf)); [FIPA Communicative Act Library specification](https://jmvidal.cse.sc.edu/library/XC00037H.pdf).
2. Erman, Hayes-Roth, Lesser, Reddy, **The Hearsay-II Speech-Understanding System**, ACM Computing Surveys, 1980 ([author-hosted paper](https://mas.cs.umass.edu/Documents/Erman_Hearsay80.pdf)).
3. Cohen and Levesque, **Teamwork**, 1991 ([author institute](https://www.sri.com/publication/teamwork/)).
4. FIPA specifications, above; behavioral semantics should not be mistaken for observable sincerity or policy enforcement.
5. Hellerstein and Alvaro, **Keeping CALM**, 2019 preprint / CACM 2020 ([paper](https://arxiv.org/abs/1901.01930)); Bailis et al., **Coordination Avoidance in Database Systems**, PVLDB 2014 ([paper](https://arxiv.org/abs/1402.2237)).
6. Lamport, **Time, Clocks, and the Ordering of Events in a Distributed System**, CACM 1978 ([author page](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/)).
7. Kschischang, Frey, Loeliger, **Factor Graphs and the Sum-Product Algorithm**, IEEE Transactions on Information Theory 2001 ([paper](https://web.stanford.edu/~montanar/TEACHING/Stat375/papers/sumprod.pdf)).
8. **Distributed Multisensor Data Fusion under Unknown Correlation and Data Inconsistency**, Sensors 2017 ([paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5713506/)); **Decentralized data fusion with inverse covariance intersection**, Automatica 2017 ([institutional record](https://repository.tno.nl/SingleDoc?docId=44802)).
9. Li, Walsh, Littman, **Towards a Unified Theory of State Abstraction for MDPs**, ISAIM 2006 ([author paper](https://thomasjwalsh.net/pub/aima06Towards.pdf)).
10. Cusumano-Towner et al., **Gen: A General-Purpose Probabilistic Programming System with Programmable Inference**, PLDI 2019 ([author paper](https://www.cs.cmu.edu/~fsaad/assets/papers/2019-CusumanoTownerEtAl-PLDI.pdf)).
11. Saltzer and Schroeder, **The Protection of Information in Computer Systems**, Proceedings of the IEEE 1975 ([paper](https://www.cs.virginia.edu/~evans/cs551/saltzer/)).
12. Birgisson et al., **Macaroons**, NDSS 2014 ([conference](https://www.ndss-symposium.org/ndss2014/ndss-2014-programme/macaroons-cookies-contextual-caveats-decentralized-authorization-cloud/)).
13. Honda, Yoshida, Carbone, **Multiparty Asynchronous Session Types**, POPL 2008 / extended JACM treatment ([author manuscript](https://mrg.cs.ox.ac.uk/publications/multiparty-asynchronous-session-types-jacm/jacm.pdf)).
14. Hawblitzel et al., **IronFleet: Proving Practical Distributed Systems Correct**, SOSP 2015 ([author institute](https://www.microsoft.com/en-us/research/publication/ironfleet-proving-practical-distributed-systems-correct/)).
15. Kambhampati et al., **LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks**, ICML 2024 position paper ([paper](https://arxiv.org/abs/2402.01817)). Its broad title is not treated here as a universal incapability theorem.
16. Phan et al., **Neural Simplex Architecture**, NFM 2020 ([paper](https://arxiv.org/abs/1908.00528)); Ames et al., **Control Barrier Function Based Quadratic Programs for Safety Critical Systems**, IEEE TAC 2017 ([paper](https://arxiv.org/abs/1609.06408)).
17. Necula, **Proof-Carrying Code**, POPL 1997 ([publisher](https://doi.org/10.1145/263699.263712)).
18. Brooks, **A Robust Layered Control System for a Mobile Robot**, IEEE JRA 1986 ([paper](https://jmvidal.cse.sc.edu/library/brooks86a.pdf)).
19. Wu et al., **AutoGen**, 2023 preprint ([paper](https://arxiv.org/abs/2308.08155)).
20. MCP, **July 28, 2026 specification**, [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization).
21. Temporal, [Workflow Execution](https://docs.temporal.io/workflow-execution), [Activity Execution](https://docs.temporal.io/activity-execution), current documentation inspected at cutoff.
22. Akka, [Actor Systems](https://doc.akka.io/libraries/akka-core/current/general/actor-systems.html), current official documentation.
23. Moritz et al., **Ray**, OSDI 2018 ([conference](https://www.usenix.org/conference/osdi18/presentation/moritz)).
24. Colledanchise and Ögren, **Behavior Trees in Robotics and AI**, 2017 preprint / 2018 book ([paper](https://arxiv.org/abs/1709.00084)); **Behavior Trees in Robot Control Systems**, Annual Review 2022 ([publisher](https://www.annualreviews.org/content/journals/10.1146/annurev-control-042920-095314)).
25. ROS 2, [Deadline, Liveliness, and Lifespan QoS](https://design.ros2.org/articles/qos_deadline_liveliness_lifespan.html), official design documentation.
26. A2A, [specification](https://a2a-protocol.org/latest/specification/), current specification inspected at cutoff; this unversioned URL can change.
27. Zou et al., **Latent Collaboration in Multi-Agent Systems**, ICML 2026 ([proceedings](https://proceedings.mlr.press/v306/zou26k.html)); [August 3 extended version](https://arxiv.org/html/2511.20639v4), including heterogeneous-agent discussion.
28. Singh et al., **Agent-BRACE**, May 2026 preprint ([paper](https://arxiv.org/abs/2605.11436)).
29. Hong et al., **MetaGPT**, ICLR 2024 ([paper](https://arxiv.org/abs/2308.00352)).
30. Fischer, Lynch, Paterson, **Impossibility of Distributed Consensus with One Faulty Process**, JACM 1985 ([original manuscript](https://groups.csail.mit.edu/tds/papers/Lynch/MIT-LCS-TR-282.pdf)).
31. **Beyond Message Passing: A Semantic View of Agent Communication Protocols**, April 2026 preprint ([paper](https://arxiv.org/html/2604.02369v3)).
32. Cemri et al., **Why Do Multi-Agent LLM Systems Fail?**, 2025, revised October 2025 ([paper](https://arxiv.org/abs/2503.13657)).
33. **SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems**, September 2026 preprint ([paper](https://arxiv.org/abs/2609.00595)).
34. Foerster et al., **Learning to Communicate with Deep Multi-Agent Reinforcement Learning**, NeurIPS 2016 ([conference](https://papers.nips.cc/paper/6042-learning-to-communicate-with-deep-multi-agent-reinforcement-learning)).
35. **HyLaT**, May 2026 preprint ([paper](https://arxiv.org/html/2605.25421v1)).

Repository artifacts: [SHAD0W architecture](https://github.com/jayjz/SHAD0W/blob/8e5e6f9e94dd47a7ca2a209e73d6019d51ac201f/docs/ARCHITECTURE.md); [BTC branch status](https://github.com/jayjz/SHAD0W/blob/feat/btc-paper-learning-loop/docs/STATUS.md); [TEMPER validation](https://github.com/jayjz/TEMPER/blob/0747730d18cdb692142d9c2b50f9e8bc1ff0c45f/docs/results/EXP-0001-B2-validation-2026-09-17.md); [CipherLoop validator](https://github.com/jayjz/CipherLoop/blob/f03a1e186e491cf24aa0f0e0671cac766c1fa8ab/src/cipherloop/executor/validator.py); [TraceForge](https://github.com/jayjz/TraceForge/tree/51af0f4ed2e9fb0416bffcb3f0bc8140bc1c38bd); [AetherForge server](https://github.com/jayjz/AetherForge/blob/265c26769eba257ac40540a7e1da5378d7515532/src/server.py); [Fracture runtime](https://github.com/jayjz/Fracture/blob/300ef83a0ee999857189542bd836f215490da116/src/fracture/core/runtime.py).
