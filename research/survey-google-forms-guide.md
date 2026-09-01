# Google Forms Setup Guide — Myntra Wishlist Survey



## Option A — Auto-build (recommended, ~2 min)



Use the Apps Script in **`create-google-form.gs`** to generate the full **21-question** form with sections, screener branching, and validation.



1. Open [script.google.com](https://script.google.com) → **New project**

2. Delete the default `function myFunction()` code

3. Copy the entire contents of `research/create-google-form.gs` and paste into the editor

4. Click **Run** (▶) → select **`createMyntraWishlistSurvey`** → **Authorize** when Google prompts you

5. Open **View → Executions** or **View → Logs** — copy the **Share this link** URL

6. Optional: open the **Edit form here** URL to add Myntra purple theme (#FF3F6C) under Customize



The script sets up:

- All 21 questions in 7 sections

- Screener branching (Q1 Never, Q2 Never, Q4 No → end survey)

- Q12 max 2 selections

- Likert scale for Q13

- Confidence Brief concept block before Q16

- Anonymous responses (no email collection)



Save the published URL in your deck and share via WhatsApp / Instagram.



---



## Option B — Manual setup (~10 min)



1. Go to [forms.google.com](https://forms.google.com) → **Blank form**

2. Title: **How do you decide whether to buy items on your Myntra wishlist?**

3. Paste description from `wishlist-user-survey.md` Section intro

4. Settings ⚙️:

   - Collect **email addresses** — OFF (anonymous)

   - Limit to **1 response** — ON (optional)

   - **Make this a quiz** — OFF

5. Add questions below in order (question types noted)



---



## Question type mapping



| Q# | Type in Google Forms | Notes |

|----|----------------------|-------|

| Q1 | Multiple choice | Never → Thank you end |

| Q2 | Multiple choice | Never use wishlist → Thank you end |

| Q3 | Multiple choice | |

| Q4 | Multiple choice | No → Thank you end (optional) |

| Q5 | Multiple choice | |

| Q6 | Checkboxes | |

| Q7 | Multiple choice | |

| Q8–Q11 | Multiple choice | |

| Q12 | Checkboxes | Max 2 selections |

| Q13 | Linear scale 1–5 | Strongly disagree → Strongly agree |

| Q14 | Checkboxes | |

| Q15 | Multiple choice | |

| Q16–Q18 | Multiple choice | Concept description before Q16; Q18 = AI openness |

| Q19 | Paragraph | Required |

| Q20 | Short answer | Required |

| Q21 | Multiple choice + short answer if Yes | |



---



## Section breaks (recommended)



| Section | Questions |

|---------|-----------|

| Screener | Q1–Q4 |

| About you | Q5–Q7 |

| Wishlist behavior | Q8–Q11 |

| Blockers | Q12–Q13 |

| Before you buy | Q14–Q15 |

| Concept test | Q16–Q18 |

| Open feedback & follow-up | Q19–Q21 |



---



## Concept block (paste before Q16)



**Section title:** New feature idea — Confidence Brief



**Description:**

> Imagine this: On each wishlisted item, Myntra uses **AI** to show a short **Confidence Brief** — your recommended size, what buyers with a similar body type said about fit, and whether it works for the occasion you had in mind. **No extra discount** — just help deciding.



---



## After collecting responses



1. **Responses** tab → **Download CSV (.csv)**

2. Save as `research/data/survey-responses.csv`

3. Score fit-anxious segment using rules in `wishlist-user-survey.md`

4. Pick 5–6 from Q21 opt-in + high fit-anxious score for interviews

5. Use quotes from Q19–Q20 in deck



---



## Share link text (copy for WhatsApp / Instagram)



> 📋 7-min anonymous survey on Myntra wishlist habits — how you decide what to buy (or not buy) from saved items. No sales pitch, no discounts. Would really help if you've used Myntra wishlist!  

> [paste Google Form link]



---



## For deck / submission



- Hyperlink survey URL in slide 3 or slide 4

- Report: "n = __ responses, __% fit-anxious segment, __% cite size/fit blocker"

- Note: Survey supplements 5–6 interviews (project requirement)

