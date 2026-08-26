# Workstream 2 — AI Discovery Engine

## What was built

| Component | File | Purpose |
|-----------|------|---------|
| Play Store scraper | `discovery/scrape_play_store.py` | Fetch Myntra reviews (target ~350) |
| Manual importer | `discovery/paste_importer.py` | Import Reddit/forum/social CSV |
| Classifier | `discovery/classify.py` | Groq LLM or heuristic fallback |
| Aggregator | `discovery/aggregate.py` | Theme counts, crosstabs, quotes |
| Validation | `discovery/validate.py` | 40-item human validation sample |
| Pipeline | `discovery/run_pipeline.py` | End-to-end orchestrator |
| Offline bootstrap | `discovery/bootstrap_offline.py` | Run on seeds without API |
| **Live scrape** | `discovery/live_scrape.py` | Scrape + classify in real time (demo) |
| **Daily sync** | `discovery/daily_sync.py` | GitHub Actions cron entrypoint |
| Demo | `discovery/app.py` | Streamlit 5-tab demo |

## Taxonomy (11 fields)

See `discovery/schemas/taxonomy.json`

Key fields for W2P-30 research:
- `wishlist_related` — is this about save/wishlist behavior?
- `funnel_step` — maps to Slide 1 decomposition (add → revisit → uncertainty → cart → purchase)
- `blocker_type` — size_fit, price_wait, decision_overload, etc.
- `signal_type` — **noise | real | silent** (Preetham-style silent signal hunt)
- `addressable_without_discount` — aligns with project constraint

## How to run (requires Python 3.10+)

```powershell
cd "C:\project myntra"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Add GROQ_API_KEY to .env for LLM classification
```

### Option A — Full pipeline (recommended)

```powershell
python -m discovery.run_pipeline --import-seeds --scrape-count 350
```

### Option B — Offline bootstrap (no API, seeds only)

```powershell
python -m discovery.bootstrap_offline
```

### Launch demo
```powershell
.\.venv\Scripts\python.exe -m streamlit run discovery/app.py
```

### Daily sync (local — same as GitHub Actions)
```powershell
python -m discovery.daily_sync --scrape-count 100
```

### GitHub Actions (daily 10:00 AM IST)
1. Push repo to GitHub
2. Settings → Secrets → Actions → add `GROQ_API_KEY`
3. Workflow: `.github/workflows/discovery-pipeline.yml`
4. Runs automatically daily; manual trigger via **Actions → Run workflow**

See `docs/GITHUB_SCHEDULE.md` for setup details.

## Target corpus (450+ items)

| Source | Target | Method |
|--------|--------|--------|
| Play Store | ~350 | `scrape_play_store.py` |
| App Store | ~10–15 | paste via CSV |
| Reddit | ~15–20 | paste via CSV |
| Forums / Quora | ~40 | paste via CSV |
| Social | ~30 | paste via CSV |
| **Seeds (included)** | **50** | `data/seeds/manual_sources.csv` |

## Outputs

- `data/raw/corpus.json` — deduped unified corpus
- `data/classified/tagged_reviews.json` — classified items
- `data/insights/insights.json` — aggregated themes
- `data/insights/validation_sample.json` — human validation export

## Next steps (Workstream 3)

1. Run full pipeline with Groq API key for LLM classification
2. Scale Play Store scrape to 350+ reviews
3. Paste additional Reddit/forum sources via CSV
4. Hand-label validation sample → compute agreement %
5. Write killer insight + target segment hypothesis for survey/interviews
