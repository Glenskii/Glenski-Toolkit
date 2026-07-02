# Contributing to Glenski-Toolkit

Thanks for considering a contribution. This toolkit is built for real workflows — keep that bar in mind.

---

## What belongs here

- **Skills** that enforce quality or process in AI-assisted work (design, writing, code review, etc.)
- **Prompt guides** that are field-tested and immediately usable, not theoretical

**MCP servers** live in a separate repo: **[github.com/Glenskii/Glenski-MCPs](https://github.com/Glenskii/Glenski-MCPs)**. Contribute those there, not here.

What doesn't belong: wrappers around existing tools without improvement, prompts that are just rephrased versions of stock ChatGPT prompts, anything requiring a paid API without a free fallback or clear disclosure.

---

## Adding an MCP server

MCP servers are not kept in this repo. They live in their own home: **[github.com/Glenskii/Glenski-MCPs](https://github.com/Glenskii/Glenski-MCPs)**. Open MCP contributions there, following that repo's structure and contribution notes. This keeps the two concerns cleanly separated: skills and prompt guides here, live-capability servers there.

---

## Adding a skill

```
skills/
└── your-skill-name/
    ├── SKILL.md                  YAML frontmatter (name, description) + markdown instructions
    └── (optional support files)  modules/, schemas/, scripts/, security/, references/, README.md
```

Two rules keep skills frictionless to adopt:

1. **The folder name and the `name:` field must match.** `skills/foo/` has `name: foo`. No surprises for the person installing it.
2. **The skill folder is self-contained.** Everything the skill needs ships inside it, so `cp -r skills/your-skill-name ~/.claude/skills/your-skill-name` is the entire install. Do not scatter a skill's runnable parts elsewhere in the repo.

Keep `SKILL.md` under 500 lines. If the instructions run longer, move detail into a `references/` or `modules/` subdirectory and link from `SKILL.md`.

---

## Pull request checklist

- [ ] New skill follows the folder structure above (folder name == `name:` field, self-contained)
- [ ] `SKILL.md` is complete — no placeholder sections
- [ ] No hardcoded API keys, tokens, or personal credentials
- [ ] Any bundled scripts pin dependency floors with `>=`, not exact `==` locks
- [ ] Root `README.md` updated to reference the new skill in the Skills table

---

## Commit style

```
feat(seo-aeo-geo-gbp): add citation-tracking module
fix(anti-slop-design): correct font ban list in Quality Gate section
docs: update root README skills table
```

---

## License

By contributing, you agree your additions are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
