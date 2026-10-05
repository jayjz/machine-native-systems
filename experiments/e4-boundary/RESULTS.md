# E4 run-001: observations, interpretation, and limits

Date: October 4 UTC / October 3 local, 2026. Protocol was committed locally before implementation as `5f3b243`. Research base: `760697b40d2946647a5a69301f4ad34bfc07e2e8`. No external research or model calls. Input hashes and exact Python/platform configuration are in `results/run-001/configuration.json`.

## Observations

20 unique fixtures × 4 arms × 2 scripted producer implementations × 2 consumer versions × 2 styles = 640 rows. These are repeated factorial fixture executions, not 640 independent sampled tasks. Five trust-boundary/integrity checks passed before the run.

For the version-compatible consumer (four executions per unique fixture):

| Arm | Oracle agreement | Useful completion | Correct recovery | Duplicate-effect rows | Mean bytes |
|---|---|---|---|---|---|
| Controlled prose, full information | 80/80 | 16/16 | 12/12 | 0 | 354.8 |
| JSON, full information | 80/80 | 16/16 | 12/12 | 0 | 296.25 |
| Hybrid, full information | 80/80 | 16/16 | 12/12 | 0 | 333.85 |
| Compact JSON | 56/80 | 12/16 | 0/12 | 8 | 217.05 |

At unique-fixture level, full arms agree on 20/20; compact agrees on 14/20 and duplicates an effect in 2/20. All 640 rows report zero unauthorized effects and zero false verification under the defined property-specific audit. Producer/style replacements and replay have zero decision disagreements; this does not imply correctness, since compact's wrong decisions repeat consistently.

Compact disagrees on unknown alternatives, ambiguity, producer-only success claim, lost acknowledgment, unresolved prior effect, and foreign receipt. Dropped fields/defaults make it treat each as a fresh unambiguous proposal. Lost-acknowledgment and unresolved-effect cases create a second effect using a different attempt key. The independent gate still sees a valid scoped release grant; duplicate or epistemically inappropriate execution is not the same metric as credential misuse. The generated new receipt really matches the artifact, so this is not false completion verification under our narrow definition.

The v1-only consumer safely rejects breaking v2 messages in all formats. It therefore loses one useful case (four repeated rows) relative to the compatible consumer. Its oracle is adjusted to require safe version rejection; 80/80 agreement must not obscure that compatibility tax. Both consumers reject unsupported v3.

The `field_loss` aggregate includes rejected messages: full compatible arms have 40 unavailable fields from four v3 rejections, not lost serialization content. Compact has those same 40 plus 40 changed/defaulted fields across accepted rows. V1-only adds another 40 unavailable fields for v2. Report rejection separately from corruption.

JSON-full is smaller and decodes faster in this implementation. Recorded median timing is a single-process microbenchmark with fixed order, tiny durations and no neural inference. It is not a stable deployment latency or dollar-cost result. Compact is smaller still but performs extra registry reads (312 versus 224 for compatible full arms, including replay) while failing the oracle.

## Interpretation and hypothesis evidence

- **H1:** No full-format superiority established. A controlled prose contract matches typed and hybrid contracts. These observations materially weaken a claim that nonlinguistic encoding is necessary here. They do not compare contracted versus uncontracted systems.
- **H2:** Scripted proposer replacement requires no authority bypass; no credential violations observed. The shared gate makes this largely a mechanism check, not evidence for a format advantage or a universal security guarantee.
- **H4:** Retaining attempt identity supports receipt reconciliation in these fixtures. Omitting it can repeat an effect despite honest new receipts and valid grants. This is a reliable simulator, not distributed durable execution.
- **H5:** The full formats support the two authored producer adapters and field-order variations. Version compatibility is explicit and has a measurable useful-work cost. Different containers are not different learned intelligence; no broad interoperability result follows.
- **H3:** Not tested.

The result is negative for a typed-format advantage and narrower positive evidence for preserving distinctions between unknown/absent, proposed/completed, and new/prior attempts. Correct credential enforcement and truthful artifact receipts alone do not guarantee coherent intent or exactly-once effects.

## Confounds and limitations after inspection

Full encode/decode paths were designed to preserve the same finite semantic fields and feed the same policy. Their tie is expected by construction; this run demonstrates an executable comparison and exposed information-loss failures, not a novel causal discovery. The compact defaults are optimistic by design, biasing the ablation toward unsafe repetition. A fail-closed compact protocol might avoid those errors while sacrificing useful completion. This rival was not tested and cannot be dismissed.

Fixtures are hand-authored, visible during coding, small, and selected for these semantics. There is no blind held-out evaluation, natural-language extraction, calibrated uncertainty, real model replacement, independent consumer author, measured integration labor, or distribution shift. Scripted producer containers change no reasoning capabilities. Authority and evidence registries are trusted. The consumer can see current revision; stale-data detection is straightforward. Recovery is in-memory with an exact receipt store. No persistent journal, process crash, concurrent consumer, revoked grant race, or network failure is modeled. Timing/order and definitions constrain every assurance claim.

The audit of false verification checks artifact identity and receipt agreement, not that ambiguous human intent was satisfied. Zero on this metric must not hide compact's semantic mistakes. Defaulting missing context is the tested policy choice, not an unavoidable consequence of a shorter JSON record.

## Single next experiment justified

**One-field restoration versus conservative missing-state semantics.** Keep these fixtures/gate/consumer fixed; compare compact with fail-closed unknown defaults against compact with only ambiguity restored, only prior-attempt identity restored, and both restored. Predeclare a safe/useful tradeoff: if conservative compact achieves zero duplicate effects and full useful completion without those fields, reject their claimed necessity in this domain; if only specific restorations recover useful work without unsafe repetition, identify that minimum sufficient boundary. This isolates omission from optimistic defaults before spending on model behavior or a framework.

No disappointing result was reclassified as proof of the leading thesis. No implementation was tuned after run-001.
