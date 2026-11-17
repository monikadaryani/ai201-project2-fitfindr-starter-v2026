"""
Structured run log for FitFindr. ← CAPSTONE

Every agent run writes one JSON line to logs/runs.jsonl, including runs that
stopped early, crashed, or were rejected before the agent started. A failure
that only shows up as a missing line is one you never find, so the record is
written in a `finally`.

    logged_run(query, wardrobe, source="cli")   → session dict (or raises)
    log_rejected(query, reason, source="http")  → for input refused up front

Read it back with:

    python runlog.py            last 10 records, one line each
    python runlog.py 25         last 25

Fields (one record per run):

    ts               UTC timestamp, ISO 8601
    run_id           short random id
    source           "cli", "http" or "eval"
    outcome          "fit_card"  — all three tools ran
                     "stopped"   — the agent ended early with session["error"]
                     "crashed"   — an exception escaped run_agent
                     "rejected"  — input refused before the agent started
    query            what came in
    strategy         "keyword" or "semantic"
    parsed           description / size / max_price the agent pulled out
    n_results        how many listings search returned
    selected_id      the listing chosen (None if none)
    selected_title
    selected_price
    error            session["error"], or the exception text
    fit_card         what came out
    duration_ms      the whole run, end to end
    search_ms        the MCP search_listings call alone, incl. the query embedding
    model_calls      text-model calls this run (suggest_outfit + create_fit_card)
    prompt_tokens    text-model tokens, as reported by the service
    output_tokens
    cache_hits       text-model answers served from the local cache (cost nothing)
    embed_calls      embedding calls made by the search (inside the MCP server)
    embed_tokens     tokens in the text sent to the embedding model
    cache_enabled    whether the response cache was on for this run
"""

import json
import sys
import time
import uuid
from datetime import datetime, timezone

import config
import generate

LOG_DIR = config.ROOT / "logs"
LOG_FILE = LOG_DIR / "runs.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _write(record: dict) -> None:
    # Logging must never break a run that already produced an answer.
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"  [runlog] couldn't write the log: {exc}", file=sys.stderr)


def logged_run(query: str, wardrobe: dict, source: str = "cli", strategy: str | None = None) -> dict:
    """Run the agent once and append one record to the log, whatever happens."""
    from agent import run_agent

    strategy = strategy or config.SEARCH_STRATEGY
    calls_before = generate.call_count()
    tokens_before = generate.token_counts()
    hits_before = generate.cache_hits()

    session = None
    crash = None
    start = time.perf_counter()
    try:
        session = run_agent(query, wardrobe, strategy=strategy)
        return session
    except Exception as exc:  # noqa: BLE001 — recorded, then re-raised
        crash = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        duration_ms = round((time.perf_counter() - start) * 1000)
        tokens_after = generate.token_counts()
        s = session or {}
        item = s.get("selected_item") or {}
        usage = s.get("search_usage") or {}

        if crash:
            outcome = "crashed"
        elif s.get("fit_card") and not s.get("error"):
            outcome = "fit_card"
        else:
            outcome = "stopped"

        _write({
            "ts": _now(),
            "run_id": uuid.uuid4().hex[:8],
            "source": source,
            "outcome": outcome,
            "query": query,
            "strategy": strategy,
            "parsed": s.get("parsed") or {},
            "n_results": len(s.get("search_results") or []),
            "selected_id": item.get("id"),
            "selected_title": item.get("title"),
            "selected_price": item.get("price"),
            "error": crash or s.get("error"),
            "fit_card": s.get("fit_card"),
            "duration_ms": duration_ms,
            "search_ms": (s.get("timings") or {}).get("search_ms"),
            "model_calls": generate.call_count() - calls_before,
            "prompt_tokens": tokens_after["prompt"] - tokens_before["prompt"],
            "output_tokens": tokens_after["output"] - tokens_before["output"],
            "cache_hits": generate.cache_hits() - hits_before,
            "embed_calls": usage.get("embed_calls", 0),
            "embed_tokens": usage.get("embed_tokens", 0),
            "cache_enabled": config.CACHE_ENABLED,
        })


def log_rejected(query: str, reason: str, source: str = "http", strategy: str | None = None) -> None:
    """Record input that was refused before the agent ran."""
    _write({
        "ts": _now(),
        "run_id": uuid.uuid4().hex[:8],
        "source": source,
        "outcome": "rejected",
        "query": query,
        "strategy": strategy or config.SEARCH_STRATEGY,
        "error": reason,
        "duration_ms": 0,
    })


def read(n: int = 10) -> list[dict]:
    try:
        lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [json.loads(line) for line in lines[-n:] if line.strip()]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for r in read(n):
        print(
            f"{r['ts'][:19]}  {r['outcome']:8}  {r.get('strategy', ''):8}  "
            f"{str(r.get('duration_ms')):>6}ms  search={r.get('search_ms')}ms  "
            f"{r.get('selected_id') or '-':8}  {r['query']!r}"
            + (f"  error={r['error'][:60]!r}" if r.get("error") else "")
        )
