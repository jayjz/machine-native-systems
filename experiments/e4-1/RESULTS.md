# E4.1 run-001 — observations and limits

Protocol committed locally as `7ea4dc4` before implementation. October 4, 2026. 5,280 rows: 20 known fixtures × 33 arms × 8 adapter/version/style combinations. These are 20 cases, not 5,280 independent observations. Original E4 code and all prior artifacts are unchanged. Three adapter checks and five E4 checks passed.

## Observations

Compatible consumer (80 rows per arm; 16 useful and 12 recovery opportunities):

| Representation/defaults | Agreement | Useful | Recovery | Duplicate rows | Mean bytes |
|---|---:|---:|---:|---:|---:|
| Empty compact, optimistic | 56/80 | 12/16 | 0/12 | 8 | 217.05 |
| Empty compact, conservative | 56/80 | 0/16 | 0/12 | 0 | 217.05 |
| Conservative + alternatives | 44/80 | 0/16 | 8/12 | 0 | 238.45 |
| Conservative + attempt | 56/80 | 0/16 | 0/12 | 0 | 235.5 |
| Conservative + both | 68/80 | 4/16 | 12/12 | 0 | 256.90 |
| Optimistic + alternatives | 64/80 | 12/16 | 0/12 | 8 | 238.45 |
| Optimistic + attempt | 68/80 | 16/16 | 12/12 | 0 | 235.50 |
| Optimistic + both | 76/80 | 16/16 | 12/12 | 0 | 256.90 |
| Either + alternatives, attempt, status | 80/80 | 16/16 | 12/12 | 0 | 278.90 |
| Full reference | 80/80 | 16/16 | 12/12 | 0 | 296.25 |

Conservative empty compact avoids effects by abstaining throughout: 16 eligible completions withheld. With both restored, 12 eligible completions remain withheld; status restores those fresh proposals. Optimistic both still executes a producer-only completion claim. All arms have zero authority violations and narrow false verification. Exact outcomes and failures for every subset/version are in summary.json; strict-v1 rejects the same v2 case as E4. No producer/style disagreement appears. Rejection still counts as unavailable fields, not serialization corruption.

Both default policies have the SAME minimum sufficient subset among the four tested omissions: alternatives + attempt + status. Receipt reference is unnecessary in this exact receipt registry/policy/fixture suite. Conditional deletion witnesses: omit alternatives and ambiguity is flattened or everything is withheld; omit attempt and prior success cannot be reconciled or repeats; omit status and a claimed success becomes a fresh action or fresh proposals are withheld. Receipt identity is still independently established by lookup of attempt identity; this does not show receipts/evidence are unnecessary. The six originally transmitted fields were not ablated, so this is not a global minimum over all possible boundaries or compressed encodings.

## Interpretation and counterevidence

Fail-closed defaults alone resolve duplication without rich state. That weakens any inference from E4 that omitted information necessarily causes unsafe effects. They do not preserve useful work here. Restoring ambiguity and attempt alone is not sufficient for full behavior: producer status matters to the unchanged consumer. An optional supplied receipt reference is redundant here. Fields are not universally necessary merely because E4 named them.

H1 receives a narrow sufficient-state result, no typed/prose advantage. H4 is narrowed to attempt-linked independent lookup rather than mandatory transport of a receipt reference. H5 remains limited to scripted adapters; E4.1 tests no learned cognition. H2/H3 unchanged. Minimum depends on the fixed consumer, reliable store, known fixtures, reserved unknown sentinel and exact oracle distinction between abstained/unresolved. Alternatives-only conservative has lower agreement because missing attempt changes denied/claimed-success outcomes to unresolved; this is a decision-policy ordering cost, not an unsafe effect. No calibration, concurrency, unknown real-world effects or generalization established.

Next: freeze an interface on development tasks and measure learned heterogeneous components on novel context, with rich, explicit, hybrid and specific-information-request arms. No redesign after held-out failures.
