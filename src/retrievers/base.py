"""Common retriever interface so retrieval methods can be swapped and compared in eval."""

from dataclasses import dataclass, field
from typing import Protocol

from src.schema import Clause


@dataclass
class RetrievedChunk:
    clause: Clause
    score: float
    rank: int
    debug: dict = field(default_factory=dict)  # method-specific details for the transparency panel


class Retriever(Protocol):
    name: str

    def retrieve(self, query: str, k: int, filters: dict | None = None) -> list[RetrievedChunk]: ...
