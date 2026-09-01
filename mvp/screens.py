"""Screen renderers matching Stitch Myntra prototype."""
from __future__ import annotations

import base64
import html
from pathlib import Path
from typing import Any

from mvp.styles import MYNTRA_STYLES

_LOGO_PATH = Path(__file__).resolve().parent / "assets" / "myntra-logo.png"


def _logo_data_uri() -> str:
    if _LOGO_PATH.exists():
        encoded = base64.b64encode(_LOGO_PATH.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Myntra_Logo.png/160px-Myntra_Logo.png"


MYNTRA_LOGO_SRC = _logo_data_uri()


def _esc(value: Any) -> str:
    return html.escape(str(value or ""))


def _header(*, wishlist_active: bool = False, bag_count: int = 0) -> str:
    wishlist_cls = "util-item active" if wishlist_active else "util-item"
    badge = f'<div class="badge">{bag_count}</div>' if bag_count else ""
    return f"""
<header class="header">
  <div style="display:flex;align-items:center;gap:40px;">
    <a class="logo" href="#" aria-label="Myntra home">
      <img src="{MYNTRA_LOGO_SRC}" alt="Myntra"/>
    </a>
    <nav class="nav">
      <a href="#" class="active">Men</a>
      <a href="#">Women</a>
      <a href="#">Kids</a>
      <a href="#">Home</a>
      <a href="#">Beauty</a>
      <a href="#">Studio<sup style="background:var(--primary);color:white;font-size:10px;padding:2px 4px;border-radius:2px;margin-left:4px;">NEW</sup></a>
    </nav>
  </div>
  <div class="search">
    <span class="material-symbols-outlined" style="color:#5b4042;font-size:20px;">search</span>
    <input type="text" placeholder="Search for products, brands and more" readonly/>
  </div>
  <div class="utilities">
    <div class="util-item">
      <div style="width:32px;height:32px;border-radius:50%;background:var(--primary);display:flex;align-items:center;justify-content:center;">
        <span class="material-symbols-outlined" style="color:white;font-size:18px;">person</span>
      </div>
      <span style="margin-top:4px;font-size:12px;">Profile</span>
    </div>
    <div class="{wishlist_cls}" style="position:relative;">
      <span class="material-symbols-outlined icon">favorite</span>
      <span style="margin-top:4px;font-size:12px;">Wishlist</span>
    </div>
    <div class="util-item" style="position:relative;">
      <span class="material-symbols-outlined icon">shopping_bag</span>
      <span style="margin-top:4px;font-size:12px;">Bag</span>
      {badge}
    </div>
  </div>
</header>
<div class="promo-tab">Upto ₹200 OFF</div>
"""


def render_home(categories: list[dict[str, Any]]) -> str:
    tiles = []
    for cat in categories[:6]:
        tiles.append(
            f"""
<a class="category-tile">
  <img src="{_esc(cat.get('image'))}" alt="{_esc(cat.get('name'))}"/>
  <div class="category-info">
    <h3 style="font-size:16px;font-weight:700;margin:0 0 4px;">{_esc(cat.get('name'))}</h3>
    <p style="font-size:20px;font-weight:700;margin:0 0 8px;">{_esc(cat.get('discount'))}</p>
    <span style="font-size:12px;color:var(--primary);text-transform:uppercase;">Shop Now</span>
  </div>
</a>"""
        )
    return f"""
{MYNTRA_STYLES}
<div class="myntra-mvp">
{_header()}
<main class="main">
  <h1 class="shop-title">Shop by Category</h1>
  <div class="category-grid">{''.join(tiles)}</div>
</main>
</div>
"""


def _wishlist_card(item: dict[str, Any], *, in_bag: bool = False, selected: bool = False) -> str:
    locked = not item.get("brief_ready", True)
    card_cls = "product-card locked" if locked else "product-card"
    if selected:
        card_cls += " selected"
    if in_bag:
        cta = """
<button class="btn-in-bag" disabled>
  <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">check_circle</span>
  In Bag
</button>"""
    elif locked:
        cta = '<button class="btn-disabled" disabled>Generating Brief...</button>'
    else:
        cta = ""  # Streamlit button rendered separately

    rating_label = f"{item.get('avg_rating')} | {item.get('review_count')}"
    if int(item.get("review_count") or 0) >= 1000:
        rating_label = f"{item.get('avg_rating')} | {int(item.get('review_count', 0) / 1000)}k+"

    if locked:
        brief_box = f"""
<div class="brief-box locked">
  <span class="material-symbols-outlined" style="color:var(--text-muted);font-size:18px;">schedule</span>
  <p class="brief-ready" style="color:var(--text-muted);">{_esc(item.get('brief_subtitle', 'Brief in 2 days'))}</p>
</div>"""
        lock_overlay = """
<div class="lock-overlay">
  <div class="lock-circle"><span class="material-symbols-outlined" style="font-size:32px;color:var(--text-muted);">lock</span></div>
</div>"""
    else:
        brief_box = f"""
<div class="brief-box">
  <span class="material-symbols-outlined sparkle">auto_awesome</span>
  <div>
    <p class="brief-ready">Brief Ready</p>
    <p class="brief-sub">{_esc(item.get('brief_subtitle'))}</p>
  </div>
</div>"""
        lock_overlay = ""

    return f"""
<div class="{card_cls}">
  <div class="product-img-wrap">
    <img src="{_esc(item.get('image_url'))}" alt="{_esc(item.get('name'))}"/>
    {lock_overlay}
    <div class="rating-badge">
      <span class="rating-pill">{rating_label}
        <span class="material-symbols-outlined" style="font-size:12px;color:var(--primary);font-variation-settings:'FILL' 1;">star</span>
      </span>
    </div>
  </div>
  <div class="card-body">
    <h3 class="brand">{_esc(item.get('brand'))}</h3>
    <p class="product-name">{_esc(item.get('name'))}</p>
    <div class="price-row">
      <span class="price">₹{item.get('price_inr', 0):,}</span>
      <span class="mrp">₹{item.get('mrp_inr', 0):,}</span>
      <span class="off">({item.get('discount_pct')}% OFF)</span>
    </div>
    <p class="saved">{_esc(item.get('saved_label'))}</p>
    {brief_box}
    {cta}
  </div>
</div>"""


def render_wishlist(
    items: list[dict[str, Any]],
    *,
    bag_items: set[str],
    selected_id: str | None = None,
    bag_count: int = 0,
    show_toast: bool = False,
    toast_item: dict[str, Any] | None = None,
    toast_size: str = "M",
) -> str:
    cards = []
    for item in items:
        cards.append(
            _wishlist_card(
                item,
                in_bag=item.get("id") in bag_items,
                selected=item.get("id") == selected_id,
            )
        )

    toast_html = ""
    if show_toast and toast_item:
        toast_html = f"""
<div class="toast">
  <div class="toast-icon"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">check</span></div>
  <div style="font-size:14px;">Added <b>{_esc(toast_item.get('short_name') or toast_item.get('brand'))} (Size {toast_size})</b> to bag</div>
  <div style="width:1px;height:32px;background:#e2e2e2;"></div>
  <span style="color:var(--primary);font-size:14px;font-weight:700;text-transform:uppercase;">View Bag</span>
</div>"""

    return f"""
{MYNTRA_STYLES}
<div class="myntra-mvp">
{_header(wishlist_active=True, bag_count=bag_count)}
{toast_html}
<main class="main">
  <div class="wishlist-header">
    <h1 style="font-size:28px;font-weight:700;margin:0;">Wishlist <span style="color:var(--text-muted);font-size:16px;font-weight:400;">({len(items)} items)</span></h1>
    <div style="display:flex;gap:16px;">
      <button class="filter-btn"><span class="material-symbols-outlined" style="font-size:18px;">filter_list</span> Filter</button>
      <button class="filter-btn"><span class="material-symbols-outlined" style="font-size:18px;">sort</span> Sort</button>
    </div>
  </div>
  <div class="wishlist-grid">{''.join(cards)}</div>
</main>
</div>
"""


def render_brief_modal(
    item: dict[str, Any],
    brief: dict[str, Any],
    user: dict[str, Any],
) -> str:
    size = brief.get("recommended_size", "M")
    rationale = brief.get(
        "size_rationale",
        f"At {user.get('height_cm')} cm and {user.get('weight_kg')} kg you usually wear {size}.",
    )
    bullets = brief.get("fit_summary_bullets") or []
    insights = "".join(
        f'<div class="insight-item"><span class="material-symbols-outlined check">check_circle</span><span>{_esc(b)}</span></div>'
        for b in bullets[:4]
    )
    thumb = item.get("brief_image_url") or item.get("image_url")
    price = item.get("price_inr", 0)

    return f"""
{MYNTRA_STYLES}
<div class="myntra-mvp">
{_header(wishlist_active=True)}
<div class="modal-backdrop">
  <div class="brief-modal">
    <div class="modal-header">
      <div class="modal-title">
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">auto_awesome</span>
        Confidence Brief
      </div>
      <span class="material-symbols-outlined" style="color:#5b4042;cursor:pointer;">close</span>
    </div>
    <div class="product-row">
      <img class="product-thumb" src="{_esc(thumb)}" alt="{_esc(item.get('brand'))}"/>
      <div>
        <h2 style="font-size:20px;font-weight:700;margin:0;">{_esc(item.get('short_name') or item.get('brand'))}</h2>
        <div style="display:flex;align-items:center;gap:8px;margin-top:8px;">
          <span style="font-weight:700;font-size:12px;">₹{price:,}</span>
          <span style="border:1px solid var(--border-light);border-radius:4px;padding:2px 6px;font-size:12px;font-weight:700;">
            {item.get('avg_rating')} <span class="material-symbols-outlined" style="font-size:12px;color:var(--tertiary-container);font-variation-settings:'FILL' 1;vertical-align:middle;">star</span>
            <span style="color:var(--text-muted);font-size:10px;margin-left:4px;">| {item.get('review_count')}</span>
          </span>
        </div>
      </div>
    </div>
    <div class="size-hero">
      <p class="size-label">Recommended size</p>
      <div class="size-circle">{_esc(size)}</div>
      <p style="font-size:14px;max-width:90%;margin:0 auto;line-height:1.5;">{_esc(rationale)}</p>
    </div>
    <div class="insights">
      <h4>Key Insights</h4>
      {insights}
    </div>
    <div class="modal-footer">
      <div class="modal-actions">
        <button class="btn-outline">Still not sure</button>
        <button class="btn-add-bag">Add to Bag — Size {_esc(size)}</button>
      </div>
      <div class="ai-footer">
        <span class="material-symbols-outlined" style="font-size:14px;vertical-align:middle;">smart_toy</span>
        Powered by Myntra AI
      </div>
    </div>
  </div>
</div>
</div>
"""


def render_locked_modal(item: dict[str, Any], similar: list[dict[str, Any]]) -> str:
    progress = item.get("locked_days_progress", 5)
    total = item.get("locked_days_total", 7)
    pct = int(progress / total * 100)
    thumbs = ""
    for sim in similar[:2]:
        thumbs += f"""
<div class="similar-thumb">
  <img src="{_esc(sim.get('image_url'))}" alt="{_esc(sim.get('brand'))}"/>
  <div style="position:absolute;bottom:0;left:0;right:0;padding:8px;background:linear-gradient(transparent,rgba(0,0,0,0.6));">
    <span style="color:white;font-size:10px;font-weight:700;">{_esc(sim.get('brand'))}</span>
  </div>
</div>"""

    return f"""
{MYNTRA_STYLES}
<div class="myntra-mvp">
{_header(wishlist_active=True)}
<div class="modal-backdrop">
  <div class="locked-modal">
    <div style="width:64px;height:64px;border-radius:50%;background:var(--surface-container-low);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">
      <span class="material-symbols-outlined" style="font-size:32px;color:#5b4042;font-variation-settings:'FILL' 1;">lock</span>
    </div>
    <h2 style="font-size:20px;font-weight:700;margin:0 0 8px;">Brief not ready yet</h2>
    <p style="font-size:14px;color:#5b4042;margin:0 0 24px;padding:0 16px;">
      Your personalized style brief is still compiling. Keep saving items to unlock it.
    </p>
    <div class="progress-box">
      <div style="display:flex;justify-content:space-between;padding-left:8px;">
        <span style="font-size:12px;font-weight:700;text-transform:uppercase;">Unlocking Brief</span>
        <span style="font-size:10px;color:var(--primary);font-weight:700;">{progress}/{total} DAYS</span>
      </div>
      <div class="progress-bar" style="margin-left:8px;"><div class="progress-fill" style="width:{pct}%;"></div></div>
      <p style="font-size:10px;color:#5b4042;margin:8px 0 0 8px;">Saved {progress} of {total} consecutive days.</p>
    </div>
    <div style="width:100%;text-align:left;margin-bottom:24px;">
      <span style="font-size:12px;color:#5b4042;text-transform:uppercase;letter-spacing:0.05em;">Keep exploring</span>
      <div class="similar-thumbs">{thumbs}</div>
    </div>
    <button class="btn-primary" style="margin-top:0;">Got it</button>
  </div>
</div>
</div>
"""
