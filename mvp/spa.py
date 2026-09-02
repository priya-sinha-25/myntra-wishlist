"""Single-page interactive Myntra MVP — all clicks work inside the UI."""
from __future__ import annotations

import base64
import html
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode


from mvp.compare import INTENT_LABELS, compare_groups, render_compare_screen
from mvp.styles import MYNTRA_STYLES

_LOGO_PATH = Path(__file__).resolve().parent / "assets" / "myntra-logo.png"


def _logo_data_uri() -> str:
    if _LOGO_PATH.exists():
        encoded = base64.b64encode(_LOGO_PATH.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Myntra_Logo.png/160px-Myntra_Logo.png"


MYNTRA_LOGO_SRC = _logo_data_uri()
MVP_MODAL_NONE = "mvp-modal-none"


def _esc(value: Any) -> str:
    return html.escape(str(value or ""))


def _mvp_href(**params: str) -> str:
    clean = {k: str(v) for k, v in params.items() if v is not None and str(v) != ""}
    return "?" + urlencode(clean)


def _bag_action_link(
    *,
    item_id: str,
    size: str = "",
    label: str = "",
    button_text: str,
    button_class: str = "btn-add-bag",
) -> str:
    """Same-page query-param link — works with st.html (not sandboxed iframe)."""
    href = _mvp_href(bag_add=item_id, bag_size=size, bag_label=label, screen="bag")
    return f'<a href="{href}" class="{button_class}">{_esc(button_text)}</a>'


def _bag_remove_link(item_id: str) -> str:
    href = _mvp_href(bag_remove=item_id, screen="bag")
    return (
        f'<a href="{href}" class="bag-remove" aria-label="Remove">'
        f'<span class="material-symbols-outlined">close</span>'
        f"</a>"
    )


def _img(src: str, *, alt: str = "", cls: str = "", seed: str = "myntra") -> str:
    alt_attr = f' alt="{_esc(alt)}"' if alt else ""
    cls_attr = f' class="{cls}"' if cls else ""
    fallback = f"https://picsum.photos/seed/{_esc(seed)}/400/500"
    return (
        f'<img src="{_esc(src)}"{alt_attr}{cls_attr} '
        f'loading="lazy" '
        f"onerror=\"this.onerror=null;this.src='{fallback}';\"/>"
    )


def _format_inr(amount: int) -> str:
    return f"₹{amount:,}"


def _bag_rows_html(
    items_by_id: dict[str, dict[str, Any]],
    bag_items: list[str],
    bag_details: dict[str, dict[str, Any]],
) -> tuple[str, int]:
    rows: list[str] = []
    subtotal = 0
    for item_id in bag_items:
        item = items_by_id.get(item_id)
        if not item:
            continue
        detail = bag_details.get(item_id, {})
        size = detail.get("size", "M")
        subtotal += int(item.get("price_inr") or 0)
        rows.append(
            f"""
<div class="bag-item-row">
  {_img(item.get("image_url", ""), alt=item.get("brand", ""), seed=item_id)}
  <div class="bag-item-info">
    <h4>{_esc(item.get("brand"))}</h4>
    <p>{_esc(item.get("name"))}</p>
    <span class="bag-item-size">Size: {_esc(size)}</span>
    <span class="bag-item-price">{_format_inr(int(item.get("price_inr") or 0))}</span>
  </div>
  {_bag_remove_link(item_id)}
</div>"""
        )
    return "".join(rows), subtotal


def _nav_radios(initial_screen: str) -> str:
    radios = []
    for name in ("home", "wishlist", "bag", "compare"):
        checked = " checked" if initial_screen == name else ""
        radios.append(
            f'<input type="radio" name="mvp-screen" id="mvp-nav-{name}" '
            f'class="mvp-nav-radio"{checked} aria-hidden="true"/>'
        )
    return "\n".join(radios)


def _screen_href(screen: str) -> str:
    return _mvp_href(screen=screen)


def _header(*, bag_count: int = 0) -> str:
    badge_style = "" if bag_count else ' style="display:none;"'
    badge = f'<div class="badge" id="bag-badge"{badge_style}>{bag_count or 0}</div>'
    return f"""
<header class="header">
  <div style="display:flex;align-items:center;gap:40px;">
    <a href="{_screen_href("home")}" class="logo util-item" aria-label="Myntra home">
      <img src="{MYNTRA_LOGO_SRC}" alt="Myntra"/>
    </a>
    <nav class="nav">
      <a href="#" class="active">Men</a>
      <a href="#">Women</a>
      <a href="#">Kids</a>
      <a href="{_screen_href("home")}" class="nav-home-link">Home</a>
      <a href="#">Beauty</a>
      <a href="#">Studio<sup style="background:var(--primary);color:white;font-size:10px;padding:2px 4px;border-radius:2px;margin-left:4px;">NEW</sup></a>
    </nav>
  </div>
  <div class="search">
    <span class="material-symbols-outlined search-icon">search</span>
    <input type="text" placeholder="Search for products, brands and more" readonly/>
  </div>
  <div class="utilities">
    <div class="util-item util-item-static" aria-hidden="true">
      <div class="profile-avatar">
        <span class="material-symbols-outlined">person</span>
      </div>
      <span class="util-label">Profile</span>
    </div>
    <a href="{_screen_href("home")}" class="util-item" id="nav-home">
      <span class="material-symbols-outlined icon">home</span>
      <span class="util-label">Home</span>
    </a>
    <a href="{_screen_href("wishlist")}" class="util-item" id="nav-wishlist">
      <span class="material-symbols-outlined icon">favorite</span>
      <span class="util-label">Wishlist</span>
    </a>
    <a href="{_screen_href("bag")}" class="util-item" id="nav-bag">
      <span class="material-symbols-outlined icon">shopping_bag</span>
      <span class="util-label">Bag</span>
      {badge}
    </a>
  </div>
</header>
<div class="promo-tab">Upto ₹200 OFF</div>
"""


def _intent_chip_row(item_id: str, current_intent: str) -> str:
    label = INTENT_LABELS.get(current_intent, "Set intent")
    options = []
    for key, text in INTENT_LABELS.items():
        active = " active" if key == current_intent else ""
        href = _mvp_href(set_intent=item_id, intent=key, screen="wishlist")
        options.append(f'<a href="{href}" class="intent-option{active}">{_esc(text)}</a>')
    return f"""
<div class="intent-row">
  <span class="intent-chip">{_esc(label)}</span>
  <details class="intent-picker">
    <summary class="intent-edit">Edit</summary>
    <div class="intent-menu">{"".join(options)}</div>
  </details>
</div>"""


def _compare_cta(item: dict[str, Any], groups: dict[str, list[dict[str, Any]]]) -> str:
    sub = str(item.get("subcategory") or "")
    group = groups.get(sub, [])
    if len(group) < 2 or not item.get("brief_ready"):
        return ""
    title = sub.replace("_", " ").title()
    href = _mvp_href(screen="compare", compare_group=sub)
    return (
        f'<a href="{href}" class="compare-card-cta">'
        f'<span class="material-symbols-outlined" style="font-size:16px;">compare_arrows</span>'
        f" Compare {len(group)} {title} saves</a>"
    )


def _journey_strip() -> str:
    return """
<div class="conversion-journey">
  <p class="journey-label">How this MVP lifts W2P-30</p>
  <div class="journey-steps">
    <div class="journey-step"><span class="material-symbols-outlined">favorite</span><strong>Save</strong><span>Build intent</span></div>
    <span class="journey-arrow material-symbols-outlined">arrow_forward</span>
    <div class="journey-step"><span class="material-symbols-outlined">auto_awesome</span><strong>Brief</strong><span>Fit confidence</span></div>
    <span class="journey-arrow material-symbols-outlined">arrow_forward</span>
    <div class="journey-step"><span class="material-symbols-outlined">compare_arrows</span><strong>Compare</strong><span>Pick winner</span></div>
    <span class="journey-arrow material-symbols-outlined">arrow_forward</span>
    <div class="journey-step"><span class="material-symbols-outlined">notifications</span><strong>Revisit</strong><span>Return nudge</span></div>
    <span class="journey-arrow material-symbols-outlined">arrow_forward</span>
    <div class="journey-step"><span class="material-symbols-outlined">shopping_bag</span><strong>Bag</strong><span>Purchase</span></div>
  </div>
</div>"""


def _revisit_banner(ready_count: int, *, dismissed: bool) -> str:
    if dismissed or ready_count < 1:
        return ""
    plural = "s are" if ready_count != 1 else " is"
    dismiss_href = _mvp_href(dismiss_revisit="1", screen="wishlist")
    wishlist_href = _screen_href("wishlist")
    return f"""
<div class="revisit-banner">
  <div class="revisit-banner-body">
    <span class="material-symbols-outlined revisit-icon">notifications_active</span>
    <div>
      <p class="revisit-title">{ready_count} Confidence Brief{plural} ready</p>
      <p class="revisit-sub">Revisit your saves — compare similar items before prices shift.</p>
    </div>
  </div>
  <div class="revisit-actions">
    <a href="{wishlist_href}" class="revisit-cta">View briefs</a>
    <a href="{dismiss_href}" class="revisit-dismiss" aria-label="Dismiss">Dismiss</a>
  </div>
</div>"""


def _share_toast_html(*, visible: bool) -> str:
    if not visible:
        return ""
    return """
<div class="share-toast">
  <span class="material-symbols-outlined" style="color:var(--tertiary-container);">share</span>
  <p>Brief link ready — share with a friend for a second opinion (demo).</p>
</div>"""


def _wishlist_card(
    item: dict[str, Any],
    *,
    in_bag: bool = False,
    save_intent: str = "",
    compare_groups_map: dict[str, list[dict[str, Any]]] | None = None,
) -> str:
    compare_groups_map = compare_groups_map or {}
    item_id = item.get("id", "")
    locked = not item.get("brief_ready", True)

    review_count = int(item.get("review_count") or 0)
    rating_label = f"{item.get('avg_rating')} | {review_count}"
    if review_count >= 1000:
        rating_label = f"{item.get('avg_rating')} | {review_count // 1000}k+"

    card_cls = "product-card locked" if locked else "product-card"
    if in_bag:
        cta = """
<button class="btn-in-bag" type="button" disabled>
  <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">check_circle</span>
  In Bag
</button>"""
    elif locked:
        cta = f'<label for="modal-locked-{_esc(item_id)}" class="btn-disabled">Why is this locked?</label>'
    else:
        cta = f'<label for="modal-brief-{_esc(item_id)}" class="btn-primary">Get Confidence Brief</label>'

    if locked:
        unlock_hint = _esc(item.get("locked_unlock_hint") or item.get("brief_subtitle", "Brief not ready"))
        brief_box = f"""
<label for="modal-locked-{_esc(item_id)}" class="brief-box locked">
  <span class="material-symbols-outlined" style="color:var(--text-muted);font-size:18px;">lock</span>
  <div>
    <p class="brief-ready" style="color:var(--text-muted);">Brief locked</p>
    <p class="brief-sub">{unlock_hint}</p>
  </div>
</label>
<label for="modal-locked-{_esc(item_id)}" class="locked-hint">
  <span class="material-symbols-outlined" style="font-size:14px;vertical-align:middle;">info</span>
  Tap to see why
</label>"""
        lock_overlay = f"""<label for="modal-locked-{_esc(item_id)}" class="lock-overlay">
  <div class="lock-circle"><span class="material-symbols-outlined" style="font-size:32px;color:var(--text-muted);">lock</span></div>
</label>"""
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
<div class="{card_cls}" data-item-id="{_esc(item_id)}">
  <div class="product-img-wrap">
    {_img(item.get("image_url", ""), alt=item.get("name", ""), seed=item_id)}
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
    {_intent_chip_row(item_id, save_intent)}
    {brief_box}
    {_compare_cta(item, compare_groups_map)}
    {cta}
  </div>
</div>"""


def _brief_modal_html(
    item: dict[str, Any],
    brief: dict[str, Any],
    user: dict[str, Any],
    *,
    compare_peers: list[dict[str, Any]] | None = None,
    brief_cache: dict[str, dict[str, Any]] | None = None,
    open_checked: bool = False,
) -> str:
    size = brief.get("recommended_size", "M")
    item_id = item.get("id", "")
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
    badge = _esc(brief.get("confidence_badge") or "Good match")
    occasion = _esc(user.get("occasion") or "Your saved occasion")
    reviews = item.get("reviews") or []
    quote_body = _esc(reviews[0].get("body", "")[:140] + ("…" if reviews and len(reviews[0].get("body", "")) > 140 else "")) if reviews else ""
    quote_size = _esc(reviews[0].get("size_bought", size)) if reviews else size
    add_link = _bag_action_link(
        item_id=item_id,
        size=str(size),
        label=str(item.get("short_name") or item.get("brand") or ""),
        button_text=f"Add to Bag — Size {size}",
    )

    compare_html = ""
    compare_peers = compare_peers or []
    brief_cache = brief_cache or {}
    if len(compare_peers) >= 2:
        sub = str(item.get("subcategory") or "items")
        compare_href = _mvp_href(screen="compare", compare_group=sub)
        peer_lines = []
        for peer in compare_peers[:3]:
            peer_id = peer.get("id", "")
            peer_brief = brief_cache.get(peer_id, {})
            peer_size = peer_brief.get("recommended_size", "—")
            peer_lines.append(
                f"<li>{_esc(peer.get('brand'))} · Size {peer_size} · "
                f"{_esc(peer_brief.get('confidence_badge', '—'))}</li>"
            )
        compare_html = f"""
<div class="brief-compare-snippet">
  <h4>Compare with your saves</h4>
  <ul>{"".join(peer_lines)}</ul>
  <a href="{compare_href}" class="compare-inline-link">Open side-by-side compare →</a>
</div>"""

    share_text = (
        f"Myntra Confidence Brief for {item.get('short_name') or item.get('brand')}: "
        f"Size {size} ({brief.get('confidence_badge', 'Good match')}). "
        f"Saved for {user.get('occasion', 'an occasion')}."
    )
    wa_href = f"https://wa.me/?text={quote(share_text)}"
    share_href = _mvp_href(share_brief="1", screen="wishlist", open_brief=item_id)

    checked = " checked" if open_checked else ""

    return f"""
<input type="radio" name="mvp-modal" id="modal-brief-{_esc(item_id)}" class="modal-radio"{checked}/>
<div class="modal-backdrop">
  <label for="{MVP_MODAL_NONE}" class="modal-dismiss" tabindex="-1" aria-hidden="true"></label>
  <div class="brief-modal">
    <div class="modal-header">
      <div class="modal-title">
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">auto_awesome</span>
        Confidence Brief
      </div>
      <label for="{MVP_MODAL_NONE}" class="modal-close-btn" aria-label="Close">
        <span class="material-symbols-outlined" style="color:#5b4042;">close</span>
      </label>
    </div>
    <div class="brief-badge-row">
      <span class="confidence-badge">{badge}</span>
      <span class="occasion-pill">{occasion}</span>
    </div>
    <div class="product-row">
      {_img(thumb, alt=item.get("brand", ""), cls="product-thumb")}
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
    {compare_html}
    <div class="social-proof">
      <h4>What buyers say</h4>
      <blockquote>"{quote_body}"</blockquote>
      <span class="social-meta">Verified buyer · Size {quote_size}</span>
    </div>
    <div class="modal-footer">
      <div class="share-row">
        <a href="{wa_href}" class="share-btn" target="_blank" rel="noopener noreferrer">
          <span class="material-symbols-outlined" style="font-size:16px;">share</span> WhatsApp
        </a>
        <a href="{share_href}" class="share-btn secondary">Copy demo link</a>
      </div>
      <div class="modal-actions">
        <label for="{MVP_MODAL_NONE}" class="btn-outline">Still not sure</label>
        {add_link}
      </div>
      <div class="ai-footer">
        <span class="material-symbols-outlined" style="font-size:14px;vertical-align:middle;">smart_toy</span>
        Powered by Myntra AI · Brief + Compare + Revisit
      </div>
    </div>
  </div>
</div>"""


def _locked_progress_meta(item: dict[str, Any]) -> tuple[str, str, int, str]:
    lock_type = item.get("locked_type", "save_streak")
    if lock_type == "similar_items":
        progress = int(item.get("locked_similar_progress") or 0)
        total = int(item.get("locked_similar_total") or 2)
        label = "Similar items saved"
        count = f"{progress}/{total} ITEMS"
    else:
        progress = int(item.get("locked_days_progress") or 0)
        total = int(item.get("locked_days_total") or 7)
        label = "7-day save streak"
        count = f"{progress}/{total} DAYS"
    pct = min(100, round(progress / total * 100)) if total else 0
    hint = item.get("locked_unlock_hint") or ""
    return label, count, pct, hint


def _similar_thumbs_html(item: dict[str, Any], ready_items: list[dict[str, Any]]) -> str:
    item_id = item.get("id", "")
    similar = [
        ready
        for ready in ready_items
        if ready.get("subcategory") == item.get("subcategory") and ready.get("id") != item_id
    ]
    picks = similar[:2]
    if not picks:
        picks = [ready for ready in ready_items if ready.get("id") != item_id][:2]
    thumbs = []
    for sim in picks:
        brand = _esc(sim.get("brand"))
        thumbs.append(
            f"""
<div class="similar-thumb">
  {_img(sim.get("image_url", ""), alt=brand, seed=str(sim.get("id", "sim")))}
  <div style="position:absolute;bottom:0;left:0;right:0;padding:8px;background:linear-gradient(transparent,rgba(0,0,0,0.6));">
    <span style="color:white;font-size:10px;font-weight:700;">{brand}</span>
  </div>
</div>"""
        )
    return "".join(thumbs)


def _locked_modal_html(item: dict[str, Any], ready_items: list[dict[str, Any]]) -> str:
    item_id = item.get("id", "")
    title = _esc(item.get("short_name") or item.get("brand") or "Brief not ready yet")
    reason = _esc(item.get("locked_reason") or "Your personalized style brief is still compiling.")
    label, count, pct, hint = _locked_progress_meta(item)
    thumbs = _similar_thumbs_html(item, ready_items)
    return f"""
<input type="radio" name="mvp-modal" id="modal-locked-{_esc(item_id)}" class="modal-radio"/>
<div class="modal-backdrop">
  <label for="{MVP_MODAL_NONE}" class="modal-dismiss" tabindex="-1" aria-hidden="true"></label>
  <div class="locked-modal">
    <div style="width:64px;height:64px;border-radius:50%;background:var(--surface-container-low);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">
      <span class="material-symbols-outlined" style="font-size:32px;color:#5b4042;font-variation-settings:'FILL' 1;">lock</span>
    </div>
    <h2 style="font-size:20px;font-weight:700;margin:0 0 8px;">{title}</h2>
    <p style="font-size:14px;color:#5b4042;margin:0 0 16px;padding:0 8px;line-height:1.5;">{reason}</p>
    <div class="progress-box">
      <div style="display:flex;justify-content:space-between;padding-left:8px;">
        <span style="font-size:12px;font-weight:700;text-transform:uppercase;">{_esc(label)}</span>
        <span style="font-size:10px;color:var(--primary);font-weight:700;">{_esc(count)}</span>
      </div>
      <div class="progress-bar" style="margin-left:8px;"><div class="progress-fill" style="width:{pct}%;"></div></div>
      <p style="font-size:10px;color:#5b4042;margin:8px 0 0 8px;">{_esc(hint)}</p>
    </div>
    <div style="width:100%;text-align:left;margin-bottom:24px;">
      <span style="font-size:12px;color:#5b4042;text-transform:uppercase;letter-spacing:0.05em;">Keep exploring</span>
      <div class="similar-thumbs">{thumbs}</div>
    </div>
    <label for="{MVP_MODAL_NONE}" class="btn-primary" style="margin-top:0;">Got it</label>
  </div>
</div>"""


def render_spa(
    *,
    categories: list[dict[str, Any]],
    items: list[dict[str, Any]],
    bag_items: list[str],
    bag_details: dict[str, dict[str, Any]] | None = None,
    brief_cache: dict[str, dict[str, Any]],
    user: dict[str, Any],
    initial_screen: str = "home",
    save_intents: dict[str, str] | None = None,
    dismiss_revisit: bool = False,
    compare_group: str = "",
    open_brief: str = "",
    share_toast: bool = False,
) -> str:
    """Render full interactive SPA — header wishlist + all CTAs work in-page."""
    bag_details = bag_details or {}
    save_intents = save_intents or {}
    groups = compare_groups(items)
    nav_radios = _nav_radios(initial_screen)
    bag_count = len(bag_items)
    bag_label = f"({bag_count} item{'s' if bag_count != 1 else ''})"
    ready_count = sum(1 for i in items if i.get("brief_ready"))

    modal_none_checked = "" if open_brief else " checked"

    category_tiles = []
    for cat in categories:
        category_tiles.append(
            f"""
<a class="category-tile" onclick="return false;">
  {_img(cat.get("image", ""), alt=cat.get("name", ""))}
  <div class="category-info">
    <h3 style="font-size:16px;font-weight:700;margin:0 0 4px;">{_esc(cat.get('name'))}</h3>
    <p style="font-size:20px;font-weight:700;margin:0 0 8px;">{_esc(cat.get('discount'))}</p>
    <span style="font-size:12px;color:var(--primary);text-transform:uppercase;">Shop Now</span>
  </div>
</a>"""
        )

    wishlist_cards = [
        _wishlist_card(
            item,
            in_bag=item.get("id") in bag_items,
            save_intent=save_intents.get(item.get("id", ""), item.get("save_intent", "")),
            compare_groups_map=groups,
        )
        for item in items
    ]

    compare_header_link = ""
    if groups.get("kurta"):
        compare_header_link = (
            f'<a href="{_mvp_href(screen="compare", compare_group="kurta")}" class="filter-btn">'
            f'<span class="material-symbols-outlined" style="font-size:18px;">compare_arrows</span> '
            f"Compare kurtas ({len(groups['kurta'])})</a>"
        )

    brief_modals = ""
    for item_id, brief in brief_cache.items():
        item = next((i for i in items if i.get("id") == item_id), None)
        if item and brief.get("eligible", True) is not False:
            sub = str(item.get("subcategory") or "")
            peers = groups.get(sub, [])
            brief_modals += _brief_modal_html(
                item,
                brief,
                user,
                compare_peers=peers,
                brief_cache=brief_cache,
                open_checked=(open_brief == item_id),
            )

    ready_items = [i for i in items if i.get("brief_ready")]
    locked_modals = "".join(
        _locked_modal_html(item, ready_items)
        for item in items
        if not item.get("brief_ready")
    )
    items_by_id = {i.get("id"): i for i in items}
    bag_rows_html, bag_subtotal = _bag_rows_html(items_by_id, bag_items, bag_details)
    has_bag_items = bag_count > 0
    bag_list_style = "" if has_bag_items else ' style="display:none;"'
    bag_empty_style = ' style="display:none;"' if has_bag_items else ""
    bag_summary_style = "" if has_bag_items else ' style="display:none;"'

    compare_screen_html = ""
    active_group = compare_group if compare_group in groups else ""
    if active_group:
        compare_screen_html = render_compare_screen(
            group_key=active_group,
            items=groups[active_group],
            brief_cache=brief_cache,
            save_intents=save_intents,
            bag_items=bag_items,
            screen_href=_mvp_href,
        )

    return f"""
{MYNTRA_STYLES}
<div class="myntra-mvp">
<input type="radio" name="mvp-modal" id="{MVP_MODAL_NONE}" class="modal-radio"{modal_none_checked}/>
{nav_radios}
{_header(bag_count=len(bag_items))}
{_share_toast_html(visible=share_toast)}

<div id="screen-home" class="screen">
  <main class="main">
    {_journey_strip()}
    <h1 class="shop-title">Shop by Category</h1>
    <div class="category-grid">{''.join(category_tiles)}</div>
  </main>
</div>

<div id="screen-wishlist" class="screen">
  <main class="main">
    {_revisit_banner(ready_count, dismissed=dismiss_revisit)}
    <div class="wishlist-header">
      <h1 style="font-size:28px;font-weight:700;margin:0;">Wishlist <span style="color:var(--text-muted);font-size:16px;font-weight:400;">({len(items)} items)</span></h1>
      <div style="display:flex;gap:16px;flex-wrap:wrap;">
        {compare_header_link}
        <button type="button" class="filter-btn"><span class="material-symbols-outlined" style="font-size:18px;">filter_list</span> Filter</button>
        <button type="button" class="filter-btn"><span class="material-symbols-outlined" style="font-size:18px;">sort</span> Sort</button>
      </div>
    </div>
    <div class="wishlist-grid">{''.join(wishlist_cards)}</div>
  </main>
</div>

{compare_screen_html}

<div id="screen-bag" class="screen">
  <main class="main bag-main">
    <div class="bag-header">
      <h1 style="font-size:28px;font-weight:700;margin:0;">Shopping Bag <span style="color:var(--text-muted);font-size:16px;font-weight:400;">{bag_label}</span></h1>
      <div style="display:flex;gap:16px;">
        <a href="{_screen_href("home")}" class="filter-btn">
          <span class="material-symbols-outlined" style="font-size:18px;">home</span> Go to Home
        </a>
        <a href="{_screen_href("wishlist")}" class="filter-btn">
          <span class="material-symbols-outlined" style="font-size:18px;">favorite</span> Back to Wishlist
        </a>
      </div>
    </div>
    <div class="bag-layout">
      <div id="bag-items-list" class="bag-items-list"{bag_list_style}>{bag_rows_html}</div>
      <div id="bag-empty" class="bag-empty"{bag_empty_style}>
        <span class="material-symbols-outlined" style="font-size:64px;color:var(--text-muted);">shopping_bag</span>
        <h2>Your bag is empty</h2>
        <p>Add items from your wishlist after viewing a Confidence Brief.</p>
        <a href="{_screen_href("wishlist")}" class="btn-primary bag-empty-cta">Go to Wishlist</a>
      </div>
      <aside id="bag-summary" class="bag-summary"{bag_summary_style}>
        <h3>Order Summary</h3>
        <div class="summary-row"><span>Bag Total</span><span>{_format_inr(bag_subtotal)}</span></div>
        <div class="summary-row muted"><span>Delivery</span><span>FREE</span></div>
        <div class="summary-row total"><span>Total</span><span>{_format_inr(bag_subtotal)}</span></div>
        <button type="button" class="btn-primary" style="margin-top:16px;" onclick="alert('Demo MVP — checkout not connected.')">Place Order</button>
        <p class="bag-demo-note">Demo checkout — simulates W2P conversion path</p>
      </aside>
    </div>
  </main>
</div>

{brief_modals}
{locked_modals}
</div>
"""
