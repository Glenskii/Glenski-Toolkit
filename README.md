# Glenski Toolkit

Skills I use to build, review and ship software. Each one started as a fix for a problem in my own projects, then got cleaned up so anyone can drop it into their coding agent and use it.

I'm Glen Grant, a Toronto developer and photographer. More about me at [profile.glenegrant.com](https://profile.glenegrant.com).

## The skills

| Skill | What it does |
| --- | --- |
| [universal-audit](skills/universal-audit/) | A full software audit with scored evidence, a clear ship or don't-ship verdict, and a built-in security hunt. |
| [vibe-security-audit](skills/vibe-security-audit/) | Safe pre-release security checks for FastAPI, Flask and Django apps. |
| [cross-platform-compliance](skills/cross-platform-compliance/) | Catches the browser, phone and accessibility bugs that never show up on your desktop. |
| [seo-aeo-geo-gbp](skills/seo-aeo-geo-gbp/) | Search visibility review that sticks to evidence and promises no rankings. |
| [human-writer](skills/human-writer/) | Edits your draft so it sounds like you again, without changing what you said. |
| [save-context](skills/save-context/) | Writes a handoff note before a long session is compacted or passed to another tool. |
| [task-state-ledger](skills/task-state-ledger/) | One small status file so a long project can pick up where it stopped. |
| [inbox-guardian-for-gmail](skills/inbox-guardian-for-gmail/) | Keeps junk out of a personal Gmail inbox, using local rules and holding mail for your review instead of deleting it. |

## Install

Clone the repo and copy the skill folder you want into your agent's skills directory.

```bash
git clone https://github.com/Glenskii/Glenski-Toolkit.git
cp -r Glenski-Toolkit/skills/<skill-name> <your-agent-skills-directory>/<skill-name>
```

Copy the whole folder. The scripts and references inside it are part of the skill.

## What's in here

Skills only, written to work without my private setup. No client details, credentials or internal notes. Anything that needs a live connection, like an MCP server, lives in [Glenski-MCPs](https://github.com/Glenskii/Glenski-MCPs).

Skills that cite platform rules or search behavior tell you to check the official source on the day you use them.

## License

MIT. See [LICENSE](LICENSE).
