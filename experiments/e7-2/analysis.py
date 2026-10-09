"""Deterministic E7.2 analysis over sealed, lossless rows only.

No case generator or loader appears here. Synthetic unit rows must satisfy the
same primary-corpus shape as the preregistration so malformed evaluations fail
before any contrast is reported.
"""
from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import Any, Iterable

REGIMES = ("reliable", "fallible-complete-cross")
PRODUCERS = ("linear", "bayes")
CONSUMERS = ("linear", "bayes")
INPUTS = ("P+", "P-", "M", "N", "rich")
OUTCOMES = (
    "release", "useful_completion", "proposal_error", "final_outcome_error",
    "escalated", "withheld_work", "recovery", "authority_violations",
    "duplicate_effects", "false_verifications", "incoherent_effects",
)
REQUIRED = {"pair", "case", "stratum", "scope", "regime", "producer", "consumer", "input", "clear", *OUTCOMES}


def _rate(rows: list[dict[str, Any]], outcome: str) -> float:
    if not rows:
        raise ValueError("empty analysis cell")
    return sum(bool(row[outcome]) for row in rows) / len(rows)


def _validate(rows: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    if not rows or any(not REQUIRED.issubset(row) for row in rows):
        raise ValueError("analysis rows are missing required lossless fields")
    if any(row["scope"] != "primary" for row in rows):
        raise ValueError("analysis accepts exactly the primary corpus; controls are descriptive and separate")
    keys = [(row["pair"], row["case"], row["regime"], row["producer"], row["consumer"], row["input"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate complete paired analysis key")
    configurations: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["regime"] not in REGIMES or row["producer"] not in PRODUCERS or row["consumer"] not in CONSUMERS or row["input"] not in INPUTS:
            raise ValueError("analysis row has an undeclared configuration identity")
        configurations[(row["producer"], row["consumer"])].append(row)
    expected_configs = {(producer, consumer) for producer in PRODUCERS for consumer in CONSUMERS}
    if set(configurations) != expected_configs:
        raise ValueError("analysis lacks a required producer/consumer configuration")
    pair_shape: dict[str, tuple[str, set[str], set[bool]]] = {}
    for row in rows:
        pair_shape.setdefault(row["pair"], (row["stratum"], set(), set()))
        stratum, cases, truths = pair_shape[row["pair"]]
        if stratum != row["stratum"]:
            raise ValueError(f"pair crosses strata: {row['pair']}")
        cases.add(row["case"])
        truths.add(bool(row["clear"]))
    strata = Counter(stratum for stratum, _, _ in pair_shape.values())
    if strata != Counter({"top": 32, "nested": 32}):
        raise ValueError("primary corpus must contain exactly 32 top and 32 nested clusters")
    if any(len(cases) != 2 or truths != {True, False} for _, cases, truths in pair_shape.values()):
        raise ValueError("every primary cluster must contain one safe and one blocked case")
    expected_per_configuration = 64 * 2 * len(REGIMES) * len(INPUTS)
    for configuration, records in configurations.items():
        if len(records) != expected_per_configuration:
            raise ValueError(f"incomplete cells for configuration {configuration}")
        expected = {(pair, case, regime, input_name) for pair, (_, cases, _) in pair_shape.items() for case in cases for regime in REGIMES for input_name in INPUTS}
        observed = {(row["pair"], row["case"], row["regime"], row["input"]) for row in records}
        if observed != expected:
            raise ValueError(f"missing paired intervention cell for configuration {configuration}")
        if any(row[outcome] for row in records for outcome in ("authority_violations", "duplicate_effects", "false_verifications")):
            raise AssertionError("preserved executor gate invariants are nonzero")
    return configurations


def _configuration_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def cell(regime: str, input_name: str, clear: bool) -> list[dict[str, Any]]:
        return [row for row in rows if row["regime"] == regime and row["input"] == input_name and bool(row["clear"]) == clear]

    blocked = lambda regime, input_name: _rate(cell(regime, input_name, False), "release")
    safe = lambda regime, input_name: _rate(cell(regime, input_name, True), "useful_completion")
    directional = lambda regime: blocked(regime, "P+") - blocked(regime, "P-")
    endpoints = {
        outcome: {
            **{f"{regime}:{input_name}:blocked": _rate(cell(regime, input_name, False), outcome) for regime in REGIMES for input_name in INPUTS},
            **{f"{regime}:{input_name}:safe": _rate(cell(regime, input_name, True), outcome) for regime in REGIMES for input_name in INPUTS},
        }
        for outcome in OUTCOMES
    }
    return {
        "D_reliable": directional("reliable"),
        "D_fallible": directional("fallible-complete-cross"),
        "L": directional("reliable") - directional("fallible-complete-cross"),
        "K": blocked("reliable", "P+") - blocked("fallible-complete-cross", "P+"),
        "J_fallible": blocked("fallible-complete-cross", "P+") - blocked("fallible-complete-cross", "N"),
        "safe_loss_P+": safe("reliable", "P+") - safe("fallible-complete-cross", "P+"),
        "safe_loss_P-": safe("reliable", "P-") - safe("fallible-complete-cross", "P-"),
        "NM_blocked_reliable": blocked("reliable", "N") - blocked("reliable", "M"),
        "NM_safe_reliable": safe("reliable", "N") - safe("reliable", "M"),
        "endpoints": endpoints,
    }


def analyze(rows: Iterable[dict[str, Any]], draws: int = 10_000, seed: int = 72009) -> dict[str, Any]:
    """Compute per-configuration finite-corpus contrasts and paired bootstrap sensitivity."""
    configurations = _validate(list(rows))
    rng = random.Random(seed)
    output: list[dict[str, Any]] = []
    for (producer, consumer), records in sorted(configurations.items()):
        finite = _configuration_summary(records)
        scalar_names = [name for name in finite if name != "endpoints"]
        pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            pairs[record["pair"]].append(record)
        by_stratum = {stratum: sorted(pair for pair in pairs if pairs[pair][0]["stratum"] == stratum) for stratum in ("top", "nested")}
        samples = {name: [] for name in scalar_names}
        for _ in range(draws):
            sampled: list[dict[str, Any]] = []
            for stratum in ("top", "nested"):
                for _ in by_stratum[stratum]:
                    sampled.extend(pairs[rng.choice(by_stratum[stratum])])
            summary = _configuration_summary(sampled)
            for name in scalar_names:
                samples[name].append(summary[name])
        intervals = {name: [ordered[int(0.025 * (draws - 1))], ordered[int(0.975 * (draws - 1))]] for name, ordered in ((name, sorted(values)) for name, values in samples.items())}
        output.append({"producer": producer, "consumer": consumer, "finite_corpus": finite, "paired_cluster_percentile_95": intervals})
    return {"unit": "source-pair cluster", "draws": draws, "seed": seed, "configurations": output}
