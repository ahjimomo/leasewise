"""Question → retrieve → prompt → LLM. Returns every intermediate step for the transparency panel."""

import time
from dataclasses import dataclass

from src.config import DEFAULT_K, RELEVANCE_THRESHOLD
from src.llm import LLMResult, generate
from src.prompts import build_messages
from src.retrievers.base import RetrievedChunk, Retriever


@dataclass
class PipelineResult:
    question: str
    chunks: list[RetrievedChunk]  # what went into the prompt (above threshold)
    messages: list[dict]
    llm: LLMResult
    retrieval_ms: float


def answer(
    question: str,
    retriever: Retriever,
    k: int = DEFAULT_K,
    threshold: float = RELEVANCE_THRESHOLD,
    models: list[str] | None = None,
) -> PipelineResult:
    t0 = time.perf_counter()
    retrieved = retriever.retrieve(question, k=k)
    retrieval_ms = (time.perf_counter() - t0) * 1000

    chunks = [c for c in retrieved if c.score >= threshold]
    messages = build_messages(question, chunks)
    return PipelineResult(question, chunks, messages, generate(messages, models), retrieval_ms)
