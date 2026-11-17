#!/usr/bin/env python3
"""
Capstone trial runner — runs every criterion in criteria.md, 3 trials each.

    python capstone_eval.py --label before      the full trial run
    python capstone_eval.py --label after       after the improvement
    python capstone_eval.py --cost              the 10-run cost measurement

Every run goes through runlog.logged_run, so each one is also a record in
logs/runs.jsonl (source "eval"). The response cache is forced off: five
cached answers are one answer, and cached runs cost nothing.

Writes:
    results/capstone_<label>_<timestamp>.md     tables + verdicts
    results/capstone_<label>_<timestamp>.json   every run's raw record

The queries and targets live in the block below. They mirror criteria.md —
if a criterion changes there, change it here too, before running anything.
"""

import os

# Before config is imported anywhere: config reads this once, at import.
os.environ["AI201_CACHE"] = "0"

import argparse
import json
from datetime import datetime

import config
import runlog
import semantic
from utils.data_loader import get_example_wardrobe, load_listings

# ── The criteria, as data ─────────────────────────────────────────────────────

TRIALS = 3

# Criterion 1 — paraphrased queries and the one listing each should find.
PARAPHRASES = [
    ("leather motorcycle coat", "lst_022"),
    ("flowery summer frock", "lst_013"),
    ("ankle booties", "lst_028"),
    ("chunky wool sweater", "lst_008"),
    ("gym shorts", "lst_026"),
]
C1_TARGET_PER_TRIAL = 4          # semantic hits out of 5, in every trial
                                 # ...and semantic hits > keyword hits, summed over all trials

# Criterion 2 — things the catalog doesn't carry.
IMPOSSIBLE = [
    "bikini swimsuit",
    "black tuxedo",
    "stiletto heels",
    "winter gloves",
    "pearl necklace",
]
C2_TARGET_PER_TRIAL = 4          # stops early, out of 5, in every trial

# Criterion 3 — unit 4 queries that worked under keyword search.
# Keyword's pick is taken from the SAME trial.
REGRESSION = [
    "vintage graphic tee under $30",
    "denim jacket under $50",
]
C3_TARGET = 6                    # out of 2 queries x 3 trials

# Criterion 4 — extra cost of semantic over keyword, same query, same trial.
# Reuses criterion 3's runs of this query (same conditions: cache off, warm).
COST_QUERY = "vintage graphic tee under $30"
C4_EXTRA_CALLS = 1               # exactly
C4_MAX_EMBED_TOKENS = 20         # tokens sent to the embedding model (query only)
C4_TARGET = 3                    # out of 3 trials

# Criterion 5 — price ceiling under semantic search. (query, ceiling)
# Pass = no over-budget item selected: the pick costs <= ceiling, or it stopped.
PRICE_QUERIES = [
    ("leather jacket under $40", 40.0),
    ("platform shoes below $40", 40.0),
    ("leather jacket less than $40", 40.0),
    ("velvet blazer max $40", 40.0),
    ("platform shoes $40 or less", 40.0),
]
C5_TARGET_PER_TRIAL = 5          # out of 5, in every trial

# The 10-run cost measurement (--cost).
COST_RUNS = 10


# ── Running ───────────────────────────────────────────────────────────────────

WARDROBE = get_example_wardrobe()


def run(query: str, strategy: str) -> dict:
    """One logged agent run. Returns its log record plus the selected category."""
    session = {}
    try:
        session = runlog.logged_run(query, WARDROBE, source="eval", strategy=strategy)
    except Exception:  # noqa: BLE001 — the crash is already in the log record
        pass
    record = runlog.read(1)[0]
    item = session.get("selected_item") or {}
    record["selected_category"] = item.get("category")
    record["outfit_called"] = session.get("outfit_suggestion") is not None
    tag = record["selected_id"] or record["outcome"]
    print(f"    {strategy:8} {query!r:34} → {tag:10} search={record.get('search_ms')}ms")
    return record


def warm_up() -> bool:
    """Make sure the listing embeddings are cached. Returns True if it was cold."""
    cold = not (config.CACHE_DIR / "listing_embeddings.json").exists()
    semantic.listing_vectors(load_listings())
    return cold


def api_calls(r: dict) -> int:
    return (r.get("model_calls") or 0) + (r.get("embed_calls") or 0)


def input_tokens(r: dict) -> int:
    return (r.get("prompt_tokens") or 0) + (r.get("embed_tokens") or 0)


def stopped_early(r: dict) -> bool:
    return (
        r["n_results"] == 0
        and not r["outfit_called"]
        and r.get("fit_card") is None
        and bool(r.get("error"))
    )


def met(ok: bool) -> str:
    return "MET" if ok else "MISSED"


# ── Scoring (pure: takes records, returns verdicts) ───────────────────────────


def score(runs: dict) -> dict:
    """runs = {"c1": [...], "c2": [...], "c3": [...], "c5": [...]} of trial-tagged records."""
    out = {}

    # Criterion 1
    rows, per_trial_ok = [], True
    for t in range(1, TRIALS + 1):
        sem = {r["query"]: r for r in runs["c1"] if r["trial"] == t and r["strategy"] == "semantic"}
        kw = {r["query"]: r for r in runs["c1"] if r["trial"] == t and r["strategy"] == "keyword"}
        sem_hits = sum(sem[q]["selected_id"] == want for q, want in PARAPHRASES)
        kw_hits = sum(kw[q]["selected_id"] == want for q, want in PARAPHRASES)
        ok = sem_hits >= C1_TARGET_PER_TRIAL
        per_trial_ok &= ok
        rows.append({
            "trial": t, "semantic_hits": sem_hits, "keyword_hits": kw_hits, "met": ok,
            "picks": {q: (sem[q]["selected_id"], kw[q]["selected_id"]) for q, _ in PARAPHRASES},
        })
    sem_total = sum(r["semantic_hits"] for r in rows)
    kw_total = sum(r["keyword_hits"] for r in rows)
    out["c1"] = {"rows": rows, "semantic_total": sem_total, "keyword_total": kw_total,
                 "met": per_trial_ok and sem_total > kw_total}

    # Criterion 2
    rows, all_ok = [], True
    for t in range(1, TRIALS + 1):
        trial = {r["query"]: r for r in runs["c2"] if r["trial"] == t}
        stops = sum(stopped_early(trial[q]) for q in IMPOSSIBLE)
        ok = stops >= C2_TARGET_PER_TRIAL
        all_ok &= ok
        rows.append({
            "trial": t, "stopped": stops, "met": ok,
            "leaks": {q: trial[q]["selected_id"] for q in IMPOSSIBLE if not stopped_early(trial[q])},
        })
    out["c2"] = {"rows": rows, "met": all_ok}

    # Criterion 3
    rows, passes = [], 0
    for t in range(1, TRIALS + 1):
        for q in REGRESSION:
            sem = next(r for r in runs["c3"] if r["trial"] == t and r["query"] == q and r["strategy"] == "semantic")
            kw = next(r for r in runs["c3"] if r["trial"] == t and r["query"] == q and r["strategy"] == "keyword")
            ok = sem["outcome"] == "fit_card" and sem["selected_category"] == kw["selected_category"]
            passes += ok
            rows.append({
                "trial": t, "query": q, "semantic": (sem["outcome"], sem["selected_id"], sem["selected_category"]),
                "keyword": (kw["outcome"], kw["selected_id"], kw["selected_category"]), "met": ok,
            })
    out["c3"] = {"rows": rows, "passes": passes, "met": passes >= C3_TARGET}

    # Criterion 4 (criterion 3's runs of COST_QUERY)
    rows, passes = [], 0
    for t in range(1, TRIALS + 1):
        sem = next(r for r in runs["c3"] if r["trial"] == t and r["query"] == COST_QUERY and r["strategy"] == "semantic")
        kw = next(r for r in runs["c3"] if r["trial"] == t and r["query"] == COST_QUERY and r["strategy"] == "keyword")
        extra_calls = api_calls(sem) - api_calls(kw)
        extra_tokens = input_tokens(sem) - input_tokens(kw)
        ok = extra_calls == C4_EXTRA_CALLS and (sem.get("embed_tokens") or 0) <= C4_MAX_EMBED_TOKENS
        passes += ok
        rows.append({
            "trial": t, "extra_calls": extra_calls, "extra_input_tokens": extra_tokens,
            "embed_tokens": sem.get("embed_tokens"), "same_item": sem["selected_id"] == kw["selected_id"],
            "met": ok,
        })
    out["c4"] = {"rows": rows, "passes": passes, "met": passes >= C4_TARGET}

    # Criterion 5
    rows, all_ok = [], True
    for t in range(1, TRIALS + 1):
        trial = {r["query"]: r for r in runs["c5"] if r["trial"] == t}
        over = {q: (trial[q]["selected_id"], trial[q]["selected_price"]) for q, cap in PRICE_QUERIES
                if trial[q]["selected_price"] is not None and trial[q]["selected_price"] > cap}
        held = len(PRICE_QUERIES) - len(over)
        ok = held >= C5_TARGET_PER_TRIAL
        all_ok &= ok
        rows.append({"trial": t, "held": held, "over_budget": over, "met": ok,
                     "picks": {q: (trial[q]["selected_id"], trial[q]["selected_price"],
                                   trial[q]["parsed"].get("max_price")) for q, _ in PRICE_QUERIES}})
    out["c5"] = {"rows": rows, "met": all_ok}
    return out


# ── Report ────────────────────────────────────────────────────────────────────


def report(label: str, stamp: str, cold: bool, s: dict) -> str:
    L = [f"# Capstone run log — {label}", "",
         f"Run {stamp}. {TRIALS} trials per criterion. Response cache off. "
         f"Listing embeddings were {'COLD (built at start, before any trial)' if cold else 'already cached'}. "
         f"SEMANTIC_MIN_SCORE = {config.SEMANTIC_MIN_SCORE}.", "",
         "| # | Criterion | Target | Result | Verdict |", "|---|---|---|---|---|"]
    c1 = s["c1"]["rows"]
    L.append(f"| 1 | paraphrases found | ≥{C1_TARGET_PER_TRIAL}/5 each trial, and total > keyword total | "
             + ", ".join(f"T{r['trial']}: {r['semantic_hits']}/5" for r in c1)
             + f"; total {s['c1']['semantic_total']}/15 vs keyword {s['c1']['keyword_total']}/15"
             + f" | {met(s['c1']['met'])} |")
    L.append(f"| 2 | impossible queries stop | ≥{C2_TARGET_PER_TRIAL}/5 each trial | "
             + ", ".join(f"T{r['trial']}: {r['stopped']}/5" for r in s["c2"]["rows"])
             + f" | {met(s['c2']['met'])} |")
    L.append(f"| 3 | old queries still work | {C3_TARGET}/6 | {s['c3']['passes']}/6 | {met(s['c3']['met'])} |")
    L.append(f"| 4 | +{C4_EXTRA_CALLS} call, query embedding ≤{C4_MAX_EMBED_TOKENS} tokens | {C4_TARGET}/3 | "
             f"{s['c4']['passes']}/3 | {met(s['c4']['met'])} |")
    L.append(f"| 5 | no over-budget pick | {C5_TARGET_PER_TRIAL}/5 each trial | "
             + ", ".join(f"T{r['trial']}: {r['held']}/5" for r in s["c5"]["rows"])
             + f" | {met(s['c5']['met'])} |")

    L += ["", "## 1. Paraphrases — selected id (semantic / keyword)", "",
          "| Query | Intended | " + " | ".join(f"Trial {t}" for t in range(1, TRIALS + 1)) + " |",
          "|---|---|" + "---|" * TRIALS]
    for q, want in PARAPHRASES:
        L.append(f"| {q} | {want} | " + " | ".join(
            "{} / {}".format(*r["picks"][q]) for r in c1) + " |")

    L += ["", "## 2. Impossible queries — leaks (selected id when it didn't stop)", ""]
    for r in s["c2"]["rows"]:
        L.append(f"- Trial {r['trial']}: {r['stopped']}/5 stopped" + (f"; leaked: {r['leaks']}" if r["leaks"] else ""))

    L += ["", "## 3. Old queries — (outcome, id, category)", "",
          "| Trial | Query | Semantic | Keyword | Met |", "|---|---|---|---|---|"]
    for r in s["c3"]["rows"]:
        L.append(f"| {r['trial']} | {r['query']} | {r['semantic']} | {r['keyword']} | {met(r['met'])} |")

    L += ["", f"## 4. Extra cost of semantic on {COST_QUERY!r}", "",
          "| Trial | Extra API calls | Extra input tokens | Embed tokens | Same item both ways | Met |",
          "|---|---|---|---|---|---|"]
    for r in s["c4"]["rows"]:
        L.append(f"| {r['trial']} | {r['extra_calls']} | {r['extra_input_tokens']} | {r['embed_tokens']} | "
                 f"{r['same_item']} | {met(r['met'])} |")
    L.append("")
    L.append("The limit applies to embed tokens (the query embedding alone). Extra input tokens, "
             "which include the text-model prompts, are shown for reference only.")

    L += ["", "## 5. Price ceiling — (selected id, price, parsed max_price)", "",
          "| Query | Ceiling | " + " | ".join(f"Trial {t}" for t in range(1, TRIALS + 1)) + " |",
          "|---|---|" + "---|" * TRIALS]
    for q, cap in PRICE_QUERIES:
        L.append(f"| {q} | ${cap:.0f} | " + " | ".join(
            "{} / {} / {}".format(*r["picks"][q]) for r in s["c5"]["rows"]) + " |")
    L.append("")
    L.append("A parsed max_price of None means the query parser didn't recognise the price, "
             "so no price filter was applied.")
    return "\n".join(L) + "\n"


def trials() -> dict:
    runs = {"c1": [], "c2": [], "c3": [], "c5": []}
    for t in range(1, TRIALS + 1):
        print(f"\n── Trial {t} of {TRIALS}")
        print("  Criterion 1 — paraphrases")
        for q, _ in PARAPHRASES:
            for strategy in ("semantic", "keyword"):
                runs["c1"].append({**run(q, strategy), "trial": t})
        print("  Criterion 2 — impossible queries")
        for q in IMPOSSIBLE:
            runs["c2"].append({**run(q, "semantic"), "trial": t})
        print("  Criterion 5 — price ceiling")
        for q, _ in PRICE_QUERIES:
            runs["c5"].append({**run(q, "semantic"), "trial": t})
        print("  Criterion 3 / 4 — old queries")
        for q in REGRESSION:
            for strategy in ("semantic", "keyword"):
                runs["c3"].append({**run(q, strategy), "trial": t})
    return runs


def cost_runs() -> None:
    print(f"\n── Cost: {COST_RUNS} runs of {COST_QUERY!r}, each strategy, cache off")
    for strategy in ("keyword", "semantic"):
        recs = [run(COST_QUERY, strategy) for _ in range(COST_RUNS)]
        n = len(recs)
        avg = lambda k: sum((r.get(k) or 0) for r in recs) / n  # noqa: E731
        print(f"\n  {strategy}: averages over {n} runs")
        print(f"    model calls {avg('model_calls'):.2f}, embed calls {avg('embed_calls'):.2f}")
        print(f"    prompt tokens {avg('prompt_tokens'):.1f}, output tokens {avg('output_tokens'):.1f}, "
              f"embed tokens {avg('embed_tokens'):.1f}")
        print(f"    duration {avg('duration_ms'):.0f} ms, search {avg('search_ms'):.0f} ms")
    print("\n  Every run is in logs/runs.jsonl (source \"eval\"). Multiply the average tokens by")
    print("  the per-token prices for the two models to get dollars, and write down which prices.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--label", help="before / after — names the results files")
    parser.add_argument("--cost", action="store_true", help=f"the {COST_RUNS}-run cost measurement")
    args = parser.parse_args()

    cold = warm_up()
    if cold:
        print("Listing embeddings were not cached; built them now, before any trial.")

    if args.cost:
        cost_runs()
        return
    if not args.label:
        parser.error("give --label (before / after) or --cost")

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    runs = trials()
    s = score(runs)
    config.RESULTS_DIR.mkdir(exist_ok=True)
    base = config.RESULTS_DIR / f"capstone_{args.label}_{stamp}"
    base.with_suffix(".md").write_text(report(args.label, stamp, cold, s), encoding="utf-8")
    base.with_suffix(".json").write_text(json.dumps({"runs": runs, "scores": s}, indent=1, default=str), encoding="utf-8")
    print(f"\nWrote {base.with_suffix('.md').relative_to(config.ROOT)} and .json")
    for k in ("c1", "c2", "c3", "c4", "c5"):
        print(f"  criterion {k[1]}: {met(s[k]['met'])}")


if __name__ == "__main__":
    main()
