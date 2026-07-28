# cross-platform-compliance

**Version:** 2.2
**Author:** [Glenski Toolkit](https://example.com)
**License:** CC BY 4.0

Two-layer website compliance skill for desktop-to-mobile compatibility, browser-specific frontend risks, mobile UX, and accessibility release gates.

Works as a normal Codex/Claude skill with no install required for static review. The optional rendered audit uses Playwright.

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
