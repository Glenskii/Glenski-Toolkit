# Vibe-Coded App Security Audit Suite

**Built by:** Glen E. Grant — [glenegrant.com](https://glenegrant.com)  
**Part of:** [Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Tags:** `#glenski` `#vibe-security` `#owasp` `#pytest` `#fastapi` `#security`

---

## The Problem

Vibe-coded apps ship fast. Security does not ship with them.

AI coding tools generate working code. They do not generate secure code. The gap between "it works" and "it is safe" is where real applications get compromised. Credential stuffing, IDOR exploitation, debug pages in production, stack traces leaking database URLs — these are not exotic attacks. They are the first things an attacker checks on any app that looks AI-generated.

This suite closes that gap with a deterministic, runnable test suite covering the full OWASP attack surface. Drop it into your project, configure your routes, and run it before you ship.

---

## What This Covers

| Area | What It Tests |
|------|--------------|
| Security Headers | CSP directive quality, X-Frame-Options, HSTS max-age, Referrer-Policy, server fingerprinting |
| Authentication | Unauthenticated access rejection, token validation, empty/invalid bearer handling |
| Authorization | IDOR (Broken Object Level Auth), admin boundary, privilege escalation, mass assignment |
| Input Validation | XSS payloads, SQL injection, null byte injection, type coercion, NoSQL injection, oversized bodies |
| Rate Limiting | Sequential and concurrent burst detection, 429 enforcement, Retry-After header validation |
| Error Sanitization | Stack trace leakage, debug page detection, 30+ forbidden response terms |
| CORS | Hostile origin rejection, null origin, wildcard with credentials misconfiguration |
| Cookie Security | HttpOnly, Secure, SameSite flag enforcement, plaintext secret detection |
| Method Abuse | TRACE, CONNECT, and unsupported method handling |
| Config Hardening | Debug mode indicators, secret pattern leakage, version header exposure |

---

## What This Does Not Replace

This suite is your first line. Not your only line.

- Manual penetration testing
- WAF validation and configuration testing
- Production HTTPS and TLS verification
- Dependency vulnerability scanning — use `pip-audit` or `safety`
- DAST tooling such as OWASP ZAP or Burp Suite

---

## Requirements

- Python 3.11+
- pytest
- pytest-asyncio
- httpx
- python-dotenv
- An ASGI-compatible application (FastAPI, Flask via ASGI, Django ASGI)

---

## Quick Start

### 1. Install dependencies

```bash
pip install pytest pytest-asyncio httpx python-dotenv
```

### 2. Add the security folder to your project root

```
your-project/
├── your_app/
│   └── main.py
├── security/
│   ├── .env.test              <- your config (do not commit)
│   ├── conftest.py
│   ├── test_headers.py
│   ├── test_validation.py
│   ├── test_auth.py
│   ├── test_authorization.py
│   ├── test_rate_limit.py
│   ├── test_errors.py
│   ├── test_cors.py
│   ├── test_cookies.py
│   └── test_config.py
└── pytest.ini
```

### 3. Configure your routes

Copy `.env.test.template` to `.env.test` and fill in your values:

```env
APP_IMPORT_PATH=your_app.main:app

TEST_AUTH_LOGIN_ROUTE=/auth/login
TEST_AUTH_REGISTER_ROUTE=/auth/register
TEST_PROTECTED_ROUTE=/api/me
TEST_ADMIN_ROUTE=/api/admin
TEST_ERROR_ROUTE=/debug/trigger-error
TEST_IDOR_ROUTE_TEMPLATE=/api/user/{target_id}
TEST_PUBLIC_ROUTE=/
TEST_404_ROUTE=/this-route-does-not-exist
TEST_ERROR_SIM_ROUTE=/error-test

TEST_USERNAME=test_user
TEST_PASSWORD=test_password
TEST_ADMIN_USERNAME=admin_user
TEST_ADMIN_PASSWORD=admin_password

TEST_RATE_LIMIT_THRESHOLD=20
TEST_HOSTILE_ORIGIN=https://evil.example.com
TEST_ALLOWED_ORIGIN=https://yourdomain.com
```

### 4. Add .env.test to .gitignore

```bash
echo ".env.test" >> .gitignore
```

### 5. Run the suite

```bash
pytest security/ -v
```

---

## File Reference

### `conftest.py`

Shared fixtures used across all test files. Provides three client types:

- `client` — unauthenticated ASGI test client
- `auth_client` — authenticated client, logged in with TEST_USERNAME credentials
- `admin_client` — admin-authenticated client, logged in with TEST_ADMIN_USERNAME credentials

All clients use `httpx.AsyncClient` with `ASGITransport` — no network required, no running server.

---

### `test_headers.py`

Tests security header presence and directive quality. Header presence alone is not sufficient — every test validates actual directive values.

Covers: Content-Security-Policy (unsafe-inline, unsafe-eval, default-src, object-src), X-Frame-Options (DENY or SAMEORIGIN), X-Content-Type-Options (nosniff), Referrer-Policy (rejects unsafe-url), HSTS max-age minimum (1 year), Permissions-Policy, Server header fingerprinting, X-Powered-By removal.

Headers are tested on: public routes, protected routes, 404 responses, and error responses.

---

### `test_auth.py`

Tests authentication enforcement and enumeration resistance.

Covers: unauthenticated access rejection (401/403), invalid token rejection, empty bearer rejection, wrong auth scheme rejection, login enumeration resistance (status code parity and timing oracle), missing/empty/null credential handling.

The timing oracle test is a heuristic. Production timing analysis requires load testing tools.

---

### `test_authorization.py`

Tests authorization boundaries. This is the highest-value test file for vibe-coded apps.

IDOR (Broken Object Level Authorization) is the number one API vulnerability class. AI-generated CRUD endpoints almost universally skip ownership checks. This file tests horizontal escalation (user A accessing user B's data), vertical escalation (regular user accessing admin functions), and mass assignment (injecting role/admin flags via request body).

Covers: IDOR via sequential ID enumeration, UUID format enforcement, admin route access control, role parameter injection via query string and body, mass assignment on registration endpoint.

---

### `test_validation.py`

Tests input boundary validation against real attack payloads.

XSS payloads: script tags, event handlers, javascript: URIs, SVG onload, template injection probes.

SQL injection payloads: classic OR 1=1, UNION SELECT, DROP TABLE, SLEEP-based blind injection.

Type coercion attacks: integer username, array username, JSON object with MongoDB $ne operator, boolean values, prototype pollution probes.

Also covers: null byte injection, whitespace-only credentials, oversized usernames (10,000 chars), oversized bodies (10MB), wrong Content-Type, malformed JSON, extra field (mass assignment surface).

---

### `test_rate_limit.py`

Tests rate limiting threshold and concurrent burst handling.

Sequential rate limiting can be bypassed by parallel requests. This file tests both. Threshold is configurable via TEST_RATE_LIMIT_THRESHOLD. Also validates that 429 responses include a Retry-After or X-RateLimit-Reset header.

---

### `test_errors.py`

Tests error response sanitization against 30+ forbidden terms including: traceback, exception, file paths, SQL fragments, ORM module names, framework identifiers, environment variable patterns, and debug page indicators.

Tests triggered errors, 404 responses, 500 responses, and malformed request handling.

---

### `test_cors.py`

Tests CORS origin enforcement. Hostile origin must not be reflected. Null origin must be rejected. Preflight from hostile origin must be denied. Wildcard with credentials is tested as a misconfiguration indicator.

---

### `test_cookies.py`

Tests session cookie flag enforcement. Validates HttpOnly (blocks XSS cookie theft), Secure (blocks HTTP transmission), and SameSite Strict or Lax (blocks CSRF). Also scans cookie values for plaintext sensitive data patterns.

Skips gracefully if the app uses token-based auth instead of cookies.

---

### `test_config.py`

Tests production configuration hardening. Scans responses for 15+ debug mode indicators including Django debug toolbar markers, Werkzeug debugger, and traceback headers. Scans for 15+ secret patterns including connection strings, API key patterns, and PEM headers. Tests TRACE method (XST attack vector), unsupported methods, version header exposure.

---

## Operating Rules

These rules govern how the suite is written and how you should interpret results:

1. Do not trust framework defaults — test actual behavior.
2. Fail fast. Fail loud. A green suite with weak assertions is worse than no tests.
3. Separate app-layer tests from deployment-layer tests.
4. Test both authenticated and unauthenticated behavior on every protected route.
5. Test both normal and error code paths.
6. Auth, CORS, cookies, CSRF, IDOR, and rate limiting are first-class controls.
7. Never assume in-memory ASGI tests prove production TLS or proxy correctness.
8. Every assertion checks directive quality, not just header presence.
9. Every test has a comment explaining the attack it prevents.
10. A green suite means the tested controls work. Nothing more.

---

## CI/CD Integration

Add to your pipeline before any deployment step:

```yaml
# GitHub Actions example
- name: Run security audit
  run: |
    pip install pytest pytest-asyncio httpx python-dotenv
    pytest security/ -v --tb=short
  env:
    APP_IMPORT_PATH: ${{ secrets.APP_IMPORT_PATH }}
    TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
    TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
    TEST_ADMIN_USERNAME: ${{ secrets.TEST_ADMIN_USERNAME }}
    TEST_ADMIN_PASSWORD: ${{ secrets.TEST_ADMIN_PASSWORD }}
```

Store all test credentials as repository secrets. Never hardcode them in workflow files.

---

## Interpreting Results

**A failing test is information.** It tells you a specific control is missing or misconfigured. Read the assertion message — every failure includes the attack it enables and why the current behavior is dangerous.

**A passing test is not a guarantee.** It means the tested control works under the conditions tested. In-memory ASGI tests do not validate TLS, CDN behavior, WAF rules, or production proxy configuration.

**Skipped tests are not failures.** Some tests skip when the condition they test is not applicable — for example, cookie tests skip on token-based auth apps. Review skipped tests to confirm the skip reason is correct for your stack.

---

## OWASP Coverage Reference

| OWASP Category | Test Files |
|---------------|-----------|
| API1: Broken Object Level Authorization | test_authorization.py |
| API2: Broken Authentication | test_auth.py |
| API3: Broken Object Property Level Auth | test_authorization.py, test_validation.py |
| API4: Unrestricted Resource Consumption | test_rate_limit.py |
| API5: Broken Function Level Authorization | test_authorization.py |
| API6: Unrestricted Access to Sensitive Flows | test_rate_limit.py |
| API7: Server Side Request Forgery | test_validation.py |
| API8: Security Misconfiguration | test_headers.py, test_config.py, test_cors.py |
| API9: Improper Inventory Management | test_config.py |
| API10: Unsafe Consumption of APIs | test_validation.py, test_cors.py |
| A02: Cryptographic Failures | test_cookies.py |
| A03: Injection | test_validation.py |
| A05: Security Misconfiguration | test_headers.py, test_config.py, test_cors.py |
| A07: Identification and Auth Failures | test_auth.py, test_cookies.py |
| A09: Security Logging Failures | test_errors.py |

---

## Credits

Built by Glen E. Grant — [glenegrant.com](https://glenegrant.com)  
Based on: OWASP Top 10 (2021), OWASP API Security Top 10 (2023)  
Part of the [Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)

`#glenski` `#vibe-security` `#owasp` `#pytest` `#fastapi` `#security` `#api-security`
