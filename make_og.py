#!/usr/bin/env python3
"""og.png 1200x630 — Saint Mars: dark listening-room art with vinyl groove rings, brass label type.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

def font(path_names, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in path_names:
            p = b + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

ESPRESSO = (22, 17, 13); GROOVE1 = (13, 10, 6); GROOVE2 = (24, 18, 11)
CREAM = (243, 234, 217); MUTED = (185, 169, 142); BRASS = (201, 162, 79); BRASS2 = (226, 192, 107)

img = Image.new("RGB", (W, H), ESPRESSO)
d = ImageDraw.Draw(img, "RGBA")

# vertical wash: lighter at top
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(26 - 8 * t), int(20 - 6 * t), int(15 - 5 * t)))

# groove rings centered off the right edge, like a record parked mid-field
cx, cy = 1010, 315
for r in range(60, 470, 6):
    alpha = 26 if (r // 6) % 2 == 0 else 12
    col = GROOVE2 if (r // 6) % 2 == 0 else GROOVE1
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (alpha,), width=3)
# brass outer rim + label rings
d.ellipse((cx - 468, cy - 468, cx + 468, cy + 468), outline=BRASS + (60,), width=2)
d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=(196, 156, 76) + (255,))
d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=(150, 116, 52) + (255,), width=2)
d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=ESPRESSO + (255,))

f_eye = font(["Arial Bold.ttf", "Helvetica.ttc"], 21)
f_title = font(["Georgia Bold.ttf", "Georgia Italic.ttf", "Georgia.ttf", "Times New Roman.ttf"], 118)
f_sub = font(["Georgia Italic.ttf", "Georgia.ttf"], 30)
f_nap = font(["Helvetica.ttc", "Arial.ttf"], 19)

def tracked(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x

# left text block
tracked(d, (78, 118), "VINYL ONLY · FULL RECORDS · DEAD AIR INCLUDED", f_eye, BRASS, tracking=3)
d.text((74, 168), "Saint Mars", font=f_title, fill=CREAM)
d.text((78, 318), "A listening room and cocktail bar", font=f_sub, fill=CREAM)
d.text((78, 358), "beneath Bar Virgile · Durham, NC", font=f_sub, fill=MUTED)

# hairline + NAP line
d.line([(78, 520), (560, 520)], fill=BRASS + (140,), width=2)
d.text((78, 542), "105 S Mangum St  ·  (919) 973-3000  ·  open until 1 AM", font=f_nap, fill=MUTED)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
