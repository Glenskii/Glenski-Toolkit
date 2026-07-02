# MODULE 07: SEO CONTENT BRIEF
**Skill:** seo-aeo-geo-gbp v2.1.0
**Trigger:** `/seo brief [topic + url]`

---

## PURPOSE

Produce a complete, actionable SEO content brief for a new or existing page. The brief defines the target keyword, intent, structure, AEO requirements, word count, internal linking plan, and schema type. The writer (or AI writer) follows this brief and produces content that ranks and answers.

This module does NOT write the content itself. It specifies exactly what the content must contain.

---

## INPUT REQUIREMENTS

```yaml
required:
  - topic_or_url          # Topic for new content, or URL of existing page to improve

strongly_recommended:
  - primary_keyword: ""   # Target keyword for the page
                          # If not provided: module will recommend based on topic
  - at_least_one_of:
    - keyword_research    # Output from module 02 for this topic
    - gsc_data            # GSC queries landing on this URL (for existing pages)
    - competitor_pages: []# Competitor pages ranking for this topic

optional:
  - page_type: ""         # "service" | "product" | "blog" | "landing" | "about" | "faq"
  - word_count_target: 0  # Override the module's recommendation
  - aeo_queries: []       # Specific questions to answer (from module 04 or manual input)
  - audience: ""          # Who is reading this (informs tone, depth, jargon level)
```

---

## CONTENT BRIEF EXECUTION

### STEP 1 — PAGE CLASSIFICATION AND INTENT

Classify the page and its primary intent before any brief work:

```
PAGE CLASSIFICATION
────────────────────────────────────────────────────
Page type:           [service | product | blog | landing | about | faq]
Primary intent:      [TXN | COM | INFO | LOCAL | NAV]
Secondary intent:    [if dual-intent]
Content goal:        [rank for keyword X | convert visitors to [action] | answer [query]]
Target audience:     [who is reading this and why]
────────────────────────────────────────────────────
```

**Content goal must be specific.** "Rank for 'Toronto commercial photographer' and convert visitors to book a discovery call" is a content goal. "Improve SEO" is not.

---

### STEP 2 — KEYWORD TARGETING

```
KEYWORD BRIEF
────────────────────────────────────────────────────
Primary keyword:         [the one term this page owns]
Monthly volume:          [H/M/L or specific number if known] [E1 if data, E3 if estimated]
Keyword difficulty:      [H/M/L] [E1 if data, E3 if estimated]
Current rank:            [position or NR] [E1 if GSC, E3 if not known]
Target rank:             [position target]
Secondary keywords:      [list — these appear naturally throughout, never forced]
LSI/semantic terms:      [related terms and phrases to include naturally]
Keyword in title:        [YES — exact match or natural variant?]
Keyword in H1:           [YES — exact match or close variant?]
Keyword in URL:          [current URL | recommended URL if new page]
Keyword in first 100 words: [YES — required]
────────────────────────────────────────────────────
```

**Secondary keywords note:** Secondary keywords should appear once each, naturally. They are not additional optimization targets — they signal topical relevance to Google's semantic understanding.

---

### STEP 3 — SERP COMPETITIVE ANALYSIS FOR THIS KEYWORD

Look at what's currently ranking for the primary keyword:

```
SERP SNAPSHOT [E1 if pulled from live SERP, E2 if from tool data]
────────────────────────────────────────────────────
Position 1: [URL] — [title] — [word count if known] — [schema types]
Position 2: [URL] — [title] — [word count if known] — [schema types]
Position 3: [URL] — [title] — [word count if known] — [schema types]
────────────────────────────────────────────────────
SERP features present: [Featured snippet | PAA | Local pack | Shopping | Video]
Content format winning: [long-form | short answer | list | table | video]
Average word count (top 3): [N words]
Content gap vs top rankers: [what they cover that target page should also cover]
Differentiation opportunity: [what target page can do that they don't]
────────────────────────────────────────────────────
```

**Word count target:** Match or modestly exceed the average of top 3 results. Not "more content = better" — topically complete content = better. 600 well-structured words can outrank 2,000 padded words.

---

### STEP 4 — PAGE STRUCTURE

Define the exact structure of the page:

```
PAGE STRUCTURE BRIEF
────────────────────────────────────────────────────
URL:           [final recommended URL — kebab-case, keyword in URL]
Title tag:     "[Primary keyword | Brand name]" ([X] chars)
Meta desc:     "[150 chars — keyword + action + differentiator]"
H1:            "[Exact H1 — keyword present, conversational, not stuffed]"
────────────────────────────────────────────────────
CONTENT SECTIONS:
[Section 1]
H2: "[heading — keyword variant]"
Purpose: [what this section answers / establishes]
Content type: [paragraph | list | table | FAQ]
Word count target: [N words]
AEO opportunity: [YES: query + answer block needed | NO]
Schema type: [if applicable]

[Section 2]
H2: "[heading]"
[...repeat for each section...]

[Final section — CTA]
H2: "[optional heading for CTA section]"
Purpose: conversion — [specific action]
CTA text: "[exact button/link text — verb first]"
CTA destination: "[URL]"
────────────────────────────────────────────────────
```

---

### STEP 5 — AEO REQUIREMENTS

List every question this page must answer, with target format:

```
AEO REQUIREMENTS FOR THIS PAGE
────────────────────────────────────────────────────
Primary question: "[the exact query this page answers]"
Answer placement: [first 100 words of body | dedicated FAQ section | H2 section]
Answer format: [40-60 word paragraph | ordered list | table]
Schema: [FAQPage | HowTo | Speakable]

Additional questions to answer:
- "[question 2]" → [format] → [placement]
- "[question 3]" → [format] → [placement]
- "[question 4]" → [format] → [placement]
────────────────────────────────────────────────────
```

**Speakable schema note:** Add Speakable schema for any section that is a direct, spoken-friendly answer (good for voice search and Google Assistant responses).

---

### STEP 6 — INTERNAL LINKING PLAN

```
INTERNAL LINKING BRIEF
────────────────────────────────────────────────────
Pages that should LINK TO this page:
- [URL] → anchor text: "[descriptive anchor]" → reason: [topical relevance]
- [URL] → anchor text: "[descriptive anchor]" → reason: [keyword support]

Pages this page should LINK OUT TO:
- [URL] → anchor text: "[descriptive anchor]" → reason: [supporting content]
- [URL] → anchor text: "[descriptive anchor]" → reason: [CTA destination]
────────────────────────────────────────────────────
```

**Internal linking rules:**
- Anchor text must be descriptive — not "click here" or "read more"
- Homepage should link to top-priority service pages
- Service pages link to related service pages and pricing
- Blog posts link to the relevant service page they support

---

### STEP 7 — E-E-A-T REQUIREMENTS

Google's quality rater guidelines emphasize Experience, Expertise, Authoritativeness, Trustworthiness `[E2-REF: Google's Quality Rater Guidelines, 2024]`.

For this page, specify which E-E-A-T signals must be present:

```
E-E-A-T CHECKLIST FOR THIS PAGE
────────────────────────────────────────────────────
Experience signals needed:
□ First-person examples of doing the work described
□ Specific client outcomes (without inventing data)
□ Process descriptions that only come from doing it

Expertise signals needed:
□ Author name + credentials visible on page
□ Years of experience stated
□ Specific technical or industry knowledge demonstrated

Authoritativeness signals needed:
□ Publication credits or press mentions referenced
□ Awards or certifications mentioned (with dates)
□ Industry association memberships referenced

Trustworthiness signals needed:
□ Contact information visible on page (or in site-wide header)
□ Privacy/terms links in footer (for any form or data collection)
□ Real testimonials or case study references (no invented quotes)
□ Schema markup implemented (LocalBusiness, Person, or Product)
────────────────────────────────────────────────────
```

---

### STEP 8 — COPY RULES (PAGE-SPECIFIC)

Apply the relevant PRODUCT.md copy rules for the site being written for. Then add page-specific rules:

```
COPY RULES FOR THIS PAGE
────────────────────────────────────────────────────
Voice/tone: [specific to audience and page type]
Forbidden: [terms specific to this page that must not appear]
Required: [specific claims that must be included — with exact phrasing if critical]
CTA language: "[exact CTA copy]" — must be a verb
Price mention: [YES/NO — if yes, exact price range to state]
Location mention: [YES — "Toronto" appears at minimum once in first 200 words]
────────────────────────────────────────────────────
```

---

### STEP 9 — SCHEMA AND META BRIEF

```
SCHEMA BRIEF
────────────────────────────────────────────────────
Required schema types: [list — route to /seo schema for full generation]
Priority: [schema type that unlocks SERP feature, e.g., FAQPage for PAA]
────────────────────────────────────────────────────

SOCIAL META BRIEF (OpenGraph + Twitter Card)
og:title:       "[same as title tag — or slightly longer/more conversational]"
og:description: "[same as meta description, or more compelling for social share]"
og:image:       "[1200x630px — URL of page-specific image]"
og:type:        "website" | "article" | "product"
twitter:card:   "summary_large_image"
────────────────────────────────────────────────────
```

---

## CONTENT BRIEF OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTENT BRIEF
Topic: [topic]
Page type: [type]
Primary keyword: [keyword]
Target URL: [url]
Date: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAGE META
Title:       [final tag — char count]
Meta desc:   [final description — char count]
URL:         [recommended URL]
H1:          [final H1]
Word count:  [target range — e.g., 600-800 words]

SERP SNAPSHOT
[competitive table]

KEYWORD TARGETS
Primary: [keyword]
Secondary: [list]

PAGE STRUCTURE
[full section-by-section breakdown with H2s, content types, word targets]

AEO REQUIREMENTS
[question list with formats and placements]

INTERNAL LINKING PLAN
[inbound and outbound links]

E-E-A-T CHECKLIST
[required signals per section]

COPY RULES
[page-specific rules]

SCHEMA NEEDED
→ /seo schema [url] to generate: [list schema types]

SOCIAL META
[OG + Twitter card specs]

RECOMMENDED NEXT MODULES
→ /seo schema [url]      generate all schema types listed above
→ /seo aeo [url]         after publishing, build answer blocks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC BRIEF DEFAULTS

When generating briefs for Glen's sites, apply these defaults unless overridden:

**All photography pages (glenegrant.com):**
- Voice: Direct, professional, outcome-focused — not aspirational, not cliché
- Forbidden: "passionate", "capturing moments", "telling stories through light", "helping you achieve your vision"
- Required: Specific service type named, location "Toronto" in first paragraph, pricing range visible
- CTA: "Book a consultation" → links to /contact or booking URL

**Software landing pages:**
- Voice: Direct, specific, no marketing filler
- Required: Specific feature with specific metric ("batch 5,000 images", "3 watermark layers")
- Forbidden: "AI-powered", "powerful", "seamless", "blazing fast", "revolutionize"
- CTA: "Download Free Trial" or "Buy Pro License" — never "Get Started" without specificity

**Profile page (profile.glenegrant.com):**
- Voice: First person, confident, Glen's own voice — not a bio template
- Forbidden: any em dash, any "Hi I'm Glen", "passionate about"
- Required: Both photography AND software mentioned in first section
- No invented quotes or unverified claims
