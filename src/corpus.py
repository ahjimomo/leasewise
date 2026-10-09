"""Load the markdown corpus into validated Clause objects.

Clause headings look like:  ## 7. Break Option {type=break_option}
Amendments add the clauses they change:  ## 2. Deletion of Break Option {type=break_option modifies=7}
(`modifies` takes a comma-separated list of clause ids in the amended document.)
"""

import re
from pathlib import Path

import frontmatter

from src.config import LEASES_DIR
from src.schema import Clause, ClauseType, DocumentMeta

HEADING_RE = re.compile(
    r"^##\s+(?P<id>\d+(?:\.\d+)*)\.?\s+(?P<title>.+?)\s*\{(?P<attrs>[^}]*)\}\s*$", re.MULTILINE
)
ATTR_RE = re.compile(r"(\w+)=([^\s]+)")


def parse_document(path: Path) -> list[Clause]:
    post = frontmatter.load(path)
    meta = DocumentMeta(**post.metadata)
    body = post.content
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        raise ValueError(f"{path.name}: no tagged clause headings found")

    clauses = []
    # Text above the first clause (title, parties, signing date) becomes clause "0".
    preamble = "\n".join(
        line
        for line in body[: matches[0].start()].splitlines()
        if line.strip() and not line.startswith(("# ", "*Fictional"))
    ).strip()
    if preamble:
        clauses.append(
            Clause(
                doc=meta,
                clause_id="0",
                clause_title="Preamble",
                clause_type=ClauseType.GENERAL,
                text=preamble,
            )
        )

    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        attrs = dict(ATTR_RE.findall(m.group("attrs")))
        if "type" not in attrs:
            raise ValueError(f"{path.name}: clause {m.group('id')} missing type=")
        modifies = [c for c in attrs.get("modifies", "").split(",") if c]
        clauses.append(
            Clause(
                doc=meta,
                clause_id=m.group("id"),
                clause_title=m.group("title"),
                clause_type=ClauseType(attrs["type"]),
                text=body[m.end() : end].strip(),
                modifies_clause_ids=modifies,
            )
        )
    return clauses


def load_corpus(leases_dir: Path = LEASES_DIR) -> list[Clause]:
    clauses = []
    for path in sorted(leases_dir.glob("*.md")):
        clauses.extend(parse_document(path))
    return clauses
