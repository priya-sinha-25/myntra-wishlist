"""CLI entrypoint for daily GitHub Actions sync."""
from __future__ import annotations

import argparse
import json

from discovery.live_scrape import run_daily_sync


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily discovery sync (scrape + classify + aggregate)")
    parser.add_argument("--scrape-count", type=int, default=100, help="Fresh Play Store reviews per run")
    parser.add_argument("--classify-limit", type=int, default=None, help="Cap new classifications per run")
    parser.add_argument("--import-seeds", action="store_true", help="Re-import manual seed CSV")
    args = parser.parse_args()

    meta = run_daily_sync(
        scrape_count=args.scrape_count,
        classify_limit=args.classify_limit,
        import_seeds=args.import_seeds,
    )
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
