#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_horde.py — genera por lotes (en segundo plano) el arte faltante de cap01
usando AI Horde + Hassaku XL, escena-por-escena, reanudable.

Se salta: pantallas 1-5 (arte del usuario) y paneles ya generados (>50KB).
Cada panel se encola y espera; un job a la vez para no saturar kudos.

Cancela: tocar un archivo pdf/.stop_batch
"""
import json, os, sys, time, urllib.request, urllib.error, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art_multi as A
import webtoon_v2 as v2
import webtoon_estilo as est
from PIL import Image
from io import BytesIO

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(RAIZ, "img")
STOP = os.path.join(RAIZ, "pdf", ".stop_batch")
DIRS = os.path.join(IMG, "cap01")
MP = os.path.join(DIRS, "manifest.json")

def descs():
    return v2.desc_viñetas(1)

def paneles_pendientes(ns, force=False):
    m = json.load(open(MP, encoding="utf-8"))
    pend = []
    for scr in m["screens"]:
        if scr["n"] < 6:
            continue
        if ns is not None and scr["n"] not in ns:
            continue
        v0 = scr.get("vinheta_inicio", 1)
        for i, ph in enumerate(scr["paneles"]):
            d = os.path.join(DIRS, "s%02d_p%d.png" % (scr["n"], i + 1))
            if not force and os.path.exists(d) and os.path.getsize(d) > 50000:
                continue
            pend.append((scr["n"], i + 1, ph, v0 + i))
    return pend

def gen_y_guarda(n, i, ph, vnum):
    p = v2.prompt_panel(vnum, descs())
    hw, hh = A.horde_dims(800, ph)
    data = None
    from horde_cli import gen, status, download
    r = gen(p, hw, hh)
    if r["status"] != "ok":
        print("  s%02dp%02d submit ERR %s" % (n, i, r["status"]))
        return False
    rid = r["body"]["id"]
    t = 0
    while t < 2400:
        if os.path.exists(STOP):
            print("  STOP detectado (s%02d p%d)" % (n, i)); return False
        time.sleep(20); t += 20
        s = status(rid)
        if not s.get("body"):
            continue
        b = s["body"]
        if b.get("faulted"):
            print("  s%02dp%02d faulted: %s" % (n, i, b.get("errors"))); return False
        if b.get("done"):
            g = (b.get("generations") or [{}])[0]
            img = g.get("img")
            if not img:
                print("  s%02dp%02d sin imagen" % (n, i))
                return False
            data = download(img) if img.startswith("http") else base64.b64decode(img + "=" * (-len(img) % 4))
            break
    if data is None:
        print("  s%02dp%02d timeout" % (n, i)); return False
    im = Image.open(BytesIO(data)).convert("RGB")
    im = A.recortar_a(im, 800, ph)
    est.grade(im).save(os.path.join(DIRS, "s%02d_p%d.png" % (n, i)))
    print("  s%02dp%02d OK" % (n, i), flush=True)
    return True

if __name__ == "__main__":
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]
    ns = None
    if args and args[0] != "all":
        ns = [int(x) for x in args[0].split(",")]
    pend = paneles_pendientes(ns, force)
    print("%d paneles pendientes" % len(pend), flush=True)
    ok = 0
    for (n, i, ph, vnum) in pend:
        if os.path.exists(STOP):
            print("PARADO por .stop_batch"); break
        try:
            if gen_y_guarda(n, i, ph, vnum):
                ok += 1
        except Exception as e:
            print("  s%02dp%02d EXC: %s" % (n, i, e), flush=True)
    print("batch: %d/%d ok" % (ok, len(pend)), flush=True)