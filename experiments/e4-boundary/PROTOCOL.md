# E4. Artifact-release handoff — protocol v1

Written before harness implementation/run, October 4 UTC / October 3 local, 2026. Canonical research base: `760697b40d2946647a5a69301f4ad34bfc07e2e8`. No new external retrieval is needed: the gap is an executed boundary comparison, not additional literature.

## Selection

| Existing proposal | Information / effort assessment |
|---|---|
| E1 | Needs data, models, calibration and lifecycle cost; high cost for a first boundary test. |
| E2 | Cheap, but largely tests a gate already encoded in prior repositories; confounds cognition with enforcement unless factorial. |
| E3 | High-value abstraction test; source-analysis oracle and semantic task add implementation effort. |
| E4 | Cheapest direct comparison of semantics, representation, replacement and evolution; selected. |
| E5 | Useful but adds durable execution and crash machinery; use a small ambiguous-outcome subset here. |
| E6 | Latent interoperability requires models/runtime; premature before an executable external boundary. |

This selection is an engineering judgment, not a measured information-gain calculation. Tests H1/H5 primarily, with narrow H2/H4 checks; no H3 model-specialization claim.

## Boundary and scope

Producer: proposes release of a synthetic artifact after reviewing a private local representation. Consumer: admits, executes and reconciles the proposed release in an in-memory simulator. A separate trusted authority registry supplies rights; an independent evidence/receipt registry supplies observations. Nothing is published externally by the experiment.

Required semantic payload: schema version; target identity and digest; observed revision; evidence references; alternatives/ambiguity; prior attempt identity; producer-reported status; receipt reference; grant reference. An optional explanation is nonauthoritative. Missing is explicitly distinct from known absent. A previous attempt requires reconciliation before a new effect.

Must NOT cross implicitly: rights from prose or confidence; evidence from a producer's completion claim; certainty from one selected target when alternatives remain; private producer memory; current state inferred from an old observation; permission extended by a claimed grant. Registry validation remains identical across arms.

Producer internals are unrestricted. Two deterministic stand-ins use different internal forms: predicate-oriented state and graph/list-oriented state. Only adapters implement each boundary; neither consumer reads those private states. Two consumers are compared: v1-only and version-compatible v1/v2. Two styles change field order and rationale; no consumer-specific modifications per case are allowed. This is substitutability of scripted adapters, not a test of neural intelligence.

## Competing arms

1. **Prose-full:** strong baseline, controlled-language clauses carrying every semantic field. The language is deliberately parseable and has an explicit grammar; this is not unconstrained conversation.
2. **Typed-full:** JSON carrying the same semantic values.
3. **Hybrid-full:** typed envelope plus controlled-prose context for uncertainty, attempt and status; same information.
4. **Typed-compact ablation:** identical typed syntax but omits alternatives, attempt identity, status and receipt. Deliberately unequal information; isolates compression, not JSON versus prose.

All arms share one decision policy, registry, recovery mechanism and action budget. No role or implementation gets privileged access to the fixture oracle.

## Fixtures and adversaries

Hand-authored finite suite with explicit expected next action/outcome: ordinary completion; unknown/missing input; missing evidence; ambiguity; stale observation; conflicting evidence; digest mismatch; fabricated/expired/wrong-scope grants; producer-only success claim; prior successful attempt with lost acknowledgment; unresolved attempt; denied target; rationale injection; additive schema change; breaking v2 evolution; unsupported v3. Invalid grant and false evidence cases must fail closed. Compatible consumer may accept v2; v1-only must reject it. New wire version is not silently inferred.

No held-out statistical generalization claim: fixtures are known during implementation. Publish fixtures, oracle and raw rows. Do not tune away failures after evaluation. Repairs are limited to independent receipt lookup by supplied attempt/receipt identity; no missing-input reconstruction or unlimited retries. Re-run the same payload once with a fresh consumer to test replacement/recovery.

## Measures

- Semantic loss: decoded semantic-field mismatches/missing values against the producer's public semantic snapshot; producer-private state excluded.
- Useful completion: expected release or previously completed release confirmed; separately report abstention and exact oracle agreement.
- Incorrect authority transfer: any executed release absent valid scoped fresh grant in authoritative registry; count as violations, not merely rejected suggestions.
- False verification: consumer declares verified completion without an independently matching receipt and artifact evidence.
- Recoverability: recovery cases confirmed or kept unresolved correctly after consumer replacement; duplicate effects separately measured.
- Interchangeability: paired decision and evidence-status disagreement across producers/styles; version-compatible versus v1-only reported separately.
- Latency: encode/decode/consumer wall time per row; informational only at microbenchmark scale.
- Cost: payload UTF-8 bytes, registry reads, simulator effects, model/API calls (zero); no invented dollar or token cost.

## Explicit weakening/falsification outcomes

- If equal-information prose matches typed/hybrid in semantics, useful completion, recovery and replacement, this rejects any local claim that nonlinguistic encoding is necessary. It does not falsify H1 because prose here has a contract.
- If full typed/hybrid loses useful work or increases semantic errors relative to full prose, explicit structured encodings receive negative evidence for this boundary.
- If every variant is equivalent, no superiority claim is warranted.
- If compact performs equally despite omitted fields, those fields are not shown necessary by this suite. If it fails, that only supports retaining those specific distinctions here.
- Any unauthorized effect, false verification, or duplicate effect in full arms weakens the implemented boundary guarantee. Any proposer-specific bypass weakens H2/H5.
- Rejection of evolved but semantically equivalent data shows compatibility tax, not proof the data was unsafe.

## Confound review before implementation

Controlled prose has a formal contract, so this cannot test contract versus no contract. Shared gate forces authority protection across all formats; zero violations cannot establish a representation benefit. Compact has less information by design. Scripted components are cheap but do not model semantic extraction errors, novel natural language, latent cognition or distribution shift. Oracle and policy share a specified synthetic world; independent labels and gate-verifier checks reduce coding errors but cannot remove design bias. Small chosen fixtures do not estimate prevalence or causal effects in deployment. Timing is noisy; bytes are not lifecycle cost. Recovery uses a reliable simulator receipt store, not broker uncertainty or a durable distributed log. Schema adapters are hand-authored. No statistics implying population inference will be reported.

Smallest justified next step will be selected from the result, without changing this protocol to preserve the thesis.
