# MODULE 08: AI CITATION TRACKING
**Skill:** seo-aeo-geo-gbp v2.1.0
**Trigger:** `/seo citations [brand-name]`

---

## PURPOSE

Monitor and improve a brand's presence in AI-generated answers across LLM-powered search products. Track whether the brand is cited, how accurately, and what content it's citing from. Identify gaps and the specific content interventions needed to improve citation frequency and accuracy.

---

## CONTEXT: WHY THIS MATTERS (2026)

AI-powered answer surfaces now intercept a meaningful percentage of navigational and informational queries:

- **Google AI Overviews:** Appear above organic results for a large percentage of informational queries
- **Perplexity AI:** Widely adopted as a research tool; shows sources prominently
- **ChatGPT (browsing-enabled):** Used for commercial research, product comparisons, local service queries
- **Gemini Advanced:** Google's conversational AI — distinct from AI Overviews, used for deeper queries
- **Claude.ai with web search:** Research and recommendation queries
- **Bing Copilot:** Integrated into Windows and Edge, significant enterprise reach

A brand that doesn't appear in these surfaces loses visibility on zero-click queries — where the user never scrolls to organic results because the AI answered their question directly.

---

## INPUT REQUIREMENTS

```yaml
required:
  - brand_name: ""          # Exact entity name to track (e.g., "Glen E. Grant")

strongly_recommended:
  - brand_variations: []    # Other names the brand may appear under
  - primary_domain: ""      # Main website URL
  - competitor_brands: []   # Brands to benchmark against in same space
  - query_list: []          # Specific queries to test (from module 02/04 output)
                            # If not provided: module generates test queries

optional:
  - tools_available: []     # "profound" | "otterly" | "gummy-search" | "manual"
                            # Default: manual testing protocol
  - monitoring_frequency: ""# "weekly" | "monthly" | "quarterly"
```

---

## TRACKING METHODOLOGY

### LAYER 1: MANUAL PROMPT TESTING

The most accessible method. Run these test prompts across each AI platform and record results.

**Test prompt categories:**

**Direct entity queries:**
```
"Who is [brand name]?"
"What does [brand name] do?"
"Tell me about [brand name]"
"[brand name] [city]"
```

**Service/product queries (commercial intent):**
```
"Best [service type] in [city]"
"[service type] near me" (use location-based account or note location)
"How to [solve problem the brand solves]"
"[product name] review"
"[product name] vs [competitor product]"
```

**Question queries (informational — should cite authoritative answers):**
```
"How much does [service] cost in [city]?"
"What is [product category]?"
"How do I [task brand helps with]?"
```

**For each test query on each platform, record:**

```
CITATION TEST RECORD
────────────────────────────────────────────────────
Query: "[exact query tested]"
Platform: [ChatGPT | Perplexity | Gemini | Claude | Bing Copilot | Google AIO]
Test date: [date]
Brand mentioned: [YES / NO / PARTIAL]
Brand citation type: [Named citation | URL cited | Indirect reference | None]
Source cited: [URL if provided by platform]
Accuracy: [ACCURATE | INACCURATE | INCOMPLETE]
Inaccuracies noted: [e.g., wrong location, wrong service described, outdated price]
Competitor citations: [brands that appeared instead]
Confidence level: [STRONG — brand is primary result | WEAK — brand is one of many | ABSENT]
────────────────────────────────────────────────────
```

**Testing platforms:**

| Platform | How to test | Citation visibility |
|----------|-------------|---------------------|
| ChatGPT (GPT-4o with browsing) | Browser search; enable browsing | Shows cited URLs |
| Perplexity AI | perplexity.ai | Shows source cards prominently |
| Google AI Overviews | Google Search (logged in) | Shows "Expand" sources |
| Gemini Advanced | gemini.google.com | Shows some sources |
| Claude.ai (web search) | claude.ai with search enabled | Shows cited URLs |
| Bing Copilot | bing.com/chat | Shows citations |

---

### LAYER 2: TOOL-BASED MONITORING

For systematic, recurring tracking. Use if available:

**Profound (profound.com)**
- Tracks brand visibility across AI platforms at scale
- Monitors share-of-voice in LLM responses
- Shows which queries include/exclude your brand
- Best for ongoing monitoring and trend tracking

**Otterly (otterly.ai)**
- Monitors brand mentions in AI-generated search results
- Tracks specific queries over time
- Alerts when brand appears or disappears

**Gummy Search (gummysearch.com)**
- Reddit monitoring — tracks brand mentions and adjacent discussions
- Useful for identifying negative sentiment that may suppress LLM citations

**Setup for tool-based monitoring:**
```
Monitor these query sets:
1. Direct brand queries (entity recognition)
2. Top 10 service/product queries (commercial intent)
3. Top 5 competitor comparison queries
4. Top 5 local intent queries (if local business)

Alert triggers:
- Brand citation drops below [X]% of responses
- New competitor appears in brand's query results
- Inaccurate brand description detected
- New source being cited about brand (positive or negative)
```

---

### LAYER 3: CITATION SOURCE ANALYSIS

When the AI cites a URL for brand information, identify and audit that source:

```
CITATION SOURCE AUDIT
────────────────────────────────────────────────────
Source URL: [url being cited]
Source type: [own website | directory | press | review | social | Wikipedia]
Content accuracy: [ACCURATE | OUTDATED | INACCURATE]
Last updated: [date if visible]
Action needed: [UPDATE own site | CLAIM/UPDATE directory | PITCH press update | NONE]
────────────────────────────────────────────────────
```

**Common citation sources by LLM:**
- ChatGPT: Wikipedia, major press, LinkedIn, official website, GitHub
- Perplexity: Official website (strongest), Yelp/Google reviews, industry directories, Reddit
- Google AIO: Official website (strongest), structured data on page, top-ranked pages
- Gemini: Google-owned surfaces (GBP, YouTube, Google Discover), official website

---

## GAP ANALYSIS AND FIXES

### Gap Type 1: Brand Not Cited at All

**Likely causes:**
- Brand entity not well-established across authoritative sources
- Website content is thin or lacks declarative fact-rich language
- No structured data (schema) signaling the entity
- Competitors have stronger link profiles and citation footprints

**Fixes:**
```
1. Run /seo aeo [url] → add GEO-optimized content blocks with entity-rich language
2. Run /seo schema [url] → add Person/Organization/LocalBusiness schema
3. Add entity to Wikipedia (if notable) or Wikidata (lower bar, anyone can add)
4. Build press/media citations (see citation building below)
5. Claim and complete all major business directory profiles
6. Ensure GBP listing is fully optimized (/seo gbp)
```

### Gap Type 2: Brand Cited Inaccurately

**Common inaccuracies and fixes:**

| Inaccuracy | Likely Source | Fix |
|------------|---------------|-----|
| Wrong city/location | Old directory listing | Update all directory profiles |
| Wrong service description | Old website content | Update homepage + About + schema |
| Wrong pricing | Outdated page | Update pricing page + schema |
| Old product name | Old product page indexed | Update page + add redirect |
| Missing award/credential | Not on authoritative source | Add to website, GBP, LinkedIn |

### Gap Type 3: Competitor Cited Instead

**Analysis:** Which competitor is appearing? What content do they have that you don't?

```
COMPETITOR CITATION ANALYSIS
────────────────────────────────────────────────────
Query: "[query where competitor appears instead]"
Competitor cited: [brand name]
Why they're cited: [likely reason — stronger entity, better content, more citations from press]
Content gap to close: [what specific content/page would compete]
Entity gap to close: [what authority signals they have that you don't]
Action: [specific task — usually: /seo brief or /seo aeo for that query topic]
────────────────────────────────────────────────────
```

---

## CITATION BUILDING STRATEGY

Building new citation sources improves both GEO visibility and traditional SEO.

**Priority citation targets for local businesses:**

Tier 1 — Most impactful for Google/AI:
- Google Business Profile (already covered in module 05)
- Apple Maps (maps.apple.com/business)
- Bing Places for Business
- Yelp (for Google SERP and Perplexity)
- LinkedIn Company Page or Professional Profile
- Wikipedia / Wikidata (for notable entities)

Tier 2 — Industry-specific authority:
- Photography: PhotoShelter directory, Association of Photographers, PPOC (Professional Photographers of Canada)
- Software: Product Hunt, G2, Capterra, AlternativeTo
- General: Better Business Bureau, Alignable, Chambers of Commerce

Tier 3 — Local directories:
- Yellow Pages Canada
- Canada411
- Foursquare
- Local city business directories

**NAP consistency rule — CRITICAL:**
Every directory listing must use the exact same business name, address, and phone number. Variations confuse both Google's entity resolution and LLM knowledge bases.

```
GLEN'S NAP (use exactly as written on every citation):
Business name: Glen E. Grant Creative
Address: Liberty Village, Toronto, ON M6K 3R1, Canada
Phone: +1-416-801-2525
Website: https://www.glenegrant.com
```

---

## PRESS AND MEDIA CITATIONS

Press mentions from credible publications carry significant weight for LLM knowledge graphs.

**Current press assets Glen already has:**
- Inside Fitness Magazine (print + digital) — establish online link if not already
- Cannes recognition (October 2024) — ensure this is listed on website with verifiable detail
- CBBF/IFBB affiliations — ensure these appear on official CBBF/IFBB member pages if applicable

**Press pitch targets for future citation building:**
- Toronto-based business press (Toronto Star, Globe and Mail business section, Toronto Life)
- Photography industry press (Professional Photographer magazine, Photo District News)
- Tech/software press (for software products: TechCrunch, The Next Web, Product Hunt)
- AI content multiplication angle — unique story for marketing/photography trade press

---

## CITATION TRACKING OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI CITATION TRACKING REPORT
Brand: [brand name]
Queries tested: [N]
Platforms tested: [list]
Date: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CITATION PRESENCE SUMMARY
────────────────────────────────────────────────────
Platform          | Cited | Accuracy | Competitor displacing
────────────────────────────────────────────────────
Google AI Overviews | YES/NO | [rating] | [if applicable]
Perplexity          | YES/NO | [rating] | [if applicable]
ChatGPT             | YES/NO | [rating] | [if applicable]
Gemini              | YES/NO | [rating] | [if applicable]
Claude.ai           | YES/NO | [rating] | [if applicable]
Bing Copilot        | YES/NO | [rating] | [if applicable]
────────────────────────────────────────────────────
Overall visibility score: [X/6 platforms citing]

INACCURACIES FOUND
[list with source and fix for each]

CITATION SOURCE AUDIT
[table: source URL | type | accuracy | action]

GAP ANALYSIS
[gap type per query + fix]

CITATION BUILDING PLAN (priority order)
1. [most impactful action first]
2. [...]
3. [...]

MONITORING SETUP
Recommended tool: [Profound | Otterly | manual]
Query set to monitor: [list]
Frequency: [weekly | monthly]
Next check date: [specific date]

RECOMMENDED NEXT MODULES
→ /seo aeo [url]    add GEO content blocks to address citation gaps
→ /seo schema [url] add Person/Organization schema if entity not resolved
→ /seo gbp          update GBP as primary citation anchor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC CITATION CONTEXT

**Current known citation strengths:**
- 25-year tenure (founded 2000) — long operating history is strong LLM trust signal
- Inside Fitness Magazine credits — press entity signal
- CBBF/IFBB affiliation — association entity signal
- Cannes recognition October 2024 — award entity signal (confirm this is on official Cannes site or equivalent source — LLMs need a citable URL, not just "Cannes recognition" on Glen's own website)
- GitHub (github.com/Glenskii) — technical credibility for software queries

**Priority citation gaps to investigate:**
- Wikipedia or Wikidata entry for "Glen E. Grant" — not confirmed as existing
- PPOC membership — not confirmed, worth verifying
- Press coverage with live URLs — Inside Fitness Magazine work needs accessible online citation
- Product Hunt profiles for each software product — none confirmed

**Test queries to run first:**
1. "Toronto commercial photographer" — does Glen appear in local pack or AI answer?
2. "watermark 5000 images software" — does Watermark Gienie appear?
3. "Glen E. Grant" — does the entity resolve with correct description?
4. "AI content photography Toronto" — unique positioning query, Glen should own this
5. "IdeaThreader Pro" — direct product query, should resolve to correct product page
