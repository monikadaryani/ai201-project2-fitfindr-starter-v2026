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

**Moment 3**

- *What I asked for:* I asked AI to argue the opposite verdict on the project criteria so I could test whether my own judgments were too strict or whether the rubric itself was too ambiguous.
- *What came back:* It argued that the project should be judged by behavior under imperfect data rather than by perfect catalog metadata, and that stopping on unverifiable size or price is a form of respecting the user’s constraints.
- *What I changed:* I kept the rubric as written but clarified the logic in my diagnosis: the system is not necessarily failing when it refuses to continue with an unverifiable match, because that is a conservative and safer interpretation of size and price compliance.

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
| 1. matching query completes | 4/5 | MET  | MET  | MET  | MET  | MET  | MET |
| 2. impossible query stops early | 5/5 | MET  |  MET | MET  | MET  |  MET | MET |
| empty wardrobe _(diagnostic — not one of your five)_ | 5/5 |  MET | MET  | MET  | MET  | MET  | MET |
| 3. selected item stays consistent | 5/5 | MET  | MET  | MET  | MET  | MET  | MET |
| 4. fit card names item and price | 4/5 |  MET |  MET |  MET | MET  |  MET | MET |
| 5. selected item respects size and price | 5/5 | MISSED | MISSED  | MISSED  | MISSED  | MISSED  | MISSED |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Ooh, what a fun find! A Y2K butterfly print baby tee is the ultimate nostalgic, playful piece. Because it’s fi…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Found this absolute gem of a Y2K butterfly baby tee on Depop for just $18, and it’s giving major early-2000s n…
  try 1: completed — fit card 371 chars

impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    empty result; stopping before suggest_outfit
  try 1: stopped early — No listings match size XXS. The catalog uses sizes like L, L
empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +4 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! A cropped, light-wash denim jacket is one of the most versatile and high-ROI pieces you can thrift.…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Scored this cropped light-wash denim jacket on Poshmark for just $42, and honestly, it’s about to be the harde…
  try 1: completed — fit card 373 chars

selected item stays consistent  (example wardrobe)
  query: denim jacket under $50
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +4 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! That light wash, cropped thrifted denim jacket is an absolute gem. A lighter wash provides a cool c…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Scored this vintage light-wash cropped denim jacket on Poshmark for just $42, and it is officially my new favo…
  try 1: completed — fit card 442 chars

fit card names item and price  (example wardrobe)
  query: vintage graphic tee under $30
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
  [rate limit] 15 requests used this minute. Waiting 32s. This is normal.
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Ooh, a Y2K butterfly baby tee is such a fun piece! Since baby tees are fitted and cropped, they create a fanta…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Scored this Y2K butterfly baby tee on Depop for just $18, and I am officially obsessed! It creates the dreamie…
  try 1: completed — fit card 389 chars


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
| 1 | matching query completes | 4/5 | MET | For all the matching listing, the agent completes all three tool calls and returns a fit card — in 5 of 5 tries. |
| 2 | impossible query stops early | 5/5 | MET | For all impossible queries, the agent stops early and names what needs to be changed if possible. |
| 3 | selected item stays consistent | 5/5 | MET | The selected item stays consistent across all function calls |
| 4 | fit card names item and price | 4/5 | MET | The fit card names the price if available and the item. |
| 5 | selected item respects size and price | 5/5 | MISSED | The searched item in all the tries didn't have the size, so it isn't possible to verify the size constraint |

**Diagnoses**

1. For criterion 5, the selected item often lacked a verifiable size or price. The wording was also ambiguous because it did not say what should happen when a listing omits one of those fields.

This miss happened at the loop/tool boundary. The search tool returned a candidate that did not meet the user’s stated size or price constraints, and the loop continued without re-checking the selected item before moving on. The mechanism was missing constraint enforcement after selection.

The fix is to enforce the constraint after selection or to search again with a stricter filter and return a clear message when the listing does not include a verifiable size or price.

2. For criterion 2, it worked on the main run file, but additional queries showed that it cannot always identify the root cause. When it cannot confidently classify the empty result as a description, size, or budget issue, it falls back to a generic message instead of naming the specific fix.

This miss is in the diagnostic branch, not in the stop condition. The agent does stop before suggest_outfit, but the explanation logic is sometimes too weak to tell whether the issue is description, size, or price.




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
python app.py ask 'sneakers below $40' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 1 items: Low-Top Canvas Sneakers — Off-White
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Hey there! Those off-white low-top canvas sneakers are an absolute steal for $20—they are timeless, effortless…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Score! 👟 snagged these off-white canvas low-tops on Poshmark for literally just $20, and I am obsessed. They’v…

  Found:    Low-Top Canvas Sneakers — Off-White — $20.0 on poshmark

  Outfit:   Hey there! Those off-white low-top canvas sneakers are an absolute steal for $20—they are timeless, effortlessly cool, and go with literally everything.

Since those sneakers have a casual, vintage-inspired vibe, I've put together two distinct outfits using pieces straight from your wardrobe. Here is how we're styling them:

### Outfit 1: Casual '90s Off-Duty
*This look leans into a relaxed, effortless aesthetic. The baggy denim paired with the low-profile sneakers creates a classic, balanced silhouette.*

* **Thrifted Addition:** Low-Top Canvas Sneakers (Off-White)
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Tops:** White ribbed tank top
* **Outerwear:** Vintage black denim jacket
* **Accessories:** Black crossbody bag

**Styling Tip:** Tuck the white tank top into the dark wash jeans, add the black crossbody bag, and drape the vintage black denim jacket over your shoulders for a double-denim moment that feels modern and cool.

---

### Outfit 2: Elevated Streetwear Prep
*This look mixes structured, tailored pieces with sporty, casual elements for a high-low vibe that feels very current.*

* **Thrifted Addition:** Low-Top Canvas Sneakers (Off-White)
* **Bottoms:** Wide-leg khaki trousers
* **Tops:** Black cropped zip hoodie
* **Accessories:** Brown leather belt, Black crossbody bag

**Styling Tip:** Cinch the wide-leg khaki trousers with the brown leather belt, and wear the black cropped zip hoodie zipped up (or partially unzipped with a hint of collarbone showing). The off-white sneakers will pop against the warm khaki tones, keeping the outfit from feeling too formal.

Which one are you wearing first?

  Fit card: Score! 👟 snagged these off-white canvas low-tops on Poshmark for literally just $20, and I am obsessed. They’ve got that perfect vintage, beaten-in vibe that goes with literally everything in my closet—whether we're leaning into a '90s double-denim moment or keeping it sporty with wide-leg khakis. Tell me the truth: are you rocking the baggy jeans or the tailored trousers first? ✨

2 model calls this session, 591 prompt + 480 output tokens

```

**Empty search**

```
python app.py ask 'blouse below $50' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    empty result; stopping before suggest_outfit

  No listings match the description 'blouse'. This looks more like a description mismatch than a budget problem. Try broader keywords or a different item type.

0 model calls this session
```

**On the MCP move:**
I rewired the branch in `run_agent()` from the direct `search_listings()` call to `mcp_client.call_tool("search_listings", {...})` and kept the same session flow afterwards. The call shape changed from a direct Python function invocation to an MCP tool payload, but the returned value still had to be the list of matching listings and the empty-list handling had to remain the same. The happy path still completed normally, and the empty-search branch still stopped before `suggest_outfit()`. The behavior did not change materially after the rewire; the important difference was that the tool call now passed through the MCP transport instead of a direct in-process function call.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
I added a second validation step in `agent.py` after selecting the first search result. The agent now checks whether the chosen listing still satisfies the user’s requested size and maximum price before it continues to `suggest_outfit()`. If the item is missing a size or price, the size is wrong, or the price is over budget, it stops and stores a precise `session["error"]` message instead of styling an invalid item.

**Which failure it was meant to fix:**
This was meant to fix the loop continuing after a candidate item failed the user’s original constraints, especially when the listing omitted size/price information or the item exceeded the requested budget. The bug was not only in the empty-search branch; it was also in the post-selection logic that never re-validated the chosen item.

This fix is in place, but I have not yet proven it on a real non-empty selected-item case, because the current catalog filters size and price before selection and most failing examples terminate earlier with an empty-search branch.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4/5 | MET | MET | MET | MET | MET | MET |
| 2. impossible query stops early | 5/5 | MET | MET | MET | MET | MET | MET |
| 3. selected item stays consistent | 5/5 | MET | MET | MET | MET | MET | MET |
| 4. fit card names item and price | 4/5 | MET | MET | MET | MET | MET | MET |
| 5. selected item respects size and price | 5/5 | MISSED | MISSED | MISSED | MISSED | MISSED | MISSED |

**Did it help, and how do I know:**

The new guard is active and prevents the loop from continuing when the chosen item is missing or invalid on size/price. I can confirm the code path exists and returns a clear `session["error"]` when it is triggered, but I cannot honestly mark criterion 5 as MET yet because the current catalog still reaches the stop condition earlier through empty-search results more often than through a non-empty selected-item failure. In other words, the fix is present, but the proof case for a real selected-item violation is still missing.



---

## What's Still Broken

Criterion 5 is still the main unresolved issue. The guard is now in place in `agent.py`, but I have not yet proven it on a real non-empty selected-item case. In this dataset, most size or budget failures never reach the selection step because the earlier empty-search branch stops first. That means the app is safer than before, but it still needs a direct proof case: a listing that survives the search layer, is chosen as the item, and then fails the user’s size or price constraints before styling begins.

The next thing I would do is create or find a test case where the result list is non-empty but the selected item is still invalid. For example, a query with a size constraint where the catalog contains a candidate with a mismatched or missing size field, or a budget query where the chosen item is priced above the cap. The fix would be to run that exact case through `run_agent()` and confirm the session stops with a clear error and no outfit or fit card is generated.

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

---

---

## Capstone

**The System**

FitFindr, the thrift-shopping agent from units 3 and 4: parse the query → `search_listings` (over MCP) → `suggest_outfit` → `create_fit_card`. I picked it because I know where it's weak. Its search is a literal keyword match, and in unit 4 I saw that weakness show up directly in the results.

**The Shape**

Shape C: extend one capability. I'm adding **semantic search** as a second retrieval strategy next to the existing keyword search in `search_listings` (`tools.py`). Keyword search only finds a listing that shares exact words with the query, so "band shirt" can miss a listing written as "graphic tee". Semantic search embeds the query and the 40 listings with a Gemini embedding model and ranks by similarity, so it can match on meaning. Listing embeddings are computed once and cached to disk. Size and price filters work exactly as before. A minimum similarity score makes an impossible query still return an empty list, so the existing stop-before-`suggest_outfit` branch keeps working. A setting in `config.py` picks the strategy, so I can run the same scenarios through both and compare. Alongside it, as every shape requires: one structured JSON log line per request, a measured cost per run for each strategy, and a Path B run path (one documented command, run locally, with a committed log).

**Out of Scope**

- **Blending keyword and semantic scores into one hybrid ranking.** It's tempting, but it would add weights to tune and make it impossible to say which strategy produced a result. Comparing the two cleanly is the evidence this shape needs.
- **Improving the "no match" message from unit 4's criterion 2** (`agent.py`, lines 244–255). When it can't tell whether the description, size or price caused the miss, it falls back to a generic line. I'm not fixing that, and I'm not rewriting it to use embeddings either. It stays keyword-based. Either change would be a second capability.
- **Fixing criterion 5 from unit 4** (the selected item must match the requested size and price). It's a bug in the existing size filter, not part of the new capability, so it stays listed under What's Still Broken above.
- **Hosting it (Path A) or adding a UI.** It runs locally under Path B and is used through `POST /ask`. A host signup and a frontend would take time away from testing and add nothing the brief scores.

No stretch goals this unit.

**Size Check**

About 90 minutes of building, estimated:

- Embedding the listings and caching them: ~20 min
- Query embedding, similarity ranking and the minimum score: ~25 min
- The `config.py` setting, wired through the MCP search call: ~15 min
- The JSON log line in `serve.py`: ~20 min
- The `RUNNING.md` command: ~10 min

The riskiest part is choosing the minimum score. If it runs long, I'll pick one value from a handful of known-good and known-impossible queries and record that choice, rather than tuning it further.


**Run Path**

Path B, local with logs. One command starts it, `AI201_SEARCH=semantic python serve.py`. The environment it needs and how to call it are in [RUNNING.md](RUNNING.md) under "Capstone run path". I tested those instructions on a fresh clone of this repo in a new folder. The only failure was the placeholder API key in `.env`, which the instructions tell you to replace. The test also caught that the first semantic search made 40 separate token-counting calls, which I batched into one before any trials.

**Instrumentation**

Every run writes one JSON line to `logs/runs.jsonl` through `runlog.py::logged_run`, from the CLI (`app.py ask`), the HTTP server (`serve.py` `/ask`) and the trial runner (`capstone_eval.py::run`). The record is written in a `finally` block, so runs that stop early, crash or are rejected (a 400 from `/ask`) are logged too. The fields are documented at the top of `runlog.py`. The ones specific to this extension are `strategy`, `search_ms` (the MCP search call alone), `embed_calls`, `embed_tokens` and `count_ms`. The embedding happens inside the MCP server process, which the agent's own counters can't see, so `mcp_server.py` writes each search's embedding usage to `.cache/last_search_usage.json` and `agent.py::run_agent` reads it back.

Twelve real entries from `logs/runs.jsonl`, unedited except that `fit_card` is cut to 70 characters to keep lines readable:

```jsonl
{"ts": "2026-11-17T06:40:03.406+00:00", "run_id": "61689b8c", "source": "eval", "outcome": "fit_card", "query": "leather motorcycle coat", "strategy": "semantic", "parsed": {"description": "leather motorcycle coat", "size": null, "max_price": null}, "n_results": 1, "selected_id": "lst_022", "selected_title": "90s Leather Bomber — Black", "selected_price": 75.0, "error": null, "fit_card": "Still pinching myself over finding this butter-soft 90s leather bomber…", "duration_ms": 23354, "search_ms": 1242, "model_calls": 2, "prompt_tokens": 756, "output_tokens": 648, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 4, "count_ms": 127, "cache_enabled": false}
{"ts": "2026-11-17T06:40:11.833+00:00", "run_id": "37bd7e52", "source": "eval", "outcome": "fit_card", "query": "leather motorcycle coat", "strategy": "keyword", "parsed": {"description": "leather motorcycle coat", "size": null, "max_price": null}, "n_results": 4, "selected_id": "lst_014", "selected_title": "Leather Belt — Brown, Braided", "selected_price": 12.0, "error": null, "fit_card": "Found the ultimate 90s vintage steal on thredUp: this gorgeous brown b…", "duration_ms": 8420, "search_ms": 444, "model_calls": 2, "prompt_tokens": 680, "output_tokens": 559, "cache_hits": 0, "embed_calls": 0, "embed_tokens": 0, "count_ms": 0, "cache_enabled": false}
{"ts": "2026-11-17T06:40:23.951+00:00", "run_id": "31e83ebf", "source": "eval", "outcome": "fit_card", "query": "ankle booties", "strategy": "semantic", "parsed": {"description": "ankle booties", "size": null, "max_price": null}, "n_results": 1, "selected_id": "lst_028", "selected_title": "Suede Chelsea Boots — Tan", "selected_price": 44.0, "error": null, "fit_card": "Score! I just hunted down these tan suede Chelsea boots on Poshmark fo…", "duration_ms": 3921, "search_ms": 1094, "model_calls": 2, "prompt_tokens": 626, "output_tokens": 536, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 116, "cache_enabled": false}
{"ts": "2026-11-17T06:40:24.279+00:00", "run_id": "d1b75ef3", "source": "eval", "outcome": "stopped", "query": "ankle booties", "strategy": "keyword", "parsed": {"description": "ankle booties", "size": null, "max_price": null}, "n_results": 0, "selected_id": null, "selected_title": null, "selected_price": null, "error": "No listings match the description 'ankle booties'. This looks more like a description mismatch than a budget problem. Try broader keywords or a different item type.", "fit_card": null, "duration_ms": 323, "search_ms": 322, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_hits": 0, "embed_calls": 0, "embed_tokens": 0, "count_ms": 0, "cache_enabled": false}
{"ts": "2026-11-17T06:41:15.562+00:00", "run_id": "0d7f98bd", "source": "eval", "outcome": "stopped", "query": "black tuxedo", "strategy": "semantic", "parsed": {"description": "black tuxedo", "size": null, "max_price": null}, "n_results": 0, "selected_id": null, "selected_title": null, "selected_price": null, "error": "No listings match 'black tuxedo'. Try broader keywords or a more general description.", "fit_card": null, "duration_ms": 1035, "search_ms": 1034, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 115, "cache_enabled": false}
{"ts": "2026-11-17T06:41:18.713+00:00", "run_id": "fee4faad", "source": "eval", "outcome": "stopped", "query": "pearl necklace", "strategy": "semantic", "parsed": {"description": "pearl necklace", "size": null, "max_price": null}, "n_results": 0, "selected_id": null, "selected_title": null, "selected_price": null, "error": "No listings match the description 'pearl necklace'. This looks more like a description mismatch than a budget problem. Try broader keywords or a different item type.", "fit_card": null, "duration_ms": 1032, "search_ms": 1031, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 109, "cache_enabled": false}
{"ts": "2026-11-17T06:41:34.326+00:00", "run_id": "e67eb0d3", "source": "eval", "outcome": "fit_card", "query": "vintage graphic tee under $30", "strategy": "semantic", "parsed": {"description": "vintage graphic tee", "size": null, "max_price": 30.0}, "n_results": 9, "selected_id": "lst_033", "selected_title": "Vintage Band Tee — Faded Grey", "selected_price": 19.0, "error": null, "fit_card": "Scored this perfectly faded grey vintage band tee on Depop for just $1…", "duration_ms": 4517, "search_ms": 1010, "model_calls": 2, "prompt_tokens": 620, "output_tokens": 493, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 4, "count_ms": 102, "cache_enabled": false}
{"ts": "2026-11-17T06:41:41.835+00:00", "run_id": "c4d533b6", "source": "eval", "outcome": "fit_card", "query": "denim jacket under $50", "strategy": "semantic", "parsed": {"description": "denim jacket", "size": null, "max_price": 50.0}, "n_results": 3, "selected_id": "lst_007", "selected_title": "Denim Jacket — Light Wash, Cropped", "selected_price": 42.0, "error": null, "fit_card": "Scored this light wash cropped denim jacket on Poshmark for just $42, …", "duration_ms": 4349, "search_ms": 1038, "model_calls": 2, "prompt_tokens": 707, "output_tokens": 591, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 110, "cache_enabled": false}
{"ts": "2026-11-17T06:41:21.833+00:00", "run_id": "9a826618", "source": "eval", "outcome": "stopped", "query": "leather jacket less than $40", "strategy": "semantic", "parsed": {"description": "leather jacket", "size": null, "max_price": 40.0}, "n_results": 0, "selected_id": null, "selected_title": null, "selected_price": null, "error": "No listings fit within your budget of $40. Try a higher max price or a broader description.", "fit_card": null, "duration_ms": 1033, "search_ms": 1032, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 109, "cache_enabled": false}
{"ts": "2026-11-17T06:41:28.763+00:00", "run_id": "a13e2046", "source": "eval", "outcome": "fit_card", "query": "velvet blazer max $40", "strategy": "semantic", "parsed": {"description": "velvet blazer", "size": null, "max_price": 40.0}, "n_results": 1, "selected_id": "lst_018", "selected_title": "Vintage Linen Blazer — Cream", "selected_price": 38.0, "error": null, "fit_card": "Scored this vintage cream linen blazer on thredUp for just $38, and I …", "duration_ms": 6929, "search_ms": 1014, "model_calls": 2, "prompt_tokens": 669, "output_tokens": 555, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 3, "count_ms": 102, "cache_enabled": false}
{"ts": "2026-11-17T05:45:44.556+00:00", "run_id": "6e72450e", "source": "eval", "outcome": "fit_card", "query": "velvet blazer max $40", "strategy": "semantic", "parsed": {"description": "velvet blazer max $40", "size": null, "max_price": null}, "n_results": 2, "selected_id": "lst_036", "selected_title": "Velvet Blazer — Emerald Green", "selected_price": 52.0, "error": null, "fit_card": "Scored this emerald green velvet blazer on Depop for just $52, and hon…", "duration_ms": 14966, "search_ms": 1475, "model_calls": 2, "prompt_tokens": 722, "output_tokens": 614, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 7, "count_ms": 214, "cache_enabled": false}
{"ts": "2026-11-17T05:50:34.995+00:00", "run_id": "f4264e8a", "source": "eval", "outcome": "stopped", "query": "vintage graphic tee under $30", "strategy": "semantic", "parsed": {"description": "vintage graphic tee", "size": null, "max_price": 30.0}, "n_results": 9, "selected_id": "lst_033", "selected_title": "Vintage Band Tee — Faded Grey", "selected_price": 19.0, "error": "The styling model is unavailable right now. Please try again later.", "fit_card": null, "duration_ms": 20666, "search_ms": 1244, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0, "cache_hits": 0, "embed_calls": 1, "embed_tokens": 4, "count_ms": 115, "cache_enabled": false}
```

Reading them: entries 1–2 are the extension's point. "leather motorcycle coat" finds the Leather Bomber (lst_022) with semantic search and a leather belt (lst_014) with keyword search. Entries 3–4 show keyword search finding nothing for "ankle booties" while semantic search finds the Chelsea Boots. Entries 5–6 are deliberate failures: impossible queries stopped before `suggest_outfit` with `n_results: 0`. Entries 10 and 11 are the same query after and before the improvement. Before (entry 11), no price was parsed and the $52 Velvet Blazer was picked. After (entry 10), the price is parsed and it's the $38 Linen Blazer.

**Failed runs:** entry 12 is a real, unplanned failure from the 21:42 before-run. The search worked and picked lst_033, but the text model failed in `suggest_outfit`, so the agent stopped with `outcome: "stopped"`, `model_calls: 1` and no fit card. That's 14 such failures across both before-runs (8 + 6), all logged. A whole broken run is kept in `results/invalid/`: the first attempt ran under the wrong Python, all 72 searches failed with `No module named 'mcp'`, and every one left a record with the error.

**What It Costs**

Measured with `python capstone_eval.py --cost`: 10 runs of "vintage graphic tee under $30" with each strategy, response cache off, listing embeddings already cached. All 20 runs completed with a fit card. The numbers are averaged from those 20 records in `logs/runs.jsonl` (lines 145–164). Token counts are what the service reported for the text model (`usage_metadata`). For the embedding they come from the service's `count_tokens` for the exact text embedded, because the embedding API doesn't report usage.

| Per run (average of 10) | Keyword | Semantic |
|---|---|---|
| Text-model calls | 2.00 | 2.00 |
| Embedding calls | 0 | 1.00 |
| Input tokens (text model) | 649.9 | 624.5 |
| Output tokens (text model) | 532.0 | 516.5 |
| Embedding tokens | 0 | 4.0 |
| Duration, end to end | 6,988 ms | 7,246 ms |
| Search step (`search_ms`) | 329 ms | 1,155 ms |

In dollars, at $0.30 per 1M input and $2.50 per 1M output tokens for `gemini-3.5-flash-lite`: **about $0.0015 per run for both strategies** (keyword ≈ $0.00152, semantic ≈ $0.00148). Those prices come from third-party price listings (looked up 2026-11-16), not Google's own pricing page, so check them there. The 4 embedding tokens add under $0.000001 at any listed embedding price. Actual spend was **$0**, because this runs on the free tier.

The tokens show that semantic search costs almost nothing extra: 4 tokens and one API call per run. Semantic's text-model tokens are slightly *lower* only because it picks a different tee (lst_033, not lst_002), whose description is shorter. The real cost of semantic search is **time**: about 0.8 s more per search (one embedding round trip plus the ~100 ms token count), roughly 4% of a 7-second run.

**Run Log — Before**

Run by `capstone_eval.py::trials`, scored by `capstone_eval.py::score`. Three runs per criterion, cache off. The full report is in `results/capstone_before_2026-11-16_1653.md`, with every raw record in the `.json` beside it.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Semantic search finds paraphrased items | ≥4 of 5 each run; 3-run total beats keyword | 5/5 (kw 2/5) | 5/5 (kw 2/5) | 5/5 (kw 2/5) | MET (15/15 vs kw 6/15) |
| 2. Impossible queries stop before suggest_outfit | ≥4 of 5 each run | 5/5 | 5/5 | 5/5 | MET |
| 3. Queries that already worked still work | 2 of 2 each run (6 of 6) | 2/2 | 2/2 | 1/2 | MISSED |
| 4. Semantic adds 1 API call, query embedding ≤20 tokens | 1 of 1 each run (3 of 3) | 1/1 (+1 call, 4 tok) | 1/1 (+1 call, 4 tok) | 1/1 (+1 call, 4 tok) | MET |
| 5. Never selects an item over the user's price | 5 of 5 each run | 2/5 | 2/5 | 2/5 | MISSED |

I ran the whole thing a second time before changing anything (`results/capstone_before_2026-11-16_2142.md`). Criteria 1, 2 and 5 came out identical. Criteria 3 and 4 didn't: C3 was 2/2, 0/2, 2/2 and C4 was 1/1, 0/1, 1/1, both MISSED. That disagreement is part of the diagnosis below.

**Real output, one run per criterion** (from `capstone_eval.py::report`, before-run 21:42 unless noted):

```
1. Paraphrases — selected id (semantic / keyword), all three runs identical
   leather motorcycle coat  lst_022 / lst_014     flowery summer frock  lst_013 / lst_023
   ankle booties            lst_028 / None        chunky wool sweater   lst_008 / lst_008
   gym shorts               lst_026 / lst_026
2. Impossible queries: Trial 1: 5/5 stopped  Trial 2: 5/5 stopped  Trial 3: 5/5 stopped
3. Trial 2 | vintage graphic tee under $30 | ('stopped', 'lst_033', 19.0) | MISSED
   error: "The styling model is unavailable right now. Please try again later."
4. Trial 2 | extra API calls 0 | embed tokens 4 | MISSED   (trials 1 and 3: +1 call, 4 tokens, MET)
5. leather jacket less than $40 | lst_022 / 75.0 / None   (selected id / price / parsed max_price)
   velvet blazer max $40        | lst_036 / 52.0 / None
   platform shoes $40 or less   | lst_019 / 48.0 / None
```

**Verdicts and Diagnoses**

| # | Verdict (before) | How I decided |
|---|---|---|
| 1 | MET | Semantic found the intended listing 15 of 15 times. Keyword found it 6 of 15 times. |
| 2 | MET | All 15 impossible-query runs returned an empty list and stopped before `suggest_outfit`. None leaked. |
| 3 | MISSED | 5 of 6 in one before-run and 4 of 6 in the other. Every miss was a run that stopped with "model is unavailable". |
| 4 | MISSED (21:42) / MET (16:53) | The embedding side was +1 call and 4 tokens in every trial of both runs. The one miss was a run with one fewer *text-model* call. |
| 5 | MISSED | 2 of 5 in every run of both before-runs, always the same three queries. |

*Criterion 5: the query parser.* The miss was in `agent.py::parse_query`, not in semantic search or the search tool. The price pattern only knew "under / below / at most / up to / <=". "less than $40", "max $40" and "$40 or less" came out with `max_price: None`. `search_listings` therefore had no ceiling to filter on, and semantic search did exactly its job: it ranked the closest-meaning item first. Those were the $75 Leather Bomber, the $52 Velvet Blazer and the $48 Platform Sneakers. The leftover "less than $40" also stayed in the description and was embedded as part of the item. The same result came back every run because both the parsing and the embeddings are deterministic. Semantic search didn't create this gap, since it's been in the parser since unit 3, but it makes it matter more: it encourages natural wording, and it always finds *something* to rank first.

*Criteria 3 and 4: the model call, not the search.* Every miss on these two was the same failure: `suggest_outfit` raised `ModelUnavailable`, so the agent stopped with "The styling model is unavailable right now" before `create_fit_card`. It happened 8 times in the 16:53 run and 6 in the 21:42 run, under both strategies, spread across the run. The mechanism is in `generate.py::generate`: it retries rate limits (429) only, and turns any other error, including a temporary unavailable/overloaded response, into `ModelUnavailable` on the first attempt. I can't name the exact error code, because `agent.py::run_agent` replaces the exception with a fixed sentence, so the original text never reaches the log. For criterion 4 this also exposed a weakness in how the criterion is counted: it compares total API calls of two whole runs, so a failure anywhere in the run moves the count. Search behaved correctly in every trial.

**The Improvement**

**What I changed:** `agent.py::parse_query` now recognises price wording before the number ("less than", "no more than", "max", "maximum of") and after it ("$40 or less", "$40 or under", "$40 max"). One change, in one function.

**Why the diagnosis pointed at it:** criterion 5 missed the same three queries every time, and in each one `parsed.max_price` was `None`. Before running anything, I compared the old and new parser on every query the criteria use plus the unit 4 scenarios. Only those three queries parse differently, so the change couldn't move criteria 1–4.

**Run Log — After** (`results/capstone_after_2026-11-16_2239.md`)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Semantic search finds paraphrased items | ≥4 of 5 each run; 3-run total beats keyword | 5/5 (kw 2/5) | 5/5 (kw 2/5) | 5/5 (kw 2/5) | MET (15/15 vs kw 6/15) |
| 2. Impossible queries stop before suggest_outfit | ≥4 of 5 each run | 5/5 | 5/5 | 5/5 | MET |
| 3. Queries that already worked still work | 2 of 2 each run (6 of 6) | 2/2 | 2/2 | 2/2 | MET |
| 4. Semantic adds 1 API call, query embedding ≤20 tokens | 1 of 1 each run (3 of 3) | 1/1 (+1 call, 4 tok) | 1/1 (+1 call, 4 tok) | 1/1 (+1 call, 4 tok) | MET |
| 5. Never selects an item over the user's price | 5 of 5 each run | 5/5 | 5/5 | 5/5 | MET |

**Side by side**

| Criterion | Before (16:53) | Before (21:42) | After | Caused by the change? |
|---|---|---|---|---|
| 1 | MET | MET | MET | — |
| 2 | MET | MET | MET | — |
| 3 | MISSED (5/6) | MISSED (4/6) | MET (6/6) | **No** |
| 4 | MET | MISSED (2/3) | MET | **No** |
| 5 | MISSED (2/5 ×3) | MISSED (2/5 ×3) | **MET (5/5 ×3)** | **Yes** |

**Did it help, and how do I know:** For criterion 5, yes. The three queries that failed every time before now parse to `max_price: 40.0` in all three runs. Two now stop, with no leather jacket or platform shoe under $40. "velvet blazer max $40" now picks the $38 Linen Blazer instead of the $52 Velvet Blazer.

Criteria 3 and 4 also turned MET, **but not because of my change.** Their queries parse identically before and after. The after-run simply had zero "model is unavailable" failures, against 8 and 6 in the two before-runs. Nothing about the cause has been fixed.

**What's Still Broken**

1. **Temporary model failures aren't retried** (`generate.py::generate`). This caused every criterion 3 and 4 miss, and it's still there; the after-run was lucky. Next I'd retry temporary unavailable/overloaded errors with the same backoff already used for rate limits. I'd also log the original exception text instead of `agent.py`'s fixed sentence, so the error code is visible. I stopped short of this because it was my second improvement, and a fix for a random failure can't be proven in three runs. It needs many runs, or a deliberately injected failure, to show anything.
2. **Criterion 4 counts calls across the whole run.** Better wording would count embedding calls directly ("exactly 1 embedding call per semantic run"), so an unrelated failure can't move it. I haven't changed it, because criteria don't get rewritten after results.
3. **"velvet blazer max $40" returns a blazer that isn't velvet.** With no velvet blazer under $40, semantic search offers the closest blazer instead of stopping. That's within budget, so criterion 5 passes, but it's arguably a near-miss the user didn't ask for. Raising `SEMANTIC_MIN_SCORE` would stop it, but it would also put criterion 1 at risk, because the 0.62 cutoff sits in a gap only about 0.06 wide.
4. **The stop message still blames the wrong thing for semantic stops.** It still uses keyword logic (out of scope this unit), so a semantic stop can say "No listings fit within your budget" when the real issue is the description.
5. **Smaller:** "no more than 20 dollars" leaves "dollars" in the description. The size filter is still an exact string match ("M" never matches "S/M"; unit 4 criterion 5, out of scope).

**How I Used AI**

I worked with Claude (Claude Code) throughout this unit.
- **Planning:** it helped me compare the three shapes and draft the scope.
- **Code:** it wrote the semantic search code (`semantic.py`, `generate.py::embed`), the logging (`runlog.py`), the trial runner (`capstone_eval.py`) and the parser change.
- **Criteria:** I picked which five to use and made the key decisions: compare totals for criterion 1, lower criterion 2 to 4 of 5, keep a loose regression check, drop the timing criterion because measuring only warm runs felt like cheating, and replace it with the price ceiling. Claude drafted much of the criteria wording, including the "why this target" reasons for criteria 3 and 5. The course asks for criteria written unaided, so I'm stating that plainly.
- **Feedback I acted on:** a self-check review showed criterion 3's "same category" check would pass a cardigan for a graphic tee, so I changed it to a list of acceptable listing IDs fixed before testing.
- **What I caught by running it:** my first before-run used the wrong Python and every search failed. The trial runner had scored criteria 2 and 5 as MET anyway, because the agent turned the crash into a clean stop. That run is kept in `results/invalid/` and the runner was fixed before the real run.
