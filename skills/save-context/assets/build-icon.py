#!/usr/bin/env python3
"""
Icon generator for save-context's agents/openai.yaml
icon_large: 512x512px PNG, Glenski dark rounded-square tile with an orange
floppy-disk (save) glyph, matching icon-small.svg's line art.
Glen E. Grant | glenegrant.com | github.com/Glenskii
"""

from PIL import Image, ImageDraw

W, H = 512, 512
BG     = (10, 10, 10, 255)     # #0A0A0A
ORANGE = (232, 93, 4, 255)     # #E85D04
TRANSPARENT = (0, 0, 0, 0)

# Supersample for clean anti-aliased curves, then downscale
SS = 4
canvas = Image.new("RGBA", (W * SS, H * SS), TRANSPARENT)
draw = Image.new("RGBA", (W * SS, H * SS), TRANSPARENT)
d = ImageDraw.Draw(draw)

# Rounded-square dark background tile
pad = 8 * SS
radius = 96 * SS
d.rounded_rectangle(
    [(pad, pad), (W * SS - pad, H * SS - pad)],
    radius=radius, fill=BG
)

# Floppy-disk glyph, scaled from the 24x24 viewBox of icon-small.svg
scale = (W * SS) / 24
stroke_w = max(2, int(1.6 * scale * 0.5))

def pt(x, y):
    return (x * scale, y * scale)

# Outer body: clean rounded rectangle, matches the simplified icon-small.svg
d.rounded_rectangle(
    [pt(3.5, 3.5)[0], pt(3.5, 3.5)[1], pt(20.5, 20.5)[0], pt(20.5, 20.5)[1]],
    radius=3 * scale, outline=ORANGE, width=stroke_w
)

# Label window (top rectangle)
d.rectangle(
    [pt(7.5, 3.5)[0], pt(7.5, 3.5)[1], pt(14.5, 9)[0], pt(14.5, 9)[1]],
    outline=ORANGE, width=stroke_w
)

# Data slot (bottom rectangle)
d.rectangle(
    [pt(7.5, 14.5)[0], pt(7.5, 14.5)[1], pt(16.5, 20.5)[0], pt(16.5, 20.5)[1]],
    outline=ORANGE, width=stroke_w
)

canvas = Image.alpha_composite(canvas, draw)
canvas = canvas.resize((W, H), Image.LANCZOS)

OUT = "C:/Users/Glen/.claude/skills/save-context/assets/icon-large.png"
canvas.save(OUT, "PNG")
print(f"Saved: {OUT}")
print(f"Dimensions: {canvas.size}")
