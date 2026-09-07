# Handoff format

Use this format for an append-only project handoff. Omit a field only when it
truly does not apply. Do not replace the safe wording rules in `SKILL.md` with
placeholders that reveal sensitive information.

```markdown
## YYYY-MM-DD: Short task label

**Completed**
- Concrete change, file, or verified result.

**Key decisions**
- Decision and the reason it matters to the next session.

**Evidence**
- Command, test, deployment readback, or durable local artifact.

**Issues resolved**
- Root cause and correction, when relevant.

**Standing rules**
- Constraint, owner decision, or proven workaround to retain.

**Pending**
- What remains, why, and the next practical action.
```

Keep the record factual and compact. A future worker should be able to answer:
what changed, why it changed, what proves it, and what comes next.
