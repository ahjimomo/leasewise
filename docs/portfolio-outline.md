# Portfolio Outline — Atlas Bay Properties (fictional)

Blueprint for the synthetic corpus in `data/leases/` (all 29 documents written; this file is kept in sync).

**As-of date:** `2026-10-01`. All relative questions ("next 18 months", "current rent") are evaluated
against this fixed date so the golden set stays stable over time. Configured as `AS_OF_DATE`.

**Totals:** 4 properties · 20 tenants · 20 leases · 6 amendments · 3 side letters = **29 documents**.
(The prompt-injection lease for MVP 3 is added later as a separate document.)

## Properties

| ID | Name | Type | Notes |
|---|---|---|---|
| P1 | Harbourline Tower | Grade A office | CBD-style tower, ~S$11–12 psf/month |
| P2 | Lumen Point Mall | Suburban retail mall | Anchor supermarket + specialty; base-or-GTO rents |
| P3 | Kestrel Logistics Hub | Light industrial / warehouse | ~S$1.80–2.20 psf/month; heavy reinstatement |
| P4 | Atlas Bay Commons | Mixed use | Ground-floor retail, upper-floor office |

## Tenants and documents

Rent = base rent, S$ psf/month, excl. GST. ⚑ = planted hard case (see map below).

| T | Tenant | Prop · Unit | Use | sq ft | Rent | Lease term | Notable clauses | Other docs |
|---|---|---|---|---|---|---|---|---|
| T01 | Larchmere Analytics Pte Ltd | P1 · #18-01 | Office | 12,400 | 11.20 | 2024-03-01 → 2030-02-28 | Tenant break effective 2027-03-01 on 6 mo notice | **A1** (2025-09-15): break option **deleted**, 2 mo rent-free ⚑ |
| T02 | Calderwood & Lim LLP | P1 · #22-01–04 | Office | 18,000 | 10.80 | 2022-07-01 → 2027-06-30 | Market rent review at yr 3; renewal option | **A1** (2026-05-20): term **extended** to 2030-06-30, rent 12.10 ⚑ |
| T03 | Quorvan Capital Pte Ltd | P1 · #10-05 | Office | 3,200 | 11.50 | 2024-11-01 → 2027-10-31 | **No** break, **no** renewal ⚑ | – |
| T04 | Verdance Health Pte Ltd | P1 · #15-02 | Office | 6,500 | 10.50 | 2023-05-01 → 2026-04-30, +3 renewal | Service charge cap S$1.20 psf | **A1** (2026-03-01): renewal exercised to 2029-04-30, rent 11.40, service charge cap 1.35 ⚑ |
| T05 | Quillon Software Pte Ltd | P1 · #08-03 | Office | 2,100 | 11.80 | 2025-08-01 → 2027-07-31 | Subletting **prohibited** | **SL1** (2025-10-01): may sublet up to 30% to an affiliate for 12 months ⚑ |
| T06 | Pantrywell Supermarkets Pte Ltd | P2 · #B1-01 | Retail (anchor) | 28,000 | 9.50 or 1.5% GTO | 2022-01-01 → 2027-12-31, +6 renewal | **Exclusivity** for supermarket use, binding on any purchaser of the mall ⚑ | – |
| T07 | Kopi Lane Café Pte Ltd | P2 · #01-14 | F&B | 1,050 | 28.00 or 8% GTO | 2024-06-01 → 2027-05-31, +3 renewal | Wording near-identical to T17 ⚑ | – |
| T08 | Lumière Optics Pte Ltd | P2 · #02-07 | Retail | 800 | 24.00 | 2024-03-01 → 2027-02-28 | **Sales-performance break**: tenant may terminate if GTO < S$600k in any 12 months ⚑ | – |
| T09 | Pinewood Pharmacy Pte Ltd | P2 · #01-03 | Retail | 1,600 | 22.00 | 2025-01-01 → 2027-12-31, +3 renewal | **Exclusivity** for pharmacy (carve-out: anchor's health aisle) | – |
| T10 | Sprout & Scholar Enrichment Pte Ltd | P2 · #03-11 | Commercial school | 2,400 | 14.00 | 2025-04-01 → 2028-03-31 | A&P charge S$0.80 psf | **SL1** (2025-04-01): A&P charge **waived** for first 6 months ⚑ |
| T11 | Golden Ladle Noodle House Pte Ltd | P2 · #B1-22 | F&B | 900 | 30.00 | 2023-12-01 → 2026-11-30 | Signed **before** the retail leases Act (no Code clause) | **A1** (2025-06-01): rent cut to 26.00 for 12 months ⚑ |
| T12 | Urban Stride Footwear Pte Ltd | P2 · #01-20 | Retail | 1,300 | 20.00 | 2024-09-01 → 2027-08-31 | **No** break, **no** exclusivity, **no** renewal ⚑ | – |
| T13 | Larchmere Logistics (S) Pte Ltd | P3 · #01-01–04 | Warehouse | 42,000 | 1.85 | 2023-01-01 → 2027-12-31 | **CPI-linked** annual review (floor 0%, cap 5%) ⚑; name similar to T01 ⚑; **right of first refusal** to buy the building ⚑ | – |
| T14 | Halvorne Precision Engineering Pte Ltd | P3 · #02-05 | Light industrial | 9,600 | 2.10 | 2024-07-01 → 2029-06-30, +3 renewal | Tenant break effective 2027-07-01 on 6 mo notice (window still open at as-of date); heavy reinstatement | – |
| T15 | Polarvale Cold Storage Pte Ltd | P3 · #01-08 | Cold storage | 15,000 | 2.20 | 2025-03-01 → 2028-02-29 | – | **A1** (2026-02-01): +3,000 sq ft, new rent from 2026-04-01; **A2** (2026-03-15): amends A1, pushes date to 2026-06-01 ⚑ |
| T16 | Tidewater Packaging Pte Ltd | P3 · #03-02 | Light industrial | 5,200 | 1.95 | 2025-11-01 → 2027-10-31 | Short and simple; no renewal | – |
| T17 | Tembusu Brew Pte Ltd | P4 · #01-02 | F&B | 950 | 26.00 or 8% GTO | 2025-02-01 → 2028-01-31, +3 renewal | Wording near-identical to T07 ⚑ | – |
| T18 | Pulsewell Fitness Pte Ltd | P4 · #02-01 | Gym | 7,800 | 6.50 | 2024-02-15 → 2029-02-14 | Tenant break effective 2028-02-15; **declared deviation** from the retail Code ⚑ | – |
| T19 | Saltmarsh Design Studio Pte Ltd | P4 · #05-03 | Office | 1,800 | 8.90 | 2025-06-01 → 2028-05-31, +3 renewal | Service charge escalates 3%/yr | **SL1** (2025-06-01): service charge **frozen** at S$1.10 for 24 months ⚑ |
| T20 | Lanternfish Dental Clinic Pte Ltd | P4 · #01-05 | Clinic | 1,100 | 18.00 | 2024-05-01 → 2027-04-30 | Permitted use limited to dental | – |

## Hard-case map

| Brief §4 hard case | Where it's planted | Question type |
|---|---|---|
| Amendment changes rent | T11-A1 (temporary cut), T02-A1, T04-A1 | Q3 |
| Current figure only in a recital | T02-A1 recites the 2025 rent review (S$11.30) that no lease clause states | Q3 |
| Side-letter consent has lapsed | T05-SL1 sublet consent ran 2025-10-01 → 2026-09-30, so it has expired at the as-of date | Q2, Q3 |
| Amendment extends term | T02-A1 (moves out of the 2027 expiry set) | Q3, Q5 |
| Amendment removes break option | T01-A1 (trap for "breaks in next 18 months") | Q3, Q4 |
| Side letter waives a clause for a limited period | T10-SL1, T19-SL1, T05-SL1 | Q2, Q3 |
| Amendment chain (A2 amends A1) | T15-A1 → T15-A2 | Q3 (MVP 4 graph) |
| Sales-threshold break | T08 | Q1, Q4 |
| Index-linked rent review | T13: current rent depends on published CPI, which is not in the corpus, so the answer must explain the mechanism, not invent a figure | Q1, Q3 |
| Temporary change already ended | T11-A1 rent cut ended 2026-05-31 (current rent back to S$30.00); T10-SL1 A&P waiver ended 2025-09-30 | Q3 |
| Temporary change still running | T19-SL1 service charge frozen at S$1.10 until 2027-05-31 (lease alone implies ~S$1.133) | Q3 |
| Step rent | T06 base rent stepped from S$9.50 to S$10.20 on 2025-01-01 | Q1, Q5 |
| Missing clauses ("no such clause") | T03, T12 (also exclusivity absent everywhere except T06, T09) | Q6 |
| Similar wording across tenants | T07 vs T17 (café leases) | Q2 |
| Similar tenant names | T01 Larchmere Analytics vs T13 Larchmere Logistics | Q2 |
| Retail Code timing | T11 (pre-Feb 2024) vs T07/T08/T18 (post) | Q1 |
| Property sale: tenant purchase right | T13 has a right of first refusal (ROFR); **nobody** has an option to purchase (trap: ROFR ≠ option) | Q1, Q6 |
| Property sale: lease survives a sale | Every lease: "Sale of the Property" clause (deposit passes to purchaser, tenant signs estoppel certificate); T06 exclusivity expressly binds purchaser | Q1, Q4 |
| Turnover (sales) reporting | Retail GTO leases (T06, T07, T17): monthly sales statements, annual audited certificate, landlord audit right | Q1, Q4 |

## Quick sanity checks for Q4/Q5 (as of 2026-10-01)

- **Break options in next 18 months (to 2028-03-31):** T14 (2027-07-01), T18 (2028-02-15), T08 (any time, conditional on sales < S$600k). **Not** T01: removed by A1.
- **Leases expiring in 2027:** T03, T05, T06, T07, T08, T09, T12, T13, T16, T20. **Not** T02: extended by A1.

## Deferred (later iterations)

- **Acquisition due diligence**: a buyer or lender asking "what's the WALE and break risk if we buy Kestrel Logistics Hub?". Mostly Q4/Q5 aggregation, so it fits MVP 3's lease schedule.
- **Sale-and-leaseback**, **purchase agreements**, **tenant guarantees**: new document types; add once the schema is proven.

## Writing conventions

- Each lease follows the same numbered clause skeleton (§4 clause types), but the wording varies by
  property "template" (P1/P4 office, P2 retail, P3 industrial) so retrieval can't rely on clause numbers.
- Amendments and side letters cite the clauses they change (`modifies_clause_ids`) and restate
  the new wording, as real deeds of variation do.
- Names checked by web search (2026-10-07) for real-company clashes. Replaced: FreshMart, Kopi Corner,
  Brightshore Capital, Northwind, Arclight, Frostline, Halcyon Fitness. Remaining names had no exact match.
