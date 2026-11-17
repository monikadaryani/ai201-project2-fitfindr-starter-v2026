# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

If some keywords are missed because we are using regex, we can expect the tool to miss occasionally.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Updated criterion**
Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 4 of 5 tries.

**Why updated**
A stronger challenge is that stopping early is only half the requirement. The system must also identify why the request is impossible and explain it correctly. If the diagnosis is vague or cannot reliably separate description, size, or price issues, then the system is not fully meeting the criterion even if it does stop before suggesting an outfit. On that interpretation, the stop condition is present, but the explanation logic is not consistently strong enough to earn a full pass on all 5. 

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
We have explicitly said that if no listing is received, it should stop before `suggest_outfit`, so this path should follow that rule.

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

For 5 of 5 tries, the listing chosen by the search is the same item stored in `session["selected_item"]`, the same item passed into `suggest_outfit`, and the same item referenced in the fit card.

**Why this target:**
This is a direct state-check, not a vague quality judgment. If the agent changes items between tools, the system can still produce a polished response while recommending the wrong product. The test is observable and countable: the same listing identifier or title must flow through each step.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

For at least 4 of 5 tries, the fit card includes the item’s title or a unique listing name and the sale price, and the card remains 2–4 sentences long.

**Why this target:**
The model is allowed to vary its wording, so the criterion should not require identical phrasing. What matters is that the final card still contains the item identity and the numeric price, because those are the parts users need to decide whether the recommendation is worth it. If the model or the listing drops the item name or price, the card may still fail the criterion in a real scenario.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

When the user provides a size or a maximum price, the selected listing must match that size and cost no more than the stated limit in 5 of 5 tries. If only one constraint is provided, only that one is checked.

**Why this target:**
This is a core user-value check. The tool is not useful if it writes a stylish caption for an item that ignores the user’s budget or size, even when the rest of the workflow appears successful. The rule is simple, measurable, and easy to grade without subjective interpretation.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria — semantic search

Written 2026-11-16, after building semantic search and before running any trials. The five criteria above are from units 3 and 4 and are left as they were.

The queries below are new. None of them were used in the smoke test or to pick `SEMANTIC_MIN_SCORE` (0.62). Those queries were "band shirt", "jean jacket", "something cozy for winter", "wedding dress", "laptop charger" and "car tires". Testing on them would only show that the cutoff fits the queries it was picked from.

Every criterion is run **3 trials**. Criteria 1–3 and 5 are about how semantic search behaves; 4 is about what it costs to run.

---

## 1. Semantic search finds paraphrased items

Five queries, each worded differently from the one listing it should find:

| Query | Intended listing |
|---|---|
| leather motorcycle coat | lst_022 — 90s Leather Bomber |
| flowery summer frock | lst_013 — 90s Silk Slip Dress |
| ankle booties | lst_028 — Suede Chelsea Boots |
| chunky wool sweater | lst_008 — Knit Cardigan |
| gym shorts | lst_026 — Biker Shorts |

With `AI201_SEARCH=semantic`, the selected item is the intended listing for **at least 4 of 5 queries, in each of 3 trials**. Across all 3 trials combined (out of 15), semantic search must also get **more** intended listings than keyword search does on the same queries.

**Why this target:**
No search can be perfect, so I don't expect semantic search to find the intended listing every time. That's why it's 4 of 5 per trial, not 5 of 5. What I do expect is that semantic search does better than keyword search, so I compare the totals across all 3 trials.

---

## 2. Impossible queries still stop before `suggest_outfit`

Five queries for things the catalog doesn't carry: **bikini swimsuit, black tuxedo, stiletto heels, winter gloves, pearl necklace**.

With `AI201_SEARCH=semantic`, the search returns an empty list and the agent stops before calling `suggest_outfit` (`outfit_suggestion` and `fit_card` stay `None`, `error` is set). That must happen for **at least 4 of 5 queries, in each of 3 trials**.

**Why this target:**
A leaked item, where the agent styles an outfit for something the user didn't ask for, is bad, but it isn't the worst failure. So 4 of 5 per trial is an acceptable target.

---

## 3. Queries that already worked still work

The two matching queries from unit 4's scenarios: **"vintage graphic tee under $30"** and **"denim jacket under $50"**.

Acceptable listings, decided from the data before any trial:

| Query | Ceiling | Acceptable listing ids |
|---|---|---|
| vintage graphic tee under $30 | $30 | lst_002 (Y2K Baby Tee, butterfly graphic), lst_006 (Graphic Tee, 2003 Tour), lst_033 (Vintage Band Tee) |
| denim jacket under $50 | $50 | lst_007 (Denim Jacket, Light Wash) |

Left out on purpose: lst_015 (Graphic Hoodie, a hoodie, not a tee) and lst_038 (Denim Vest, a vest, not a jacket).

With `AI201_SEARCH=semantic`, a run passes when all three hold: the selected item is one of the acceptable listings for that query; its price is at most the ceiling; and the run returns a non-empty fit card with no `error`. That must happen for **both queries, in each of 3 trials (6 of 6)**.

**Why this target:**
These two queries passed under keyword search in unit 4, so if they fail now, the change caused it. I check against a list of acceptable listings that I picked from the data before testing, not against keyword's pick. A category match would pass a cardigan for "vintage graphic tee", and keyword's pick isn't proof of a correct answer either. More than one graphic tee is acceptable, because semantic search may reasonably prefer a different one. The target is 6 of 6 because these are the easy cases: the words in the query appear in the listings, and each query has an acceptable item under its price. The one way they should fail is the 0.62 cutoff dropping a correct match, or semantic ranking a near-miss (the Graphic Hoodie, the Denim Vest) first. Either would mean semantic search broke something that already worked.

---

## 4. Semantic search adds one API call and almost no tokens

With the response cache off and the listing embeddings already cached, a semantic run makes **exactly 1 more API call** than a keyword run of the same query: the query embedding. (The token-counting call that exists only to measure cost is not counted as an API call.) The query embedding sends **no more than 20 tokens** to the embedding model; text-model prompt tokens are not part of this limit. This must hold in **3 of 3 trials** on "vintage graphic tee under $30". I'll also report the cost of one run of each strategy in dollars, from the measured tokens.

**Why this target:**
The listing vectors are supposed to be embedded once and reused. If a run makes more than one extra call, the listing cache isn't working, and every request is quietly paying to re-embed the 40 listings. That's the failure this criterion is for. 20 tokens is generous for a short shopping query, so missing it means something other than the query is being embedded.

---

## 5. Semantic search never selects an item over the user's price

Five queries with a price ceiling, each with an over-budget listing that semantic search would likely rank first if the price were ignored. Two use phrasings the query parser recognises ("under", "below"); three use natural phrasings it doesn't:

| Query | Ceiling | Over-budget listing it could pick |
|---|---|---|
| leather jacket under $40 | $40 | lst_022 — 90s Leather Bomber, $75 |
| platform shoes below $40 | $40 | lst_009 — Platform Mary Janes, $55 |
| leather jacket less than $40 | $40 | lst_022 — 90s Leather Bomber, $75 |
| velvet blazer max $40 | $40 | lst_036 — Velvet Blazer, $52 |
| platform shoes $40 or less | $40 | lst_009 — Platform Mary Janes, $55 |

With `AI201_SEARCH=semantic`, no over-budget item is selected: either the selected item costs at most the ceiling, or the agent stops without selecting anything. That must hold for **5 of 5 queries, in each of 3 trials**.

**Why this target:**
Going over budget is a different kind of mistake from picking a near-miss item. A near-miss is still something the user might want. An over-budget item ignores a limit the user stated outright, and they can't buy it. That's why this is 5 of 5 when criteria 1 and 2 allow one miss. Search applies the price filter before ranking, so whenever the price is parsed, an over-budget item can't be selected. The real risk is wording. Semantic search invites natural queries, and the query parser only recognises "under", "below", "at most" and "up to". "Less than $40", "max $40" or "$40 or less" get no price filter at all, and semantic search will happily rank the $75 Leather Bomber first. So this criterion tests whether the extension is safe with the phrasing it encourages.

> **Revised before any trials (2026-11-16):** criterion 5 was originally "the warm search step finishes in under 2.0 seconds". I replaced it before running anything, because measuring only warm searches felt like excluding the slow case. Duration is still logged for every run; it just isn't a criterion.
