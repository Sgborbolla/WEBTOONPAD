#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webtoon_arte.py — genera una imagen de página 9:16 por pantalla (864x1536) para
los 10 capítulos y la monta en img/capNN/ como bg_img de la pantalla.

Estilo homogéneo (manhwa/webtoon coreano, cisura, mundo de NPAD). El prompt de
cada página se construye desde la descripción de la primer viñeta del guion.
Sin texto/letras/marca: los globos, cajas, SFX y rótulos los pone maquetador.py.

Uso:
  python3 webtoon_arte.py prueba            # 3 páginas de cap01 para validar
  python3 webtoon_arte.py cap 1            # completa el arte que falta de cap01
  python3 webtoon_arte.py todo             # caps 1-10 (reanuda donde faltan)
"""
import json, os, re, sys, time, urllib.request, urllib.parse
from io import BytesIO
from PIL import Image
import webtoon_estilo as est

RAIZ = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(RAIZ, "img")
W, H = 864, 1536

def desc_viñetas(cap):
    """{viñeta:int -> descripcion} desde el guion (detalado o resumen)."""
    s = open(os.path.join(RAIZ, "Guiones", "cap%02d.txt" % cap), encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^\*\*[Vv]?(\d+)\.\*\*\s*(.+)$", s, re.M):
        n = int(m.group(1))
        txt = re.sub(r"\s+", " ", m.group(2)).strip()
        txt = re.sub(r"\*\*(.+?)\*\*", r"\1", txt)
        txt = txt.strip(" .")[:500]
        if txt:
            out[n] = txt
    return out

def prompt_pantalla(cap, vinheta_inicio, descs):
    d = descs.get(vinheta_inicio, "")
    if not d:
        for k in range(vinheta_inicio, vinheta_inicio + 3):
            if k in descs:
                d = descs[k]; break
    partes = []
    if d:
        partes.append(d.capitalize()[:380])
    fichas = est.desc_personajes(d or "")
    if fichas:
        for f in fichas:
            partes.append(f)
    else:
        partes.append(est.ESCENA_VACIA)
    partes.append(est.estilo())
    partes.append(est.DESC_KI)
    return ". ".join(p for p in partes if p)

def pedir(url):
    timeout = 90
    req = urllib.request.Request(url, headers={"User-Agent": "npad-webtoon-builder"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def generar_pagina(cap, n, prompt, dest):
    for intento in range(5):
        seed = n * 1000 + cap * 7 + intento * 131
        url = ("https://image.pollinations.ai/prompt/" +
               urllib.parse.quote(prompt) +
               f"?width={W}&height={H}&nologo=true&model=flux&seed={seed}")
        try:
            data = pedir(url)
            if len(data) < 5000:
                print(f"    s{n:02d}: descarga corta ({len(data)}b), reintento")
                time.sleep(8); continue
            img = Image.open(BytesIO(data))
            est.grade(img).save(dest)
            print(f"    s{n:02d}: ok ({len(data)//1024}KB, seed {seed})")
            return True
        except Exception as e:
            print(f"    s{n:02d}: error {type(e).__name__} {e}; reintento {intento+1}")
            time.sleep(12 + intento * 10)
    return False

def montar(cap, n, dest):
    m = json.load(open(os.path.join(IMG, "cap%02d" % cap, "manifest.json"),
                       encoding="utf-8"))
    for scr in m["screens"]:
        if scr["n"] == n:
            scr["bg_img"] = os.path.basename(dest)
            for p in range(len(scr["paneles"])):
                f = os.path.join(IMG, "cap%02d" % cap, "s%02d_p%d.png" % (n, p + 1))
                if os.path.exists(f):
                    os.remove(f)
            break
    json.dump(m, open(os.path.join(IMG, "cap%02d" % cap, "manifest.json"), "w",
                      encoding="utf-8"), ensure_ascii=False, indent=1)

def procesar_cap(cap, limite=None):
    dirs = os.path.join(IMG, "cap%02d" % cap)
    m = json.load(open(os.path.join(dirs, "manifest.json"), encoding="utf-8"))
    descs = desc_viñetas(cap)
    hecho = 0
    for scr in m["screens"]:
        if limite and hecho >= limite:
            break
        n = scr["n"]
        dest = os.path.join(dirs, "pag_s%02d.png" % n)
        if scr.get("bg_img") or os.path.exists(dest):
            continue                      # ya montada / referencia / pendiente
        p = prompt_pantalla(cap, scr.get("vinheta_inicio", 1), descs)
        if generar_pagina(cap, n, p, dest):
            montar(cap, n, dest)
            hecho += 1
    print("  cap%02d: %d páginas nuevas" % (cap, hecho))
    return hecho

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prueba"
    if cmd == "prueba":
        procesar_cap(2) if False else procesar_cap(1, limite=3)
    elif cmd == "cap":
        procesar_cap(int(sys.argv[2]))
    else:
        for i in range(1, 11):
            try:
                procesar_cap(i)
            except Exception as e:
                print("  cap%02d ERROR: %s" % (i, e))