---
name: "vibe-security-audit"
title: "VIBE-CODED APP SECURITY AUDIT SKILL"
version: "1.0"
description: >
  Production-grade security audit suite for apps built with AI coding tools.
  Provides a deterministic, runnable pytest test suite covering the full OWASP
  attack surface: security headers, authentication, authorization, IDOR, input
  validation, rate limiting, error sanitization, CORS, cookie flags, method abuse,
  and config hardening. Use when auditing, reviewing, or hardening any Python ASGI
  application before shipping.
author: "Glen E. Grant"
website: "https://glenegrant.com"
compatible_with:
  - "FastAPI"
  - "Flask (ASGI)"
  - "Django ASGI"
  - "Any Python ASGI application"
license: "CC BY 4.0"
repo: "https://github.com/Glenskii/Glenski-Toolkit"
tags:
  - "security"
  - "vibe-security"
  - "owasp"
  - "fastapi"
  - "pytest"
  - "glenski"
---

# VIBE-CODED APP SECURITY AUDIT SKILL v1.0

**Built by:** Glen E. Grant (glenegrant.com)  
**Purpose:** Production-grade security audit suite for apps built with AI coding tools.  
**Compatible:** FastAPI, Flask (ASGI), Django ASGI, any Python ASGI app  
**License:** CC BY 4.0 — share freely, credit appreciated  
**Tags:** `#glenski` `#vibe-security` `#owasp` `#fastapi` `#security` `#pytest`

---

## THE PROBLEM THIS SOLVES

Vibe-coded apps ship fast. Security does not ship with them by default.

AI coding tools generate working code. They do not generate secure code.
The gap between "it works" and "it is safe" is where real applications get
compromised. This suite closes that gap with deterministic, runnable tests
covering the full OWASP attack surface.

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

---

## QUICK START

### 1. Install dependencies

```bash
pip install pytest pytest-asyncio httpx python-dotenv
```

### 2. Copy the security/ folder into your project root

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

1. Do not trust framework defaults — test actual behavior.
2. Fail fast. Fail loud. A passing test suite with weak assertions is worse than no tests.
3. Separate app-layer tests from deployment-layer tests.
4. Test both authenticated and unauthenticated behavior on every protected route.
5. Test both normal and error code paths.
6. Auth, CORS, cookies, CSRF, IDOR, and rate limiting are first-class controls — not afterthoughts.
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

## CREDITS

Built by Glen E. Grant — glenegrant.com  
Based on OWASP Top 10 (2021), OWASP API Security Top 10 (2023)  
Part of the Glenski-Toolkit: github.com/Glenskii/Glenski-Toolkit
