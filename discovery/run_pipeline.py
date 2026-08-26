"""Run full discovery pipeline: scrape -> classify -> aggregate."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_step(label: str, command: list[str]) -> None:
    print(f"\n=== {label} ===")
    print(">", " ".join(command))
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Step failed: {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Myntra discovery pipeline")
    parser.add_argument("--scrape-count", type=int, default=350)
    parser.add_argument("--classify-limit", type=int, default=None)
    parser.add_argument("--skip-scrape", action="store_true")
    parser.add_argument("--import-seeds", action="store_true", help="Import bundled seed sources")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    py = sys.executable

    if args.import_seeds:
        seeds = root / "data" / "seeds" / "manual_sources.csv"
        if seeds.exists():
            run_step("Import seed sources", [py, "-m", "discovery.paste_importer", str(seeds)])

    if not args.skip_scrape:
        run_step("Scrape Play Store", [py, "-m", "discovery.scrape_play_store", "--count", str(args.scrape_count)])

    classify_cmd = [py, "-m", "discovery.classify"]
    if args.classify_limit is not None:
        classify_cmd.extend(["--limit", str(args.classify_limit)])
    run_step("Classify corpus", classify_cmd)

    run_step("Aggregate insights", [py, "-m", "discovery.aggregate"])
    run_step("Export validation sample", [py, "-m", "discovery.validate"])
    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
