# Myntra Wishlist Growth Project

Growth team project to improve **W2P-30** — the % of users who purchase at least one wishlisted item within 30 days of adding it.

## Workstreams

| # | Workstream | Status |
|---|------------|--------|
| 1 | Goal & metric decomposition | ✅ `deck/slide-01-goal-metric-decomposition.md` |
| 2 | AI Discovery Engine | 🚧 `discovery/` |
| 3 | Insight synthesis | Pending |
| 4 | User research (5–6 interviews) | Pending |
| 5 | Problem framing | Pending |
| 6 | MVP | Pending |

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
  app.py                 # Streamlit 5-tab demo
data/
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
