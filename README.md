# Glenski-Toolkit

**By Glen E. Grant — [glenegrant.com](https://glenegrant.com)**  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share freely, credit appreciated

A growing series of practical tools for working with AI — covering design, security, and workflow automation. Built for real-world use, not demos. Each toolkit ships with a human guide and a skill file for AI coding tools.

---

## Why This Exists

AI tools are powerful and fast. They are also predictable in the worst ways — defaulting to the same UI patterns, skipping security controls, and generating output that looks finished but isn't. This toolkit series exists to correct those defaults with tested, opinionated prompts and rules that actually change how the AI behaves.

Every file here has been built from real work, not theory.

---

## Toolkit 1 — Anti-Slop Design Skill

> Stop AI tools from generating the same UI, over and over.

Every AI-generated interface defaults to Inter, purple gradients, rounded cards, and the same `hero → feature cards → CTA` layout. This toolkit breaks that pattern and keeps it broken by forcing a named aesthetic commitment before any code is written.

**What it enforces:** Design Declaration before any code, typography bans, color bans, layout bans, 12 named aesthetic directions, and a 12-point quality gate checklist.

**Compatible with:** Claude, GPT-4o, Gemini, Cursor, Windsurf, any LLM-powered IDE.

| File | Who It's For |
|------|-------------|
| [`claude-project-instructions.md`](./claude-project-instructions.md) | Claude.ai users — 5-step setup, paste directly into Project Instructions |
| [`anti-slop-companion-prompt.md`](./anti-slop-companion-prompt.md) | Full human reference: aesthetic library, quality checklist, pushback phrases |
| [`skills/anti-slop-design/SKILL.md`](./skills/anti-slop-design/SKILL.md) | AI coding tools — Cursor, Windsurf, Claude Code |

---

## Toolkit 2 — Vibe-Coded App Security Audit

> Vibe-coded apps ship fast. Security does not ship with them.

AI coding tools generate working code. They do not generate secure code. The gap between "it works" and "it is safe" is where real applications get compromised. This toolkit is a deterministic, runnable test suite covering the full OWASP attack surface — drop it into any Python ASGI project and run it before you ship.

**What it covers:** Security headers, authentication enforcement, IDOR and authorization boundaries, input validation against real attack payloads, rate limiting, error sanitization, CORS, cookie flags, method abuse, and config hardening.

**Compatible with:** FastAPI, Flask (ASGI), Django ASGI, any Python ASGI application.

| File | Who It's For |
|------|-------------|
| [`vibe-security-audit/README.md`](./vibe-security-audit/README.md) | Full setup guide, file reference, CI/CD integration, OWASP coverage map |
| [`skills/vibe-security-audit/SKILL.md`](./skills/vibe-security-audit/SKILL.md) | AI coding tools — load into Cursor, Windsurf, or Claude Code |

---

## Repo Structure

```
Glenski-Toolkit/
├── README.md                              This file
│
├── claude-project-instructions.md         Toolkit 1 — Claude Projects paste-in
├── anti-slop-companion-prompt.md          Toolkit 1 — Full human reference
│
├── vibe-security-audit/
│   └── README.md                          Toolkit 2 — Setup and reference guide
│
└── skills/
    ├── anti-slop-design/
    │   └── SKILL.md                       Toolkit 1 — AI coding tool skill
    └── vibe-security-audit/
        └── SKILL.md                       Toolkit 2 — AI coding tool skill
```

---

## More Coming

This repo grows as new tools get built and tested. Follow or star to get notified.

---

`#glenski` `#anti-slop` `#vibe-security` `#frontend` `#design-system` `#owasp` `#security` `#ai-tools` `#prompt-engineering`
