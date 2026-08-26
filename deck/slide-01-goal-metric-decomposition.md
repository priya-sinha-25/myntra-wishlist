# Slide 1 — Millions Wishlist on Myntra, But Few Buy Within 30 Days

> **Workstream 1:** Goal & Product Mapping (Part 2 — Business Metric Decomposition)  
> **Product:** Myntra · **Team:** Growth · **Constraint:** No monetary incentives to users  
> **Deck format note:** Font size 14 when transferred to final PDF · Message-driven title · No fellow name

---

## GOAL

**Increase the percentage of users who purchase at least one item from their wishlist within 30 days of adding it.**

This is our north star metric:

### W2P-30 (Wishlist-to-Purchase within 30 Days)

**Definition:** Of all users who add at least one product to their Myntra wishlist, the percentage who complete a purchase of **at least one of those wishlisted items** within **30 calendar days** of the add action.

**Formula:**

```
W2P-30 = (Users who purchase ≥1 wishlisted item within 30d of adding it)
         ─────────────────────────────────────────────────────────────────
         (Total users who add ≥1 item to wishlist in the measurement period)
```

**Why 30 days?**
- Aligns with the project brief and Myntra’s typical fashion consideration window
- Industry benchmarks suggest wishlist-to-purchase cycles often fall in the **30–90 day** range; 30 days is a rigorous early conversion window
- Long enough for occasion/event shoppers to decide; short enough to be actionable for growth experiments

**What success looks like:**
- More high-intent saves convert without discounts or coupons
- Wishlist stops functioning primarily as a passive bookmark graveyard
- Myntra captures value from demand already expressed on-platform

---

## MARKET ANALYSIS

| Stat | Figure | Source |
|------|--------|--------|
| Myntra mobile MAU (peak) | 90M+ (Mar 2026, all-time high) | [Sensor Tower / Business Outreach ↗](https://www.businessoutreach.in/india-fashion-ecommerce-growth-2026/) |
| Myntra MAU (festive peak) | ~80M monthly active users | [Business Upturn ↗](https://businessupturn.com/brand-post/myntra-set-to-hit-200-million-annual-active-users-in-2025-50-of-the-active-customer-base-is-gen-z/) |
| Annual active users | ~200M (2025) | [Business Upturn ↗](https://businessupturn.com/brand-post/myntra-set-to-hit-200-million-annual-active-users-in-2025-50-of-the-active-customer-base-is-gen-z/) |
| Organized online fashion share | ~35–40% (early 2026) | [Business Model Canvas ↗](https://businessmodelcanvastemplate.com/blogs/competitors/myntra-competitive-landscape) |
| Fashion GMV (2023 baseline) | INR 208.75B | [Granthaalayah Research ↗](https://www.granthaalayahpublication.org/journals/granthaalayah/article/download/6175/6026) |
| Gen Z share of active base | ~50% | [Business Upturn ↗](https://businessupturn.com/brand-post/myntra-set-to-hit-200-million-annual-active-users-in-2025-50-of-the-active-customer-base-is-gen-z/) |
| App share of sales | ~80% of orders via mobile app | [Granthaalayah Research ↗](https://www.granthaalayahpublication.org/journals/granthaalayah/article/download/6175/6026) |
| India fashion e-commerce return rate | 25–40% of orders | [Unicommerce via Angadi Labs ↗](https://www.angadilabs.com/blog/india-fashion-ecommerce-benchmarks) |
| Returns driven by size/fit | 40–53% of fashion returns | [Economic Times / Return Prime ↗](https://economictimes.indiatimes.com/industry/cons-products/fashion-/-cosmetics-/-jewellery/more-than-a-third-of-fashion-and-footwear-products-get-returned-in-online-shopping-report/articleshow/112142214.cms) |
| Wishlist-to-purchase (industry benchmark) | 10–15% without automation; 15–25% with nurturing | [Shopify / Growth Suite benchmarks ↗](https://www.growthsuite.net/glossary/wishlist) |
| Users who save to purchase later | 30.4% of wishlist users (vs 49% never use wishlist) | [Bizrate Insights via Getflits ↗](https://www.getflits.com/blog/shopify-wishlist-statistics) |

**What this tells us:**
- Myntra operates at massive scale with highly engaged fashion shoppers — small W2P-30 improvements have large revenue impact
- Fashion is a **high-consideration, high-return** category; fit uncertainty is structural, not edge-case
- Wishlists capture real intent, but industry conversion from save → buy is **low unless uncertainty is resolved**
- Improving W2P-30 without discounts is viable if we address **information and confidence gaps**, not price

---

## SCENARIO TABLE — What Users Expect vs What Actually Happens

| Scenario | What users expect | What actually happens |
|----------|-------------------|------------------------|
| **Save to wishlist** | A smart holding spot for items I genuinely want to buy later | Wishlist becomes a graveyard of 20–100+ items; only a small fraction ever gets purchased |
| **Revisit wishlist** | Easy to remember why I saved each item and act on it | Items blur together; user forgets context (occasion, size concern, why they liked it) |
| **Decide whether to buy** | Enough information to feel confident purchasing | Size chart + scattered reviews still leave fit, styling, and occasion doubts unresolved |
| **Compare saved items** | Help picking the best option from shortlisted products | No structured compare flow; mental overload leads to no decision |
| **Wait for the right moment** | Buy when price, occasion, or availability aligns | Item goes out of stock, sale ends, event date passes, or user loses interest |
| **Check before committing** | Trust that the product will work for me | User leaves Myntra → YouTube try-ons, Instagram, friends, AJIO/Nykaa to validate |

---

## WHY FOCUS ON WISHLIST? (Business Case)

1. **Wishlist = explicit purchase intent signal**  
   Unlike passive browsing, saving an item is a deliberate act — the user has identified something they like but stopped short of buying.

2. **High volume, low conversion = leaky bucket**  
   Millions of users wishlist; industry data suggests only **10–25%** of saved items convert to purchase. Myntra likely leaves significant high-intent demand on the table.

3. **Growth without acquisition cost**  
   Converting existing wishlist intent is cheaper than acquiring new users — this is monetization of demand already on the platform.

4. **Constraint-compatible**  
   The brief prohibits monetary incentives. Wishlist abandonment is often driven by **fit, occasion, quality, and decision uncertainty** — addressable through product and AI, not discounts.

5. **Strategic moment for Myntra**  
   Myntra is investing in AI (MyFashionGPT, virtual try-on, personalization). Wishlist is an under-leveraged surface where AI can resolve pre-purchase uncertainty at the moment of revisit.

6. **Competitive gap**  
   Myntra, AJIO, and Nykaa all offer save/wishlist — none fully solve “help me decide if I should buy what I already saved.”

---

## W2P-30 METRIC DECOMPOSITION

### The Wishlist Conversion Funnel

Every wishlist add is a potential purchase. W2P-30 improves only if one or more of these behavioral steps improve:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1          STEP 2           STEP 3          STEP 4         STEP 5      │
│  ADD TO     →    REVISIT     →    RE-OPEN    →    RESOLVE    →   ADD TO  →  │
│  WISHLIST        WISHLIST         PDP             UNCERTAINTY      CART       │
│  (intent         (within 30d)     (from           (fit, occasion,             │
│   captured)                       wishlist)        quality, etc.)             │
│                                                                               │
│                                                          STEP 6               │
│                                                     COMPLETE PURCHASE         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Breakdown

| Step | User behavior | Metric (conceptual) | If this fails… |
|------|---------------|---------------------|----------------|
| **1 — Add to wishlist** | User saves item | Wishlist add rate | Top of funnel (not our primary optimization focus) |
| **2 — Revisit wishlist** | User opens wishlist again within 30 days | Wishlist revisit rate (7d, 30d) | Item forgotten; intent decays |
| **3 — Re-engage with item** | User taps through to product detail page from wishlist | Wishlist → PDP click rate | Saved item never re-evaluated |
| **4 — Resolve uncertainty** | User gains enough confidence on fit, occasion, quality, value | Uncertainty resolution rate | User stuck in “maybe”; exits app to validate elsewhere |
| **5 — Add to cart** | User moves item from consideration to intent | Wishlist → cart rate | High interest but no action |
| **6 — Complete purchase** | User checks out | Cart → purchase rate | Last-mile drop (payment, delivery, distraction) |

### Behavioral Equation

```
W2P-30 ≈ Revisit Rate
       × Re-engagement Rate (Wishlist → PDP)
       × Uncertainty Resolution Rate
       × Wishlist → Cart Rate
       × Checkout Conversion Rate
```

**How to use this equation:**
- If users **don’t revisit** → problem is recall/timing (Workstream 2 may show “forgot” / passive bookmark patterns)
- If users **revisit but don’t open PDP** → problem is wishlist UX overload or low urgency
- If users **open PDP but don’t buy** → problem is unresolved uncertainty (likely #1 for fashion — fit, occasion, quality)
- If users **add to cart but don’t buy** → checkout friction, price timing, or last-minute doubt

Our discovery engine (Workstream 2) will tag each user pain point to a funnel step so we know **which step to target**.

---

## PRODUCT OUTCOMES THAT INFLUENCE W2P-30

| Product outcome | Funnel step(s) affected | Example interventions (non-discount) |
|-----------------|-------------------------|--------------------------------------|
| Users remember and return to saved items | Step 2 | Contextual revisit prompts, occasion reminders |
| Users re-click wishlisted items | Step 3 | Prioritized wishlist, “needs decision” sorting |
| Users resolve fit/occasion/quality doubt | Step 4 | AI confidence brief, aggregated “people like you” reviews |
| Users decide among saved items | Step 4 | Compare flow, Buy / Wait / Compare recommendation |
| Users distinguish intent vs bookmark | Step 2–4 | “Save to buy” vs “Save to browse” intent capture |
| Users stay inside Myntra to decide | Step 4 | Replace YouTube/friend validation with in-app guidance |
| Users move to cart with confidence | Step 5 | Post-resolution CTA, styling suggestions for occasion |

---

## MYNTRA WISHLIST JOURNEY TODAY (As-Is)

```
Discover product          Save to wishlist           Time passes (days/weeks)
      │                         │                              │
      ▼                         ▼                              ▼
 Browse feed/          Explicit intent            Wishlist grows; context fades
 search/PDP            captured on-platform        (why saved? for what occasion?)
      │                         │                              │
      │                         │                              ▼
      │                         │                    ┌─────────────────────┐
      │                         │                    │  User paths:         │
      │                         │                    │  • Forgets item      │
      │                         │                    │  • Revisits but      │
      │                         │                    │    can't decide      │
      │                         │                    │  • Leaves app        │
      │                         │                    │    (YouTube, friends)│
      │                         │                    │  • Waits for sale    │
      │                         │                    │  • Item goes OOS     │
      │                         │                    └──────────┬──────────┘
      │                         │                               │
      │                         │         ┌─────────────────────┼─────────────────────┐
      │                         │         ▼                     ▼                     ▼
      │                         │    Purchase              No purchase           Buys elsewhere
      │                         │    (W2P-30 ✓)            (W2P-30 ✗)           (AJIO/competitor)
      │                         │
      └─────────────────────────┴── Myntra has the intent signal but often loses the decision moment
```

**Key insight:** The wishlist captures **intent** early, but Myntra often loses the **decision** later — especially when users need fit, styling, or occasion validation.

---

## WHY THIS PROBLEM EXISTS (Working Hypothesis — To Be Validated)

*This is our starting hypothesis before AI discovery and interviews. Workstreams 2–4 will confirm or revise.*

1. **Fashion purchases require confidence users don’t get from a save action alone**  
   Size/fit drives 40%+ of returns; if users fear wrong fit, they save but don’t buy.

2. **Wishlist is used as bookmark, not commit-to-buy**  
   ~49% of shoppers never use wishlists; among those who do, many save without strong purchase intent (compare later, mood board, gift ideas).

3. **No decision support at revisit moment**  
   Myntra shows saved items but doesn’t help answer: “Should I buy this *now* for *this occasion* — and will it fit me?”

4. **Users externalize validation**  
   When uncertain, users go to YouTube try-ons, Instagram, friends, or competitor apps — leakage from Myntra’s funnel at Step 4.

5. **Decision overload at scale**  
   Users accumulate dozens of saved items; without compare/prioritize tools, they buy nothing.

6. **Algorithm/UX optimizes for discovery and checkout, not wishlist resolution**  
   Myntra invests in finding products and completing orders — the middle stage (“I already like this, help me decide”) is underserved.

---

## WHICH BEHAVIORS MATTER MOST (Initial Hypothesis for Discovery)

Based on market data and fashion category dynamics, we hypothesize W2P-30 is most constrained at **Step 4 — Resolve uncertainty**, specifically:

| Priority | Behavior gap | Rationale |
|----------|--------------|-----------|
| **#1 (hypothesis)** | Uncertainty resolution — fit, occasion, styling | Size/fit = 40–53% of returns; fashion is try-before-you-buy offline; wishlist users likely stall here |
| **#2** | External validation outside app | Users don’t trust in-app info alone; leave to YouTube/friends before buying |
| **#3** | Decision overload across many saved items | Large wishlists → paralysis → zero purchases |
| **#4** | Passive bookmarking vs genuine intent | Not all wishlist adds are equal; treating them the same dilutes W2P-30 |
| **#5** | Revisit/recall failure | Items forgotten before uncertainty can even be addressed |

**Workstream 2 (AI Discovery Engine) will quantify these** — e.g., “38% of wishlist-related feedback cites size/fit” — and identify the target segment where the gap is largest.

---

## COMPETITOR CONTEXT (Wishlist & Pre-Purchase Decision)

| Platform | Wishlist / save behavior | Gap |
|----------|--------------------------|-----|
| **Myntra** | Save, price drop alerts, reviews, size chart | No per-item confidence/decision layer on revisit |
| **AJIO** | Save, stylist/chat features | Stylist is human/async; not scaled on every wishlist item |
| **Nykaa Fashion** | Save, reviews, shade/fit guides | Beauty-first; fashion wishlist decision support limited |
| **Amazon Fashion** | Save, compare (limited) | Generic UX; weak occasion/fit reasoning for fashion |

**Opportunity:** Own the “wishlist decision moment” — help users buy what they already said they want, without discounts.

---

## WHAT NEEDS TO CHANGE FOR W2P-30 TO IMPROVE

For the business metric to move meaningfully:

1. **More users must revisit** their wishlist while intent is still warm (Step 2 ↑)
2. **More revisits must lead to PDP re-engagement** (Step 3 ↑)
3. **More PDP sessions must resolve key uncertainty** — especially fit and occasion (Step 4 ↑) ← *likely highest leverage*
4. **More resolved sessions must convert to cart** (Step 5 ↑)
5. **Checkout must remain stable** — we must not increase returns via bad confidence advice (Step 6 guardrail)

**Non-discount levers that can move these steps:**
- AI-powered confidence/decision briefs on wishlisted items
- “People like you” fit synthesis from reviews
- Occasion suitability scoring
- Buy / Wait / Compare framework
- Wishlist prioritization (“buy this first for your event”)
- In-app replacement for YouTube/friend validation

---

## CONNECTION TO NEXT WORKSTREAMS

| Workstream | How Slide 1 connects |
|------------|----------------------|
| **WS2 — AI Discovery Engine** | Tag each feedback theme to funnel Step 1–6; quantify which step leaks most |
| **WS3 — Insight & Hypothesis** | Rank blockers by %; pick segment × blocker cell with highest intent |
| **WS4 — User Research** | Validate whether Step 4 (uncertainty) or another step dominates for Myntra users |
| **WS5 — Problem Framing** | Collapse funnel + discovery + interviews into one problem statement |
| **WS6 — MVP** | Build intervention targeting the weakest funnel step (hypothesis: Step 4) |
| **WS8 — Metrics** | Define leading indicators per funnel step; W2P-30 as north star |

---

## SLIDE 1 — KEY MESSAGE (For Final Deck)

**Title:** *Millions wishlist on Myntra, but W2P-30 stays low because users revisit without resolving fit and occasion uncertainty*

**One-line summary:** Wishlist captures high-intent demand; the conversion leak is primarily a **decision confidence** problem at revisit — not a lack of interest and not solvable only through discounts.

---

## SOURCES (All links for deck hyperlinks)

- [Sensor Tower / Business Outreach — Myntra 90M MAU, Mar 2026](https://www.businessoutreach.in/india-fashion-ecommerce-growth-2026/)
- [Business Upturn — 200M AAU, 80M MAU festive peak, Gen Z 50%](https://businessupturn.com/brand-post/myntra-set-to-hit-200-million-annual-active-users-in-2025-50-of-the-active-customer-base-is-gen-z/)
- [Business Model Canvas — Myntra competitive landscape](https://businessmodelcanvastemplate.com/blogs/competitors/myntra-competitive-landscape)
- [Granthaalayah — Myntra GMV, MAU, market share](https://www.granthaalayahpublication.org/journals/granthaalayah/article/download/6175/6026)
- [Angadi Labs — India fashion return benchmarks 2026](https://www.angadilabs.com/blog/india-fashion-ecommerce-benchmarks)
- [Economic Times / Return Prime — 30–35% fashion returns, 40%+ size issues](https://economictimes.indiatimes.com/industry/cons-products/fashion-/-cosmetics-/-jewellery/more-than-a-third-of-fashion-and-footwear-products-get-returned-in-online-shopping-report/articleshow/112142214.cms)
- [Growth Suite — Wishlist to purchase 15–25% benchmark](https://www.growthsuite.net/glossary/wishlist)
- [Getflits / Bizrate — 30.4% save to purchase later](https://www.getflits.com/blog/shopify-wishlist-statistics)

---

*Document status: Workstream 1 complete · Next step: Workstream 2 — AI Discovery Engine*
