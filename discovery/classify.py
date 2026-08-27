"""LLM classification for corpus items using Groq."""
from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from discovery.config import (
    BATCH_SIZE,
    CLASSIFIED_DIR,
    MAX_RETRIES,
    ROOT,
    refresh_runtime_config,
)
import discovery.config as config
from discovery.corpus import load_corpus

TAXONOMY_PATH = ROOT / "discovery" / "schemas" / "taxonomy.json"

SYSTEM_PROMPT = """You classify public user feedback about Myntra fashion shopping for a growth team's wishlist conversion research (W2P-30).

Return ONLY valid JSON matching this schema:
{
  "wishlist_related": boolean,
  "funnel_step": "add|revisit|pdp|uncertainty|cart|purchase|none",
  "save_reason": "purchase_intent|passive_bookmark|compare|gift|wait_for_sale|unknown|not_applicable",
  "blocker_type": "size_fit|price_wait|quality_doubt|occasion_mismatch|decision_overload|forgot|oos|delivery_returns|app_ux|none",
  "external_validation": "youtube|friends|instagram|competitor|none",
  "segment_signal": "occasion_shopper|deal_hunter|fit_anxious|passive_saver|heavy_wishlister|unknown",
  "intent_strength": 1-5 integer,
  "addressable_without_discount": boolean,
  "signal_type": "noise|real|silent",
  "theme_label": "short_snake_case_theme",
  "evidence_quote": "short verbatim excerpt"
}

Rules:
- signal_type=silent when feedback implies decision/confidence/wishlist failure WITHOUT user explicitly asking for wishlist help
- size_fit, quality_doubt, delivery_returns are often post-purchase but still tag funnel_step accurately
- segment_signal: MUST be one of occasion_shopper|deal_hunter|fit_anxious|passive_saver|heavy_wishlister — avoid "unknown"; infer from blocker and wishlist context
- wishlist_related=true if text mentions wishlist, save for later, shortlisted, heart/save icon behaviour, or indecision on saved items
- Prefer ONE best theme_label; do not invent facts not in the text
- evidence_quote must be copied from the input text
"""


def load_taxonomy() -> dict[str, Any]:
    with TAXONOMY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def extract_json(content: str) -> dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def classify_with_groq(text: str, model: str) -> dict[str, Any]:
    refresh_runtime_config()
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    from groq import Groq

    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify this feedback:\n\n{text}"},
        ],
    )
    raw = response.choices[0].message.content or "{}"
    return extract_json(raw)


def heuristic_classify(text: str) -> dict[str, Any]:
    """Deterministic fallback when no API key — keyword-based baseline."""
    lowered = text.lower()
    wishlist_related = any(
        token in lowered
        for token in ["wishlist", "wish list", "save for later", "saved item", "shortlist", "heart icon"]
    )
    blocker = "none"
    if any(token in lowered for token in ["size", "fit", "fitting", "too tight", "too loose"]):
        blocker = "size_fit"
    elif any(token in lowered for token in ["price", "expensive", "costly", "sale", "discount", "offer"]):
        blocker = "price_wait"
    elif any(token in lowered for token in ["quality", "fake", "duplicate", "material", "fabric"]):
        blocker = "quality_doubt"
    elif any(token in lowered for token in ["delivery", "late", "return", "refund", "exchange"]):
        blocker = "delivery_returns"
    elif any(token in lowered for token in ["crash", "bug", "slow", "login", "otp", "ui"]):
        blocker = "app_ux"

    signal_type = "noise"
    if wishlist_related or blocker != "none":
        signal_type = "real"
    if any(token in lowered for token in ["youtube", "instagram", "friend", "compare", "confused which"]):
        signal_type = "silent"

    return {
        "wishlist_related": wishlist_related,
        "funnel_step": "uncertainty" if blocker == "size_fit" else "none",
        "save_reason": "unknown" if not wishlist_related else "purchase_intent",
        "blocker_type": blocker,
        "external_validation": "youtube" if "youtube" in lowered else ("instagram" if "instagram" in lowered else "none"),
        "segment_signal": "fit_anxious" if blocker == "size_fit" else "unknown",
        "intent_strength": 3,
        "addressable_without_discount": blocker in {"size_fit", "quality_doubt", "decision_overload", "occasion_mismatch"},
        "signal_type": signal_type,
        "theme_label": f"{blocker}_mention" if blocker != "none" else "unrelated",
        "evidence_quote": text[:160],
        "classifier": "heuristic_fallback",
    }


def classify_text(text: str) -> dict[str, Any]:
    refresh_runtime_config()
    if not config.GROQ_API_KEY:
        if config.CLASSIFIER_HEURISTIC_FALLBACK:
            return heuristic_classify(text)
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to .env or Streamlit secrets before running the discovery engine."
        )

    models = [config.GROQ_MODEL_PRIMARY, config.GROQ_MODEL_FALLBACK]
    last_error: Exception | None = None

    for model in models:
        for attempt in range(MAX_RETRIES):
            try:
                result = classify_with_groq(text, model)
                result["classifier"] = "groq"
                result["model_used"] = model
                return result
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(1.5 * (attempt + 1))

    if config.CLASSIFIER_HEURISTIC_FALLBACK:
        result = heuristic_classify(text)
        result["groq_error"] = str(last_error)[:240]
        return result

    raise RuntimeError(f"Groq classification failed after retries: {last_error}")


def load_classified(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    return {row["uid"]: row for row in items}


def save_classified(items: list[dict[str, Any]], path: Path) -> None:
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(items),
        "items": items,
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def run_classification(limit: int | None = None, only_unclassified: bool = True) -> Path:
    corpus = load_corpus()
    output_path = CLASSIFIED_DIR / "tagged_reviews.json"
    existing = load_classified(output_path)

    targets = corpus
    if only_unclassified:
        targets = [row for row in corpus if row["uid"] not in existing]

    if limit is not None:
        targets = targets[:limit]

    print(f"Classifying {len(targets)} items...")
    for index, row in enumerate(targets, start=1):
        classification = classify_text(row["text"])
        enriched = {
            **row,
            **classification,
            "classified_at": datetime.now(timezone.utc).isoformat(),
        }
        existing[row["uid"]] = enriched
        if index % BATCH_SIZE == 0 or index == len(targets):
            save_classified(list(existing.values()), output_path)
            print(f"  saved progress: {index}/{len(targets)}")

    save_classified(list(existing.values()), output_path)
    print(f"Classification complete -> {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify corpus with Groq LLM")
    parser.add_argument("--limit", type=int, default=None, help="Max items to classify this run")
    parser.add_argument("--all", action="store_true", help="Reclassify all items")
    args = parser.parse_args()
    run_classification(limit=args.limit, only_unclassified=not args.all)


if __name__ == "__main__":
    main()
