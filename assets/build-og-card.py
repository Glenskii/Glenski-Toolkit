#!/usr/bin/env python3
"""
Social Preview Card Generator
Glenski-Toolkit -- 1280x640px GitHub / Twitter OG card, dark edition
Glen E. Grant | glenegrant.com | github.com/Glenskii

Layout matches the approved glenski-web-research-mcp card. Repo-level card
covering the full skill lineup, not a single skill. Run with system Python
(Pillow required).
"""

from PIL import Image, ImageDraw, ImageFont

# --- Dimensions ----------------------------------------------------------------
W, H = 1280, 640

# --- Color System (dark edition) ------------------------------------------------
BG      = (10, 10, 10)
ORANGE  = (232, 93, 4)          # brand accent #E85D04
WHITE   = (255, 255, 255)
LIGHT   = (168, 168, 168)
MID     = (180, 180, 180)
DIM     = (200, 200, 200)
PILL_BG = (16, 16, 16)
DETAIL_COL = (160, 160, 160)

# --- Font Loader -----------------------------------------------------------------
FDIR = "C:/Users/Glen/.claude/skills/canvas-design/canvas-fonts/"

def font(name, size):
    try:
        return ImageFont.truetype(FDIR + name, size)
    except Exception as e:
        print(f"  [font] could not load {name}: {e}")
        return ImageFont.load_default()

# --- Canvas ------------------------------------------------------------------------
canvas = Image.new("RGB", (W, H), BG)
draw   = ImageDraw.Draw(canvas)

# --- Subtle dot grid (left zone only, very faint) -----------------------------------
for gx in range(0, 800, 36):
    for gy in range(0, H, 36):
        draw.point((gx, gy), fill=(19, 19, 19))

# --- Load fonts ----------------------------------------------------------------------
f_label   = font("InstrumentSans-Regular.ttf",  22)
f_heading = font("BigShoulders-Bold.ttf",        58)
f_sub     = font("InstrumentSans-Regular.ttf",   20)
f_code    = font("JetBrainsMono-Bold.ttf",       14)
f_feature = font("InstrumentSans-Regular.ttf",   16)
f_handle  = font("GeistMono-Regular.ttf",        16)

PAD = 72   # left margin
RIGHT_EDGE = 760  # pills / text wrap boundary before the vertical separator

# --- Measure heading block ------------------------------------------------------------
line1 = "glenski"
line2 = "toolkit"

f_heading_use = f_heading
b1 = draw.textbbox((0, 0), line1, font=f_heading_use)
w1 = b1[2] - b1[0]
if w1 > (RIGHT_EDGE - PAD - 10):
    f_heading_use = font("BigShoulders-Bold.ttf", 50)
    print("  Reduced heading to 50px")

b1m = draw.textbbox((0, 0), line1, font=f_heading_use)
b2m = draw.textbbox((0, 0), line2, font=f_heading_use)
H1  = b1m[3] - b1m[1]
H2  = b2m[3] - b2m[1]

# --- Pill layout: wraps across rows, 7 skills won't fit on one line ------------------
skills = [
    "human-writer", "universal-audit", "anti-slop-design", "frontend-taste",
    "cross-platform-compliance", "seo-aeo-geo-gbp", "vibe-security-audit",
]

def layout_pills(skills, start_x, max_x, pill_h_pad=13, pill_w_pad=22, gap=10, row_gap=10):
    """Returns (rows, total_height). Each row is a list of (label, x, w)."""
    rows = []
    current_row = []
    px = start_x
    row_h = 0
    for label in skills:
        bb = draw.textbbox((0, 0), label, font=f_code)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pw, ph = tw + pill_w_pad, th + pill_h_pad
        row_h = max(row_h, ph)
        if px + pw > max_x and current_row:
            rows.append((current_row, row_h))
            current_row = []
            px = start_x
            row_h = ph
        current_row.append((label, px, pw, ph))
        px += pw + gap
    if current_row:
        rows.append((current_row, row_h))
    total_h = sum(rh for _, rh in rows) + row_gap * (len(rows) - 1 if rows else 0)
    return rows, total_h

pill_rows, PILLS_TOTAL_H = layout_pills(skills, PAD, RIGHT_EDGE)

LABEL_H  = 26
GAP_LH   = 26   # label to heading
GAP_L12  = 6    # between heading lines
SUB_H    = 26
GAP_HS   = 20   # heading to subtitle
BAR_H    = 2
GAP_SB   = 30   # subtitle to bar
GAP_BP   = 16   # bar to pills
GAP_PF   = 34   # pills to feature line
FEAT_H   = 20
GAP_FD   = 26   # feature to detail
DETAIL_H = 20
GAP_DA   = 32   # detail to attribution divider
DIV_H    = 1
GAP_DT   = 14   # divider to attribution text
ATTR_H   = 18
ROW_GAP  = 10

TOTAL_H = (LABEL_H + GAP_LH + H1 + GAP_L12 + H2 + GAP_HS +
           SUB_H + GAP_SB + BAR_H + GAP_BP + PILLS_TOTAL_H + GAP_PF +
           FEAT_H + GAP_FD + DETAIL_H + GAP_DA + DIV_H + GAP_DT + ATTR_H)

TOP_PAD  = 130
BOT_PAD  = 40
AVAIL    = H - TOP_PAD - BOT_PAD
Y_START  = TOP_PAD + max(0, (AVAIL - TOTAL_H) // 2)

print(f"  Pill rows: {len(pill_rows)}, total content height: {TOTAL_H}px, starting at y={Y_START}")

# --- Draw content block ----------------------------------------------------------------
y = Y_START

# Repo label
draw.text((PAD, y), "github.com/Glenskii/Glenski-Toolkit", font=f_label, fill=WHITE)
y += LABEL_H + GAP_LH

# Heading line 1
draw.text((PAD, y), line1, font=f_heading_use, fill=WHITE)
y += H1 + GAP_L12

# Heading line 2
draw.text((PAD, y), line2, font=f_heading_use, fill=ORANGE)
y += H2 + GAP_HS

# Subtitle
draw.text((PAD, y), "Practical AI tools for creative and technical workflows.", font=f_sub, fill=LIGHT)
y += SUB_H + GAP_SB

# Orange accent bar
draw.rectangle([(PAD, y), (PAD + 200, y + BAR_H)], fill=ORANGE)
y += BAR_H + GAP_BP

# Skill pills, wrapped
Y_PILLS = y
row_y = Y_PILLS
for row, row_h in pill_rows:
    for label, px, pw, ph in row:
        draw.rounded_rectangle(
            [(px, row_y), (px + pw, row_y + ph)],
            radius=4, outline=ORANGE, fill=PILL_BG, width=1
        )
        draw.text((px + 11, row_y + 6), label, font=f_code, fill=ORANGE)
    row_y += row_h + ROW_GAP
y = row_y - ROW_GAP + GAP_PF

# Feature tagline
draw.text((PAD, y), "7 skills.   Enforced quality.   Zero templated output.",
          font=f_feature, fill=MID)
y += FEAT_H + GAP_FD

# Secondary detail
draw.text((PAD, y), "Design, security, SEO, audits, writing. Built for real use, free to share.",
          font=f_feature, fill=DETAIL_COL)
y += DETAIL_H + GAP_DA

# Divider
draw.line([(PAD, y), (700, y)], fill=(40, 40, 40), width=1)
y += DIV_H + GAP_DT

# Attribution -- white on dark
draw.text((PAD, y), "Glen E. Grant   ·   glenegrant.com", font=f_handle, fill=WHITE)

# --- Vertical separator (warm fade) -----------------------------------------------------
SEP_X = 800
for sy in range(H):
    dist = abs(sy - H / 2) / (H / 2)
    intensity = int(38 * (1 - dist ** 1.6))
    r = min(255, intensity * 6)
    g = min(255, intensity * 3)
    b = 0
    draw.point((SEP_X, sy), fill=(r, g, b))

# --- Right zone: logo ---------------------------------------------------------------------
LOGO_PATH = r"Y:\Dropbox\_Glen\_Logos\_SPECIAL\Glenski-logo.png"
logo_raw  = Image.open(LOGO_PATH).convert("RGBA")

LOGO_SIZE = 340
logo = logo_raw.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)

# Center horizontally in right zone (800 to 1280 = 480px)
right_cx = 800 + (1280 - 800) // 2   # = 1040
logo_x   = right_cx - LOGO_SIZE // 2
logo_y   = (H - LOGO_SIZE) // 2

# Faint orange glow behind logo
glow_cx  = logo_x + LOGO_SIZE // 2
glow_cy  = logo_y + LOGO_SIZE // 2
for step in range(22, 0, -1):
    intensity = int(12 * (step / 22) ** 2)
    r = min(255, ORANGE[0] * intensity // 12)
    g = min(255, ORANGE[1] * intensity // 12)
    radius   = LOGO_SIZE // 2 + step + 6
    draw.ellipse(
        [(glow_cx - radius, glow_cy - radius),
         (glow_cx + radius, glow_cy + radius)],
        outline=(r, g, 0), width=1
    )

# Paste logo with alpha
canvas.paste(logo, (logo_x, logo_y), logo)

# GitHub handle below logo
handle   = "github.com/Glenskii"
hb       = draw.textbbox((0, 0), handle, font=f_handle)
handle_w = hb[2] - hb[0]
handle_y = logo_y + LOGO_SIZE + 14
if handle_y + 18 < H - 20:
    draw.text(
        (right_cx - handle_w // 2, handle_y),
        handle, font=f_handle, fill=(100, 100, 100)
    )

# --- Save --------------------------------------------------------------------------------
OUT = "C:/Users/Glen/Documents/GitHub/Glenski-Github/assets/social-preview.png"
canvas.save(OUT, "PNG")
print(f"\n  Saved: {OUT}")
print(f"  Dimensions: {canvas.size}")
