---
name: save-context
description: >
  Run this before /compact, before ending a long session, or when the user
  says "save context", "save state", "I need to compact", "let's continue
  this in a new session", or similar. Writes everything durable from the
  current session to persistent storage BEFORE any compaction or session
  handoff happens, so a fresh session (or a different agent, e.g. Codex,
  Antigravity, Grok) picks up with full continuity instead of re-deriving
  context from scratch or losing it outright. Detects which agent/harness
  is running and which persistence mechanism it actually has, then adapts.
  This is a hard gate: do the write first, before responding to anything
  else in the same turn. Never skip the write on the assumption it already
  happened; verify from a real file read, not from memory of a prior turn.
---

# Save Context, Pre-Compact and Pre-Handoff Memory Write

## Why this exists

`/compact` (or the equivalent in any harness) throws away the transcript
and replaces it with a lossy summary the agent doesn't control. Durable
storage persists across compaction and across brand-new sessions, loaded
fresh every time regardless of what happened to the transcript. Anything
not written before compaction is gone for good. This skill is the explicit
trigger to do that write, so it never depends on the agent guessing whether
"now" is a significant enough stopping point, or trusting its own sense
that the write already happened.

Two problems this solves:

1. **Moving to a new chat.** A fresh session has no transcript at all.
   Without a deliberate write to somewhere durable, everything learned this
   session is gone the moment it ends.
2. **Compaction inside the same session.** `/compact` keeps the session
   alive but discards the real transcript in favor of a lossy summary.
   Anything not captured before that summary is written is unrecoverable,
   even though the session technically "continues."

## Hard rule: "already done" requires proof, not a feeling

This skill has previously produced a false-negative bug: told to run on a
session where nothing had been saved, it responded with something like
"Already done, I ran this proactively at the end of my last turn," and
skipped the write. There was no prior turn to run in. This must never
happen again.

**Never claim the write already happened unless you can point to it.**
Concretely, before saying anything resembling "already done" or "nothing
new since last time":

1. Actually open the target persistence file (whichever one Step 1 below
   resolves to) with a real read, not a recollection.
2. Check whether it contains a dated section for *today's actual date* that
   covers the specific work done *in this visible conversation*.
3. If you cannot produce that file content as evidence in this turn, the
   answer is no, it is not done. Do the write.

A vague impression of "I probably already did this" is not evidence.
Session boundaries are invisible to you from the inside; a fresh session
has no prior turn, and a compacted session has no reliable memory of one
either. Only a file you just read counts.

## Step 1: Detect the environment and pick a persistence target

Don't assume any one platform's memory system exists. Probe, in this
order, and use the first one that matches:

1. **A platform-native memory system**, if the current harness has one
   (for example, an auto-loaded project memory index under the user's
   config directory, structured as an index file plus per-topic notes
   files). If present, use it: an indexed set of topic files referenced
   from a top-level index. Use the full workflow in Step 2a.

2. **An `AGENTS.md`-style convention**, common in Codex and similar CLI
   agents. Check for a repo-local `AGENTS.md` at the project root, or the
   agent's global equivalent. That file is normally standing instructions,
   not a session log, so don't overwrite it wholesale. Instead: look for
   an existing dated-log section already in that file, or in a linked
   notes file it references. If one exists, append to it. If none exists,
   don't invent a new convention inside `AGENTS.md` itself; fall back to
   the generic mechanism below instead, and only add a pointer to
   `AGENTS.md` if the user asks for one.

3. **No recognized native memory system.** Use a generic, agent-agnostic
   fallback: a single file at the project root, `.agent-context/HANDOFF.md`.
   Create the directory and file if they don't exist. Keep this file plain
   markdown, append-only, dated sections, with no assumption of any
   particular tool reading it beyond "an LLM coding agent with file
   access." This is the safest default because every agent that can read
   the repo can read this file.

State which of these three was detected and why, in the final report
(Step 4). Don't silently pick one; the report is how a future session
knows which storage to check.

## Step 2a: Platform-native memory path

### Identify the active project memory file
Every active project should have its own topic file (for example,
`project_<short-name>.md`). Find it via the index file. If none exists yet
for this project, create one now; don't skip the write because a file
doesn't exist yet.

### Append a dated section, don't overwrite prior sections
Head it `## YYYY-MM-DD: <short label for what this session covered>`.
Cover, concretely, not vaguely:

- **What shipped.** Concrete outcomes, not "worked on X." Name the actual
  files, features, or fixes. If it was deployed, say so and to where.
- **Any deviation from what was literally asked, and why.** If the agent
  declined a literal spec (a fake toggle, an unsafe pattern, an
  already-satisfied request) and built something else instead, that
  reasoning must survive. A fresh session re-reading only the code will
  not recover *why* the deviation happened, and might "fix" it back to the
  broken version.
- **Bugs found and root-caused**, especially non-obvious ones. The fix is
  visible in the diff; the *why it broke* usually isn't. Write that down.
- **Standing rules reaffirmed or newly established this session.** Anything
  the user corrected, confirmed, or that got discovered operationally
  (a workaround for a broken CLI flag, a tool's actual behavior versus its
  documented behavior) belongs here, not just in a general feedback note.
- **What's explicitly pending or was punted**, so the next session doesn't
  have to re-derive whether something's done. Say what and why it's not
  done, not just that it isn't.
- **Anything genuinely reusable across sessions or agents** (a workflow
  pattern, a gotcha, a decision the user made). Also check whether it
  belongs in its own topic file per the existing taxonomy, not just buried
  in this session's dated section.

### Update the top-level index
One-line pointer if this is a new topic file. Keep the index terse, it's
always loaded into context, so it has to stay skimmable.

## Step 2b: Codex or generic fallback path

Same content requirements as Step 2a (what shipped, deviations and why,
root-caused bugs, standing rules, what's pending, reusable gotchas), same
dated-section format, just a flatter file with no index and no per-project
taxonomy:

```markdown
## YYYY-MM-DD: <short label for what this session covered>

**Shipped:** ...
**Deviations from spec:** ...
**Bugs found / root cause:** ...
**Standing rules established:** ...
**Pending / punted:** ...
```

Append, never overwrite prior sections. If the file is new, add one line at
the top explaining what it is: `<!-- Session handoff notes for this repo.
Any agent working here should read this before starting and append before
finishing a non-trivial session. -->`.

## Step 3: Cross-agent handoff, when explicitly requested

If the user says this session's work needs to hand off to a *different*
agent than the one currently running (for example, a Claude session
handing off to Codex, or the reverse), the Step 2a memory-file write alone
is usually not enough, since platform-native memory files are typically
invisible to other agents. Explicitly:

- If the target agent uses a different convention (such as Codex's
  `AGENTS.md`/`.agent-context/HANDOFF.md`) and it doesn't exist yet, create
  it now in addition to (not instead of) the native memory write, with the
  same session summary.
- Ask whether the user also wants a GitHub issue or PR comment as the
  handoff mechanism, if that's the established pattern for this project.
  Check for an existing cross-agent handoff convention already in use on
  this project before inventing a new one.
- Don't assume the native memory write alone is sufficient for a
  cross-agent handoff just because it succeeded.

## Step 4: Final report, always structured, always explicit

End every run of this skill with a short, structured report, not a vague
"done!". Cover:

1. **Environment detected:** which of the three targets in Step 1 was
   used, and how it was detected (which file or path confirmed it).
2. **Target file(s) written:** full path(s).
3. **What was written:** one line per major point covered (shipped,
   deviations, bugs, standing rules, pending), not a re-paste of the whole
   section.
4. **Verification:** confirm the write was read back, or that pre-existing
   content proved a prior write already covered this session's work. Name
   the evidence, don't assert.
5. **Cross-agent handoff status:** whether Step 3 applied and what was
   done, or "not requested" if it didn't come up.
6. **Bottom line:** one sentence, such as "Safe to compact." or "Safe to
   switch sessions." If something couldn't be written (permissions, no
   detected target, ambiguous project root), say so plainly instead of
   pretending it succeeded.

## What not to do

- Don't write a summary so compressed it loses the "why." A bullet list of
  file names with no reasoning is not useful weeks from now.
- Don't skip this because "nothing major happened." Even a short session
  that fixed one subtle bug is worth one paragraph, especially if the root
  cause wasn't obvious.
- Don't wait for compaction to actually start before writing. By then the
  detail needed to write it well is already gone. Write it before
  responding to anything else once this skill is triggered.
- Don't claim "already done" without the file-read evidence required
  above. This is the specific bug this skill exists to never repeat.
- Don't assume a platform-native memory path exists just because it might
  in general; confirm it for the current project before using it, and fall
  back cleanly if it's absent.

---

Credit: Glen E. Grant, [profile.glenegrant.com](https://profile.glenegrant.com)
