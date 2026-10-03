# Repository inspection findings retained from the Work investigations

This consolidates already gathered observations and limitations. It is not a fresh repository audit, test run, or updated status report. Full citations and revision provenance are preserved in both imported reports.

## SHAD0W

Default snapshot `8e5e6f9e94dd47a7ca2a209e73d6019d51ac201f` (September 20). Architecture separates strategy proposals, risk authority, execution lifecycle, and timestamp availability. The inspected risk gate uses a process-local lock and atomic decide/reserve/issue/consume flow. This is not a distributed persistent authority proof or proof of broker state. Grant consumption does not itself establish fresh external submission conditions.

Separately inspected `feat/btc-paper-learning-loop`, including its README and canonical `docs/STATUS.md`. Journal-before-dispatch and broker-authoritative reconciliation distinguish FLAT, ENTRY_PENDING, HOLDING, EXIT_PENDING, UNRESOLVED, and HALTED. The bounded session restricts entry/exit attempts and avoids automatic retries on uncertain submission. Operational PAPER_SOAK has different, explicitly weaker fee-finality semantics; synthetic validation is not proof of strict real-crypto fee finality. README and status claims must not be flattened together. The branch reference is mutable and no exact BTC branch head was retained in the imported memo.

**Research implication:** strategy confidence, permission, committed intent, and observed external state must remain distinguishable. **Limit:** no comparative architectural superiority was established.

## TEMPER

Snapshot `0747730d18cdb692142d9c2b50f9e8bc1ff0c45f` (September 17). EXP-0001-B2 result record reports frozen BERT mean validation macro F1 0.9538719 versus B1 0.886399 on CLINC150. These are reported results; external predictions were not recomputed. Result documentation supersedes stale B2-next README text.

Calibration, out-of-scope behavior, untouched final-test comparison, general-purpose LLM comparison, and full cost per verified correct decision were not demonstrated by the inspected validation. Valid output, correctness, normalized probabilities, calibration, and safe action are distinct properties.

**Research implication:** specialist feasibility deserves controlled comparison with deferral and lifecycle cost. **Limit:** the complete deployment thesis remains untested.

## CipherLoop

Snapshot `f03a1e186e491cf24aa0f0e0671cac766c1fa8ab` (September 7). Inspected `src/cipherloop/executor/validator.py`: simple intra-procedural AST source-to-sink tracing, fixed confidence 0.9, syntax-error path returning no finding. Limited taint evidence does not prove exploitability. Broad README/fallback descriptions should not substitute for actual analysis semantics. The trajectory ledger distinguishes raw output from compressed context.

**Research implication:** evidence should state its property and analysis limits. **Limit:** fixed confidence is not calibration and a bounded checker is not a general security oracle.

## TraceForge

Snapshot `51af0f4ed2e9fb0416bffcb3f0bc8140bc1c38bd` (September 14). Original baseline has two scripted cases. Production-v2 ingestion independently checks capture integrity/source references without importing CipherLoop or judging general task success. A real preflight error was ingested; a successful live production audit was not demonstrated in the inspected material. General trajectory rubric scoring was not implemented.

**Research implication:** evidence ingestion and evaluation can be logically independent. **Limit:** capture integrity is not task correctness.

## AetherForge

Snapshot `265c26769eba257ac40540a7e1da5378d7515532` (August 23). Inspected `src/server.py`: explicit swap/I/O/generation timing comparison, queue semaphore, thermal watchdog hysteresis, structured admission failures. Mock safety validation does not validate experimental real-hardware fast swaps.

**Research implication:** resource admission and feedback are natural bounded control tasks. **Limit:** analytical rules and mocks do not establish operating-condition stability or performance.

## Fracture

Snapshot `300ef83a0ee999857189542bd836f215490da116` (August 18). README proposes pipeline/supervisor/diamond comparisons, tool and partial-result failures, state corruption, goal drift, timeout/cost failures, and schema/code-anchor/model-critic verification. Inspected `src/fracture/core/runtime.py` still raises `NotImplementedError`.

**Research implication:** topology and verifier choice can be tested by controlled fault injection. **Limit:** planned comparisons and commit descriptions are not completed measurements.

## Cross-artifact caution

These artifacts share one author and are not independent replications. The investigation sampled sources rather than exhaustively auditing 90 days of history. No source repository's tests were run during the research. Later memories of test counts or session results were not imported as newly verified facts.
