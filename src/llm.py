"""OpenRouter client with an ordered fallback list and per-call timing."""

import time
from dataclasses import dataclass, field

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from src.config import (
    DEFAULT_MODEL,
    FALLBACK_MODELS,
    LLM_TIMEOUT_S,
    OPENROUTER_BASE_URL,
    TEMPERATURE,
    get_api_key,
)


class LLMError(RuntimeError):
    """Every model in the fallback list failed. `attempts` explains why, for the UI."""

    def __init__(self, attempts: list[str]):
        super().__init__("All models failed: " + "; ".join(attempts))
        self.attempts = attempts


@dataclass
class LLMResult:
    text: str
    model: str
    prompt_tokens: int | None
    completion_tokens: int | None
    latency_ms: float
    fallbacks: list[str] = field(default_factory=list)  # models tried and skipped, with reason


def _client() -> OpenAI:
    key = get_api_key()
    if not key:
        raise LLMError(["OPENROUTER_API_KEY is not set"])
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=key, timeout=LLM_TIMEOUT_S, max_retries=0)


def generate(messages: list[dict], models: list[str] | None = None) -> LLMResult:
    models = models or [m for m in [DEFAULT_MODEL, *FALLBACK_MODELS] if m]
    if not models:
        raise LLMError(["no model configured (set LEASEWISE_MODEL)"])

    client = _client()
    skipped = []
    for model in models:
        t0 = time.perf_counter()
        try:
            resp = client.chat.completions.create(
                model=model, messages=messages, temperature=TEMPERATURE
            )
        except APIStatusError as e:  # 429 rate limit, 404 unavailable, 5xx provider errors
            skipped.append(f"{model}: HTTP {e.status_code}")
            continue
        except (APITimeoutError, APIConnectionError) as e:
            skipped.append(f"{model}: {type(e).__name__}")
            continue

        text = (resp.choices[0].message.content or "").strip() if resp.choices else ""
        if not text:
            skipped.append(f"{model}: empty response")
            continue
        usage = resp.usage
        return LLMResult(
            text=text,
            model=model,
            prompt_tokens=usage.prompt_tokens if usage else None,
            completion_tokens=usage.completion_tokens if usage else None,
            latency_ms=(time.perf_counter() - t0) * 1000,
            fallbacks=skipped,
        )
    raise LLMError(skipped)
