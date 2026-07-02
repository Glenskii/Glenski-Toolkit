# MODULE 05: GOOGLE BUSINESS PROFILE OPTIMIZER
**Skill:** seo-aeo-geo-gbp v2.1.0
**Trigger:** `/seo gbp [listing-url or business-name]`

---

## PURPOSE

Deliver a GBP compliance audit and optimization plan. Covers listing completeness, category selection, photo strategy, review velocity management, Q&A seeding, Posts cadence, and full compliance with Google's April 2026 policies — including Gemini-enforced review rules and FTC $51,744/violation exposure.

---

## INPUT REQUIREMENTS

```yaml
required:
  - at_least_one_of:
    - gbp_listing_url         # Direct link to the Google Maps listing
    - business_name_location  # "Business Name, City" — will analyze publicly visible data

strongly_recommended:
  - gbp_insights_export       # GBP insights export CSV (views, search queries, actions)
  - photo_count               # Current number of photos on listing
  - review_count              # Current total review count
  - average_rating            # Current star rating
  - last_post_date            # Date of most recent GBP Post

optional:
  - competitor_gbp_urls: []   # Competitor GBP listings for benchmark
  - service_area_cities: []   # For SABs (Service Area Businesses)
```

---

## CRITICAL: APRIL 2026 POLICY COMPLIANCE

**This section must run before any recommendations.**

Google updated its GBP policies in April 2026. Key enforcement changes:

### Gemini-Powered Enforcement `[E2-REF: Google Business Profile Policy, April 2026]`

Google now uses Gemini AI to proactively detect and remove:
- Reviews that appear incentivized (gifted, discount-for-review, contest entries)
- Reviews left at kiosks or devices on business premises
- Reviews from employees or people associated with the business
- Reviews that contain the business name in unnatural patterns (signals bulk generation)
- Review responses that ask for rating changes

**Detection note:** Gemini correlates review timing patterns, device location at time of review, reviewer history, and text similarity. Detection is automated and does not require a user complaint.

### Review Acquisition — PROHIBITED METHODS `[E2-REF: April 2026 Policy Update]`

```
HARD PROHIBITIONS — any violation risks listing suspension:
✗ On-premises review kiosks or tablets
✗ Devices pre-loaded with the GBP listing for customer review
✗ Incentivized reviews (discount, gift, entry into draw for a review)
✗ Asking for a review in exchange for anything of value
✗ Review gating (filtering customers by experience before asking)
✗ Third-party review generation services
✗ Paying for reviews in any form

FTC EXPOSURE: $51,744 per violation for fake reviews or undisclosed incentives
(FTC Rule on the Use of Consumer Reviews and Testimonials, effective August 2024)
```

### Review Acquisition — COMPLIANT METHODS `[E2-REF: April 2026 Policy]`

```
COMPLIANT — these are allowed:
✓ Asking satisfied customers verbally after completing service
✓ Follow-up email asking for a review (no incentive attached, no pre-screening)
✓ Business card or thank-you note with GBP link (printed, given after service)
✓ Review link on website or in email signature (passive invitation)
✓ Responding to all reviews — Google rewards engagement
```

### Responding to Reviews — Compliance Rules

- Do NOT ask reviewers to change their rating or edit their review — this is prohibited
- Do NOT offer any incentive in your response
- Do NOT respond negatively to negative reviews in ways that could be seen as retaliatory
- DO respond to every review within 72 hours (signals active management to Google)
- DO include: business name, location signal, and a natural mention of the service category in at least 1-2 responses per week (reinforces local entity signal)

---

## GBP AUDIT EXECUTION

### SECTION 1 — LISTING COMPLETENESS AUDIT

Score each field:

```
COMPLETENESS AUDIT
────────────────────────────────────────────────────
Field                    | Status | Priority to Fix
────────────────────────────────────────────────────
Business name            | [OK/ISSUE] | [note on issue if any]
Primary category         | [OK/ISSUE] | [see category guidance]
Secondary categories     | [OK/ISSUE] | [max 9 additional]
Address                  | [OK/ISSUE] | [must match NAP exactly]
Service area             | [OK/ISSUE] | [SAB vs storefront]
Phone number             | [OK/ISSUE] | [must match NAP]
Website URL              | [OK/ISSUE] | [UTM-tagged preferred]
Hours                    | [OK/ISSUE] | [special hours set?]
Holiday hours            | [OK/ISSUE] | [set in advance]
Business description     | [OK/ISSUE] | [750 char limit — use it]
Services list            | [OK/ISSUE] | [each service named]
Products list            | [OK/ISSUE] | [if applicable]
Attributes               | [OK/ISSUE] | [all relevant checked]
Photos — exterior        | [count] | [min 3]
Photos — interior        | [count] | [min 3 if storefront]
Photos — team/people     | [count] | [min 2]
Photos — product/work    | [count] | [min 5]
Photos — cover photo     | [OK/MISSING] | [required]
Photos — logo            | [OK/MISSING] | [required]
Q&A section              | [count] | [min 5 seeded Q&As]
GBP Posts                | [last date] | [target: 2x/month]
────────────────────────────────────────────────────
COMPLETENESS SCORE: [X/20 fields complete]
```

---

### SECTION 2 — CATEGORY SELECTION

Category selection is the single highest-impact GBP optimization. Correct primary category = correct pack inclusions.

**Primary category rules:**
- Must be the most specific category that describes the core business
- Cannot be changed frequently (triggers re-verification risk)
- Determines which "local pack" searches the listing is eligible for

**Secondary categories:** Add all that legitimately apply. Each additional accurate category = additional search inclusion opportunities. Max 9 secondary.

**For Glen E. Grant Creative:**
```
Recommended primary: "Commercial Photographer"
                     or "Photographer" if "Commercial Photographer" unavailable
                     (verify current category availability in GBP interface)

Recommended secondary categories:
- "Photography Studio" (if studio sessions offered)
- "Fashion Photographer" (if available as category)
- "Headshot Photographer"
- "Portrait Studio"
- "Videographer" (if video work is offered)

DO NOT add: "Software Company", "App Developer" — these dilute the photography
local pack eligibility and confuse Google's business classification
```

**Hybrid business classification** (photography + software):
Glen runs two distinct businesses. GBP should reflect the local commercial photography business ONLY. Software products are not local services and should not appear in GBP categories. Keep GBP 100% photography-focused.

---

### SECTION 3 — BUSINESS DESCRIPTION OPTIMIZATION

**Rules** `[E2-REF: Google GBP guidelines]`:
- 750 character maximum — use all of it
- No URLs, HTML, or special characters
- No promotional/marketing language ("best", "#1", "award-winning" without specifics)
- Must describe what the business does, not just credentials
- Front-load the most important keyword phrase (first 250 characters appear in panel without expanding)

**Format:**
```
[What the business does — primary service + location] [Who it serves — specific client types]
[Years / credibility signal] [Secondary services] [Specific differentiator]
```

**Glen's recommended description:**
```
Toronto commercial photographer specializing in fashion, glamour, lifestyle,
and brand photography for businesses and agencies across Canada. Operating
since 2000, with 25+ years of editorial and commercial assignments. Work
published in Inside Fitness Magazine. Services include brand campaigns, product
photography, fitness and lifestyle shoots, and AI-powered content multiplication
for high-volume visual content needs. Packages from $799 to $2,999.
```
*(Approx 490 characters — has room to expand with current seasonal focus or recent projects)*

---

### SECTION 4 — PHOTO STRATEGY

Photos are the highest-engagement GBP element `[E1 signal from GBP insights data, E2-REF: Google GBP best practices]`.

**Minimum photo counts by type:**
- Logo: 1 (square format, minimum 250x250px)
- Cover photo: 1 (1080x608px minimum, 16:9 ratio — this is the hero image in the panel)
- Team/people photos: 2-5 (adds authenticity signal)
- Work samples: 10+ (commercial photography: show variety of work types)
- Behind-the-scenes: 2-3 (equipment, studio, on-location)

**Technical requirements:**
- Minimum: 720px on shortest side
- Maximum: 10MB per photo
- Formats: JPG, PNG (AVIF not supported by GBP — convert from AVIF before uploading)
- No watermarks on GBP photos (ironically — GBP guidelines prohibit watermarked images)
- No text overlays, logos, or borders on photos

**Photo naming:** GBP does not use file names for SEO — but alt text from the GBP interface and geotagged EXIF data do have minor signals. Geotag photos to Toronto, ON coordinates where appropriate.

**Upload cadence:** Add 1-2 new photos per week. Google rewards freshness and new photo uploads trigger notification to followers.

---

### SECTION 5 — REVIEW STRATEGY (COMPLIANCE-FIRST)

**Review velocity target:** `[E3-BEST-PRACTICE]`
- 10-20 reviews/month for a local service business is strong
- Consistency matters more than spikes (sudden burst = Gemini detection risk)
- Aim for reviews spread across 3-4 weeks, not 10 reviews in one day

**Compliant ask flow:**
```
STEP 1: Complete service delivery
STEP 2: Confirm client satisfaction verbally or in final delivery email
STEP 3: 48-72 hours after delivery — send follow-up email:
  Subject: [Project name] — thank you
  Body: [Brief thank-you note] + [single line: "If you were happy with the work,
  a Google review would mean a lot: [GBP review link]"] + [no ask for rating,
  no mention of 5 stars, no incentive]
STEP 4: Respond to every review within 72 hours
```

**Review link:** Generate a direct review link from GBP dashboard (Share > Copy link). This takes the reviewer directly to the review form, reducing drop-off.

**Review response templates** (compliant):

Positive review:
```
Thank you, [name]! Really glad the [type of shoot] came together well.
It was great working with you on [project type], and I'm pleased the
results delivered for your [brand/campaign/event]. If you need photography
again in Toronto, I'd love to work together.
– Glen E. Grant
```

Negative review:
```
Thank you for the feedback, [name]. I'm sorry the experience didn't meet
expectations. Please reach out directly at glen@glenegrant.com — I'd like
to understand what happened and see if there's anything I can do.
– Glen E. Grant
```

---

### SECTION 6 — Q&A SEEDING

GBP allows anyone to post questions. You can answer your own questions. Seed the Q&A section with the most common client questions `[E2-REF: Google GBP Q&A feature documentation]`.

**Seeding process:**
1. Log into a Google account that is NOT the GBP owner account
2. Navigate to the GBP listing on Google Maps
3. Find the Q&A section and click "Ask a question"
4. Post the question
5. Switch to the GBP owner account and answer it

**Glen's recommended seed Q&As:**
```
Q: What types of photography does Glen E. Grant Creative specialize in?
A: We specialize in commercial brand photography, fashion and glamour,
   lifestyle, fitness, and editorial work for businesses and agencies across
   Toronto and Canada. All packages include retouching and digital delivery.

Q: What are your commercial photography rates?
A: Photography packages start at $799 for portfolio-focused shoots and go
   to $2,999 for full production brand campaigns. All pricing is inclusive
   — no hidden setup fees. Current package details at glenegrant.com/pricing.

Q: How far in advance should I book?
A: For standard commercial shoots, 2-3 weeks lead time works well. For
   larger productions, 4-6 weeks gives us time to scout locations and
   coordinate talent. Priority bookings available — contact us to discuss.

Q: Do you offer AI content multiplication services?
A: Yes. We produce multiple campaign variations from a single production
   day using AI-enhanced post-production. This is particularly useful for
   brands needing high-volume visual content across digital channels.

Q: Where is your studio located?
A: We're based in Liberty Village, Toronto, with a home studio available
   for certain session types. We also shoot on location throughout the GTA
   and travel for larger productions.
```

---

### SECTION 7 — GBP POSTS STRATEGY

GBP Posts appear in the listing panel and in Google Search results for branded queries `[E2-REF: Google Business Profile Posts documentation]`.

**Post types and cadence:**
- Update posts: 2x/month minimum (general business updates, recent work highlights)
- Offer posts: only for real, compliant offers (no fake urgency, no fake discounts)
- Event posts: for actual events — set accurate dates
- Product posts: highlight specific services with photos

**Post content rules:**
- 300-1500 characters (aim for 300-500 — most gets cut off)
- Include a call-to-action button
- Photo required — use real photography, not stock
- No "call now for special deal" urgency language
- Posts expire after 7 days (Update type) — schedule recurring

**Glen's post templates:**

Recent work post:
```
[Compelling project description — 2-3 sentences describing the shoot, the brand,
and the outcome without naming the client unless they've approved it]

[Service type] | Toronto Commercial Photography
[GBP CTA: Learn more → glenegrant.com]
```

Availability post:
```
Booking [month] commercial photography sessions now. Limited dates for
[service type] available. Based in Liberty Village, serving Toronto and beyond.
[GBP CTA: Book → email or booking link]
```

---

## GBP OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GBP AUDIT & OPTIMIZATION REPORT
Business: [name]
GBP Listing: [url]
Audit Date: [date]
Data Sources: [list]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPLIANCE STATUS — APRIL 2026
[PASS/FAIL per compliance rule — any FAIL is CRITICAL priority]

COMPLETENESS SCORE: [X/20]
[completeness table]

CRITICAL FIXES (do first)
[numbered list with exact fix for each]

HIGH PRIORITY OPTIMIZATIONS
[numbered list]

CATEGORY RECOMMENDATION
[current → recommended, with rationale]

BUSINESS DESCRIPTION
[final-draft description ready to paste]

PHOTO STRATEGY
[current count per type | target count | gap]

REVIEW STRATEGY
[compliant ask flow + response templates]

Q&A SEEDS
[5 seed Q&As ready to post]

POSTS PLAN (next 30 days)
[Week 1, Week 2, Week 3, Week 4 posts with content]

RECOMMENDED NEXT MODULES
→ /seo schema [url]        add LocalBusiness + Review schema to website
→ /seo audit [url]         audit website for NAP consistency with GBP
→ /seo citations [brand]   build citation consistency across directories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
