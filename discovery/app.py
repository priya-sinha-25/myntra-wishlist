"""Streamlit demo — 5-tab Myntra AI Discovery Engine."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery.aggregate import BLOCKER_LABELS, SEGMENT_LABELS, build_insights
from discovery.classify import classify_text
import discovery.config as config
from discovery.config import CLASSIFIED_DIR, INSIGHTS_DIR, refresh_runtime_config, subprocess_env
from discovery.corpus import load_corpus
from discovery.live_scrape import load_last_run, scrape_and_classify_live
from discovery.research_qa import answer_research_question

MYNTRA_PINK = "#FF3F6C"
MYNTRA_INK = "#282C3F"
MYNTRA_MUTED = "#94969F"
MYNTRA_SURFACE = "#F5F5F6"


def inject_myntra_branding() -> None:
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit chrome */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stDeployButton"] {{display: none;}}
        .stDeployButton {{display: none;}}
        header[data-testid="stHeader"] [data-testid="stToolbar"] {{
            gap: 0.5rem;
        }}

        /* Myntra header */
        .myntra-header {{
            background: linear-gradient(90deg, {MYNTRA_PINK} 0%, #ff527a 100%);
            color: #ffffff;
            padding: 1.1rem 1.4rem;
            border-radius: 0 0 12px 12px;
            margin: -1rem -1rem 1.25rem -1rem;
            box-shadow: 0 2px 12px rgba(255, 63, 108, 0.25);
        }}
        .myntra-header-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .myntra-logo {{
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            line-height: 1;
        }}
        .myntra-badge {{
            background: rgba(255, 255, 255, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 999px;
            padding: 0.25rem 0.75rem;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }}
        .myntra-title {{
            margin: 0.55rem 0 0.15rem 0;
            font-size: 1.35rem;
            font-weight: 700;
        }}
        .myntra-caption {{
            margin: 0;
            font-size: 0.92rem;
            opacity: 0.92;
        }}

        /* Tabs & metrics accent */
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {MYNTRA_PINK} !important;
            border-bottom-color: {MYNTRA_PINK} !important;
        }}
        div[data-testid="stMetricValue"] {{
            color: {MYNTRA_PINK};
        }}
        .stButton > button[kind="primary"] {{
            background-color: {MYNTRA_PINK};
            border-color: {MYNTRA_PINK};
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: #e7355f;
            border-color: #e7355f;
        }}
        </style>
        <div class="myntra-header">
            <div class="myntra-header-top">
                <div class="myntra-logo">MYNTRA</div>
                <div class="myntra-badge">Growth Team · W2P-30</div>
            </div>
            <div class="myntra-title">Wishlist Discovery Engine</div>
            <p class="myntra-caption">AI-powered review intelligence for wishlist conversion research</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Myntra | Wishlist Discovery Engine",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_myntra_branding()
refresh_runtime_config()


def run_pipeline_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=subprocess_env(),
    )


@st.cache_data(ttl=30)
def load_json(path: str) -> dict | list | None:
    file_path = Path(path)
    if not file_path.exists():
        return None
    with file_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def tagged_items() -> list[dict]:
    payload = load_json(str(CLASSIFIED_DIR / "tagged_reviews.json"))
    if not payload:
        return []
    return payload.get("items", [])


def refresh_insights_display() -> dict:
    items = tagged_items()
    if items:
        return build_insights(items)
    return load_json(str(INSIGHTS_DIR / "insights.json")) or {}


def mask_key(key: str) -> str:
    if not key:
        return "Not configured"
    if len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"


SOURCE_LABELS = {
    "play_store": "Play Store",
    "reddit": "Reddit",
    "forum": "Forum / MouthShut",
    "social": "Social (YouTube / IG / Twitter)",
    "quora": "Quora",
    "blog": "Blog / industry",
    "app_store": "App Store",
    "ux_research": "UX research (Medium)",
    "manual": "Manual paste",
}


def source_label(source: str) -> str:
    return SOURCE_LABELS.get(source, source.replace("_", " ").title())


def research_rows(items: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source": source_label(row.get("source", "")),
                "date": row.get("date"),
                "rating": row.get("rating"),
                "wishlist": row.get("wishlist_related"),
                "blocker": row.get("blocker_type"),
                "signal": row.get("signal_type"),
                "segment": row.get("segment_signal"),
                "theme": row.get("theme_label"),
                "text": (row.get("text") or "")[:280],
                "url": row.get("url"),
            }
            for row in items
        ]
    )

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Live Demo", "Pipeline Run", "Pipeline Insights", "Ask Research", "Architecture", "My Research"]
)

with tab1:
    st.subheader("Live Demo — scrape Play Store + classify in real time")

    if not config.GROQ_API_KEY:
        if config.CLASSIFIER_HEURISTIC_FALLBACK:
            st.warning("GROQ_API_KEY missing — using keyword heuristic fallback. Add a key to `.env` or Streamlit secrets.")
        else:
            st.error("GROQ_API_KEY missing — add to `.env` or Streamlit Cloud secrets.")

    last_run = load_last_run()
    if last_run:
        st.caption(
            f"Last live sync: **{last_run.get('ran_at', 'unknown')}** · "
            f"corpus={last_run.get('corpus_total', '?')} · tagged={last_run.get('tagged_total', '?')}"
        )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        live_count = st.number_input("Live scrape count", min_value=1, max_value=25, value=5, step=1)
    with col2:
        merge_live = st.checkbox("Save to corpus + refresh insights", value=True)
    with col3:
        st.markdown("Fetches **fresh** Myntra Play Store reviews now and classifies each with **Groq LLM**.")

    if st.button("Scrape & classify live", type="primary", key="live_scrape_btn"):
        with st.spinner(f"Scraping {live_count} fresh Play Store reviews and classifying with Groq..."):
            try:
                result = scrape_and_classify_live(count=int(live_count), merge_corpus=merge_live)
                st.session_state["live_scrape_result"] = result
                load_json.clear()
                st.success(
                    f"Live scrape complete — {result['meta']['fetched']} fetched, "
                    f"{result['meta']['classified']} classified."
                )
            except Exception as exc:  # noqa: BLE001
                st.error(f"Live scrape failed: {exc}")

    if "live_scrape_result" in st.session_state:
        live_items = st.session_state["live_scrape_result"].get("items", [])
        if live_items:
            st.markdown("**Just scraped & classified (live)**")
            live_df = pd.DataFrame(
                [
                    {
                        "rating": row.get("rating"),
                        "blocker": row.get("blocker_type"),
                        "signal": row.get("signal_type"),
                        "wishlist": row.get("wishlist_related"),
                        "segment": row.get("segment_signal"),
                        "quote": (row.get("evidence_quote") or row.get("text", ""))[:120],
                    }
                    for row in live_items
                ]
            )
            st.dataframe(live_df, use_container_width=True)

    st.divider()
    st.subheader("Classify custom text")
    sample_text = st.text_area(
        "Paste a review or forum comment",
        value="Added 12 dresses to Myntra wishlist for a wedding but still haven't bought. Checking YouTube try-ons because reviews contradict on sizing.",
        height=100,
        key="custom_text",
    )
    if st.button("Classify pasted text", key="classify_text_btn"):
        with st.spinner("Running Groq classifier..."):
            try:
                result = classify_text(sample_text)
                if result.get("classifier") == "heuristic_fallback":
                    st.warning("Groq unavailable — used keyword heuristic fallback. Update models in `.env` or check your API key.")
                cols = st.columns(4)
                cols[0].metric("Wishlist related", str(result.get("wishlist_related")))
                cols[1].metric("Blocker", result.get("blocker_type"))
                cols[2].metric("Signal", result.get("signal_type"))
                cols[3].metric("Intent", result.get("intent_strength"))
                st.json(result)
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))

    st.divider()
    st.markdown("**Latest wishlist-relevant samples (from corpus)**")
    items = tagged_items()
    wishlist_samples = [
        row for row in items
        if row.get("wishlist_related") or row.get("signal_type") == "silent"
    ][:5]
    if not wishlist_samples:
        wishlist_samples = [row for row in items if row.get("source") == "play_store"][:5]
    for row in wishlist_samples:
        st.markdown(
            f"- **{row.get('theme_label')}** · {row.get('signal_type')} · "
            f"blocker={row.get('blocker_type')}  \n"
            f"  _\"{(row.get('evidence_quote') or row.get('text', ''))[:180]}\"_"
        )

with tab2:
    st.subheader("Pipeline Run — stage tracker")
    st.caption("Use **Quick refresh** to update insights in seconds. Full pipeline is for bulk scrape + classify.")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        scrape_count = st.number_input("Play Store count", min_value=10, max_value=500, value=50, step=10)
        classify_limit = st.number_input("Classify limit (0 = all new)", min_value=0, value=30, step=10)
        import_seeds = st.checkbox("Import manual seed sources", value=False)
        skip_scrape = st.checkbox("Skip scrape (use existing corpus)", value=True)

    with col_b:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            quick_refresh = st.button("Quick refresh insights", type="primary")
        with btn_col2:
            run_full = st.button("Run full pipeline")

    if quick_refresh:
        commands = [
            [sys.executable, "-m", "discovery.aggregate"],
            [sys.executable, "-m", "discovery.validate"],
        ]
        logs = []
        for command in commands:
            logs.append(f"$ {' '.join(command)}")
            proc = run_pipeline_command(command)
            logs.append(proc.stdout or proc.stderr or "OK")
        st.session_state["pipeline_logs"] = "\n".join(logs)
        load_json.clear()
        st.success("Insights refreshed from existing classified reviews.")

    if run_full:
        commands = []
        if import_seeds:
            commands.append(
                [sys.executable, "-m", "discovery.paste_importer", str(ROOT / "data" / "seeds" / "manual_sources.csv")]
            )
        if not skip_scrape:
            commands.append([sys.executable, "-m", "discovery.scrape_play_store", "--count", str(int(scrape_count))])
        classify_cmd = [sys.executable, "-m", "discovery.classify"]
        if classify_limit > 0:
            classify_cmd.extend(["--limit", str(int(classify_limit))])
        commands.extend([
            classify_cmd,
            [sys.executable, "-m", "discovery.aggregate"],
            [sys.executable, "-m", "discovery.validate"],
        ])

        logs = []
        progress = st.progress(0, text="Starting pipeline...")
        for i, command in enumerate(commands):
            logs.append(f"$ {' '.join(command)}")
            proc = run_pipeline_command(command)
            logs.append(proc.stdout)
            if proc.stderr:
                logs.append(proc.stderr)
            progress.progress((i + 1) / len(commands), text=f"Step {i + 1}/{len(commands)}")
            if proc.returncode != 0:
                logs.append(f"FAILED with code {proc.returncode}")
                break
            logs.append("OK")
        st.session_state["pipeline_logs"] = "\n".join(logs)
        load_json.clear()
        st.success("Pipeline finished. Check Pipeline Insights tab.")

    corpus_count = len(load_corpus())
    tagged_count = len(tagged_items())
    stages = ["1 · Scrape", "2 · Import seeds", "3 · Classify", "4 · Aggregate", "5 · Validation sample"]
    for label in stages:
        done = corpus_count > 0 if "Scrape" in label or "Import" in label else tagged_count > 0
        st.write(f"{'✅' if done else '⏳'} {label}")

    if "pipeline_logs" in st.session_state:
        st.code(st.session_state["pipeline_logs"])

with tab3:
    st.subheader("Pipeline Insights — from classified review corpus")
    insights_payload = refresh_insights_display()

    if not insights_payload:
        st.warning("No insights yet. Run Quick refresh or classify reviews first.")
    else:
        summary = insights_payload.get("summary", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total classified", summary.get("total_items", 0))
        c2.metric("Wishlist-related %", f"{summary.get('wishlist_related_pct', 0)}%")
        c3.metric("Silent signals", summary.get("silent_signal_count", 0))
        c4.metric("External validation", summary.get("external_validation_count", 0))

        st.markdown("**Key findings from reviews**")
        for finding in insights_payload.get("key_findings", []):
            if finding:
                st.markdown(f"- {finding}")

        col_l, col_r = st.columns(2)
        with col_l:
            blocker_df = pd.DataFrame(
                insights_payload.get("wishlist_blocker_ranking") or insights_payload.get("blocker_ranking", []),
                columns=["blocker", "count"],
            )
            if not blocker_df.empty:
                blocker_df["label"] = blocker_df["blocker"].map(lambda b: BLOCKER_LABELS.get(b, b))
                fig = px.bar(
                    blocker_df,
                    x="label",
                    y="count",
                    title="Top blockers (wishlist-tagged reviews)" if insights_payload.get("wishlist_blocker_ranking") else "Top blockers",
                    color_discrete_sequence=[MYNTRA_PINK],
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_r:
            seg_rows = insights_payload.get("wishlist_segment_distribution") or insights_payload.get("segment_distribution", [])
            if seg_rows:
                segment_df = pd.DataFrame(seg_rows, columns=["segment", "count", "label"])
                fig2 = px.pie(
                    segment_df,
                    names="label",
                    values="count",
                    title="Segment distribution (inferred)",
                    color_discrete_sequence=px.colors.sequential.RdPu,
                )
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("**Segment × blocker (wishlist-tagged reviews)**")
        crosstab = insights_payload.get("segment_x_blocker", {})
        if crosstab:
            display_crosstab = {
                SEGMENT_LABELS.get(seg, seg): {
                    BLOCKER_LABELS.get(b, b): n for b, n in blockers.items()
                }
                for seg, blockers in crosstab.items()
            }
            st.json(display_crosstab)
        else:
            st.info("Not enough wishlist-tagged reviews for crosstab yet.")

        st.markdown("**Killer insight**")
        st.info(insights_payload.get("killer_insight_hypothesis", ""))

        st.markdown("**Top quotes from corpus**")
        for quote in insights_payload.get("top_quotes", []):
            blocker = quote.get("blocker") or quote.get("theme", "")
            st.markdown(
                f"- **{quote['source']}** ({BLOCKER_LABELS.get(blocker, blocker)}, {quote['signal_type']}): "
                f"_\"{quote['quote']}\"_"
            )

with tab4:
    st.subheader("Ask Research — grounded Q&A")
    st.caption(
        "Answers are synthesized from aggregated insights + matching evidence quotes in the corpus."
    )

    if not config.GROQ_API_KEY and not config.CLASSIFIER_HEURISTIC_FALLBACK:
        st.error("Add GROQ_API_KEY to Streamlit secrets or `.env` for full Q&A synthesis.")

    sample_questions = [
        "Why do users save items to wishlist but not buy within 30 days?",
        "How important is YouTube or friend validation before purchasing saved items?",
        "What blocks heavy wishlisters with 100+ saved items from checking out?",
        "Is wishlist used as bookmarking or genuine purchase intent?",
        "Which opportunity area should Myntra prioritize for W2P-30 without discounts?",
        "How do fit-anxious shoppers behave differently from deal hunters?",
    ]

    col_q, col_lens = st.columns([3, 1])
    with col_lens:
        corpus_lens = st.selectbox(
            "Corpus lens",
            options=["all", "wishlist", "curated"],
            format_func=lambda key: {
                "all": "All sources",
                "wishlist": "Wishlist + silent",
                "curated": "Curated (non Play Store)",
            }[key],
            key="qa_corpus_lens",
        )

    with col_q:
        question = st.text_area(
            "Your research question",
            height=90,
            key="qa_question_input",
            placeholder="Ask anything about wishlist behavior, blockers, segments, external validation…",
        )

    st.markdown("**Example questions**")
    example_cols = st.columns(3)
    for index, sample in enumerate(sample_questions):
        label = sample if len(sample) <= 48 else sample[:45] + "…"
        if example_cols[index % 3].button(label, key=f"qa_sample_{index}"):
            st.session_state["qa_question_input"] = sample
            st.rerun()

    ask = st.button("Ask research engine", type="primary", key="qa_ask_btn")

    if ask:
        items = tagged_items()
        if not items:
            st.warning("No classified corpus yet. Run classify or Quick refresh first.")
        elif not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Retrieving evidence and synthesizing answer…"):
                try:
                    result = answer_research_question(
                        question.strip(),
                        items,
                        insights=refresh_insights_display(),
                        corpus_lens=corpus_lens,
                    )
                    st.session_state["qa_result"] = result
                except Exception as exc:  # noqa: BLE001
                    st.error(str(exc))

    if "qa_result" in st.session_state:
        result = st.session_state["qa_result"]
        conf = result.get("confidence", "medium").upper()
        mode = result.get("mode", "groq")
        st.markdown(f"**Confidence:** `{conf}` · **Mode:** `{mode}` · **Lens:** `{result.get('corpus_lens')}`")

        if result.get("mode") == "fallback":
            st.warning("Groq unavailable — showing evidence-backed fallback answer.")

        st.markdown(result.get("answer", ""))

        stats = result.get("key_stats") or []
        if stats:
            st.markdown("**Key stats from research**")
            for stat in stats:
                st.markdown(f"- {stat}")

        implication = result.get("w2p30_implication")
        if implication:
            st.info(f"**W2P-30 implication:** {implication}")

        limitations = result.get("limitations")
        if limitations:
            st.caption(f"Limitations: {limitations}")

        st.markdown("**Evidence cited**")
        cited_ids = set(result.get("cited_evidence_ids") or [])
        for row in result.get("evidence", []):
            blocker = BLOCKER_LABELS.get(row.get("blocker_type", ""), row.get("blocker_type", ""))
            prefix = "**→** " if row.get("id") in cited_ids else ""
            st.markdown(
                f"{prefix}[{row.get('id')}] **{source_label(row.get('source', ''))}** · "
                f"{row.get('signal_type')} · {blocker}  \n"
                f"_{row.get('quote')}_"
            )

with tab5:
    st.subheader("Architecture")
    refresh_runtime_config()
    groq_status = (
        "✅ Configured"
        if config.GROQ_API_KEY
        else "❌ Missing — heuristic fallback"
        if config.CLASSIFIER_HEURISTIC_FALLBACK
        else "❌ Missing"
    )
    st.markdown(f"**Groq API:** {groq_status} · Key: `{mask_key(config.GROQ_API_KEY)}`")
    st.markdown(f"**Models:** `{config.GROQ_MODEL_PRIMARY}` → `{config.GROQ_MODEL_FALLBACK}`")

    st.markdown(
        """
```
Play Store / App Store / Reddit / Forums / Social
        ↓
   scrape_play_store.py + paste_importer.py
        ↓
   corpus.json (deduped, unified schema)
        ↓
   classify.py — Groq LLM (openai/gpt-oss-120b primary, openai/gpt-oss-20b fallback; heuristic if Groq fails)
        ↓
   tagged_reviews.json
        ↓
   aggregate.py → insights.json + insights.md
        ↓
   validate.py → human validation sample
        ↓
   research_qa.py → grounded evaluator Q&A (Tab: Ask Research)
        ↓
   Streamlit demo (this app)
```

**Live scraping**
- Tab 1 **Scrape & classify live** hits Google Play Store in real time via Groq
- GitHub Actions cron runs the same scrape daily at 10:00 AM IST

**Design choices**
- Closed-set taxonomy (11 fields) to reduce hallucination
- `signal_type = silent` captures unvoiced wishlist/decision gaps
- Segment labels inferred from blocker + wishlist context (no "unknown" in charts)
- All classification powered by **Groq LLM** — set `GROQ_API_KEY` in `.env` (local) or **Streamlit secrets** (cloud)
- If Groq fails, keyword **heuristic fallback** runs automatically (`CLASSIFIER_HEURISTIC_FALLBACK=1`)
- Resumable classification keyed by review UID
        """
    )
    st.code(
        "pip install -r requirements.txt\n"
        "copy .env.example .env\n"
        "# Set GROQ_API_KEY=your_key in .env\n"
        "python -m discovery.daily_sync --scrape-count 100",
        language="bash",
    )

with tab6:
    st.subheader("My Research — classified corpus")
    st.caption("Browse all collected reviews. Use the source filter to see Play Store, curated paste, UX research, etc.")

    items = tagged_items()
    corpus_total = len(load_corpus())
    unclassified = max(corpus_total - len(items), 0)

    if not items:
        st.warning("No classified reviews yet. Run classify or Quick refresh first.")
    else:
        source_counts: dict[str, int] = {}
        for row in items:
            src = row.get("source") or "unknown"
            source_counts[src] = source_counts.get(src, 0) + 1

        source_keys = sorted(source_counts, key=lambda key: (-source_counts[key], key))
        filter_options = ["all"] + source_keys

        col_filter, col_meta = st.columns([2, 3])
        with col_filter:
            selected_source = st.selectbox(
                "Filter by source",
                options=filter_options,
                format_func=lambda key: (
                    f"All sources ({len(items)})"
                    if key == "all"
                    else f"{source_label(key)} ({source_counts[key]})"
                ),
                key="research_source_filter",
            )
        with col_meta:
            if unclassified:
                st.caption(f"Corpus total: **{corpus_total}** · Classified: **{len(items)}** · Unclassified: **{unclassified}**")
            else:
                st.caption(f"Showing classified reviews from corpus (**{corpus_total}** total)")

        filtered = items if selected_source == "all" else [row for row in items if row.get("source") == selected_source]
        st.markdown(f"**{len(filtered)}** review(s) · source: **{source_label(selected_source) if selected_source != 'all' else 'All'}**")
        st.dataframe(research_rows(filtered), use_container_width=True, hide_index=True)

    insights_payload = refresh_insights_display()
    if insights_payload:
        st.markdown("**Killer insight (from classified corpus)**")
        st.info(insights_payload.get("killer_insight_hypothesis", ""))

        st.markdown("**Corpus summary**")
        summary = insights_payload.get("summary", {})
        st.markdown(
            f"- Total classified: **{summary.get('total_items', 0)}**  \n"
            f"- Wishlist-related: **{summary.get('wishlist_related_count', 0)}** "
            f"({summary.get('wishlist_related_pct', 0)}%)  \n"
            f"- Silent signals: **{summary.get('silent_signal_count', 0)}**  \n"
            f"- External validation mentions: **{summary.get('external_validation_count', 0)}**"
        )

        st.markdown("**Top quotes**")
        for quote in insights_payload.get("top_quotes", [])[:5]:
            blocker = quote.get("blocker") or quote.get("theme", "")
            st.markdown(
                f"- **{quote['source']}** ({BLOCKER_LABELS.get(blocker, blocker)}): _\"{quote['quote'][:160]}\"_"
            )
