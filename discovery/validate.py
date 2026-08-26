"""Random sample validation — export + score human agreement."""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from discovery.config import CLASSIFIED_DIR, INSIGHTS_DIR
from discovery.classify import load_classified


def export_sample(size: int, seed: int) -> None:
    tagged_path = CLASSIFIED_DIR / "tagged_reviews.json"
    items = list(load_classified(tagged_path).values())
    if not items:
        raise SystemExit("No classified items found")

    random.seed(seed)
    sample = random.sample(items, min(size, len(items)))

    export = []
    for row in sample:
        export.append(
            {
                "uid": row["uid"],
                "source": row.get("source"),
                "text": row.get("text"),
                "ai_labels": {
                    "wishlist_related": row.get("wishlist_related"),
                    "blocker_type": row.get("blocker_type"),
                    "signal_type": row.get("signal_type"),
                    "theme_label": row.get("theme_label"),
                    "segment_signal": row.get("segment_signal"),
                },
                "human_labels": {
                    "wishlist_related": None,
                    "blocker_type": None,
                    "signal_type": None,
                    "theme_label": None,
                    "segment_signal": None,
                    "agreement": None,
                },
            }
        )

    out_path = INSIGHTS_DIR / "validation_sample.json"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sample_size": len(export),
        "instructions": "Fill human_labels fields, set agreement=true/false, then run validate.py --score",
        "items": export,
    }
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    print(f"Validation sample exported -> {out_path}")


def score_validation(path: Path) -> None:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    scored = [row for row in payload.get("items", []) if row.get("human_labels", {}).get("agreement") is not None]
    if not scored:
        print("No scored human labels yet.")
        return

    agreements = sum(1 for row in scored if row["human_labels"]["agreement"] is True)
    agreement_pct = round(100.0 * agreements / len(scored), 1)
    result = {
        "scored_items": len(scored),
        "agreements": agreements,
        "agreement_pct": agreement_pct,
    }
    out_path = INSIGHTS_DIR / "validation_score.json"
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    print(f"Validation agreement: {agreement_pct}% ({agreements}/{len(scored)})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validation sample export/score")
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--size", type=int, default=40)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--path", default=str(INSIGHTS_DIR / "validation_sample.json"))
    args = parser.parse_args()

    if args.score:
        score_validation(Path(args.path))
    else:
        export_sample(args.size, args.seed)


if __name__ == "__main__":
    main()
