# References

Real-world sources that shaped the **conventions** of the synthetic portfolio. None of these are
ingested into LeaseWise's corpus: the assistant answers only from the fictional leases, so it never
appears to give legal or regulatory advice. Links only; no third-party documents are committed.

> Summaries below are for realism in a demo. They are not legal advice and may be out of date —
> always check the primary source.

## Retail leases — Fair Tenancy Framework

| Source | What we took from it |
|---|---|
| [Lease Agreements for Retail Premises Act 2023](https://sso.agc.gov.sg/Act/LARPA2023) (in force 1 Feb 2024, per [Allen & Gledhill](https://www.allenandgledhill.com/sg/perspectives/articles/26893/sgkh-lease-agreements-for-retail-premises-act-2023-to-take-effect-from-1-february-2024)) | Qualifying retail leases (tenure ≥ 1 year, signed or renewed on/after 1 Feb 2024) must comply with the Code's leasing principles. Our retail leases are dated on both sides of this date, so some reference the Code and some don't. |
| [Code of Conduct for Leasing of Retail Premises](https://www.ftic.org.sg/code-of-conduct/) (FTIC, Version 3, 1 Nov 2023) | The Code's 11 key tenancy terms drive which clauses our retail leases contain: exclusivity, lease preparation and third-party costs, advertising & promotion and service charges, landlord pre-termination for redevelopment, sales performance, material adverse change, tenant pre-termination, security deposit, floor area alterations, building maintenance, rental structure. |
| [Lease Agreements for Retail Premises Regulations 2023](https://sso.agc.gov.sg/SL/LARPA2023-S708-2023) | Scope of qualifying premises (F&B, retail shops, clinics, commercial schools, gyms, etc.), used to decide which of our tenants are "retail" for Code purposes. |

**Design use:** post-Feb 2024 retail leases include a short clause acknowledging the Code. One lease
records a declared deviation from a key tenancy term, as a realistic, citable edge case. LeaseWise
reports what the lease says; it never judges whether a clause complies.

## Tax conventions

| Source | What we took from it |
|---|---|
| [IRAS — Stamp duty for renting a property](https://www.iras.gov.sg/taxes/stamp-duty/for-property/renting-a-property) | Lease duty at 0.4% of total rent for terms up to 4 years (4× annual rent for longer terms); supplemental agreements are dutiable on the rent increase. Leases include a stamp-duty clause allocating this to the tenant. |
| IRAS — GST (standard rate 9% from 1 Jan 2024) | Rents and service charges are quoted exclusive of GST, with GST payable on top. |

## Lending context (the user story, not the corpus)

| Source | Relevance |
|---|---|
| [Banking Regulations, Part IV](https://sso.agc.gov.sg/SL/BA1970-RG5?DocDate=20160926&ProvIds=P1IV-) | A bank's property sector exposure is capped (35% of total eligible assets). This is why CRE lending teams review leases as collateral: rent roll, weighted average lease expiry (WALE), and break risk all affect a loan's credit quality. Motivates Q4/Q5 question types. |

## Market conventions (no single source)

- Typical structures: **3+3** (3-year term with a 3-year renewal option) for office and retail; longer for anchors; 3–5 years for industrial.
- Rent quoted in **SGD per sq ft per month**; security deposit expressed in months of gross rent.
- Retail rent often **base rent or a % of gross turnover (GTO), whichever is higher**.
- **Fit-out** periods (rent-free) at start; **reinstatement** to original condition at lease end.

## Planned iteration: Regulatory context (after MVP 4)

Goal: show the relevant regulatory principle *next to* a lease clause (e.g. a retail lease's security
deposit clause alongside the Code's principle on security deposits), without judging compliance.

**Approach: versioned local snapshots, not live web search.** Live search would make evaluation
non-reproducible, invite prompt injection from web content, and blur the "not legal advice" line.

| Decision | Plan |
|---|---|
| Source registry | `data/regulatory/sources.yaml`: one entry per document with `source_id`, publisher, title, URL, version / effective date, `retrieved_on`, SHA-256 of the file |
| Storage | Files kept outside git (`private/regulatory/`) until reuse terms are confirmed for each publisher; only the registry is committed |
| Index | Separate collection from the leases, with its own citation style: `[Publisher · Title · version date · section]` |
| Routing | The MVP 3 query router decides lease vs regulation vs both; lease answers never silently mix in regulatory text |
| Updates | Re-download → diff against previous version → bump `retrieved_on` and hash → re-run eval → note in `docs/eval-notes/` |
| Guardrails | Answers present the clause and the principle side by side; no "complies / does not comply" verdicts. Red-team cases added for "is this lease legal?" prompts |
| Priority sources | Retail Code of Conduct (FTIC), Lease Agreements for Retail Premises Act 2023 and Regulations, IRAS stamp duty and GST guides. MAS Banking Regulations as lending context only |
