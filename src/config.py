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
DISCLAIMER ="All properties, tenants, and leases are fictional. This is a demo, not legal advice."

# LLM (OpenRouter). Default model is chosen from the current free list at build time.
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.getenv("LEASEWISE_MODEL", "")
FALLBACK_MODELS = [m for m in os.getenv("LEASEWISE_FALLBACK_MODELS", "").split(",") if m]
TEMPERATURE = 0.2
LLM_TIMEOUT_S = 60

# Retrieval
DEFAULT_K = 5
RELEVANCE_THRESHOLD = 0.1  # tuned against the golden set


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
