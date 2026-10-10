"""Compare candidate free models on a few golden questions, using identical retrieved context.

Usage:
    uv run python scripts/compare_models.py MODEL [MODEL ...] [--questions q023,q031,q048]

Each model x question is one OpenRouter request (free tier: 50/day without credits).
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import EVAL_DIR  # noqa: E402
from src.ingest import build  # noqa: E402
from src.llm import LLMError, generate  # noqa: E402
from src.prompts import NOT_FOUND, build_messages  # noqa: E402

CITATION_RE = re.compile(r"\[[^\[\]]+ · [^\[\]]+ · Cl\. [\d.]+\]")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("models", nargs="+")
    parser.add_argument("--questions", default="q023,q031,q048")
    args = parser.parse_args()

    golden = {}
    with open(EVAL_DIR / "golden_set.jsonl") as f:
        for line in f:
            item = json.loads(line)
            golden[item["id"]] = item

    retriever = build(contextual_prefix=True)
    for qid in args.questions.split(","):
        item = golden[qid]
        chunks = retriever.retrieve(item["question"], k=5)
        messages = build_messages(item["question"], chunks)
        valid = {c.clause.citation for c in chunks}
        print(f"\n=== {qid} ({item['question_type']}): {item['question']}")
        print(f"Expected: {item['expected_answer']}")
        for model in args.models:
            try:
                r = generate(messages, [model])
            except LLMError as e:
                print(f"\n--- {model}: FAILED {e.attempts}")
                continue
            cites = CITATION_RE.findall(r.text)
            invalid = [c for c in cites if c not in valid]
            print(
                f"\n--- {model}  {r.latency_ms / 1000:.1f}s  "
                f"tokens {r.prompt_tokens}/{r.completion_tokens}  "
                f"citations {len(cites)} (invalid {len(invalid)})  "
                f"refused={NOT_FOUND in r.text}"
            )
            print(r.text)


if __name__ == "__main__":
    main()
