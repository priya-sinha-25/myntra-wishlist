"""Unified review record helpers."""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from discovery.config import RAW_DIR


def make_uid(source: str, text: str, url: str = "") -> str:
    payload = f"{source}|{url}|{text.strip()[:500]}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def normalize_record(
    *,
    source: str,
    text: str,
    url: str = "",
    rating: int | None = None,
    date: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cleaned = " ".join(text.split())
    if len(cleaned) < 20:
        raise ValueError("Review text too short after normalization")

    return {
        "uid": make_uid(source, cleaned, url),
        "source": source,
        "text": cleaned,
        "url": url,
        "rating": rating,
        "date": date or datetime.now(timezone.utc).date().isoformat(),
        "metadata": metadata or {},
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def load_corpus(path: Path | None = None) -> list[dict[str, Any]]:
    corpus_path = path or (RAW_DIR / "corpus.json")
    if not corpus_path.exists():
        return []
    with corpus_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else data.get("items", [])


def save_corpus(items: list[dict[str, Any]], path: Path | None = None) -> Path:
    corpus_path = path or (RAW_DIR / "corpus.json")
    deduped: dict[str, dict[str, Any]] = {}
    for item in items:
        deduped[item["uid"]] = item
    ordered = sorted(deduped.values(), key=lambda row: row.get("date", ""), reverse=True)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(ordered),
        "items": ordered,
    }
    with corpus_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    return corpus_path


def merge_records(existing: list[dict[str, Any]], new_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = {row["uid"]: row for row in existing}
    for item in new_items:
        merged[item["uid"]] = item
    return list(merged.values())
