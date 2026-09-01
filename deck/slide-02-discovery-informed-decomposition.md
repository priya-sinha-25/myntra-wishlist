# Slide 2 — Discovery Confirms Step 4 Is the Leak; Fit-Anxious Wishlisters Are the Highest-Leverage Segment

> **Part 2:** Business Metric Decomposition × AI Discovery Engine  
> **Product:** Myntra · **Team:** Growth · **Constraint:** No monetary incentives  
> **Data as of:** 739 classified reviews (647 Play Store + 92 curated) · 113 wishlist-tagged · Daily pipeline active

---

## KEY MESSAGE (For Final Deck)

**Title:** *W2P-30 is constrained at Step 4 — users save with intent but leave Myntra to resolve fit before buying*

**One-line:** The funnel math says uncertainty resolution is the leverage point; the discovery engine confirms it — especially **size/fit confidence** among **fit-anxious wishlisters**, without needing discounts.

---

## NORTH STAR (Recap)

**W2P-30** = % of users who purchase ≥1 wishlisted item within **30 days** of adding it.

```
W2P-30 ≈ Revisit × Wishlist→PDP × Uncertainty Resolution × Wishlist→Cart × Checkout
```

Part 2 answers: **Which step and behavior should we move first?**

---

## DISCOVERY ENGINE — WHAT WE LEARNED AT SCALE

| Signal | Full corpus (739) | Wishlist lens (113) | Interpretation |
|--------|-------------------|---------------------|----------------|
| Explicit wishlist mention | 15.3% | 100% | Most Play Store noise is post-purchase; wishlist friction is **under-voiced** |
| Silent decision gaps | 31 | ~27% of silent in wishlist context | Users stall without asking Myntra for help |
| External validation (YT / friends / IG) | 30 | Concentrated in fit/social quotes | **Decision leakage** outside the app |
| Addressable without discount | 45.7% | Higher in wishlist blockers | Constraint-compatible interventions exist |

**Killer insight (from engine):** Loud complaints = delivery & returns (122). Wishlist conversion failure = **silent** — users locate items but hesitate at **Add to Bag**, then validate on YouTube/WhatsApp.

---

## BLOCKERS MAPPED TO W2P-30 FUNNEL

| Funnel step | User behavior | Discovery evidence | Wishlist-tagged signal |
|-------------|---------------|--------------------|-------------------------|
| **Step 2 — Revisit** | Opens wishlist again | `forgot` (2), passive_saver segment (25) | Low explicit volume; UX research cites 300–400 item lists |
| **Step 3 — Re-open PDP** | Taps item from wishlist | `app_ux` (9 wishlist), decision overload from cluttered list | Share/filter gaps; scroll fatigue |
| **Step 4 — Resolve uncertainty** | Gains confidence to buy | **`size_fit` (28)**, quality (10), occasion (2), **uncertainty funnel (41)** | **Primary leak** |
| **Step 4 — Compare / decide** | Picks among saved items | **`decision_overload` (16)**, duplicate listings quotes | Heavy wishlister segment (32) |
| **Step 4 — External validation** | Leaves app to decide | **30 external validation mentions**, silent signals | YouTube try-ons, friend approval |
| **Step 5 — Add to cart** | Moves to purchase intent | `price_wait` (12 wishlist), `oos` (3) | Deal hunters (13); sale timing — secondary under no-discount constraint |
| **Step 6 — Purchase** | Completes checkout | `delivery_returns` loud (122 full) | Trust drag on repeat wishlist purchase, not first-order blocker |

### Funnel diagnosis

```
Hypothesis (Slide 1):     Step 4 is the constraint
Discovery confirmation:   Step 4 dominates wishlist-tagged blockers (size/fit + decide + external)
                          Step 2–3 are real but secondary (UX overload, forgot)
                          Step 5 price-wait matters for deal hunters — deprioritize under constraint
```

---

## SEGMENT × BLOCKER (Wishlist-tagged only)

| Segment | Top blockers | W2P-30 implication |
|---------|--------------|-------------------|
| **Fit-anxious (33)** | size_fit **27**, quality 2 | Highest intent + highest uncertainty — **primary target** |
| **Heavy wishlister (32)** | decision_overload **12**, app_ux 8 | Many saves, few purchases — needs compare/prioritize |
| **Passive saver (25)** | delivery_returns 5, quality 4 | Bookmark behavior; lower near-term conversion |
| **Deal hunter (13)** | price_wait **11** | Sale-driven; weak fit for no-discount strategy |
| **Occasion shopper (10)** | decision_overload 3, occasion_mismatch 2 | Event-deadline urgency — secondary segment |

**Segment × blocker cell with highest leverage:**  
**Fit-anxious × size/fit uncertainty** (27 of 33 fit-anxious wishlist signals cite fit)

---

## OPPORTUNITY COMPARISON (Part 2 Deliverable)

Ranked by **wishlist signal strength × addressability without discount × funnel alignment (Step 4)**

| Rank | Opportunity area | Wishlist signals | Funnel step | Top segment | Discount needed? | Priority |
|------|------------------|------------------|-------------|-------------|------------------|----------|
| **#1** | **Pre-purchase fit confidence on saved items** | size_fit **28** | Step 4 | Fit-anxious | No | **Pursue** |
| **#2** | **In-app replacement for YouTube/friend validation** | external **30**, silent **31** | Step 4 | Fit-anxious | No | **Pursue** |
| **#3** | **Compare / decide among shortlisted items** | decision_overload **16**, app_ux **9** | Step 3–4 | Heavy wishlister | No | Strong secondary |
| **#4** | Occasion suitability (“right for this event?”) | occasion **10** segment, mismatch **2** | Step 4 | Occasion shopper | No | Validate in interviews |
| **#5** | Wishlist UX (filter, sort, share) | UX research + app_ux | Step 2–3 | Heavy wishlister | No | Enables #1–#3 |
| **#6** | Price / sale timing | price_wait **12** | Step 5 | Deal hunter | Yes / partial | **Deprioritize** (constraint) |
| — | Delivery / returns | **122** loud | Post-purchase | All | No | Trust guardrail, not W2P-30 primary |

---

## REVISED PRIORITY vs SLIDE 1 HYPOTHESIS

| Slide 1 hypothesis | Discovery result | Status |
|--------------------|------------------|--------|
| #1 Step 4 uncertainty (fit, occasion) | size_fit leads wishlist blockers; 41 uncertainty funnel tags | **Confirmed** |
| #2 External validation outside app | 30 mentions; core silent signal pattern | **Confirmed** |
| #3 Decision overload | 16 wishlist-tagged; heavy wishlister segment | **Confirmed** |
| #4 Passive bookmark vs intent | passive_saver 25; needs save_reason deep-dive in interviews | **Partial — validate in Part 3** |
| #5 Revisit/recall failure | Lower signal count in corpus | **Secondary** |

---

## WHAT MUST CHANGE FOR W2P-30 TO IMPROVE (Data-Informed)

For the business metric to move **without discounts**:

1. **Step 4 ↑ — Resolve fit uncertainty on wishlisted items**  
   Users already saved = intent exists. Missing piece is confidence (size chart distrust, need for “people like me” synthesis).

2. **Step 4 ↑ — Keep validation inside Myntra**  
   Replace the YouTube → WhatsApp → maybe buy loop with an in-app **Confidence Brief** at revisit.

3. **Step 3–4 ↑ — Reduce compare paralysis**  
   Heavy wishlisters stall on 20–100+ items; structured compare/prioritize unlocks Add to Bag.

4. **Step 6 guardrail — Do not trade conversion for returns**  
   Fit advice must reduce return risk, not increase it (quality_doubt still 10 in wishlist lens).

**Leading indicators to track (Part 6 preview):**
- Wishlist → PDP click rate (Step 3)
- PDP → “confidence resolved” proxy (brief viewed / compare used) (Step 4)
- Wishlist → cart rate (Step 5)
- W2P-30 (north star)

---

## RECOMMENDED FOCUS FOR PART 3 (User Research)

| Dimension | Recommendation |
|-----------|----------------|
| **Target segment** | **Fit-anxious wishlisters** — save ethnic/western wear, 5–30 items, buy after external validation |
| **Opportunity area** | **Step 4 — Pre-purchase fit confidence** on wishlisted items |
| **Interview n** | 5–6 users matching segment |
| **Validate** | Do they still intend to buy? What stops them? What info do they seek on YouTube/friends? Would in-app fit synthesis change behavior? |
| **Do NOT over-index** | Play Store delivery complaints; deal-hunter sale-wait (constraint conflict) |

**Working problem statement (pre-interview):**  
*Fit-anxious Myntra users wishlist items they genuinely want but don’t purchase within 30 days because they don’t trust size/fit information on-platform and exit to external validation before Add to Bag.*

---

## EVIDENCE QUOTES (For Deck)

- *"I save so many kurtas on Myntra wishlist but end up buying only one after checking YouTube try-ons for sizing."* — Reddit, fit-anxious, silent  
- *"saved 5 kurtas on wishlist need confidence on size"* — Forum, gift/fit, silent  
- *"wishlisted group chat voting for 2 weeks still no purchase"* — Reddit, occasion, decision overload  
- *"Duplicate listings for same kurta set confuse me when comparing wishlisted items"* — Forum, heavy wishlister  

---

## CONNECTION TO REMAINING PARTS

| Part | What Slide 2 enables |
|------|----------------------|
| **Part 3 — Interviews** | Segment + opportunity already chosen; validate Step 4 fit hypothesis |
| **Part 4 — Problem definition** | Collapse funnel + discovery + interview into one crisp statement |
| **Part 5 — MVP** | Hypothesis: **AI Confidence Brief** on wishlist items (fit + reviews + occasion, no discount) |
| **Part 6 — Success metrics** | Leading indicators per funnel step; W2P-30 north star |
| **Part 7 — Risks** | Bad fit advice → returns; low wishlist revisit; deal hunters unaffected |

---

## SLIDE 2 — KEY MESSAGE (For Final Deck)

**Title:** *Discovery data confirms W2P-30 leaks at Step 4 — fit-anxious wishlisters need in-app confidence, not discounts*

**Bullets:**
- 739 reviews classified; wishlist friction is mostly **silent** (31 signals)
- Wishlist blockers: **size/fit (28) > decision overload (16) > price wait (12)**
- **Fit-anxious × size/fit** = highest-leverage cell for no-discount growth
- Next: **5–6 interviews** to validate before MVP

---

*Document status: Part 2 complete · Next step: Part 3 — User interviews (fit-anxious wishlisters)*
