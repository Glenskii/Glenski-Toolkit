#!/usr/bin/env python3
"""
Social Preview Card Generator
save-context -- 1280x640px GitHub / Twitter OG card, white edition
Glen E. Grant | glenegrant.com | github.com/Glenskii

Layout matches the approved glenski-web-research-mcp / universal-audit
white cards. Run with system Python (Pillow required).
"""

from PIL import Image, ImageDraw, ImageFont

# --- Dimensions --------------------------------------------------------------
W, H = 1280, 640

# --- Color System (white edition) ---------------------------------------------
BG      = (255, 255, 255)
ORANGE  = (232, 93, 4)          # brand accent #E85D04
INK     = (10, 10, 10)          # heading
SUBTLE  = (85, 85, 85)          # subtitle
FEATURE = (95, 95, 95)          # feature tagline
DETAIL  = (130, 130, 130)       # secondary detail
ATTR    = (110, 110, 110)       # attribution + handle
PILL_BG = (252, 247, 242)       # warm near-white pill fill
GRID    = (243, 243, 243)       # faint dot grid
DIVIDER = (225, 225, 225)

# --- Font Loader ---------------------------------------------------------------
FDIR = "C:/Users/Glen/.claude/skills/canvas-design/canvas-fonts/"

def font(name, size):
    try:
        return ImageFont.truetype(FDIR + name, size)
    except Exception as e:
        print(f"  [font] could not load {name}: {e}")
        return ImageFont.load_default()

# --- Canvas ---------------------------------------------------------------------
canvas = Image.new("RGB", (W, H), BG)
draw   = ImageDraw.Draw(canvas)

# --- Subtle dot grid (left zone only) ---------------------------------------------
for gx in range(0, 800, 36):
    for gy in range(0, H, 36):
        draw.point((gx, gy), fill=GRID)

# --- Load fonts -------------------------------------------------------------------
f_label   = font("InstrumentSans-Regular.ttf", 14)
f_heading = font("BigShoulders-Bold.ttf",      58)
f_sub     = font("InstrumentSans-Regular.ttf", 20)
f_code    = font("JetBrainsMono-Bold.ttf",     15)
f_feature = font("InstrumentSans-Regular.ttf", 15)
f_handle  = font("GeistMono-Regular.ttf",      13)

PAD = 72   # left margin

# --- Measure content block height to center it vertically -------------------------
line1 = "glenski"
line2 = "save-context"

f_heading_use = f_heading
b1 = draw.textbbox((0, 0), line1, font=f_heading_use)
w1 = b1[2] - b1[0]
if w1 > (800 - PAD - 10):
    f_heading_use = font("BigShoulders-Bold.ttf", 50)
    print("  Reduced heading to 50px")

b1m = draw.textbbox((0, 0), line1, font=f_heading_use)
b2m = draw.textbbox((0, 0), line2, font=f_heading_use)
H1  = b1m[3] - b1m[1]
H2  = b2m[3] - b2m[1]

LABEL_H  = 18
GAP_LH   = 20
GAP_L12  = 6
SUB_H    = 26
GAP_HS   = 20
BAR_H    = 2
GAP_SB   = 32
GAP_BP   = 16
PILL_H   = 36
GAP_PF   = 44
FEAT_H   = 20
GAP_FD   = 28
DETAIL_H = 20
GAP_DA   = 36
DIV_H    = 1
GAP_DT   = 14
ATTR_H   = 18

TOTAL_H = (LABEL_H + GAP_LH + H1 + GAP_L12 + H2 + GAP_HS +
           SUB_H + GAP_SB + BAR_H + GAP_BP + PILL_H + GAP_PF +
           FEAT_H + GAP_FD + DETAIL_H + GAP_DA + DIV_H + GAP_DT + ATTR_H)

TOP_PAD = 56
BOT_PAD = 48
AVAIL   = H - TOP_PAD - BOT_PAD
Y_START = TOP_PAD + max(0, (AVAIL - TOTAL_H) // 2)

# --- Draw content block ---------------------------------------------------------
y = Y_START

# Repo label
draw.text((PAD, y), "github.com/Glenskii/Glenski-Toolkit", font=f_label, fill=ORANGE)
y += LABEL_H + GAP_LH

# Heading line 1
draw.text((PAD, y), line1, font=f_heading_use, fill=INK)
y += H1 + GAP_L12

# Heading line 2
draw.text((PAD, y), line2, font=f_heading_use, fill=ORANGE)
y += H2 + GAP_HS

# Subtitle
draw.text((PAD, y), "Compaction and new chats both lose context. This stops that.", font=f_sub, fill=SUBTLE)
y += SUB_H + GAP_SB

# Orange accent bar
draw.rectangle([(PAD, y), (PAD + 200, y + BAR_H)], fill=ORANGE)
y += BAR_H + GAP_BP

# Concept pills
Y_PILLS = y
tools = ["auto-detect env", "pre-compact", "cross-agent"]
px = PAD
for label in tools:
    bb = draw.textbbox((0, 0), label, font=f_code)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    pw = tw + 22
    ph = th + 13
    draw.rounded_rectangle(
        [(px, Y_PILLS), (px + pw, Y_PILLS + ph)],
        radius=4, outline=ORANGE, fill=PILL_BG, width=1
    )
    draw.text((px + 11, Y_PILLS + 6), label, font=f_code, fill=ORANGE)
    px += pw + 10
y += PILL_H + GAP_PF

# Feature tagline
draw.text((PAD, y), "Claude memory.   Codex AGENTS.md.   Generic fallback.",
          font=f_feature, fill=FEATURE)
y += FEAT_H + GAP_FD

# Secondary detail
draw.text((PAD, y), "Hard verification rule.   Structured final report.   Zero silent skips.",
          font=f_feature, fill=DETAIL)
y += DETAIL_H + GAP_DA

# Divider
draw.line([(PAD, y), (700, y)], fill=DIVIDER, width=1)
y += DIV_H + GAP_DT

# Attribution
draw.text((PAD, y), "Glen E. Grant   ·   glenegrant.com", font=f_handle, fill=ATTR)
ATTRIBUTION_Y = y  # reused to align the right-zone handle below the logo

# --- Vertical separator (warm fade, tuned for white) ------------------------------
SEP_X = 800
for sy in range(H):
    dist = abs(sy - H / 2) / (H / 2)
    strength = (1 - dist ** 1.6)
    r = int(255 - (255 - ORANGE[0]) * strength)
    g = int(255 - (255 - ORANGE[1]) * strength)
    b = int(255 - (255 - ORANGE[2]) * strength)
    draw.point((SEP_X, sy), fill=(r, g, b))

# --- Right zone: logo ---------------------------------------------------------------
LOGO_PATH = r"Y:\Dropbox\_Glen\_Logos\_SPECIAL\Glenski-logo.png"
logo_raw  = Image.open(LOGO_PATH).convert("RGBA")

LOGO_SIZE = 340
logo = logo_raw.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)

right_cx = 800 + (1280 - 800) // 2
logo_x   = right_cx - LOGO_SIZE // 2
logo_y   = (H - LOGO_SIZE) // 2 - 30  # shifted up to leave clearance for handle below

# Faint orange ring glow behind logo, blended toward white
glow_cx = logo_x + LOGO_SIZE // 2
glow_cy = logo_y + LOGO_SIZE // 2
for step in range(16, 0, -1):
    strength = (step / 16) ** 2 * 0.55
    r = int(255 - (255 - ORANGE[0]) * strength)
    g = int(255 - (255 - ORANGE[1]) * strength)
    b = int(255 - (255 - ORANGE[2]) * strength)
    radius = LOGO_SIZE // 2 + step + 6
    draw.ellipse(
        [(glow_cx - radius, glow_cy - radius),
         (glow_cx + radius, glow_cy + radius)],
        outline=(r, g, b), width=1
    )

canvas.paste(logo, (logo_x, logo_y), logo)

# GitHub handle, aligned with the left attribution line, same white/ink
# InstrumentSans label style and size as the top repo-URL line
handle   = "github.com/Glenskii"
hb       = draw.textbbox((0, 0), handle, font=f_label)
handle_w = hb[2] - hb[0]
draw.text(
    (right_cx - handle_w // 2, ATTRIBUTION_Y),
    handle, font=f_label, fill=INK
)

# --- Save ------------------------------------------------------------------------------
OUT = "C:/Users/Glen/.claude/skills/save-context/assets/social-preview.png"
canvas.save(OUT, "PNG")
print(f"  Saved: {OUT}")
print(f"  Dimensions: {canvas.size}")
