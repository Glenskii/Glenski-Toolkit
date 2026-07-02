# MODULE 03: COMPETITOR ANALYSIS
**Skill:** seo-aeo-geo-gbp v2.1.0
**Trigger:** `/seo competitors [url]`

---

## PURPOSE

Deliver a gap analysis and share-of-voice assessment against direct competitors. Identify what they rank for that the target site doesn't, what structural advantages they have, and where the target site can realistically displace them. No fabricated metrics — E1 from data exports, E2 from direct observation, E3 flagged as estimated.

---

## INPUT REQUIREMENTS

```yaml
required:
  - target_url              # Primary domain being analyzed

strongly_recommended:
  - competitor_urls: []     # 2-5 direct competitors
                            # If not provided: skill will identify candidates from
                            # keyword overlap — but quality is lower without explicit input
  - at_least_one_of:
    - semrush_gap_export    # Keyword gap tool export
    - ahrefs_gap_export     # Content gap or keyword gap export
    - gsc_performance_data  # Your GSC data (needed for share-of-voice baseline)

optional:
  - keyword_list: []        # Specific keywords to compare on
  - geo_target: ""          # Local-specific comparison (city/region)
```

**Competitor identification fallback:** If no competitors are provided, analyze the target URL's top content topics, infer the competitive set from the niche, and ask for confirmation: *"Based on [topic], likely competitors include [A, B, C]. Confirm these are your direct competitors before I proceed."*

---

## COMPETITOR ANALYSIS EXECUTION

### STEP 1 — COMPETITOR PROFILING

For each competitor, produce this profile before gap analysis:

```
COMPETITOR PROFILE: [domain]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domain Authority / DR: [if provided or observable] [E1 if from tool, E3 if estimated]
Estimated organic traffic: [from tool data] [E1 if tool data, E3 if estimated]
Top ranking pages: [list top 5 by traffic or prominence — E1 if tool, E2 if observed live]
Primary keyword clusters they own: [list 3-5 themes]
Schema types implemented: [check live — E1 via direct observation]
GBP listing: [YES/NO, claimed/unclaimed if local]
Content volume: [approx page count or post frequency — E2 if observed]
Site technology: [WordPress, Squarespace, custom — E2 via observation]
Key differentiators: [what makes their positioning distinct]
Weaknesses: [thin content areas, missing schema, poor mobile, slow LCP]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### STEP 2 — KEYWORD GAP MATRIX

Build the gap matrix: keywords competitors rank for that the target site doesn't appear for.

```
KEYWORD GAP MATRIX
──────────────────────────────────────────────────────────────────
Keyword | Volume | Intent | Comp A rank | Comp B rank | Target rank | Opportunity
──────────────────────────────────────────────────────────────────
[keyword] | [H/M/L] | [INT] | [pos] | [pos] | [NR/pos] | [HIGH/MED/LOW]
```

**Opportunity scoring:**
- HIGH: Target site not ranking, competitors ranking 1-10, keyword is transactional or local, volume is M+
- MED: Target site not ranking or ranking 20+, at least one competitor ranking well, volume L-M
- LOW: Informational, low volume, or all competitors ranking weakly — opportunity exists but not priority

---

### STEP 3 — SHARE OF VOICE

Share of Voice (SOV) measures how visible the target site is vs competitors across a defined keyword set.

**Calculation** (requires position data for all sites on all keywords):
```
SOV = Sum of CTR-weighted visibility scores for your rankings
      ──────────────────────────────────────────────────────────
      Sum of CTR-weighted visibility scores for all competitors combined
```

**CTR weights by position** `[E2-REF: Sistrix CTR study, industry benchmark]`:
- Position 1: 28.5%
- Position 2: 15.7%
- Position 3: 11.0%
- Position 4: 8.0%
- Position 5: 7.2%
- Position 6-10: 3-5%
- Position 11-20: 1-2%
- Not ranking: 0%

**Output:**
```
SHARE OF VOICE SUMMARY [E1 if position data provided, E3 if estimated]
─────────────────────────────────────────
[target_site]:  [X]%
[competitor_1]: [X]%
[competitor_2]: [X]%
[competitor_3]: [X]%
─────────────────────────────────────────
Total tracked keywords: [N]
Target's current SOV gap to top competitor: [X percentage points]
Keywords where target leads: [N]
Keywords where target trails: [N]
Keywords where target is not present: [N]
```

---

### STEP 4 — CONTENT STRUCTURE COMPARISON

For the top 5 most competitive pages in the target niche, compare structure directly:

```
PAGE COMPARISON: "[keyword cluster]"
─────────────────────────────────────────────────────────────────
                | TARGET SITE | COMP A | COMP B
─────────────────────────────────────────────────────────────────
Word count      | [N]         | [N]    | [N]
H2 sections     | [N]         | [N]    | [N]
Images          | [N]         | [N]    | [N]
Schema type     | [type/none] | [type] | [type]
FAQ section     | YES/NO      | YES/NO | YES/NO
Internal links  | [N]         | [N]    | [N]
CTA present     | YES/NO      | YES/NO | YES/NO
AEO block       | YES/NO      | YES/NO | YES/NO
Page speed (LCP)| [time]      | [time] | [time]
─────────────────────────────────────────────────────────────────
Target gaps: [list specific structural items to add]
```

---

### STEP 5 — LINK PROFILE COMPARISON

*(Requires Semrush/Ahrefs data for E1 — E3 otherwise)*

```
BACKLINK COMPARISON [E1 if tool data, E3 if estimated]
──────────────────────────────────────────
Domain: referring domains count | authority distribution | notable links
──────────────────────────────────────────
[target]:     [N RD] | [authority spread] | [notable sources]
[competitor]: [N RD] | [authority spread] | [notable sources]
```

**Link gap opportunities:**
- Identify domains linking to competitors but not the target
- Flag: "Industry directories they're listed in that you're not" (route to module 08 for local citation work)
- Flag: "Media/press coverage they've received" (informational for PR strategy)

---

### STEP 6 — COMPETITIVE ADVANTAGES AUDIT

What does the target site do better than competitors? This matters for messaging and doubling down.

Assess each advantage area:
- Schema implementation (more complete schema = richer SERP features)
- Page speed / Core Web Vitals (faster = ranking signal + better UX)
- Content depth on specific topics
- GBP optimization (more reviews, photos, attributes, posts)
- AEO readiness (structured answer blocks, FAQ schema)
- AI citation presence (appears in ChatGPT/Perplexity answers)
- Local authority (more local signals, NAP consistency, citations)

---

## COMPETITOR OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPETITOR ANALYSIS REPORT
Site: [target_url]
Competitors analyzed: [list]
Date: [date]
Data Sources: [list]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPETITOR PROFILES
[profile block per competitor]

SHARE OF VOICE
[SOV table]

TOP 10 KEYWORD GAPS — HIGH OPPORTUNITY
[table: keyword | volume | intent | best competitor rank | action]

CONTENT STRUCTURE GAPS
[table per competitive page]

TARGET SITE ADVANTAGES TO LEVERAGE
[list — where target is ahead and can go further]

90-DAY ACTION PLAN
Priority 1 (Month 1): [highest-impact gap to close]
Priority 2 (Month 2): [second-tier gaps]
Priority 3 (Month 3): [structural improvements]

RECOMMENDED NEXT MODULES
→ /seo brief [topic]     for each new page identified in gaps
→ /seo keywords [url]    to expand gap keywords into full research
→ /seo schema [url]      if competitor schema implementation is ahead
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC COMPETITOR CONTEXT

When running competitor analysis for Glen's photography business, these are the relevant competitive sets:

**Photography (glenegrant.com) — Toronto commercial photography**
Known competitive landscape:
- Other Toronto commercial/editorial photographers with strong SEO presence
- Photography agencies/studios (not direct — different service model)
- Stock photo sites are not competitors for "hire a photographer" intent
- Comp differentiation angle: AI content multiplication is Glen's unique positioning — no direct local competitor offers this

**Key competitive advantages to always surface:**
- 25-year track record (founded 2000) — most competitors can't match tenure
- Cannes recognition (2024) — award signal
- Inside Fitness Magazine / CBBF / IFBB affiliations — niche authority
- AI content multiplication as service (differentiated offering)
- Dual identity: photographer + software developer (unique positioning for tech-adjacent clients)

**Software products — competitive sets vary by product**
- Watermark Gienie V3: competes with iWatermark, Visual Watermark, uMark, TSR Watermark Image
- IdeaThreader Pro: competes with Typefully, Taplio, Hypefury, Fedica
- Sitemap Architect Pro: competes with XML-Sitemaps.com, Screaming Frog (free tier), Yoast sitemap
- Competitor analysis for software should focus on: pricing page structure, trial conversion, feature comparison pages, schema types (Product, SoftwareApplication, FAQPage)
