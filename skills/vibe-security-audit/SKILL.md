---
name: vibe-security-audit
description: Audit or harden a Python ASGI application before release. Use for FastAPI, Flask ASGI, Django ASGI, and comparable services that need a defensive pytest review of authentication, authorization, input validation, headers, CORS, cookies, rate limits, errors, and configuration.
license: CC-BY-4.0
---

# PYTHON WEB APP SECURITY AUDIT

**Purpose:** A runnable security check for Python web applications built through rapid development workflows.
**Use with:** FastAPI, Flask, Django, and similar Python web applications that can run through ASGI.
**License:** CC BY 4.0. Share freely, credit appreciated.
**Tags:** `#glenski` `#vibe-security` `#owasp` `#fastapi` `#security` `#pytest`

---

## THE PROBLEM THIS SOLVES

Vibe-coded apps ship fast. Security does not ship with them by default.

Rapid development tools can generate working code. They do not guarantee secure code.
The gap between "it works" and "it is safe" is where real applications get
compromised. This suite closes that gap with deterministic, runnable tests
covering the full OWASP attack surface.

**Plain-language scope:** This is for Python web apps. ASGI is the technical interface that lets the tests talk to FastAPI, Django, Flask through an ASGI adapter, and similar applications without starting a public server. It is not for Node, PHP, WordPress, native mobile, or desktop apps.

---

## WHAT THIS COVERS

| Area | Tests |
|------|-------|
| Security headers | CSP, X-Frame-Options, HSTS, Referrer-Policy, Permissions-Policy |
| Authentication | Unauthenticated access, token validation, session handling |
| Authorization | IDOR, privilege escalation, admin boundary enforcement |
| Input validation | XSS, SQLi, null bytes, oversized payloads, type coercion |
| Rate limiting | Threshold detection, 429 enforcement, abuse patterns |
| Error sanitization | Stack trace leakage, debug pages, SQL fragments, env data |
| CORS | Hostile origin rejection, preflight strictness |
| Cookie security | HttpOnly, Secure, SameSite enforcement |
| Method abuse | Unsupported HTTP method handling |
| Config hardening | Debug mode, test route exposure, secret leakage |

---

## WHAT THIS DOES NOT REPLACE

- Manual penetration testing
- WAF validation
- Production HTTPS / TLS verification
- Dependency vulnerability scanning (use `pip-audit` or `safety`)
- DAST tooling (ZAP, Burp Suite)

Run this suite as your first line. Not your only line.

**Known gap:** this suite covers CORS and cookie flags but does not yet test anti-CSRF token flow (double-submit or synchronizer token). If your app mutates state via cookie-authenticated POST, add a CSRF token test and treat a green run here as necessary, not sufficient.

---

## QUICK START

### 1. Install dependencies

```bash
pip install "pytest>=8" "pytest-asyncio>=0.24" "httpx>=0.27" python-dotenv
```

The suite depends on `asyncio_mode = auto` in the bundled `pytest.ini`. Without it, the async fixtures in `conftest.py` do not run and every test errors on collection. Keep `pytest.ini` alongside the `security/` folder.

### 2. Copy the security/ folder into your project root

The runnable suite is bundled in this skill folder: `security/` plus `pytest.ini`. Copy both into your project root.

```
your-project/
├── your_app/
│   └── main.py
├── security/
│   ├── .env.test
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

### 3. Configure your routes in .env.test

See `.env.test` template in this package.

### 4. Run

```bash
pytest security/ -v
```

---

## OPERATING RULES

1. Do not trust framework defaults. Test actual behavior.
2. Fail fast. Fail loud. A passing test suite with weak assertions is worse than no tests.
3. Separate app-layer tests from deployment-layer tests.
4. Test both authenticated and unauthenticated behavior on every protected route.
5. Test both normal and error code paths.
6. Auth, CORS, cookies, CSRF, IDOR, and rate limiting are first-class controls, not afterthoughts.
7. Never assume in-memory ASGI tests prove production TLS or proxy correctness.
8. Every assertion must check directive quality, not just header presence.
9. Every test must have a comment explaining what attack it prevents.
10. No false confidence. A green suite means the tested controls work. Nothing more.

---

## FILE REFERENCE

| File | Purpose |
|------|---------|
| `conftest.py` | Shared fixtures: client, auth tokens, env loading |
| `test_headers.py` | Security header presence and directive quality |
| `test_validation.py` | Input boundary, hostile strings, type coercion |
| `test_auth.py` | Authentication enforcement, enumeration resistance |
| `test_authorization.py` | IDOR, admin boundary, privilege escalation |
| `test_rate_limit.py` | Abuse threshold, 429 enforcement |
| `test_errors.py` | Error sanitization, stack trace leakage |
| `test_cors.py` | Origin restrictions, preflight handling |
| `test_cookies.py` | Cookie flag enforcement |
| `test_config.py` | Debug mode, secret exposure, test route hardening |

---

## REFERENCES

Based on OWASP Top 10 (2021) and OWASP API Security Top 10 (2023).
