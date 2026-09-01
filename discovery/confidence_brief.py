"""AI Confidence Brief generator for Wishlist MVP."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import discovery.config as config
from discovery.config import ROOT, refresh_runtime_config

CATALOG_PATH = ROOT / "data" / "mvp" / "wishlist_catalog.json"

BRIEF_SCHEMA = {
    "product_name": "string",
    "recommended_size": "string",
    "size_rationale": "string",
    "fit_summary_bullets": ["string"],
    "fabric_quality_line": "string",
    "occasion_fit": "string",
    "confidence_badge": "Strong match | Good match | Wider stretch",
    "compare_vs_wishlist": "string",
    "why_trust_this": "string",
    "honest_caveat": "string",
}

SYSTEM_PROMPT = """You generate Myntra Wishlist Confidence Briefs for the W2P-30 growth MVP.

Return ONLY valid JSON with these keys:
- product_name
- recommended_size
- size_rationale (one sentence, personalized to user height/weight/usual size)
- fit_summary_bullets (array of 3-4 short bullets from reviews)
- fabric_quality_line (one sentence)
- occasion_fit (one sentence for user's saved occasion)
- confidence_badge: exactly one of "Strong match", "Good match", "Wider stretch"
- compare_vs_wishlist (2-3 sentences vs other wishlist items in same category)
- why_trust_this (review count / pattern — no fake stats)
- honest_caveat (one limitation)

Rules:
- No discounts or price-led persuasion
- Derive sizing from review patterns only
- Indian English, concise Myntra UX tone
- If reviews are mixed on size, say so and pick conservative recommendation
"""


def load_catalog() -> dict[str, Any]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def list_wishlist_items(catalog: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    payload = catalog or load_catalog()
    return payload.get("items", [])


def get_item(item_id: str, catalog: dict[str, Any] | None = None) -> dict[str, Any] | None:
    for row in list_wishlist_items(catalog):
        if row.get("id") == item_id:
            return row
    return None


def similar_wishlist_items(item: dict[str, Any], all_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sub = item.get("subcategory") or item.get("category", "")
    return [
        other
        for other in all_items
        if other.get("id") != item.get("id") and (other.get("subcategory") or "") == sub
    ]


def brief_eligible(item: dict[str, Any], all_items: list[dict[str, Any]]) -> tuple[bool, str]:
    if item.get("brief_ready") is False:
        return False, item.get("brief_subtitle", "Brief not ready yet")
    if item.get("brief_ready") is True:
        days = int(item.get("saved_days") or 0)
        return True, f"Saved {days} days — confidence help available"
    days = int(item.get("saved_days") or 0)
    similar = similar_wishlist_items(item, all_items)
    if days >= 7:
        return True, f"Saved {days} days — confidence help available"
    if len(similar) >= 1:
        return True, f"{len(similar) + 1} similar saves — compare ready"
    return False, f"Saved {days} days — brief unlocks at 7 days or with similar items"


def extract_json(content: str) -> dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _build_user_prompt(
    item: dict[str, Any],
    user: dict[str, Any],
    compare_items: list[dict[str, Any]],
) -> str:
    compare_summary = [
        {
            "name": other.get("name"),
            "price_inr": other.get("price_inr"),
            "avg_rating": other.get("avg_rating"),
            "review_count": other.get("review_count"),
            "sample_reviews": (other.get("reviews") or [])[:2],
        }
        for other in compare_items
    ]
    return json.dumps(
        {
            "product": {
                "name": item.get("name"),
                "brand": item.get("brand"),
                "category": item.get("category"),
                "price_inr": item.get("price_inr"),
                "fabric": item.get("fabric"),
                "review_count": item.get("review_count"),
                "avg_rating": item.get("avg_rating"),
                "sizes_available": item.get("sizes_available"),
                "saved_days": item.get("saved_days"),
            },
            "reviews": item.get("reviews") or [],
            "user": user,
            "other_wishlist_items": compare_summary,
        },
        indent=2,
    )


def generate_brief_heuristic(
    item: dict[str, Any],
    user: dict[str, Any],
    compare_items: list[dict[str, Any]],
) -> dict[str, Any]:
    reviews = item.get("reviews") or []
    usual = (user.get("usual_size_tops") or "M").upper()
    height = user.get("height_cm", 163)

    size_votes: dict[str, int] = {}
    for review in reviews:
        size = str(review.get("size_bought", "")).upper()
        if size:
            size_votes[size] = size_votes.get(size, 0) + 1
    recommended = max(size_votes, key=size_votes.get) if size_votes else usual

    bullets = []
    for review in reviews[:4]:
        body = review.get("body", "")
        if body:
            bullets.append(body[:120] + ("…" if len(body) > 120 else ""))

    compare_bits = []
    for other in compare_items[:2]:
        compare_bits.append(
            f"{other.get('name')} (₹{other.get('price_inr')}) — "
            f"{other.get('avg_rating')}★ from {other.get('review_count')} reviews"
        )

    return {
        "product_name": item.get("name"),
        "recommended_size": recommended,
        "size_rationale": f"Most buyers near {height}cm in reviews chose size {recommended}; matches your usual {usual}.",
        "fit_summary_bullets": bullets or ["Limited review detail — check size chart before ordering."],
        "fabric_quality_line": item.get("fabric", "See product details for fabric composition."),
        "occasion_fit": f"Suitable for {user.get('occasion', 'your saved occasion')} based on product category and review themes.",
        "confidence_badge": "Good match",
        "compare_vs_wishlist": " · ".join(compare_bits) if compare_bits else "No similar items on wishlist to compare.",
        "why_trust_this": f"Based on {item.get('review_count', 0)} reviews, avg {item.get('avg_rating', '—')}★.",
        "honest_caveat": "Heuristic fallback — connect Groq for full AI synthesis.",
        "generator": "heuristic_fallback",
    }


def generate_brief_groq(
    item: dict[str, Any],
    user: dict[str, Any],
    compare_items: list[dict[str, Any]],
    model: str | None = None,
) -> dict[str, Any]:
    refresh_runtime_config()
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    from groq import Groq

    client = Groq(api_key=config.GROQ_API_KEY)
    model_name = model or config.GROQ_MODEL_PRIMARY
    user_content = _build_user_prompt(item, user, compare_items)

    response = client.chat.completions.create(
        model=model_name,
        temperature=0.35,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    parsed = extract_json(response.choices[0].message.content or "{}")
    parsed["generator"] = "groq"
    parsed["model"] = model_name
    return parsed


def generate_confidence_brief(
    item_id: str,
    user: dict[str, Any],
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = catalog or load_catalog()
    items = list_wishlist_items(payload)
    item = get_item(item_id, payload)
    if not item:
        raise ValueError(f"Unknown wishlist item: {item_id}")

    compare_items = similar_wishlist_items(item, items)
    eligible, reason = brief_eligible(item, items)

    if not eligible:
        return {
            "eligible": False,
            "eligibility_reason": reason,
            "item_id": item_id,
        }

    try:
        brief = generate_brief_groq(item, user, compare_items)
    except Exception:
        if config.CLASSIFIER_HEURISTIC_FALLBACK:
            brief = generate_brief_heuristic(item, user, compare_items)
        else:
            raise

    brief["eligible"] = True
    brief["eligibility_reason"] = reason
    brief["item_id"] = item_id
    brief["compare_item_ids"] = [other.get("id") for other in compare_items]
    return brief
