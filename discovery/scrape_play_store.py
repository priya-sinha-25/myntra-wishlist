"""Scrape Myntra reviews from Google Play Store (India)."""
from __future__ import annotations

import argparse
import json
import time
from typing import Any

from discovery.config import MYNTRA_PLAY_STORE_ID, RAW_DIR
from discovery.corpus import load_corpus, merge_records, normalize_record, save_corpus


def fetch_play_store_reviews(app_id: str, count: int, lang: str = "en", country: str = "in") -> list[dict[str, Any]]:
    try:
        from google_play_scraper import Sort, reviews
    except ImportError as exc:
        raise SystemExit("Install google-play-scraper: pip install google-play-scraper") from exc

    collected: list[dict[str, Any]] = []
    token = None

    while len(collected) < count:
        batch_size = min(200, count - len(collected))
        batch = None
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                batch, token = reviews(
                    app_id,
                    lang=lang,
                    country=country,
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=token,
                )
                last_error = None
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(2 * (attempt + 1))
        if last_error is not None:
            raise RuntimeError(f"Play Store scrape failed after retries: {last_error}") from last_error
        if not batch:
            break
        for review in batch:
            text = review.get("content") or ""
            if not text.strip():
                continue
            try:
                collected.append(
                    normalize_record(
                        source="play_store",
                        text=text,
                        url=f"https://play.google.com/store/apps/details?id={app_id}&reviewId={review.get('reviewId', '')}",
                        rating=review.get("score"),
                        date=str(review.get("at").date()) if review.get("at") else None,
                        metadata={
                            "review_id": review.get("reviewId"),
                            "thumbs_up": review.get("thumbsUpCount"),
                            "user_name": review.get("userName"),
                        },
                    )
                )
            except ValueError:
                continue
        if token is None:
            break

    return collected[:count]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Myntra Play Store reviews")
    parser.add_argument("--count", type=int, default=350, help="Number of reviews to fetch")
    parser.add_argument("--app-id", default=MYNTRA_PLAY_STORE_ID)
    parser.add_argument("--output", default=str(RAW_DIR / "play_store_batch.json"))
    args = parser.parse_args()

    print(f"Fetching up to {args.count} reviews for {args.app_id}...")
    fresh = fetch_play_store_reviews(args.app_id, args.count)
    print(f"Fetched {len(fresh)} reviews")

    batch_path = RAW_DIR / "play_store_batch.json"
    with batch_path.open("w", encoding="utf-8") as handle:
        json.dump(fresh, handle, indent=2, ensure_ascii=False)

    existing = load_corpus()
    merged = merge_records(existing, fresh)
    corpus_path = save_corpus(merged)
    print(f"Corpus updated: {len(merged)} total items -> {corpus_path}")


if __name__ == "__main__":
    main()
