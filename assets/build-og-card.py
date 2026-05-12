#!/usr/bin/env python3
"""
Social Preview Card Generator
glenski-web-research-mcp -- 1280x640px GitHub / Twitter OG card
Glen E. Grant | glenegrant.com | github.com/Glenskii
"""

from PIL import Image, ImageDraw, ImageFont

# ─── Dimensions ──────────────────────────────────────────────────────────────
W, H = 1280, 640

# ─── Color System ────────────────────────────────────────────────────────────
BG      = (10, 10, 10)
ORANGE  = (232, 93, 4)
WHITE   = (255, 255, 255)
LIGHT   = (168, 168, 168)
MID     = (105, 105, 105)
DIM     = (55, 55, 55)
PILL_BG = (16, 16, 16)

# ─── Font Loader ─────────────────────────────────────────────────────────────
FDIR = "C:/Users/Glen/.claude/skills/canvas-design/canvas-fonts/"

def font(name, size):
    try:
        return ImageFont.truetype(FDIR + name, size)
    except Exception as e:
        print(f"  [font] could not load {name}: {e}")
        return ImageFont.load_default()

# ─── Canvas ──────────────────────────────────────────────────────────────────
canvas = Image.new("RGB", (W, H), BG)
draw   = ImageDraw.Draw(canvas)

# ─── Subtle dot grid (left zone only, very faint) ────────────────────────────
for gx in range(0, 800, 36):
    for gy in range(0, H, 36):
        draw.point((gx, gy), fill=(19, 19, 19))

# ─── Load fonts ──────────────────────────────────────────────────────────────
f_label   = font("InstrumentSans-Regular.ttf",  14)
f_heading = font("BigShoulders-Bold.ttf",        60)
f_sub     = font("InstrumentSans-Regular.ttf",   21)
f_code    = font("JetBrainsMono-Bold.ttf",       15)
f_feature = font("InstrumentSans-Regular.ttf",   15)
f_handle  = font("GeistMono-Regular.ttf",        13)

PAD = 72   # left margin

# ─── Measure content block height to center it vertically ────────────────────
line1 = "glenski-web-research"
line2 = "— mcp"

f_heading_use = f_heading
b1 = draw.textbbox((0, 0), line1, font=f_heading_use)
w1 = b1[2] - b1[0]
print(f"  Heading line 1 width: {w1}px  (available: {800 - PAD}px)")
if w1 > (800 - PAD - 10):
    f_heading_use = font("BigShoulders-Bold.ttf", 52)
    print("  Reduced heading to 52px")

b1m = draw.textbbox((0, 0), line1, font=f_heading_use)
b2m = draw.textbbox((0, 0), line2, font=f_heading_use)
H1  = b1m[3] - b1m[1]
H2  = b2m[3] - b2m[1]

LABEL_H  = 18
GAP_LH   = 20   # label to heading
GAP_L12  = 6    # between heading lines
SUB_H    = 26
GAP_HS   = 20   # heading to subtitle
BAR_H    = 2
GAP_SB   = 32   # subtitle to bar
GAP_BP   = 16   # bar to pills
PILL_H   = 36
GAP_PF   = 44   # pills to feature line
FEAT_H   = 20
GAP_FD   = 28   # feature to detail
DETAIL_H = 20
GAP_DA   = 36   # detail to attribution divider
DIV_H    = 1
GAP_DT   = 14   # divider to attribution text
ATTR_H   = 18

TOTAL_H = (LABEL_H + GAP_LH + H1 + GAP_L12 + H2 + GAP_HS +
           SUB_H + GAP_SB + BAR_H + GAP_BP + PILL_H + GAP_PF +
           FEAT_H + GAP_FD + DETAIL_H + GAP_DA + DIV_H + GAP_DT + ATTR_H)

TOP_PAD  = 56
BOT_PAD  = 48
AVAIL    = H - TOP_PAD - BOT_PAD
Y_START  = TOP_PAD + max(0, (AVAIL - TOTAL_H) // 2)

print(f"  Total content height: {TOTAL_H}px, starting at y={Y_START}")

# ─── Draw content block ──────────────────────────────────────────────────────
y = Y_START

# Repo label
draw.text((PAD, y), "github.com/Glenskii/Glenski-Toolkit", font=f_label, fill=ORANGE)
y += LABEL_H + GAP_LH

# Heading line 1
draw.text((PAD, y), line1, font=f_heading_use, fill=WHITE)
y += H1 + GAP_L12

# Heading line 2
draw.text((PAD, y), line2, font=f_heading_use, fill=ORANGE)
y += H2 + GAP_HS

# Subtitle
draw.text((PAD, y), "API-free live research for Claude.", font=f_sub, fill=LIGHT)
y += SUB_H + GAP_SB

# Orange accent bar
draw.rectangle([(PAD, y), (PAD + 200, y + BAR_H)], fill=ORANGE)
y += BAR_H + GAP_BP

# Tool pills
Y_PILLS = y
tools = ["web_search", "fetch_page", "multi_search"]
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
draw.text((PAD, y), "Zero API keys.   DuckDuckGo-powered.   MCP-native.",
          font=f_feature, fill=MID)
y += FEAT_H + GAP_FD

# Secondary detail
draw.text((PAD, y), "Parallel search.   JS-page detection.   Playwright-ready.",
          font=f_feature, fill=(75, 75, 75))
y += DETAIL_H + GAP_DA

# Divider
draw.line([(PAD, y), (700, y)], fill=(26, 26, 26), width=1)
y += DIV_H + GAP_DT

# Attribution
draw.text((PAD, y), "Glen E. Grant   ·   glenegrant.com",
          font=f_handle, fill=(90, 90, 90))

# ─── Vertical separator (warm fade) ──────────────────────────────────────────
SEP_X = 800
for sy in range(H):
    dist = abs(sy - H / 2) / (H / 2)
    intensity = int(38 * (1 - dist ** 1.6))
    r = min(255, intensity * 6)
    g = min(255, intensity * 3)
    b = 0
    draw.point((SEP_X, sy), fill=(r, g, b))

# ─── Right zone: logo ────────────────────────────────────────────────────────
LOGO_PATH = "C:/Users/Glen/Documents/GitHub/Glenski-Github/assets/GEG-Head-logo.png"
logo_raw  = Image.open(LOGO_PATH).convert("RGBA")

LOGO_SIZE = 420
logo = logo_raw.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)

# Center horizontally in right zone (800 to 1280 = 480px)
right_cx = 800 + (1280 - 800) // 2   # = 1040
logo_x   = right_cx - LOGO_SIZE // 2  # = 830
logo_y   = (H - LOGO_SIZE) // 2       # = 110

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
if handle_y + 18 < H - 20:   # only draw if it fits
    draw.text(
        (right_cx - handle_w // 2, handle_y),
        handle, font=f_handle, fill=(100, 100, 100)
    )

# ─── Save ────────────────────────────────────────────────────────────────────
OUT = "C:/Users/Glen/Documents/GitHub/Glenski-Github/assets/social-preview.png"
canvas.save(OUT, "PNG")
print(f"\n  Saved: {OUT}")
print(f"  Dimensions: {canvas.size}")
