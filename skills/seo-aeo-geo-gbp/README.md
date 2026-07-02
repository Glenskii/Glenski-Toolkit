# SEO / AEO / GEO / GBP Orchestrator

**Version:** 2.1.0
**Author:** Glen E. Grant (profile.glenegrant.com)
**License:** CC BY 4.0
**Tags:** `#glenski` `#seo` `#aeo` `#geo` `#gbp` `#schema` `#local-seo`

---

## What It Does

Complete search presence skill covering the full modern search stack:

| Layer | Module | What it covers |
|-------|--------|----------------|
| Technical | `/seo audit` | Crawlability, indexation, Core Web Vitals, on-page |
| Keyword | `/seo keywords` | Intent mapping, volume tiers, quick wins, gap analysis |
| Competitive | `/seo competitors` | Share-of-voice, gap matrix, 90-day action plan |
| AI Search | `/seo aeo` | Google AI Overviews, featured snippets, LLM citations |
| Local | `/seo gbp` | GBP audit, April 2026 compliance, photos, reviews, Q&As |
| Schema | `/seo schema` | JSON-LD generation for all types, @graph blocks |
| Content | `/seo brief` | Full SEO + AEO content brief with structure and intent |
| Monitoring | `/seo citations` | AI citation tracking across ChatGPT, Perplexity, Gemini |

---

## Principles

**Data discipline first.** Every finding carries an evidence tier:
- `[E1-VERIFIED]` — from live data you provided (GSC, Screaming Frog, tool exports)
- `[E2-REF]` — from authoritative documentation (Google Search Central, GBP policy)
- `[E3-BEST-PRACTICE]` — industry consensus; explicitly flagged as needing verification

**Mandatory input gate.** No module runs without a target URL and at least one data source. The skill asks for what it needs rather than guessing.

**Deterministic output.** Every module delivers specific artifacts: complete JSON-LD blocks, final-draft copy, prioritized finding tables — not vague "consider improving" suggestions.

---

## Installation

**Global install (available in all Claude Code projects):**
```powershell
xcopy /E /I /Y "C:\path\to\this\skill" "C:\Users\Glen\.claude\skills\seo-aeo-geo-gbp\"
```

**Or copy SKILL.md + modules/ directory** into any project's `.claude/skills/seo-aeo-geo-gbp/` for project-scoped install.

---

## Usage

```
/seo audit https://www.glenegrant.com
/seo keywords Toronto commercial photographer
/seo competitors https://www.glenegrant.com
/seo aeo "how much does commercial photography cost in Toronto"
/seo gbp Glen E. Grant Creative Toronto
/seo schema https://watermarkgienie.com
/seo brief commercial photography Toronto landing page
/seo citations Glen E. Grant
/seo help
```

---

## Pre-loaded Brand Context

The `schemas/brand-entity.yaml` file contains Glen E. Grant Creative's complete data bundle — NAP, geo coordinates, pricing, affiliations, awards, product inventory, and infrastructure notes. When loaded alongside SKILL.md, all schema, GBP, and AEO work is pre-populated with real data.

---

## Structure

```
seo-aeo-geo-gbp/
├── SKILL.md                      # Main entry point + input gate + router
├── README.md                     # This file
├── CHANGELOG.md                  # Version history
├── modules/
│   ├── 01-seo-audit.md           # Technical SEO audit
│   ├── 02-keyword-research.md    # Keyword research + intent mapping
│   ├── 03-competitor-analysis.md # Gap analysis + share-of-voice
│   ├── 04-aeo-geo-brief.md       # AEO + GEO content optimization
│   ├── 05-gbp-optimizer.md       # Google Business Profile + compliance
│   ├── 06-schema-generator.md    # JSON-LD schema generation
│   ├── 07-content-brief.md       # SEO content brief
│   └── 08-citation-tracking.md  # AI citation monitoring
├── schemas/
│   ├── brand-entity.yaml         # Pre-loaded brand data (Glen E. Grant Creative)
│   └── evidence-tiers.md         # Evidence tier system reference
└── templates/
    └── json-ld-templates.md      # Ready-to-deploy schema blocks
```

---

## Companion Skills

Recommended pairing:
- **impeccable** — design/brand system validation for any pages being optimized
- **vibe-security-audit** — security audit before deploying new pages

---

## License

CC BY 4.0 — Share freely, credit appreciated: "Glen E. Grant / profile.glenegrant.com"

Part of the **Glenski Toolkit** — github.com/Glenskii/Glenski-Toolkit
