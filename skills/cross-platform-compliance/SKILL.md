---
name: cross-platform-compliance
description: Two-layer browser and device compliance audit for web frontend code. Use when asked to audit, verify, harden, or review websites, landing pages, web apps, React/Next/Vite frontends, static HTML/CSS/JS, or Electron renderers for desktop-to-mobile compatibility, mobile UX failures, browser-specific CSS/JS issues, accessibility regressions, viewport problems, touch target problems, Safari/iOS risks, Android Chrome/Samsung Internet risks, or release readiness. Runs Layer 1 static source review and, when a preview URL is available, Layer 2 Playwright rendered checks with screenshots, computed styles, axe accessibility scan, and a final BLOCKED / REVIEW REQUIRED / PASS gate.
license: CC BY 4.0
metadata:
  title: CROSS-PLATFORM BROWSER COMPLIANCE AUDIT SKILL
  version: "2.2"
  author: Glenski Toolkit
  website: https://example.com
  repo: https://github.com/Glenskii/Glenski-Toolkit
  compatible_with:
    - HTML/CSS/JS static sites
    - React / Next.js / Vite
    - Electron renderer
    - Cloudflare Pages
    - Any web frontend code
  tags:
    - browser-compatibility
    - cross-platform
    - mobile
    - css
    - playwright
    - accessibility
    - audit
    - glenski
---

# Cross-Platform Compliance

Audit real frontend code for desktop-to-mobile compatibility before release. Run two layers:

1. Layer 1: static source audit from HTML, CSS, JS, TS, JSX, TSX, and framework files.
2. Layer 2: rendered audit with `scripts/compliance-audit.spec.js` when a local or live preview URL is available.

The final audit verdict must be one of:

- `BLOCKED`: one or more FAIL findings remain.
- `REVIEW REQUIRED`: no FAIL findings, but WARN findings remain and need owner sign-off.
- `PASS`: no FAIL or WARN findings. NOTE findings are advisory.

## Platform Scope

Default targets unless the project specifies otherwise:

```yaml
targets:
  ios_safari_min: "16"
  android_chrome_min: "120"
  samsung_internet_min: "23"
  desktop_safari_min: "16"
  firefox_min: "120"
  edge_min: "120"

project:
  type: "static | react | nextjs | vite | electron | cloudflare-pages | other"
  build_cmd: ""
  preview_cmd: ""
  base_url: ""
  entry_html: ""
```

When browser support facts matter, verify them against current MDN Browser Compatibility Data, Can I Use, or the project's Browserslist config. Do not rely on old support notes.

Useful commands:

```bash
npx update-browserslist-db@latest
npx browserslist
```

## Required Workflow

1. Identify project type, key entry pages, build command, preview command, and target browsers.
2. Run Layer 1 static audit always.
3. If a preview URL can be served safely, run Layer 2 with the companion Playwright runner.
4. Compile findings by severity with exact file/line or rendered evidence.
5. End with the compliance gate.

Do not audit from descriptions. Use real source files, pasted code, or a real preview URL.

## Layer 1 Static Audit

Read source files directly. Report file path and line number where possible.

### 1. Mobile Viewport

- FAIL: missing `<meta name="viewport">`.
- FAIL: `user-scalable=no`.
- WARN: `maximum-scale` below `2`.
- WARN: `interactive-widget=resizes-content` missing only when fixed bottom UI must remain visible above the Android virtual keyboard and Android Chrome 108+ is a target.
- FAIL: `height: 100vh` as the sole full-screen height for heroes, modals, wrappers, splash screens, or app shells.
- PASS: `height: 100vh` fallback followed by `height: 100dvh`.
- WARN: `dvh`, `svh`, or `lvh` without fallback when supporting browsers older than Safari 15.4, Chrome/Edge 108, or Firefox 101.
- FAIL: fixed/sticky bottom UI without safe-area padding when content reaches device edges.
- WARN: `viewport-fit=cover` missing when edge-to-edge UI depends on safe-area insets.
- FAIL: form controls with declared or inherited font-size below `16px`.

Safe-area order:

```css
.bottom-bar {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
```

### 2. Touch and Input

- WARN: interactive controls below 44x44 CSS px effective tap area.
- FAIL: interaction available only through `:hover` without focus, click, tap, or disclosure alternative.
- NOTE: hover behavior should be scoped with `(hover: hover)` where it is not needed on touch.
- NOTE: custom tap UI missing `-webkit-tap-highlight-color` reset when visual polish matters.
- NOTE: interactive images missing `-webkit-touch-callout: none` where long-press menus interrupt the action.
- WARN: custom drag/swipe UI missing `touch-action`.
- WARN: modal/drawer/sheet that does not lock body scroll.
- FAIL: scroll lock implementation that resets or loses page scroll position on close.

### 3. CSS Compatibility

- WARN: `-webkit-text-size-adjust: 100%` missing from `html` or `body`.
- WARN: `backdrop-filter` without `-webkit-backdrop-filter` when Safari support is required.
- WARN: flex `gap` when supporting Safari below 14.1.
- WARN: nested `@supports` inside a rule block in plain CSS without a compiler that handles nesting.
- WARN: animation/transition/auto-play effects without `prefers-reduced-motion` handling.
- FAIL: animation longer than 3 seconds without reduced-motion override when it affects essential UI or accessibility.
- NOTE: modern selectors such as `:has()` are broadly supported in current browsers, but still verify against the target matrix when older browsers matter.

### 4. Images and Media

- WARN: direct AVIF image use without fallback when unsupported browsers are in scope.
- WARN: large content images missing `srcset` and `sizes`.
- WARN: images missing intrinsic `width` and `height`.
- NOTE: below-fold images missing `loading="lazy"`.
- WARN: CSS background images used as essential content without accessible text alternative.
- WARN: autoplaying video/audio without reduced-motion or user-control consideration.

### 5. Forms and Accessibility

- FAIL: input/select/textarea missing an associated label, `aria-label`, or `aria-labelledby`.
- WARN: missing or generic input `type` where mobile keyboards would improve entry.
- NOTE: missing `autocomplete` on personal-data fields.
- FAIL: `outline: none` / `outline: 0` on interactive elements without visible replacement focus style.
- WARN: modal/dialog/drawer without focus trap.
- WARN: icon-only button or link without accessible name.

### 6. Desktop and Tablet Gotchas

- WARN: `width: 100vw` on full-width layout elements because desktop scrollbars can create horizontal overflow.
- WARN: breakpoints treating 768px or 1024px as desktop without hover/pointer checks.
- WARN: mouse-only JavaScript (`mousedown`, `mousemove`, `mouseup`) without pointer/touch equivalent.
- WARN: sticky headers without `scroll-margin-top` on anchor targets.
- WARN: `position: sticky` inside overflow ancestors that prevent sticky behavior.

## Layer 2 Rendered Audit

Use `scripts/compliance-audit.spec.js` when a preview URL exists. It is optional for using the skill, but required for rendered compliance evidence.

Default behavior:

- FAIL findings produce `BLOCKED` and fail the Playwright run after all checks complete.
- WARN findings produce `REVIEW REQUIRED` but do not fail the process by default.
- Set `COMPLIANCE_FAIL_ON_WARN=1` to fail on WARN findings too.
- NOTE findings are advisory.

Install in the target project or a temporary audit harness:

```bash
npm install --save-dev @playwright/test @axe-core/playwright
npx playwright install chromium
```

For multi-engine checks:

```bash
npx playwright install chromium firefox webkit
```

Run:

```bash
BASE_URL=http://localhost:4173 AUDIT_PATHS="/,/register/,/thanks/" npx playwright test --reporter=list --workers=1
```

PowerShell:

```powershell
$env:BASE_URL='http://localhost:4173'
$env:AUDIT_PATHS='/,/register/,/thanks/'
npx playwright test --reporter=list --workers=1
```

Useful environment options:

```text
AUDIT_BROWSERS=chromium                  # chromium | firefox | webkit | comma-separated
AUDIT_PATHS=/,/about/,/contact/
AUDIT_OVERFLOW_TOLERANCE=2
AUDIT_DISCOVER_LINKS=1
AUDIT_MAX_PAGES=10
COMPLIANCE_FAIL_ON_WARN=1
```

Layer 2 automated checks:

- L2-1 horizontal overflow with configurable tolerance.
- L2-2 tap target measurement from rendered boxes.
- L2-3 computed input/select/textarea font-size.
- L2-4 visible focus indicator.
- L2-5 axe accessibility scan.
- L2-6 screenshots for each page/profile/browser combination.

Layer 2 report-level manual notes:

- L2-7 fixed/sticky bottom overlap.
- L2-8 modal scroll lock.
- L2-9 Lighthouse mobile.

Playwright WebKit is useful for engine coverage, but it is not a replacement for real iOS Safari hardware testing.

## Evidence Format

Every finding should include:

```text
[FAIL|WARN|NOTE] CHECK-ID: Short description
Detection: Static file:line | Rendered browser/profile/page/screenshot
Browser affected: specific browser names, never "All browsers"
Location: file:line, selector, or rendered element
Issue: concrete failure and user impact
Fix: exact code or exact next action
Verified by: static inspection, Playwright, axe, screenshot, or manual check
```

If an issue affects every supported target, list them explicitly: Chrome, Safari iOS, Safari macOS, Firefox, Edge, Samsung Internet.

## Report Format

```text
CROSS-PLATFORM COMPLIANCE AUDIT
Project: [name]
Entry: [URL or file]
Date: [date]
Layer 1: [complete | partial - reason]
Layer 2: [complete | skipped - reason]

FAIL FINDINGS
[findings]

WARN FINDINGS
[findings]

NOTE FINDINGS
[findings]

PASSES
[short grouped pass summary]

COMPLIANCE GATE
FAIL count: [N]
WARN count: [N]
NOTE count: [N]
STATUS: [BLOCKED | REVIEW REQUIRED | PASS]
```

## Operating Rules

- Run against real code or a real URL.
- Every FAIL must include a paste-ready fix or exact next action.
- Do not claim full Safari/iOS coverage from Chromium viewport emulation.
- Do not silently skip Layer 2 failures. State why Layer 2 was skipped or incomplete.
- Keep findings minimal and actionable. Prefer fewer high-confidence issues over noisy generic advice.
- A PASS audit means checked patterns passed. It does not replace real-device iOS and Android sign-off.
