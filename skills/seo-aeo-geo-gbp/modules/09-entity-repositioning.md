# MODULE 09: ENTITY REPOSITIONING & AI-TERM SCRUB
**Skill:** seo-aeo-geo-gbp-orchestrator
**Trigger:** `/seo entity [url]` — or any time an AI Overview / AI engine mis-reads *who a client is*, or AI-forward copy is burying a client's core identity.

---

## PURPOSE

Reclaim how search engines and AI engines understand a client's **entity** (who they are, what they do) when the machine-built picture has drifted away from the business reality. Built from the Glen E. Grant case (2026-07): Google's AI Overview had rebuilt a 26-year commercial/fashion/editorial photographer as an "AI photographer," burying the craft and scaring off AI-skittish clients.

---

## THE GOVERNING RULE (read first)

**AI-forward positioning is OPT-IN, never the default.** Unless a client *explicitly* asks to be marketed as an AI/tech offering, keep "AI" language off their client-facing marketing surfaces entirely. AI overexposure in a client's own content is the single most common cause of a poisoned entity: the machine builds the identity from the loudest, densest, freshest signal, and if that signal is "AI," the core business identity gets averaged into the background.

Corollary (the client's craft is the trunk): describe technical/AI capability in **real-world craft terms**, never the tech label, AND never let it bury the client's tenure or core discipline. Capability is a branch a client discovers, never the headline.

---

## SUBSTITUTION LEXICON ("say it without naming it")

| Instead of | Use (real craft language) |
|---|---|
| AI-enhanced / AI-powered / AI-assisted / AI-driven | advanced post-production, modern studio production, or the outcome verb: *extended, scaled, multiplied, amplified* |
| "intelligent production" | post-production craft |
| AI content/asset multiplication | asset multiplication, content multiplication |
| "Photography Amplified by AI" | "Photography, Amplified" |
| AI-Augmented Imagery (schema skill) | remove, or "Post-Production Craft" |

Keep AI language ONLY where it is protective or genuinely the subject: legal anti-AI-training clauses, copyright disclosure of generative works, model-release consent language, and actual AI *products*. Flag these as intentional-keep.

---

## DIAGNOSIS (map the whole entity, on-site AND off)

1. **On-site AI density** — `grep -rniE '\bAI\b|AI-driven|AI-enhanced|AI-powered|AI-assisted|AI-augmented|artificial intelligence'` across all HTML. Separate three piles: (a) marketing copy/meta/headings/alt → scrub, (b) schema `knowsAbout`/serviceType/offers → scrub, (c) intentional-keep (legal, consent, products).
2. **Schema + dates** — check `knowsAbout`, `jobTitle`, `serviceType`, `foundingDate`. Contradictions (e.g. two different founding years across pages) make the machine *hedge*, and that hedge is what produces insulting output like "over 20 years" for a 26-year career. Resolve by MEANING, not by flattening: a client often has TWO legitimately different dates (craft tenure vs business/professional founding). Model them distinctly and use each CONSISTENTLY, e.g. Person = "26 years behind the lens since 2000", Organization `foundingDate` = 2003 (professional practice began). Framed that way they read as complementary facts, never a conflict. Lead every experience claim with the strongest number.
3. **Off-site self-inflicted signals** — the client's OWN bios (Instagram, LinkedIn, Threads, Behance, Facebook, marketplace profiles). These are frequently the loudest AI signal and the client controls them. Name consistency matters (a middle initial dropped on one profile fragments the entity).
4. **External sources the AI cites** — pull what the AI Overview cites. Watch for (a) wrong attributions (a generic article grafted onto the client), (b) off-brand marketplaces reframing them, (c) ignored positive signals (Google reviews the Overview omits — add AggregateRating/Review schema so they become machine-visible).

5. **llms.txt (the direct agent summary)** — if the site has an `llms.txt` at root, it is the FIRST thing AI agents read to decide who the client is, so it is a top-tier entity surface and the easiest to miss (it is not linked in the nav). Audit it exactly like the rest of the site: no AI framing on the marketing lines, dates consistent with the schema, no stale/renamed URLs, no identity blending (e.g. a "Software Products" section on a photographer's llms.txt tells every agent "photographer + software dev"). A clean, photographer-first llms.txt is one of the highest-leverage, lowest-effort entity fixes. It is also a scored PageSpeed **Agentic Browsing** audit (module 01), so getting it right helps two goals at once.

**VERIFY EVERYTHING (hard gate).** Never relay research-agent output about a client's live pages or bios as fact. Agents hallucinate specific quotes. Confirm every external claim against the live render (browser MCP or authenticated fetch) before it goes into a deliverable or a fix. This rule exists because a hallucinated "bio says X" claim cost real trust on the originating engagement.

---

## EXECUTION SEQUENCE (proven, one clean pass)

1. **Back up** every file before touching it (`_backups/pre-scrub-YYYY-MM-DD/`).
2. **Scrub** copy, meta, keywords, OG/Twitter, JSON-LD schema, alt text — reweight photography/craft keywords in as AI comes out.
3. **Rename AI-slugged URLs** (e.g. `/innovative-ai-driven-creativity/` → `/creative-solutions/`) and add a **301** old→new. Update every internal link + the nav/cards that point at it.
4. **AI-only galleries/pages** the client wants to keep: **noindex** them AND **de-link** them from the primary nav/portfolio, so they exist by URL but stop feeding the crawled entity. Remove them from the sitemap (a noindexed page in a sitemap is a contradictory signal).
5. **Rename AI-named asset folders** (e.g. `/images-master/ai-work/` → `/creative-work/`) — server folder + all refs together.
6. **Sitemap** — bump `lastmod` to today on every changed page (the recrawl signal), swap renamed slugs, drop noindexed/redirecting URLs. Validate as XML.
7. **Force recrawl** — upload sitemap, purge CDN, resubmit in GSC, and URL-Inspect → Request Indexing on the top 4-5 pages.

## VERIFY (before declaring done)
- `grep` for zero AI on marketing surfaces (intentional-keep excluded).
- Validate every edited JSON-LD block parses (`json.loads`).
- Check the client's hard copy rules still hold (e.g. no em dashes — sweep and fix).
- Confirm live: 301s resolve, renamed page 200s clean, sitemap validated.

## MEASURE (weeks, not days)
AI Overviews rebuild on recrawl. Individual pages recache in days; the Overview/entity shifts over 1-3 weeks. Don't judge before the corpus re-reads. Wrong external sources drop out as the client's own signals get cleaner and stronger — you out-signal them, you don't disavow them directly.

---

## OWNED vs CLIENT-ACTION SPLIT
- **You do:** all on-site schema, copy, slug renames, 301s, noindex/de-link, sitemap, review schema, content briefs.
- **Client does (only they have the logins):** the off-site bio rewrites, marketplace profile fixes, name-consistency, GBP, directory submissions. These are often the highest-leverage items, so hand them a precise, checkbox list.
