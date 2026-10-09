# Machine-Native Systems

**How can intelligent components communicate decision-relevant information efficiently while preserving semantic sufficiency, interoperability, adaptability under novelty, and independent verification?**

Machine-Native Systems is a public research program investigating that question through preserved literature synthesis and bounded executable comparisons. It separates intelligence, authority, execution, and evidence, and tests what information must survive component boundaries. This repository is the canonical research record.

## Current falsifiable position

Explicit semantics around consequential state changes, permissions, attempts, and evidence remain a working hypothesis, with freedom of representation inside components. They are not an established recipe for semantic sufficiency or architectural superiority. E7 materially weakened economical frozen/adaptive boundaries under learned novelty; E7.1 showed that assessment-bundle presence can interfere with use of facts already available through a hybrid boundary.

The position must weaken further if matched comparisons show no useful coherence, recovery, or substitution advantage, or if information loss and integration cost outweigh those gains. No universal wire format, general LLM-replacement result, or deployment-wide remedy has been established. See [hypotheses and evidence updates](HYPOTHESES.md).

## Research progression

Each step changes the working model; negative findings remain part of the record.

| Stage | Question | Observation / result | Change in working model |
|---|---|---|---|
| [Baseline](RESEARCH_INDEX.md) | What prior work supports separating intelligence, authority, coordination, and evidence? | Literature synthesis and selected repository inspection supported separation more strongly than universal replacement of language models; no program experiment had run. | Explicit boundary semantics became a falsifiable hypothesis, with no universal communication substrate. |
| [E4](experiments/e4-boundary/RESULTS.md) | Does representation change handoff quality at matched authority? | Controlled prose, full JSON, and hybrid full-information arms tied in 20 implemented fixtures. Compact JSON disagreed in six and duplicated effects in two, under optimistic defaults. | No typed-format superiority; preserve consequential distinctions and separate omission from default behavior. |
| [E4.1](experiments/e4-1/RESULTS.md) | Which omissions matter independently of defaults? | Fail-closed compact avoided duplicates but lost useful completion. Alternatives + attempt + status was the minimum sufficient subset among the four tested omissions. | Sufficiency is relative to this consumer, fixtures, oracle, and exact receipt model; safe nonexecution is not useful completion. |
| [E7](experiments/e7/RESULTS.md) | Can a frozen boundary and adaptive retrieval support learned novelty? | Rich context outperformed explicit, hybrid, and inventory-first adaptive arms. Hybrid supplied all supporting context, yet learned consumers often failed to use it. | Economical fixed/adaptive sufficiency weakened here; availability and use of facts are distinct. This does not establish universal explicit-boundary failure. |
| [E7.1](experiments/e7-1/RESULTS.md) | Does producer assessment interfere with contradictory context use? | Masking improved novelty in several configurations with supporting facts unchanged: causal assessment-bundle interference. Three configuration verdicts A and one D retained the preregistered pooled **D / inconclusive**. | Universal shortcut learning remains unestablished; confidence fingerprints, rendering, and fitting effects remain plausible. Masking lost some useful completion across the full set and is not a deployment-wide remedy. |

Canonical protocols: [E4](experiments/e4-boundary/PROTOCOL.md), [E4.1](experiments/e4-1/PROTOCOL.md), [E7](experiments/e7/PROTOCOL.md), [E7.1](experiments/e7-1/PROTOCOL.md). Raw artifacts, configuration, and reproduction instructions are linked from each experiment's [record](experiments/README.md).

## Current frontier

Can a learned component distinguish when producer assessments should yield to contradictory supporting context, and can that failure be diagnosed cleanly before introducing context-recovery architecture?

E7.2 was [preregistered in an immutable commit](https://github.com/jayjz/machine-native-systems/blob/3420834c6a447b4fead476858c2f9fbb1c60dcbf/experiments/e7-2/PROTOCOL.md) **before** [development-only implementation](https://github.com/jayjz/machine-native-systems/blob/02780b41bd2493e5c6617f450a2697a05e051be1/experiments/e7-2/DEVELOPMENT_PREFLIGHT.md). Its [current preflight record](https://github.com/jayjz/machine-native-systems/blob/f4cff7faab8f35e41aecfe5b3cd2a21cad65691f/experiments/e7-2/DEVELOPMENT_PREFLIGHT.md) reports a pinned runtime but a blocking exact-reproduction mismatch: 32 floating-point coefficients differ in the historical linear producer state (Bayes matches). **No E7.2 development fit, independently curated heldout evaluation, evaluation authorization, or result exists.** Those commits remain on research branches, not `main`. No context-recovery or escape-hatch architecture has been validated. See the [E7.1 postrun audit](experiments/e7-1/POSTRUN_AUDIT.json) for the motivation.

## Method and limits

- Freeze protocols and explicit falsification criteria before evaluation where used. E4/E4.1/E7 protocols were committed locally before execution and published afterward; they are not externally timestamped preregistrations. E7.1's protocol was published before implementation and evaluation creation.
- Preserve raw outputs, fitted states, checksums, negative results, deviations, and exact commit ancestry. Corrections are dated and explicit; published experiment history is not cleaned up to favor a thesis.
- Reproduce bounded implementation behavior separately from interpreting it. Valid authorization and matching receipts do not establish correct intent; determinism and passing tests do not establish general correctness.
- Search existing evidence before targeted retrieval. Keep observation, inference, causal evidence, hypothesis, and conclusion distinct.

E4/E4.1 use known scripted fixtures. E7/E7.1 use two bounded statistical text-model families, familiar generated vocabulary in novel locations, same-author cases, uncalibrated probabilities, and trusted simulated registries/receipts. Crossed executions are correlated repetitions, not independent population samples. No open-world, LLM, production, calibrated-uncertainty, or full lifecycle economics claim follows.

The October 2–3, 2026 synthesis has an October 2 local literature cutoff. Its motivating repositories share one author and are not independent replications. Original reports remain preserved; later organizational summaries do not add experimental evidence.

## Read and verify

[PUBLIC_RESEARCH_SUMMARY.md](PUBLIC_RESEARCH_SUMMARY.md) is the stable editorial source intended for `jaysystems.dev/research`; it is maintained from canonical evidence, not generated activity. The portfolio consumes it separately; no portfolio implementation or deployment code belongs here.

Read [durable questions](RESEARCH_QUESTIONS.md), [research index](RESEARCH_INDEX.md), [worklog](WORKLOG.md), and [preservation inventory](research/session/PRESERVATION_INVENTORY.md). For checks and publication ancestry, use [E4.1/E7 validation](experiments/VALIDATION.md), [E7.1 validation](experiments/e7-1/VALIDATION.md), [E7.1 publication mapping](experiments/e7-1/PUBLICATION.json), and the [dated public-program review](docs/PUBLIC_PROGRAM_REVIEW_2026-10-05.md).

Run the existing checks from the root with the [pinned dependencies](experiments/e7/requirements.txt):

```sh
python3 experiments/verify_results.py
python3 experiments/e7-1/verify.py
python3 -m unittest discover -s experiments/e4-boundary -p test_harness.py -v
python3 -m unittest discover -s experiments/e4-1 -p test_harness.py -v
python3 -m unittest discover -s experiments/e7 -p 'test_*.py' -v
python3 -m unittest discover -s experiments/e7-1 -p 'test_*.py' -v
sha256sum -c research/session/SHA256SUMS
```

These commands validate existing records and replay frozen outputs. They do not create a new experiment or overwrite the canonical runs.
