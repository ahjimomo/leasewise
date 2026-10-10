"""Central configuration. Secrets come from .env locally or Streamlit secrets when deployed."""

import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
LEASES_DIR = ROOT / "data" / "leases"
INDEX_DIR = ROOT / "index"
EVAL_DIR = ROOT / "eval"

LANDLORD_NAME = "Atlas Bay Properties"
# Fixed "today" for the synthetic portfolio, so date-relative answers and the golden set stay stable.
AS_OF_DATE = date(2026, 10, 1)
DISCLAIMER = "All properties, tenants, and leases are fictional. This is a demo, not legal advice."

# LLM (OpenRouter)
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# Picked from the free list on 2026-10-10 (see docs/eval-notes/model-selection.md). Env vars override.
DEFAULT_MODEL = os.getenv("LEASEWISE_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")
FALLBACK_MODELS = [
    m
    for m in os.getenv(
        "LEASEWISE_FALLBACK_MODELS",
        "dots-studio/dots-3-note-preview:free,google/gemma-4-31b-it:free,google/gemma-4-26b-a4b-it:free",
    ).split(",")
    if m
]
TEMPERATURE = 0.2
LLM_TIMEOUT_S = 60

# Retrieval
DEFAULT_K = 5
RELEVANCE_THRESHOLD = 0.1  # filters off-topic input only; Q6 scores overlap answerable ones (see eval notes)


def get_api_key() -> str | None:
    """Prefer env var; fall back to Streamlit secrets when running on Community Cloud."""
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    try:
        import streamlit as st

        return st.secrets.get("OPENROUTER_API_KEY")
    except Exception:
        return None
