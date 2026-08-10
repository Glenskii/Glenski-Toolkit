# Task State Ledger

Version 1.0.0

Task State Ledger is a portable working-notes method for complex technical tasks. It keeps a concise state file beside a private local evidence directory, so a person or compatible tool can understand the current work without repeatedly opening every command log and file dump.

Use it where operational continuity, evidentiary traceability, and privacy-sensitive retention must remain explicit across extended implementation work.

Its purpose is disciplined coordination, not invisible automation or speculative persistence.

## What it does

- Captures the current objective, completed milestones, decisions, blockers, and verification limits.
- Stores selected sanitized evidence in local files with stable node IDs.
- Keeps the state record readable without requiring Mermaid support.
- Supports deliberate handoffs without claiming to replace platform memory.

## What it does not do

- It does not access hidden conversation history.
- It does not reduce token use by a guaranteed amount.
- It does not make local files private by itself.
- It does not store secrets safely. Exclude them instead.

## Install

Copy this folder into a supported project-level skills directory. Keep the folder intact so the script, template, references, and tests remain available.

```bash
cp -r task-state-ledger <your-skills-directory>/task-state-ledger
```

## Typical layout

```text
project/
├── .task-state/
│   ├── task-state.md
│   └── evidence/
│       └── build-01.md
└── .gitignore
```

Add `.task-state/` to `.gitignore` before recording operational evidence in a repository. Publish only a separate, reviewed summary when it is genuinely safe for public release.

## Documentation

- [Skill instructions](SKILL.md)
- [Privacy and retention](references/privacy-and-retention.md)
- [Portable layout](references/portable-layout.md)
- [Task-state template](templates/task-state-template.md)

## License

CC BY 4.0. See [LICENSE](LICENSE).
