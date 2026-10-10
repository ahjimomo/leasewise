# Model selection (2026-10-10)

Free OpenRouter models change often; re-check with `uv run python scripts/check_openrouter.py`.
Comparison: `scripts/compare_models.py`, same retrieved context for every model, questions q023 (Q3),
q031 (Q3), q048 (Q6). Only successful calls count against the free daily quota.

| Model | Result | Notes |
|---|---|---|
| nvidia/nemotron-3-super-120b-a12b:free | **Default** | Fast (1–9 s), concise, valid citations. On q023 it said "can't find" *and* cited clauses; prompt rule 4 reworded to handle partial context |
| dots-studio/dots-3-note-preview:free | Fallback 1 | Best handling of incomplete context (flagged the missing side-letter dates), but slow (5–24 s) and verbose |
| google/gemma-4-31b-it:free, gemma-4-26b-a4b-it:free | Fallbacks 2–3 | HTTP 429: rate-limited upstream by Google AI Studio during testing |
| thinkingmachines/inkling, inkling-small | Excluded | HTTP 403: "only available on agentic harnesses" |
| cohere/north-mini-code, poolside/laguna-* | Excluded | Coding-agent models |
| liquid/lfm-2.5-2.6b | Excluded | Too small for reliable citation following |
| nvidia/nemotron-3.5-content-safety | Not a generator | Candidate input/output guardrail for the MVP 3 red-team work |

**Main finding:** on both Q3 questions the side letter's operative clause (with its dates) was not
retrieved, only its preamble, so no model could tell the consent or waiver had ended. Q3 failures are
retrieval failures first. This motivates fetching amending clauses alongside the clause they modify
(MVP 4 precedence graph).

This is a smoke test (3 questions), not a verdict. The default is confirmed or replaced by the full
golden-set run.
