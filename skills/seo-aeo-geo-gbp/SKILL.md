---
name: seo-aeo-geo-gbp
description: Perform an evidence-led search visibility review for a website or local business. Use when auditing technical SEO, page content, structured data, search-result readiness, answer-engine claims, or public business-profile accuracy. Verify current platform guidance from primary sources, separate evidence from recommendations, and never promise rankings, traffic, rich results, or visibility in answer engines.
---

# Search Evidence Audit

Produce a focused audit of what can be verified. Treat this as a decision-support workflow, not a ranking guarantee.

## The problem this solves

Generic search advice too often starts with a guess. This skill starts with the site, the supplied data, and current official guidance. It covers technical discovery, page content, structured data, local-profile accuracy, keyword intent, and answer-engine claims without inventing traffic, rankings, citations, or business facts.

The output must be useful to act on. Every finding states what was checked, what was found, why it matters, what evidence supports it, and the safest next action.

## Required input gate

Collect the following before making project-specific claims:

```yaml
target_url: ""             # A public URL or a local project path
business_type: ""          # local | ecommerce | software | portfolio | publisher | other
market_or_audience: ""     # Country, region, audience, or search market
available_evidence: []      # public URL, crawl export, Search Console, analytics, logs, profile export
```

Useful optional inputs include competitor URLs, priority pages, target queries, a public business-profile URL, and a defined conversion goal.

If no inspectable target or data is available, provide general guidance only. Mark it as `[RECOMMENDATION]`, state the evidence needed, and do not present it as a site finding.

## Evidence tiers

Every finding carries one label:

| Label | Meaning | Use it when |
|---|---|---|
| `[VERIFIED]` | Directly observed in the reviewed page, source, crawl, export, or authorized data. | The evidence identifies the page, asset, or record. |
| `[DOCUMENTED]` | Supported by a current primary source. | A platform rule or technical behavior is cited. |
| `[RECOMMENDATION]` | A reasonable next action without project-specific proof. | The target or data is incomplete. |
| `[UNVERIFIED]` | The question cannot be answered from available evidence. | State the missing evidence. |

Never describe a recommendation as verified. Never convert a third-party tool score into a search-engine verdict.

## Work modules

Select only the modules required by the request. Record modules that were not run and why.

1. **Technical discovery**: inspect status behavior, canonical URLs, robots directives, sitemap references, renderability, internal links, and indexability signals.
2. **Content and intent**: inspect page purpose, headings, visible copy, duplication, helpful structure, and evidence for material claims.
3. **Keyword and competitor review**: map supplied queries and public competitors to search intent. Do not claim volumes, positions, or share without supporting data.
4. **Structured data**: compare syntax, declared type, and properties with the visible page. Produce schema only from owner-approved facts.
5. **Local-profile accuracy**: compare owner-approved public name, category, contact details, hours, and links. Do not infer profile ownership.
6. **Answer-engine review**: assess whether a specific claim is supported by current primary documentation and visible site evidence. Do not promise citations or inclusion.
7. **Measurement review**: inspect supplied Search Console, analytics, crawl, log, or rank-tracking data. State limitations when data is absent.

## Start with the target and scope

Confirm the site or pages to review, the market or audience, available access, and whether the request includes a public business profile. Do not request or record credentials, private addresses, personal contact information, origin IPs, hosting details, internal tickets, or unrelated business data in a public artifact.

If the target cannot be inspected, state the limit and return a checklist of the evidence required. Do not infer crawlability, index coverage, traffic, rankings, or profile ownership from a URL alone.

## Gather evidence

Check only claims that can be supported by the supplied project, an accessible page, or a current primary source.

- Inspect rendered pages and source for titles, headings, canonical URLs, robots directives, internal links, visible content, and structured data.
- Review structured data against the visible page. Do not add facts that are absent, outdated, or unsupported.
- For local business information, compare public name, address, phone, category, hours, and links only when the owner supplies or authorizes that data.
- For claims about Google Search, Google Business Profile, answer-engine features, rich results, or other platforms, check the current official documentation before making a recommendation.
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

## Delivery standards

- Lead with the finding, then the action. Do not bury the decision under theory.
- Order work as Critical, High, Medium, and Low. Severity reflects impact on the reviewed target, not a generic checklist.
- Include the affected URL, file, record, or query wherever the evidence permits it.
- Provide complete, deployable JSON-LD only when the owner has supplied or approved every fact in it. Otherwise provide a field list and the evidence required.
- Cite the exact current primary source for platform-policy and product-behavior claims.
- Keep reusable examples fictional. Use `example.com` and placeholder business details.
- Do not package private analytics, contact details, origin infrastructure, client documents, or internal process notes in a public report.

## Limits

This skill does not guarantee indexing, rankings, traffic, rich results, profile reinstatement, review removal, or answer-engine inclusion. It does not replace a full accessibility audit, security assessment, legal review, or a platform's own policy decision.

## Guardrails

- Do not publish client details, personal details, infrastructure identifiers, analytics exports, credentials, or internal operations notes in reusable examples.
- Do not fabricate citations, rankings, reviews, local coverage, entity relationships, or schema fields.
- Do not use hidden text, misleading markup, doorway pages, review manipulation, or other deceptive tactics.
- Treat platform policy as time-sensitive. Link to the primary policy or documentation used for the conclusion.
- Keep generic reusable examples on `example.com` and use fictional data only.
