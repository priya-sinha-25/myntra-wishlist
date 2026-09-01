# Slide 5 — Solutions: 3 Directions, 1 Choice (Part 5 MVP)

> **Part 5:** MVP Definition  
> **Pattern:** Reference deck — 3 solutions with why each wins/loses + ICE score → pick 1  
> **Constraint:** No monetary incentives · **North star:** W2P-30

---

## KEY MESSAGE (For Final Deck)

**Title:** *Three ways to fix wishlist conversion — only one is generative, buildable, and research-backed*

**One-line:** We ICE-scored three no-discount interventions; **AI Confidence Brief** wins because it replaces off-app validation at the exact moment users stall.

---

## HYPOTHESIS (State before solutions — reference deck pattern)

> If Myntra shows an **AI Confidence Brief** on wishlisted items where users stall (7+ days saved or competing similar items), then **wishlist → Add to Bag** and **W2P-30** will increase because users get **in-app fit/review synthesis and compare help** — replacing the YouTube/WhatsApp/offline loop — **without discounts**.

**Why only this hypothesis?**
- Targets **moment of abandonment** (Step 4 revisit) — not generic wishlist UX  
- **Solvable with AI** on existing reviews + catalog (discovery: 45.7% addressable w/o discount)  
- **Survey validated:** 79% concept-positive; 8/18 want review/fit summary most  
- **No competitor** offers opinionated AI brief on saves  

---

## THREE SOLUTIONS

### Solution 1: Wishlist Smart Reminders / Price-Drop Alerts

**Idea:** Notify users when wishlisted items go on sale or hit target price.

| | |
|--|--|
| **Key features** | Price-drop push · EORS alerts · "Back in stock" ping |
| **User needs solved** | Saves money on items already wanted |
| **Evidence for** | Survey: **47%** cite "waiting for sale" as blocker |
| **Why it loses** | **Violates no-discount constraint** · Optimizes deal hunters (discovery segment 13) · Doesn't resolve fit/decide — user still won't buy if uncertain · Commodity feature (Amazon, AJIO already do this) |
| **ICE** | Impact **5** · Confidence **7** · Effort **4** → **Score 8.75** |

---

### Solution 2: Wishlist UX Overhaul (Filter, Sort, Categorize)

**Idea:** Reorganize wishlist — folders, occasion tags, sort by price/rating, clean up 100+ item lists.

| | |
|--|--|
| **Key features** | Category folders · Sort/filter · Bulk remove · Share lists |
| **User needs solved** | Reduces scroll fatigue; finds items faster |
| **Evidence for** | Discovery: app_ux **9**, heavy wishlister **32**; Survey magic-wand: "categorize wishlist" |
| **Why it loses** | Fixes **Step 2–3** (revisit/navigation) not **Step 4** (confidence to buy) · Doesn't replace off-app validation (84% survey) · Larger eng effort · **Enabler, not converter** — users still leave to check fit on YouTube |
| **ICE** | Impact **6** · Confidence **6** · Effort **8** → **Score 4.5** |

---

### Solution 3: AI Confidence Brief on Wishlisted Items ✅ WINNER

**Idea:** On each stalled save, show a short AI-generated brief — fit summary from reviews, recommended size, optional compare vs similar wishlist items. One tap from wishlist card.

| | |
|--|--|
| **Key features** | Review/fit synthesis · Body-type size rec · "Compare my saves" for similar items · Relevance badge (Strong/Uncertain fit signal) |
| **User needs solved** | Trust fit without leaving app · Pick among similar saves · Decide without waiting for sale |
| **Evidence for** | Discovery: size_fit **28**, external **30**, decide **16** · Survey: **79%** concept +, **8/18** want review summary · Open-text: offline validation → still not bought |
| **Why it wins** | **Generative** — creates new confidence, not just reorganizes list · **Buildable** on reviews + catalog + Groq (you already have pipeline) · **Matches silent signal** discovery found · **No discount** · Directly attacks 84% off-app validation |
| **ICE** | Impact **9** · Confidence **8** · Effort **6** → **Score 12.0** ★ |

---

## ICE SCORING SUMMARY (Put as table on slide)

| Solution | Impact | Confidence | Effort | ICE Score | Verdict |
|----------|--------|------------|--------|-----------|---------|
| 1. Price-drop alerts | 5 | 7 | 4 | **8.75** | Rejected — constraint + wrong segment |
| 2. Wishlist UX overhaul | 6 | 6 | 8 | **4.5** | Rejected — enabler only, not Step 4 |
| **3. AI Confidence Brief** | **9** | **8** | **6** | **12.0 ★** | **Selected MVP** |

*ICE = (Impact × Confidence) / Effort*

---

## WHY SOLUTION 3 WINS — DATA LADDER (Preetham-style)

```
1. DISCOVERY     size/fit 28 + external 30 + silent 31  →  Step 4 leak confirmed
        ↓
2. SEGMENT       Fit-anxious 33 (27/33 fit)             →  Target defined
        ↓
3. SURVEY        74% fit-anxious · 84% off-app          →  Human validation
        ↓
4. CONCEPT       79% positive · review summary #1       →  Feature direction
        ↓
5. ROOT CAUSE    No in-app decision mechanism           →  Confidence Brief fills gap
```

---

## MVP SCOPE — CONFIDENCE BRIEF v1

### Build (P0)

| Feature | Detail |
|---------|--------|
| **Fit & Review Brief** | 3–5 lines: "Buyers your size say…", fabric notes, runs small/large flags |
| **Recommended size** | One suggestion from size chart + review patterns |
| **Entry points** | Wishlist card CTA + PDP when opened from wishlist |
| **Trigger** | Item saved **≥7 days** OR **≥2 similar items** in same subcategory |
| **AI stack** | Groq on review text (reuse discovery pipeline patterns) |

### Build if time (P1)

| Feature | Detail |
|---------|--------|
| **Compare my saves** | Side-by-side 2–3 similar items: fit sentiment, price, occasion |
| **Optional user input** | Height / usual size for better rec |

### Do NOT build (Non-goals)

- Coupons, price alerts, EORS triggers  
- Full wishlist redesign (Solution 2 — Phase 2 enabler)  
- Push notifications / revisit nudges (Phase 2)  
- Auto-add to cart  

---

## USER FLOW (MVP)

```
Wishlist → Item idle 7+ days → "Get Confidence Brief" CTA
       ↓
Brief panel: size rec + review synthesis + [compare if applicable]
       ↓
Add to Bag (primary) · "Still not sure" (feedback)
```

**UX contrast (reference deck "Before / After" row):**

| Today | With Confidence Brief |
|-------|----------------------|
| Reopen PDP → read 50 reviews → leave for YouTube | One AI brief → decide in-app |
| 3 kurtas saved → ask WhatsApp group | Compare brief across saves |
| Wait for sale indefinitely | Buy when **confident**, not only when cheap |

---

## PROTOTYPE DELIVERABLES (What you submit for Part 5)

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | This slide — 3 solutions + ICE + winner | ✅ |
| 2 | Wireframe — wishlist card + Brief panel | ⬜ To do |
| 3 | **1 sample Brief** — real product + Groq output | ⬜ To do |
| 4 | Honesty callout — live vs mocked (like reference) | ⬜ To do |
| 5 | Link discovery Streamlit demo | ✅ Built |

**Honesty callout (copy reference pattern):**

| ✓ Live / real | ~ Mocked / simplified |
|---------------|----------------------|
| ✓ Groq-generated fit summary | ~ Product from static catalog, not live API |
| ✓ Review text from real Myntra PDP | ~ Personalization = category-level, not full history |
| ✓ Brief UI flow in prototype | ~ Compare uses 2 hardcoded wishlist items |

---

## SLIDE 5 BULLETS (Copy-paste)

- **3 solutions scored:** Price alerts · UX overhaul · **AI Confidence Brief**  
- **ICE winner:** Confidence Brief (12.0) — generative, no-discount, Step 4  
- **Rejected #1:** Price alerts — constraint + deal hunters  
- **Rejected #2:** UX overhaul — helps find items, not trust them  
- **MVP:** Brief on wishlist (fit summary + size rec + compare) · 7-day trigger  
- **Proof chain:** Discovery 739 → Survey 18 → 79% concept positive  

---

## PHASE 2 (Mention on slide — don't build now)

- Solution 2 elements: wishlist folders / occasion tags  
- Revisit notifications when Brief ready  
- Occasion suitability line in Brief  
- A/B test Brief vs control on W2P-30  

---

*Next: Part 6 metrics (`slide-06-metrics.md`) · Part 7 risks · Final deck assembly*
