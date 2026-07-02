/**
 * compliance-audit.spec.js — Cross-Platform Compliance Audit Script
 * Layer 2 companion for the cross-platform-compliance skill v2.1.
 *
 * REQUIRED DEPS (add to your project's devDependencies):
 * ---------------------------------------------------------------
 * {
 *   "devDependencies": {
 *     "@playwright/test": "^1.44.0",
 *     "@axe-core/playwright": "^4.9.0"
 *   }
 * }
 *
 * HOW TO RUN:
 * ---------------------------------------------------------------
 * 1. Install deps:        npm install
 * 2. Install browsers:    npx playwright install chromium
 * 3. Copy as:             compliance-audit.spec.js
 * 4. Run audit:           npx playwright test --reporter=list --workers=1
 *    With env var:        BASE_URL=https://example.com npx playwright test --workers=1
 *
 * IMPORTANT — always run with --workers=1
 *   Parallel workers each get their own process scope. The global REPORT object
 *   is not shared across worker processes. Without --workers=1, results from
 *   different workers will be silently lost from the JSON report and summary.
 *   Add to playwright.config.js: workers: 1, or always pass --workers=1.
 *
 * OUTPUT:
 *   - Screenshots → ./compliance-screenshots/
 *   - JSON report → ./compliance-report.json (written in afterAll)
 *   - Human summary with BLOCKED/REVIEW REQUIRED/PASS gate → stdout
 *
 * MANUAL CHECKS (recorded once per report):
 *   - L2-7: Fixed/sticky bottom overlap visual check
 *   - L2-8: Modal scroll lock verification
 *   - L2-9: Lighthouse mobile score
 *   These report-level notes do not affect the compliance gate.
 *
 * GATE / EXIT POLICY:
 *   - FAIL findings fail the Playwright run and produce BLOCKED.
 *   - WARN findings produce REVIEW REQUIRED but do not fail the process by default.
 *   - Set COMPLIANCE_FAIL_ON_WARN=1 to fail the process on WARN findings too.
 *
 * CUSTOMISE the CONFIG block below before running.
 */

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 1: IMPORTS
// ─────────────────────────────────────────────────────────────────────────────

const { test } = require('@playwright/test');
const { AxeBuilder } = require('@axe-core/playwright');
const fs = require('fs');
const path = require('path');

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 2: CONFIGURATION — edit these values for your project
// ─────────────────────────────────────────────────────────────────────────────

const CONFIG = {
  /** Base URL to audit. Override via BASE_URL env var. */
  BASE_URL: process.env.BASE_URL || 'http://localhost:3000',

  /** Paths to audit. Each path is appended to BASE_URL. */
  PAGES_TO_AUDIT: (process.env.AUDIT_PATHS || '/').split(',').map(p => p.trim()),

  /** Directory where screenshots are saved. */
  SCREENSHOT_DIR: process.env.SCREENSHOT_DIR || './compliance-screenshots',

  /** Minimum tap target dimension in px (both width AND height must meet this). */
  MIN_TAP_TARGET: Number(process.env.MIN_TAP_TARGET) || 44,

  /** Minimum computed font size in px for form inputs. */
  MIN_INPUT_FONT_SIZE: Number(process.env.MIN_INPUT_FONT_SIZE) || 16,

  /** Fail the Playwright run on WARN findings as well as FAIL findings. */
  FAIL_ON_WARN: process.env.COMPLIANCE_FAIL_ON_WARN === '1',

  /**
   * Viewports to test.
   * isMobile flags whether this viewport should treat horizontal overflow as FAIL
   * (vs WARN on tablet/desktop).
   */
  VIEWPORTS: [
    { name: 'iPhone-14',      width: 390,  height: 844,  isMobile: true  },
    { name: 'iPhone-14-Plus', width: 430,  height: 932,  isMobile: true  },
    { name: 'Android-360',    width: 360,  height: 800,  isMobile: true  },
    { name: 'iPad-768',       width: 768,  height: 1024, isMobile: false },
    { name: 'Tablet-1024',    width: 1024, height: 768,  isMobile: false },
    { name: 'Laptop-1366',    width: 1366, height: 768,  isMobile: false },
  ],
};

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 3: SEVERITY CONSTANTS
// ─────────────────────────────────────────────────────────────────────────────

const SEVERITY = {
  FAIL: 'FAIL',  // Broken or inaccessible on target platform — blocks ship
  WARN: 'WARN',  // Degrades UX — requires owner sign-off to accept
  NOTE: 'NOTE',  // Best practice gap or not-yet-implemented check — advisory only
};

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 4: REPORT ACCUMULATOR
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Global report object. Accumulates all findings across tests.
 * Written to compliance-report.json in afterAll.
 *
 * NOTE: Only valid when run with --workers=1. See file header.
 */
const REPORT = {
  meta: {
    generatedAt: new Date().toISOString(),
    baseUrl: CONFIG.BASE_URL,
    pages: CONFIG.PAGES_TO_AUDIT,
    viewports: CONFIG.VIEWPORTS.map(v => v.name),
  },
  results: [],
  manualChecks: [
    {
      id: 'L2-7',
      severity: SEVERITY.NOTE,
      name: 'Fixed/Sticky Bottom Overlap',
      summary: 'Manual check required. Scroll to the page bottom on mobile and verify no fixed UI overlaps readable content or controls.',
    },
    {
      id: 'L2-8',
      severity: SEVERITY.NOTE,
      name: 'Modal Scroll Lock',
      summary: 'Manual check required when modals/drawers exist. Open each modal and verify the background page does not scroll behind it.',
    },
    {
      id: 'L2-9',
      severity: SEVERITY.NOTE,
      name: 'Lighthouse Mobile',
      summary: 'Optional manual check. Run Lighthouse mobile for Performance, Accessibility, and Best Practices when release risk warrants it.',
    },
  ],
  summary: {
    totalChecks:  0,
    passedChecks: 0,
    failChecks:   0,
    warnChecks:   0,
    noteChecks:   0,
    manualNoteChecks: 0,
    axeViolations: 0,
    axeIncomplete: 0,
  },
  gate: null, // Set in writeReport(): 'BLOCKED' | 'REVIEW REQUIRED' | 'PASS'
};

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 5: UTILITY FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function toSlug(str) {
  return str.replace(/[^a-zA-Z0-9-_]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
}

/**
 * Write the full JSON report and print a human-readable summary with compliance gate.
 */
function writeReport() {
  // ── Compliance gate ────────────────────────────────────────────────────────
  // BLOCKED if any FAIL. REVIEW REQUIRED if any WARN (and no FAIL). PASS if clean.
  REPORT.gate =
    REPORT.summary.failChecks > 0   ? 'BLOCKED' :
    REPORT.summary.warnChecks > 0   ? 'REVIEW REQUIRED' :
    'PASS';

  REPORT.summary.manualNoteChecks = REPORT.manualChecks.length;
  const totalNotes = REPORT.summary.noteChecks + REPORT.summary.manualNoteChecks;

  // ── Write JSON ─────────────────────────────────────────────────────────────
  const reportPath = path.resolve('./compliance-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(REPORT, null, 2), 'utf8');

  // ── Print summary ──────────────────────────────────────────────────────────
  console.log('\n');
  console.log('══════════════════════════════════════════════════════');
  console.log('  CROSS-PLATFORM COMPLIANCE AUDIT');
  console.log('══════════════════════════════════════════════════════');
  console.log(`  Base URL     : ${REPORT.meta.baseUrl}`);
  console.log(`  Pages        : ${REPORT.meta.pages.join(', ')}`);
  console.log(`  Viewports    : ${REPORT.meta.viewports.join(', ')}`);
  console.log('──────────────────────────────────────────────────────');
  console.log(`  FAIL         : ${REPORT.summary.failChecks}`);
  console.log(`  WARN         : ${REPORT.summary.warnChecks}`);
  console.log(`  NOTE         : ${totalNotes}`);
  console.log(`  PASS         : ${REPORT.summary.passedChecks}`);
  console.log(`  Axe violations: ${REPORT.summary.axeViolations}`);
  console.log(`  Axe incomplete: ${REPORT.summary.axeIncomplete}`);
  console.log('──────────────────────────────────────────────────────');

  // Per-result breakdown — only print non-passing checks to reduce noise
  for (const result of REPORT.results) {
    const nonPassing = result.checks.filter(c => !c.passed);
    if (nonPassing.length === 0) continue;
    console.log(`\n  ${result.viewport} — ${result.page}`);
    for (const check of nonPassing) {
      const icon = check.severity === SEVERITY.FAIL ? '✗ FAIL' :
                   check.severity === SEVERITY.WARN ? '⚠ WARN' : '· NOTE';
      console.log(`    [${icon}] ${check.id}: ${check.name}`);
      console.log(`            ${check.summary}`);
      if (check.details && check.details.length > 0) {
        const preview = check.details.slice(0, 3);
        for (const d of preview) {
          console.log(`            → ${typeof d === 'object' ? JSON.stringify(d) : d}`);
        }
        if (check.details.length > 3) console.log(`            … and ${check.details.length - 3} more`);
      }
    }
    if (result.axe && result.axe.violations.length > 0) {
      console.log(`    Axe violations (${result.axe.violations.length}):`);
      for (const v of result.axe.violations.slice(0, 3)) {
        console.log(`      ✗ [${v.impact}] ${v.id}: ${v.description}`);
      }
    }
  }

  if (REPORT.manualChecks.length > 0) {
    console.log('\n  Report-level manual checks');
    for (const check of REPORT.manualChecks) {
      console.log(`    [NOTE] ${check.id}: ${check.name}`);
      console.log(`           ${check.summary}`);
    }
  }

  console.log('\n══════════════════════════════════════════════════════');
  console.log(`  COMPLIANCE GATE: ${REPORT.gate}`);
  if (REPORT.gate === 'BLOCKED')          console.log('  → Fix all FAIL findings before shipping.');
  if (REPORT.gate === 'REVIEW REQUIRED')  console.log('  → No FAILs. WARN findings require owner sign-off before ship.');
  if (REPORT.gate === 'PASS')             console.log('  → No FAIL or WARN findings. NOTEs are advisory only.');
  if (REPORT.gate === 'REVIEW REQUIRED' && !CONFIG.FAIL_ON_WARN) {
    console.log('  → Process exit remains successful by default. Set COMPLIANCE_FAIL_ON_WARN=1 to fail on WARN.');
  }
  console.log('══════════════════════════════════════════════════════');
  console.log(`  Full JSON report: ${reportPath}`);
  console.log('══════════════════════════════════════════════════════\n');
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 6: IN-PAGE CHECK FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────

/** L2-1: Horizontal overflow — true if page scrolls horizontally. */
async function checkHorizontalOverflow(page) {
  return await page.evaluate(() =>
    document.documentElement.scrollWidth > window.innerWidth
  );
}

/** L2-3: Inputs/selects/textareas with computed font-size below threshold. */
async function checkInputFontSizes(page, minFontSize) {
  return await page.evaluate((threshold) => {
    return Array.from(document.querySelectorAll('input, select, textarea'))
      .filter(el => {
        const s = window.getComputedStyle(el);
        if (s.display === 'none' || s.visibility === 'hidden') return false;
        return parseFloat(s.fontSize) < threshold;
      })
      .map(el => ({
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type') || '',
        fontSize: window.getComputedStyle(el).fontSize,
        selector: `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}${el.name ? '[name="' + el.name + '"]' : ''}`,
      }));
  }, minFontSize);
}

/** L2-2: Interactive elements whose bounding box is below minSize x minSize. */
async function checkTapTargets(page, minSize) {
  return await page.evaluate((threshold) => {
    const selectors = 'button, a[href], input, select, textarea, [role="button"], [role="link"], [tabindex]:not([tabindex="-1"])';
    return Array.from(document.querySelectorAll(selectors))
      .filter(el => {
        const s = window.getComputedStyle(el);
        if (el.disabled || el.getAttribute('aria-hidden') === 'true') return false;
        if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return false;
        return r.width < threshold || r.height < threshold;
      })
      .map(el => {
        const r = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          width: Math.round(r.width),
          height: Math.round(r.height),
          text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40),
          selector: `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}`,
        };
      });
  }, minSize);
}

/**
 * L2-4: Tab through focusable elements. Return those with no visible focus indicator
 * (outline collapses to none/0 AND no box-shadow substitution).
 */
async function checkFocusOutlines(page) {
  return await page.evaluate(() => {
    const focusable = Array.from(document.querySelectorAll(
      'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ));
    const missing = [];
    for (const el of focusable) {
      const s = window.getComputedStyle(el);
      if (el.disabled || el.getAttribute('aria-hidden') === 'true') continue;
      if (s.display === 'none' || s.visibility === 'hidden') continue;
      el.focus();
      if (document.activeElement !== el) continue;
      const focused = window.getComputedStyle(el);
      const outline = focused.outline || '';
      const boxShadow = focused.boxShadow || '';
      const outlineClear = outline.includes('none') || outline.startsWith('0px') ||
                           outline === '' || outline.includes('0px 0px 0px 0px');
      const boxShadowClear = boxShadow === 'none' || boxShadow === '' ||
                             boxShadow.startsWith('rgba(0, 0, 0, 0)');
      if (outlineClear && boxShadowClear) {
        missing.push({
          tag: el.tagName.toLowerCase(),
          selector: `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}`,
          text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40),
          outline: outline.slice(0, 80),
          boxShadow: boxShadow.slice(0, 80),
        });
      }
    }
    return missing;
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 7: PLAYWRIGHT TEST SUITE
// ─────────────────────────────────────────────────────────────────────────────

for (const pagePath of CONFIG.PAGES_TO_AUDIT) {
  const fullUrl = CONFIG.BASE_URL.replace(/\/$/, '') + (pagePath.startsWith('/') ? pagePath : '/' + pagePath);

  test.describe(`Compliance Audit: ${pagePath}`, () => {

    for (const viewport of CONFIG.VIEWPORTS) {

      test(`[${viewport.name} ${viewport.width}x${viewport.height}] ${pagePath}`, async ({ page }, testInfo) => {

        // ── 7.1 Setup ─────────────────────────────────────────────────────────

        ensureDir(CONFIG.SCREENSHOT_DIR);
        await page.setViewportSize({ width: viewport.width, height: viewport.height });

        // domcontentloaded is faster and more reliable than networkidle on sites
        // with analytics, fonts, or streaming connections that never go idle.
        // A short settle period after DOMContentLoaded handles any deferred renders.
        await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(500); // Allow deferred renders to settle

        // Result object for this page + viewport
        const result = {
          page: pagePath,
          viewport: `${viewport.name} (${viewport.width}x${viewport.height})`,
          url: fullUrl,
          timestamp: new Date().toISOString(),
          screenshotPath: null,
          checks: [],
          axe: null,
        };

        /**
         * Record a check result with severity classification.
         * @param {object} opts
         * @param {string} opts.id       - Check ID (e.g. 'L2-1')
         * @param {string} opts.name     - Human label
         * @param {boolean} opts.passed  - true = PASS, false = triggered (severity applies)
         * @param {string} opts.severity - SEVERITY.FAIL | SEVERITY.WARN | SEVERITY.NOTE
         * @param {string} opts.summary  - One-line description of outcome
         * @param {Array}  [opts.details] - Additional detail items for failing checks
         */
        function recordCheck({ id, name, passed, severity, summary, details = [] }) {
          result.checks.push({ id, name, passed, severity: passed ? 'PASS' : severity, summary, details });
          REPORT.summary.totalChecks++;
          if (passed) {
            REPORT.summary.passedChecks++;
          } else {
            if (severity === SEVERITY.FAIL) REPORT.summary.failChecks++;
            if (severity === SEVERITY.WARN) REPORT.summary.warnChecks++;
            if (severity === SEVERITY.NOTE) REPORT.summary.noteChecks++;
          }
        }

        // ── 7.2 Screenshot ────────────────────────────────────────────────────

        const screenshotName = `${toSlug(pagePath || 'root')}_${viewport.name}_${viewport.width}x${viewport.height}.png`;
        const screenshotPath = path.join(CONFIG.SCREENSHOT_DIR, screenshotName);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        result.screenshotPath = screenshotPath;
        testInfo.attach('screenshot', { path: screenshotPath, contentType: 'image/png' });

        // ── 7.3 L2-1: Horizontal Overflow ────────────────────────────────────
        // FAIL on mobile viewports (should never scroll horizontally).
        // WARN on tablet/desktop (may be intentional for data tables etc).

        const hasOverflow = await checkHorizontalOverflow(page);
        const overflowSeverity = viewport.isMobile ? SEVERITY.FAIL : SEVERITY.WARN;
        recordCheck({
          id: 'L2-1',
          name: 'Horizontal Overflow',
          passed: !hasOverflow,
          severity: overflowSeverity,
          summary: hasOverflow
            ? `Page scrolls horizontally at ${viewport.width}px — likely mobile layout break.`
            : 'No horizontal overflow detected.',
        });

        // ── 7.4 L2-3: Input Font Size ─────────────────────────────────────────
        // FAIL: any input below 16px computed font size triggers iOS auto-zoom.

        const smallInputs = await checkInputFontSizes(page, CONFIG.MIN_INPUT_FONT_SIZE);
        recordCheck({
          id: 'L2-3',
          name: 'Input Font Size',
          passed: smallInputs.length === 0,
          severity: SEVERITY.FAIL,
          summary: smallInputs.length === 0
            ? `All inputs meet ${CONFIG.MIN_INPUT_FONT_SIZE}px minimum.`
            : `${smallInputs.length} input(s) below ${CONFIG.MIN_INPUT_FONT_SIZE}px — triggers iOS auto-zoom.`,
          details: smallInputs,
        });

        // ── 7.5 L2-2: Tap Target Size ─────────────────────────────────────────
        // WARN: elements below 44x44px tap area degrade mobile touch accuracy.

        const smallTargets = await checkTapTargets(page, CONFIG.MIN_TAP_TARGET);
        recordCheck({
          id: 'L2-2',
          name: 'Tap Target Size',
          passed: smallTargets.length === 0,
          severity: SEVERITY.WARN,
          summary: smallTargets.length === 0
            ? `All interactive elements meet ${CONFIG.MIN_TAP_TARGET}x${CONFIG.MIN_TAP_TARGET}px minimum.`
            : `${smallTargets.length} element(s) below ${CONFIG.MIN_TAP_TARGET}x${CONFIG.MIN_TAP_TARGET}px.`,
          details: smallTargets,
        });

        // ── 7.6 L2-4: Focus Outline ───────────────────────────────────────────
        // FAIL: WCAG 2.4.7 — focus must be visible. This is a hard accessibility failure.

        const missingOutlines = await checkFocusOutlines(page);
        recordCheck({
          id: 'L2-4',
          name: 'Focus Visibility',
          passed: missingOutlines.length === 0,
          severity: SEVERITY.FAIL,
          summary: missingOutlines.length === 0
            ? 'All focusable elements have a visible focus indicator.'
            : `${missingOutlines.length} element(s) lack a visible focus indicator — WCAG 2.4.7 failure.`,
          details: missingOutlines,
        });

        // ── 7.7 L2-5: Axe Accessibility Scan ─────────────────────────────────
        // violations → FAIL (confirmed failures).
        // incomplete → WARN (needs manual review — axe couldn't determine pass/fail).

        let axeResults;
        try {
          axeResults = await new AxeBuilder({ page })
            .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'])
            .analyze();
        } catch (err) {
          axeResults = { violations: [], incomplete: [], error: err.message };
        }

        result.axe = {
          error: axeResults.error || null,
          violations: axeResults.violations.map(v => ({
            id: v.id, impact: v.impact, description: v.description,
            help: v.help, helpUrl: v.helpUrl, nodes: v.nodes.length,
            nodesSample: v.nodes.slice(0, 2).map(n => n.html?.slice(0, 120)),
          })),
          incomplete: axeResults.incomplete.map(i => ({
            id: i.id, impact: i.impact, description: i.description, nodes: i.nodes.length,
          })),
        };

        REPORT.summary.axeViolations += result.axe.violations.length;
        REPORT.summary.axeIncomplete += result.axe.incomplete.length;

        recordCheck({
          id: 'L2-5',
          name: 'Axe Scan Completed',
          passed: !result.axe.error,
          severity: SEVERITY.WARN,
          summary: result.axe.error
            ? `Axe scan failed and accessibility results are incomplete: ${result.axe.error}`
            : 'Axe scan completed.',
          details: result.axe.error ? [result.axe.error] : [],
        });

        recordCheck({
          id: 'L2-5a',
          name: 'Axe Violations',
          passed: result.axe.violations.length === 0,
          severity: SEVERITY.FAIL,
          summary: result.axe.violations.length === 0
            ? 'No axe violations found.'
            : `${result.axe.violations.length} axe violation(s) — confirmed accessibility failures.`,
          details: result.axe.violations.map(v => `[${v.impact}] ${v.id}: ${v.description}`),
        });

        recordCheck({
          id: 'L2-5b',
          name: 'Axe Incomplete (manual review)',
          passed: result.axe.incomplete.length === 0,
          severity: SEVERITY.WARN,
          summary: result.axe.incomplete.length === 0
            ? 'No axe incomplete items.'
            : `${result.axe.incomplete.length} item(s) need manual accessibility review.`,
          details: result.axe.incomplete.map(i => `[${i.impact}] ${i.id}: ${i.description}`),
        });

        // ── 7.8 Accumulate ───────────────────────────────────────────────────

        REPORT.results.push(result);

        // Do not assert inside individual tests. This audit must complete every
        // viewport/page first, then apply the compliance gate once in afterAll.
        // Per-test assertion failures make Playwright restart the worker, which
        // breaks process-scoped report accumulation even with --workers=1.

        // Inline progress log for CI visibility
        console.log(`[${viewport.name}] ${pagePath} — FAIL:${result.checks.filter(c=>c.severity===SEVERITY.FAIL && !c.passed).length} WARN:${result.checks.filter(c=>c.severity===SEVERITY.WARN && !c.passed).length}`);
      });
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 8: GLOBAL TEARDOWN
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Fires once after all tests in this file complete.
 * Writes the JSON report and prints the full summary with compliance gate.
 *
 * Requires --workers=1 for accurate totals — see file header.
 */
test.afterAll(() => {
  writeReport();
  if (REPORT.gate === 'BLOCKED') {
    throw new Error('Compliance gate BLOCKED: fix all FAIL findings before shipping.');
  }
  if (REPORT.gate === 'REVIEW REQUIRED' && CONFIG.FAIL_ON_WARN) {
    throw new Error('Compliance gate REVIEW REQUIRED: WARN findings present and COMPLIANCE_FAIL_ON_WARN=1.');
  }
});
