"""Compare-my-saves table for wishlist MVP."""
from __future__ import annotations

import html
from typing import Any


def _esc(value: Any) -> str:
    return html.escape(str(value or ""))


def _format_inr(amount: int) -> str:
    return f"₹{amount:,}"


INTENT_LABELS = {
    "compare": "Comparing options",
    "buy_soon": "Buy soon",
    "occasion": "For an occasion",
    "moodboard": "Mood-boarding",
    "wait_sale": "Waiting for sale",
}


def compare_groups(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group brief-ready items by subcategory when 2+ saves exist."""
    buckets: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if not item.get("brief_ready"):
            continue
        key = str(item.get("subcategory") or item.get("category") or "other")
        buckets.setdefault(key, []).append(item)
    return {key: rows for key, rows in buckets.items() if len(rows) >= 2}


def _fit_signal(item: dict[str, Any], brief: dict[str, Any] | None) -> str:
    if brief:
        badge = brief.get("confidence_badge") or "Good match"
        size = brief.get("recommended_size") or "—"
        return f"{badge} · Size {size}"
    reviews = item.get("reviews") or []
    if reviews:
        return f"{reviews[0].get('size_bought', 'M')} most bought"
    return "See brief"


def _review_snippet(item: dict[str, Any]) -> str:
    reviews = item.get("reviews") or []
    if not reviews:
        return "No review snippet"
    body = reviews[0].get("body", "")
    return body[:90] + ("…" if len(body) > 90 else "")


def _pick_winner(
    group: list[dict[str, Any]],
    brief_cache: dict[str, dict[str, Any]],
) -> str | None:
    if not group:
        return None
    scored: list[tuple[float, str]] = []
    for item in group:
        brief = brief_cache.get(item.get("id", ""), {})
        rating = float(item.get("avg_rating") or 0)
        reviews = int(item.get("review_count") or 0)
        badge = brief.get("confidence_badge", "")
        bonus = {"Strong match": 2, "Good match": 1, "Wider stretch": 0}.get(badge, 0)
        scored.append((rating + bonus + min(reviews / 1000, 1), str(item.get("id"))))
    scored.sort(reverse=True)
    return scored[0][1] if scored else None


def compare_recommendation(
    group: list[dict[str, Any]],
    brief_cache: dict[str, dict[str, Any]],
) -> str:
    winner_id = _pick_winner(group, brief_cache)
    if not winner_id:
        return "Compare fit signals and pick what matches your occasion."
    winner = next((i for i in group if i.get("id") == winner_id), group[0])
    brief = brief_cache.get(winner_id, {})
    size = brief.get("recommended_size", "M")
    return (
        f"<strong>{_esc(winner.get('short_name') or winner.get('brand'))}</strong> leads on fit confidence "
        f"({_esc(brief.get('confidence_badge', 'Good match'))}) — recommended size <strong>{_esc(size)}</strong>."
    )


def render_compare_screen(
    *,
    group_key: str,
    items: list[dict[str, Any]],
    brief_cache: dict[str, dict[str, Any]],
    save_intents: dict[str, str],
    bag_items: list[str],
    screen_href,
) -> str:
    winner_id = _pick_winner(items, brief_cache)
    rows = []
    for item in items:
        item_id = item.get("id", "")
        brief = brief_cache.get(item_id, {})
        is_winner = item_id == winner_id
        row_cls = "compare-row winner" if is_winner else "compare-row"
        intent = INTENT_LABELS.get(save_intents.get(item_id) or item.get("save_intent", ""), "")
        intent_html = f'<span class="intent-chip">{_esc(intent)}</span>' if intent else ""
        in_bag = item_id in bag_items
        size = brief.get("recommended_size", "M")
        if in_bag:
            action = '<span class="compare-in-bag">In Bag</span>'
        elif brief:
            bag_href = screen_href(
                bag_add=item_id,
                bag_size=str(size),
                bag_label=str(item.get("short_name") or item.get("brand") or ""),
                screen="bag",
            )
            action = f'<a href="{bag_href}" class="btn-add-bag compare-add">Add Size {size}</a>'
        else:
            action = f'<a href="?screen=wishlist&amp;open_brief={_esc(item_id)}" class="btn-outline compare-add">View Brief</a>'
        rows.append(
            f"""
<div class="{row_cls}">
  <div class="compare-product">
    <img src="{_esc(item.get('image_url', ''))}" alt="{_esc(item.get('brand'))}" loading="lazy"/>
    <div>
      <h3>{_esc(item.get('brand'))}</h3>
      <p>{_esc(item.get('short_name') or item.get('name'))}</p>
      {intent_html}
    </div>
  </div>
  <div class="compare-metric"><span>Price</span><strong>{_format_inr(int(item.get('price_inr') or 0))}</strong></div>
  <div class="compare-metric"><span>Rating</span><strong>{item.get('avg_rating')}★ · {item.get('review_count')}</strong></div>
  <div class="compare-metric"><span>Fit signal</span><strong>{_esc(_fit_signal(item, brief))}</strong></div>
  <div class="compare-snippet">"{_esc(_review_snippet(item))}"</div>
  <div class="compare-actions">
    <a href="?screen=wishlist&amp;open_brief={_esc(item_id)}" class="compare-link">Full Brief</a>
    {action}
  </div>
</div>"""
        )

    title = group_key.replace("_", " ").title()
    rec = compare_recommendation(items, brief_cache)

    return f"""
<div id="screen-compare" class="screen">
  <main class="main compare-main">
    <div class="wishlist-header">
      <h1 style="font-size:28px;font-weight:700;margin:0;">Compare My Saves</h1>
      <div style="display:flex;gap:16px;">
        <a href="{screen_href('wishlist')}" class="filter-btn">
          <span class="material-symbols-outlined" style="font-size:18px;">favorite</span> Back to Wishlist
        </a>
      </div>
    </div>
    <p class="compare-subtitle">Side-by-side for <strong>{_esc(title)}</strong> — decide without leaving Myntra.</p>
    <div class="compare-rec-box">
      <span class="material-symbols-outlined" style="color:var(--primary);">emoji_events</span>
      <p>{rec}</p>
    </div>
    <div class="compare-table">{"".join(rows)}</div>
    <p class="compare-demo-note">Demo compare — uses review patterns + Confidence Brief signals (no discounts).</p>
  </main>
</div>"""
