# MODULE 01: TECHNICAL SEO AUDIT
**Skill:** seo-aeo-geo-gbp v2.1.0
**Trigger:** `/seo audit [url]`

---

## PURPOSE

Produce a prioritized technical SEO audit with evidence-tiered findings. Every finding is labelled E1 (live data), E2 (authoritative reference), or E3 (best practice). Every finding has a specific fix — not "consider improving."

---

## INPUT REQUIREMENTS

Before running this module, confirm:

```yaml
required:
  - target_url          # Full URL to audit (domain root or specific page)
  - at_least_one_of:
    - screaming_frog_crawl_export   # .csv from Screaming Frog crawl
    - gsc_coverage_report           # Google Search Console Coverage export
    - ga4_export                    # GA4 traffic/behavior data
    - live_url_access               # Will fetch and analyze live pages directly

optional:
  - competitor_urls       # For benchmark comparisons
  - sitemap_url           # If not at /sitemap.xml
  - robots_txt_content    # If custom location
```

If only `target_url` is provided with no data source: proceed with live fetch analysis (E1 for what can be observed live) + E3 for anything requiring crawl data. Clearly label the difference.

---

## AUDIT EXECUTION SEQUENCE

### PHASE 1 — CRAWLABILITY & INDEXATION

**1.1 Robots.txt Analysis**
Fetch `[target_url]/robots.txt`. Check:
- [ ] File exists and is valid
- [ ] No critical paths accidentally blocked (`Disallow: /`)
- [ ] Sitemap declared: `Sitemap: https://...`
- [ ] User-agent rules are intentional (wildcard `*` vs specific bots)

**Output format per finding:**
```
FINDING [CRITICAL|HIGH|MED|LOW] [E1|E2|E3]
Location: robots.txt line X
Issue: [specific description]
Fix: [exact string or action]
```

**1.2 XML Sitemap**
Fetch declared sitemap URL. Check:
- [ ] Sitemap exists and is valid XML
- [ ] All URLs return 200 (no 301/404/410 in sitemap)
- [ ] `lastmod` dates are present and reasonable (not all identical, not all >1 year old)
- [ ] `changefreq` and `priority` set (optional but useful)
- [ ] No noindexed pages included in sitemap
- [ ] Sitemap submitted in Google Search Console

**1.3 Crawl Depth Analysis** *(Screaming Frog data required for E1)*
- [ ] No important pages deeper than 3 clicks from root
- [ ] Orphaned pages (no internal links pointing to them)
- [ ] Crawl traps (infinite parameter strings, session IDs in URLs)

---

### PHASE 2 — INDEXATION STATUS

**2.1 Index Coverage** *(GSC data required for E1)*
Pull from GSC Coverage report:
- Error count and types (Server errors, Redirect errors, Not found)
- Valid with warnings (Submitted and indexed / Discovered but not indexed)
- Excluded pages (Noindexed, Duplicate without canonical, Crawl anomaly)

Flag anything in "Discovered but not indexed" — this is Google's signal that the content is low value or the site has crawl budget issues.

**2.2 Canonical Tags**
Check every page sampled:
- [ ] `<link rel="canonical">` present
- [ ] Canonical points to itself (self-referencing) for unique pages
- [ ] No canonical chains (canonical pointing to a page that itself has a different canonical)
- [ ] HTTPS canonical on HTTPS pages (no HTTP canonical on HTTPS page)
- [ ] Canonical matches the URL shown in sitemap

**2.3 Meta Robots**
Check for accidental `noindex`:
- [ ] No `<meta name="robots" content="noindex">` on pages meant to be indexed
- [ ] No `X-Robots-Tag: noindex` in HTTP headers on indexable pages
- [ ] Pagination handled correctly (no noindex on paginated pages that should be indexed)

---

### PHASE 3 — ON-PAGE FUNDAMENTALS

For each page audited, produce this table:

```
PAGE: [URL]
─────────────────────────────────────────────────────
Title tag:          [current] → [recommended if issue]
Length:             [char count] [PASS/FAIL: max 60]
Meta description:   [current] → [recommended if issue]
Length:             [char count] [PASS/FAIL: max 155]
H1:                 [current] [PASS/FAIL: exactly 1 H1]
H1 keyword match:   [primary keyword present? YES/NO]
H2 count:           [count] [structure note]
Image alt text:     [count missing] / [total images]
Internal links:     [count] [any broken?]
─────────────────────────────────────────────────────
```

**Title Tag Rules** `[E2-REF: Google Search Central]`:
- 50-60 characters (Google typically truncates at ~60)
- Format: `Primary Keyword | Brand Name` or `Primary Keyword — City | Brand`
- Front-load the keyword (Google reads left-to-right, truncates right)
- Unique per page — no duplicate titles

**Meta Description Rules** `[E2-REF: Google Search Central]`:
- 150-155 characters max
- Include primary keyword naturally
- Include a clear action (what will the user get/do?)
- Unique per page — duplicate meta descriptions are a quality signal issue

---

### PHASE 4 — TECHNICAL PERFORMANCE

**4.1 Core Web Vitals** *(E1 if GSC CWV data provided, E3 otherwise)*

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | <2.5s | 2.5–4s | >4s |
| INP (Interaction to Next Paint) | <200ms | 200–500ms | >500ms |
| CLS (Cumulative Layout Shift) | <0.1 | 0.1–0.25 | >0.25 |

For each failing metric, identify the likely cause:
- LCP slow: large hero images not preloaded, render-blocking resources, slow TTFB
- INP high: heavy JavaScript on interaction, long tasks blocking main thread
- CLS high: images without dimensions, late-loading fonts, injected content

**4.2 Page Speed — Mobile Priority**

Cloudflare Pages sites (Glen's stack): confirm the following are in place:
- [ ] AVIF images served with correct `Content-Type: image/avif`
- [ ] Cloudflare Rocket Loader not interfering with critical scripts
- [ ] Cloudflare Polish enabled (automatic image optimization)
- [ ] Cache-Control headers appropriate (static assets: long TTL, HTML: short)
- [ ] Critical CSS inlined in `<head>` (no render-blocking stylesheets)

**4.3 Mobile Usability**
- [ ] Viewport meta tag present: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] No horizontal scroll on 375px viewport
- [ ] Tap targets minimum 48x48px (especially navigation, CTAs)
- [ ] Font size minimum 16px on body text (never 12px/14px body copy)
- [ ] No intrusive interstitials (pop-ups that block content on mobile)

---

### PHASE 5 — SECURITY & TRUST SIGNALS

**5.1 HTTPS**
- [ ] Full site on HTTPS (no mixed content)
- [ ] HTTP redirects to HTTPS (301, not 302)
- [ ] HSTS header present (for established sites)
- [ ] SSL certificate valid and not expiring within 30 days

**5.2 Structured Data Presence**
Check what schema types are currently implemented:
- [ ] Organization or LocalBusiness schema
- [ ] Person schema (for personal brands)
- [ ] BreadcrumbList on interior pages
- [ ] FAQPage where applicable
- [ ] Product/SoftwareApplication on product pages

For each missing schema type that would apply: flag as HIGH priority and route to `/seo schema`.

---

### PHASE 6 — LINK ARCHITECTURE

**6.1 Internal Linking**
- [ ] No broken internal links (404 on internal hrefs)
- [ ] No redirect chains in internal links (link directly to final URL)
- [ ] Anchor text is descriptive (not "click here", "read more")
- [ ] Priority pages have the most internal links pointing to them
- [ ] Footer links not overlapping to the point of keyword dilution

**6.2 External Link Health**
- [ ] No outbound links to 404/gone domains
- [ ] `rel="nofollow"` or `rel="sponsored"` on commercial links where appropriate
- [ ] Affiliate links use `rel="sponsored"`

---

## AUDIT OUTPUT FORMAT

Deliver findings in this structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEO AUDIT REPORT
Site: [target_url]
Audit Date: [date]
Data Sources: [list what was provided]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL FINDINGS (fix before anything else)
[#] [E1/E2/E3] [description] → [exact fix]

HIGH PRIORITY FINDINGS
[#] [E1/E2/E3] [description] → [exact fix]

MEDIUM PRIORITY FINDINGS
[#] [E1/E2/E3] [description] → [exact fix]

LOW PRIORITY / POLISH
[#] [E1/E2/E3] [description] → [exact fix]

PASSES (confirm these are in place)
[list of passing checks]

RECOMMENDED NEXT MODULES
→ /seo schema [url]     if schema gaps found
→ /seo keywords [url]   if title/H1 targets need verification
→ /seo aeo [url]        if AI Overview presence is a goal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLEN-SPECIFIC AUDIT NOTES

When auditing Glen's properties, apply these known constraints and watch for these patterns:

**glenegrant.com (WordPress + Cloudflare + Hostinger)**
- Origin: 157.173.209.121 (Hostinger). Edge: Cloudflare CDN.
- Known issue: `.htaccess` has known 403 pattern on some paths — do not recommend wholesale `.htaccess` changes; flag as "surgical edit required."
- WordPress pages being replaced by standalone HTML files in subdirectories — check that WP pages are correctly 301'd to HTML overrides where applicable
- RankMath installed — check that it's not generating duplicate schema conflicting with hand-written JSON-LD

**profile.glenegrant.com (Static HTML, Cloudflare Pages)**
- No CMS — all HTML static. Pure Cloudflare Pages deployment.
- AVIF images throughout — confirm correct MIME types served
- Target LCP: <2s on mobile

**Cloudflare Pages sites generally:**
- Confirm `_headers` file sets correct security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- Confirm `_redirects` file handles any needed 301s
- No server-side rendering — all meta tags must be in static HTML

**ideathreader.com**
- Has active 403 issue — any audit findings here should note the .htaccess constraint
- Do not recommend changes that require wholesale .htaccess edits
