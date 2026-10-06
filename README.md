# LeaseWise

AI assistant for Commercial Real Estate Services (CRES) teams that answers questions across a portfolio of commercial leases — and cites the exact clause behind every answer.

> **All properties, tenants, and leases are fictional. This is a demo, not legal advice.**

**Status:** MVP 1 in progress. Full brief: [docs/cres-lease-portfolio-assistant-brief.md](docs/cres-lease-portfolio-assistant-brief.md) · Data contract: [docs/schema.md](docs/schema.md)

## Quick start

```bash
uv sync
cp .env.example .env   # add your OPENROUTER_API_KEY
uv run python -m src.ingest
uv run streamlit run app.py
```

Run tests: `uv run pytest`

## Results

_One row per iteration, one column per question type. Populated by `eval/run_eval.py`._

| Iteration | Q1 Lookup | Q2 Tenant | Q3 Precedence | Q4 Filter | Q5 Aggregate | Q6 Not covered |
|---|---|---|---|---|---|---|
| MVP 1 (TF-IDF) | – | – | – | – | – | – |
