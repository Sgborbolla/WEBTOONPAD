#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
art_multi.py — generador de arte multi-backend gratuito y scriptable.

Orden de uso:
  1. AI Horde (stablehorde.net) — red GPUs gratuita, API sin cuenta, modelos
     anime/webtoon de la comunidad.
  2. Pollinations (respaldo) — ya usado; inestable (HTTP 402), sin cuenta.

Uso:
  python3 art_multi.py s08p1 "prompt..."   # genera y guarda en pdf/prueba_horde.png
"""
import base64, io, json, os, sys, time, urllib.request, urllib.parse

HORDE = "https://stablehorde.net/api/v2"

MODELOS_PREFERIDOS = ["Hassaku XL", "Anything v3", "Anything Diffusion",
                      "Anything v5", "Deliberate", "Deliberate 3.0",
                      "Counterfeit", "Dreamshaper", "MeinaMix"]

_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(_dir, "api_keys.json")) as _f:
        APIKEY = (json.load(_f).get("horde") or "")
except Exception:
    APIKEY = ""
if not APIKEY:
    APIKEY = "0000000000000000"

def http_json(url, metodo="GET", datos=None):
    h = {"Content-Type": "application/json",
         "apikey": APIKEY, "User-Agent": "npad-art-multi/1.0"}
    req = urllib.request.Request(url, json.dumps(datos).encode() if datos is not None else None,
                                 headers=h, method=metodo)
    with urllib.request.urlopen(req, timeout=100) as r:
        return json.loads(r.read().decode())

def modelos_disponibles():
    try:
        lista = http_json(HORDE + "/status/models")
        return [(m.get("name"), int(m.get("count", 0) or 0)) for m in lista]
    except Exception as e:
        return []

MALOS = ("nsfw", "hentai", "porn", "pony", "yiff", "clop", "inpainting", "grapefruit", "lustify")

def elegir_modelo(modelos):
    disp = {a for a, _ in modelos}
    for m in MODELOS_PREFERIDOS:
        if m in disp:
            return m
    return (modelos[0][0] if modelos else "Deliberate")

def mult64(x):
    return int(x) - (int(x) % 64)

def gen_horde(prompt, w=800, h=1200, modelo=None, max_wait=2700):
    modelos = modelos_disponibles()
    if modelo is None:
        modelo = elegir_modelo(modelos)
    cuerpo = {
        "prompt": prompt,
        "params": {"width": mult64(w), "height": mult64(h), "steps": 24,
                   "cfg_scale": 7, "sampler_name": "k_euler_a",
                   "karras": True, "n": 1},
        "nsfw": False, "r2": True, "shared": False, "models": [modelo],
    }
    candidatos = [x for x in MODELOS_PREFERIDOS
                  if x in [a for a, _ in modelos]]
    if not candidatos:
        candidatos = [a for a, c in modelos
                      if not any(b in str(a).lower() for b in MALOS)][:6]
    # reintentamos con otros modelos si da error
    for m in [modelo] + [x for x in candidatos if x != modelo][:6]:
        cuerpo["models"] = [m]
        try:
            rid = http_json(HORDE + "/generate/async", "POST", cuerpo)["id"]
            t = 0
            while t < max_wait:
                time.sleep(12); t += 12
                chk = http_json(HORDE + "/generate/check/" + rid)
                if chk.get("done"):
                    st = http_json(HORDE + "/generate/status/" + rid)
                    gens = st.get("generations") or []
                    if gens and gens[0].get("img"):
                        img = gens[0]["img"]
                        if img.startswith("http"):
                            req = urllib.request.Request(img, headers={"User-Agent": "npad"})
                            data = urllib.request.urlopen(req, timeout=120).read()
                        else:
                            img += "=" * (-len(img) % 4)
                            data = base64.b64decode(img)
                        seed = gens[0].get("seed")
                        return data, seed, m
                    return None, None, m
            return None, None, m
        except Exception as e:
            print("  horde %s: %s; pruebo otro modelo" % (m, e))
    return None, None, modelo

def gen_pollinations(prompt, w=800, h=1200):
    url = ("https://image.pollinations.ai/prompt/" +
           urllib.parse.quote(prompt) +
           f"?width={w}&height={h}&nologo=true&model=flux&seed={int(time.time())%100000}")
    req = urllib.request.Request(url, headers={"User-Agent": "npad"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def horde_dims(w, h, box=768):
    # cuadro maximo permitido sin kudos extra: ambos lados <= box
    ar = w / float(h)
    if ar >= 1:
        nw, nh = box, max(64, mult64(box / ar))
    else:
        nw, nh = max(64, mult64(box * ar)), box
    return nw, nh

def generar(prompt, w=800, h=1200, backend=None):
    if backend != "pollinations":
        hw, hh = horde_dims(w, h)
        data, seed, m = gen_horde(prompt, hw, hh)
        if data:
            print("  [horde] modelo=%s seed=%s (%dx%d)" % (m, seed, hw, hh))
            return data
    print("  [pollinations]")
    return gen_pollinations(prompt, w, h)

def cargar(data):
    try:
        from PIL import Image
    except ImportError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
        from PIL import Image
    return io.BytesIO(data), Image

def recortar_a(image, w, h):
    # crop al aspect ratio objetivo (centrado) y redimensiona
    ar_t = w / float(h)
    iw, ih = image.size
    ar_i = iw / float(ih)
    if ar_i > ar_t:
        nw = int(ih * ar_t)
        x = (iw - nw) // 2
        image = image.crop((x, 0, x + nw, ih))
    elif ar_i < ar_t:
        nh = int(iw / ar_t)
        y = (ih - nh) // 2
        image = image.crop((0, y, iw, y + nh))
    return image.resize((w, h), 5)

if __name__ == "__main__":
    prompt = sys.argv[1]
    w, h = int(sys.argv[2]), int(sys.argv[3])
    data = generar(prompt, w, h)
    buf, Image = cargar(data)
    img = Image.open(buf).convert("RGB")
    img = recortar_a(img, w, h)
    img.save("pdf/prueba_horde.png")
    print("guardado pdf/prueba_horde.png", w, "x", h)