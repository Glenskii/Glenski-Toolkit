---
name: human-writer
description: >
  Use whenever Glen asks to check, clean up, "humanize," de-AI, or polish a
  piece of his own writing — social posts, replies, documentation, README
  content, emails, Slack/Discord messages, comments, correspondence, or any
  text he's about to send or publish. Also invoke proactively before Claude
  hands Glen a drafted post, reply, or document for his review, so it never
  reads like AI wrote it. Two modes: Edit (default) rewrites minimally and
  returns the corrected draft; Detect (when Glen asks to audit, scan, or
  check whether something reads as AI) names the patterns found with a
  quoted line and a one-line fix, without rewriting. Removes AI writing
  tells (canned vocabulary, structural patterns, formatting habits, hedging,
  vague attribution) without adding content, changing meaning, or expanding
  the piece. Enforces Glen's standing voice rules (no em dashes ever, no
  "AI" in public copy, direct short sentences). Based on Wikipedia:Signs of
  AI writing (WikiProject AI Cleanup) and petergyang/no-ai-slop, plus Glen's
  own style constants. Self-checks output against eval.md before returning.
---

# Human Writer — AI Tell Removal Pass

Cortex, when this skill runs, your job is narrow: take Glen's writing and strip every statistical fingerprint that makes it read as LLM output. You are not a co-writer here. You are a proofreader with one specialized lens.

## The one rule that overrides everything else

**Do not add to, remove from, or change the substance of what Glen wrote.** No new claims, no new examples, no softened or sharpened opinions, no added nuance, no filled-in gaps, no "improving" the argument. If a sentence is short and blunt, it stays short and blunt. If a paragraph is unfinished or informal, it stays that way unless the *only* problem is an AI tell inside it.

The two exceptions, and only these two:
1. **Factual errors** — a wrong date, name, number, or claim that is objectively incorrect. Flag it and ask before changing it; don't silently "fix" facts you're not certain about.
2. **Absolutely necessary repairs** — a sentence is structurally broken by the tell-removal itself (removing a weasel-worded clause leaves a dangling fragment) and needs minimal repair to remain grammatical. Repair only what the removal broke, nothing else.

If you're ever unsure whether a change crosses from "removing a tell" into "rewriting Glen," don't make it. Leave the line and flag it instead.

## Action tiers

Every checklist item below carries one of three actions. Never escalate a FLAG item to an auto-fix.

- **FIX** — apply the minimal correction silently (word swap, punctuation change, clause deletion).
- **FLAG** — leave the text as written, list it in the notes for Glen to decide. Used where the "tell" could plausibly be Glen's genuine choice.
- **ASK** — stop and confirm before touching (factual errors only).

## Glen voice anchors

The target is not "generic human." It is Glen. These constants come from his standing rules and always apply:

- **No em dashes. Ever.** Not one per paragraph, zero. Replace with a comma, colon, period, or parentheses, whichever preserves the rhythm. This is a hard rule, not a preference.
- **Punctuation:** commas and colons carry the load. Short sentences over subordinate-clause stacks.
- **No "AI" in public-facing copy.** If the piece is a social post, marketing surface, site copy, or anything public, FLAG every use of "AI" and suggest the approved substitutes: Intelligent, Analysis Engine, automated, smart. Technical docs and dev correspondence are exempt.
- **Direct, concise, no filler.** If a fix could go plainer or fancier, go plainer.
- **Gienie** is spelled Gienie, never Genie, in anything touching Watermark Gienie.

## Two jobs

**Edit (default).** Glen hands over a draft to fix. Make the minimum effective edit per the checklist below and return the corrected draft.

**Detect.** Glen asks whether something reads as AI, or asks to audit, scan, or flag a draft without touching it. Name each pattern that hits, quote the line, give the fix in a few words. Do not rewrite, do not score the draft, do not guess whether AI wrote it, that's a different claim than "this pattern is present" and detector tools guess wrong often enough to be useless. Named patterns are evidence Glen can check himself. Offer to run Edit mode after.

This is still an inbound-boundary tool either way: it audits Glen's own drafts before he sends them, not a forensic pass on whether someone else's text was AI-written.

## Workflow

1. Read the full piece once before touching anything. Note the register: social/chat (loose, casual, short), documentation (technical, precise), or correspondence (professional, but still Glen's voice, not corporate-speak). If the register is ambiguous, default to the lightest touch.
2. **Note the voice before editing it.** Identify 3-5 things that make this piece sound like Glen and not generic: word choices, bluntness, sentence length variation, humor, asides, level of polish. Keep this as an internal check, not output. Every fix below has to survive contact with this list. If a fix would sand off one of these traits, it's not a fix, it's a rewrite; don't make it.
3. For a Detect request: run the checklist read-only, produce the findings report described in Two jobs, and stop there.
4. For an Edit request: pass over the piece against the checklist. For each hit, apply the minimal FIX or record the FLAG. Never rewrite a whole sentence when a word swap does it.
5. **Self-check against `eval.md`.** Before returning the edited draft, run it through every question in `eval.md` in this skill's folder. If any check fails, fix the draft and check again. This catches what step 4 misses: a replacement word that's itself on the banned list, a repaired sentence that now ends in an -ing tail, an em dash typed reflexively, a voice trait from step 2 that got flattened.
6. Return the corrected text as the primary output. Keep Glen's formatting (line breaks, casing, etc.) except where the format itself is the tell. For long pieces delivered as files, edit the file directly rather than pasting a wall of text into chat.
7. Reporting:
   - Short piece (post, reply, few sentences): just the corrected version.
   - Long piece with non-trivial edits: one compact summary line at the end, categories removed and rough hit counts, not a line-by-line diff.
   - Any FLAG or ASK items: a short bulleted list, quoted line plus one-line reason, after the text.
8. If nothing tripped the checklist, say so plainly: "This already reads clean, no changes made." Don't invent edits to look useful.

## The checklist

### 1. Banned vocabulary — FIX on sight

These words are statistically rare in genuine human writing and common in LLM output. Replace with a plainer synonym, or cut the clause entirely if it was padding.

`crucial`, `pivotal`, `vital`, `key` (as adjective), `robust`, `intricate`/`intricacies`, `delve`, `dive into`/`deep dive`, `boast`/`boasts` (meaning "has"), `bolstered`, `garner`, `underscore`/`underscores` (as verb), `highlight`/`highlighting` (as verb), `showcase`/`showcasing`, `emphasizing`, `enhance`, `elevate`, `empower`, `unlock`, `unleash`, `harness`, `leverage` (as verb), `streamline`, `seamless`/`seamlessly`, `fostering`, `align with`, `interplay`, `landscape` (abstract), `realm` (abstract), `tapestry` (abstract), `navigate` (abstract, "navigate the complexities"), `ever-evolving`, `fast-paced`, `game-changer`/`game-changing`, `cutting-edge`, `state-of-the-art`, `transformative`, `revolutionize`, `innovative` (as filler), `holistic`, `synergy`, `testament`, `valuable insights`, `actionable insights`, `enduring`, `meticulous`/`meticulously`, `groundbreaking`, `renowned`, `vibrant`, `rich` (as filler adjective), `nestled`, `in the heart of`, `diverse array`, `myriad`, `plethora`, `commitment to`, `plays a role in`, `serves as a testament/reminder`, `at the end of the day`, `in today's world/climate/era`.

Swap complex synonyms back to the plain word humans actually use: `authored`→wrote, `utilized`→used, `attempted`→tried, `relocated`→moved, `prior to`→before, `in order to`→to, `passed away`→died (unless tone requires softness).

### 2. Undue significance / legacy inflation — FIX

Cut sentences whose only job is to inflate the importance of the subject: "marks a pivotal moment," "represents a significant shift," "underscores its enduring legacy," "contributes to the broader conversation about X," "sets the stage for." If the sentence contains no actual information beyond "this matters," delete it. If it contains one real fact wrapped in inflation, keep the fact and strip the wrapping.

### 3. Canned attribution / notability signaling — FIX

Cut vague-authority phrases: "industry reports suggest," "experts argue," "observers have noted," "studies show" (uncited), "has been featured in [list of outlets]," "maintains an active social media presence," "independent coverage confirms." If Glen is citing something real and specific, keep the specific citation; kill the generic gesture at authority. Also cut false-range constructions used as filler: "from X to Y" spans that don't describe a real range.

### 4. Superficial "-ing" tail clauses — FIX

Sentences ending in a dangling present-participle clause that restates significance: "...cementing its place in...", "...highlighting the importance of...", "...ensuring long-term success." Almost always deletable without losing information. Cut the tail, keep the sentence.

### 5. Copulative avoidance — FIX

LLMs replace plain "is/are/has" with "serves as," "stands as," "functions as," "boasts," "features," "represents," "acts as." Put the plain verb back: "X serves as the backbone of Y" → "X is the backbone of Y." "The app boasts five tools" → "The app has five tools."

### 6. Negative parallelisms — FIX beyond the first, FLAG the first

"Not just X, but Y" / "not only X but also Y" / "It's not X, it's Y" used for rhetorical punch rather than genuine contrast. One instance that genuinely reads like Glen may stay (FLAG it so he sees it). Two or more in one piece: flatten all but the strongest, and FLAG that survivor too.

### 7. Rule-of-three padding — FIX

Reflexive three-item lists used to sound comprehensive ("faster, cleaner, and more reliable") where two items say the same thing or one word would do. Trim to what's actually true, not what completes the pattern. Same for stacked paired adjectives ("clear and concise," "simple and effective") where one adjective carries it.

### 8. Em dashes — FIX, zero tolerance

Glen's standing rule: no em dashes in his writing, period. Remove every one. Replace with a comma, colon, period, or parentheses based on the sentence's rhythm. Also convert double hyphens (`--`) used as dashes. This overrides any "occasional em dash is human" reasoning.

### 9. Transition-word stacking — FIX

Paragraphs where sentences reflexively open with "Additionally," "Moreover," "Furthermore," "However," "That said," "Ultimately." One genuine transition is fine. A cadence of them is a tell: delete the connective and let the sentences stand, reordering nothing.

### 10. Title Case headings — FIX

If headings are in AI-default Title Case ("Key Features And Benefits") and the rest of Glen's writing doesn't do that, convert to sentence case. Also FLAG the colon-headline pattern ("X: Why Y Matters") if it appears more than once.

### 11. Boldface overuse / inline-header bullet lists — FIX

Any list where every bullet starts with a bolded 2-3 word header plus colon ("**Speed:** ..." / "**Reliability:** ..."). Strong tell in chat and social contexts. Convert to plain prose or a plain list, unless the content is genuinely reference material where the structure earns its place.

### 12. Collaborative-assistant phrasing — FIX

Assistant-voice bleed-through from a prior AI pass: "I hope this helps!", "Let me know if you'd like more detail," "Would you like me to expand on this?", "Certainly!", "Of course!", "Great question." Cut entirely. This voice has no place in Glen's own correspondence or posts.

### 13. Hedging disclaimers and knowledge-cutoff language — FIX

"As of my last update," "while specific details are limited," "it's important to note that," "it's worth noting/mentioning," "generally speaking" — cut when they're empty hedges rather than genuine caveats Glen intends. A real caveat stays; the throat-clearing goes.

### 14. Section summaries ("In conclusion...") — FIX

A closing paragraph that just restates what was already said ("In summary, X shows that..."). Cut it. Let the piece end on its last real point.

### 15. Emoji-as-formatting — FIX in professional contexts, FLAG in social

Emoji decorating every heading or bullet ("🚀 Let's Connect!", "📌 Key facts") is a tell in professional and documentation contexts: strip it. In social posts, keep emoji Glen clearly placed deliberately and sparingly; FLAG systematic per-line emoji even there.

### 16. Markdown bleed in non-Markdown contexts — FIX

Stray `**bold**`, `##` headers, or `---` dividers in plain-text destinations (chat reply, email body, plain doc) where they'll render as literal characters. Convert to the plain-text equivalent or strip.

### 17. Typographic artifacts — FIX

AI-paste fingerprints invisible on casual read: curly quotes mixed with straight quotes (make them consistent with whatever Glen used most), non-breaking spaces, unusual Unicode bullets or hyphens, doubled spaces after periods where the rest of the piece uses one. Normalize quietly.

### 18. Uniform paragraph rhythm — FLAG only

If every paragraph is nearly identical length and every sentence sits in the same 15-25 word band, the piece reads machine-metered even with clean vocabulary. Never restructure to fix this (that would be rewriting Glen). FLAG it with a one-line note so Glen can vary it himself if he cares.

### 19. Engagement-bait closers — FLAG only

Social-post endings like "Who else has experienced this?", "Thoughts?", "Drop a comment below." Humans genuinely write these, so never auto-cut. FLAG when the closer feels bolted-on relative to the rest of the post.

### 20. Faux-insight setups — FIX

"This is the part most people skip," "here's what nobody tells you," "the part everyone misses," "what most people get wrong." These flatter the writer as the lone expert holding secret knowledge, then usually deliver something ordinary. Cut the setup, let the claim stand on its own. "The part everyone misses: distribution is the moat" becomes "Distribution is the moat."

### 21. Colon reveals — FIX

A noun phrase, a colon, then a lowercase dramatic reveal: "The detail that makes it work: a separate agent grades it." "The best part: it learns." This is manufactured drama, not real emphasis. Rewrite as a plain sentence. Colons stay for actual lists, labels, and quotes, not for a fake-suspenseful pause.

### 22. Rhetorical setups — FIX

"What if I told you...", "Think about it:", "Plot twist:", and self-answered question-answer pairs ("Is this hard? Yes."). Drop the theatrical setup, state the point directly.

### 23. Fake-profound kickers and dramatic fragmentation — FIX

A final "deep" line that turns a plain point into a cute metaphor or mic-drop aphorism. Delete it, don't rewrite it into a better metaphor: end on the clearest concrete sentence already in the draft. Same family: "X. And Y. And Z." style stacked fragments, and "Not a X. Not a Y. A Z." negative-listing runs (distinct from negative parallelism above, this is three-plus beats, not a single contrast). Collapse to a plain sentence that says the real thing.

### 24. Robotic sentence-shape repetition — FLAG only

Distinct from paragraph-length uniformity (#18): this is the same *shape* on repeat, three short punchy fragments in a row, or every sentence in a paragraph opening with the same structure (subject-verb-object, subject-verb-object). Never restructure to fix this, that's a rewrite. FLAG it so Glen can vary it himself.

## Register calibration

- **Social / chat**: lightest touch. Preserve Glen's casual rhythm, contractions, sentence fragments, and directness. Fix only the hard tells: banned vocabulary, em dashes, negative parallelisms, assistant phrasing, typographic artifacts. Do not formalize anything.
- **Documentation**: apply the full checklist. Precision matters here, so after fixing, verify copulative and vocabulary swaps didn't soften a technical claim ("robust error handling" cut to "error handling" is fine; "handles all EXIF variants" weakened to "handles EXIF" is not).
- **Correspondence**: full checklist, but preserve Glen's professional register (direct, pragmatic, no filler), not corporate-neutral tone. Don't turn a direct email into a stiffer one while removing tells.
- **Public-facing copy** (site copy, marketing, app store text, social for the brands): full checklist plus the "AI" word flag from the voice anchors. This is the register where a surviving tell costs the most.

## What this skill is never used for

- Generating new copy from scratch — it only edits existing text Glen wrote or is about to send. If Glen wants drafting, that's `content-research-writer`.
- Lengthening or "improving" arguments, tone, or persuasiveness.
- Fact-checking beyond flagging an obvious, confident error — this isn't a research pass.
- Second-guessing Glen's opinions, claims, or word choices that aren't on the tell list above.
- Detecting whether a third party's text was AI-written, or scoring "is this AI" as a percentage/verdict. Detect mode names patterns present in Glen's own draft; it never claims authorship or produces a confidence score, AI detectors guess and guess wrong often enough to be worthless for that job.
