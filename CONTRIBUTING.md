# Contributing to Glenski-Toolkit

Thanks for considering a contribution. This toolkit is built for real workflows — keep that bar in mind.

---

## What belongs here

- **MCP servers** that add genuine capability to Claude — live data, external APIs, system integrations
- **Skills** that enforce quality or process in AI-assisted work (design, writing, code review, etc.)
- **Prompt guides** that are field-tested and immediately usable, not theoretical

What doesn't belong: wrappers around existing tools without improvement, prompts that are just rephrased versions of stock ChatGPT prompts, anything requiring a paid API without a free fallback or clear disclosure.

---

## Adding an MCP server

```
mcps/
└── your-mcp-name/
    ├── README.md                 Required — setup, tools table, usage examples, parameters
    ├── server.py                 Single-file preferred; add subdirs if complexity demands it
    ├── requirements.txt          Pin major versions: package>=x.y.0
    ├── claude_desktop_config.json  Config snippet users can copy directly
    ├── LICENSE                   CC BY 4.0 preferred for consistency
    └── .gitignore
```

README must include: tool table, install steps, at least 2 usage examples, parameter docs, and honest disclosure of any API key requirements.

---

## Adding a skill

```
skills/
└── your-skill-name/
    └── SKILL.md                  YAML frontmatter (name, description) + markdown instructions
```

Skills should be under 500 lines. If the instructions are longer, add a `references/` subdirectory and link from SKILL.md.

---

## Pull request checklist

- [ ] New files follow the folder structure above
- [ ] README or SKILL.md is complete — no placeholder sections
- [ ] No hardcoded API keys, tokens, or personal credentials
- [ ] `requirements.txt` uses `>=` version pins, not exact `==` locks
- [ ] Root `README.md` updated to reference the new tool in the appropriate table
- [ ] Tested locally — MCP servers must import cleanly and register tools

---

## Commit style

```
feat(web-research-mcp): add multi_search tool for parallel queries
fix(anti-slop-design): correct font ban list in Quality Gate section
docs: update root README with mcps/ table
```

---

## License

By contributing, you agree your additions are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
