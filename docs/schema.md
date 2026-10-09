# Lease Abstraction Schema v1

The shared contract between **extraction** (Contract Intelligence app) and **reasoning** (LeaseWise).
LeaseWise defines it first; the Contract Intelligence app should emit documents in this shape.
Source of truth: [`src/schema.py`](../src/schema.py).

## Document (front matter)

Each source document is one markdown file in `data/leases/` with YAML front matter.

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | str | yes | `"1.0"` |
| `doc_id` | str | yes | Stable, unique. Convention: `ABP-L-007` (lease), `ABP-L-007-A1` (amendment 1), `ABP-L-007-SL1` (side letter 1) |
| `doc_type` | enum | yes | `lease` · `amendment` · `side_letter` |
| `title` | str | yes | Human label used in citations, e.g. `Lease`, `Amendment No. 2`, `Side Letter (Rent Relief)` |
| `tenant_id` | str | yes | Stable key, e.g. `T07`. Lets "Acme" and "Acme Foods Pte Ltd" resolve to one tenant |
| `tenant` | str | yes | Registered name as written in the document |
| `property_id` | str | yes | e.g. `P1` |
| `property` | str | yes | Building name |
| `unit` | str | yes | As written, e.g. `#03-12` |
| `use` | enum | yes | `office` · `retail` · `industrial` |
| `effective_date` | date | yes | ISO `YYYY-MM-DD` |
| `amends` | str | amendments / side letters | `doc_id` of the document this one modifies. Chains are allowed (A2 may amend A1) |

## Clause (chunk)

Clauses are level-2 markdown headings with a number, a title, and an attribute tag:

```markdown
## 7. Break Option {type=break_option}
## 2. Deletion of Break Option {type=break_option modifies=7}
```

`type` is required. `modifies` (amendments and side letters only) is a comma-separated list of clause ids
in the `amends` document. Sub-clauses (7.1, 7.2) are numbered paragraphs inside the clause. Text above the first clause (parties, signing date) is kept as clause `0` ("Preamble"). Parser: [`src/corpus.py`](../src/corpus.py).
Ingestion emits one chunk per clause, carrying all document fields plus:

| Field | Notes |
|---|---|
| `clause_id` | Number as written, e.g. `7.2` |
| `clause_title` | Heading text |
| `clause_type` | One of: `parties_premises`, `term_commencement`, `rent_payment`, `rent_review`, `service_charge`, `security_deposit`, `break_option`, `renewal_option`, `assignment_subletting`, `permitted_use`, `fit_out_reinstatement`, `repair`, `insurance`, `exclusivity`, `termination`, `landlord_sale`, `purchase_right`, `turnover_reporting`, `general` |
| `modifies_clause_ids` | Amendments / side letters only: which clauses of the `amends` doc this clause changes. Feeds the MVP 4 precedence graph |

Citation format derived from these fields: `[Tenant · Title · Cl. clause_id]`.

## Why these choices

- **Stable ids alongside display names** (`tenant_id`, `property_id`): names vary across documents; ids don't. Needed for metadata filtering (MVP 2) and graph nodes (MVP 4).
- **`amends` + `modifies_clause_ids`**: precedence is explicit data, not something the LLM must infer. The graph in MVP 4 is built directly from these edges.
- **Enum `clause_type`**: lets the structured layer (MVP 3) and eval group by clause kind; extraction tools can classify into a fixed list.
