"""Lease abstraction schema (v1).

This is the canonical contract between document extraction and reasoning. The Contract
Intelligence app should emit documents in this shape so LeaseWise can ingest them directly.
See docs/schema.md for field-by-field guidance.
"""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

SCHEMA_VERSION = "1.0"


class DocType(StrEnum):
    LEASE = "lease"
    AMENDMENT = "amendment"
    SIDE_LETTER = "side_letter"


class PropertyUse(StrEnum):
    OFFICE = "office"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"


class ClauseType(StrEnum):
    PARTIES_PREMISES = "parties_premises"
    TERM_COMMENCEMENT = "term_commencement"
    RENT_PAYMENT = "rent_payment"
    RENT_REVIEW = "rent_review"
    SERVICE_CHARGE = "service_charge"
    SECURITY_DEPOSIT = "security_deposit"
    BREAK_OPTION = "break_option"
    RENEWAL_OPTION = "renewal_option"
    ASSIGNMENT_SUBLETTING = "assignment_subletting"
    PERMITTED_USE = "permitted_use"
    FIT_OUT_REINSTATEMENT = "fit_out_reinstatement"
    REPAIR = "repair"
    INSURANCE = "insurance"
    EXCLUSIVITY = "exclusivity"
    TERMINATION = "termination"
    LANDLORD_SALE = "landlord_sale"  # sale of the property, estoppel, deposit transfer
    PURCHASE_RIGHT = "purchase_right"  # tenant ROFR / option to purchase
    TURNOVER_REPORTING = "turnover_reporting"  # GTO statements, audit rights
    GENERAL = "general"  # boilerplate: notices, governing law, definitions, etc.


class DocumentMeta(BaseModel):
    """Front matter for one source document (lease, amendment, or side letter)."""

    schema_version: str = SCHEMA_VERSION
    doc_id: str = Field(description="Stable unique id, e.g. 'ABP-L-007' or 'ABP-L-007-A1'")
    doc_type: DocType
    title: str
    tenant_id: str = Field(description="Stable key; survives tenant name variants")
    tenant: str = Field(description="Tenant's registered name as written in the document")
    property_id: str
    property: str
    unit: str
    use: PropertyUse
    effective_date: date
    amends: str | None = Field(
        default=None, description="doc_id of the document this one modifies"
    )

    @model_validator(mode="after")
    def _amends_required_for_non_leases(self):
        if self.doc_type == DocType.LEASE and self.amends:
            raise ValueError("a lease cannot amend another document")
        if self.doc_type != DocType.LEASE and not self.amends:
            raise ValueError(f"{self.doc_type} must set 'amends'")
        return self


class Clause(BaseModel):
    """One clause-level chunk, carrying its parent document's metadata."""

    doc: DocumentMeta
    clause_id: str = Field(description="Clause number as written, e.g. '7.2'")
    clause_title: str
    clause_type: ClauseType
    text: str
    modifies_clause_ids: list[str] = Field(
        default_factory=list,
        description="For amendments/side letters: clause_ids in the amended doc this clause changes",
    )

    @property
    def chunk_id(self) -> str:
        return f"{self.doc.doc_id}#{self.clause_id}"

    @property
    def citation(self) -> str:
        """Citation label in the house format: [Tenant · Document · Clause]."""
        return f"[{self.doc.tenant} · {self.doc.title} · Cl. {self.clause_id}]"
