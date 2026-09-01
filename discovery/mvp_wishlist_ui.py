"""Streamlit UI for Wishlist Confidence Brief MVP."""
from __future__ import annotations

import streamlit as st

import discovery.config as config
from discovery.confidence_brief import (
    brief_eligible,
    generate_confidence_brief,
    get_item,
    list_wishlist_items,
    load_catalog,
    similar_wishlist_items,
)

MYNTRA_PINK = "#FF3F6C"
BADGE_COLORS = {
    "Strong match": "#1b8f4d",
    "Good match": "#c77d00",
    "Wider stretch": "#d64b4b",
}


def _init_mvp_state() -> None:
    defaults = {
        "mvp_selected_id": None,
        "mvp_brief_cache": {},
        "mvp_briefs_opened": 0,
        "mvp_add_to_bag": 0,
        "mvp_still_not_sure": 0,
        "mvp_bag_items": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _inject_mvp_styles() -> None:
    st.markdown(
        f"""
        <style>
        .wishlist-card {{
            border: 1px solid #e9e9eb;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.75rem;
            background: #fff;
            box-shadow: 0 1px 4px rgba(40,44,63,0.06);
        }}
        .wishlist-card.selected {{
            border-color: {MYNTRA_PINK};
            box-shadow: 0 0 0 1px {MYNTRA_PINK};
        }}
        .brief-badge {{
            display: inline-block;
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.5rem;
        }}
        .brief-panel {{
            border: 1px solid #ffe0e8;
            background: linear-gradient(180deg, #fff9fb 0%, #ffffff 100%);
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
        }}
        .price-tag {{ color: {MYNTRA_PINK}; font-weight: 700; }}
        .muted {{ color: #94969f; font-size: 0.88rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _badge_html(label: str) -> str:
    color = BADGE_COLORS.get(label, "#666")
    return f'<span class="brief-badge" style="background:{color}">{label}</span>'


def render_wishlist_mvp_tab() -> None:
    _init_mvp_state()
    _inject_mvp_styles()

    st.subheader("Wishlist Confidence Brief — Live MVP")
    st.caption(
        "Part 5 product: AI fit/review synthesis on stalled saves · "
        "Triggers when saved **7+ days** or **2+ similar items** · No discounts"
    )

    if not config.GROQ_API_KEY:
        if config.CLASSIFIER_HEURISTIC_FALLBACK:
            st.warning("GROQ_API_KEY missing — briefs use heuristic fallback. Add key to `.env` for live AI.")
        else:
            st.error("GROQ_API_KEY required for Confidence Brief MVP.")

    catalog = load_catalog()
    items = list_wishlist_items(catalog)
    defaults = catalog.get("user_defaults", {})

    with st.sidebar:
        st.markdown("### Your fit profile")
        height_cm = st.number_input("Height (cm)", min_value=140, max_value=200, value=int(defaults.get("height_cm", 163)))
        weight_kg = st.number_input("Weight (kg)", min_value=40, max_value=120, value=int(defaults.get("weight_kg", 58)))
        usual_size = st.selectbox("Usual top size", ["XS", "S", "M", "L", "XL", "XXL"], index=2)
        occasion = st.text_input("Occasion you're shopping for", value=defaults.get("occasion", ""))
        user = {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "usual_size_tops": usual_size,
            "occasion": occasion,
        }

        st.divider()
        st.markdown("### Session metrics (MVP demo)")
        st.metric("Briefs opened", st.session_state["mvp_briefs_opened"])
        st.metric("Add to Bag", st.session_state["mvp_add_to_bag"])
        st.metric("Still not sure", st.session_state["mvp_still_not_sure"])

    col_list, col_brief = st.columns([1, 1.2])

    with col_list:
        st.markdown("#### ♥ Your wishlist")
        for item in items:
            eligible, reason = brief_eligible(item, items)
            selected = st.session_state["mvp_selected_id"] == item.get("id")
            card_class = "wishlist-card selected" if selected else "wishlist-card"

            st.markdown(
                f"""
                <div class="{card_class}">
                    <div style="font-size:1.6rem">{item.get('image_emoji', '🛍️')}</div>
                    <div style="font-weight:700;margin-top:0.3rem">{item.get('name')}</div>
                    <div class="muted">{item.get('brand')} · {item.get('category')}</div>
                    <div class="price-tag" style="margin-top:0.35rem">₹{item.get('price_inr'):,}</div>
                    <div class="muted">Saved {item.get('saved_days')} days · {item.get('review_count')} reviews</div>
                    <div class="muted" style="margin-top:0.25rem">{'✨ Brief available' if eligible else '🔒 ' + reason}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_label = "View Confidence Brief" if eligible else "Select item"
            if st.button(btn_label, key=f"select_{item.get('id')}", use_container_width=True):
                st.session_state["mvp_selected_id"] = item.get("id")

    with col_brief:
        selected_id = st.session_state.get("mvp_selected_id")
        if not selected_id:
            st.info("Select a wishlist item to generate your Confidence Brief.")
            return

        item = get_item(selected_id, catalog)
        if not item:
            st.error("Item not found.")
            return

        eligible, reason = brief_eligible(item, items)
        st.markdown(f"#### ✨ Confidence Brief")
        st.caption(reason)

        if not eligible:
            st.warning(
                "This item isn't eligible yet. MVP triggers when saved **≥7 days** "
                "or you have **2+ similar items** (e.g. multiple kurtas)."
            )
            similar = similar_wishlist_items(item, items)
            if similar:
                st.markdown("**Similar saves on your wishlist:**")
                for other in similar:
                    st.markdown(f"- {other.get('name')} · ₹{other.get('price_inr'):,}")
            return

        cache_key = f"{selected_id}:{height_cm}:{weight_kg}:{usual_size}:{occasion}"
        if st.button("Generate / refresh Brief", type="primary", key="gen_brief"):
            with st.spinner("Groq is synthesizing fit & review signal…"):
                try:
                    brief = generate_confidence_brief(selected_id, user, catalog=catalog)
                    st.session_state["mvp_brief_cache"][cache_key] = brief
                    st.session_state["mvp_briefs_opened"] += 1
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Brief generation failed: {exc}")

        brief = st.session_state["mvp_brief_cache"].get(cache_key)
        if not brief:
            st.markdown(
                "_Tap **Generate / refresh Brief** to run the live AI pipeline on this item's reviews._"
            )
            return

        badge = brief.get("confidence_badge", "Good match")
        st.markdown(
            f"""
            <div class="brief-panel">
                {_badge_html(badge)}
                <div style="font-size:1.05rem;font-weight:700;margin-bottom:0.35rem">
                    Recommended size: {brief.get('recommended_size', '—')}
                </div>
                <div class="muted">{brief.get('size_rationale', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**What buyers like you say**")
        for bullet in brief.get("fit_summary_bullets") or []:
            st.markdown(f"- {bullet}")

        st.markdown(f"**Fabric & quality:** {brief.get('fabric_quality_line', '')}")
        st.markdown(f"**Occasion fit:** {brief.get('occasion_fit', '')}")

        if brief.get("compare_vs_wishlist"):
            st.markdown("**vs your other saves**")
            st.markdown(brief.get("compare_vs_wishlist"))

        st.markdown(f"**Trust signal:** {brief.get('why_trust_this', '')}")
        if brief.get("honest_caveat"):
            st.caption(f"Note: {brief.get('honest_caveat')}")

        gen = brief.get("generator", "unknown")
        model = brief.get("model", "")
        st.caption(f"Generator: `{gen}`" + (f" · `{model}`" if model else ""))

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Add to Bag", type="primary", use_container_width=True, key="atb"):
                st.session_state["mvp_add_to_bag"] += 1
                if selected_id not in st.session_state["mvp_bag_items"]:
                    st.session_state["mvp_bag_items"].append(selected_id)
                st.success(f"Added **{item.get('name')}** ({brief.get('recommended_size')}) to bag — MVP conversion logged.")

        with btn_col2:
            if st.button("Still not sure", use_container_width=True, key="unsure"):
                st.session_state["mvp_still_not_sure"] += 1
                st.info("Feedback logged — would refine Brief or suggest external validation alternatives in production.")

        if st.session_state["mvp_bag_items"]:
            st.divider()
            st.markdown("**Your bag (this session)**")
            for bag_id in st.session_state["mvp_bag_items"]:
                bag_item = get_item(bag_id, catalog)
                if bag_item:
                    st.markdown(f"- {bag_item.get('name')} · ₹{bag_item.get('price_inr'):,}")

    st.divider()
    with st.expander("MVP honesty callouts (for deck / reviewers)"):
        st.markdown(
            """
| ✓ Live in this MVP | ~ Simplified |
|--------------------|--------------|
| Groq-generated Confidence Brief (or heuristic fallback) | Wishlist catalog = curated demo products with embedded reviews |
| Eligibility rules (7+ days / similar items) | Not connected to live Myntra account or catalog API |
| Add to Bag + session metrics | Cart/checkout not integrated — conversion logged in-session |
| Compare block uses other items on demo wishlist | 4 demo products; kurta cluster drives compare flow |
            """
        )
