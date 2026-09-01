"""One-off survey analysis for Part 3."""
import csv
from collections import Counter
from pathlib import Path

path = Path(__file__).parent / "data" / "Untitled form.csv"
with path.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rows = [r for r in rows if any((v or "").strip() for v in r.values())]


def col(r, *prefixes):
    for k, v in r.items():
        for p in prefixes:
            if k.strip().startswith(p):
                return (v or "").strip()
    return ""


def score_row(r):
    pts = 0
    details = []
    q2 = col(r, "Do you use the wishlist")
    if "often" in q2.lower() or "sometimes" in q2.lower():
        pts += 1
        details.append("wishlist_use")
    q3 = col(r, "Roughly how many items")
    if q3 not in ("0", "1–2", "1-2", ""):
        pts += 1
        details.append("3plus_items")
    q4 = col(r, "In the last 3 months")
    if q4.lower() == "yes":
        pts += 1
        details.append("didnt_buy")
    blockers = col(r, "What stops you")
    if "size / fit" in blockers.lower() or "how it will look" in blockers.lower():
        pts += 1
        details.append("fit_blocker")
    ext = col(r, "Before buying something")
    if ext and "No — I decide only using Myntra" not in ext:
        pts += 1
        details.append("external_validation")
    trust = col(r, "How much do you agree")
    if any(x in trust for x in ("Neutral", "disagree")):
        pts += 1
        details.append("low_trust")
    return pts, details


blockers_all = []
concept = Counter()
brief = Counter()
ext_only = 0
fit_anxious = 0

for r in rows:
    pts, _ = score_row(r)
    if pts >= 4:
        fit_anxious += 1
    b = col(r, "What stops you")
    for part in b.split(";"):
        if part.strip():
            blockers_all.append(part.strip())
    concept[col(r, "If this existed")] += 1
    brief[col(r, "Which part of the Confidence Brief")] += 1
    ext = col(r, "Before buying something")
    if "No — I decide only using Myntra" in ext:
        ext_only += 1

n = len(rows)
bc = Counter(blockers_all)
fit_rows = sum(1 for r in rows if "size / fit" in col(r, "What stops you").lower())
positive = sum(v for k, v in concept.items() if "more likely" in k.lower())

print(f"n={n}")
print(f"fit_anxious_score>=4: {fit_anxious} ({fit_anxious/n*100:.0f}%)")
print(f"size_fit_blocker: {fit_rows} ({fit_rows/n*100:.0f}%)")
print(f"external_validation: {n-ext_only} ({(n-ext_only)/n*100:.0f}%)")
print(f"concept_positive: {positive} ({positive/n*100:.0f}%)")
print("blockers:", bc.most_common())
print("concept:", dict(concept))
print("brief:", dict(brief))
