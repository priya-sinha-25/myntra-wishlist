"""Bootstrap corpus + heuristic classification without network/API."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from discovery.aggregate import build_insights, insights_to_markdown
from discovery.classify import classify_text
from discovery.config import CLASSIFIED_DIR, INSIGHTS_DIR, RAW_DIR, ROOT
from discovery.corpus import merge_records, normalize_record, save_corpus
from discovery.validate import export_sample


def load_seeds() -> list[dict]:
    seed_path = ROOT / "data" / "seeds" / "manual_sources.csv"
    rows = []
    with seed_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                normalize_record(
                    source=row["source"],
                    text=row["text"],
                    url=row.get("url", ""),
                    rating=int(row["rating"]) if row.get("rating") else None,
                    date=row.get("date"),
                )
            )
    return rows


def main() -> None:
    seeds = load_seeds()
    save_corpus(seeds)

    classified = []
    for row in seeds:
        labels = classify_text(row["text"])
        classified.append(
            {
                **row,
                **labels,
                "classified_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    tagged_path = CLASSIFIED_DIR / "tagged_reviews.json"
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(classified),
        "items": classified,
    }
    with tagged_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)

    insights = build_insights(classified)
    with (INSIGHTS_DIR / "insights.json").open("w", encoding="utf-8") as handle:
        json.dump(insights, handle, indent=2, ensure_ascii=False)
    with (INSIGHTS_DIR / "insights.md").open("w", encoding="utf-8") as handle:
        handle.write(insights_to_markdown(insights))

    export_sample(size=min(40, len(classified)), seed=42)
    print(f"Bootstrapped {len(classified)} items from seeds")
    print(f"Corpus -> {RAW_DIR / 'corpus.json'}")
    print(f"Tagged -> {tagged_path}")
    print(f"Insights -> {INSIGHTS_DIR / 'insights.json'}")


if __name__ == "__main__":
    main()
