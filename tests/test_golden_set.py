"""The golden set must stay consistent with the corpus: every cited clause has to exist."""

import json

from src.config import EVAL_DIR
from src.corpus import load_corpus

QUESTION_TYPES = {"Q1", "Q2", "Q3", "Q4", "Q5", "Q6"}


def _load():
    with open(EVAL_DIR / "golden_set.jsonl") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_golden_set_shape():
    items = _load()
    assert len(items) >= 40
    assert len({i["id"] for i in items}) == len(items)
    assert {i["question_type"] for i in items} == QUESTION_TYPES
    for i in items:
        assert i["question"] and i["expected_answer"]
        assert i["answerable"] == bool(i["source_clause_ids"]), i["id"]


def test_not_covered_share():
    items = _load()
    share = sum(not i["answerable"] for i in items) / len(items)
    assert 0.10 <= share <= 0.25


def test_source_clauses_exist():
    chunk_ids = {c.chunk_id for c in load_corpus()}
    for i in _load():
        for cid in i["source_clause_ids"]:
            assert cid in chunk_ids, f"{i['id']} cites missing clause {cid}"
