"""Integrity checks on the synthetic corpus. These guard the precedence links that MVP 3–4 rely on."""

from collections import defaultdict

import pytest

from src.corpus import load_corpus
from src.schema import DocType


@pytest.fixture(scope="module")
def clauses():
    return load_corpus()


def test_corpus_loads(clauses):
    assert clauses


def test_chunk_ids_unique(clauses):
    ids = [c.chunk_id for c in clauses]
    assert len(ids) == len(set(ids))


def test_amendment_links_resolve(clauses):
    docs = {c.doc.doc_id: c.doc for c in clauses}
    clause_ids = defaultdict(set)
    for c in clauses:
        clause_ids[c.doc.doc_id].add(c.clause_id)

    for c in clauses:
        if c.doc.doc_type == DocType.LEASE:
            assert not c.modifies_clause_ids, f"{c.chunk_id}: leases cannot modify clauses"
            continue
        target = c.doc.amends
        assert target in docs, f"{c.doc.doc_id} amends unknown doc {target}"
        assert docs[target].tenant_id == c.doc.tenant_id, f"{c.doc.doc_id}: tenant mismatch"
        assert c.doc.effective_date >= docs[target].effective_date
        for cid in c.modifies_clause_ids:
            assert cid in clause_ids[target], f"{c.chunk_id} modifies missing {target}#{cid}"
