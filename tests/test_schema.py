from datetime import date

import pytest
from pydantic import ValidationError

from src.schema import Clause, ClauseType, DocType, DocumentMeta


def _meta(**overrides) -> DocumentMeta:
    base = dict(
        doc_id="ABP-L-001",
        doc_type=DocType.LEASE,
        title="Lease",
        tenant_id="T01",
        tenant="Acme Foods Pte Ltd",
        property_id="P1",
        property="Harbourline Tower",
        unit="#03-12",
        use="retail",
        effective_date=date(2025, 1, 1),
    )
    return DocumentMeta(**(base | overrides))


def test_lease_cannot_amend():
    with pytest.raises(ValidationError):
        _meta(amends="ABP-L-000")


def test_amendment_requires_amends():
    with pytest.raises(ValidationError):
        _meta(doc_id="ABP-L-001-A1", doc_type=DocType.AMENDMENT, title="Amendment No. 1")


def test_citation_format():
    clause = Clause(
        doc=_meta(),
        clause_id="7.2",
        clause_title="Market Review",
        clause_type=ClauseType.RENT_REVIEW,
        text="...",
    )
    assert clause.citation == "[Acme Foods Pte Ltd · Lease · Cl. 7.2]"
    assert clause.chunk_id == "ABP-L-001#7.2"
