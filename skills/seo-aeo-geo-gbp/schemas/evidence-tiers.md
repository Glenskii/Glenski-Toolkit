# Evidence Tier Reference
**Skill:** seo-aeo-geo-gbp v2.1.0

---

## THE EVIDENCE TIER SYSTEM

Every finding and recommendation in this skill carries an evidence label. This is not optional. The tier tells the user how much to trust a finding and what verification is needed before acting on it.

---

## TIER DEFINITIONS

### E1 — VERIFIED `[E1-VERIFIED]`

**Definition:** Finding is drawn from live, project-specific data that has been directly observed or provided.

**Acceptable E1 sources:**
- Google Search Console export (queries, impressions, clicks, positions, coverage, Core Web Vitals)
- GA4 export (traffic, landing pages, conversion data)
- Screaming Frog crawl export (all URLs, status codes, titles, meta, H1s, canonical, etc.)
- Semrush or Ahrefs export (keyword positions, backlinks, domain metrics)
- GBP Insights export (views, searches, actions, photo views)
- Live URL fetch — content of the actual page as it renders right now
- Direct observation of SERP (screenshot or live test — date-stamped)

**How to label:** `[E1-VERIFIED: source name]`
Example: `[E1-VERIFIED: GSC export 2026-05-15]`

**Rule:** If a finding is labeled E1, a specific data source must be cited. "I'm confident this is E1" without a data source is not E1.

---

### E2 — AUTHORITATIVE REFERENCE `[E2-REF]`

**Definition:** Finding is supported by authoritative external reference — official Google documentation, confirmed Google policy, established industry research with a citable source.

**Acceptable E2 sources:**
- Google Search Central documentation (developers.google.com/search)
- Google Business Profile official policy documentation
- Google Quality Rater Guidelines (official published document)
- Google Core Web Vitals documentation
- Official FTC ruling or regulatory document
- Published research from Sistrix, Ahrefs, Moz, BrightLocal (with source URL cited)
- Schema.org specification

**How to label:** `[E2-REF: source name or URL]`
Example: `[E2-REF: Google Search Central — robots.txt documentation]`
Example: `[E2-REF: FTC Rule on Consumer Reviews, August 2024]`

**Rule:** If a finding is labeled E2, the source must be named. "Google says" without a documentation URL is not E2 — it's E3.

---

### E3 — BEST PRACTICE `[E3-BEST-PRACTICE]`

**Definition:** Industry consensus, common recommendation, or pattern observed across the industry — but not backed by project-specific data or a citable authoritative source.

**When E3 applies:**
- Volume estimates when no keyword tool data is provided
- Competitive difficulty assessments without tool data
- General "this usually works" recommendations
- Any finding where the basis is "this is generally true for most sites"

**How to label:** `[E3-BEST-PRACTICE]`

**Required disclaimer when using E3 for a critical recommendation:**
> "This is an E3 best-practice recommendation. Verify against your GSC, Semrush, or Screaming Frog data before implementing."

**Rule:** E3 findings are useful starting points. They should never be presented as confirmed facts about the specific site being analyzed.

---

## EVIDENCE ESCALATION

When new data is provided, escalate findings:

| Initial tier | New data provided | Action |
|-------------|-------------------|--------|
| E3 (no data) | GSC export received | Re-run affected module, promote findings to E1 |
| E3 (no data) | Semrush export received | Re-run keyword research, promote volume data to E1 |
| E2 (doc reference) | Live test confirms behavior | Promote to E1 for the specific site |
| E1 (old data) | Data is >90 days old | Downgrade to E2 or E3 with date noted, request fresh data |

---

## WHAT NEVER QUALIFIES AS E1 OR E2

These sources produce unreliable data and must be flagged as E3 at best:

- Unsourced "industry statistics" from blog posts
- AI-generated keyword volume estimates (from any AI tool that hasn't pulled live API data)
- "I believe this site ranks for X" without checking
- Historical data >6 months old presented as current rankings
- Competitor data inferred from content alone (needs tool data for E1)
- Any metric labeled "estimated" by the tool itself (e.g., Semrush "estimated" traffic)

**For estimated metrics from tools:** Label as `[E2-EST: Semrush estimate, may differ from actual]` — this acknowledges the source while noting uncertainty.

---

## APPLYING TIERS IN PRACTICE

**Correct:**
```
The homepage title tag is 72 characters long — 12 over the 60-character target.
[E1-VERIFIED: Screaming Frog crawl 2026-05-15] [E2-REF: Google Search Central title guidelines]
Fix: Trim to "Toronto Commercial Photographer | Glen E. Grant Creative" (58 chars)
```

**Incorrect:**
```
Your title tag is probably too long. Google usually truncates around 60 characters.
You should make it shorter.
```

The incorrect version makes claims without evidence tiers, doesn't state the actual finding with specifics, and gives a vague recommendation instead of an exact fix.
