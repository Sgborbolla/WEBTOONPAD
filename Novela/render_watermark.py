#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_watermark.py — marca de agua transparente diagonal (watermark.png)."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT = "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf"
OUT  = os.path.join(BASE, "watermark.png")

W, H = 1414, 2000
A1, A2 = 60, 50  # opacidad: se ve, pero sigue tras el texto

def font(pt):
    return ImageFont.truetype(FONT, pt)

base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(capa)

l1 = "NIPPON POST-APOCALYPTIC DISASTER"
l2 = "Sergio Grabiel Borbolla Verdecia"

f1 = font(116)
f2 = font(72)
w1 = d.textlength(l1, font=f1)
w2 = d.textlength(l2, font=f2)

d.text(((W - w1) / 2, int(H * 0.44)), l1, font=f1, fill=(72, 72, 88, A1))
d.text(((W - w2) / 2, int(H * 0.44) + 160), l2, font=f2, fill=(72, 72, 88, A2))
d.text(((W - d.textlength("©", font=f2)) / 2, int(H * 0.44) + 230),
       "©", font=f2, fill=(88, 88, 105, A2))

capa = capa.rotate(-30, resample=Image.BILINEAR, expand=False)
base.alpha_composite(capa)
base.save(OUT)
print("OK ->", OUT, os.path.getsize(OUT), "bytes")