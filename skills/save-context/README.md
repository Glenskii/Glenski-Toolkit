# Save Context

![Save Context icon](assets/icon-large.png)

**Version:** 1.1.0 | **License:** MIT

Save Context writes a short, dated handoff file before a session is compacted, closed, or handed to another tool. Run it when you are about to lose the conversation. The next session reads the file instead of rebuilding the work from a lost transcript.

## The problem

A conversation is not a project record. A compacted thread may keep only a short summary. A new session starts without the reasoning, command results, and decisions behind the work.

Save Context writes those down in a small, readable file.

## What it does

1. **Finds a place to save.** It uses an existing, verified project memory or handoff convention if there is one. If not, it creates the fallback `.agent-context/HANDOFF.md` at the project root.
2. **Writes the entry.** Each dated entry records what changed, key decisions and the reasons, evidence, unresolved work, and the next action.
3. **Checks before it claims.** It reads the target file before saying a handoff already covers the current work. If it cannot prove that, it writes or updates the handoff.
4. **Hands off across tools.** When you ask, it writes a portable repository handoff in addition to any platform-specific notes.
5. **Reports the result.** The report names the storage location, what was recorded, the readback evidence, and whether it is safe to move on.

## No read, no claim

The skill does not assume a save happened because an earlier turn sounded complete. It checks the actual target file in the current run. A handoff counts as current only when the file explicitly covers the work in progress.

No file-read evidence means no claim that the context is safe to leave behind.

## Privacy and repository safety

The handoff may include decisions, file paths, commands, verification results, and blockers. It never records credentials, tokens, cookies, private keys, raw personal data, or copied configuration secrets.

Before writing the repository fallback, the skill checks whether the project ignores `.agent-context/`. If the folder is not ignored, it says so. You decide whether the handoff stays private or is tracked with the project.

## Use it

Ask for it directly:

```text
save context
```

Use it before compaction, before closing a substantial task, or before a planned handoff to another compatible tool. It creates the fallback path on first use, so there is no setup step.

For the entry format and the final report, see [the handoff format](references/handoff-format.md).

## Part of the Glenski Toolkit

[github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit) holds local-first tools for development, creative production, and software quality.

Licensed under the MIT License. See [LICENSE](LICENSE).
