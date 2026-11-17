# Capstone run log — before

Run 2026-11-16_2142. 3 trials per criterion. Response cache off. Listing embeddings were already cached. SEMANTIC_MIN_SCORE = 0.62.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Semantic search finds paraphrased items | ≥4 of 5 each run; 3-run total beats keyword | 5/5 (kw 2/5) | 5/5 (kw 2/5) | 5/5 (kw 2/5) | MET (15/15 vs kw 6/15) |
| 2. Impossible queries stop before suggest_outfit | ≥4 of 5 each run | 5/5 | 5/5 | 5/5 | MET |
| 3. Queries that already worked still work | 2 of 2 each run (6 of 6) | 2/2 | 0/2 | 2/2 | MISSED |
| 4. Semantic adds 1 API call, query embedding ≤20 tokens | 1 of 1 each run (3 of 3) | 1/1 (+1 call, 4 tok) | 0/1 (+0 call, 4 tok) | 1/1 (+1 call, 4 tok) | MISSED |
| 5. Never selects an item over the user's price | 5 of 5 each run | 2/5 | 2/5 | 2/5 | MISSED |

## 1. Paraphrases — selected id (semantic / keyword)

| Query | Intended | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|---|
| leather motorcycle coat | lst_022 | lst_022 / lst_014 | lst_022 / lst_014 | lst_022 / lst_014 |
| flowery summer frock | lst_013 | lst_013 / lst_023 | lst_013 / lst_023 | lst_013 / lst_023 |
| ankle booties | lst_028 | lst_028 / None | lst_028 / None | lst_028 / None |
| chunky wool sweater | lst_008 | lst_008 / lst_008 | lst_008 / lst_008 | lst_008 / lst_008 |
| gym shorts | lst_026 | lst_026 / lst_026 | lst_026 / lst_026 | lst_026 / lst_026 |

## 2. Impossible queries — leaks (selected id when it didn't stop)

- Trial 1: 5/5 stopped
- Trial 2: 5/5 stopped
- Trial 3: 5/5 stopped

## 3. Old queries — (outcome, id, price); keyword shown for reference only

| Trial | Query | Semantic | Keyword | Met |
|---|---|---|---|---|
| 1 | vintage graphic tee under $30 | ('fit_card', 'lst_033', 19.0) | ('fit_card', 'lst_002', 18.0) | MET |
| 1 | denim jacket under $50 | ('fit_card', 'lst_007', 42.0) | ('fit_card', 'lst_007', 42.0) | MET |
| 2 | vintage graphic tee under $30 | ('stopped', 'lst_033', 19.0) | ('fit_card', 'lst_002', 18.0) | MISSED |
| 2 | denim jacket under $50 | ('stopped', 'lst_007', 42.0) | ('fit_card', 'lst_007', 42.0) | MISSED |
| 3 | vintage graphic tee under $30 | ('fit_card', 'lst_033', 19.0) | ('fit_card', 'lst_002', 18.0) | MET |
| 3 | denim jacket under $50 | ('fit_card', 'lst_007', 42.0) | ('fit_card', 'lst_007', 42.0) | MET |

## 4. Extra cost of semantic on 'vintage graphic tee under $30'

| Trial | Extra API calls | Extra input tokens | Embed tokens | Same item both ways | Met |
|---|---|---|---|---|---|
| 1 | 1 | -20 | 4 | False | MET |
| 2 | 0 | -592 | 4 | False | MISSED |
| 3 | 1 | 62 | 4 | False | MET |

The limit applies to embed tokens (the query embedding alone). Extra input tokens, which include the text-model prompts, are shown for reference only.

## 5. Price ceiling — (selected id, price, parsed max_price)

| Query | Ceiling | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|---|
| leather jacket under $40 | $40 | None / None / 40.0 | None / None / 40.0 | None / None / 40.0 |
| platform shoes below $40 | $40 | None / None / 40.0 | None / None / 40.0 | None / None / 40.0 |
| leather jacket less than $40 | $40 | lst_022 / 75.0 / None | lst_022 / 75.0 / None | lst_022 / 75.0 / None |
| velvet blazer max $40 | $40 | lst_036 / 52.0 / None | lst_036 / 52.0 / None | lst_036 / 52.0 / None |
| platform shoes $40 or less | $40 | lst_019 / 48.0 / None | lst_019 / 48.0 / None | lst_019 / 48.0 / None |

A parsed max_price of None means the query parser didn't recognise the price, so no price filter was applied.
