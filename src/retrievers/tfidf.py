"""MVP 1 baseline: TF-IDF over clause chunks with cosine similarity."""

from dataclasses import dataclass

import numpy as np
from scipy.sparse import spmatrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from src.retrievers.base import RetrievedChunk
from src.schema import Clause


@dataclass
class TfidfRetriever:
    clauses: list[Clause]
    vectorizer: TfidfVectorizer
    matrix: spmatrix
    contextual_prefix: bool = False
    name: str = "tfidf"

    @classmethod
    def fit(cls, clauses: list[Clause], texts: list[str], contextual_prefix: bool = False):
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2), sublinear_tf=True, stop_words="english", min_df=1
        )
        matrix = vectorizer.fit_transform(texts)
        return cls(clauses, vectorizer, matrix, contextual_prefix)

    def retrieve(self, query: str, k: int, filters: dict | None = None) -> list[RetrievedChunk]:
        # Vectors are L2-normalised, so the dot product is cosine similarity.
        scores = linear_kernel(self.vectorizer.transform([query]), self.matrix).ravel()
        if filters:
            mask = np.array([_matches(c, filters) for c in self.clauses])
            scores = np.where(mask, scores, -1.0)

        top = np.argsort(-scores, kind="stable")[:k]
        return [
            RetrievedChunk(clause=self.clauses[i], score=float(scores[i]), rank=r + 1)
            for r, i in enumerate(top)
            if scores[i] >= 0
        ]


def _matches(clause: Clause, filters: dict) -> bool:
    """Filter on clause fields first, then document fields, e.g. {"tenant_id": "T07"}."""
    for key, want in filters.items():
        value = getattr(clause, key, None) if hasattr(clause, key) else getattr(clause.doc, key)
        allowed = want if isinstance(want, (list, set, tuple)) else [want]
        if value not in allowed:
            return False
    return True
