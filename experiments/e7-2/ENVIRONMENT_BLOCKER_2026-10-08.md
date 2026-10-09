# E7.2 runtime availability record — 2026-10-08

## Superseded initial finding

The frozen implementation contract requires Python 3.12.14. The initial
implementation check incorrectly treated the absence of a Windows installer
as evidence that the release source was unavailable. At that point it found:

- `uv 0.11.28` reported no managed or installed interpreter for `3.12.14`.

That finding did **not** establish that the source release was unavailable,
and must not be used to justify a version substitution.

## Corrected source verification

The official Python 3.12.14 release page identifies the release as
source-only and publishes `Python-3.12.14.tgz` with SHA-256
`6c6df908d2c3fd24e6d76869e92542abd0f33aec9dfc18df8875f89660286d43`.
The independently downloaded archive matched that SHA-256 exactly. Its
detached signature was present and referenced signing key
`7169605F62C751356D054A26A821E680E5FA6305`; the key was not locally trusted,
so this record claims checksum verification, not a completed local GPG trust
chain.

An isolated x64 Release interpreter was built from that archive in the
worktree using CPython's documented MSBuild toolset override and the installed
Visual Studio 2026 `v145` toolset. CPython warns that `v145` is not one of its
official-release toolsets; that compiler identity must remain in the runtime
manifest and the runtime must pass its targeted self-checks before it can be
used for a fit. No scientific pin was changed.

The available system interpreter was Python 3.11.15 and does not satisfy the
contract. The runner and corpus-generation paths refuse execution on it before
importing/fitting models. No development fit, consumer fit, evaluation loading,
case generation, or heldout access occurred under that mismatched interpreter.

This is a frozen-environment availability conflict, not evidence about E7.2.
The registration, thresholds, datasets, bundle design, and historical evidence
remain unchanged.

## Remaining condition before fitting

The source-built interpreter now has the required hash-locked package
environment. Historical E7 producer-state reproduction is nevertheless
blocking: the Bayes state matches, while 32 linear coefficient values differ
at roughly 1e-14. Fitting must stop until that exact-state discrepancy is
resolved; Python 3.11.15 or another patch release remains prohibited as a
substitute.
