# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

The project functions like a thrift-shopping style assistant. A user searches for an item that matches specific requirements, such as a vintage graphic tee under $30, and the app parses the request, filters the listings, and finds suitable matches. It then suggests outfit combinations based on the selected item and the user’s wardrobe, and creates a fit card summarizing the look. The app is designed to avoid unrealistic requests, such as a ballgown under $5, and instead focus on practical, wearable options.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Finds thrift listings matching a search description, then filters by size and max price and ranks the remaining items by keyword overlap.
- **Inputs:** `description` (str), `size` (str | None), `max_price` (float | None)
- **Returns:** A list of matching listing dictionaries, sorted by best keyword match first; each dict includes the listing fields from `listings.json`.
- **When it has nothing:** Returns an empty list when no listing matches the description, size, and budget constraints.

### `suggest_outfit`

- **What it does:** Takes a selected listing and the user’s wardrobe and returns a short outfit recommendation based on what the user already owns.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing 1–3 outfit suggestions.
- **When it has nothing:** If the wardrobe is empty, it returns general styling advice instead of failing or returning an empty string.

### `create_fit_card`

- **What it does:** Turns the outfit suggestion and the chosen item into a short fit-card caption for a thrift post.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A 2–4 sentence caption that mentions the item, price, and platform in a natural, social-post style.
- **When it has nothing:** If the outfit text is empty or whitespace, it returns a fallback descriptive message instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If `search_listings` returns an empty list, the agent stops and stores a helpful message in `session["error"]` explaining whether the user should broaden the description, widen the size range, or raise the price cap. Otherwise, it takes the first result and continues to `suggest_outfit()` and then `create_fit_card()`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** The query is parsed with a regex-based approach that extracts `description`, `size`, and `max_price`, with extra cleanup using string normalization and keyword stripping.

**What moves through the session:** `query` → `parsed` → `search_results` → `selected_item` → `outfit_suggestion` → `fit_card` → `error`

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```
python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Ooh, a Y2K butterfly baby tee is such a fun, nostalgic piece! Because baby tees are so fitted and cropped, the best styling rule is to balance out their proportions with looser bottoms, while playing into that 2000s aesthetic.

Here are 2 stylish outfit combinations using your wardrobe, anchored by your new thrifted find:

### Outfit 1: Effortless Off-Duty Model (Streetwear Vibe)
This look plays with proportions by pairing the ultra-tight baby tee with ultra-baggy denim, leaning hard into the Y2K skater/streetwear trend.

*   **The Thrifted Star:** Y2K Butterfly Baby Tee ($18.00)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Vintage black denim jacket (wear it off the shoulders or open to show off the tee)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Styling Tip:** Cinch the baggy jeans with a cool belt (even if you don't need one) to break up the look, and let the white sneakers tie in any white accents from the baby tee's butterfly print.

---

### Outfit 2: Edgy '90s Contrast (Sweet meets Tough)
This combination takes the sweet, feminine energy of the butterfly baby tee and toughens it up with dark hardware and structured trousers.

*   **The Thrifted Star:** Y2K Butterfly Baby Tee ($18.00)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt & Black crossbody bag

**Styling Tip:** Tuck the baby tee tightly into the wide-leg khakis and define your waist with the brown leather belt. The chunky black combat boots will peek out from under the wide trousers, giving it that cool, slightly grunge contrast against the playful top.

  Fit card: Scored the ultimate $18 Depop holy grail: a Y2K butterfly baby tee that’s giving total nostalgic perfection! I'm balancing out the tiny, cropped fit by styling it two ways—either paired with ultra-baggy dark denim and chunky sneakers for an off-duty model vibe, or toughened up with wide-leg khakis and combat boots. Which look are we wearing out? 🦋✨

1 model calls this session, 1 served from cache, 489 prompt + 87 output tokens

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

```
$ python -c "from tools import suggest_outfit; ..."

```
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; item = load_listings()[0]; print(suggest_outfit(item, get_example_wardrobe()))"

Ooh, a vintage pair of medium-wash Levi's 501s is the ultimate wardrobe holy grail! They have that timeless, structured denim feel that goes with literally everything.

Here are two effortless outfit combinations utilizing your current wardrobe to style your new $38 thrift find:

### Outfit 1: Effortless Off-Duty Streetwear
*This look plays with proportions by pairing the structured, straight-leg fit of the 501s with cozy, oversized layers for that cool-girl off-duty model aesthetic.*

* **The New Addition:** Vintage Levi's 501 Jeans (Medium Wash)
* **From Your Wardrobe:**
  * **Tops:** Oversized grey crewneck sweatshirt
  * **Shoes:** Chunky white sneakers
  * **Accessories:** Black crossbody bag, Brown leather belt

**Styling Tip:** Do a "French tuck" with the front of your grey crewneck into the waistband of the 501s (secured with your brown leather belt) to define your waist, while letting the back drape loosely. Finish with the chunky white sneakers and sling the black crossbody bag across your chest for an easy, everyday errand-running look.

---

### Outfit 2: Edgy Casual with a 90s Edge
*This look leans into a tougher, slightly grunge-inspired vibe by layering black pieces over the classic medium-wash denim.*

* **The New Addition:** Vintage Levi's 501 Jeans (Medium Wash)
* **From Your Wardrobe:**
  * **Tops:** White ribbed tank top
  * **Outerwear:** Vintage black denim jacket
  * **Shoes:** Black combat boots
  * **Accessories:** Brown leather belt, Black crossbody bag

**Styling Tip:** Tuck the white ribbed tank tightly into the jeans. Layer the vintage black denim jacket on top, but wear it off-the-shoulder or slouchy for a relaxed feel. Let the black combat boots peek out from under the hems of the 501s, and accessorize with your brown leather belt to tie the denim tones together.

```
$ python -c "from tools import create_fit_card; ..."

```
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; item = load_listings()[0]; print(create_fit_card('a relaxed striped tee with wide-leg jeans and white sneakers', item))"

Still chasing the high of scoring these vintage Levi's 501s on Depop for just $38—truly the thrift gods were smiling on me today. They have that 100% rigid cotton medium wash that only gets better with time, especially paired with a slouchy striped tee and crisp white sneakers. Excuse me while I wear this exact combo every single day until further notice.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI to help code `search_listings` and improve the no-results behavior.
- *What came back:* It suggested a generic fallback for empty results instead of telling the user whether the issue was likely in the description, size, or price.
- *What I changed:* I updated the no-results logic in `agent.py` so it identifies which part of the request is most likely too strict and gives the user a clearer, more actionable message.

**Moment 2**

- *What I asked for:* I asked whether the README/spec was specific enough that someone else could build the tool from it without needing follow-up clarifying questions.
- *What came back:* It flagged that the spec still needed precise rules for query parsing, filter logic, and how state moves between tools, especially in the empty-search and item-passing cases.
- *What I changed:* I tightened the Planning Loop and Tool Inventory so they name the actual inputs, output shapes, and stop conditions, and I rewrote the acceptance criteria to make them measurable rather than vague.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
