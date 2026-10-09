"""Run the golden set and report metrics by question type.

Usage:
    uv run python -m eval.run_eval --retrieval-only            # no LLM calls
    uv run python -m eval.run_eval --retrieval-only --prefix   # contextual prefixes on
"""

import argparse
import json
import time
from collections import defaultdict
from datetime import date

from eval.metrics import bootstrap_ci, hit_at_k, recall_at_k, reciprocal_rank, tenant_accuracy
from src.config import DEFAULT_K, EVAL_DIR, RELEVANCE_THRESHOLD
from src.ingest import build

QUESTION_TYPES = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
RETRIEVAL_METRICS = ["hit", "recall", "rr", "tenant_acc"]


def load_golden() -> list[dict]:
    with open(EVAL_DIR / "golden_set.jsonl") as f:
        return [json.loads(line) for line in f if line.strip()]


def evaluate_retrieval(retriever, items: list[dict], k: int, threshold: float) -> list[dict]:
    by_chunk = {c.chunk_id: c for c in retriever.clauses}
    rows = []
    for item in items:
        t0 = time.perf_counter()
        results = retriever.retrieve(item["question"], k=k)
        latency_ms = (time.perf_counter() - t0) * 1000

        ids = [r.clause.chunk_id for r in results]
        top_score = results[0].score if results else 0.0
        row = {
            "id": item["id"],
            "question_type": item["question_type"],
            "answerable": item["answerable"],
            "retrieved": ids,
            "top_score": round(top_score, 4),
            "abstains": top_score < threshold,  # retrieval-level "not found"
            "retrieval_ms": round(latency_ms, 2),
        }
        if item["answerable"]:
            gold = item["source_clause_ids"]
            gold_tenants = {by_chunk[g].doc.tenant_id for g in gold}
            row |= {
                "hit": hit_at_k(ids, gold),
                "recall": recall_at_k(ids, gold),
                "rr": reciprocal_rank(ids, gold),
                "tenant_acc": tenant_accuracy([r.clause.doc.tenant_id for r in results], gold_tenants),
            }
        rows.append(row)
    return rows


def summarise(rows: list[dict]) -> dict:
    groups = defaultdict(list)
    for r in rows:
        groups[r["question_type"]].append(r)
    groups["ALL"] = rows

    summary = {}
    for name, group in groups.items():
        answerable = [r for r in group if r["answerable"]]
        unanswerable = [r for r in group if not r["answerable"]]
        s = {"n": len(group)}
        for m in RETRIEVAL_METRICS:
            if answerable:
                s[m] = bootstrap_ci([r[m] for r in answerable])
        if unanswerable:
            # Correct behaviour on Q6 is to abstain.
            s["abstain_correct"] = bootstrap_ci([float(r["abstains"]) for r in unanswerable])
        if answerable:
            s["false_abstain"] = bootstrap_ci([float(r["abstains"]) for r in answerable])
        summary[name] = s
    return summary


def print_summary(summary: dict, k: int) -> None:
    cols = ["n", f"hit@{k}", f"recall@{k}", "MRR", "tenant_acc", "abstain_ok", "false_abstain"]
    keys = ["n", "hit", "recall", "rr", "tenant_acc", "abstain_correct", "false_abstain"]
    print("  ".join(f"{c:>18}" for c in ["type"] + cols))
    for name in QUESTION_TYPES + ["ALL"]:
        s = summary.get(name)
        if not s:
            continue
        cells = [f"{s['n']:>18}"]
        for key in keys[1:]:
            v = s.get(key)
            cells.append(f"{'–':>18}" if v is None else f"{v[0]:.2f} [{v[1]:.2f},{v[2]:.2f}]".rjust(18))
        print("  ".join([f"{name:>18}"] + cells))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrieval-only", action="store_true", help="skip LLM generation")
    parser.add_argument("--prefix", action="store_true", help="contextual chunk prefixes")
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--threshold", type=float, default=RELEVANCE_THRESHOLD)
    args = parser.parse_args()
    if not args.retrieval_only:
        parser.error("full LLM evaluation is not implemented yet; use --retrieval-only")

    retriever = build(contextual_prefix=args.prefix)
    method = "tfidf_prefix" if args.prefix else "tfidf"
    rows = evaluate_retrieval(retriever, load_golden(), args.k, args.threshold)
    summary = summarise(rows)

    print(f"\nMethod: {method}  k={args.k}  threshold={args.threshold}  n={len(rows)}\n")
    print_summary(summary, args.k)

    out_dir = EVAL_DIR / "results"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{date.today().isoformat()}_{method}_retrieval.json"
    config = {"method": method, "k": args.k, "threshold": args.threshold, "mode": "retrieval"}
    with open(out, "w") as f:
        json.dump({"config": config, "summary": summary, "rows": rows}, f, indent=2)
    print(f"\nWrote {out.relative_to(EVAL_DIR.parent)}")


if __name__ == "__main__":
    main()
