"""Retrieval metrics and bootstrap confidence intervals. Hand-rolled on purpose (brief §13)."""

import random
from statistics import mean


def hit_at_k(retrieved_ids: list[str], source_ids: list[str]) -> float:
    """1 if any gold clause appears in the retrieved list."""
    return float(any(r in source_ids for r in retrieved_ids))


def recall_at_k(retrieved_ids: list[str], source_ids: list[str]) -> float:
    """Share of gold clauses retrieved. Matters for multi-clause questions (Q3–Q5)."""
    return sum(s in retrieved_ids for s in source_ids) / len(source_ids)


def reciprocal_rank(retrieved_ids: list[str], source_ids: list[str]) -> float:
    for rank, r in enumerate(retrieved_ids, start=1):
        if r in source_ids:
            return 1.0 / rank
    return 0.0


def tenant_accuracy(retrieved_tenants: list[str], gold_tenants: set[str]) -> float:
    """Share of retrieved chunks that belong to a tenant the question is about."""
    if not retrieved_tenants:
        return 0.0
    return sum(t in gold_tenants for t in retrieved_tenants) / len(retrieved_tenants)


def bootstrap_ci(
    values: list[float], n_resamples: int = 2000, alpha: float = 0.05, seed: int = 0
) -> tuple[float, float, float]:
    """Mean with a percentile bootstrap (1 - alpha) interval. Fixed seed for reproducible tables."""
    if not values:
        return (float("nan"),) * 3
    rng = random.Random(seed)
    n = len(values)
    means = sorted(mean(rng.choices(values, k=n)) for _ in range(n_resamples))
    lo = means[int(alpha / 2 * n_resamples)]
    hi = means[int((1 - alpha / 2) * n_resamples) - 1]
    return mean(values), lo, hi
