"""Import hand-collected reviews from CSV or JSON."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from discovery.config import RAW_DIR
from discovery.corpus import load_corpus, merge_records, normalize_record, save_corpus


def load_input(path: Path) -> list[dict]:
    if path.suffix.lower() == ".csv":
        rows = []
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(row)
        return rows

    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return payload
    return payload.get("items", [])


def import_rows(rows: list[dict], default_source: str) -> list[dict]:
    imported = []
    for row in rows:
        text = row.get("text") or row.get("review") or row.get("content") or ""
        source = row.get("source") or default_source
        url = row.get("url") or row.get("link") or ""
        rating = row.get("rating")
        try:
            rating_val = int(rating) if rating not in (None, "") else None
        except ValueError:
            rating_val = None
        try:
            imported.append(
                normalize_record(
                    source=source,
                    text=text,
                    url=url,
                    rating=rating_val,
                    date=row.get("date"),
                    metadata={k: v for k, v in row.items() if k not in {"text", "review", "content", "source", "url", "link", "rating", "date"}},
                )
            )
        except ValueError:
            continue
    return imported


def main() -> None:
    parser = argparse.ArgumentParser(description="Import pasted reviews into corpus")
    parser.add_argument("input", type=Path, help="CSV or JSON file")
    parser.add_argument("--source", default="manual", help="Default source label if missing in file")
    args = parser.parse_args()

    rows = load_input(args.input)
    imported = import_rows(rows, args.source)
    print(f"Imported {len(imported)} valid rows from {args.input}")

    existing = load_corpus()
    merged = merge_records(existing, imported)
    corpus_path = save_corpus(merged)
    print(f"Corpus updated: {len(merged)} total items -> {corpus_path}")


if __name__ == "__main__":
    main()
