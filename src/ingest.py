"""Build the retrieval index from the lease corpus.

Usage:
    uv run python -m src.ingest                  # baseline index
    uv run python -m src.ingest --prefix         # with contextual chunk prefixes
"""

import argparse
import pickle

from src.config import INDEX_DIR
from src.corpus import load_corpus
from src.retrievers.tfidf import TfidfRetriever
from src.schema import Clause


def index_text(clause: Clause, contextual_prefix: bool) -> str:
    """Text that gets indexed. The prefix names the tenant and unit so similar clauses stay apart."""
    if not contextual_prefix:
        return f"{clause.clause_title}\n{clause.text}"
    d = clause.doc
    return (
        f"{d.tenant}, {d.property} {d.unit}, {d.title}, "
        f"Clause {clause.clause_id} {clause.clause_title}:\n{clause.text}"
    )


def build(contextual_prefix: bool = False) -> TfidfRetriever:
    clauses = load_corpus()
    texts = [index_text(c, contextual_prefix) for c in clauses]
    return TfidfRetriever.fit(clauses, texts, contextual_prefix=contextual_prefix)


def index_path(contextual_prefix: bool):
    return INDEX_DIR / ("tfidf_prefix.pkl" if contextual_prefix else "tfidf.pkl")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", action="store_true", help="add contextual chunk prefixes")
    args = parser.parse_args()

    retriever = build(args.prefix)
    INDEX_DIR.mkdir(exist_ok=True)
    path = index_path(args.prefix)
    with open(path, "wb") as f:
        pickle.dump(retriever, f)
    print(f"Indexed {len(retriever.clauses)} clauses -> {path.relative_to(INDEX_DIR.parent)}")


if __name__ == "__main__":
    main()
