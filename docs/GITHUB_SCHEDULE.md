# GitHub Daily Live Scrape Schedule

The discovery engine runs **live Play Store scraping every day at 10:00 AM IST** via GitHub Actions.

## Setup (one time)

1. **Push this project to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "Add Myntra discovery engine"
   git remote add origin https://github.com/YOUR_USERNAME/myntra-wishlist.git
   git push -u origin main
   ```

2. **Add Groq API secret**
   - GitHub repo → **Settings** → **Secrets and variables** → **Actions**
   - **New repository secret**
   - Name: `GROQ_API_KEY`
   - Value: your Groq key from [console.groq.com](https://console.groq.com)

3. **Enable Actions**
   - Repo → **Actions** tab → enable workflows if prompted

## What runs daily

Workflow file: `.github/workflows/discovery-pipeline.yml`

| Step | Action |
|------|--------|
| Cron | `30 4 * * *` UTC = **10:00 AM IST** |
| Scrape | 100 fresh Myntra Play Store reviews (live) |
| Classify | All new/unclassified items via Groq |
| Aggregate | Refresh `data/insights/insights.json` |
| Commit | Push updated `data/` back to repo |

## Manual trigger

Actions → **Discovery Pipeline (Daily)** → **Run workflow**

Optional inputs:
- `scrape_count` — reviews to fetch (default 100)
- `classify_limit` — cap classifications if needed

## Local equivalent

Same logic as GitHub cron:

```powershell
cd "C:\project myntra"
.\.venv\Scripts\python.exe -m discovery.daily_sync --scrape-count 100
```

## Streamlit live demo

Tab 1 → **Scrape & classify live** — same live scrape, runs on your machine instantly (default 5 reviews).

## Files updated each run

- `data/raw/corpus.json`
- `data/classified/tagged_reviews.json`
- `data/insights/insights.json`
- `data/insights/last_run.json` — timestamp of last live sync
