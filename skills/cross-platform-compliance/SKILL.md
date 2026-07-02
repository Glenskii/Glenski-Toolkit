---
name: "cross-platform-compliance"
title: "CROSS-PLATFORM BROWSER COMPLIANCE AUDIT SKILL"
version: "2.1"
description: >
  Two-layer browser and device compliance audit for web frontend code. Layer 1:
  static code analysis — find bad CSS/HTML/JS patterns without running the project.
  Layer 2: rendered device audit — Playwright viewports, screenshot evidence,
  axe accessibility scan, horizontal overflow detection, and computed style checks.
  Fires on demand against existing code. Returns evidence-tiered findings with a
  final compliance gate: BLOCKED / REVIEW REQUIRED / PASS.
author: "Glen E. Grant"
website: "https://glenegrant.com"
compatible_with:
  - "HTML/CSS/JS — static sites"
  - "React / Next.js"
  - "Electron renderer"
  - "Any web frontend code"
license: "CC BY 4.0"
repo: "https://github.com/Glenskii/Glenski-Toolkit"
tags:
  - "browser-compatibility"
  - "cross-platform"
  - "mobile"
  - "css"
  - "playwright"
  - "audit"
  - "glenski"
---

## THE PROBLEM THIS SOLVES

AI tools write for Chrome. Chrome is not the web. iOS Safari runs on every iPhone
and iPad regardless of which browser the user installs — Chrome on iOS is WebKit
under the hood. The 100vh bug, safe area insets, input zoom at under 16px, hover
states that never fire on touch, backdrop-filter without -webkit-prefix — none of
these surface in Chrome DevTools. DevTools lie. Real devices don't.

v1.0 of this skill was a useful checklist. Experienced engineers can read it and
audit manually. That is not enough. v2.1 is an executable compliance runner: two
layers, defined execution order, Playwright evidence, and a hard compliance gate
that outputs BLOCKED, REVIEW REQUIRED, or PASS. The audit either runs or it
explains exactly why it cannot.

---

## SEVERITY TIERS

| Tier | Meaning | Action |
|------|---------|--------|
| FAIL | Will break or completely fail on the target platform. Layout collapses, interaction blocked, content unreachable. | Non-negotiable fix before ship. |
| WARN | Degrades UX on target platform. Noticeable jank, mis-sizing, inaccessible interaction. | Fix before ship unless explicitly accepted and documented with owner sign-off. |
| NOTE | Best practice gap. Non-critical. Does not break the experience. | Address in next pass. |
| PASS | Compliant. Do not list individual PASS items — summarise at end: "Groups 1, 3, 4 — all checks passed." |

---

## TARGET CONFIGURATION

Before any audit begins, confirm or establish this config block. If not provided
by the user, ask for it — do not assume defaults.

```yaml
targets:
  ios_safari_min: "16"         # Minimum iOS Safari version to support
  android_chrome_min: "120"    # Minimum Android Chrome version
  samsung_internet_min: "23"   # Minimum Samsung Internet version
  desktop_safari_min: "16"     # Minimum macOS Safari version
  firefox_min: "120"           # Minimum Firefox version
  edge_min: "120"              # Minimum Edge version

project:
  type: ""          # "static" | "react" | "nextjs" | "electron" | "other"
  build_cmd: ""     # e.g., "npm run build" — leave blank if not applicable
  preview_cmd: ""   # e.g., "npm run preview" or "npx serve dist"
  base_url: ""      # e.g., "http://localhost:4173"
  entry_html: ""    # e.g., "dist/index.html" or "index.html"

layer2_available: false  # Set true when Playwright is available in the project
```

**Browser support lookups:** When rules reference CSS property support or prefix
requirements, verify against MDN Browser Compatibility Data (developer.mozilla.org)
or caniuse.com with the target versions above. Do not rely on hardcoded support
notes in this skill — they age. Quick check command (requires browserslist):

```bash
npx browserslist "ios_saf >= 16, chrome >= 120, firefox >= 120, edge >= 120, samsung >= 23"
npx update-browserslist-db@latest  # keep the db current before any audit
```

---

## AUDIT EXECUTION WORKFLOW

### STEP 1 — TRIAGE

1. Identify project type and confirm target config
2. Confirm whether Layer 2 (Playwright) is available: check for `playwright` in
   package.json, or offer to generate the companion script
3. Run Layer 1 (static) always
4. Run Layer 2 (rendered) when preview server is available

### STEP 2 — LAYER 1: STATIC CODE AUDIT

Read HTML, CSS, and JS/TS files directly. Flag issues by file path and line
number where possible. This layer catches structural and pattern-based failures
that do not require rendering.

### STEP 3 — LAYER 2: RENDERED DEVICE AUDIT

Start preview server if available, then run Playwright checks at the six required
viewports. See Layer 2 section for full execution spec.

### STEP 4 — COMPILE FINDINGS AND GATE

Produce the final findings report and compliance gate output.

---

## LAYER 1: STATIC CODE AUDIT

### GROUP 1 — MOBILE VIEWPORT

**1.1 Viewport Meta Tag**
- FAIL: `<meta name="viewport">` missing from `<head>`
- FAIL: `user-scalable=no` present (WCAG 1.4.4 violation — prevents zoom for
  low-vision users)
- WARN: `interactive-widget=resizes-content` not set on pages with fixed bottom
  bars that must stay visible when the virtual keyboard opens. Chrome Android 108+
  only — not a universal requirement. Flag if the project has fixed bottom UI and
  targets Android Chrome 108+; skip otherwise.
- WARN: `maximum-scale` set below `2`
- Required baseline:
  `<meta name="viewport" content="width=device-width, initial-scale=1">`
- For notched devices:
  `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`

**1.2 The 100vh iOS Safari Bug**
- FAIL: `height: 100vh` used as the SOLE height declaration on hero sections,
  modal overlays, sticky navigation, full-screen wrappers, or splash screens
- PASS: `height: 100vh` present as a fallback alongside `height: 100dvh` — this
  is the correct pattern
- Correct pattern to recognise as PASS:
```css
.hero {
  height: 100vh;        /* Fallback — PASS when dvh follows */
  height: 100dvh;
}
```
- FAIL pattern (100vh alone, no dvh):
```css
.hero { height: 100vh; }  /* FAIL — sole declaration, no dvh fallback */
```
- New viewport units (svh, dvh, lvh): require Safari 15.4+. If target
  `ios_safari_min < 15.4`, WARN on dvh without 100vh fallback.

**1.3 Safe Area Inset**
- FAIL: any `position: fixed` or `position: sticky` element at `bottom: 0`
  without `padding-bottom: env(safe-area-inset-bottom)`
- WARN: `viewport-fit=cover` not in viewport meta when content reaches screen edges
- Required CSS:
```css
.bottom-nav {
  padding-bottom: constant(safe-area-inset-bottom); /* legacy Safari — must come first */
  padding-bottom: env(safe-area-inset-bottom);       /* modern — wins in cascade */
}
```

**1.4 Input Font Size — iOS Auto-Zoom**
- FAIL: any `<input>`, `<select>`, or `<textarea>` with computed or declared
  `font-size` below `16px`
- This includes inherited font sizes — if body is 14px and inputs inherit, that
  is a FAIL
- 16px is a hard floor. No exceptions.

---

### GROUP 2 — MOBILE TOUCH

**2.1 Touch Target Size**
- WARN: interactive elements (`<button>`, `<a>`, `<input>`, toggles, icon
  buttons) with effective tap area below 44x44px (iOS HIG) / 48x48dp (Android
  Material)
- Measure full area including padding — a 16px icon with 14px padding = 44px =
  PASS
- Note: Layer 2 (Playwright) provides the reliable measurement; Layer 1 flags
  obvious cases

**2.2 Hover-Only Interactive States**
- FAIL: interaction reachable ONLY via `:hover` with no `:focus`,
  `:focus-within`, or click/tap equivalent
- PASS pattern:
```css
@media (hover: hover) {
  .menu:hover .dropdown { display: block; }
}
.menu:focus-within .dropdown { display: block; }
```
- NOTE: breakpoints that activate hover-dependent UI by width alone (e.g.,
  `@media (min-width: 1024px)`) without `(hover: hover)` check

**2.3 Tap Highlight / Touch Callout**
- NOTE: missing `-webkit-tap-highlight-color: transparent` in reset/body
- NOTE: missing `-webkit-touch-callout: none` on images used as interactive
  elements

**2.4 position: fixed Scroll Jank**
- WARN: `position: fixed` combined with `overflow: auto/scroll` inside the
  fixed element on iOS targets
- Prefer `position: sticky` where layout permits

**2.5 touch-action and overscroll-behavior**
- NOTE: custom drag/swipe interactions missing `touch-action` declaration
  (prevents default scroll from interfering)
- NOTE: page or modal missing `overscroll-behavior: contain` where
  bounce/chain scroll is undesirable

**2.6 Body Scroll Lock — Modal Behaviour**
- WARN: modal/drawer/sheet implementations that do not lock body scroll
  (`overflow: hidden` or equivalent on `<body>`) when open
- Symptom: background page scrolls while modal is open on iOS
- FAIL: modal implementation that locks body scroll but loses scroll position
  on close (position: fixed approach without capturing scroll Y)

---

### GROUP 3 — CSS COMPATIBILITY

**3.1 -webkit- Prefixes**
- WARN: `-webkit-text-size-adjust: 100%` missing (iOS text inflation on
  orientation change)
- WARN: `backdrop-filter` without `-webkit-backdrop-filter` prefix
- Verify current Safari prefix requirements against MDN BCD before flagging —
  do not hardcode support assumptions
- `-webkit-font-smoothing` on body: NOTE (macOS cosmetic, not functional)

**3.2 flex gap Support**
- WARN: `gap` in flex context when target `ios_safari_min < 14.1`
- Grid gap: supported broader — check MDN for exact version against configured
  target

**3.3 CSS Custom Properties in calc()**
- WARN: `calc(var(--x) * value)` patterns — known Safari edge cases. Flag for
  manual test in Layer 2.

**3.4 @supports Nesting**
- WARN: nested `@supports` inside a rule block (e.g.,
  `.hero { @supports not (height: 100dvh) {} }`) — only safe with a CSS nesting
  compiler (PostCSS, Sass, Lightning CSS, or native CSS nesting with target
  browser support). Use top-level `@supports` blocks in plain CSS:
```css
/* WARN — nested @supports, plain CSS only */
.hero {
  height: 100dvh;
  @supports not (height: 100dvh) { height: -webkit-fill-available; }
}

/* PASS — top-level @supports, safe everywhere */
.hero { height: 100dvh; }
@supports not (height: 100dvh) {
  .hero { height: -webkit-fill-available; }
}
```

**3.5 Scroll Snap**
- WARN: `scroll-snap-type` without `-webkit-overflow-scrolling: touch` for iOS
  targets below Safari 15

**3.6 Reduced Motion**
- WARN: animations, transitions, or auto-playing effects without
  `@media (prefers-reduced-motion: reduce)` override
- FAIL: any animation that runs for more than 3 seconds without a
  reduced-motion override (WCAG 2.3.3)

---

### GROUP 4 — IMAGES AND MEDIA

**4.1 Image Format Fallbacks**
- WARN: `<img src="...avif">` without `<picture>` providing WebP and JPEG
  fallbacks
- WARN: CSS `background-image: url(*.avif)` without `@supports` fallback
- Correct `<picture>` pattern:
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="1200" height="800">
</picture>
```

**4.2 srcset and sizes**
- WARN: large images (>800px wide) without `srcset`
- WARN: images missing `width` and `height` attributes (causes CLS — Cumulative
  Layout Shift)

**4.3 Lazy Loading**
- NOTE: below-fold images missing `loading="lazy"`

---

### GROUP 5 — FORMS AND INPUTS

**5.1 Input type Attributes**
- WARN: `<input>` missing `type` or using `type="text"` where a specific type
  would trigger the correct mobile keyboard
- email → type="email" | phone → type="tel" | numeric → type="number" |
  URL → type="url" | search → type="search"

**5.2 autocomplete Attributes**
- NOTE: personal-data form fields missing `autocomplete` (WCAG 1.3.5 — required
  for name, email, phone, address)

**5.3 Label Association**
- FAIL: `<input>`, `<select>`, or `<textarea>` without `<label for>`, wrapping
  `<label>`, `aria-label`, or `aria-labelledby`
- WCAG 1.3.1 failure. Also breaks iOS tap target prediction and voice control.

---

### GROUP 6 — DESKTOP GOTCHAS

**6.1 Scrollbar Width**
- WARN: `width: 100vw` on full-width elements — Windows scrollbar causes
  horizontal overflow
- Fix: use `width: 100%` or `scrollbar-gutter: stable`

**6.2 Tablet Breakpoints**
- WARN: breakpoints treating 1024px or 768px as desktop without a paired
  `(hover: hover)` check
- iPad landscape = 1024px wide, touch-primary, no hover
- NOTE: hover-dependent UI activated by width alone without `pointer: coarse`
  or `hover: hover` check

**6.3 Pointer vs Touch Events**
- WARN: JS using mousedown/mousemove/mouseup only — no pointer or touch event
  equivalent
- Fix: use Pointer Events API (pointerdown/pointermove/pointerup) for unified
  coverage

**6.4 Focus Outline Removal**
- FAIL: `outline: none` or `outline: 0` on interactive elements without a
  visible replacement focus style
- WCAG 2.4.7 failure
- Fix: use `:focus-visible` with a custom replacement outline

**6.5 Sticky Header Overlap**
- WARN: `position: sticky` headers without `scroll-margin-top` on anchor
  targets — in-page anchor links scroll content under the sticky header

**6.6 position: sticky Inside overflow Parents**
- WARN: `position: sticky` inside a parent with `overflow: hidden`,
  `overflow: auto`, or `overflow: scroll` — sticky silently stops working when
  any ancestor has overflow set. Flag this pattern.

**6.7 Focus Trap in Modals**
- WARN: modal/dialog/drawer implementations that do not trap focus (Tab and
  Shift+Tab should cycle within the open modal, not escape to background content)

---

## LAYER 2: RENDERED DEVICE AUDIT

Layer 2 requires a running preview server. If not available, state: "Layer 2
skipped — no preview server. Run `[project.preview_cmd]` and re-invoke."

The companion script's default exit policy is:
- FAIL findings fail the Playwright run and produce `BLOCKED`
- WARN findings produce `REVIEW REQUIRED` but do not fail the process by default
- Set `COMPLIANCE_FAIL_ON_WARN=1` to make WARN findings fail the process too
- NOTE findings are advisory only and never affect the gate

### VIEWPORT MATRIX

Run Playwright checks at all six viewports:

| ID | Name | Width | Height | Notes |
|----|------|-------|--------|-------|
| V1 | iPhone 14 | 390 | 844 | Primary iOS target |
| V2 | iPhone 14 Plus | 430 | 932 | Large iPhone |
| V3 | Android mid | 360 | 800 | Standard Android |
| V4 | iPad portrait | 768 | 1024 | Tablet — touch at "desktop" width |
| V5 | iPad landscape | 1024 | 768 | Fires most desktop breakpoints |
| V6 | Desktop | 1366 | 768 | Typical laptop viewport |

Extended (run if time permits):

| V7 | Large desktop | 1920 | 1080 | Wide monitor |
| V8 | Narrow mobile | 320 | 568 | iPhone SE — narrow edge case |

### AUTOMATED CHECKS TO RUN AT EACH VIEWPORT

Use the companion Playwright script (`compliance-audit.spec.js`). It runs these
automated checks:

**L2-1: Horizontal Overflow Detection**
```javascript
const hasOverflow = await page.evaluate(() =>
  document.documentElement.scrollWidth > window.innerWidth
);
```
- FAIL if true at V1–V3 (mobile viewports should never scroll horizontally)
- WARN if true at V4–V5 (tablets)

**L2-2: Tap Target Size Scan**

Measure all interactive elements — report any with effective area below 44x44px:
```javascript
const smallTargets = await page.evaluate(() => {
  const selectors = 'a, button, input, select, textarea, [role="button"], [tabindex]';
  return Array.from(document.querySelectorAll(selectors)).map(el => {
    const rect = el.getBoundingClientRect();
    return {
      tag: el.tagName,
      id: el.id,
      class: el.className,
      width: rect.width,
      height: rect.height,
      tooSmall: rect.width < 44 || rect.height < 44
    };
  }).filter(el => el.tooSmall);
});
```

**L2-3: Input Font Size Verification**

Get computed font-size on all inputs:
```javascript
const tooSmall = await page.evaluate(() => {
  const inputs = document.querySelectorAll('input, select, textarea');
  return Array.from(inputs).filter(el =>
    parseFloat(getComputedStyle(el).fontSize) < 16
  ).map(el => ({
    tag: el.tagName,
    id: el.id,
    class: el.className,
    size: getComputedStyle(el).fontSize
  }));
});
```
- FAIL on any result

**L2-4: Focus Visibility Check**

Tab through all focusable elements, screenshot focus state:
- FAIL: any focusable element where `outline` and `box-shadow` are both
  `none`/`0` in computed styles when focused

**L2-5: axe Accessibility Scan**

Run `@axe-core/playwright` at each viewport:
```javascript
const { AxeBuilder } = require('@axe-core/playwright');
const results = await new AxeBuilder({ page }).analyze();
// Report violations at FAIL, incomplete at WARN
```

**L2-6: Screenshot Evidence**

Capture full-page screenshot at each viewport. Name format:
`compliance-[viewport-id]-[page-slug]-[timestamp].png`

### MANUAL / REPORT-LEVEL CHECKS

The companion script records these once per report as NOTE findings. They do not
affect the compliance gate until implemented as automated checks.

**L2-7: Fixed/Sticky Bottom Overlap**

Manual check: scroll to bottom of page on mobile and verify no fixed UI chrome
overlaps readable content or controls.

**L2-8: Modal Scroll Lock**

Manual check when modals/drawers exist: open each modal, attempt body scroll,
and verify the background page does not scroll behind the modal.

**L2-9: Lighthouse Mobile (optional)**

Optional manual check: run Lighthouse mobile audit when release risk warrants
it. Capture Performance, Accessibility, and Best Practices scores.

---

## EVIDENCE FORMAT

Every finding must include all fields:

```
[FAIL|WARN|NOTE] CHECK-ID: Short description
Detection: [Static — file:line | Rendered — viewport V1, screenshot path]
Browser affected: [Specific browsers — never "all browsers"]
Location: /absolute/path/to/file.css:142 — .selector or element
Issue: [Specific description of what fails and why]
Fix: [Exact code, paste-ready]
Verified by: [Static pattern match | Playwright at V1/V3 | axe scan | computed style check]
```

**Evidence rule:** "Browser affected: All browsers" is never a valid entry. If
an issue truly affects every browser, list: "Chrome, Safari iOS, Safari macOS,
Firefox, Edge, Samsung Internet." Name them.

---

## AUDIT REPORT FORMAT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CROSS-PLATFORM COMPLIANCE AUDIT
Project: [name]
Entry: [URL or file]
Date: [date]
Layer 1: [complete | partial — reason]
Layer 2: [complete at V1–V6 | skipped — reason]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAIL FINDINGS
[each finding in evidence format]

WARN FINDINGS
[each finding in evidence format]

NOTE FINDINGS
[each finding in evidence format]

PASSES
Groups [list]: all checks passed — no issues found.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLIANCE GATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAIL count:  [N]
WARN count:  [N]
NOTE count:  [N]

STATUS: [BLOCKED | REVIEW REQUIRED | PASS]

BLOCKED          — one or more FAIL findings remain unresolved.
REVIEW REQUIRED  — no FAIL findings, but WARN findings remain. Owner sign-off
                   required before ship.
PASS             — no FAIL or WARN findings. NOTEs are advisory only.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## OPERATING RULES

1. Run against real code, not descriptions. Paste the code block or identify the
   file path. Do not audit from a description.
2. Every FAIL must ship an exact, paste-ready fix. A FAIL without a fix is not
   a finding.
3. "Browser affected: All browsers" is never valid. Name the browsers.
4. Do not audit Chrome-only. Chrome is the dev environment, not the target.
5. iOS Safari is the primary risk target. It runs on every iOS device regardless
   of browser brand. Weight its findings accordingly.
6. 100vh alone (no dvh fallback) is a FAIL. 100vh plus 100dvh as a fallback
   pair is a PASS. Read the full declaration before flagging.
7. Nested @supports inside a rule block is WARN for plain CSS. Only PASS if the
   project has a CSS compiler that handles nesting.
8. Font sizes on inputs: 16px is the floor. 15px is a FAIL. Check computed
   values in Layer 2, not just declared values.
9. Touch targets: measure the full effective tap area including padding. A 16px
   icon with 14px padding each side = 44px = PASS.
10. A PASS audit means the checked patterns are compliant. Test on real iOS and
    Android devices for final sign-off — the audit catches known patterns, real
    devices catch unknown rendering behaviour.

---

## WHAT THIS DOES NOT REPLACE

- Testing on real iOS and Android hardware
- BrowserStack / Sauce Labs automated cross-browser matrix testing
- Full WCAG accessibility audits (axe Layer 2 check covers overlap, not full
  WCAG)
- Performance auditing (Lighthouse score and Core Web Vitals — use WebPageTest)

---

## CREDITS

Built by Glen E. Grant — glenegrant.com
Pattern informed by MDN Browser Compatibility Data, Can I Use (caniuse.com),
WebKit Bug Tracker, WCAG 2.1, and real-world iOS Safari debugging.
Part of the Glenski-Toolkit: github.com/Glenskii/Glenski-Toolkit
