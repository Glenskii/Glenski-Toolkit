# MODULE 02: KEYWORD RESEARCH
**Skill:** seo-aeo-geo-gbp-orchestrator v2.1.0
**Trigger:** `/seo keywords [url or topic]`

---

## PURPOSE

Produce a prioritized keyword matrix with intent mapping, volume tiers, difficulty assessment, and AEO opportunity flags. No fabricated metrics. If volume data is not provided, all estimates are explicitly E3 with a request for data.

---

## INPUT REQUIREMENTS

```yaml
required:
  - target_url_or_topic   # URL being optimized, or topic/niche description

strongly_recommended:
  - seed_keywords: []     # Known terms you already rank for or are targeting
  - at_least_one_of:
    - semrush_export       # Keyword overview CSV or position tracking export
    - ahrefs_export        # Site explorer or keyword explorer export
    - gsc_performance_data # GSC queries + impressions + clicks + position CSV
    - ga4_organic_report   # Organic traffic with landing pages

optional:
  - competitor_urls: []   # Competitor domains for gap analysis
  - geo_target: ""        # City/region if local intent is primary
  - business_type: ""     # Informs which intent clusters matter most
```

**If no volume data provided:** build the keyword framework with intent mapping and priority logic, label everything `[E3-BEST-PRACTICE]`, and explicitly state: *"Volume estimates are illustrative. Confirm with Semrush, Ahrefs, or GSC before committing to targets."*

---

## SEARCH INTENT TAXONOMY

Every keyword must be classified by intent before prioritization.

| Intent | Code | Description | Best page type |
|--------|------|-------------|----------------|
| Informational | `[INFO]` | User wants to learn | Blog post, FAQ, resource page |
| Navigational | `[NAV]` | User wants a specific brand/site | Brand homepage, direct URL |
| Commercial | `[COM]` | User is researching before buying | Comparison page, feature page, review |
| Transactional | `[TXN]` | User is ready to buy/book/sign up | Service page, product page, pricing |
| Local | `[LOCAL]` | User wants a service near them | Location page, GMB, local service page |

**Note:** Keywords can carry multiple intents. "Toronto commercial photographer pricing" = `[COM] + [LOCAL]`. Assign the dominant intent for routing decisions.

---

## KEYWORD RESEARCH EXECUTION

### STEP 1 — SEED EXPANSION

From the provided seeds (or from the target URL's topic), build the initial keyword universe using these expansion techniques:

**Head terms:** Broad, high-volume, high-competition — usually 1-2 words.
Example: "commercial photographer", "watermark software"

**Body terms:** Mid-length, 2-4 words, moderate competition, clearer intent.
Example: "Toronto commercial photographer", "batch watermark images"

**Long-tail terms:** 4+ words, lower volume, high intent, lower competition.
Example: "Toronto fashion photographer for brand campaigns", "watermark 5000 images at once"

**Question-format terms:** Key for AEO/featured snippets.
Format: "How do I...", "What is the best...", "Who is...", "How much does [service] cost in [city]"
Example: "how much does a commercial photographer cost in Toronto"

**Local modifier terms** (for location-based businesses):
- `[service] + [city]`
- `[service] + [neighborhood]` (Liberty Village, downtown Toronto)
- `[service] near me` queries (target with localized page + GBP signals)

---

### STEP 2 — KEYWORD MATRIX

Build this table for every keyword in scope. Sort by Priority Score (see scoring below).

```
KEYWORD MATRIX
───────────────────────────────────────────────────────────────────────────────
Keyword | Intent | Volume Tier | Difficulty | Current Rank | Priority | Notes
───────────────────────────────────────────────────────────────────────────────
[keyword] | [INT] | [H/M/L] | [H/M/L] | [position or "NR"] | [1-5] | [note]
```

**Volume tiers** (use if exact data unavailable):
- H (High): 1,000+ monthly searches
- M (Medium): 100-999 monthly searches
- L (Low): 10-99 monthly searches
- VL (Very Low): <10 monthly searches (niche, long-tail — still valuable if high intent)

**Difficulty tiers:**
- H (Hard): Established authority sites dominate first page, 50+ DA competitors
- M (Medium): Mix of authority and mid-tier sites, opportunity with strong content
- L (Low): Weak first page, opportunity for a focused page to rank

**Priority Score 1-5:**
- 5: High intent + achievable ranking + business-critical term
- 4: Good volume + clear intent match + currently ranking 6-20 (quick win)
- 3: Long-tail + transactional, lower volume but converts
- 2: Informational, builds authority, supports other targets
- 1: Aspirational — high difficulty, build toward over 12+ months

---

### STEP 3 — INTENT CLUSTER MAPPING

Group keywords into clusters. Each cluster maps to one page or content piece.

**Cluster structure:**
```
CLUSTER: [cluster name]
Target page: [URL or proposed new page]
Primary keyword: [the main term this page should rank for]
Supporting keywords: [2-5 secondary terms to include naturally]
Intent: [dominant intent code]
Action: [CREATE new page | OPTIMIZE existing page | EXPAND existing page]
AEO opportunity: [YES — query format + answer block opportunity | NO]
```

**Example:**
```
CLUSTER: Toronto Commercial Photography Services
Target page: https://www.glenegrant.com/commercial-photography/
Primary keyword: Toronto commercial photographer
Supporting keywords: commercial photography Toronto, brand photography Toronto,
  commercial photographer rates Toronto, corporate photography Toronto
Intent: [TXN] + [LOCAL]
Action: OPTIMIZE existing page
AEO opportunity: YES — "how much does a commercial photographer cost in Toronto"
  + "what is commercial photography"
```

---

### STEP 4 — QUICK WINS IDENTIFICATION

Flag keywords where ALL of the following are true — these are highest-ROI targets:
1. Currently ranking positions 6-20 (data from GSC required for E1)
2. Decent volume (M or H tier)
3. High intent (COM or TXN)
4. Existing page partially targets this keyword

Quick win fix: optimize the existing page's title, H1, meta description, and add 1-2 internal links pointing to it from related pages. Do not create a new page — push the existing page up.

---

### STEP 5 — GAP IDENTIFICATION

Keywords that competitors rank for but the target site does not:
- Source: Semrush/Ahrefs keyword gap tool, or manual review of competitor pages
- Flag as: `CONTENT GAP — needs new page or existing page expansion`
- Prioritize gaps that match high-intent clusters (TXN + LOCAL > INFO)

---

### STEP 6 — AEO FLAG

For every question-format keyword and any keyword with informational intent, flag it for module 04:
```
AEO FLAG: [keyword]
Query type: [question | comparison | definition | how-to | local]
Module: /seo aeo — build answer block for this query
Priority: [HIGH if featured snippet opportunity | MED | LOW]
```

---

## KEYWORD OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEYWORD RESEARCH REPORT
Site: [target_url]
Date: [date]
Data Sources: [list]
Total keywords analyzed: [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK WINS (optimize existing pages NOW) [E1 if GSC provided, E3 otherwise]
[table: keyword | current position | target position | page | fix]

PRIORITY CLUSTERS
[cluster 1 — full cluster block]
[cluster 2 — full cluster block]
[...]

FULL KEYWORD MATRIX
[sorted table]

AEO OPPORTUNITIES
[list of AEO flags with /seo aeo routing]

GAPS — NEW CONTENT NEEDED
[list of gap clusters with proposed page titles and URLs]

RECOMMENDED NEXT MODULES
→ /seo brief [topic]    for each new page cluster identified
→ /seo aeo [query]      for each AEO flagged keyword
→ /seo audit [url]      if title/H1 changes needed on existing pages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC KEYWORD CONTEXT

When running keyword research for Glen's properties, these seed clusters are pre-loaded:

**Photography (glenegrant.com)**
- Primary: "Toronto commercial photographer", "commercial photographer Toronto"
- Services: "fashion photographer Toronto", "glamour photographer Toronto", "lifestyle photographer Toronto", "fitness photographer Toronto", "brand photography Toronto"
- AI angle: "AI photography Toronto", "AI content photography", "content multiplication photography"
- Transactional: "hire photographer Toronto", "commercial photography rates Toronto", "book photographer Toronto"
- Pricing: "commercial photographer cost Toronto", "photography packages Toronto"

**Software products**
- Watermark Gienie V3: "batch watermark software", "watermark 5000 images", "bulk watermark tool Windows", "watermark photos in bulk", "professional watermark app"
- IdeaThreader Pro: "idea threading tool", "Twitter thread generator", "social media content threads"
- Sitemap Architect Pro: "sitemap generator tool", "XML sitemap builder", "visual sitemap creator"
- MailMindz: "email intelligence tool", "email triage software", "smart email management"

**Personal brand (profile.glenegrant.com)**
- "Glen E. Grant", "Glen Grant photographer", "Glen Grant software developer"
- "Toronto photographer software developer", "creative technologist Toronto"

**NAP-critical local terms** — always keep consistent:
- "Toronto" (not "the GTA", not "North York" — Liberty Village is Toronto)
- "commercial photographer" (not "photography studio" — Glen is the product, not a studio)
