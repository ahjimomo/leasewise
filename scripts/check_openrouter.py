"""Check the OpenRouter key in .env and list current free models.

Usage:
    uv run python scripts/check_openrouter.py            # key status + free models
    uv run python scripts/check_openrouter.py MODEL_ID   # also send a one-line test prompt

Never prints the key itself.
"""

import json
import sys
import urllib.request
from urllib.error import HTTPError

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from src.config import OPENROUTER_BASE_URL, get_api_key  # noqa: E402


def _request(path: str, key: str | None = None, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        OPENROUTER_BASE_URL + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json"}
        | ({"Authorization": f"Bearer {key}"} if key else {}),
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main() -> None:
    key = get_api_key()
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key.")

    try:
        info = _request("/key", key)["data"]
    except HTTPError as e:
        sys.exit(f"Key check failed: HTTP {e.code}. Check the key in .env.")
    print("Key OK.")
    for field in ("label", "limit", "usage", "free_model_daily_requests"):
        if field in info:
            print(f"  {field}: {info[field]}")

    free = sorted(m["id"] for m in _request("/models")["data"] if m["id"].endswith(":free"))
    print(f"\n{len(free)} free models available:")
    for m in free:
        print(f"  {m}")

    if len(sys.argv) > 1:
        model = sys.argv[1]
        try:
            out = _request(
                "/chat/completions",
                key,
                {"model": model, "messages": [{"role": "user", "content": "Reply with: ok"}]},
            )
            print(f"\nTest call to {model}: {out['choices'][0]['message']['content']!r}")
        except HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            print(f"\nTest call to {model} failed: HTTP {e.code} {detail}")
            if e.code == 404 and "data policy" in detail:
                print("Enable free-model endpoints at https://openrouter.ai/settings/privacy")


if __name__ == "__main__":
    main()
