# Slide 6 — MVP: Live Wishlist Confidence Brief

> **Part 5 deliverable:** **Deployed MVP** — Streamlit tab **Wishlist MVP**  
> **Run:** `streamlit run discovery/app.py` → tab **Wishlist MVP**

---

## KEY MESSAGE (For Final Deck)

**Title:** *Live MVP — Groq generates Confidence Brief on stalled wishlist saves*

**One-line:** Not a wireframe — select item → AI brief → Add to Bag, with eligibility rules and session metrics.

---

## WHAT IS LIVE

| Component | Status |
|-----------|--------|
| Wishlist UI (4 demo products) | ✅ Live |
| Eligibility (7+ days / similar items) | ✅ Live |
| Groq Confidence Brief | ✅ Live |
| Fit profile sidebar | ✅ Live |
| Compare vs other saves | ✅ Live |
| Add to Bag + metrics | ✅ Live |
| Myntra catalog API | ~ Demo JSON catalog |
| Real checkout | ~ Session bag |

---

## DEMO FLOW

1. `streamlit run discovery/app.py`
2. Tab **Wishlist MVP**
3. Select **Anouk kurta** (12 days — eligible)
4. Generate Brief → size M · Strong match · vs Sangria/Libas
5. Add to Bag → session metric ↑

---

## SLIDE 6 BULLETS

- **MVP shipped** in Streamlit — Groq live, not static mock  
- **Triggers:** 7+ days OR 2+ similar saves  
- **Output:** Size rec + review synthesis + compare + Add to Bag  
- **Honesty:** Demo catalog; AI pipeline real  

---

*Code: `discovery/confidence_brief.py` · `discovery/mvp_wishlist_ui.py`*
