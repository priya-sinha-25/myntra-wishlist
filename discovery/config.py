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


def _apply_streamlit_secrets() -> None:
    """Load Groq settings from Streamlit Cloud secrets when .env is absent."""
    global GROQ_API_KEY, GROQ_MODEL_PRIMARY, GROQ_MODEL_FALLBACK, CLASSIFIER_HEURISTIC_FALLBACK
    try:
        import streamlit as st

        secrets = st.secrets
        if secrets.get("GROQ_API_KEY"):
            GROQ_API_KEY = str(secrets["GROQ_API_KEY"])
        if secrets.get("GROQ_MODEL_PRIMARY"):
            GROQ_MODEL_PRIMARY = str(secrets["GROQ_MODEL_PRIMARY"])
        if secrets.get("GROQ_MODEL_FALLBACK"):
            GROQ_MODEL_FALLBACK = str(secrets["GROQ_MODEL_FALLBACK"])
        if "CLASSIFIER_HEURISTIC_FALLBACK" in secrets:
            CLASSIFIER_HEURISTIC_FALLBACK = str(secrets["CLASSIFIER_HEURISTIC_FALLBACK"]) == "1"
    except Exception:
        return


def refresh_runtime_config() -> None:
    """Reload secrets and mirror config into os.environ for subprocess pipelines."""
    global GROQ_API_KEY, GROQ_MODEL_PRIMARY, GROQ_MODEL_FALLBACK, CLASSIFIER_HEURISTIC_FALLBACK

    if not GROQ_API_KEY:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    if not GROQ_MODEL_PRIMARY:
        GROQ_MODEL_PRIMARY = os.getenv("GROQ_MODEL_PRIMARY", "openai/gpt-oss-120b")
    if not GROQ_MODEL_FALLBACK:
        GROQ_MODEL_FALLBACK = os.getenv("GROQ_MODEL_FALLBACK", "openai/gpt-oss-20b")

    _apply_streamlit_secrets()

    if GROQ_API_KEY:
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    os.environ["GROQ_MODEL_PRIMARY"] = GROQ_MODEL_PRIMARY
    os.environ["GROQ_MODEL_FALLBACK"] = GROQ_MODEL_FALLBACK
    os.environ["CLASSIFIER_HEURISTIC_FALLBACK"] = "1" if CLASSIFIER_HEURISTIC_FALLBACK else "0"


def subprocess_env() -> dict[str, str]:
    """Environment for discovery subprocesses (classify, scrape, aggregate)."""
    refresh_runtime_config()
    return os.environ.copy()


_apply_streamlit_secrets()
refresh_runtime_config()

BATCH_SIZE = int(os.getenv("CLASSIFY_BATCH_SIZE", "5"))
MAX_RETRIES = 3

for directory in (RAW_DIR, CLASSIFIED_DIR, INSIGHTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
