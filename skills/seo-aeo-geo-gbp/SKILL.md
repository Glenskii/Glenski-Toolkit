---
name: seo-aeo-geo-gbp
description: Perform an evidence-led search visibility review for a website or local business. Use when auditing technical SEO, page content, structured data, search-result readiness, AI-search claims, or public business-profile accuracy. Verify current platform guidance from primary sources, separate evidence from recommendations, and never promise rankings, traffic, rich results, or AI visibility.
---

# Search Evidence Audit

Produce a focused audit of what can be verified. Treat this as a decision-support workflow, not a ranking guarantee.

## Start with the target and scope

Confirm the site or pages to review, the market or audience, available access, and whether the request includes a public business profile. Do not request or record credentials, private addresses, personal contact information, origin IPs, hosting details, internal tickets, or unrelated business data in a public artifact.

If the target cannot be inspected, state the limit and return a checklist of the evidence required. Do not infer crawlability, index coverage, traffic, rankings, or profile ownership from a URL alone.

## Gather evidence

Check only claims that can be supported by the supplied project, an accessible page, or a current primary source.

- Inspect rendered pages and source for titles, headings, canonical URLs, robots directives, internal links, visible content, and structured data.
- Review structured data against the visible page. Do not add facts that are absent, outdated, or unsupported.
- For local business information, compare public name, address, phone, category, hours, and links only when the owner supplies or authorizes that data.
- For claims about Google Search, Google Business Profile, AI search features, rich results, or other platforms, check the current official documentation before making a recommendation.
- Label every finding as `[VERIFIED]`, `[DOCUMENTED]`, `[RECOMMENDATION]`, or `[UNVERIFIED]`.

Read [references/search-evidence.md](references/search-evidence.md) for the evidence standard and report format.

## Evaluate the work

Group findings by impact and confidence.

1. Technical discovery: indexability signals, canonical consistency, robots directives, status behavior, rendering blockers, and internal linking.
2. Page usefulness: clear purpose, accurate headings, original visible copy, helpful structure, and evidence for important claims.
3. Structured data: valid syntax, matching visible content, appropriate type selection, and no duplicate or contradictory markup.
4. Local profile accuracy: only public details the owner has approved, consistent across the reviewed sources.
5. Measurement: available Search Console, analytics, log, or rank-tracking evidence. Mark unavailable data as unverified.

Do not treat a score from a third-party tool as a search-engine verdict. Do not describe AEO or GEO as separate technical requirements unless a current primary source supports the specific claim.

## Return a usable report

Use this structure:

```text
Scope and limits

Evidence reviewed

Verified findings

Recommendations

Unverified items and the evidence needed

Priority order

Expected outcome and limits
```

Each recommendation must name the page or asset, the reason, the supporting evidence, and the safe next action. Say plainly when an outcome cannot be guaranteed.

## Guardrails

- Do not publish client details, personal details, infrastructure identifiers, analytics exports, credentials, or internal operations notes in reusable examples.
- Do not fabricate citations, rankings, reviews, local coverage, entity relationships, or schema fields.
- Do not use hidden text, misleading markup, doorway pages, review manipulation, or other deceptive tactics.
- Treat platform policy as time-sensitive. Link to the primary policy or documentation used for the conclusion.
- Keep generic reusable examples on `example.com` and use fictional data only.
