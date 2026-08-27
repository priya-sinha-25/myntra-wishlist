"""Grounded Q&A over classified corpus and aggregated insights."""
from __future__ import annotations

import json
import re
from typing import Any

from discovery.aggregate import BLOCKER_LABELS, SEGMENT_LABELS, build_insights
import discovery.config as config
from discovery.config import refresh_runtime_config

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is",
    "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "would", "could", "should", "may", "might", "must", "shall", "can",
    "what", "why", "how", "when", "where", "who", "which", "their", "they", "them",
    "users", "user", "myntra", "wishlist", "wishlisted", "about", "from", "with",
    "that", "this", "these", "those", "it", "its", "any", "some", "many", "most",
}

SYNONYMS: dict[str, set[str]] = {
    "fit": {"size", "sizing", "fit", "fitting", "petite", "plus", "chart"},
    "price": {"price", "sale", "discount", "expensive", "cost", "eors", "offer"},
    "compare": {"compare", "comparison", "shortlist", "duplicate", "versus", "between"},
    "external": {"youtube", "instagram", "friend", "friends", "whatsapp", "competitor", "ajio"},
    "postpone": {"wait", "waiting", "later", "delay", "postpone", "sale"},
    "intent": {"intent", "bookmark", "save", "saved", "purchase", "buy", "buying"},
    "segment": {"segment", "shopper", "wedding", "occasion", "festive", "deal"},
    "silent": {"silent", "unvoiced", "implicit", "without", "asking"},
    "delivery": {"delivery", "return", "refund", "exchange", "late"},
    "quality": {"quality", "fabric", "material", "fake", "photo", "review"},
    "styling": {"style", "styling", "outfit", "occasion", "dress", "code"},
    "decision": {"decide", "decision", "confused", "paralysis", "overload", "choose"},
}


def _tokenize(text: str) -> set[str]:
    tokens = {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}
    return {token for token in tokens if token not in STOPWORDS}


def _expand_tokens(tokens: set[str]) -> set[str]:
    expanded = set(tokens)
    for token in tokens:
        for group in SYNONYMS.values():
            if token in group:
                expanded |= group
    return expanded


def _row_text(row: dict[str, Any]) -> str:
    parts = [
        row.get("text") or "",
        row.get("evidence_quote") or "",
        row.get("theme_label") or "",
        row.get("blocker_type") or "",
        row.get("save_reason") or "",
        row.get("segment_signal") or "",
        row.get("external_validation") or "",
        row.get("source") or "",
    ]
    return " ".join(str(part) for part in parts if part).lower()


def retrieve_relevant_items(
    question: str,
    items: list[dict[str, Any]],
    *,
    top_k: int = 12,
    wishlist_boost: bool = True,
) -> list[dict[str, Any]]:
    """Keyword + label retrieval with wishlist/silent boosting."""
    query_tokens = _expand_tokens(_tokenize(question))
    if not query_tokens:
        query_tokens = _tokenize(question)

    scored: list[tuple[float, dict[str, Any]]] = []
    for row in items:
        haystack = _row_text(row)
        overlap = sum(1 for token in query_tokens if token in haystack)
        if overlap == 0 and query_tokens:
            continue

        score = float(overlap)
        if wishlist_boost and row.get("wishlist_related"):
            score += 2.0
        if row.get("signal_type") == "silent":
            score += 1.5
        if row.get("blocker_type") not in {None, "none"}:
            score += 0.5
        score += min(int(row.get("intent_strength") or 0), 5) * 0.1

        if score > 0 or not query_tokens:
            scored.append((score, row))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    if not scored and items:
        # Fallback: top wishlist + silent items
        fallback = sorted(
            items,
            key=lambda row: (
                1 if row.get("wishlist_related") else 0,
                1 if row.get("signal_type") == "silent" else 0,
                int(row.get("intent_strength") or 0),
            ),
            reverse=True,
        )
        return fallback[:top_k]

    return [row for _, row in scored[:top_k]]


def _insights_context(insights: dict[str, Any]) -> str:
    summary = insights.get("summary", {})
    lines = [
        f"Total classified reviews: {summary.get('total_items', 0)}",
        f"Wishlist-related: {summary.get('wishlist_related_count', 0)} ({summary.get('wishlist_related_pct', 0)}%)",
        f"Silent signals: {summary.get('silent_signal_count', 0)}",
        f"External validation mentions: {summary.get('external_validation_count', 0)}",
        f"Addressable without discount: {summary.get('addressable_without_discount_count', 0)} ({summary.get('addressable_without_discount_pct', 0)}%)",
        f"Killer insight: {insights.get('killer_insight_hypothesis', '')}",
    ]

    lines.append("Top blockers (wishlist-tagged):")
    for blocker, count in insights.get("wishlist_blocker_ranking", [])[:5]:
        lines.append(f"- {BLOCKER_LABELS.get(blocker, blocker)}: {count}")

    lines.append("Segment distribution (wishlist-tagged):")
    for seg, count, label in insights.get("wishlist_segment_distribution", [])[:5]:
        lines.append(f"- {label}: {count}")

    for finding in insights.get("key_findings", []):
        if finding:
            lines.append(f"Finding: {finding}")

    return "\n".join(lines)


def _evidence_context(rows: list[dict[str, Any]]) -> str:
    chunks = []
    for index, row in enumerate(rows, start=1):
        quote = (row.get("evidence_quote") or row.get("text") or "")[:320]
        blocker = BLOCKER_LABELS.get(row.get("blocker_type", ""), row.get("blocker_type", ""))
        segment = SEGMENT_LABELS.get(row.get("segment_signal", ""), row.get("segment_signal", ""))
        chunks.append(
            f"[{index}] source={row.get('source')} wishlist={row.get('wishlist_related')} "
            f"signal={row.get('signal_type')} blocker={blocker} segment={segment} "
            f"save_reason={row.get('save_reason')} external={row.get('external_validation')}\n"
            f"Quote: {quote}"
        )
    return "\n\n".join(chunks)


def _parse_answer_json(content: str) -> dict[str, Any]:
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _answer_with_groq(question: str, insights: dict[str, Any], evidence_rows: list[dict[str, Any]]) -> dict[str, Any]:
    refresh_runtime_config()
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    from groq import Groq

    system = """You are a research analyst for Myntra's W2P-30 (wishlist-to-purchase) discovery engine.

Answer evaluator questions using ONLY the provided aggregated insights and evidence quotes.
Do not invent statistics, user counts, or quotes not supported by the context.
If evidence is thin, say so explicitly and suggest what additional research would help.

Return ONLY valid JSON:
{
  "answer": "2-4 short paragraphs in plain language",
  "confidence": "high|medium|low",
  "key_stats": ["bullet with numbers from insights context only"],
  "cited_evidence_ids": [1, 2],
  "w2p30_implication": "one sentence on how this relates to wishlist conversion",
  "limitations": "what the corpus may miss"
}

Rules:
- Prefer wishlist-tagged and silent-signal evidence when relevant
- Distinguish loud Play Store noise (delivery) vs wishlist decision friction
- Cite evidence by [id] numbers from the evidence block
- key_stats must come from insights summary or countable evidence patterns
"""

    user = f"""QUESTION:
{question}

AGGREGATED INSIGHTS:
{_insights_context(insights)}

EVIDENCE QUOTES:
{_evidence_context(evidence_rows)}
"""

    client = Groq(api_key=config.GROQ_API_KEY)
    for model in (config.GROQ_MODEL_PRIMARY, config.GROQ_MODEL_FALLBACK):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.2,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            payload = _parse_answer_json(response.choices[0].message.content or "{}")
            payload["model_used"] = model
            return payload
        except Exception:
            continue
    raise RuntimeError("Groq Q&A failed on all models")


def _fallback_answer(question: str, insights: dict[str, Any], evidence_rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary = insights.get("summary", {})
    top_blockers = insights.get("wishlist_blocker_ranking") or insights.get("blocker_ranking") or []
    blocker_line = ""
    if top_blockers:
        label = BLOCKER_LABELS.get(top_blockers[0][0], top_blockers[0][0])
        blocker_line = f"The strongest pattern in wishlist-tagged data is **{label}** ({top_blockers[0][1]} mentions)."

    quote_lines = []
    for index, row in enumerate(evidence_rows[:3], start=1):
        quote = (row.get("evidence_quote") or row.get("text") or "")[:180]
        quote_lines.append(f"[{index}] {quote}")

    answer = (
        f"Based on **{summary.get('total_items', 0)}** classified conversations "
        f"({summary.get('wishlist_related_count', 0)} wishlist-related, "
        f"{summary.get('silent_signal_count', 0)} silent signals), "
        f"here is what the corpus suggests about your question.\n\n"
        f"{blocker_line}\n\n"
        f"{insights.get('killer_insight_hypothesis', '')}\n\n"
        "Representative evidence:\n" + "\n".join(f"- {line}" for line in quote_lines)
    )

    return {
        "answer": answer,
        "confidence": "medium",
        "key_stats": insights.get("key_findings", [])[:4],
        "cited_evidence_ids": list(range(1, min(4, len(evidence_rows) + 1))),
        "w2p30_implication": "Wishlist conversion likely improves when pre-purchase uncertainty is resolved without discounts.",
        "limitations": "Fallback mode — enable Groq for richer synthesis.",
        "model_used": "fallback",
    }


def answer_research_question(
    question: str,
    items: list[dict[str, Any]],
    insights: dict[str, Any] | None = None,
    *,
    top_k: int = 12,
    corpus_lens: str = "all",
) -> dict[str, Any]:
    """Answer an evaluator question grounded in classified corpus + insights."""
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty")

    insights_payload = insights or build_insights(items)

    filtered = items
    if corpus_lens == "wishlist":
        filtered = [
            row for row in items
            if row.get("wishlist_related") or row.get("signal_type") == "silent"
        ]
    elif corpus_lens == "curated":
        filtered = [row for row in items if row.get("source") != "play_store"]

    if not filtered:
        filtered = items

    evidence_rows = retrieve_relevant_items(question, filtered, top_k=top_k)

    try:
        llm_payload = _answer_with_groq(question, insights_payload, evidence_rows)
        mode = "groq"
    except Exception as exc:
        llm_payload = _fallback_answer(question, insights_payload, evidence_rows)
        llm_payload["groq_error"] = str(exc)[:240]
        mode = "fallback"

    return {
        "question": question,
        "corpus_lens": corpus_lens,
        "mode": mode,
        "answer": llm_payload.get("answer", ""),
        "confidence": llm_payload.get("confidence", "medium"),
        "key_stats": llm_payload.get("key_stats", []),
        "cited_evidence_ids": llm_payload.get("cited_evidence_ids", []),
        "w2p30_implication": llm_payload.get("w2p30_implication", ""),
        "limitations": llm_payload.get("limitations", ""),
        "model_used": llm_payload.get("model_used"),
        "evidence": [
            {
                "id": index,
                "source": row.get("source"),
                "wishlist_related": row.get("wishlist_related"),
                "signal_type": row.get("signal_type"),
                "blocker_type": row.get("blocker_type"),
                "segment_signal": row.get("segment_signal"),
                "quote": (row.get("evidence_quote") or row.get("text") or "")[:240],
            }
            for index, row in enumerate(evidence_rows, start=1)
        ],
    }
