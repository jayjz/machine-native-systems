"""Deterministic, development-tested E7.2 analysis; no corpus construction/loading."""
from __future__ import annotations

import random
from collections import defaultdict
from typing import Any, Iterable


def _rate(rows: list[dict[str, Any]], field: str) -> float:
    if not rows:
        raise ValueError("empty analysis cell")
    return sum(bool(row[field]) for row in rows) / len(rows)


def _cell(rows: list[dict[str, Any]], regime: str, input_name: str, clear: bool) -> list[dict[str, Any]]:
    output = [row for row in rows if row["regime"] == regime and row["input"] == input_name and bool(row["clear"]) == clear]
    if not output:
        raise ValueError(f"missing analysis cell: {regime}/{input_name}/{clear}")
    return output


def analyze(rows: Iterable[dict[str, Any]], draws: int = 10_000, seed: int = 72009) -> dict[str, Any]:
    """Compute finite-corpus E7.2 contrasts using source-pair clusters only."""
    observations = list(rows)
    required = {"pair", "stratum", "regime", "input", "clear", "release", "useful_completion"}
    if not observations or any(not required.issubset(row) for row in observations):
        raise ValueError("analysis rows are missing required lossless fields")
    keys = [(row["pair"], row["regime"], row["input"], bool(row["clear"])) for row in observations]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate analysis intervention key")
    pairs = defaultdict(list)
    for row in observations:
        pairs[row["pair"]].append(row)
    by_stratum = defaultdict(list)
    for pair, members in pairs.items():
        strata = {member["stratum"] for member in members}
        if len(strata) != 1:
            raise ValueError(f"pair crosses strata: {pair}")
        by_stratum[next(iter(strata))].append(pair)
    if set(by_stratum) != {"top", "nested"}:
        raise ValueError("paired bootstrap requires top and nested strata")

    def contrasts(sample: list[dict[str, Any]]) -> dict[str, float]:
        b = lambda regime, input_name: _rate(_cell(sample, regime, input_name, False), "release")
        u = lambda regime, input_name: _rate(_cell(sample, regime, input_name, True), "useful_completion")
        d = lambda regime: b(regime, "P+") - b(regime, "P-")
        return {
            "D_reliable": d("reliable"),
            "D_fallible": d("fallible-complete-cross"),
            "L": d("reliable") - d("fallible-complete-cross"),
            "K": b("reliable", "P+") - b("fallible-complete-cross", "P+"),
            "J_fallible": b("fallible-complete-cross", "P+") - b("fallible-complete-cross", "N"),
            "safe_loss_P+": u("reliable", "P+") - u("fallible-complete-cross", "P+"),
            "safe_loss_P-": u("reliable", "P-") - u("fallible-complete-cross", "P-"),
            "NM_blocked_reliable": b("reliable", "N") - b("reliable", "M"),
            "NM_safe_reliable": u("reliable", "N") - u("reliable", "M"),
        }

    estimate = contrasts(observations)
    rng = random.Random(seed)
    samples: dict[str, list[float]] = {name: [] for name in estimate}
    for _ in range(draws):
        picked: list[dict[str, Any]] = []
        for stratum in ("top", "nested"):
            choices = by_stratum[stratum]
            for _ in choices:
                picked.extend(pairs[rng.choice(choices)])
        for name, value in contrasts(picked).items():
            samples[name].append(value)
    interval = {
        name: [values[int(0.025 * (draws - 1))], values[int(0.975 * (draws - 1))]]
        for name, values in ((name, sorted(values)) for name, values in samples.items())
    }
    return {"unit": "source-pair cluster", "draws": draws, "seed": seed, "finite_corpus_contrasts": estimate, "paired_cluster_percentile_95": interval}
