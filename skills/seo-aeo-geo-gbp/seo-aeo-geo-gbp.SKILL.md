---
name: "seo-aeo-geo-gbp"
title: "SEO / AEO / GEO / GBP ORCHESTRATOR"
version: "2.1.0"
last_updated: "2026-05-17"
description: >
  Production-grade search presence skill covering technical SEO auditing, keyword
  research, competitor gap analysis, Answer Engine Optimization (AEO), Generative
  Engine Optimization (GEO), Google Business Profile compliance, JSON-LD schema
  generation, SEO content briefs, and AI citation monitoring. Operates on a
  mandatory input gate — no recommendations without verified data. Evidence is
  tiered E1/E2/E3. All outputs are deterministic artifacts: audits, briefs,
  schema blocks, compliance reports.
author: "Glen E. Grant"
website: "https://profile.glenegrant.com"
license: "CC BY 4.0"
repo: "https://github.com/Glenskii/Glenski-Toolkit"
tags:
  - "seo"
  - "aeo"
  - "geo"
  - "gbp"
  - "schema"
  - "local-seo"
  - "answer-engine"
  - "glenski"
compatible_with:
  - "Claude"
  - "Claude Projects"
  - "Any LLM with file context support"
---

# SEO / AEO / GEO / GBP ORCHESTRATOR v2.1.0

**Author:** Glen E. Grant (profile.glenegrant.com)
**Purpose:** Complete search presence management — from technical audit to AI citation monitoring.
**License:** CC BY 4.0 — share freely, credit appreciated
**Tags:** `#glenski` `#seo` `#aeo` `#geo` `#gbp` `#schema` `#local-seo`

---

## THE PROBLEM THIS SOLVES

Generic SEO advice is everywhere. What's missing is a skill that:
- Refuses to recommend without verified data (no guessing at traffic or rankings)
- Covers the full modern search stack: classic SEO + AI answer engines + GBP + LLM citations
- Ties GBP compliance to the **April 2026 policy** (Gemini-enforced, FTC $51,744/violation)
- Generates ready-to-deploy JSON-LD, not placeholder schema templates
- Tracks whether your brand appears in ChatGPT, Perplexity, and Google AI Overviews

This skill enforces discipline: input gate first, evidence tier labeling on every claim, deterministic artifact delivery on every output.

---

## MANDATORY INPUT GATE

**Before invoking any module**, the following must be provided. If any field is missing, ask for it — do not proceed.

```yaml
# REQUIRED INPUTS
target_url: ""          # Full URL (https://...) — the primary domain or page under analysis
business_type: ""       # "local" | "ecommerce" | "saas" | "personal-brand" | "portfolio"
primary_location: ""    # City + Province/State (local businesses only — skip for pure SaaS/global)
data_sources: []        # At minimum ONE of: GSC export, GA4 export, Screaming Frog crawl,
                        # Semrush/Ahrefs CSV, GBP insights export, live URL

# OPTIONAL BUT STRONGLY RECOMMENDED
competitor_urls: []     # Up to 5 direct competitors
target_keywords: []     # Seed keyword list (will be expanded via research)
gbp_listing_url: ""     # Google Business Profile URL (for GBP module)
```

**If no data source is provided:** state clearly: *"I can provide best-practice guidance only (E3 evidence). For E1 findings, provide a GSC export, Screaming Frog crawl, or GA4 data."*

---

## EVIDENCE TIER SYSTEM

Every finding and recommendation must carry an evidence label.

| Tier | Label | Definition |
|------|-------|------------|
| E1 | `[E1-VERIFIED]` | Pulled from live data: GSC, GA4, Screaming Frog crawl, GBP insights export, live URL fetch |
| E2 | `[E2-REF]` | From authoritative reference: Google's own documentation, Search Central, official GBP policy docs, confirmed industry benchmarks with source cited |
| E3 | `[E3-BEST-PRACTICE]` | Industry consensus with no project-specific data. Always flag: *"Verify against your data."* |

**Rule:** Never present E3 findings as if they were E1. Never omit tier labels on claims.

---

## MODULE ROUTER

| Command | Module | Description |
|---------|--------|-------------|
| `/seo audit [url]` | 01-seo-audit | Full technical SEO crawl analysis |
| `/seo keywords [url or topic]` | 02-keyword-research | Keyword research with intent mapping |
| `/seo competitors [url]` | 03-competitor-analysis | Gap analysis + share-of-voice |
| `/seo aeo [url or topic]` | 04-aeo-geo-brief | Answer Engine + Generative Engine brief |
| `/seo gbp [listing-url or business-name]` | 05-gbp-optimizer | GBP audit, optimization, compliance |
| `/seo schema [url or business-type]` | 06-schema-generator | JSON-LD generation for all schema types |
| `/seo brief [topic + url]` | 07-content-brief | Full SEO content brief with intent + AEO structure |
| `/seo citations [brand-name]` | 08-citation-tracking | AI citation monitoring across LLMs |
| `/seo help` | — | Show this router |
| `/seo status` | — | Current input gate status (what's been provided) |

---

## BRAND ENTITY BUNDLE

This bundle is pre-loaded for Glen E. Grant Creative. When working on Glen's properties, this data is automatically injected into every module — no need to re-enter.

```yaml
brand:
  legal_name: "Glen E. Grant Creative"
  trading_name: "Glen E. Grant"
  founded: 2000
  type: "LocalBusiness > ProfessionalService"
  description: "Toronto commercial photographer and software developer. 25+ years editorial and brand photography. 13+ software products including Watermark Gienie V3 and IdeaThreader Pro."

contact:
  email: "glen@glenegrant.com"
  phone: "+1-416-801-2525"
  website: "https://www.glenegrant.com"
  profile: "https://profile.glenegrant.com"

locations:
  - city: "Toronto"
    province: "ON"
    country: "CA"
    postal_code: "M6K 3R1"
    neighborhood: "Liberty Village"
    geo_lat: 43.6532
    geo_lng: -79.3832

services:
  photography:
    - "Commercial brand photography"
    - "Fashion and glamour photography"
    - "Lifestyle photography"
    - "Editorial photography"
    - "Fitness photography"
    - "AI content multiplication"
  software:
    - "Watermark Gienie V3 (watermarkgienie.com)"
    - "IdeaThreader Pro (ideathreader.com)"
    - "Sitemap Architect Pro (sitemappro.ca)"
    - "MailMindz (mailmindz.app)"

pricing:
  range: "$799-$2999"
  packages: ["Foundation", "Strategic", "Enterprise"]

affiliations:
  - "Inside Fitness Magazine"
  - "CBBF (Canadian Bodybuilding Federation)"
  - "IFBB (International Federation of Bodybuilding)"

awards:
  - name: "Unmasking the Pain — Cannes recognition"
    year: 2024
    month: 10

social:
  github: "https://github.com/Glenskii"

design_system:
  bg: "#0A0A0A"
  accent_orange: "#E85D04"
  accent_coral: "#E63946"
  heading_font: "Georgia, serif"
  body_font: "system-ui, sans-serif"
```

---

## GLOBAL OUTPUT STANDARDS

All module outputs must follow these conventions:

**Format:**
- Lead with the finding, follow with the fix
- Label each finding with evidence tier
- Priority: Critical (breaks indexing/compliance) → High (measurable ranking impact) → Medium → Low
- Every actionable item has a deliverable: "Fix X" not "Consider fixing X"

**Schema blocks:** Valid JSON-LD, ready to paste into `<head>` or `<script type="application/ld+json">`.

**Copy artifacts:** Complete, final strings — not templates with [PLACEHOLDER] text.

**Compliance items:** Always cite the specific policy section or Google documentation URL.

---

## MODULE FILES

Full implementation logic lives in the `/modules/` directory:

- [modules/01-seo-audit.md](modules/01-seo-audit.md)
- [modules/02-keyword-research.md](modules/02-keyword-research.md)
- [modules/03-competitor-analysis.md](modules/03-competitor-analysis.md)
- [modules/04-aeo-geo-brief.md](modules/04-aeo-geo-brief.md)
- [modules/05-gbp-optimizer.md](modules/05-gbp-optimizer.md)
- [modules/06-schema-generator.md](modules/06-schema-generator.md)
- [modules/07-content-brief.md](modules/07-content-brief.md)
- [modules/08-citation-tracking.md](modules/08-citation-tracking.md)

Supporting references:

- [schemas/evidence-tiers.md](schemas/evidence-tiers.md)
- [schemas/brand-entity.yaml](schemas/brand-entity.yaml)
- [templates/json-ld-templates.md](templates/json-ld-templates.md)

---

*This skill enforces data discipline. No fabricated metrics. No invented rankings. No assumed keyword volumes. Evidence tier on every claim.*
