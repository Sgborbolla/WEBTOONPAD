#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webtoon_v2.py — pipeline v2 (reglas profesionales de tira webtoon).

Una ILUSTRACIÓN POR PANEL a 1600 px de ancho, bajada a 800 px y montada con
los gutters de cap1.txt. Los textos/glbos/cajas/SFX los pone maquetador.py.

Uso:
  python3 webtoon_v2.py demo            # paneliza S07+S08 de cap01 y arma la tira
  python3 webtoon_v2.py cap N           # paneliza todo el arte que falte de capN
  python3 webtoon_v2.py todo            # caps 1-10
"""
import json, os, re, sys, time, urllib.request, urllib.parse
import art_multi as A
from io import BytesIO
from PIL import Image
import webtoon_estilo as est

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(RAIZ, "img")

def desc_viñetas(cap):
    s = open(os.path.join(RAIZ, "Guiones", "cap%02d.txt" % cap),
             encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^\*\*[Vv]?(\d+)\.\*\*\s*(.+)$", s, re.M):
        n = int(m.group(1))
        txt = re.sub(r"\s+", " ", m.group(2)).strip()
        txt = re.sub(r"\*\*(.+?)\*\*", r"\1", txt)
        txt = txt.strip(" .")[:500]
        if txt:
            out[n] = txt
    return out

def prompt_panel(vnum, descs):
    d = descs.get(vnum, "")
    if not d:
        for k in range(vnum + 1, vnum + 3):
            if k in descs:
                d = descs[k]; break
    partes = []
    if d:
        partes.append(d.capitalize()[:380])
    fichas = est.desc_personajes(d or "")
    if fichas:
        partes.extend(fichas)
    else:
        partes.append(est.ESCENA_VACIA)
    partes.append(est.estilo())
    partes.append(est.DESC_KI)
    return ". ".join(p for p in partes if p)

def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": "npad-v2"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def gen_panel(cap, n, i, ph, prompt, dest):
    w2, h2 = 800, ph
    for intento in range(3):
        try:
            data = A.generar(prompt, w2, h2)
            if len(data) < 5000:
                print(f"    s{n:02d}p{i+1}: corta ({len(data)}b), reintento")
                time.sleep(8); continue
            im = Image.open(BytesIO(data)).convert("RGB")
            im = A.recortar_a(im, w2, h2)
            est.grade(im).save(dest)
            print(f"    s{n:02d}p{i+1}: ok ({len(data)//1024}KB)")
            return True
        except Exception as e:
            print(f"    s{n:02d}p{i+1}: {type(e).__name__} {e}; reintento {intento+1}")
            time.sleep(12 + intento * 10)
    return False

def panelizar(cap, ns=None):
    dirs = os.path.join(IMG, "cap%02d" % cap)
    mp = os.path.join(dirs, "manifest.json")
    m = json.load(open(mp, encoding="utf-8"))
    descs = desc_viñetas(cap)
    hecho = 0
    for scr in m["screens"]:
        if ns is not None and scr["n"] not in ns:
            continue
        n = scr["n"]
        v0 = scr.get("vinheta_inicio", 1)
        for i, ph in enumerate(scr["paneles"]):
            dest = os.path.join(dirs, "s%02d_p%d.png" % (n, i + 1))
            if os.path.exists(dest) and os.path.getsize(dest) > 50000:
                continue
            p = prompt_panel(v0 + i, descs)
            if gen_panel(cap, n, i, ph, p, dest):
                hecho += 1
        # pasar a arte de panel por pantalla (sin página completa de fondo)
        if ns is None or scr["n"] in ns:
            scr.pop("bg_img", None)
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("  cap%02d: %d paneles nuevos" % (cap, hecho))
    return hecho

def tira(sel, nombre):
    import maquetador as mq
    mq.pdf_capitulo(1, False)          # refresca las pantallas de cap01
    frames = [Image.open(os.path.join(IMG, "cap01", "screens",
                                      "cap01_s%02d.jpg" % n)).convert("RGB").copy()
              for n in sel]
    W = frames[0].width
    H = sum(f.height for f in frames)
    t = Image.new("RGB", (W, H), (0, 0, 0))
    y = 0
    for f in frames:
        t.paste(f, (0, y)); y += f.height
    t.save(os.path.join(RAIZ, "pdf", nombre + ".png"))
    t.save(os.path.join(RAIZ, "pdf", nombre + ".jpg"), quality=92)
    print("  tira -> pdf/%s.png/.jpg (800x%d)" % (nombre, H))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "demo":
        panelizar(1, ns=[7, 8, 16])
        tira([7, 8, 16], "tira_v2_cap1")
    elif cmd == "cap":
        panelizar(int(sys.argv[2]))
    else:
        for c in range(1, 11):
            try:
                panelizar(c)
            except Exception as e:
                print("  cap%02d ERROR: %s" % (c, e))