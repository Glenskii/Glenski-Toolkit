# cross-platform-compliance

**Version:** 2.2
**License:** MIT

A page can look finished in desktop Chrome and still fall apart on an iPhone. Viewport height quirks, tiny tap targets, missing focus states, inputs that trigger iOS zoom, Safari CSS differences and horizontal overflow on narrow screens all hide on a big monitor.

This skill audits your frontend code for those problems before you ship. If you give it a preview URL, it also renders the site at mobile, tablet and desktop sizes and measures what users actually get.

Use it to answer these questions:

- Will the desktop layout hold up on phones and tablets?
- Is there Safari, iOS, Android, Firefox or Edge risk in the CSS or JavaScript?
- Do buttons, links, forms, modals and navigation work by touch?
- Are labels, focus states and zoom support intact?
- Should this page ship, or is mobile or browser breakage blocking it?

You get a verdict, not vague advice. Findings are graded `FAIL`, `WARN`, `NOTE` or `PASS`, and every audit ends with `BLOCKED`, `REVIEW REQUIRED` or `PASS`.

There are two layers. Layer 1 is a static code audit and needs no install. Layer 2 is optional: it uses Playwright for rendered browser checks, screenshots, computed styles and an axe accessibility scan.

## Compatibility

The folder holds a portable `SKILL.md`, bundled scripts and optional compatibility metadata. The core workflow does not depend on any one client.

## What it checks

| Area | Layer 1 Static Audit | Layer 2 Rendered Audit |
|---|---|---|
| Viewport | viewport meta, `100vh`/`dvh`, safe area, keyboard viewport | rendered overflow, screenshots |
| Touch | tap target patterns, hover-only UI, scroll lock risks | measured tap targets |
| CSS | Safari prefixes, flex gap targets, nesting, reduced motion | reduced-motion emulation |
| Images | AVIF fallback, `srcset`, dimensions, lazy loading | screenshots |
| Forms | labels, input types, autocomplete, 16px input floor | computed font-size, axe |
| Accessibility | focus styles, accessible names, modal focus trap | axe scan, rendered focus check |
| Desktop/tablet | `100vw`, tablet breakpoints, mouse-only events, sticky issues | tablet and desktop profiles |

## Severity gate

| Tier | Meaning | Gate |
|---|---|---|
| FAIL | Broken, inaccessible, or likely unusable | `BLOCKED` |
| WARN | Degraded UX or review-required risk | `REVIEW REQUIRED` |
| NOTE | Advisory or manual follow-up | No gate effect |
| PASS | Checked and clean | No action |

Default process behaviour:

- FAIL findings fail the Playwright process once all checks have finished.
- WARN findings give `REVIEW REQUIRED` but do not fail the process.
- Set `COMPLIANCE_FAIL_ON_WARN=1` to fail CI on WARN findings too.

## Layer 1: static audit

No install. Point it at real source files or paste code:

```text
Use $cross-platform-compliance to audit this website for mobile and browser compatibility.
```

## Layer 2, option A: install in the target project

```bash
npm install --save-dev @playwright/test @axe-core/playwright
npx playwright install chromium
```

For multi-engine checks:

```bash
npx playwright install chromium firefox webkit
```

Copy `scripts/compliance-audit.spec.js` into the website project, then run:

```bash
BASE_URL=http://localhost:4173 AUDIT_PATHS="/,/register/,/thanks/" npx playwright test --reporter=list --workers=1
```

PowerShell:

```powershell
$env:BASE_URL='http://localhost:4173'
$env:AUDIT_PATHS='/,/register/,/thanks/'
npx playwright test --reporter=list --workers=1
```

## Layer 2, option B: temporary harness

The bundled wrapper keeps Playwright out of the target project:

```powershell
.\scripts\run-layer2-audit.ps1 -BaseUrl http://localhost:4173 -Paths "/,/register/,/thanks/"
```

Multi-engine:

```powershell
.\scripts\run-layer2-audit.ps1 -BaseUrl http://localhost:4173 -Paths "/" -Browsers "chromium,firefox,webkit"
```

Strict CI mode:

```powershell
.\scripts\run-layer2-audit.ps1 -BaseUrl http://localhost:4173 -Paths "/" -FailOnWarn
```

## Environment options

```text
BASE_URL=http://localhost:4173
AUDIT_PATHS=/,/about/,/contact/
AUDIT_BROWSERS=chromium,firefox,webkit
AUDIT_DISCOVER_LINKS=1
AUDIT_MAX_PAGES=10
AUDIT_OVERFLOW_TOLERANCE=2
COMPLIANCE_FAIL_ON_WARN=1
SCREENSHOT_DIR=./compliance-screenshots
COMPLIANCE_REPORT_PATH=./compliance-report.json
```

## Output

- Screenshots: `./compliance-screenshots/`
- JSON report: `./compliance-report.json`
- Console summary with the final gate: `BLOCKED`, `REVIEW REQUIRED` or `PASS`

## Limit

Playwright's Chromium, Firefox and WebKit widen engine coverage, but they do not replace sign-off on real iOS Safari and Android hardware. Layer 2 is an automated gate for known patterns. It will not catch every device-specific rendering bug.

## Part of the Glenski Toolkit

[github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)
