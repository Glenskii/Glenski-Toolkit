# Save Context

![Save Context icon](assets/icon-large.png)

**Version:** 1.1.0 | **License:** CC BY 4.0

Save Context gives a long technical task a proper place to land. Before a
session is compacted, closed, or handed to another tool, it writes a short,
dated record of the work, decisions, evidence, and next action. The next
session can start from the record instead of reconstructing the work from a
lost transcript.

---

## Why it matters

A conversation is useful while it is open, but it is not a reliable project
record. A compacted thread may keep only a short summary. A new session starts
without the reasoning, command results, and decisions that shaped the work.

Save Context turns that temporary work into a small, readable handoff. It is
for real project continuity, not a vague recap.

---

## What it does

1. **Finds the right place to save the handoff.** It uses an existing,
   verified project memory or handoff convention when one is available. If
   there is no usable convention, it creates the portable fallback
   `.agent-context/HANDOFF.md` at the project root.
2. **Writes the useful parts.** Each dated entry records what changed, key
   decisions and reasons, evidence, unresolved work, and the next clear
   action.
3. **Prevents false completion.** It reads the target file before reporting
   that a handoff already covers the current work. If that proof is missing,
   it writes or updates the handoff.
4. **Supports a deliberate cross-tool handoff.** When requested, it writes a
   portable repository handoff in addition to any platform-specific notes.
5. **Reports the result plainly.** The report names the storage location,
   what was recorded, the readback evidence, and whether it is safe to move
   on.

---

## A dependable handoff, not a promise

The skill does not assume a save happened because a prior turn sounded
complete. It checks the actual target file in the current run. A handoff is
only considered current when the file explicitly covers the work in progress.

That small check is the point: no file-read evidence, no claim that context is
safe to leave behind.

---

## Privacy and repository safety

The handoff may include decisions, file paths, commands, verification results,
and blockers. It never records credentials, tokens, cookies, private keys,
raw personal data, or copied configuration secrets.

Before writing the repository fallback, the skill checks whether the project
ignores `.agent-context/`. If the folder is not ignored, it says so clearly.
That leaves the owner in control of whether the handoff is private or tracked
with the project.

---

## Use it

Ask for it directly:

```text
save context
```

It is also appropriate before compaction, before closing a substantial task,
or before a planned handoff to another compatible tool. It creates the
fallback path on first use, so there is no separate setup step.

For the entry format and the final report, see
[the handoff format](references/handoff-format.md).

---

## Part of the Glenski Toolkit

[github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)
contains practical, local-first tools for development, creative production,
and software quality.

Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
