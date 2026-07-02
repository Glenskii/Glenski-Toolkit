# Glenski-Toolkit

**Practical AI tools for creative and technical workflows.**
Skills, MCP servers, and prompt guides built for real use, free to share.

By [Glen E. Grant](https://profile.glenegrant.com) · [glenegrant.com](https://glenegrant.com)

---

## What's in here

### Skills — enforce quality and process in AI-assisted work

| Skill | What it does |
|---|---|
| [anti-slop-design](skills/anti-slop-design/) | Blocks default AI aesthetics and forces original typography, color, and layout. |
| [taste](skills/taste/) | Ships landing pages, portfolios, and redesigns that do not look templated. Brief in, design direction out. |
| [cross-platform-compliance](skills/cross-platform-compliance/) | Two-layer browser and device audit: static analysis plus rendered Playwright checks, with a BLOCKED / REVIEW / PASS gate. |
| [seo-aeo-geo-gbp](skills/seo-aeo-geo-gbp/) | Search presence orchestrator: technical SEO, keyword research, AEO/GEO, Google Business Profile, JSON-LD schema. Evidence-gated. |
| [vibe-security-audit](skills/vibe-security-audit/) | Runnable pytest suite covering the OWASP surface for any Python ASGI app before it ships. |

### MCP servers — add live capability to Claude

MCP servers live in their own repo: **[Glenski-MCPs](https://github.com/Glenskii/Glenski-MCPs)**.

| Server | What it does | API key |
|---|---|---|
| [glenski-web-research-mcp](https://github.com/Glenskii/Glenski-MCPs) | Live web search + page fetch via DuckDuckGo. Parallel search, JS-page detection, Playwright fallback, SSRF-guarded fetch. | None |

### Prompt guides — paste into Claude Projects or any LLM

| Guide | Use case |
|---|---|
| [claude-project-instructions.md](claude-project-instructions.md) | Anti-slop design rules for Claude.ai / Projects users, no code tools needed. |
| [anti-slop-companion-prompt.md](anti-slop-companion-prompt.md) | Full human reference: aesthetic directions, quality checklist, pushback phrases. |

---

## Installing a skill

Every skill is a self-contained folder with a `SKILL.md` at its root, the same layout Claude Code and the Anthropic skills ecosystem expect. Install is the same for all of them:

**Claude Code (user-wide):**
```bash
git clone https://github.com/Glenskii/Glenski-Toolkit
cp -r Glenski-Toolkit/skills/<skill-name> ~/.claude/skills/<skill-name>
```

**Project-scoped (Claude Code, Cursor, Windsurf):**
```bash
cp -r Glenski-Toolkit/skills/<skill-name> .claude/skills/<skill-name>
```

No rename, no build step. The skill loads on next session. Skills that ship supporting files (`modules/`, `schemas/`, `scripts/`, `security/`) carry them in the same folder, so copying the folder is always enough.

---

## The skills, in detail

### [anti-slop-design](skills/anti-slop-design/)
> Stop AI tools from generating the same UI over and over.

Requires a named Design Declaration before any code is written, bans the tells (Inter, purple gradients, hero → cards → CTA), and ships a 12-point quality gate. Also usable outside Claude Code: paste [`claude-project-instructions.md`](claude-project-instructions.md) into a Claude Project, or drop `SKILL.md` into `.cursorrules`. Compatible with Claude, GPT-4o, Gemini, Cursor, Windsurf.

### [taste](skills/taste/)
> Design direction, inferred from the brief.

For expressive surfaces: landing pages, portfolios, marketing sites. Reads the brief, commits to a direction, and audits before shipping. Derived from Anthropic's `frontend-design`, extended with a hard typography floor and scope rules.

### [cross-platform-compliance](skills/cross-platform-compliance/)
> Will it break on someone else's browser? Find out before they do.

Layer 1 greps the code for known-bad CSS/HTML/JS patterns. Layer 2 renders it across Playwright viewports, runs an axe accessibility scan, checks horizontal overflow and computed styles, and returns evidence-tiered findings behind a BLOCKED / REVIEW REQUIRED / PASS gate.

### [seo-aeo-geo-gbp](skills/seo-aeo-geo-gbp/)
> Search presence, done on evidence, not vibes.

A single orchestrator covering technical SEO audits, keyword research, competitor gap analysis, Answer Engine and Generative Engine Optimization, Google Business Profile compliance, and JSON-LD schema. Operates on a mandatory input gate: no recommendation ships without verified data, tiered E1/E2/E3. Ships `modules/`, `schemas/`, and JSON-LD `templates/`.

### [vibe-security-audit](skills/vibe-security-audit/)
> AI tools generate working code. They do not generate secure code.

A deterministic pytest suite covering headers, auth, authorization/IDOR, input validation, rate limiting, error sanitization, CORS, cookies, method abuse, and config hardening for any Python ASGI app. Copy the bundled `security/` folder and `pytest.ini`, point it at your app, run it.

---

## Repo structure

```
Glenski-Toolkit/
├── README.md                          This file — toolkit index
├── CONTRIBUTING.md                    How to contribute
├── claude-project-instructions.md     Anti-slop for Claude.ai users
├── anti-slop-companion-prompt.md      Full anti-slop reference guide
├── skills/
│   ├── anti-slop-design/SKILL.md
│   ├── taste/SKILL.md
│   ├── cross-platform-compliance/     SKILL.md + scripts/
│   ├── seo-aeo-geo-gbp/               SKILL.md + modules/ + schemas/ + templates/
│   └── vibe-security-audit/           SKILL.md + security/ + pytest.ini
└── mcps/
    └── glenski-web-research-mcp/      Mirror of the standalone Glenski-MCPs server
```

Canonical MCP home: [github.com/Glenskii/Glenski-MCPs](https://github.com/Glenskii/Glenski-MCPs).

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share freely, credit appreciated.

---

`#mcp` `#claude` `#ai-tools` `#anti-slop` `#frontend` `#design-system` `#seo` `#security` `#web-research` `#no-api-key`
