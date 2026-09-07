---
name: save-context
description: >
  Write a verified, secret-safe project handoff before compaction, a new
  session, or a cross-tool handoff. Use when the user says "save context",
  "save state", "I need to compact", "continue in a new session", or asks
  to preserve decisions and next steps from substantial work.
---

# Save Context

## Purpose

Create a concise, durable record of the current task before its working
conversation is lost or transferred. The record must preserve the decisions
and evidence that a future session cannot safely infer from the code alone.

When this skill is explicitly invoked for a transition, write and verify the
handoff before doing unrelated work in the same turn.

## Choose a storage target

Inspect the current project before writing. Use the first target that is both
present and appropriate:

1. A verified project memory or handoff file already used by the project.
2. A platform-native project memory location, but only when it is available in
   the active environment and can be read back.
3. The portable fallback: `<project-root>/.agent-context/HANDOFF.md`.

Do not treat `AGENTS.md`, a repository README, or a global instruction file as
a session log unless it already points to a dedicated handoff location. Do not
overwrite standing instructions to create one.

State the selected target and why in the final report. If the project root is
ambiguous, say so and ask for the target rather than writing somewhere guessed.

## Write a useful dated entry

Append to the selected handoff. Never replace earlier session records. Use the
format in [references/handoff-format.md](references/handoff-format.md).

Capture only what a future worker needs:

- completed work, including concrete files, changes, and verification;
- decisions or deviations that need their reason preserved;
- important failures and their root cause when known;
- standing rules, constraints, or proven workarounds;
- unresolved work, its blocker, and the next practical action.

Use short, specific prose. Do not restate a full transcript or dump command
output. Link to a durable local artifact when that is safer and more useful.

## Prove that the handoff is current

Before saying a handoff is already complete, read the target file in the
current run. It must explicitly cover the current task and its material work.
The date alone is not enough.

If the proof is absent, append a new entry. Never rely on a recollection of a
previous turn, an assumed background action, or a generic status message.

Read back the entry after writing. If the write or readback fails, report the
failure plainly and do not claim the task is safe to compact or hand off.

## Cross-tool handoffs

Only create an additional portable repository handoff when the user asks to
move the work to another compatible tool, or when the existing target is not
available to that tool. Keep the native record when one exists. Do not create a
GitHub issue, pull request comment, or external message unless the user asks.

## Protect sensitive information

Treat every handoff as potentially visible to collaborators, backups, and
version control.

Never write secrets or raw sensitive material, including API keys, passwords,
OAuth codes, tokens, cookies, private keys, recovery codes, `.env` contents,
or private customer data. Replace sensitive detail with a useful, safe summary,
such as "OAuth authentication completed" or "a credential issue remains."

Before creating or updating `.agent-context/HANDOFF.md`, check whether
`.agent-context/` is ignored by the project. If it is not ignored, call that
out in the final report. Do not change `.gitignore` unless the user asks.

## Final report

Report these facts concisely:

1. storage target and why it was selected;
2. file path written or confirmed;
3. the major points captured;
4. readback evidence;
5. whether a cross-tool handoff was requested;
6. the plain result: safe to compact, safe to switch sessions, or the exact
   reason it is not safe.

Do not say "already done" without the file-read evidence above.

---

Licensed under CC BY 4.0.
