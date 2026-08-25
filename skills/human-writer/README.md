# Human Writer

Your draft may be clear in your head but flat on the page. It can become repetitive, over-polished, or packed with stock wording that does not sound like you.

Human Writer makes small editorial corrections while protecting your meaning, facts, structure, and voice. It is for improving a draft you already wrote, not for inventing new ideas or changing your point of view.

## Use it for

- Social posts, replies, emails, and comments before you send them.
- README files, documentation, and release notes that need a cleaner human voice.
- A read-only check when you want to know what feels canned without changing the draft.

## How it works

1. It reads the whole draft and identifies the writing habits that already make it yours.
2. It removes or flags stock vocabulary, repetitive transitions, padded emphasis, forced lists, and unnecessary em dashes.
3. It keeps the original claims intact. If a fact needs changing, it asks before touching it.

There are two modes:

- **Edit:** makes the smallest useful corrections and returns the revised draft.
- **Detect:** identifies the patterns that weaken the writing without rewriting it.

## Start prompt

```text
Use $human-writer to edit this draft. Keep my meaning and tone intact. Do not add claims or make it sound more formal than it is.
```

For a read-only review:

```text
Use $human-writer in Detect mode. Show me the lines that feel canned or over-polished, but do not rewrite them.
```

## What it will not do

- Add arguments, examples, facts, or opinions that were not in your draft.
- Silently correct an uncertain fact.
- Flatten blunt, informal, funny, or distinctive writing just to make it sound generic.
- Pretend that a detector can prove who wrote a piece of text.

## Included material

- [Core instructions](SKILL.md)
- [Editorial self-check](eval.md)
- [Editing decision guide](references/editing-decision-guide.md)
- [Voice preservation checklist](references/voice-preservation-checklist.md)
- [Voice profile template](references/voice-profile-template.md)
- [Revision acceptance guide](docs/revision-acceptance-guide.md)
- [Editorial rule checker](scripts/check_editorial_rules.py)
- [Revision note template](assets/revision-note-template.md)

## License

MIT. See [LICENSE](LICENSE).
