# Optional hooks for project memory

Hooks are optional. The skill never installs them, edits settings files, or runs anything in the background. Copy only what you want, and review each snippet before using it. Replace `<skill-path>` with the folder where the skill is installed.

Hooks cannot make an agent remember anything. They run a command and print text, and the agent may or may not act on it.

## A. Claude Code SessionStart hook: offer setup

This hook checks whether the current directory is a git repository without a `ROADMAP.md`, and prints a message so the agent offers setup. It creates nothing.

Add to `.claude/settings.json` (project) or the user settings file:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ ! -f ROADMAP.md ] && echo 'No ROADMAP.md in this repo. Offer the user to set up project memory with: python <skill-path>/scripts/memctl.py init. Do not create files until the user agrees.' || true"
          }
        ]
      }
    ]
  }
}
```

On Windows without a POSIX shell, use a short script file instead and call it from the command field.

## B. Reminder after commits: rotate and prompt for a log entry

Rotation is safe to repeat. A git `post-commit` hook can run it and print a reminder.

`.git/hooks/post-commit` (mark it executable on macOS and Linux):

```sh
#!/bin/sh
if [ -f PROJECT-LOG.md ]; then
  python <skill-path>/scripts/memctl.py rotate
  echo "Reminder: if this commit reflects a durable decision, record it with memctl.py log."
fi
```

Claude Code equivalent, as a PostToolUse hook that fires after Bash tool calls:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "[ -f PROJECT-LOG.md ] && python <skill-path>/scripts/memctl.py rotate || true"
          }
        ]
      }
    ]
  }
}
```

The hook only rotates. Writing the entry itself stays a deliberate step, because the hook cannot know which decisions are durable.

## C. Codex and Antigravity

Neither tool needs a hook. Both read repository guidance from `AGENTS.md`, so a marked block is enough. Run:

```bash
python <skill-path>/scripts/memctl.py init --integrate
```

This appends a short block to an existing `AGENTS.md` and `CLAUDE.md`, once, and never creates either file. Without `--integrate`, `init` prints the block so you can paste it yourself.

## Privacy reminder

Do not log secrets, personal data, or client confidential material. If the repository may become public, add `PROJECT-LOG.md`, `ROADMAP.md`, and `docs/PROJECT-LOG-ARCHIVE.md` to `.gitignore`.
