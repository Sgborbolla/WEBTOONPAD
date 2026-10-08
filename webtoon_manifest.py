#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webtoon_manifest.py — genera img/capNN/manifest.json y el arte placeholder
para TODOS los capítulos (1-10). Maqueta estructural del volumen 1.

Dos fuentes:
  * cap01 / cap07 / cap08 / cap09 / cap10: guion detallado. Se leen las filas
    de "Mapa de pantallas" (geometría) + las TABLAS DE TEXTO (globos, cajas,
    SFX por viñeta). Las viñetas se asignan a cada pantalla de forma
    consecutiva (orden del guion, ya verificado: totales coinciden).
  * cap02 / cap03 / cap04 / cap05 / cap06: guion resumen (36 viñetas c/u).
    Se auto-maquetan en pantallas T3R/T2R con sus globos/cajas inline.

Uso:
  python3 webtoon_manifest.py cap 7          # sola capítulo
  python3 webtoon_manifest.py todo            # caps 1-10
"""
import json, os, re, sys, math
from PIL import Image, ImageDraw, ImageFont

RAIZ   = os.path.dirname(os.path.abspath(__file__))
IMG    = os.path.join(RAIZ, "img")
FONT   = "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
ANCHO  = 800
ALTO   = 1280
DETA   = {"01", "07", "08", "09", "10"}

RE_ROW   = re.compile(r"^\s*\|\s*(S\d+[A-Z]?)\s*\|\s*([^\|]+?)\s*\|\s*(\d+)\s*\|\s*([^\|]*?)\s*\|\s*([^\|]+?)\s*\|")
RE_TITLE = re.compile(r'^#\s*CAP.*?—\s*"([^"]+)"')
RE_TITLE2 = re.compile(r'^#\s*CAP\s+\d+\s*—\s*(.+?)\s*$')
RE_T6    = re.compile(r"^###\s+(S\d+[A-Z]?)\s*·\s*T6.*$")
RE_BLOQ  = re.compile(r'^>\s*\*[^*]+\*.*$')

POS = {
    "arriba-izquierda": "arriba-izq", "arriba-izq": "arriba-izq",
    "arriba-derecha": "arriba-dcha", "arriba-dcha": "arriba-dcha",
    "abajo-izquierda": "abajo-izq", "abajo-izq": "abajo-izq",
    "abajo-derecha": "abajo-dcha", "abajo-dcha": "abajo-dcha",
    "medio-derecha": "centro-dcha", "medio-izquierda": "centro-izq",
    "centro-derecha": "centro-dcha", "centro": "centro-dcha",
}
COLA = {
    "abajo-derecha": "abajo-dcha", "abajo-dcha": "abajo-dcha",
    "abajo-izquierda": "abajo-izq", "abajo-izq": "abajo-izq",
    "arriba-derecha": "arriba-dcha", "arriba-izquierda": "arriba-izq",
    "sale a la derecha": "sal-dcha", "derecha": "dcha",
    "izquierda": "izq", "centro-derecha": "dcha",
}

def limp(t):
    t = t.strip()
    if t.startswith("*") and t.endswith("*") and t.count("*") == 2:
        t = t[1:-1]
    return t.strip()

def num_viñeta(s):
    m = re.match(r"^[vV](\d+)(?:-V?(\d+))?$", s.strip().strip("`"))
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else None)

# ---------------------------------------------------------------- guion detallado

def filas_pantallas(texto):
    """Filas | S.. | de todos los mapas, en orden, sin repetidos."""
    seen, filas = set(), []
    for ln in texto.splitlines():
        m = RE_ROW.match(ln)
        if not m:
            continue
        k = m.group(1)
        if k in seen:
            continue
        seen.add(k)
        filas.append((k, m.group(2).strip(), int(m.group(3)),
                      m.group(4).strip(), m.group(5).strip()))
    return filas

def geometria(tipo, hstr, gstr):
    """-> (paneles:[...], gaps:[...]) o None si es T6."""
    if tipo.upper().startswith("T6"):
        return [], [0]
    h = [int(x) for x in hstr.split("/") if x.strip().isdigit()]
    g = [int(x) for x in re.sub(r"[—\-].*$", "", gstr).replace(" ", "").split("/")
         if x.strip().isdigit()]
    # si no hay gaps pero hay paneles, rellenar con 0
    if h and not g:
        g = [0] * (len(h) + 1)
    return h, g

def tablas_texto(texto):
    """Extrae globos/cajas/sfx en tablas: detecta cabeceras y filas '| V.. |'."""
    globos, cajas, sfx, rotulos = [], [], [], []
    for cab in re.finditer(
            r"^#{2,4}\s+(Globos(?: de [^\n]+)?|Cajas de narración[^\n]*|SFX[^\n]*)",
            texto, re.M):
        fin = texto.find("\n#", cab.end())
        seg = texto[cab.end(): fin if fin > 0 else len(texto)]
        head = cab.group(1)
        for ln in seg.splitlines():
            if not ln.strip().startswith("|"):
                continue
            celdas = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(celdas) < 2:
                continue
            if not (celdas[0] == "Viñeta" or re.match(r"^[vVr]", celdas[0])):
                continue
            v = celdas[0]
            if v == "Viñeta":
                continue
            if re.match(r"^[Rr]ó?tulo S", v):
                m = re.search(r"(S\d+)", v)
                if m:
                    rotulos.append((m.group(1), " ".join(celdas[1:])))
                continue
            r = num_viñeta(v)
            if not r:
                continue
            fue = r[1] if r[1] is not None else r[0]
            rango = range(r[0], fue + 1)
            if head.startswith("Globos"):
                quien = celdas[1] if len(celdas) > 1 else ""
                if len(celdas) >= 5 and celdas[2] in POS:
                    pos, cola, txt = celdas[2], celdas[3], celdas[4]
                else:
                    txt = celdas[-1]
                    pos, cola = "abajo-izq", "abajo-dcha"
                for vv in rango:
                    globos.append((vv, quien, POS.get(pos, "abajo-izq"),
                                   COLA.get(cola, "abajo-dcha"), limp(txt)))
            elif head.startswith("Cajas"):
                txt = " ".join(celdas[1:]).strip()
                for vv in rango:
                    cajas.append((vv, limp(txt)))
            elif head.startswith("SFX"):
                txt = celdas[1] if len(celdas) > 1 else ""
                for vv in rango:
                    sfx.append((vv, limp(txt)))
    return globos, cajas, sfx, rotulos

def texto_rotulos_detallado(texto):
    """Texto de los rótulos T6 desde sus bloques (la línea '> *...*')."""
    out = {}
    cur = None
    for ln in texto.splitlines():
        head = re.match(r"^###\s+S\d+[A-Z]?\s*·", ln.strip())
        if head:
            cur = None
            m = RE_T6.match(ln)
            if m:
                cur = m.group(1)
            continue
        if cur is None or cur in out:
            continue
        if ln.strip().startswith(">"):
            t = ln.strip()[1:].strip()
            t = re.sub(r"^\*{1,2}[A-Z][^:]*:\*+\s*", "", t)
            if t.startswith("*") and t.endswith("*"):
                out[cur] = t[1:-1].strip()
    return out

def registrar_rotulos(man, rotulos, textos):
    for s, t in rotulos:
        for scr in man["screens"]:
            if str(scr["n"]) == s:
                scr["narracion"] = {"texto": t.replace(" / ", "\n"),
                                    "centro": True, "y": 480, "w": 700,
                                    "pt": 38, "negro": True, "sin_caja": True}
    for s, t in textos.items():
        for scr in man["screens"]:
            if str(scr["n"]) == s and not scr.get("narracion"):
                scr["narracion"] = {"texto": t.replace(" / ", "\n"),
                                    "centro": True, "y": 480, "w": 700,
                                    "pt": 38, "negro": True, "sin_caja": True}

def asignar_viñetas(filas):
    """-> {viñeta:int -> (screen_n, panel_0based)} y total."""
    mapa, cur = {}, 1
    for (k, tipo, npan, hstr, gstr) in filas:
        pan, _ = geometria(tipo, hstr, gstr)
        for i in range(len(pan)):
            mapa[cur] = (re.match(r"S(\d+)", k).group(1), i)
            cur += 1
    return mapa, cur - 1

def manifest_detallado(cap, texto, titulo):
    filas = filas_pantallas(texto)
    mapa_v, total = asignar_viñetas(filas)
    globos, cajas, sfx, rotulos = tablas_texto(texto)
    rot_txt = texto_rotulos_detallado(texto)
    screens, dialogos = [], []
    vini = 1
    for (k, tipo, npan, hstr, gstr) in filas:
        pan, gap = geometria(tipo, hstr, gstr)
        bg = "blanco"
        if tipo.upper().startswith("T6"):
            if "gris" in gstr:
                bg = "gris pasado"
            else:
                bg = "negro de corte"
        n = int(re.match(r"S(\d+)", k).group(1))
        scr = {"n": n, "paneles": pan, "gaps": gap, "bg": bg,
               "vinheta_inicio": vini}
        vini += len(pan)
        if not pan:
            scr["marco_pantalla"] = True
        screens.append(scr)
    # re-anclar diálogos
    g_by_v_panel = {vv: (pan, i) for vv, (pan, i) in mapa_v.items()}
    dial_by_panel = {}
    for (vv, quien, pos, cola, txt) in globos:
        pan, i = g_by_v_panel[vv]
        key = (pan, i)
        dial_by_panel.setdefault(key, []).append(
            {"texto": txt, "globo": pos, "cola": cola})
    caj_by_panel, sfx_by_panel = {}, {}
    for (vv, txt) in cajas:
        pan, i = g_by_v_panel[vv]
        caj_by_panel.setdefault((pan, i), []).append(txt)
    for (vv, txt) in sfx:
        pan, i = g_by_v_panel[vv]
        sfx_by_panel.setdefault((pan, i), []).append(txt)
    for scr in screens:
        n = scr["n"]
        if scr["paneles"]:
            v0 = scr["vinheta_inicio"]
            for i in range(len(scr["paneles"])):
                vv = v0 + i
                if vv in g_by_v_panel:
                    pass
        # dialogos del panel
        c = scr.get("n")
        # agrupar por pantalla: panel index -> lista
        pans_cajas, pans_sfx = [], []
        for (pant, pi), arr in dial_by_panel.items():
            if pant == str(scr["n"]):
                for d in arr:
                    dialogos.append({"pantalla": int(pant), "panel": pi + 1,
                                     "quien": "", **d})
        for (pant, pi), arr in caj_by_panel.items():
            if pant == str(scr["n"]):
                pans_cajas.append({"panel": pi + 1, "texto": "\n".join(arr)})
        for (pant, pi), arr in sfx_by_panel.items():
            if pant == str(scr["n"]):
                pans_sfx.append({"panel": pi + 1, "texto": "\n".join(arr)})
        if pans_cajas:
            scr["cajas"] = pans_cajas
        if pans_sfx:
            scr["sfx"] = pans_sfx
    registrar_rotulos({"screens": screens}, rotulos, rot_txt)
    return {
        "cap": int(cap),
        "titulo": titulo,
        "pantallas": len(screens),
        "viñetas": total,
        "ancho": ANCHO,
        "alto": ALTO,
        "screens": screens,
        "dialogos": dialogos,
    }

# ---------------------------------------------------------------- guion resumen

def bloques_resumen(texto):
    """Viñetas del resumen -> [(num, desc, [(tipo, texto)])]."""
    out, cur = [], None
    for ln in texto.splitlines():
        m = re.match(r"^\*\*(\d+)\.\*\*(.*)$", ln.strip())
        if m:
            cur = [int(m.group(1)), m.group(2).strip(), []]
            out.append(cur)
            continue
        if cur:
            mm = re.match(r"^>\s*\*\*([^:\*]+):\*\*\s*(.+?)\s*$", ln.strip())
            if mm:
                kind = mm.group(1).strip()
                t = mm.group(2).strip().strip("`").strip()
                lk = kind.lower()
                if "caja" in lk:
                    cur[2].append(("caja", t))
                elif lk in ("sfx", "sonido", "sonido descrito"):
                    cur[2].append(("sfx", t))
                else:
                    cur[2].append(("globo", t))
    return out

def manifiesto_resumen(cap, texto, titulo):
    vts = bloques_resumen(texto)
    total = max((v[0] for v in vts), default=0)
    screens, dialogos = [], []
    # agrupar de 2 en 2 (T3R) y el último solo (T2R)
    idx = 0
    while idx < total:
        a = vts[idx]
        b = vts[idx + 1] if idx + 1 < total else None
        n = len(screens) + 1
        if b:
            pan, g3 = [570, 570], [40, 60, 40]
            pares = (a, b)
        else:
            pan, g3 = [1200], [40, 40]
            pares = (a,)
        scr = {"n": n, "paneles": pan, "gaps": g3, "bg": "blanco",
               "vinheta_inicio": a[0]}
        cajas, sfx = [], []
        for j, v in enumerate(pares):
            for kind, t in v[2]:
                if kind == "caja":
                    cajas.append({"panel": j + 1, "texto": t})
                elif kind == "sfx":
                    sfx.append({"panel": j + 1, "texto": t})
                elif kind == "globo":
                    dialogos.append({"pantalla": n, "panel": j + 1,
                                     "quien": "", "texto": t,
                                     "globo": "arriba-izq", "cola": "abajo-dcha"})
        if cajas:
            scr["cajas"] = cajas
        if sfx:
            scr["sfx"] = sfx
        screens.append(scr)
        idx += len(pares)
    return {"cap": int(cap), "titulo": titulo, "pantallas": len(screens),
            "viñetas": total, "ancho": ANCHO, "alto": ALTO,
            "screens": screens, "dialogos": dialogos}

# ---------------------------------------------------------------- arte placeholder

_font_cache = {}
def fuente(pt):
    if pt not in _font_cache:
        _font_cache[pt] = ImageFont.truetype(FONT, int(pt * 3))
    return _font_cache[pt]

def paleta(cap):
    base = [(70, 84, 110), (90, 80, 60), (74, 96, 84), (96, 74, 88),
            (88, 80, 96), (78, 92, 60), (100, 76, 70), (66, 88, 104),
            (92, 92, 78), (80, 82, 100)][(cap - 1) % 10]
    return base

def placeholder(cp, viñ, h, dest):
    """Panel 800×h tono claro con su número de viñeta."""
    b = paleta(cp)
    img = Image.new("RGB", (ANCHO, h))
    px = img.load()
    dd = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h)
        f = 0.92 + 0.16 * t
        dd.line([(0, y), (ANCHO, y)],
                (min(255, int(b[0] * f)), min(255, int(b[1] * f)),
                 min(255, int(b[2] * f))))
    txt = str(viñ)
    font = fuente(54)
    tw = dd.textlength(txt, font=font)
    dd.text(((ANCHO - tw) / 2, h // 2 - 60), txt, font=font,
            fill=(255, 255, 255, 255))
    dd.text(((ANCHO - tw) / 2 + 4, h // 2 - 60 + 4), txt, font=font,
            fill=(0, 0, 0, 60))
    img.save(dest)
    return dest

# ---------------------------------------------------------------- orquestación

def titulo_cap(cap):
    s = open(os.path.join(RAIZ, "Guiones", "cap%02d.md" % cap), encoding="utf-8").read()
    primera = s.strip().splitlines()[0]
    m = RE_TITLE.search(primera)
    if m:
        return m.group(1).strip()
    m = RE_TITLE2.match(primera)
    return m.group(1).strip() if m else "Capítulo %d" % cap

def generar(cap):
    ruta = os.path.join(RAIZ, "Guiones", "cap%02d.md" % cap)
    texto = open(ruta, encoding="utf-8").read()
    titulo = titulo_cap(cap)
    if "%02d" % cap in DETA:
        texto = re.sub(r"# LOS TEXTO", "# LOS TEXTOS", texto)
        man = manifest_detallado("%02d" % cap, texto, titulo)
        # limpiar narración fantasma de portada cap01
    else:
        man = manifiesto_resumen(cap, texto, titulo)
    carpeta = os.path.join(IMG, "cap%02d" % cap)
    os.makedirs(carpeta, exist_ok=True)
    json.dump(man, open(os.path.join(carpeta, "manifest.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    # arte placeholder: por pantalla -> sNN_pX.png
    n = 0
    for scr in man["screens"]:
        v0 = scr.get("vinheta_inicio", 1)
        for i, h in enumerate(scr["paneles"]):
            dest = os.path.join(carpeta, "s%02d_p%d.png" % (scr["n"], i + 1))
            placeholder(cap, v0 + i, h, dest)
            n += 1
    print("  cap%02d '%s': %d pantallas · %d viñetas -> manifest + %d placeholders"
          % (cap, titulo, man["pantallas"], man["viñetas"], n))
    return man

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cap":
        generar(int(sys.argv[2]))
    else:
        for i in range(1, 11):
            try:
                generar(i)
            except Exception as e:
                import traceback
                print("  cap%02d ERROR: %s" % (i, e)); traceback.print_exc()