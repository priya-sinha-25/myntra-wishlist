"""Discovery engine configuration."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass
DISCOVERY_DIR = ROOT / "discovery"
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLASSIFIED_DIR = DATA_DIR / "classified"
INSIGHTS_DIR = DATA_DIR / "insights"

MYNTRA_PLAY_STORE_ID = "com.myntra.android"
MYNTRA_APP_STORE_ID = "907394059"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_PRIMARY = os.getenv("GROQ_MODEL_PRIMARY", "openai/gpt-oss-120b")
GROQ_MODEL_FALLBACK = os.getenv("GROQ_MODEL_FALLBACK", "openai/gpt-oss-20b")
CLASSIFIER_HEURISTIC_FALLBACK = os.getenv("CLASSIFIER_HEURISTIC_FALLBACK", "1") == "1"

BATCH_SIZE = int(os.getenv("CLASSIFY_BATCH_SIZE", "5"))
MAX_RETRIES = 3

for directory in (RAW_DIR, CLASSIFIED_DIR, INSIGHTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
