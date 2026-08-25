# Search Evidence Reference

## Evidence labels

- `[VERIFIED]`: Directly observed in supplied files, an accessible page, or an authorized data source. Include the URL, file, or date checked.
- `[DOCUMENTED]`: Supported by a current primary platform source. Link to that source.
- `[RECOMMENDATION]`: A reasoned next action based on verified or documented evidence. It is not a promise of ranking or traffic.
- `[UNVERIFIED]`: Plausible but not supported by accessible evidence. State what would confirm it.

## Structured data rule

Structured data must accurately represent visible page content. Validate syntax and check for duplicate or contradictory markup before release. Eligibility or a valid test result does not guarantee a rich result.

## Answer-engine rule

Do not claim that special markup, files, or tactics guarantee inclusion in an answer-engine result. Apply the same fundamentals used for ordinary search: crawlable pages, helpful and accurate content, clear site structure, and truthful structured data. Verify any platform-specific claim against current official documentation.

## Local-profile rule

Use only details the business owner has approved for the purpose. Do not copy a private home address, personal phone number, private email, origin server details, or internal operations notes into a reusable file.

## Report example

```text
[VERIFIED] https://example.com/services has no canonical link element. Checked 2026-08-06.

[DOCUMENTED] The search platform recommends canonical URLs for substantially similar pages. Source: official documentation linked in the report.

[RECOMMENDATION] Add a self-referencing canonical to /services after confirming that it is the preferred public URL.

[UNVERIFIED] Index coverage cannot be confirmed without authorized Search Console access.
```
