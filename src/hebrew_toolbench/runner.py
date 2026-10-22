"""Query an OpenAI-compatible chat endpoint and cache raw tool calls per model.

Raw outputs are stored before scoring, so the scorer can change without
re-spending free-tier quota. A rerun skips item ids already in the cache.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"
ENV_URL, ENV_KEY = "TAINTWALL_BASE_URL", "TAINTWALL_API_KEY"
MAX_RETRIES = 6


class ApiError(RuntimeError):
    pass


def load_env_file(path: Path) -> None:
    """Read KEY=VALUE lines into os.environ without echoing anything."""
    for line in path.read_text().splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and not key.startswith("#"):
            os.environ.setdefault(key.removeprefix("export ").strip(), value.strip().strip("'\""))


def model_slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9.-]+", "_", model.removeprefix("models/")).strip("_")


def raw_path(model: str) -> Path:
    return RESULTS_DIR / "raw" / f"{model_slug(model)}.jsonl"


def _strip_private_keys(schema: Any) -> Any:
    """Drop scorer-only `x-*` keys; providers reject unknown schema keywords."""
    if isinstance(schema, dict):
        return {k: _strip_private_keys(v) for k, v in schema.items() if not k.startswith("x-")}
    if isinstance(schema, list):
        return [_strip_private_keys(v) for v in schema]
    return schema


def build_request(item: dict[str, Any], model: str, temperature: float | None = 0) -> dict[str, Any]:
    """Chat-completions body. `temperature=None` sends no sampling parameter (Claude 5.5 models reject it)."""
    messages = [{"role": "user", "content": item["question"]}]
    if item.get("system"):
        messages.insert(0, {"role": "system", "content": item["system"]})
    return {
        "model": model,
        "messages": messages,
        "tools": [{"type": "function", "function": _strip_private_keys(f)} for f in item["functions"]],
        "tool_choice": "auto",
        **({} if temperature is None else {"temperature": temperature}),
    }


def _post(url: str, key: str, body: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result: dict[str, Any] = json.load(resp)
                return result
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            if e.code not in (429, 500, 502, 503, 504) or attempt == MAX_RETRIES - 1:
                raise ApiError(f"HTTP {e.code}: {detail}") from e
            wait = float(e.headers.get("Retry-After") or 0) or min(90.0, 5.0 * 2**attempt)
            time.sleep(wait)
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == MAX_RETRIES - 1:
                raise ApiError(str(e)) from e
            time.sleep(5.0 * 2**attempt)
    raise AssertionError("unreachable")


def parse_response(resp: dict[str, Any]) -> dict[str, Any]:
    """Extract tool calls; `calls` is None if any arguments string is invalid JSON."""
    if not resp.get("choices"):
        raise ApiError(f"no choices in response: {str(resp)[:300]}")
    message = resp["choices"][0].get("message") or {}
    calls: list[dict[str, Any]] | None = []
    for tc in message.get("tool_calls") or []:
        fn = tc.get("function") or {}
        try:
            args = json.loads(fn.get("arguments") or "{}")
        except json.JSONDecodeError:
            calls = None
            break
        assert calls is not None
        calls.append({"name": fn.get("name", ""), "arguments": args if isinstance(args, dict) else {}})
    return {"calls": calls, "content": message.get("content") or ""}


def run(items: list[dict[str, Any]], model: str, rpm: float, temperature: float | None = 0) -> tuple[int, int]:
    """Query `model` on uncached items. Returns (new, failed)."""
    base, key = os.environ.get(ENV_URL), os.environ.get(ENV_KEY)
    if not base or not key:
        raise SystemExit(f"set {ENV_URL} and {ENV_KEY} (or pass --env-file)")
    url = base.rstrip("/") + "/chat/completions"
    path = raw_path(model)
    path.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(line)["id"] for line in path.open(encoding="utf-8")} if path.exists() else set()
    new = failed = 0
    for item in items:
        if item["id"] in done:
            continue
        started = time.monotonic()
        try:
            response = _post(url, key, build_request(item, model, temperature))
            record = {"id": item["id"], "model": model, **parse_response(response)}
        except ApiError as e:
            failed += 1
            print(f"  {item['id']}: {e}")
            if failed >= 5 and new == 0:
                raise SystemExit("5 failures before any success; stopping (quota or bad model id?)") from e
        else:
            record["latency_s"] = round(time.monotonic() - started, 2)
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            new += 1
        time.sleep(max(0.0, 60.0 / rpm - (time.monotonic() - started)))
    return new, failed
