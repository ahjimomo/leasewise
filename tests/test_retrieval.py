import pytest

from eval.metrics import bootstrap_ci, recall_at_k, reciprocal_rank
from src.ingest import build


@pytest.fixture(scope="module")
def retriever():
    return build(contextual_prefix=True)


def test_retrieve_returns_ranked_chunks(retriever):
    results = retriever.retrieve("security deposit", k=5)
    assert [r.rank for r in results] == [1, 2, 3, 4, 5]
    assert results[0].score >= results[-1].score


def test_tenant_filter(retriever):
    results = retriever.retrieve("security deposit", k=5, filters={"tenant_id": "T07"})
    assert results and all(r.clause.doc.tenant_id == "T07" for r in results)


def test_metrics():
    assert reciprocal_rank(["a", "b", "c"], ["c"]) == pytest.approx(1 / 3)
    assert recall_at_k(["a", "b"], ["a", "x"]) == 0.5
    m, lo, hi = bootstrap_ci([1.0, 0.0, 1.0, 1.0])
    assert lo <= m <= hi
