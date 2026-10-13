# Search Evidence Audit

This skill audits a website or public business presence for search visibility. Use it when you want findings you can check, not guesses. Every result is labelled by how well it is backed, and nothing here promises rankings, traffic, rich results, or answer-engine inclusion.

It works from what it can see: the site itself, data you supply, and current official guidance. Confirmed findings stay separate from suggested next steps.

## Use it for

- Technical checks: canonical URLs, robots directives, sitemaps, renderability, internal links.
- Page and structured-data reviews, comparing declared markup with what visitors can see.
- Local-profile accuracy checks, using details the owner has approved.
- Claims about search results or answer engines that need current primary-source support.

## Start prompt

```text
Use $seo-aeo-geo-gbp to review this site for search visibility. Start by confirming the target, market, available evidence, and limits. Label each result as verified, documented, recommendation, or unverified.
```

## Evidence labels

Every result carries one of four labels:

| Label | Meaning |
| --- | --- |
| `VERIFIED` | Directly observed in the reviewed site, source, crawl, export, or authorized data. |
| `DOCUMENTED` | Supported by current official documentation. |
| `RECOMMENDATION` | A next step where project-specific proof is incomplete. |
| `UNVERIFIED` | Cannot be answered from the evidence available. |

When the evidence allows, the skill names the page, file, record, or query behind a finding. If the target cannot be inspected, it says what is missing instead of guessing.

## What it does not do

- It does not treat a third-party score as a search-engine verdict.
- It does not present a technical change as a ranking guarantee.
- It keeps private analytics, credentials, client records, and internal infrastructure out of a public report.
- It produces structured data only from facts the owner has supplied or approved.

## Files

- [Core instructions](SKILL.md)
- [Evidence and report standard](references/search-evidence.md)

## License

MIT. See [LICENSE](LICENSE).
