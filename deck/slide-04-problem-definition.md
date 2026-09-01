# Slide 4 — Problem Definition (Problem Framing Canvas)

> **Part 4:** Problem Definition  
> **Pattern:** Reference deck — Problem Framing Canvas + triangulation (discovery + survey)  
> **Inputs:** Secondary — AI engine (739 reviews) · Primary — survey (n=18)

---

## KEY MESSAGE (For Final Deck)

**Title:** *This is not a price problem — it's a silent decision failure on saved items*

**One-line:** Users wishlist to compare, then leave Myntra because the app doesn't help them trust fit or pick among saves before Add to Bag.

---

## PROBLEM FRAMING CANVAS

*(Copy this as a 2×3 grid on the slide — same structure as reference deck)*

### WHAT IS THE TRUE PROBLEM?

Myntra users **wishlist items they intend to buy** but **do not purchase within 30 days** because **Step 4 fails silently** — the app does not help them **resolve fit/review uncertainty** or **choose among similar saved items** before Add to Bag.

They **exit to YouTube, friends, offline stores, or competitor apps** to finish deciding — or **park items for a sale** without ever confirming the item is right.

**Reframe (critical — say this explicitly on slide):**

| This is NOT… | This IS… |
|--------------|----------|
| A discount / coupon problem | A **pre-purchase confidence** problem at revisit |
| Loud Play Store complaints (delivery 122) | **Silent** wishlist stall (31 signals in corpus) |
| "Users don't want the item" | Users **saved to compare** — intent exists, decision doesn't close |
| A recommendation algorithm problem | A **decision-support + transparency** problem on saved items |

**Redefined problem statement (use verbatim):**

> When a Myntra user revisits a wishlisted item they liked, the app has **no mechanism to help them trust fit/reviews or pick among similar saves** — so they **validate outside Myntra** or **wait indefinitely**, and W2P-30 never moves.

---

### WHO IS FACING THIS PROBLEM?

**Fit-anxious wishlister** — primary segment

Defined by **5 behavioural signals** (match ≥4/6):

1. Uses wishlist often or sometimes  
2. Has **3+ items** saved now  
3. Wishlisted something liked but **didn't buy** (last 3 months)  
4. Cites **size/fit, fabric, or can't decide** among saves  
5. **Checks outside Myntra** before buying  

**Secondary:** Heavy wishlister in compare mode — 11–100+ items, multiple similar saves for one occasion (discovery: 32; survey Q15: often/sometimes).

**Deprioritize:** Deal hunter — waits for EORS only (discovery: 13; survey: 47% cite price but often coexists with uncertainty).

| Source | Segment proof |
|--------|---------------|
| Discovery | Fit-anxious **33** of 113 wishlist-tagged; **27/33** cite size/fit |
| Survey | **74%** (14/18) score ≥4/6 on fit-anxious criteria |

**Persona sketch (for deck):**  
*Priya, 26 — saves 15 kurtas for a wedding, checks Instagram try-ons, still hasn't bought. Pays full price if confident; won't buy blind.*

---

### HOW DO WE KNOW IT'S A REAL PROBLEM?

**Triangulation — three layers (like reference deck):**

| Layer | Evidence |
|-------|----------|
| **AI discovery (739 reviews)** | Wishlist blockers: size/fit **28**, decide overload **16**, external validation **30**, silent gaps **31**. Play Store noise = delivery (**122**) — **not** wishlist conversion. |
| **Survey (n=18)** | **74%** fit-anxious profile · **84%** check outside app · **37%** can't decide · **79%** positive on Confidence Brief concept |
| **Open-text (survey as qual)** | Hoodie story: offline size check → OOS → delivery fail → **still wishlisted** — decision never closed in-app |

**Reconciled insight (discovery vs survey):**

- Discovery ranks **size/fit #1** in wishlist corpus; survey checkboxes rank **price (47%)** first.  
- **Both true:** users say "waiting for sale" but **84% still leave the app** — price masks unresolved uncertainty.  
- Under **no-discount constraint**, the lever is **in-app decision**, not coupons.

**Killer insight (mirror reference deck tone):**

> Reviews scream delivery and returns. Wishlist failure is **silent** — users save, hesitate, and leave to YouTube/WhatsApp without telling Myntra.

---

### VALUE FOR USERS

- **Confident purchase** from saves without guessing on size/fit/fabric  
- **Compare and pick** among similar wishlist items in one place  
- **Discover without leaving** — replaces YouTube, friends, offline checks  
- **Buy when ready** — not forced by discount, enabled by trust  

---

### VALUE FOR MYNTRA (BUSINESS)

- **W2P-30 ↑** — north star: % buying ≥1 wishlist item within 30 days  
- **Leakage reduction** — **84%** currently validate off-app; every decision recovered = engagement + conversion inside Myntra  
- **No-discount growth** — **45.7%** of discovery signals addressable without coupons  
- **AI positioning** — Confidence Brief = defensible AI layer on existing review/catalog data  
- **Differentiation** — AJIO/Amazon have wishlists; none offer **AI decision brief on saves**  

---

### WHY SOLVE THIS NOW?

1. **Discovery confirmed Step 4** as funnel leak — size/fit + external validation dominate wishlist-tagged data  
2. **Survey validated segment** at human scale (74% fit-anxious) without needing 6 interviews  
3. **Silent problem widening** — as wishlists grow (300–400 items cited in UX research), compare paralysis worsens  
4. **Constraint-compatible** — price levers excluded; confidence levers rank #1–#3 in discovery opportunity table  
5. **Concept tested** — 79% survey positive on Confidence Brief before build  

---

## ROOT CAUSE (5-WHY — optional compact slide)

| Level | Why |
|-------|-----|
| **Surface** | Users don't buy wishlisted items within 30 days |
| **Why?** | They don't trust fit/review signal enough to Add to Bag |
| **Why?** | Myntra shows size chart + reviews but not **synthesized confidence** for *their* body and *their* compare set |
| **Why?** | Users wishlist to **compare options** — app treats wishlist as storage, not decision workspace |
| **Root** | **No decision-support mechanism on saved items** — validation happens off-app (YT 30 signals; survey 84%) |

**Self-reinforcing loop:**

```
Save to compare → Revisit → Uncertainty → Leave app to validate
      ↑                                              ↓
      └──────── Never Add to Bag ← Still not confident
```

---

## WHAT EXISTING MYNTRA / COMPETITOR SOLUTIONS DID AND DIDN'T DO

*(Reference deck table — put on slide 4 or 5)*

| Solution | Did | Didn't |
|----------|-----|--------|
| **Wishlist (heart/save)** | Captures intent | No help deciding among saves or trusting fit |
| **Size chart + reviews on PDP** | Raw data exists | No synthesis; user still leaves to YT/friends |
| **Sales / EORS** | Moves price-sensitive buyers | Doesn't resolve fit/decide; excluded by constraint |
| **Compare on AJIO / Amazon** | Cross-app price check | Pulls user **out** of Myntra; no fit confidence |
| **Myntra share with friends** | Social validation | Async, off-platform — not scalable in-app brief |

**Gap:** No surface gives **one trusted answer** on a saved item — *"Is this the right fit and the right pick for me?"*

---

## SLIDE 4 BULLETS (Copy-paste)

- **True problem:** Silent Step 4 failure — not price, not delivery  
- **Who:** Fit-anxious wishlister (74% survey; 33 discovery segment)  
- **Proof:** 739 reviews + n=18 survey + 84% off-app validation  
- **Reframe:** Users save to compare; app doesn't help them decide  
- **Value:** W2P-30 ↑ without discounts · keep decision inside Myntra  

---

*Next: `slide-05-mvp-spec.md` — 3 solutions, 1 choice (ICE)*
