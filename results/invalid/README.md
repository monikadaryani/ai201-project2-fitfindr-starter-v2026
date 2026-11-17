# Invalid run — 2026-11-16 16:47

`capstone_before_2026-11-16_1647.*` and `runs_2026-11-16_1647_wrong_python.jsonl` are from a "before" run that ran under the wrong Python (Miniconda's, not the project's `.venv`). That Python has no `mcp` package, so every one of the 72 searches failed with `No module named 'mcp'` before it ran. Nothing about semantic search was tested.

Kept rather than deleted, because it exposed a bug in the trial runner. The agent turns a failed search into a clean "stopped" with a message, and the runner counted any stop as a pass. So criteria 2 and 5 reported **MET** on a run where no search happened. Fixed in `capstone_eval.py` before the real run:

- `search_failed()` — a search that failed is never a pass. Criterion 2 needs "search returned an empty list", and a crashed search returned nothing.
- `preflight()` — the runner refuses to start if it can't import `mcp`.

Rescored with the fixed runner, this run is MISSED on all five criteria, which is correct for a run where nothing worked.

The smoke-test records from before the trials (8 lines, `source` cli/http) are at the top of the jsonl file.
