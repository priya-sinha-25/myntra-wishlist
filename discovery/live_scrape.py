"""Live scrape + classify helpers for demo and daily GitHub sync."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from discovery.aggregate import build_insights, insights_to_markdown
from discovery.classify import classify_text, load_classified, save_classified
from discovery.config import CLASSIFIED_DIR, INSIGHTS_DIR, MYNTRA_PLAY_STORE_ID, RAW_DIR
from discovery.corpus import load_corpus, merge_records, save_corpus
from discovery.scrape_play_store import fetch_play_store_reviews

LAST_RUN_PATH = INSIGHTS_DIR / "last_run.json"


def scrape_and_classify_live(count: int = 5, merge_corpus: bool = True) -> dict[str, Any]:
    """Fetch fresh Play Store reviews and classify them in real time."""
    fetched = fetch_play_store_reviews(MYNTRA_PLAY_STORE_ID, count)
    classified_batch: list[dict[str, Any]] = []

    for row in fetched:
        labels = classify_text(row["text"])
        enriched = {
            **row,
            **labels,
            "classified_at": datetime.now(timezone.utc).isoformat(),
            "live_scrape": True,
        }
        classified_batch.append(enriched)

    corpus_total = len(load_corpus())
    tagged_total = len(load_classified(CLASSIFIED_DIR / "tagged_reviews.json"))

    if merge_corpus and classified_batch:
        merged_corpus = merge_records(load_corpus(), fetched)
        save_corpus(merged_corpus)
        corpus_total = len(merged_corpus)

        existing = load_classified(CLASSIFIED_DIR / "tagged_reviews.json")
        for row in classified_batch:
            existing[row["uid"]] = row
        save_classified(list(existing.values()), CLASSIFIED_DIR / "tagged_reviews.json")
        tagged_total = len(existing)

        all_items = list(existing.values())
        insights = build_insights(all_items)
        with (INSIGHTS_DIR / "insights.json").open("w", encoding="utf-8") as handle:
            json.dump(insights, handle, indent=2, ensure_ascii=False)
        with (INSIGHTS_DIR / "insights.md").open("w", encoding="utf-8") as handle:
            handle.write(insights_to_markdown(insights))

    run_meta = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "mode": "live_scrape",
        "fetched": len(fetched),
        "classified": len(classified_batch),
        "corpus_total": corpus_total,
        "tagged_total": tagged_total,
        "source": "play_store",
        "app_id": MYNTRA_PLAY_STORE_ID,
    }
    with LAST_RUN_PATH.open("w", encoding="utf-8") as handle:
        json.dump(run_meta, handle, indent=2)

    return {
        "meta": run_meta,
        "items": classified_batch,
    }


def run_daily_sync(
    scrape_count: int = 100,
    classify_limit: int | None = None,
    import_seeds: bool = False,
) -> dict[str, Any]:
    """Incremental daily sync — used by GitHub Actions cron."""
    from discovery.paste_importer import import_rows, load_input
    from discovery.classify import run_classification
    from discovery.validate import export_sample

    seeds_path = RAW_DIR.parent / "seeds" / "manual_sources.csv"
    seeds_added = 0
    if import_seeds and seeds_path.exists():
        imported = import_rows(load_input(seeds_path), "manual")
        merged = merge_records(load_corpus(), imported)
        save_corpus(merged)
        seeds_added = len(imported)

    fetched = fetch_play_store_reviews(MYNTRA_PLAY_STORE_ID, scrape_count)
    merged_corpus = merge_records(load_corpus(), fetched)
    save_corpus(merged_corpus)

    run_classification(limit=classify_limit, only_unclassified=True)

    tagged_path = CLASSIFIED_DIR / "tagged_reviews.json"
    items = list(load_classified(tagged_path).values())
    insights = build_insights(items)
    with (INSIGHTS_DIR / "insights.json").open("w", encoding="utf-8") as handle:
        json.dump(insights, handle, indent=2, ensure_ascii=False)
    with (INSIGHTS_DIR / "insights.md").open("w", encoding="utf-8") as handle:
        handle.write(insights_to_markdown(insights))

    export_sample(size=min(40, len(items)), seed=42)

    meta = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "mode": "daily_sync",
        "seeds_added": seeds_added,
        "scraped": len(fetched),
        "corpus_total": len(merged_corpus),
        "tagged_total": len(items),
        "classify_limit": classify_limit,
    }
    with LAST_RUN_PATH.open("w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)

    return meta


def load_last_run() -> dict[str, Any] | None:
    if not LAST_RUN_PATH.exists():
        return None
    with LAST_RUN_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)
