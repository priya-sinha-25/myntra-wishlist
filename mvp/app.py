"""Standalone Myntra Wishlist Confidence Brief MVP — single interactive page."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import discovery.config as config
from discovery.confidence_brief import (
    generate_brief_heuristic,
    generate_confidence_brief,
    list_wishlist_items,
    load_catalog,
    similar_wishlist_items,
)
from discovery.config import refresh_runtime_config
from mvp.compare import INTENT_LABELS, compare_groups
from mvp.spa import render_spa

_ACTION_KEYS = (
    "bag_add",
    "bag_size",
    "bag_label",
    "bag_remove",
    "screen",
    "compare_group",
    "set_intent",
    "intent",
    "dismiss_revisit",
    "open_brief",
    "share_brief",
)
VALID_INTENTS = set(INTENT_LABELS)

SAMPLE_BRIEF_PATH = ROOT / "research" / "sample-confidence-brief.json"
CATALOG_PATH = ROOT / "data" / "mvp" / "wishlist_catalog.json"


def _init_state() -> None:
    defaults = {
        "screen": "home",
        "brief_cache": {},
        "bag_items": [],
        "bag_details": {},
        "save_intents": {},
        "dismiss_revisit": False,
        "open_brief": "",
        "compare_group": "",
        "share_toast": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _user_profile(catalog: dict) -> dict:
    defaults = catalog.get("user_defaults", {})
    return {
        "height_cm": defaults.get("height_cm", 163),
        "weight_kg": defaults.get("weight_kg", 58),
        "usual_size_tops": defaults.get("usual_size_tops", "M"),
        "occasion": defaults.get("occasion", ""),
    }


def _load_sample_brief(item_id: str) -> dict:
    with SAMPLE_BRIEF_PATH.open(encoding="utf-8") as handle:
        brief = json.load(handle)
    brief["eligible"] = True
    brief["item_id"] = item_id
    brief["generator"] = "sample_seed"
    return brief


@st.cache_data(show_spinner=False)
def _groq_brief_cached(item_id: str, catalog_mtime: float) -> dict | None:
    """One Groq call per session — cached. Returns None on failure."""
    refresh_runtime_config()
    if not config.GROQ_API_KEY:
        return None
    try:
        catalog = load_catalog()
        user = _user_profile(catalog)
        brief = generate_confidence_brief(item_id, user, catalog=catalog)
        brief["eligible"] = True
        brief["item_id"] = item_id
        return brief
    except Exception:  # noqa: BLE001
        return None


def _ensure_briefs(catalog: dict, user: dict, items: list[dict]) -> None:
    """Pre-load ALL briefs before render — clicks open instantly, no iframe navigation."""
    if st.session_state.get("briefs_ready"):
        return

    cache = st.session_state["brief_cache"]
    catalog_mtime = CATALOG_PATH.stat().st_mtime if CATALOG_PATH.exists() else 0.0

    for item in items:
        if not item.get("brief_ready"):
            continue
        item_id = item["id"]
        if item_id in cache:
            continue
        compare = similar_wishlist_items(item, items)
        cache[item_id] = generate_brief_heuristic(item, user, compare)
        cache[item_id]["eligible"] = True
        cache[item_id]["item_id"] = item_id

    groq_brief = _groq_brief_cached("wl-001", catalog_mtime)
    if groq_brief:
        cache["wl-001"] = groq_brief
    elif SAMPLE_BRIEF_PATH.exists():
        cache["wl-001"] = _load_sample_brief("wl-001")

    st.session_state["briefs_ready"] = True


def _seed_save_intents(items: list[dict]) -> None:
    intents = st.session_state.setdefault("save_intents", {})
    for item in items:
        item_id = item.get("id", "")
        if item_id and item_id not in intents:
            default = item.get("save_intent")
            if default:
                intents[item_id] = default


def _apply_query_params(items: list[dict]) -> None:
    """Sync bag, screen, compare, intents, and nudges from query params."""
    qp = st.query_params
    if not any(key in qp for key in _ACTION_KEYS):
        return

    valid_ids = {item["id"] for item in items}
    changed = False

    bag_add = qp.get("bag_add")
    if bag_add and bag_add in valid_ids:
        if bag_add not in st.session_state["bag_items"]:
            st.session_state["bag_items"].append(bag_add)
        st.session_state["bag_details"][bag_add] = {
            "size": qp.get("bag_size", "M"),
            "label": qp.get("bag_label", bag_add),
        }
        st.session_state["screen"] = "bag"
        changed = True

    bag_remove = qp.get("bag_remove")
    if bag_remove and bag_remove in valid_ids:
        if bag_remove in st.session_state["bag_items"]:
            st.session_state["bag_items"].remove(bag_remove)
        st.session_state["bag_details"].pop(bag_remove, None)
        st.session_state["screen"] = "bag"
        changed = True

    set_intent = qp.get("set_intent")
    intent = qp.get("intent")
    if set_intent and set_intent in valid_ids and intent in VALID_INTENTS:
        st.session_state["save_intents"][set_intent] = intent
        st.session_state["screen"] = "wishlist"
        changed = True

    if qp.get("dismiss_revisit") == "1":
        st.session_state["dismiss_revisit"] = True
        if st.session_state.get("screen") not in {"bag", "compare"}:
            st.session_state["screen"] = "wishlist"
        changed = True

    compare_group = qp.get("compare_group")
    if compare_group:
        groups = compare_groups(items)
        if compare_group in groups:
            st.session_state["compare_group"] = compare_group
            st.session_state["screen"] = "compare"
            changed = True

    open_brief = qp.get("open_brief")
    if open_brief and open_brief in valid_ids:
        st.session_state["open_brief"] = open_brief
        st.session_state["screen"] = "wishlist"
        changed = True

    if qp.get("share_brief") == "1":
        st.session_state["share_toast"] = True
        if qp.get("screen") in {"home", "wishlist", "bag", "compare"}:
            st.session_state["screen"] = qp.get("screen")
        changed = True

    screen = qp.get("screen")
    if screen in {"home", "wishlist", "bag", "compare"} and not bag_add and not bag_remove:
        if not compare_group or st.session_state.get("screen") != "compare":
            st.session_state["screen"] = screen
        changed = True

    for key in _ACTION_KEYS:
        if key in qp:
            del st.query_params[key]

    if changed:
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Myntra | Wishlist Confidence Brief",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap"/>
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: transparent;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        .stApp {background: #f9f9f9;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    refresh_runtime_config()
    _init_state()

    catalog = load_catalog()
    items = list_wishlist_items(catalog)
    user = _user_profile(catalog)

    _apply_query_params(items)
    _seed_save_intents(items)

    catalog_mtime = CATALOG_PATH.stat().st_mtime if CATALOG_PATH.exists() else 0.0
    if st.session_state.get("catalog_mtime") != catalog_mtime:
        st.session_state["briefs_ready"] = False
        st.session_state["brief_cache"] = {}
        st.session_state["catalog_mtime"] = catalog_mtime

    if not st.session_state.get("briefs_ready"):
        with st.spinner("Preparing Confidence Briefs…"):
            _ensure_briefs(catalog, user, items)
    else:
        _ensure_briefs(catalog, user, items)

    html_page = render_spa(
        categories=catalog.get("home_categories", []),
        items=items,
        bag_items=st.session_state["bag_items"],
        bag_details=st.session_state.get("bag_details", {}),
        brief_cache=st.session_state["brief_cache"],
        user=user,
        initial_screen=st.session_state.get("screen", "home"),
        save_intents=st.session_state.get("save_intents", {}),
        dismiss_revisit=st.session_state.get("dismiss_revisit", False),
        compare_group=st.session_state.get("compare_group", ""),
        open_brief=st.session_state.get("open_brief", ""),
        share_toast=st.session_state.get("share_toast", False),
    )
    st.session_state["open_brief"] = ""
    st.session_state["share_toast"] = False

    st.html(html_page, unsafe_allow_javascript=True)


if __name__ == "__main__":
    main()
