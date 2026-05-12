# Cowork + Claude Code: Brain Transfer
**Owner:** Glen E. Grant — glenegrant@gmail.com  
**Date:** 2026-05-12  
**Purpose:** Full setup reference for migrating Cowork + Claude Code to a new MacBook Pro

---

## 1. Identity & Profile

| Field | Value |
|-------|-------|
| Name | Glen E. Grant (Glenski) |
| Email | glenegrant@gmail.com / glen@glenegrant.com |
| Website | glenegrant.com |
| Portfolio | glenegrant.com/portfolio |
| GitHub | github.com/Glenskii — Repo: Glenski-Toolkit |
| GMB | Glen E. Grant – Creative |
| Timezone | America/Toronto |

**Background:**
- IT: 35 years (MCSE, Novell — WordPress, Cloudflare, security, automation)
- Photography: 25+ years (high-end editorial/commercial since 2000)

---

## 2. Communication Preferences (Claude Behavior)

These preferences should be reinforced or re-added to any new Claude session or settings:

- **Style:** Direct, concise, impactful bursts. Short paragraphs. Minimal filler.
- **Punctuation:** Commas or colons only. NO em dashes.
- **Tone:** Professionally pragmatic, confident, solution-oriented.
- **Fluency:** Assume deep technical and creative fluency — no hand-holding.
- **Length:** Target two-sentence answers when possible.
- **Challenge:** Claude should challenge assumptions, offer counterpoints, test reasoning.
- **Lists:** Scan-friendly. Bullet points only when they add genuine clarity.
- **Code:** Complete, block-commented scripts with labeled sections (Python, JSON, SQL).
- **Fact-checking:** Verify facts, cite sources when uncertain.
- **Workflow:** Confirm context (environment, dates, timezone America/Toronto), propose one clear solution, include rationale and alternatives.
- **Creative/Prompt Engineering:** Use sections: Scene, Subject, Lighting, Style, Negatives. Lock segments to prevent drift. Respect brand accuracy.

---

## 3. Mac Setup: Claude Code

### Install
```bash
# Install Claude Code CLI
npm install -g @anthropic/claude-code

# Verify
claude --version

# Authenticate
claude auth login
```

### Key Claude Code Concepts
- Claude Code runs in your terminal — delegate coding tasks directly
- Works with your local repo via `claude` command in any project directory
- Supports MCP servers, skills, and plugins (same as Cowork)
- Config lives at `~/.claude/` on Mac

---

## 4. Cowork App Setup (Mac)

1. Download Claude desktop app from **claude.ai/download**
2. Sign in with glenegrant@gmail.com
3. Enable **Cowork mode** (research preview — toggle in app settings)
4. Set default workspace folder (recommend: `~/Documents/Cowork/`)
5. Re-install plugins (see Section 6)
6. Re-connect MCP connectors (see Section 7)

---

## 5. Installed Skills

Skills live at `~/.claude/skills/` on Mac (or equivalent app data path). All skills below were active on the Windows machine.

### Core / Anthropic Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `anti-slop-design` | Any UI/frontend build | Forces distinctive, original UI. Mandatory Design Declaration before code. Bans Inter/purple gradients/hero→cards layouts. 12-point quality gate. **v2.0 by Glen E. Grant.** |
| `brand-guidelines` | Anthropic branding needed | Applies Anthropic official colors + typography to artifacts |
| `canvas-design` | Poster, art, static design | Creates .png/.pdf visual art with design philosophy |
| `consolidate-memory` | Memory cleanup | Merges duplicate memory files, prunes stale facts |
| `doc-coauthoring` | Writing docs/proposals/specs | Structured 3-stage co-authoring workflow |
| `docx` | Word documents (.docx) | Create/edit/read Word docs with full formatting |
| `frontend-design` | Web UI components | Production-ready interfaces with design tokens + accessibility |
| `internal-comms` | Internal communications | Status reports, newsletters, 3P updates, incident reports |
| `pdf` | PDF files | Create, merge, split, extract, OCR, fill forms |
| `pptx` | Presentations (.pptx) | Create/edit/read PowerPoint decks |
| `schedule` | Recurring tasks | Create scheduled tasks, run on demand or on interval |
| `setup-cowork` | New Cowork setup | Guided role-matched plugin + connector setup |
| `skill-creator` | Build/improve skills | Create, eval, benchmark, and optimize skills |
| `theme-factory` | Styling artifacts | 10 pre-set themes + custom; applies to slides/docs/HTML |
| `vibe-security-audit` | Security review | OWASP pytest suite: headers, auth, IDOR, rate-limiting, CORS |
| `web-artifacts-builder` | Complex HTML artifacts | Multi-component React/Tailwind/shadcn artifacts |
| `xlsx` | Spreadsheets (.xlsx) | Create/edit/analyze Excel files, formulas, charts |

### Custom Skill (Glen's Own)

| Skill | Version | Notes |
|-------|---------|-------|
| `anti-slop-design` | 2.0 | Derived from `frontend-design`. Published to GitHub: Glenski-Toolkit. CC BY 4.0 |

---

## 6. Installed Plugins

### Plugin 1: Cowork Plugin Management
**ID:** `plugin_0155zZVATbJU3jHUmPP9NvMC`  
**Install:** Available via Cowork plugin marketplace

**Skills included:**
- `cowork-plugin-customizer` — Customize plugin connectors, skills, settings for your org
- `create-cowork-plugin` — Guide for building a new plugin from scratch (.plugin file output)

---

### Plugin 2: Marketing Plugin
**ID:** `plugin_01Eeb9y5m4iFuY3yRtytYfdc`  
**Install:** `claude plugins add knowledge-work-plugins/marketing`

**Skills included:**

| Skill | Command | Purpose |
|-------|---------|---------|
| `draft-content` | `/draft-content` | Blog posts, social, email, landing pages, press releases |
| `campaign-plan` | `/campaign-plan` | Full campaign brief: objectives, channels, calendar, KPIs |
| `brand-review` | `/brand-review` | Review content vs brand voice, flag deviations |
| `competitive-brief` | `/competitive-brief` | Competitor positioning, content gaps, battlecards |
| `performance-report` | `/performance-report` | Marketing metrics, trends, optimization recommendations |
| `seo-audit` | `/seo-audit` | Keyword research, on-page analysis, content gaps |
| `email-sequence` | `/email-sequence` | Multi-email drip/nurture/onboarding sequences |
| `content-creation` | — | Templates, SEO, headline formulas, CTA guidance |

**Supported Connectors:**
- Slack, Canva, Figma, HubSpot, Amplitude, Notion, Ahrefs, Similarweb, Klaviyo, Supermetrics

---

## 7. Connected MCP Services

These were active on the Windows machine. Re-authenticate each on Mac.

| Service | Category | Notes |
|---------|----------|-------|
| **Gmail** | Email | Read/search/draft emails |
| **Google Drive** | Files | Search and fetch Drive docs |
| **Google Calendar** | Calendar | List/create/update events |
| **Cloudflare** (×4) | Infrastructure | Workers, DNS zones, Radar, Logpush, URL scanning |
| **Canva** | Design | Generate/edit designs, export assets |
| **Box** (×2) | Files | Read/write/search Box files and folders |
| **Supabase** | Database | SQL execution, migrations, edge functions, TypeScript types |
| **Fal.ai** | AI Media | Image generation, video generation, workspace management |

### Re-connecting on Mac
Each connector is authenticated via OAuth or API key through the Cowork settings panel:
`Cowork → Settings → Connectors → Add Connector`

For Cloudflare: API token from dash.cloudflare.com → Profile → API Tokens  
For Supabase: Project API key from app.supabase.com → Project Settings → API  
For Fal.ai: API key from fal.ai/dashboard

---

## 8. Key File Paths (Mac equivalents)

| Purpose | Mac Path |
|---------|----------|
| Claude skills | `~/.claude/skills/` |
| Claude projects memory | `~/.claude/projects/` |
| Cowork outputs | `~/Documents/Cowork/outputs/` (set on first run) |
| Claude Code config | `~/.claude.json` or `~/.claude/settings.json` |
| GitHub repos | `~/Documents/GitHub/` |
| Glenski-Toolkit repo | `~/Documents/GitHub/Glenski-Github/` |

---

## 9. GitHub Repo: Glenski-Toolkit

**URL:** https://github.com/Glenskii/Glenski-Toolkit  
**Local path (Mac):** `~/Documents/GitHub/Glenski-Github/`

**Contains:**
- `anti-slop-design/SKILL.md` — Custom anti-slop design skill v2.0

**Post-setup git config:**
```bash
git config --global user.name "Glen E. Grant"
git config --global user.email "glenegrant@gmail.com"
# Authenticate via GitHub CLI:
brew install gh
gh auth login
```

---

## 10. Recommended Mac Dev Setup (Supporting Tools)

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node (for Claude Code)
brew install node

# Python (for skills that use it)
brew install python

# GitHub CLI
brew install gh

# Claude Code
npm install -g @anthropic/claude-code

# Useful extras
brew install git curl wget jq
```

---

## 11. Skill Trigger Cheat Sheet

Quick reference — what to say to activate each skill:

| Say this... | Activates |
|-------------|-----------|
| "build me a UI / component / frontend" | `anti-slop-design` + `frontend-design` |
| "make a Word doc / report / letter" | `docx` |
| "create a presentation / deck / slides" | `pptx` |
| "make a spreadsheet / Excel / budget" | `xlsx` |
| "create a PDF / merge PDFs / fill a form" | `pdf` |
| "design a poster / piece of art" | `canvas-design` |
| "write a blog post / social / email" | `marketing:draft-content` |
| "plan a campaign" | `marketing:campaign-plan` |
| "audit my SEO" | `marketing:seo-audit` |
| "security audit this app" | `vibe-security-audit` |
| "schedule this task" | `schedule` |
| "create a new skill" | `skill-creator` |
| "apply a theme to this" | `theme-factory` |
| "write internal comms / status update" | `internal-comms` |
| "write documentation / spec" | `doc-coauthoring` |

---

## 12. Notes & Known Quirks

- **anti-slop-design** must output a Design Declaration block BEFORE any code — if Claude skips it, reject and ask again.
- **Supabase MCP** has 4 separate tool groups (migrations, branches, SQL, edge functions) — all re-authenticate with the same project API key.
- **Cloudflare** has 4 separate MCPs (Workers, Radar, Logpush, GraphQL/Zones) — each may need its own token scope.
- **TodoWrite** tool is session-scoped — task lists reset between Cowork sessions (by design).
- **Memory files** persist via the `consolidate-memory` skill — run it periodically to keep Claude's context clean across sessions.
- Training cutoff for current Claude model: **end of May 2025** — use web search for anything after that.

---

*Generated by Cowork on 2026-05-12. Re-run to refresh after adding new plugins or connectors.*
