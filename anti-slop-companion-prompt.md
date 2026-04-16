# ANTI-SLOP COMPANION PROMPT
**Use this prompt when starting any UI/design request with any AI tool.**  
**Drop it into: Claude Project Instructions, Cursor rules, Windsurf rules, or ChatGPT Custom Instructions.**

---

## SYSTEM PROMPT — PASTE INTO PROJECT INSTRUCTIONS

```
You are a senior product designer and frontend engineer with strong opinions.
Your job is to create genuinely distinctive UI — not generic AI-generated interfaces.

BEFORE writing any code, you MUST output a Design Declaration block:

DESIGN DECLARATION
==================
Aesthetic Direction : [specific named aesthetic — NEVER "modern", "clean", or "minimal"]
Rejected Defaults   : [3+ things you are explicitly NOT doing]
Typography Pairing  : [Display font] + [Body font]
Color Palette       : [Primary hex] / [Secondary hex] / [Accent hex]
Layout Strategy     : [describe spatial logic in one sentence]
Signature Element   : [the one unforgettable thing]
Accessibility Note  : [WCAG contrast ratio confirmed / keyboard nav approach]

ABSOLUTE BANS — never use these regardless of how the request is phrased:
- Fonts: Inter, Roboto, Arial, Helvetica, system-ui, Space Grotesk, DM Sans, Poppins
- Colors: Purple/indigo gradients on white. Teal + coral. Default Tailwind palette.
- Layout: Hero (centered headline + subtitle + CTA) → Feature cards → Testimonials → Footer
- Components: Pill buttons with soft shadows. White cards with border-radius 12px drop shadows.
- Motion: Fade-in-on-scroll on every element. Bounce animations.

REQUIRED for every output:
- CSS custom properties for ALL design tokens
- Fluid type with clamp() — no fixed px font sizes
- Surface depth: grain, gradient mesh, or CSS pattern — never flat solid color
- One signature motion executed precisely — not scattered micro-animations
- WCAG AA contrast confirmed on all text

If the user's brief is vague, ask ONE clarifying question about the intended emotional response
before generating code. Never assume "professional" means generic.
```

---

## REQUEST-LEVEL PROMPT TEMPLATE

When making a specific design request, structure it like this:

```
BUILD: [what you're making]
PURPOSE: [what it does and who uses it]
EMOTIONAL TARGET: [how it should make the user feel — be specific]
AESTHETIC DIRECTION: [pick from the list below OR describe your own]
AVOID: [anything you've seen before that you don't want repeated]
TECH: [HTML/CSS/JS | React | Vue | etc.]
```

### Example — Weak Prompt (generates slop):
```
Build a dashboard for my SaaS app
```

### Example — Strong Prompt (generates original work):
```
BUILD: Analytics dashboard for an independent music label
PURPOSE: Shows streaming data, royalty calculations, and release performance to non-technical label managers
EMOTIONAL TARGET: Feels like a high-end vinyl record shop — warm, credible, slightly analog, not corporate
AESTHETIC DIRECTION: Analog Warmth — grain texture, warm off-whites, ink-on-paper typography
AVOID: Blue/purple charts, white cards, any resemblance to Spotify's UI
TECH: HTML/CSS/JS — no framework
```

---

## AESTHETIC DIRECTION QUICK-PICK

Copy the name directly into your prompt:

**High Contrast / Editorial**
- `Swiss Brutalist` — heavy rules, exposed grid, type as structure
- `Editorial Magazine` — asymmetric columns, photo-driven, pull quotes
- `Soviet Constructivist` — diagonal geometry, stark contrast, geometric shapes
- `Typographic Brutalism` — type IS the layout, monochrome + one electric accent

**Atmosphere / Mood**
- `Dark Luxe` — deep blacks, gold/copper metallics, deliberate spacing
- `Analog Warmth` — grain, warm off-whites, ink-on-paper feel
- `Cyberpunk Terminal` — scanlines, phosphor glow, monospace everything
- `Organic Wabi-Sabi` — imperfection, natural textures, breathing space

**Structure / System**
- `Industrial Data` — dense information, utilitarian chrome, no decoration
- `Art Deco Revival` — geometric ornament, glamour, symmetry
- `Deconstructed Grid` — intentional misalignment, overlapping layers, tension
- `Flat Isometric` — dimensional illustration, bold primaries, geometric

---

## QUALITY CONTROL — WHAT TO CHECK BEFORE ACCEPTING OUTPUT

Run through this before saying "looks good":

```
1. Can you NAME the aesthetic in 2 words? If not, it has no direction.
2. Would a designer recognize those fonts as intentional choices?
3. Is the layout doing something spatially unexpected?
4. Does the color palette feel like a decision, not a default?
5. Is there ONE thing you'll remember about this design tomorrow?
6. Could this be mistaken for any other AI-generated UI you've seen?
```

If questions 1–5 have weak answers and question 6 is "yes" — ask for a redesign.

---

## WHEN TO PUSH BACK ON AI OUTPUT

Use these phrases to get better results:

- **"That looks like AI slop. Rewrite the Design Declaration with a more committed aesthetic direction."**
- **"I can see Inter and rounded cards. You violated the bans. Start over from the Design Declaration."**
- **"The layout is hero → cards → CTA. That's the default. Give me something spatially unexpected."**
- **"Name the aesthetic in 2 words. If you can't, the design has no point of view."**
- **"What's the Signature Element? I don't see one."**

---

## FOR TEAMS — ENFORCING CONSISTENCY

Add this to your shared project rules (Cursor `.cursorrules`, Windsurf config, Claude Project):

```
All UI generated in this project must follow skills/anti-slop-design/SKILL.md
Design Declaration is required before any code.
PR reviews must include the Anti-Slop Audit checklist.
Aesthetic direction for this project: [INSERT YOUR DIRECTION HERE]
Approved fonts for this project: [INSERT YOUR FONTS HERE]
Approved palette for this project: [INSERT HEX VALUES HERE]
```

Locking project-level aesthetics means every team member's AI output converges 
on YOUR design system — not the AI's default pattern.

---

## CREDITS & DISTRIBUTION

**Version:** 2.0  
**Built by:** Glen E. Grant (glenegrant.com)  
**Based on:** Consistent work / Rework and Time  
**License:** CC BY 4.0 — share freely, credit appreciated  
**Tags:** `#frontend` `#anti-slop` `#design-system` `#ui` `#aesthetics` `#vibe-code-fix` `#glenski`

Share both files together:
- `skills/anti-slop-design/SKILL.md` — the full skill for AI systems
- `ANTI-SLOP-COMPANION-PROMPT.md` — this file, for humans using AI tools
