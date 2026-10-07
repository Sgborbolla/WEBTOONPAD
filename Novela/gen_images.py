#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_images.py — descarga ilustraciones a crayon (estilo coreano/japones) via Pollinations."""
import os, urllib.request, urllib.parse, io
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "img")
os.makedirs(OUTDIR, exist_ok=True)

def fetch(name, prompt, w=1024, h=640, seed=0):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) +
           "?width=%d&height=%d&nologo=true&model=flux&seed=%d" % (w, h, seed))
    print("descargando", name, "...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=120).read()
    im = Image.open(io.BytesIO(data)).convert("RGB")
    p = os.path.join(OUTDIR, name + ".png")
    im.save(p, "PNG")
    print("OK ->", p, im.size, len(data), "bytes")

fetch("cap01_portal", "Korean webtoon crayon illustration, dawn attack on a Yokohama port street, a tall black rectangular portal hovering upright in the asphalt releasing thick mist and monstrous dark beasts with too-long legs emerging and running, a man staring from a window, street lamps, muted teal and salmon palette, hand drawn colored crayon texture, paper grain, painterly, emotional, cinematic wide shot", seed=11)
fetch("cap01_batalla", "Korean webtoon crayon illustration, aerial battle over a ruined city at dawn, monstrous dark beasts fighting a military response, tanks firing flames and smoke, a helicopter flying low, fighter jets in the sky, artillery explosions across the street, soldiers running and firing, chaos, dramatic aerial perspective, hand drawn colored crayon texture, paper grain, muted gritty palette with orange explosion glow, painterly, cinematic", seed=23)
fetch("cap03_calle", "Korean webtoon crayon illustration, quiet lamplit street at blue hour, an old woman in a grey shawl with a red vegetable cart, a huge flat shadow creature with a head and an orange ember edge crouched on the asphalt, empty dangerous street, hand drawn colored crayon texture, paper grain, muted palette, cinematic, emotional", seed=37)
fetch("cap05_descarga", "Korean webtoon crayon illustration, night street, armored man kneeling on asphalt beside a fallen worker, round shield on the ground, faint wisps of steam and an orange glowing glove on the asphalt, dark flat shadow splitting into three pieces sliding away, street lamps, hand drawn colored crayon texture, paper grain, muted palette, tragedy, cinematic", seed=47)