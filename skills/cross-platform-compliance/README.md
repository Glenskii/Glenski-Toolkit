# cross-platform-compliance

**Version:** 2.2
**Author:** [Glenski Toolkit](https://example.com)
**License:** CC BY 4.0

Most website bugs do not show up while building on a desktop screen. A page can look finished in Chrome, then break on an iPhone because of viewport height behavior, tiny tap targets, hidden focus states, form inputs that trigger iOS zoom, Safari CSS differences, or simple horizontal overflow on narrow screens.

`cross-platform-compliance` gives Codex or Claude Code a structured way to catch those problems before a site ships. It audits real frontend code and, when a preview URL is available, renders the site at mobile, tablet, and desktop sizes to measure what users actually get.

Use this skill when you need to answer practical release questions:

- Will the desktop layout still work on phones and tablets?
- Are there Safari, iOS, Android, Firefox, or Edge risks hiding in the CSS or JavaScript?
- Are buttons, links, forms, modals, and navigation usable on touch devices?
- Are accessibility basics such as labels, focus states, and zoom support intact?
- Should this page ship, or is it blocked by mobile/browser issues?

The benefit is a release-style verdict instead of vague advice. Findings are grouped as `FAIL`, `WARN`, `NOTE`, or `PASS`, and every audit ends with `BLOCKED`, `REVIEW REQUIRED`, or `PASS`.

Layer 1 works as a normal Codex or Claude skill with no install required. Layer 2 is optional and uses Playwright for rendered browser checks, screenshots, computed styles, and axe accessibility scanning.

## Compatibility

This folder is designed for both:

- **Codex skills:** valid `SKILL.md` frontmatter, optional `agents/openai.yaml`, bundled scripts.
- **Anthropic / Claude Code skills:** normal `SKILL.md` instructions plus reusable scripts.

## What It Checks

| Area | Layer 1 Static Audit | Layer 2 Rendered Audit |
|---|---|---|
| Viewport | viewport meta, `100vh`/`dvh`, safe area, keyboard viewport | rendered overflow, screenshots |
| Touch | tap target patterns, hover-only UI, scroll lock risks | measured tap targets |
| CSS | Safari prefixes, flex gap targets, nesting, reduced motion | reduced-motion emulation |
| Images | AVIF fallback, `srcset`, dimensions, lazy loading | screenshots |
| Forms | labels, input types, autocomplete, 16px input floor | computed font-size, axe |
| Accessibility | focus styles, accessible names, modal focus trap | axe scan, rendered focus check |
| Desktop/tablet | `100vw`, tablet breakpoints, mouse-only events, sticky issues | tablet and desktop profiles |

## Severity Gate

| Tier | Meaning | Gate |
|---|---|---|
| FAIL | Broken, inaccessible, or likely unusable | `BLOCKED` |
| WARN | Degraded UX or review-required risk | `REVIEW REQUIRED` |
| NOTE | Advisory or manual follow-up | No gate effect |
| PASS | Checked and clean | No action |

Default process behavior:

- FAIL findings fail the Playwright process after all checks complete.
- WARN findings produce `REVIEW REQUIRED` but do not fail the process.
- Set `COMPLIANCE_FAIL_ON_WARN=1` to fail CI on WARN findings too.

## Layer 1 Usage

No install required. Use the skill in Codex or Claude Code against real source files or pasted code:

```text
Use $cross-platform-compliance to audit this website for mobile and browser compatibility.
```

## Layer 2 Option A: Install In The Target Project

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

## Layer 2 Option B: Temporary Harness

Use the bundled wrapper to avoid adding Playwright to the target project:

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

## Environment Options

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
- Console summary with final gate: `BLOCKED`, `REVIEW REQUIRED`, or `PASS`

## Important Limit

Playwright Chromium, Firefox, and WebKit improve engine coverage, but they do not replace real iOS Safari and Android hardware sign-off. Treat Layer 2 as an automated release gate for known patterns, not as a guarantee that every device-specific rendering issue is caught.

## Part Of The Glenski Toolkit

[github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)
