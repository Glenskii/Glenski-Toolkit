# cross-platform-compliance

**Version:** 2.1 | **Author:** [Glen E. Grant](https://profile.glenegrant.com) | **License:** CC BY 4.0

Two-layer browser and device compliance audit for web frontend code. Layer 1 runs static code analysis — no build required. Layer 2 runs Playwright across six device viewports with screenshot evidence, computed style checks, and axe accessibility scanning. Every audit ends with a compliance gate: **BLOCKED**, **REVIEW REQUIRED**, or **PASS**.

---

## What It Does

Audits HTML, CSS, and JS/TS for known browser-specific bugs, mobile UX failures, accessibility violations, and cross-platform pattern gaps. The two layers catch different things:

- **Layer 1 (static):** finds bad patterns in source code — 100vh without dvh fallback, missing safe-area insets, inputs below 16px, hover-only interactions, missing labels, unsafe @supports nesting, stale vendor prefixes
- **Layer 2 (rendered):** Playwright at 6 viewports — horizontal overflow, computed input font sizes, tap target dimensions, focus visibility, axe WCAG scan, full-page screenshots

---

## Coverage

| Domain | Layer 1 Checks | Layer 2 Checks |
|--------|---------------|----------------|
| Mobile Viewport | 100vh/dvh, safe-area order, 16px input floor, viewport meta, interactive-widget | Input font sizes (computed), screenshot at all viewports |
| Touch | Hover-only states, tap highlight, touch callout, fixed scroll jank, body scroll lock | Tap target dimensions, horizontal overflow |
| CSS Compat | -webkit- prefixes, backdrop-filter, flex gap, @supports nesting, reduced motion | — |
| Images | AVIF/WebP fallback, srcset, image dimensions, lazy loading | — |
| Forms | Input type attributes, label association, autocomplete | Input font size (computed), axe label scan |
| Desktop | Scrollbar width, tablet breakpoints, pointer events, focus outline removal, sticky/overflow, focus traps | Focus visibility, axe scan |
| Accessibility | — | axe WCAG 2.1 AA scan (violations = FAIL, incomplete = WARN, scan errors = WARN) |

Layer 2 also records these report-level manual checks as NOTE findings: fixed/sticky bottom overlap, modal scroll lock, and optional Lighthouse mobile scoring. They are not automated yet and do not affect the compliance gate.

---

## Severity Tiers

| Tier | Meaning | Gate effect |
|------|---------|-------------|
| **FAIL** | Broken or inaccessible on a real device | BLOCKED — must fix before ship |
| **WARN** | Degrades UX on target platform | REVIEW REQUIRED — owner sign-off required |
| **NOTE** | Best practice gap or not-yet-implemented check | No gate effect — advisory only |
| **PASS** | Compliant | Summarised, not listed individually |

Default process behavior: FAIL findings fail the Playwright run. WARN findings produce **REVIEW REQUIRED** in the report but do not fail the process unless `COMPLIANCE_FAIL_ON_WARN=1` is set.

---

## Usage

**Layer 1 — static audit (no setup needed):**
```
/compliance audit [paste code or filename]
```
Paste any HTML, CSS, or JS block into Claude and run the command. Returns tiered findings with exact fixes.

**Layer 2 — rendered audit (requires Playwright):**

```bash
# 1. Install deps in your project
npm install --save-dev @playwright/test @axe-core/playwright
npx playwright install chromium

# 2. Copy compliance-audit.spec.js from this skill's scripts/ folder into your project
# 3. Edit BASE_URL at the top of the script
# 4. Run — always with --workers=1
npx playwright test --reporter=list --workers=1
```

Strict mode for CI pipelines that should fail on WARN findings too:

```bash
COMPLIANCE_FAIL_ON_WARN=1 npx playwright test --reporter=list --workers=1
```

PowerShell:

```powershell
$env:COMPLIANCE_FAIL_ON_WARN='1'; npx playwright test --reporter=list --workers=1
```

Output: screenshots in `./compliance-screenshots/`, JSON report at `./compliance-report.json`, and a full summary with compliance gate in stdout.

---

## Part of the Glenski-Toolkit

[github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit) — skills for professional web development, creative production, and software quality.

Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit: Glen E. Grant — [profile.glenegrant.com](https://profile.glenegrant.com)
