# Public-program review — October 5, 2026

This is a dated administrative and editorial review of the existing public record, not a new experiment or a revision of experiment history. Canonical reviewed research tip: `2b9a04cf0920b54f7b994e2e2b67b5707d5192e6`. GitHub metadata confirms `jayjz/machine-native-systems` is public, with default branch `main`. Work used a fresh public clone; its initial local main matched remote main and had a clean working tree.

## Exact ancestry and integration

After fetching origin, `git ls-remote --heads origin` and local remote-tracking refs agreed:

| Ref | Exact SHA | Commits added since preceding row |
|---|---|---:|
| Local main / origin/main | `760697b40d2946647a5a69301f4ad34bfc07e2e8` | baseline |
| research/e4-boundary-handoff-20261004 | `dffa582a3fe7f2445617e22a87d4c7ed2c0ea480` | 2 |
| research/e4-1-e7-semantic-sufficiency | `bf1003f3fdde28c3d518f661ce45aa8a42c08cdd` | 5 |
| research/e7-1-belief-shortcut | `2b9a04cf0920b54f7b994e2e2b67b5707d5192e6` | 4 |

Every adjacent merge base equals the preceding row's SHA. Left/right counts are respectively `0/2`, `0/5`, and `0/4`; the accumulated research tip is eleven commits ahead of main, zero behind. These are strict descendants, not divergent alternatives. The history also retains initialization `0f91f15f524f1a768387f0b050f2cd1549661197` before main. All thirteen public commits were included in the safety scan.

The trees and full protocols/results confirm that E7.1 contains E4 → E4.1 → E7 → E7.1. E4 files and imported research are unchanged between E4 and E7.1; E4/E4.1/E7 files and imported research are unchanged between the E7 and E7.1 tips. E4.1/E7 publication mappings remain in [prior validation](../experiments/VALIDATION.md); E7.1 mappings remain in [PUBLICATION.json](../experiments/e7-1/PUBLICATION.json). Local prepublication SHAs recorded in those files are not substituted for canonical remote commits.

`research/public-program-integration` starts at the exact E7.1 tip and adds only public-program documentation and ignore rules. No experiment, preregistration, result, configuration, source, or imported research file is modified by this preparation. The stale private-only instruction is corrected in AGENTS; historical records that describe the original private creation request remain intact. Historical next-step statements in earlier experiment entries are superseded by later dated entries, not silently rewritten.

Proposed integration: review this complete branch against main, then use a fast-forward if main is still its ancestor, or a regular merge commit through a PR. Preserve all experiment and protocol commits; do not squash or rebase the published research line for tidiness. If main advances, fetch and recheck ancestry before selecting the integration operation. This preparation does not push, open a PR, merge, force-push, deploy, or rewrite history. Publication and merging remain pending authorization.

## Public-safety scope and findings

A fresh scan covered all advertised/fetched public branch histories, all 101 unique historical file blobs, commit messages/identities, tracked paths, and the working tree including new public documents. All six historical gzip blobs were decompressed and scanned: E4/E4.1/E7/E7.1 raw rows plus E7.1 training rows and model state. No tar/zip archive payloads were found. Configuration/result JSON, logs, environment records, the saved session transcript, and `.gitignore` were reviewed.

Patterns covered recognizable AWS, GitHub, OpenAI/Anthropic, Slack and Google key/token forms, bearer tokens, private-key headers, JWTs, credential/secret/password assignments, environment/key filenames, email addresses, local-machine paths, URL userinfo, and local/private-network URLs. URL hosts were inventoried. Manual follow-up reviewed path and identity hits, the full preserved research-session transcript and provenance notes, configuration/environment records, the reproduction failure log, and broad secret/session/private-context keyword matches. GitHub metadata confirmed that all six motivating repository URL targets are currently public: SHAD0W, TEMPER, CipherLoop, TraceForge, AetherForge, and Fracture.

**No actual credential, sensitive secret, private URL, or unrelated conversation/session material was found within this scope.** Identity hits are GitHub noreply commit identities. Path hits describe nonsecret hosted-runtime executable/library locations and a scratch path in the preserved test-discovery traceback. Platform, package, thread, and architecture records are reproducibility metadata, not private runtime configuration. `libfile_` identifiers in the preservation inventory describe lineage; they are not credentials or public access links. The transcript is incomplete but directly related to this research, as the original inventory states; it is not an unrelated session dump.

The initial ignore file covered only Python cache files. Added environment-file, virtual-environment, private-key, AWS-directory, and SSH-directory exclusions reduce accidental future staging. Ignore rules do not detect secrets embedded in otherwise valid artifacts and do not remove anything already tracked. No evidence was deleted or redacted.

This is pattern scanning plus scoped manual review, not universal secret detection. It covers the public refs advertised at review time, not deleted/unreachable GitHub objects, external artifact stores, or future commits. Earlier new-artifact scan statements were not treated as sufficient coverage for this audit. There was no discovered secret requiring rotation, revocation, or history remediation.

## Existing validation rerun

Validation environment: Python 3.12.3, GCC 13.3.0; isolated environment with repository-pinned scikit-learn 1.8.0, NumPy 2.3.5, SciPy 1.17.0, joblib 1.5.3, threadpoolctl 3.6.0. Original execution used Python 3.12.14/Clang; successful checks here do not erase that environment difference. No new cases, parameter tuning, interventions, or run-output directories were created.

Commands below were run from the repository root; learned-model commands used the isolated environment's Python. All exited zero:

| Command | Result |
|---|---|
| `python3 experiments/verify_results.py` | Compressed/decompressed checksums, configured source hashes, factorial uniqueness, and implemented aggregate checks pass: E4 640, E4.1 5,280, E7 640 rows. |
| `python3 experiments/e7-1/verify.py` | Checksums/source hashes, 7,680 unique crossed rows, all saved aggregates, manipulation checks, and causal criteria reconstructed; pooled verdict D. |
| `python3 -m unittest discover -s experiments/e4-boundary -p test_harness.py -v` | 5 checks pass. |
| `python3 -m unittest discover -s experiments/e4-1 -p test_harness.py -v` | 3 checks pass. |
| `python3 -m unittest discover -s experiments/e7 -p 'test_*.py' -v` | 5 checks pass, including exact fitted-state/dataset checks and replay of all 640 wires/requests/actions/effects; consumer probabilities compared to 12 decimal places by the existing test. |
| `python3 -m unittest discover -s experiments/e7-1 -p 'test_*.py' -v` | 6 checks pass, including exact fitted/training-state checks and all 7,680 non-timing output replays. |
| `sha256sum -c research/session/SHA256SUMS` | All six preserved research/session files pass. |
| `git fsck --full` | Complete reachable object integrity passes. |
| `git diff --check` | No whitespace errors. |

Additional review checks: ancestor membership and merge bases; exact remote tips; every previously tracked file outside README/AGENTS/.gitignore byte-identical to the reviewed E7.1 tip; relative Markdown targets and fragments in changed documents resolve; ignore patterns match representative local secret filenames; summary/README claims reviewed against full protocols/results, E7 postrun analysis, E7.1 publication/postrun audit/validation, and reconstructed result criteria. No earlier canonical experiment artifact changed.

These are existing reproduction/validation checks, not new experiments or deployment tests. E4/E4.1 validation used their existing mechanism tests and archive-integrity checks; no fresh factorial result archive was generated. Reproduction establishes the checked implementation properties, not an independently designed replication or scientific/production validation.

## Editorial conclusion and remaining uncertainty

The [public summary](../PUBLIC_RESEARCH_SUMMARY.md) preserves no E4 typed-format advantage, E4.1's conditional minimum, E7's rich-context advantage, and E7.1's causal assessment interference alongside its pooled D and confidence/fitting confounds. Masking is not described as a deployment-wide remedy. E7.2 remains proposed; diagnosis precedes any architecture redesign.

The prepared branch is structurally ready to provide the canonical portfolio source after review and authorized publication. The public default branch still contains only the baseline until integration occurs. Future portfolio work should consume a reviewed, pinned summary revision and remain separate from this repository. Generalization, calibration, lifecycle economics, the causal learning mechanism, and context-recovery architecture remain unvalidated; this documentation pass does not resolve them.
