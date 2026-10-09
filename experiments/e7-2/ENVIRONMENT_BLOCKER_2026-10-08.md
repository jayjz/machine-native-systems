# E7.2 runtime blocker — 2026-10-08

The frozen implementation contract requires Python 3.12.14. On this date the
pin could not be obtained from either source consulted by the implementation:

- `uv 0.11.28` reported no managed or installed interpreter for `3.12.14`.
- The official `https://www.python.org/ftp/python/3.12.14/` endpoint returned
  HTTP 404, and the Python Windows release index does not list 3.12.14.

The available interpreter is Python 3.11.15 and does not have the required ML
packages. The runner and corpus-generation paths therefore refuse execution
before importing/fitting models. No development fit, consumer fit, evaluation
loading, case generation, or heldout access occurred.

This is a frozen-environment availability conflict, not evidence about E7.2.
The registration, thresholds, datasets, bundle design, and historical evidence
remain unchanged.

## Proposed dated amendment for review

Before fitting, either supply an independently archived, hash-pinned Python
3.12.14 runtime that can be installed into an isolated environment, or publish
a dated amendment selecting an independently retrievable Python patch release
and requiring historical producer-state equivalence under that amended runtime.
Do not silently substitute Python 3.11.15 or another 3.12 patch release. A new
environment pin must precede any development fit and must be recorded in its
own immutable manifest.
