/**
 * File: scripts/compliance-audit.spec.js
 * Updated: 2026-07-28
 * Change: Layer 2 rendered cross-platform compliance runner for skill v2.2.
 *
 * Required dev dependencies:
 *   npm install --save-dev @playwright/test @axe-core/playwright
 *
 * Browser install:
 *   npx playwright install chromium
 *   npx playwright install chromium firefox webkit
 *
 * Run:
 *   npx playwright test --reporter=list --workers=1
 *
 * Environment:
 *   BASE_URL=http://localhost:4173
 *   AUDIT_PATHS=/,/about/,/contact/
 *   AUDIT_BROWSERS=chromium,firefox,webkit
 *   AUDIT_DISCOVER_LINKS=1
 *   AUDIT_MAX_PAGES=10
 *   AUDIT_OVERFLOW_TOLERANCE=2
 *   COMPLIANCE_FAIL_ON_WARN=1
 */

const { test, chromium, firefox, webkit } = require('@playwright/test');
const { AxeBuilder } = require('@axe-core/playwright');
const fs = require('fs');
const path = require('path');

const SEVERITY = {
  FAIL: 'FAIL',
  WARN: 'WARN',
  NOTE: 'NOTE',
  PASS: 'PASS',
};

const BROWSER_TYPES = { chromium, firefox, webkit };

const CONFIG = {
  BASE_URL: process.env.BASE_URL || 'http://localhost:3000',
  PAGES_TO_AUDIT: (process.env.AUDIT_PATHS || '/')
    .split(',')
    .map((p) => p.trim())
    .filter(Boolean),
  BROWSERS: (process.env.AUDIT_BROWSERS || 'chromium')
    .split(',')
    .map((b) => b.trim().toLowerCase())
    .filter(Boolean),
  DISCOVER_LINKS: process.env.AUDIT_DISCOVER_LINKS === '1',
  MAX_PAGES: Number(process.env.AUDIT_MAX_PAGES) || 10,
  SCREENSHOT_DIR: process.env.SCREENSHOT_DIR || './compliance-screenshots',
  REPORT_PATH: process.env.COMPLIANCE_REPORT_PATH || './compliance-report.json',
  MIN_TAP_TARGET: Number(process.env.MIN_TAP_TARGET) || 44,
  MIN_INPUT_FONT_SIZE: Number(process.env.MIN_INPUT_FONT_SIZE) || 16,
  OVERFLOW_TOLERANCE: Number(process.env.AUDIT_OVERFLOW_TOLERANCE) || 2,
  FAIL_ON_WARN: process.env.COMPLIANCE_FAIL_ON_WARN === '1',
  SETTLE_MS: Number(process.env.AUDIT_SETTLE_MS) || 500,
};

const DEVICE_PROFILES = [
  {
    id: 'iphone-14',
    label: 'iPhone 14',
    width: 390,
    height: 844,
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  },
  {
    id: 'iphone-plus',
    label: 'iPhone Plus',
    width: 430,
    height: 932,
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  },
  {
    id: 'android-360',
    label: 'Android 360',
    width: 360,
    height: 800,
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 3,
    userAgent:
      'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  },
  {
    id: 'ipad-portrait',
    label: 'iPad portrait',
    width: 768,
    height: 1024,
    isMobile: false,
    hasTouch: true,
    deviceScaleFactor: 2,
    userAgent:
      'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  },
  {
    id: 'ipad-landscape',
    label: 'iPad landscape',
    width: 1024,
    height: 768,
    isMobile: false,
    hasTouch: true,
    deviceScaleFactor: 2,
    userAgent:
      'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  },
  {
    id: 'desktop-1366',
    label: 'Desktop 1366',
    width: 1366,
    height: 768,
    isMobile: false,
    hasTouch: false,
    deviceScaleFactor: 1,
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  },
];

const REPORT = {
  meta: {
    generatedAt: new Date().toISOString(),
    baseUrl: CONFIG.BASE_URL,
    requestedPages: CONFIG.PAGES_TO_AUDIT,
    browsers: CONFIG.BROWSERS,
    deviceProfiles: DEVICE_PROFILES.map((profile) => profile.id),
    config: {
      overflowTolerance: CONFIG.OVERFLOW_TOLERANCE,
      minTapTarget: CONFIG.MIN_TAP_TARGET,
      minInputFontSize: CONFIG.MIN_INPUT_FONT_SIZE,
      failOnWarn: CONFIG.FAIL_ON_WARN,
      discoverLinks: CONFIG.DISCOVER_LINKS,
      maxPages: CONFIG.MAX_PAGES,
    },
  },
  pages: [],
  results: [],
  manualChecks: [
    {
      id: 'L2-7',
      severity: SEVERITY.NOTE,
      name: 'Fixed/Sticky Bottom Overlap',
      summary:
        'Manual check required. On mobile, scroll to page bottom and verify fixed UI does not overlap readable content or controls.',
    },
    {
      id: 'L2-8',
      severity: SEVERITY.NOTE,
      name: 'Modal Scroll Lock',
      summary:
        'Manual check required when modals/drawers exist. Open each modal and verify background content does not scroll behind it.',
    },
    {
      id: 'L2-9',
      severity: SEVERITY.NOTE,
      name: 'Lighthouse Mobile',
      summary:
        'Optional manual check. Run Lighthouse mobile when release risk warrants Core Web Vitals or performance scoring.',
    },
  ],
  summary: {
    totalChecks: 0,
    passedChecks: 0,
    failChecks: 0,
    warnChecks: 0,
    noteChecks: 0,
    manualNoteChecks: 0,
    axeViolations: 0,
    axeIncomplete: 0,
  },
  gate: null,
};

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function toSlug(value) {
  const slug = String(value || 'root')
    .replace(/^https?:\/\//, '')
    .replace(/[^a-zA-Z0-9-_]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
  return slug || 'root';
}

function normalizePath(pagePath) {
  if (!pagePath || pagePath === '/') return '/';
  return pagePath.startsWith('/') ? pagePath : `/${pagePath}`;
}

function buildUrl(pagePath) {
  const base = CONFIG.BASE_URL.replace(/\/$/, '');
  const normalized = normalizePath(pagePath);
  return `${base}${normalized === '/' ? '' : normalized}`;
}

function recordCheck(result, { id, name, passed, severity, summary, details = [] }) {
  result.checks.push({
    id,
    name,
    passed,
    severity: passed ? SEVERITY.PASS : severity,
    summary,
    details,
  });
  REPORT.summary.totalChecks++;
  if (passed) {
    REPORT.summary.passedChecks++;
    return;
  }
  if (severity === SEVERITY.FAIL) REPORT.summary.failChecks++;
  if (severity === SEVERITY.WARN) REPORT.summary.warnChecks++;
  if (severity === SEVERITY.NOTE) REPORT.summary.noteChecks++;
}

function applyGate() {
  REPORT.summary.manualNoteChecks = REPORT.manualChecks.length;
  REPORT.gate =
    REPORT.summary.failChecks > 0
      ? 'BLOCKED'
      : REPORT.summary.warnChecks > 0
        ? 'REVIEW REQUIRED'
        : 'PASS';
}

function writeReport() {
  applyGate();
  const reportPath = path.resolve(CONFIG.REPORT_PATH);
  fs.writeFileSync(reportPath, JSON.stringify(REPORT, null, 2), 'utf8');

  const totalNotes = REPORT.summary.noteChecks + REPORT.summary.manualNoteChecks;

  console.log('');
  console.log('======================================================');
  console.log('  CROSS-PLATFORM COMPLIANCE AUDIT');
  console.log('======================================================');
  console.log(`  Base URL        : ${REPORT.meta.baseUrl}`);
  console.log(`  Pages           : ${REPORT.pages.join(', ')}`);
  console.log(`  Browsers        : ${REPORT.meta.browsers.join(', ')}`);
  console.log(`  Device profiles : ${REPORT.meta.deviceProfiles.join(', ')}`);
  console.log('------------------------------------------------------');
  console.log(`  FAIL            : ${REPORT.summary.failChecks}`);
  console.log(`  WARN            : ${REPORT.summary.warnChecks}`);
  console.log(`  NOTE            : ${totalNotes}`);
  console.log(`  PASS            : ${REPORT.summary.passedChecks}`);
  console.log(`  Axe violations  : ${REPORT.summary.axeViolations}`);
  console.log(`  Axe incomplete  : ${REPORT.summary.axeIncomplete}`);
  console.log('------------------------------------------------------');

  for (const result of REPORT.results) {
    const nonPassing = result.checks.filter((check) => !check.passed);
    if (nonPassing.length === 0) continue;

    console.log('');
    console.log(`  ${result.browser} / ${result.profile.label} / ${result.page}`);
    console.log(`  Screenshot: ${result.screenshotPath}`);

    for (const check of nonPassing) {
      console.log(`    [${check.severity}] ${check.id}: ${check.name}`);
      console.log(`      ${check.summary}`);
      for (const detail of check.details.slice(0, 3)) {
        console.log(`      - ${typeof detail === 'object' ? JSON.stringify(detail) : detail}`);
      }
      if (check.details.length > 3) {
        console.log(`      - and ${check.details.length - 3} more`);
      }
    }
  }

  if (REPORT.manualChecks.length > 0) {
    console.log('');
    console.log('  Report-level manual checks');
    for (const check of REPORT.manualChecks) {
      console.log(`    [NOTE] ${check.id}: ${check.name}`);
      console.log(`      ${check.summary}`);
    }
  }

  console.log('');
  console.log('======================================================');
  console.log(`  COMPLIANCE GATE: ${REPORT.gate}`);
  if (REPORT.gate === 'BLOCKED') {
    console.log('  Fix all FAIL findings before shipping.');
  }
  if (REPORT.gate === 'REVIEW REQUIRED') {
    console.log('  No FAILs. WARN findings require owner sign-off before shipping.');
    if (!CONFIG.FAIL_ON_WARN) {
      console.log('  Process exit stays successful by default. Set COMPLIANCE_FAIL_ON_WARN=1 to fail on WARN.');
    }
  }
  if (REPORT.gate === 'PASS') {
    console.log('  No FAIL or WARN findings. NOTE findings are advisory.');
  }
  console.log(`  JSON report: ${reportPath}`);
  console.log('======================================================');
  console.log('');
}

async function checkHorizontalOverflow(page, tolerance) {
  return page.evaluate((allowed) => {
    const root = document.documentElement;
    const body = document.body;
    const rootDelta = Math.ceil(root.scrollWidth - root.clientWidth);
    const bodyDelta = body ? Math.ceil(body.scrollWidth - window.innerWidth) : 0;
    const delta = Math.max(rootDelta, bodyDelta, 0);

    const offenders = Array.from(document.body.querySelectorAll('*'))
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const overflowRight = Math.ceil(rect.right - window.innerWidth);
        const overflowLeft = Math.ceil(0 - rect.left);
        const overflow = Math.max(overflowRight, overflowLeft, 0);
        if (overflow <= allowed) return null;
        const text = (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 60);
        return {
          tag: el.tagName.toLowerCase(),
          id: el.id || '',
          className: typeof el.className === 'string' ? el.className.slice(0, 80) : '',
          width: Math.round(rect.width),
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          overflow,
          text,
        };
      })
      .filter(Boolean)
      .sort((a, b) => b.overflow - a.overflow)
      .slice(0, 10);

    return { hasOverflow: delta > allowed, delta, offenders };
  }, tolerance);
}

async function checkInputFontSizes(page, minFontSize) {
  return page.evaluate((threshold) => {
    return Array.from(document.querySelectorAll('input, select, textarea'))
      .filter((el) => {
        const style = window.getComputedStyle(el);
        if (el.disabled || style.display === 'none' || style.visibility === 'hidden') return false;
        return Number.parseFloat(style.fontSize) < threshold;
      })
      .map((el) => ({
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type') || '',
        fontSize: window.getComputedStyle(el).fontSize,
        selector: `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${el.name ? `[name="${el.name}"]` : ''}`,
      }));
  }, minFontSize);
}

async function checkTapTargets(page, minSize) {
  return page.evaluate((threshold) => {
    const selector = [
      'button',
      'a[href]',
      'input',
      'select',
      'textarea',
      '[role="button"]',
      '[role="link"]',
      '[tabindex]:not([tabindex="-1"])',
    ].join(',');

    return Array.from(document.querySelectorAll(selector))
      .filter((el) => {
        const style = window.getComputedStyle(el);
        if (el.disabled || el.getAttribute('aria-hidden') === 'true') return false;
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
        if (el.tagName.toLowerCase() === 'a') {
          const parentTag = el.parentElement ? el.parentElement.tagName.toLowerCase() : '';
          const display = style.display;
          const isInlineTextLink = display === 'inline' && ['p', 'li', 'span'].includes(parentTag);
          if (isInlineTextLink) return false;
        }
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) return false;
        return rect.width < threshold || rect.height < threshold;
      })
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          text: (el.textContent || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().slice(0, 60),
          selector: `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}`,
        };
      });
  }, minSize);
}

async function checkFocusVisibility(page) {
  return page.evaluate(() => {
    const selector = 'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
    const missing = [];

    for (const el of Array.from(document.querySelectorAll(selector))) {
      const style = window.getComputedStyle(el);
      if (el.disabled || el.getAttribute('aria-hidden') === 'true') continue;
      if (style.display === 'none' || style.visibility === 'hidden') continue;

      el.focus();
      if (document.activeElement !== el) continue;

      const focused = window.getComputedStyle(el);
      const outlineWidth = Number.parseFloat(focused.outlineWidth || '0');
      const outlineStyle = focused.outlineStyle || 'none';
      const boxShadow = focused.boxShadow || 'none';
      const borderColorChanged = focused.borderColor && focused.borderColor !== style.borderColor;
      const outlineVisible = outlineStyle !== 'none' && outlineWidth > 0;
      const shadowVisible = boxShadow !== 'none' && !boxShadow.startsWith('rgba(0, 0, 0, 0)');

      if (!outlineVisible && !shadowVisible && !borderColorChanged) {
        missing.push({
          tag: el.tagName.toLowerCase(),
          selector: `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}`,
          text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 60),
          outline: `${focused.outlineWidth} ${focused.outlineStyle} ${focused.outlineColor}`,
          boxShadow,
        });
      }
    }

    return missing;
  });
}

async function checkReducedMotion(page) {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  return page.evaluate(() => {
    const offenders = [];
    for (const el of Array.from(document.querySelectorAll('*'))) {
      const style = window.getComputedStyle(el);
      const animationDuration = Math.max(...style.animationDuration.split(',').map(parseTime));
      const transitionDuration = Math.max(...style.transitionDuration.split(',').map(parseTime));
      if (animationDuration > 0.01 || transitionDuration > 0.5) {
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;
        offenders.push({
          tag: el.tagName.toLowerCase(),
          id: el.id || '',
          className: typeof el.className === 'string' ? el.className.slice(0, 80) : '',
          animationDuration,
          transitionDuration,
        });
      }
      if (offenders.length >= 10) break;
    }

    function parseTime(value) {
      const trimmed = String(value || '').trim();
      if (trimmed.endsWith('ms')) return Number.parseFloat(trimmed) / 1000 || 0;
      if (trimmed.endsWith('s')) return Number.parseFloat(trimmed) || 0;
      return Number.parseFloat(trimmed) || 0;
    }

    return offenders;
  });
}

async function checkViewportMeta(page) {
  return page.evaluate(() => {
    const meta = document.querySelector('meta[name="viewport"]');
    if (!meta) return { exists: false, content: '', problems: ['missing viewport meta'] };
    const content = meta.getAttribute('content') || '';
    const problems = [];
    if (/user-scalable\s*=\s*no/i.test(content)) problems.push('user-scalable=no prevents zoom');
    const maxScale = content.match(/maximum-scale\s*=\s*([0-9.]+)/i);
    if (maxScale && Number.parseFloat(maxScale[1]) < 2) problems.push('maximum-scale below 2');
    return { exists: true, content, problems };
  });
}

async function discoverLinks(browserType, startUrl) {
  const browser = await browserType.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  try {
    await page.goto(startUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(CONFIG.SETTLE_MS);
    const discovered = await page.evaluate((maxPages) => {
      const origin = window.location.origin;
      const paths = new Set(['/']);
      for (const anchor of Array.from(document.querySelectorAll('a[href]'))) {
        try {
          const url = new URL(anchor.getAttribute('href'), window.location.href);
          if (url.origin !== origin) continue;
          if (url.hash && !url.pathname) continue;
          paths.add(`${url.pathname}${url.search}`);
          if (paths.size >= maxPages) break;
        } catch (_) {
          // Ignore malformed href values.
        }
      }
      return Array.from(paths);
    }, CONFIG.MAX_PAGES);
    return discovered.map(normalizePath).slice(0, CONFIG.MAX_PAGES);
  } finally {
    await context.close();
    await browser.close();
  }
}

async function resolvePages() {
  const requested = CONFIG.PAGES_TO_AUDIT.map(normalizePath);
  if (!CONFIG.DISCOVER_LINKS) return requested;

  const firstBrowserName = CONFIG.BROWSERS.find((name) => BROWSER_TYPES[name]) || 'chromium';
  const discovered = await discoverLinks(BROWSER_TYPES[firstBrowserName], buildUrl('/'));
  return Array.from(new Set([...requested, ...discovered])).slice(0, CONFIG.MAX_PAGES);
}

function validateConfig() {
  const invalidBrowsers = CONFIG.BROWSERS.filter((browserName) => !BROWSER_TYPES[browserName]);
  if (invalidBrowsers.length > 0) {
    throw new Error(`Unsupported AUDIT_BROWSERS value(s): ${invalidBrowsers.join(', ')}`);
  }
}

validateConfig();

test.describe.configure({ mode: 'serial' });

test.beforeAll(async () => {
  REPORT.pages = await resolvePages();
});

test('rendered compliance audit', async () => {
  ensureDir(CONFIG.SCREENSHOT_DIR);

  for (const browserName of CONFIG.BROWSERS) {
    const browserType = BROWSER_TYPES[browserName];
    const browser = await browserType.launch();

    try {
      for (const pagePath of REPORT.pages) {
        for (const profile of DEVICE_PROFILES) {
          const contextOptions = {
            viewport: { width: profile.width, height: profile.height },
            deviceScaleFactor: profile.deviceScaleFactor,
            userAgent: profile.userAgent,
          };

          // Firefox does not support Playwright's isMobile option. Keep viewport
          // and engine coverage there; use Chromium/WebKit for mobile emulation.
          if (browserName !== 'firefox') {
            contextOptions.isMobile = profile.isMobile;
            contextOptions.hasTouch = profile.hasTouch;
          }

          const context = await browser.newContext(contextOptions);
          const page = await context.newPage();
          const url = buildUrl(pagePath);
          const result = {
            browser: browserName,
            page: pagePath,
            url,
            profile,
            timestamp: new Date().toISOString(),
            screenshotPath: null,
            checks: [],
            axe: null,
          };

          try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
            await page.waitForTimeout(CONFIG.SETTLE_MS);

            const screenshotName = `${browserName}_${profile.id}_${toSlug(pagePath)}.png`;
            const screenshotPath = path.join(CONFIG.SCREENSHOT_DIR, screenshotName);
            await page.screenshot({ path: screenshotPath, fullPage: true });
            result.screenshotPath = screenshotPath;

            const viewportMeta = await checkViewportMeta(page);
            recordCheck(result, {
              id: 'L2-0',
              name: 'Viewport Meta',
              passed: viewportMeta.exists && viewportMeta.problems.length === 0,
              severity: viewportMeta.exists ? SEVERITY.WARN : SEVERITY.FAIL,
              summary: viewportMeta.exists
                ? viewportMeta.problems.length === 0
                  ? 'Viewport meta is present and does not restrict zoom.'
                  : viewportMeta.problems.join('; ')
                : 'Viewport meta tag is missing.',
              details: [viewportMeta],
            });

            const overflow = await checkHorizontalOverflow(page, CONFIG.OVERFLOW_TOLERANCE);
            recordCheck(result, {
              id: 'L2-1',
              name: 'Horizontal Overflow',
              passed: !overflow.hasOverflow,
              severity: profile.isMobile ? SEVERITY.FAIL : SEVERITY.WARN,
              summary: overflow.hasOverflow
                ? `Page overflows horizontally by ${overflow.delta}px at ${profile.width}px.`
                : `No horizontal overflow beyond ${CONFIG.OVERFLOW_TOLERANCE}px tolerance.`,
              details: overflow.offenders,
            });

            const tapTargets = await checkTapTargets(page, CONFIG.MIN_TAP_TARGET);
            recordCheck(result, {
              id: 'L2-2',
              name: 'Tap Target Size',
              passed: tapTargets.length === 0,
              severity: SEVERITY.WARN,
              summary: tapTargets.length === 0
                ? `Interactive targets meet ${CONFIG.MIN_TAP_TARGET}px minimum.`
                : `${tapTargets.length} rendered target(s) below ${CONFIG.MIN_TAP_TARGET}x${CONFIG.MIN_TAP_TARGET}px.`,
              details: tapTargets,
            });

            const smallInputs = await checkInputFontSizes(page, CONFIG.MIN_INPUT_FONT_SIZE);
            recordCheck(result, {
              id: 'L2-3',
              name: 'Input Font Size',
              passed: smallInputs.length === 0,
              severity: SEVERITY.FAIL,
              summary: smallInputs.length === 0
                ? `Inputs meet ${CONFIG.MIN_INPUT_FONT_SIZE}px minimum.`
                : `${smallInputs.length} input/control(s) below ${CONFIG.MIN_INPUT_FONT_SIZE}px.`,
              details: smallInputs,
            });

            const focusMissing = await checkFocusVisibility(page);
            recordCheck(result, {
              id: 'L2-4',
              name: 'Focus Visibility',
              passed: focusMissing.length === 0,
              severity: SEVERITY.FAIL,
              summary: focusMissing.length === 0
                ? 'Focusable elements have visible focus indicators.'
                : `${focusMissing.length} focusable element(s) lack a visible focus indicator.`,
              details: focusMissing,
            });

            const reducedMotion = await checkReducedMotion(page);
            recordCheck(result, {
              id: 'L2-4b',
              name: 'Reduced Motion Rendered Check',
              passed: reducedMotion.length === 0,
              severity: SEVERITY.WARN,
              summary: reducedMotion.length === 0
                ? 'No active animations/transitions detected under reduced-motion emulation.'
                : `${reducedMotion.length} animated/transitioning element(s) remain active under reduced-motion emulation.`,
              details: reducedMotion,
            });

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
              violations: axeResults.violations.map((violation) => ({
                id: violation.id,
                impact: violation.impact,
                description: violation.description,
                help: violation.help,
                helpUrl: violation.helpUrl,
                nodes: violation.nodes.length,
                nodesSample: violation.nodes.slice(0, 2).map((node) => node.html?.slice(0, 160)),
              })),
              incomplete: axeResults.incomplete.map((item) => ({
                id: item.id,
                impact: item.impact,
                description: item.description,
                nodes: item.nodes.length,
              })),
            };

            REPORT.summary.axeViolations += result.axe.violations.length;
            REPORT.summary.axeIncomplete += result.axe.incomplete.length;

            recordCheck(result, {
              id: 'L2-5',
              name: 'Axe Scan Completed',
              passed: !result.axe.error,
              severity: SEVERITY.WARN,
              summary: result.axe.error
                ? `Axe scan failed and accessibility results are incomplete: ${result.axe.error}`
                : 'Axe scan completed.',
              details: result.axe.error ? [result.axe.error] : [],
            });

            recordCheck(result, {
              id: 'L2-5a',
              name: 'Axe Violations',
              passed: result.axe.violations.length === 0,
              severity: SEVERITY.FAIL,
              summary: result.axe.violations.length === 0
                ? 'No axe violations found.'
                : `${result.axe.violations.length} axe violation(s) found.`,
              details: result.axe.violations.map((violation) => `[${violation.impact}] ${violation.id}: ${violation.description}`),
            });

            recordCheck(result, {
              id: 'L2-5b',
              name: 'Axe Incomplete',
              passed: result.axe.incomplete.length === 0,
              severity: SEVERITY.WARN,
              summary: result.axe.incomplete.length === 0
                ? 'No axe incomplete items.'
                : `${result.axe.incomplete.length} axe item(s) need manual review.`,
              details: result.axe.incomplete.map((item) => `[${item.impact}] ${item.id}: ${item.description}`),
            });
          } catch (err) {
            recordCheck(result, {
              id: 'L2-RUNTIME',
              name: 'Rendered Audit Runtime',
              passed: false,
              severity: SEVERITY.FAIL,
              summary: `Rendered audit failed for ${url}: ${err.message}`,
              details: [err.stack || err.message],
            });
          } finally {
            REPORT.results.push(result);
            await context.close();
          }

          const failCount = result.checks.filter((check) => check.severity === SEVERITY.FAIL && !check.passed).length;
          const warnCount = result.checks.filter((check) => check.severity === SEVERITY.WARN && !check.passed).length;
          console.log(`[${browserName}] ${profile.id} ${pagePath} - FAIL:${failCount} WARN:${warnCount}`);
        }
      }
    } finally {
      await browser.close();
    }
  }
});

test.afterAll(() => {
  writeReport();
  if (REPORT.gate === 'BLOCKED') {
    throw new Error('Compliance gate BLOCKED: fix all FAIL findings before shipping.');
  }
  if (REPORT.gate === 'REVIEW REQUIRED' && CONFIG.FAIL_ON_WARN) {
    throw new Error('Compliance gate REVIEW REQUIRED: WARN findings present and COMPLIANCE_FAIL_ON_WARN=1.');
  }
});
