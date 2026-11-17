# Capstone run log — before

Run 2026-11-16_1647. 3 trials per criterion. Response cache off. Listing embeddings were already cached. SEMANTIC_MIN_SCORE = 0.62.

| # | Criterion | Target | Result | Verdict |
|---|---|---|---|---|
| 1 | paraphrases found | ≥4/5 each trial, and total > keyword total | T1: 0/5, T2: 0/5, T3: 0/5; total 0/15 vs keyword 0/15 | MISSED |
| 2 | impossible queries stop | ≥4/5 each trial | T1: 5/5, T2: 5/5, T3: 5/5 | MET |
| 3 | old queries: acceptable item, in budget, fit card | 6/6 | 0/6 | MISSED |
| 4 | +1 call, query embedding ≤20 tokens | 3/3 | 0/3 | MISSED |
| 5 | no over-budget pick | 5/5 each trial | T1: 5/5, T2: 5/5, T3: 5/5 | MET |

## 1. Paraphrases — selected id (semantic / keyword)

| Query | Intended | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|---|
| leather motorcycle coat | lst_022 | None / None | None / None | None / None |
| flowery summer frock | lst_013 | None / None | None / None | None / None |
| ankle booties | lst_028 | None / None | None / None | None / None |
| chunky wool sweater | lst_008 | None / None | None / None | None / None |
| gym shorts | lst_026 | None / None | None / None | None / None |

## 2. Impossible queries — leaks (selected id when it didn't stop)

- Trial 1: 5/5 stopped
- Trial 2: 5/5 stopped
- Trial 3: 5/5 stopped

## 3. Old queries — (outcome, id, price); keyword shown for reference only

| Trial | Query | Semantic | Keyword | Met |
|---|---|---|---|---|
| 1 | vintage graphic tee under $30 | ('stopped', None, None) | ('stopped', None, None) | MISSED |
| 1 | denim jacket under $50 | ('stopped', None, None) | ('stopped', None, None) | MISSED |
| 2 | vintage graphic tee under $30 | ('stopped', None, None) | ('stopped', None, None) | MISSED |
| 2 | denim jacket under $50 | ('stopped', None, None) | ('stopped', None, None) | MISSED |
| 3 | vintage graphic tee under $30 | ('stopped', None, None) | ('stopped', None, None) | MISSED |
| 3 | denim jacket under $50 | ('stopped', None, None) | ('stopped', None, None) | MISSED |

## 4. Extra cost of semantic on 'vintage graphic tee under $30'

| Trial | Extra API calls | Extra input tokens | Embed tokens | Same item both ways | Met |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | True | MISSED |
| 2 | 0 | 0 | 0 | True | MISSED |
| 3 | 0 | 0 | 0 | True | MISSED |

The limit applies to embed tokens (the query embedding alone). Extra input tokens, which include the text-model prompts, are shown for reference only.

## 5. Price ceiling — (selected id, price, parsed max_price)

| Query | Ceiling | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|---|
| leather jacket under $40 | $40 | None / None / 40.0 | None / None / 40.0 | None / None / 40.0 |
| platform shoes below $40 | $40 | None / None / 40.0 | None / None / 40.0 | None / None / 40.0 |
| leather jacket less than $40 | $40 | None / None / None | None / None / None | None / None / None |
| velvet blazer max $40 | $40 | None / None / None | None / None / None | None / None / None |
| platform shoes $40 or less | $40 | None / None / None | None / None / None | None / None / None |

A parsed max_price of None means the query parser didn't recognise the price, so no price filter was applied.
