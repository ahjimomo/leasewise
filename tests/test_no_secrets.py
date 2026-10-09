"""Fail if any tracked file contains something that looks like a real credential."""

import re
import subprocess

from src.config import ROOT

SECRET_PATTERNS = [
    re.compile(r"sk-or-[A-Za-z0-9-]{20,}"),  # OpenRouter
    re.compile(r"sk-[A-Za-z0-9]{32,}"),  # OpenAI-style
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),  # GitHub token
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def test_no_secrets_in_tracked_files():
    files = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split()
    hits = []
    for name in files:
        path = ROOT / name
        if path.suffix in {".lock"} or not path.is_file():
            continue
        text = path.read_text(errors="ignore")
        hits += [f"{name}: {p.pattern}" for p in SECRET_PATTERNS if p.search(text)]
    assert not hits, f"Possible secrets committed: {hits}"


def test_env_file_is_ignored():
    result = subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=ROOT)
    assert result.returncode == 0, ".env must be listed in .gitignore"
