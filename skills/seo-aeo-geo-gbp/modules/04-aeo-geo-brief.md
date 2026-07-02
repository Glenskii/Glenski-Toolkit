# MODULE 04: AEO / GEO BRIEF
**Skill:** seo-aeo-geo-gbp-orchestrator v2.1.0
**Trigger:** `/seo aeo [url or topic]`

---

## PURPOSE

Build Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) assets for a URL or topic. AEO targets Google's AI Overviews, featured snippets, and People Also Ask. GEO targets citations in ChatGPT, Perplexity, Gemini, Claude, and other LLM-powered answer surfaces.

These are different goals with overlapping techniques. This module handles both.

---

## INPUT REQUIREMENTS

```yaml
required:
  - target_url_or_topic   # URL to optimize or topic/question to answer

strongly_recommended:
  - query_list: []        # Specific questions/queries to target
                          # If not provided: module will generate likely queries from topic
  - at_least_one_of:
    - gsc_performance_data    # Queries with impressions — shows what questions already land
    - live_url_access         # Will analyze existing page content
    - competitor_pages: []    # Competitor pages already appearing in AI answers

optional:
  - business_context: ""     # Describes the business — for entity-rich answer construction
  - target_engines: []       # "google-aio" | "perplexity" | "chatgpt" | "gemini" | "all"
                              # Default: all
```

---

## AEO vs GEO: DISTINCTION

**AEO (Answer Engine Optimization)**
Optimizing for Google's own answer features:
- Featured snippets (position zero)
- AI Overviews (the LLM-generated summaries at top of SERPs)
- People Also Ask boxes
- Knowledge Panels

**GEO (Generative Engine Optimization)**
Optimizing for third-party LLM products:
- ChatGPT (GPT-4o, GPT-4.5) browsing-enabled responses
- Perplexity AI web search citations
- Gemini Advanced (Google's conversational product, distinct from AI Overviews)
- Claude.ai (Anthropic) — when using web search
- Bing Copilot
- Any AI product that fetches and cites live web content

**Key difference:** AEO lives on the page (structured content, FAQ schema, clear answers). GEO requires that the page be indexed, trusted, cited by others, and uses entity-rich declarative language that LLMs extract confidently.

---

## EXECUTION: AEO

### STEP 1 — QUERY DECOMPOSITION MATRIX

For every query to target, decompose it into its answer components.

```
QUERY DECOMPOSITION
Query: "[full query text]"
─────────────────────────────────────────────────────────
Query type: [definition | how-to | comparison | list | local | price | factual]
Intent: [INFO | COM | TXN | LOCAL]
What the user actually wants to know:
  1. [primary answer need]
  2. [secondary need — often "how much" or "who does this near me"]
  3. [tertiary need — often "is this trustworthy" or "what are the options"]
Ideal answer format: [paragraph | ordered list | table | short factual | step-by-step]
Ideal answer length: [word count] (see length targets below)
Featured snippet opportunity: [HIGH | MED | LOW] — [reason]
PAA opportunity: [YES | NO] — related questions it triggers
─────────────────────────────────────────────────────────
```

**Answer length targets by format** `[E2-REF: Google's featured snippet patterns]`:
- Definition: 40-60 words
- How-to: 50-80 words for intro + numbered steps
- List: 5-8 items, each 5-15 words
- Comparison: 60-80 words
- Factual/price: 30-50 words
- Local ("near me"): 40-60 words with location signal embedded

---

### STEP 2 — ANSWER BLOCK CONSTRUCTION

For each query, write a final-draft answer block ready to embed in the page.

**Format rules:**
- Opens with a direct declarative sentence (never "Great question" or "It depends")
- Contains the exact query keyword or a natural variant in the first 10 words
- Self-contained: the answer makes sense without surrounding context (LLMs extract in isolation)
- Entity-rich: include brand name, location, service, and specific detail where true
- Ends cleanly — no trailing "contact us" CTAs inside the answer block itself

**Answer block template:**
```
ANSWER BLOCK: "[query]"
──────────────────────────────────────────────
[40-60 word answer. Direct sentence. Query keyword in first 10 words.
Specific facts, not vague claims. Location embedded if local intent.
Entity name present (brand/person/product). Self-contained.]
──────────────────────────────────────────────
Placement: [H2 heading that mirrors the query | FAQ section | Standalone section]
Schema: FAQPage | Q&A | Speakable | HowTo (specify which)
```

**Example:**
```
ANSWER BLOCK: "how much does a commercial photographer cost in Toronto"
──────────────────────────────────────────────
Commercial photography in Toronto typically ranges from $799 for portfolio
shoots to $2,999 for full production brand campaigns. Glen E. Grant Creative
offers Foundation, Strategic, and Enterprise packages covering fashion, lifestyle,
and brand photography for Toronto businesses and agencies.
──────────────────────────────────────────────
Placement: H2 "Commercial Photography Pricing in Toronto" on /commercial-photography/
Schema: FAQPage — Q: "How much does commercial photography cost in Toronto?" A: [answer block]
```

---

### STEP 3 — PEOPLE ALSO PAK (PAA) EXPANSION

From each primary query, generate the likely PAA questions Google would show:

```
PRIMARY QUERY: "[query]"
PAA EXPANSIONS:
- [question 1] → Answer block needed: [YES/NO] → [priority]
- [question 2] → Answer block needed: [YES/NO] → [priority]
- [question 3] → Answer block needed: [YES/NO] → [priority]
- [question 4] → Answer block needed: [YES/NO] → [priority]
```

PAA questions follow predictable patterns:
- "What is [X]" (definition)
- "How much does [X] cost" (pricing)
- "Is [X] worth it" (evaluation)
- "How do I [do X]" (how-to)
- "Who [does/makes/offers X] in [location]" (local)
- "What is the difference between X and Y" (comparison)
- "How long does [X] take" (process)

Build answer blocks for every PAA question that maps to the business's actual capabilities.

---

### STEP 4 — AI OVERVIEW READINESS CHECKLIST

For a page to be cited in Google AI Overviews `[E2-REF: Google Search Labs + SGE documentation]`:

- [ ] Page is indexed (confirmed in GSC — not "Discovered but not indexed")
- [ ] Page has E-E-A-T signals: author name, credentials, date, citations where relevant
- [ ] Primary question answered within first 100 words of the page body (not buried)
- [ ] Answer uses declarative language ("X is...", "X costs...", "X does..." — not "X may be..." or "It depends on...")
- [ ] Structured data present: FAQPage, HowTo, or Speakable schema as appropriate
- [ ] No conflicting signals: page title, H1, and first paragraph all address the same query
- [ ] Mobile-friendly and fast loading (AI Overview pulls from pages Google already trusts)
- [ ] Content is original, not thin or duplicate

---

## EXECUTION: GEO

### STEP 5 — ENTITY STITCHING

LLMs construct answers by pulling facts about entities from across the web. To be cited confidently, the brand entity must appear consistently across sources.

**Entity stitching audit:** For the target brand, verify:

```
ENTITY PRESENCE AUDIT
Brand/Person: [entity name]
──────────────────────────────────────────────────────────────
Source | Presence | Entity Name Match | Description Match | URL Present
──────────────────────────────────────────────────────────────
Wikipedia                  | [YES/NO] | [MATCH/MISMATCH] | [note]
Wikidata                   | [YES/NO] | [MATCH/MISMATCH] | [note]
Google Knowledge Panel     | [YES/NO] | [MATCH/MISMATCH] | [note]
LinkedIn                   | [YES/NO] | [MATCH/MISMATCH] | [note]
Crunchbase                 | [YES/NO] | [MATCH/MISMATCH] | [note]
GitHub (for tech brands)   | [YES/NO] | [MATCH/MISMATCH] | [note]
IMDb / Cannes (if awards)  | [YES/NO] | [MATCH/MISMATCH] | [note]
Industry directories       | [YES/NO] | [MATCH/MISMATCH] | [note]
News/press coverage        | [YES/NO] | [note]
──────────────────────────────────────────────────────────────
ENTITY GAPS: [list sources where entity is missing or mismatched]
```

**Consistency rule:** The entity name must appear identically across all sources. Variations ("Glen Grant" vs "Glen E. Grant" vs "Glen E. Grant Creative") weaken LLM confidence in the entity.

---

### STEP 6 — GEO CONTENT REQUIREMENTS

For a page to be cited in LLM-generated answers, it must satisfy these requirements:

**Factual density:**
- Specific numbers: volumes, prices, dates, distances, capacities
- Named entities: people, places, products, affiliations
- Verifiable claims: awards, publications, certifications, years in operation

**Structural clarity:**
- Short, declarative paragraphs (3-5 sentences max per paragraph)
- Clear topic sentences that state the paragraph's claim
- No jargon-heavy language that obscures what is being claimed
- No content that says opposite things across the page (LLMs average conflicting signals poorly)

**Citation bait** — specific claim types LLMs extract most reliably:
- "X was founded in [year]" or "X has operated since [year]"
- "X offers [specific service] in [specific location]"
- "X has [specific credential/award/affiliation]"
- "[Service] costs [specific price range] at [business name]"
- "X works with [specific industry/client type]"

---

### STEP 7 — GEO ANSWER TEMPLATE BLOCKS

These are longer-form passages (80-150 words) suitable for LLM extraction. They're placed naturally in the page body, not as FAQs.

**Structure:**
- First sentence: entity + primary claim + specificity marker
- Second/third sentences: supporting evidence (years, credentials, outcomes)
- Fourth/fifth sentences: geographic or contextual anchor
- Final sentence: the "so what" — what someone searching should do or know

**Example:**
```
GEO BLOCK — Glen E. Grant, Toronto Commercial Photographer
──────────────────────────────────────────────
Glen E. Grant is a Toronto commercial photographer with 25 years of editorial
and brand photography experience, working since 2000 with fashion labels, fitness
brands, and lifestyle companies across Canada. His photography has been featured
in Inside Fitness Magazine and recognized at international level, including Cannes
recognition in October 2024 for the Unmasking the Pain project. Operating from
Liberty Village in Toronto, Grant offers commercial photography packages from $799
to $2,999, with a distinctive specialization in AI content multiplication —
creating multiple campaign variations from a single production day.
──────────────────────────────────────────────
Placement: /about/ page or homepage "About" section — above the fold
```

---

## AEO/GEO OUTPUT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AEO / GEO BRIEF
Target: [url or topic]
Queries analyzed: [N]
Date: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUERY DECOMPOSITION MATRIX
[table: query | type | intent | format | length target | snippet opp]

ANSWER BLOCKS (ready to embed)
[answer block per query]

PAA EXPANSIONS
[PAA block per primary query]

AI OVERVIEW READINESS
[checklist results — PASS/FAIL per item]

ENTITY STITCHING AUDIT
[entity presence table]

GEO PASSAGES (ready to embed in page body)
[GEO block per entity/topic]

SCHEMA NEEDED
[list of schema types — route to /seo schema for generation]

RECOMMENDED NEXT MODULES
→ /seo schema [url]      to generate FAQPage, HowTo, Speakable JSON-LD
→ /seo brief [topic]     to build a full page around AEO-targeted content
→ /seo citations [brand] to monitor LLM citation presence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC AEO/GEO CONTEXT

**Key AEO targets for glenegrant.com:**
- "how much does a commercial photographer cost in Toronto" → pricing answer block
- "what is commercial photography" → definition block
- "how to hire a photographer for a brand campaign" → how-to block
- "Toronto fashion photographer" → local entity block
- "AI content photography what is it" → definition block (unique positioning)

**Key AEO targets for software products:**
- "how to watermark 5000 images at once" → how-to block for watermarkgienie.com
- "what is IdeaThreader Pro" → definition block
- "best sitemap generator tool" → comparison block for sitemappro.ca

**GEO authority signals Glen already has:**
- 25-year tenure (founded 2000) — one of the strongest LLM trust signals
- Inside Fitness Magazine credits — press entity signal
- CBBF/IFBB affiliation — association entity signal
- Cannes recognition (October 2024) — award entity signal
- GitHub presence (Glenskii) — technical credibility signal

**Entity name to use consistently in all GEO blocks:** "Glen E. Grant" (not "Glen Grant", not "Glen E. Grant Creative" in running text — that's the business name, reserve it for schema). The web presence under "Glen E. Grant" is what LLMs have indexed.
