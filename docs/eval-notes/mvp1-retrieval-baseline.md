# MVP 1 — Retrieval baseline (TF-IDF)

Run: `uv run python -m eval.run_eval --retrieval-only [--prefix]` · golden set n=55 · k=5 · 95% bootstrap CIs.
Retrieval only, so no LLM. Results in `eval/results/2026-10-09_tfidf*_retrieval.json`.

| Variant | Q1 hit@5 | Q2 | Q3 | Q4 | Q5 | All hit@5 | All recall@5 | MRR | Tenant acc. |
|---|---|---|---|---|---|---|---|---|---|
| TF-IDF, no prefix | 0.21 | 0.50 | 0.54 | 0.86 | 0.40 | 0.47 [0.32, 0.62] | 0.37 | 0.27 | 0.55 |
| TF-IDF + contextual prefix | 0.50 | 1.00 | 0.77 | 0.86 | 0.80 | 0.74 [0.62, 0.85] | 0.61 | 0.51 | 0.83 |

## Findings

1. **Without a prefix, clauses can't be told apart by tenant.** Clause text never names the tenant
   (only the preamble does), and most leases share near-identical deposit, insurance, and sale
   clauses. Q1 hit@5 is 0.21.
2. **The prefix fixes the tenant but over-weights it.** Tenant accuracy rises from 0.55 to 0.83 and
   Q2 reaches 1.00, but on Q1 the right tenant's *wrong* clauses win: short chunks such as the
   preamble repeat the tenant name, and cosine similarity favours short chunks. Planned fix:
   tenant detection + metadata filter (MVP 2), so the tenant narrows the search and the clause
   topic does the ranking.
3. **A score threshold cannot detect "not covered" questions.** Q6 top scores (0.21–0.49) overlap
   answerable ones (median 0.34): "Does Urban Stride have exclusivity?" matches Urban Stride's
   other clauses and other tenants' exclusivity clauses. The threshold stays low (0.1) to catch only
   off-topic input; refusal must come from the LLM reading the retrieved context, measured once
   generation is wired in.
4. **Q4/Q5 hit@5 flatters retrieval.** One relevant clause is enough for a hit, but these questions
   need 5–11 clauses; recall@5 is the honest number. These belong to the MVP 3 structured route.

Caveat: n per question type is 5–14, so per-type intervals are wide. Only the "All" row supports
firm comparisons.
