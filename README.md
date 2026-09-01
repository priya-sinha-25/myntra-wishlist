# Myntra Wishlist Growth Project

Growth team project to improve **W2P-30** — the % of users who purchase at least one wishlisted item within 30 days of adding it.

## Workstreams

| # | Workstream | Status |
|---|------------|--------|
| 1 | Goal & metric decomposition | ✅ `deck/slide-01-goal-metric-decomposition.md` |
| 3 | Primary research (survey n=18) | ✅ `research/survey-findings.md` |
| 4 | Problem framing | ✅ `deck/slide-04-problem-definition.md` |
| 5 | MVP — Confidence Brief | ✅ **Standalone Myntra app** (`mvp/app.py`) |
| 6 | Metrics & risks | Pending deck slides |

## Wishlist Confidence Brief MVP (Part 5 — Live)

Standalone **Myntra.com-style** prototype matching the Stitch screens — not inside the Discovery Engine.

```powershell
.\.venv\Scripts\python.exe -m streamlit run mvp/app.py
```

**Flow (matches Stitch prototype):**
1. **Home** — Shop by Category (click **Open Wishlist**)
2. **Wishlist** — 4 product cards with Brief Ready / locked states
3. **Get Confidence Brief** — Groq AI modal (size M circle, key insights)
4. **Add to Bag** — success toast + bag badge + “In Bag” on card
5. **Libas (locked)** — progress bar modal (5/7 days)

**Eligibility:** `brief_ready` on catalog items; Libas locked until 7 days.

**Code:**
- `mvp/app.py` — screen router (home → wishlist → brief → success)
- `mvp/screens.py` — Stitch-matched HTML/CSS
- `discovery/confidence_brief.py` — Groq brief generator
- `data/mvp/wishlist_catalog.json` — demo products + Stitch image URLs
- `stitch_prototype/` — exported Stitch HTML reference

**Discovery engine** (separate): `streamlit run discovery/app.py`

**Honesty:** Catalog is curated demo data. AI brief generation is **live Groq**. Cart/checkout simulated.

## Discovery Engine (Workstream 2)

Automated pipeline to classify public Myntra feedback at scale.

### Setup

```bash
cd "C:\project myntra"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq API key to `.env` (free tier works). Without it, the pipeline uses a heuristic fallback classifier.

### Run pipeline

```bash
python -m discovery.run_pipeline --import-seeds --scrape-count 350
```

Steps:
1. Import manual seed sources (Reddit/forum/social samples)
2. Scrape Myntra Play Store reviews
3. Classify with Groq LLM (or heuristic fallback)
4. Aggregate insights → `data/insights/insights.json`
5. Export validation sample for human labeling

### Live scrape in demo (Tab 1)

```powershell
.\.venv\Scripts\python.exe -m streamlit run discovery/app.py
```

Click **Scrape & classify live** — fetches fresh Play Store reviews in real time.

### Daily GitHub schedule (10:00 AM IST)

See **`docs/GITHUB_SCHEDULE.md`** — push repo, add `GROQ_API_KEY` secret, workflow runs daily.

```powershell
python -m discovery.daily_sync --scrape-count 100
```

### Launch demo (legacy command)

```bash
streamlit run discovery/app.py
```

### Project structure

```
discovery/
  scrape_play_store.py   # Play Store scraper
  paste_importer.py      # CSV/JSON importer
  classify.py            # LLM classifier
  aggregate.py           # Theme counts + crosstabs
  validate.py            # Human validation sample
  run_pipeline.py        # Orchestrator
  app.py                 # Streamlit demo (7 tabs incl. Wishlist MVP)
  confidence_brief.py    # AI Confidence Brief generator
  mvp_wishlist_ui.py     # Wishlist MVP UI
data/
  mvp/wishlist_catalog.json
  raw/corpus.json
  classified/tagged_reviews.json
  insights/insights.json
deck/
  slide-01-goal-metric-decomposition.md
```

## Taxonomy

11-field JSON schema in `discovery/schemas/taxonomy.json`:
- wishlist_related, funnel_step, blocker_type, segment_signal
- signal_type (`noise` | `real` | `silent`)
- addressable_without_discount, intent_strength, theme_label, evidence_quote

## Constraint

No monetary incentives to users — discovery focuses on confidence/decision gaps, not discounts.
