"""Aggregate classified reviews into insights.json and insights.md."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from discovery.config import CLASSIFIED_DIR, INSIGHTS_DIR

SEGMENT_LABELS = {
    "fit_anxious": "Fit-anxious shoppers",
    "occasion_shopper": "Occasion shoppers",
    "deal_hunter": "Deal hunters",
    "heavy_wishlister": "Heavy wishlisters",
    "passive_saver": "Passive savers",
    "post_purchase_friction": "Post-purchase friction",
    "app_experience": "App experience issues",
}

BLOCKER_LABELS = {
    "size_fit": "Size & fit uncertainty",
    "price_wait": "Price / sale timing",
    "quality_doubt": "Quality doubt",
    "occasion_mismatch": "Occasion mismatch",
    "decision_overload": "Decision overload",
    "forgot": "Forgot / recall failure",
    "oos": "Out of stock",
    "delivery_returns": "Delivery & returns",
    "app_ux": "App UX issues",
}


def load_tagged(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("items", [])


def pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(100.0 * numerator / denominator, 1)


def infer_segment(row: dict[str, Any]) -> str | None:
    """Infer a meaningful segment when classifier returns unknown."""
    seg = row.get("segment_signal", "unknown")
    if seg and seg != "unknown":
        return seg

    blocker = row.get("blocker_type", "none")
    wishlist = bool(row.get("wishlist_related"))
    external = row.get("external_validation", "none")

    if wishlist:
        if blocker == "size_fit" or external in {"youtube", "instagram", "friends"}:
            return "fit_anxious"
        if blocker == "occasion_mismatch":
            return "occasion_shopper"
        if blocker == "price_wait":
            return "deal_hunter"
        if blocker in {"decision_overload", "forgot"}:
            return "heavy_wishlister"
        return "passive_saver"

    if blocker == "size_fit":
        return "fit_anxious"
    if blocker == "price_wait":
        return "deal_hunter"
    if blocker in {"delivery_returns", "quality_doubt"}:
        return "post_purchase_friction"
    if blocker == "app_ux":
        return "app_experience"

    return None


def build_killer_insight(
    total: int,
    wishlist_count: int,
    wishlist_pct: float,
    silent_count: int,
    blocker_ranking: list[tuple[str, int]],
    wishlist_blocker_ranking: list[tuple[str, int]],
    external_count: int,
) -> str:
    loud_top = blocker_ranking[0] if blocker_ranking else ("none", 0)
    loud_label = BLOCKER_LABELS.get(loud_top[0], loud_top[0].replace("_", " "))

    wl_blocker_line = ""
    if wishlist_blocker_ranking:
        wb = wishlist_blocker_ranking[0]
        wl_label = BLOCKER_LABELS.get(wb[0], wb[0].replace("_", " "))
        wl_blocker_line = (
            f" Among wishlist-tagged reviews, **{wl_label}** leads ({wb[1]} mentions)."
        )

    return (
        f"Across **{total}** classified reviews, only **{wishlist_pct}%** ({wishlist_count}) "
        f"explicitly mention wishlist behaviour — yet **{silent_count}** show **silent decision gaps** "
        f"(users leave to validate on YouTube, Instagram, or via friends without asking Myntra for help). "
        f"Loud Play Store complaints centre on **{loud_label}** ({loud_top[1]} mentions); "
        f"wishlist conversion friction is largely **unvoiced**."
        f"{wl_blocker_line} "
        f"**{external_count}** reviews reference external validation before buying saved items."
    )


def pick_top_quotes(items: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    """Prioritise wishlist-related, silent, and high-intent quotes from the corpus."""
    def score(row: dict[str, Any]) -> tuple[int, int, int]:
        wishlist = 1 if row.get("wishlist_related") else 0
        silent = 1 if row.get("signal_type") == "silent" else 0
        intent = int(row.get("intent_strength") or 0)
        return (wishlist, silent, intent)

    candidates = [
        row for row in items
        if row.get("signal_type") in {"real", "silent"}
        and row.get("blocker_type") not in {None, "none"}
        and (row.get("evidence_quote") or row.get("text", "")).strip()
    ]
    ranked = sorted(candidates, key=score, reverse=True)

    quotes = []
    seen_text: set[str] = set()
    for row in ranked:
        text = (row.get("evidence_quote") or row.get("text", "")).strip()
        key = text[:80].lower()
        if key in seen_text:
            continue
        seen_text.add(key)
        quotes.append(
            {
                "source": row.get("source"),
                "theme": row.get("theme_label"),
                "signal_type": row.get("signal_type"),
                "blocker": row.get("blocker_type"),
                "segment": infer_segment(row) or row.get("segment_signal"),
                "quote": text[:220],
            }
        )
        if len(quotes) >= limit:
            break
    return quotes


def build_insights(items: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(items)
    wishlist_items = [row for row in items if row.get("wishlist_related")]
    real_items = [row for row in items if row.get("signal_type") == "real"]
    silent_items = [row for row in items if row.get("signal_type") == "silent"]
    noise_items = [row for row in items if row.get("signal_type") == "noise"]

    blocker_counts = Counter(
        row.get("blocker_type", "none")
        for row in items
        if row.get("blocker_type") not in {None, "none"}
    )
    wishlist_blocker_counts = Counter(
        row.get("blocker_type", "none")
        for row in wishlist_items
        if row.get("blocker_type") not in {None, "none"}
    )

    inferred_segments = Counter()
    for row in items:
        seg = infer_segment(row)
        if seg:
            inferred_segments[seg] += 1

    wishlist_segment_counts = Counter()
    for row in wishlist_items:
        seg = infer_segment(row)
        if seg:
            wishlist_segment_counts[seg] += 1

    funnel_counts = Counter(row.get("funnel_step", "none") for row in items)
    source_counts = Counter(row.get("source", "unknown") for row in items)
    signal_counts = Counter(row.get("signal_type", "unknown") for row in items)

    external_validation_count = sum(
        1 for row in items if row.get("external_validation") not in {None, "none", ""}
    )

    crosstab: dict[str, Counter] = defaultdict(Counter)
    for row in wishlist_items:
        seg = infer_segment(row) or "passive_saver"
        blocker = row.get("blocker_type", "none")
        if blocker != "none":
            crosstab[seg][blocker] += 1

    addressable = [row for row in items if row.get("addressable_without_discount")]
    blocker_ranking = blocker_counts.most_common()
    wishlist_blocker_ranking = wishlist_blocker_counts.most_common()

    segment_distribution = [
        [seg, count, SEGMENT_LABELS.get(seg, seg.replace("_", " ").title())]
        for seg, count in inferred_segments.most_common()
    ]

    wishlist_segment_distribution = [
        [seg, count, SEGMENT_LABELS.get(seg, seg.replace("_", " ").title())]
        for seg, count in wishlist_segment_counts.most_common()
    ]

    summary = {
        "total_items": total,
        "wishlist_related_count": len(wishlist_items),
        "wishlist_related_pct": pct(len(wishlist_items), total),
        "real_signal_count": len(real_items),
        "silent_signal_count": len(silent_items),
        "noise_count": len(noise_items),
        "addressable_without_discount_count": len(addressable),
        "addressable_without_discount_pct": pct(len(addressable), total),
        "external_validation_count": external_validation_count,
    }

    killer_insight = build_killer_insight(
        total=total,
        wishlist_count=len(wishlist_items),
        wishlist_pct=summary["wishlist_related_pct"],
        silent_count=len(silent_items),
        blocker_ranking=blocker_ranking,
        wishlist_blocker_ranking=wishlist_blocker_ranking,
        external_count=external_validation_count,
    )

    top_quotes = pick_top_quotes(items)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "source_breakdown": dict(source_counts),
        "signal_breakdown": dict(signal_counts),
        "blocker_ranking": blocker_ranking,
        "wishlist_blocker_ranking": wishlist_blocker_ranking,
        "segment_distribution": segment_distribution,
        "wishlist_segment_distribution": wishlist_segment_distribution,
        "funnel_step_distribution": funnel_counts.most_common(),
        "segment_x_blocker": {seg: dict(blockers) for seg, blockers in crosstab.items()},
        "top_quotes": top_quotes,
        "killer_insight_hypothesis": killer_insight,
        "key_findings": [
            f"Only {summary['wishlist_related_pct']}% of reviews explicitly mention wishlist — decision failure is mostly silent.",
            f"Top loud blocker: {BLOCKER_LABELS.get(blocker_ranking[0][0], blocker_ranking[0][0])} ({blocker_ranking[0][1]} mentions)" if blocker_ranking else "",
            f"Silent signals detected: {len(silent_items)} reviews imply decision gaps without asking for help.",
            f"External validation (YouTube/friends/Instagram): {external_validation_count} mentions.",
            (
                f"Among wishlist-tagged reviews, top blocker is "
                f"{BLOCKER_LABELS.get(wishlist_blocker_ranking[0][0], wishlist_blocker_ranking[0][0])} "
                f"({wishlist_blocker_ranking[0][1]} mentions)."
                if wishlist_blocker_ranking
                else "Wishlist-tagged subset is small — seeds + forums carry richer wishlist signal."
            ),
        ],
    }


def insights_to_markdown(insights: dict[str, Any]) -> str:
    summary = insights["summary"]
    lines = [
        "# Myntra Discovery Insights",
        "",
        f"Generated: {insights['generated_at']}",
        "",
        "## Summary",
        f"- Total items: **{summary['total_items']}**",
        f"- Wishlist-related: **{summary['wishlist_related_count']}** ({summary['wishlist_related_pct']}%)",
        f"- Silent signals: **{summary['silent_signal_count']}**",
        f"- External validation mentions: **{summary.get('external_validation_count', 0)}**",
        f"- Addressable without discount: **{summary['addressable_without_discount_count']}** ({summary['addressable_without_discount_pct']}%)",
        "",
        "## Blocker ranking (full corpus)",
    ]
    for blocker, count in insights["blocker_ranking"]:
        label = BLOCKER_LABELS.get(blocker, blocker)
        lines.append(f"- {label}: {count}")

    lines.extend(["", "## Blocker ranking (wishlist-tagged only)", ""])
    for blocker, count in insights.get("wishlist_blocker_ranking", []):
        label = BLOCKER_LABELS.get(blocker, blocker)
        lines.append(f"- {label}: {count}")

    lines.extend(["", "## Segment distribution (inferred)", ""])
    for seg, count, label in insights.get("segment_distribution", []):
        lines.append(f"- {label}: {count}")

    lines.extend(["", "## Top quotes", ""])
    for quote in insights["top_quotes"]:
        lines.append(
            f"- **{quote['source']}** ({quote.get('blocker', quote.get('theme'))}, {quote['signal_type']}): "
            f"\"{quote['quote']}\""
        )

    lines.extend(["", "## Killer insight", "", insights["killer_insight_hypothesis"], ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate tagged reviews into insights")
    parser.add_argument("--input", default=str(CLASSIFIED_DIR / "tagged_reviews.json"))
    args = parser.parse_args()

    items = load_tagged(Path(args.input))
    if not items:
        raise SystemExit("No classified items found. Run classify.py first.")

    insights = build_insights(items)
    json_path = INSIGHTS_DIR / "insights.json"
    md_path = INSIGHTS_DIR / "insights.md"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(insights, handle, indent=2, ensure_ascii=False)

    with md_path.open("w", encoding="utf-8") as handle:
        handle.write(insights_to_markdown(insights))

    print(f"Insights written -> {json_path}")
    print(f"Markdown summary -> {md_path}")


if __name__ == "__main__":
    main()
