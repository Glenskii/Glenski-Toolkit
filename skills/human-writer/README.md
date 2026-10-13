# Human Writer

A skill that cleans up your own draft so it sounds like you again. Use it on posts, replies, emails, docs and READMEs before you send or publish them.

It fixes stock wording, repeated transitions and padding. It does not add ideas or change your point.

## Use it for

- Social posts, replies, emails and comments before you send them.
- READMEs, docs and release notes that read too stiff.
- A read-only check when you only want to know what sounds canned.

## How it works

1. It reads the whole draft and notes the habits that already make it yours.
2. It removes or flags stock vocabulary, repeated transitions, padded emphasis, forced lists and needless em dashes.
3. It leaves your claims alone. If a fact needs changing, it asks first.

Two modes:

- **Edit:** makes the smallest useful corrections and returns the revised draft.
- **Detect:** names the patterns that weaken the writing and does not rewrite anything.

## Start prompt

```text
Use $human-writer to edit this draft. Keep my meaning and tone intact. Do not add claims or make it sound more formal than it is.
```

For a read-only review:

```text
Use $human-writer in Detect mode. Show me the lines that feel canned or over-polished, but do not rewrite them.
```

## What it won't do

- Add arguments, examples, facts or opinions that were not in your draft.
- Quietly correct a fact it is unsure about.
- Flatten blunt, informal, funny or distinctive writing into something generic.
- Claim that a detector can prove who wrote a piece of text.

## What's in the folder

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
