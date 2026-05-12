# Glenski-Toolkit

**Practical AI tools for creative and technical workflows.**  
Skills, MCP servers, and prompt guides — built for real use, free to share.

By [Glen E. Grant](https://glenegrant.com) · [glenegrant.com](https://glenegrant.com)

---

## What's in here

### MCP Servers — add live capabilities to Claude

| Tool | What it does | API Key? |
|---|---|---|
| [glenski-web-research-mcp](mcps/glenski-web-research-mcp/) | Live web search + page fetch via DuckDuckGo | None |

### Design Skills — enforce quality in AI-generated UI

| Skill | What it does |
|---|---|
| [anti-slop-design](skills/anti-slop-design/) | Blocks default AI aesthetics — forces original typography, color, and layout decisions |

### Prompt Guides — use directly in Claude Projects or any LLM

| Guide | Use case |
|---|---|
| [claude-project-instructions.md](claude-project-instructions.md) | Anti-slop design rules for Claude.ai / Projects users (no code tools needed) |
| [ANTI-SLOP-COMPANION-PROMPT.md](ANTI-SLOP-COMPANION-PROMPT.md) | Full human reference: aesthetic directions, quality checklist, pushback phrases |

---

## MCP Servers

### [glenski-web-research-mcp](mcps/glenski-web-research-mcp/)

Adds three research tools to Claude via the Model Context Protocol. No API keys. No paid accounts.

```
Tools: web_search | fetch_page | multi_search
Stack: DuckDuckGo · httpx · BeautifulSoup · Python MCP SDK
```

**Install in 2 steps:**

```bash
pip install -r mcps/glenski-web-research-mcp/requirements.txt
```

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "glenski-web-research": {
      "command": "python",
      "args": ["/path/to/Glenski-Toolkit/mcps/glenski-web-research-mcp/server.py"]
    }
  }
}
```

→ Full setup and parameter docs in [mcps/glenski-web-research-mcp/README.md](mcps/glenski-web-research-mcp/README.md)

---

## Design Skills

### [anti-slop-design](skills/anti-slop-design/)

> Stop AI tools from generating the same UI, over and over.

Every AI-generated interface defaults to Inter, purple gradients, rounded cards, and the same `hero → feature cards → CTA` layout. This toolkit breaks that pattern — and keeps it broken.

**Pick your file — three options, three audiences:**

**Option 1 — Claude.ai (chat / Projects)**  
File: [`claude-project-instructions.md`](claude-project-instructions.md)  
Paste into your Claude Project. Every design conversation runs with these rules automatically. No setup required.

**Option 2 — Cursor, Windsurf, or AI coding tools**  
File: [`skills/anti-slop-design/SKILL.md`](skills/anti-slop-design/SKILL.md)  
Add to `.cursorrules` or your equivalent project rules file.

**Option 3 — Full human reference**  
File: [`ANTI-SLOP-COMPANION-PROMPT.md`](ANTI-SLOP-COMPANION-PROMPT.md)  
Complete guide: aesthetic direction library, quality checklist, pushback phrases, team enforcement.

**What this enforces:**

- A named Design Declaration required before any code is written
- Typography bans: Inter, Roboto, Arial, Space Grotesk, Poppins — blocked
- Color bans: purple/indigo gradients, default Tailwind palette — blocked
- Layout bans: hero → cards → CTA, alternating image/text rows — blocked
- 12 named aesthetic directions with font pairings and color logic
- 12-point Quality Gate Checklist before output ships
- Team mode: lock a shared aesthetic so every team member's AI output converges

Compatible with: Claude · GPT-4o · Gemini · Cursor · Windsurf · any LLM-powered IDE

---

## Repo Structure

```
Glenski-Toolkit/
├── README.md                              This file — toolkit index
├── CONTRIBUTING.md                        How to contribute
├── claude-project-instructions.md         Anti-slop for Claude.ai users
├── ANTI-SLOP-COMPANION-PROMPT.md          Full anti-slop reference guide
├── mcps/
│   └── glenski-web-research-mcp/
│       ├── README.md                      Setup and usage docs
│       ├── server.py                      MCP server (Python)
│       ├── requirements.txt
│       ├── claude_desktop_config.json     Config snippet
│       └── LICENSE
└── skills/
    └── anti-slop-design/
        └── SKILL.md                       Cursor / Windsurf / Claude Code skill
```

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share freely, credit appreciated.

---

`#mcp` `#claude` `#ai-tools` `#anti-slop` `#frontend` `#design-system` `#web-research` `#no-api-key`
