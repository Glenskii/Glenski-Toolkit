---
name: "anti-slop-design"
title: "ANTI-SLOP DESIGN SKILL"
version: "2.0"
description: >
  Forces AI code generators to produce genuinely distinctive, original UI instead of
  recycled default aesthetics. Requires a mandatory Design Declaration before any code
  is written: named aesthetic direction, explicit rejections, committed typography and
  color logic, spatial layout strategy, and a 12-point quality gate checklist.
  Use whenever building UI, designing components, or generating frontend code.
author: "Glen E. Grant"
website: "https://glenegrant.com"
derived_from: "anthropics/skills frontend-design"
compatible_with:
  - "Claude"
  - "Claude Projects"
  - "GPT-4o"
  - "Gemini"
  - "Cursor"
  - "Windsurf"
  - "Any LLM-powered IDE"
license: "CC BY 4.0"
repo: "https://github.com/Glenskii/Glenski-Toolkit"
tags:
  - "frontend"
  - "anti-slop"
  - "design-system"
  - "ui"
  - "aesthetics"
  - "vibe-code-fix"
  - "glenski"
---

# ANTI-SLOP DESIGN SKILL v2.0

**Author:** Glen E. Grant / Derived from anthropics/skills frontend-design  
**Purpose:** Force AI code generators to produce genuinely distinctive, original UI — not recycled "vibe code" aesthetics.  
**Compatible:** Claude, GPT-4o, Gemini, Cursor, Windsurf, any LLM-powered IDE  

---

## THE CORE PROBLEM THIS SKILL SOLVES

Every AI-generated UI looks the same because models default to their most statistically common training patterns:

- Font: Inter or Space Grotesk
- Color: Purple/indigo gradient on white
- Layout: Hero → Feature cards → CTA
- Buttons: Rounded pill, soft shadow
- Cards: White, border-radius 12px, subtle drop shadow

This is not design. This is pattern collapse. This skill breaks it.

---

## MANDATORY PRE-CODE DECLARATION

**BEFORE writing a single line of code, the AI must output this block:**

```
DESIGN DECLARATION
==================
Aesthetic Direction : [name the specific aesthetic — not "modern" or "clean"]
Rejected Defaults   : [list at least 3 things you are explicitly NOT doing]
Typography Pairing  : [Display font] + [Body font] — NO Inter, Roboto, Arial, system-ui
Color Commitment    : [Primary] / [Secondary] / [Accent] — NO purple gradients
Layout Strategy     : [describe the spatial logic — not "responsive grid"]
Signature Element   : [the ONE thing that makes this unforgettable]
Accessibility Note  : [WCAG contrast ratio confirmed / keyboard nav approach]
```

If the AI cannot complete this block with specifics, it is not ready to code. Reject vague answers.

---

## AESTHETIC DIRECTION LIBRARY

Choose ONE and execute with full commitment. Mixing dilutes everything.

### TIER 1 — HIGH CONTRAST / EDITORIAL
| Direction | Signature Traits | Font Class | Color Logic |
|-----------|-----------------|------------|-------------|
| **Swiss Brutalist** | Heavy rules, grid exposed, text as structure | Neue Haas Grotesk, Suisse Int'l | Black + one raw primary |
| **Editorial Magazine** | Asymmetric columns, pull quotes, photo-driven | Freight Display, Canela, Domaine | Off-white + ink black + one warm tone |
| **Soviet Constructivist** | Diagonal geometry, stark contrast, agitprop energy | Bebas Neue, Druk Wide | Red + black + cream |
| **Typographic Brutalism** | Type IS the layout, minimal graphic elements | Monument Extended, Migra | Monochrome + one electric accent |

### TIER 2 — ATMOSPHERE / MOOD
| Direction | Signature Traits | Font Class | Color Logic |
|-----------|-----------------|------------|-------------|
| **Dark Luxe** | Deep blacks, gold/copper metallics, deliberate spacing | Cormorant Garamond, Optima | Near-black + precious metal accent |
| **Analog Warmth** | Grain texture, warm off-whites, ink-on-paper feel | Playfair Display, Lora | Warm cream + walnut brown + rust |
| **Cyberpunk Terminal** | Scanlines, phosphor glow, monospace everything | JetBrains Mono, IBM Plex Mono | Terminal green / amber on near-black |
| **Organic Wabi-Sabi** | Imperfection as beauty, natural textures, breathing space | Shippori Mincho, EB Garamond | Earth palette, no pure white or black |

### TIER 3 — STRUCTURE / SYSTEM
| Direction | Signature Traits | Font Class | Color Logic |
|-----------|-----------------|------------|-------------|
| **Industrial Data** | Dense information, utilitarian chrome, no decoration | IBM Plex Sans, DM Mono | Gunmetal + signal orange + white |
| **Art Deco Revival** | Geometric ornament, symmetry, glamour | Poiret One, Josefin Sans | Gold + deep navy + ivory |
| **Flat Isometric** | Dimensional illustration, zero shadow, geometric | Nunito, Fredoka | Bold primaries, limited palette |
| **Deconstructed Grid** | Intentional misalignment, overlapping layers, tension | Syne, Space Mono | Multi-tone with controlled chaos |

---

## TYPOGRAPHY RULES — NON-NEGOTIABLE

### Banned Fonts (Immediate Reject)
```
Inter, Roboto, Arial, Helvetica, system-ui, -apple-system,
Space Grotesk, DM Sans, Poppins, Nunito Sans, Lato, Open Sans
```

### Approved Pairing Formulas

**Formula A — Contrast Serif/Sans**
- Display: Cormorant Garamond, Freight Display, Canela, Domaine
- Body: Neue Haas Grotesk, Aktiv Grotesk, Suisse Int'l

**Formula B — Mono/Serif Stack**  
- Display: Playfair Display, IM Fell English, Libre Baskerville
- Body: JetBrains Mono, IBM Plex Mono, Courier Prime

**Formula C — All Grotesque (Weight Contrast)**
- Display: Monument Extended, Druk Wide, Bebas Neue (heavy weight)
- Body: Aktiv Grotesk Light or Regular (extreme weight contrast)

**Formula D — Variable Font Exploitation**
- Use a single variable font across all weights
- Animate font-weight on hover for micro-interaction
- Example: Recursive, Fraunces, Amstelvar

### Type Scale — Use Fluid Sizing
```css
/* Use clamp() — never fixed px type */
--text-display: clamp(3rem, 8vw, 9rem);
--text-heading: clamp(1.75rem, 4vw, 3.5rem);
--text-body: clamp(1rem, 1.5vw, 1.25rem);
--text-caption: clamp(0.75rem, 1vw, 0.875rem);
```

---

## COLOR SYSTEM RULES

### Banned Color Patterns
```
- Purple/violet + white background (most common AI default)
- Blue gradient headers
- Teal + coral "startup" combinations
- Grey cards on white background
- Any palette that looks like it came from Tailwind's default config
```

### Color Construction Method

**Step 1:** Choose a dominant temperature (warm / cool / neutral)  
**Step 2:** Pick one **unexpected** primary — not blue, not purple  
**Step 3:** Add a secondary that creates tension, not harmony  
**Step 4:** Add ONE accent — high contrast, used sparingly  
**Step 5:** Define surface colors from primary tone, not grey scale  

### Strong Palette Examples
```css
/* Palette: Scorched Earth */
--color-primary: #1C1208;    /* near-black warm */
--color-secondary: #C4500A;  /* burnt orange */
--color-accent: #F2C94C;     /* raw gold */
--color-surface: #2A1F12;    /* warm dark surface */
--color-text: #F5ECD7;       /* warm off-white */

/* Palette: Baltic Winter */
--color-primary: #0D1B2A;    /* deep navy */
--color-secondary: #415A77;  /* steel blue */
--color-accent: #E0FBFC;     /* ice */
--color-surface: #1B2838;    /* dark surface */
--color-text: #E0E0E0;       /* cool grey text */

/* Palette: Letterpress */
--color-primary: #F4ECD8;    /* aged paper */
--color-secondary: #2C2416;  /* ink black */
--color-accent: #8B1A1A;     /* deep red */
--color-surface: #EDE4CC;    /* warm card surface */
--color-text: #1A1108;       /* near-black warm */
```

---

## LAYOUT — BREAK THE GRID

### Banned Layout Patterns
```
- Full-width hero with centered headline + subtitle + CTA button
- 3-column feature card grid
- Alternating image-left / text-right sections
- Sticky nav + hero + features + testimonials + footer (in that order)
- Any layout where every section is 100vw full-bleed centered content
```

### Required Spatial Thinking

**Before laying out any section, answer:**
1. Where does the eye enter the page?
2. Where does it travel next?
3. Where does it rest?
4. What creates the tension that keeps someone reading?

### Approved Layout Strategies

**Asymmetric Column Split**
```css
.layout-split {
  display: grid;
  grid-template-columns: 1fr 2.618fr; /* golden ratio split */
}
```

**Overlapping Z-Layers**
```css
.hero-overlap {
  display: grid;
  grid-template-areas: "main";
}
.hero-overlap > * { grid-area: main; }
/* Elements overlap — use z-index and margin offsets */
```

**Viewport-Anchored Typography**
```css
.headline-giant {
  font-size: clamp(4rem, 15vw, 18rem);
  line-height: 0.9;
  letter-spacing: -0.04em;
  /* Type as the layout — not decoration */
}
```

---

## MOTION — PURPOSEFUL, NOT DECORATIVE

### Banned Motion Patterns
```
- Fade in everything on scroll (lazy, expected)
- Bounce animations on buttons
- Infinite rotating loaders
- Parallax on every section
- AOS (Animate On Scroll) default presets
```

### One Signature Motion Rule
Choose ONE signature animation for the entire project and do it exceptionally well:

| Motion Type | When to Use | Implementation |
|-------------|-------------|----------------|
| **Text Reveal (clip-path)** | Hero headlines | CSS clip-path animation, staggered per word |
| **Magnetic Hover** | CTA buttons, cards | JS mouse tracking, transform translate |
| **Scramble Text** | Data displays, terminals | JS character randomization on hover |
| **SVG Path Draw** | Logo reveals, icons | stroke-dashoffset animation |
| **Morph Shape** | Background elements | CSS clip-path keyframes between shapes |
| **Variable Font Animate** | Display type | font-weight / font-variation-settings transition |

```css
/* Example: Text Reveal — the RIGHT way */
.reveal-word {
  overflow: hidden;
  display: inline-block;
}
.reveal-word span {
  display: inline-block;
  transform: translateY(110%);
  animation: reveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: calc(var(--word-index) * 0.08s);
}
@keyframes reveal {
  to { transform: translateY(0); }
}
```

---

## SURFACE & ATMOSPHERE

### Required: No Flat Solid Backgrounds

Every surface needs a reason to exist. Choose one approach per project:

```css
/* Approach 1: Grain Texture Overlay */
.surface::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* SVG noise */
  opacity: 0.04;
  pointer-events: none;
}

/* Approach 2: Gradient Mesh */
.surface {
  background: 
    radial-gradient(ellipse at 20% 50%, hsla(25,80%,30%,0.4) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, hsla(200,60%,20%,0.3) 0%, transparent 50%),
    var(--color-primary);
}

/* Approach 3: CSS Pattern */
.surface {
  background-color: var(--color-primary);
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.02) 2px,
    rgba(255,255,255,0.02) 4px
  );
}
```

---

## COMPONENT RULES

### Buttons — Never Default
```css
/* NOT this */
.btn { border-radius: 9999px; padding: 12px 24px; }

/* Instead: choose a character */
.btn-brutalist {
  border: 3px solid currentColor;
  border-radius: 0;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.75rem;
  transition: background 0.15s, color 0.15s;
}
.btn-brutalist:hover {
  background: var(--color-text);
  color: var(--color-primary);
}
```

### Cards — No Default Shadow Cards
```css
/* NOT this */
.card { background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }

/* Instead: use border, inset, or color */
.card-editorial {
  border-top: 3px solid var(--color-accent);
  padding: 2rem 0;
  background: transparent;
}
```

---

## QUALITY GATE CHECKLIST

Run this before declaring any UI complete:

```
ANTI-SLOP AUDIT
===============
[ ] Design Declaration was written BEFORE code started
[ ] Zero banned fonts used (grep for Inter, Roboto, Arial)
[ ] Zero purple/indigo gradient backgrounds
[ ] Layout does NOT follow hero → cards → CTA pattern
[ ] At least one unexpected spatial decision made
[ ] Surface has texture/depth (not flat solid color)
[ ] Buttons have character (not pill-shaped with soft shadow)
[ ] ONE signature motion — executed well, not scattered
[ ] Fluid type sizing with clamp()
[ ] CSS custom properties for ALL design tokens
[ ] WCAG AA contrast ratio confirmed on all text
[ ] Would a designer be able to name the aesthetic in 2 words?
```

If any box is unchecked: revise before shipping.

---

## COMPANION FILES

See the full human guide and prompt templates in the repo root:

- [`anti-slop-companion-prompt.md`](../../anti-slop-companion-prompt.md) — Request templates, pushback phrases, quality checklist for humans
- [`claude-project-instructions.md`](../../claude-project-instructions.md) — 5-step Claude Projects setup

Full repo: [github.com/Glenskii/Glenski-Toolkit](https://github.com/Glenskii/Glenski-Toolkit)

---

## METADATA

**Version:** 2.0  
**Built by:** Glen E. Grant ([glenegrant.com](https://glenegrant.com))  
**License:** CC BY 4.0 — share freely, credit appreciated  
**Tags:** `#frontend` `#anti-slop` `#design-system` `#ui` `#aesthetics` `#vibe-code-fix` `#glenski`
