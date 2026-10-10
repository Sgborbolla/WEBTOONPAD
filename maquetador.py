#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maquetador.py — monta las pantallas del webtoon con Pillow (sin ImageMagick).

Lee img/capNN/manifest.json (geometria + dialogo del capNN.txt) y las viñetas
img/capNN/sNN_pX.png, y produce las pantallas 800x1280 (con gutter, marcos,
cajas de narración y GLOBOS de diálogo automáticos) y el PDF del capítulo.

Uso:
  python3 maquetador.py cap 1
  python3 maquetador.py cap 1 --pdf
  python3 maquetador.py todo
"""
import json, os, re, sys, glob
from PIL import Image, ImageDraw, ImageFont

ANCHO   = 800
ALTO    = 1280
MARCO   = 2
RAIZ    = os.path.dirname(os.path.abspath(__file__))
IMG     = os.path.join(RAIZ, "img")
SALIDA  = os.path.join(RAIZ, "pdf")
FONTS = ["/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
         "/system/fonts/DroidSans-Bold.ttf",
         "/system/fonts/Roboto-Regular.ttf"]
FONT_OK = next((f for f in FONTS if os.path.exists(f)), FONTS[0])
FONDO   = {"blanco": (255, 255, 255), "gris pasado": (42, 42, 46),
           "negro de corte": (0, 0, 0)}

_font_cache = {}
def fuente(pt):
    if pt not in _font_cache:
        _font_cache[pt] = ImageFont.truetype(FONT_OK, int(pt * 3))
    return _font_cache[pt]

def texto_centrado(draw, cx, y, linea, font, relleno, ancho=None,
                   stroke=0, stroke_fill=(0, 0, 0, 255)):
    """Dibuja una línea centrada en cx (o dentro de ancho)."""
    lw = draw.textlength(linea, font=font)
    x = cx - lw / 2 if ancho is None else cx + (ancho - lw) / 2
    if stroke:
        draw.text((x, y), linea, font=font, fill=relleno,
                  stroke_width=stroke, stroke_fill=stroke_fill)
    else:
        draw.text((x, y), linea, font=font, fill=relleno)

def validar(m):
    if not m["paneles"]:
        return
    total = sum(m["paneles"]) + sum(m["gaps"])
    if total != ALTO:
        raise ValueError("geometria invalida: %d != %d" % (total, ALTO))

def buscar_png(carpeta, num, panel=None):
    if panel is None:
        p = os.path.join(carpeta, "s%02d.png" % num)
        if os.path.exists(p):
            return p
        c = sorted(glob.glob(os.path.join(carpeta, "s%02d_p*.png" % num)))
        return c if len(c) > 1 else (c[0] if c else None)
    p = os.path.join(carpeta, "s%02d_p%d.png" % (num, panel + 1))
    return p if os.path.exists(p) else None

def resize_rellenar(img, w, h):
    img = img.convert("RGB")
    ar   = img.width / img.height
    tar  = w / h
    if ar > tar:
        nw = int(img.height * tar); x = (img.width - nw) // 2
        img = img.crop((x, 0, x + nw, img.height))
    else:
        nh = int(img.width / tar); y = (img.height - nh) // 2
        img = img.crop((0, y, img.width, y + nh))
    return img.resize((w, h), Image.LANCZOS)

def resize_contener(img, w, h, color=(0, 0, 0)):
    """Encaja la imagen ENTERA dentro de w×h sin recortar (barras)."""
    img = img.convert("RGB")
    ar  = img.width / img.height
    tar = w / h
    if ar > tar:
        nw = w; nh = int(w / ar)
    else:
        nh = h; nw = int(h * ar)
    small = img.resize((nw, nh), Image.LANCZOS)
    base = Image.new("RGB", (w, h), color)
    base.paste(small, ((w - nw) // 2, (h - nh) // 2))
    return base

def medir(texto, font, draw, ancho_max):
    lineas = []
    for frag in texto.split("\n"):
        cur = ""
        for pal in frag.split(" "):
            prueba = (cur + " " + pal).strip()
            if draw.textlength(prueba, font=font) <= ancho_max:
                cur = prueba
            else:
                if cur: lineas.append(cur)
                cur = pal
        if cur: lineas.append(cur)
    return lineas

INSET = 16
BOL_TAM = 13
BOL_MAX = 400
def caja_texto(draw, texto, font, pt, ancho_max):
    lineas = medir(texto, font, draw, ancho_max)
    alto = int(len(lineas) * pt * 1.3) + INSET
    return lineas, alto

def dibujar_narracion(base, m):
    nar = m.get("narracion")
    if not nar:
        return
    draw = ImageDraw.Draw(base, "RGBA")
    pt   = int(nar.get("pt", 26))
    font = fuente(pt)
    lineas, alto = caja_texto(draw, nar["texto"], font, pt, nar.get("w", ANCHO - 160))
    fondo = nar.get("fondo", "#ffffffcc")
    alpha = int(fondo[-2:], 16) if len(fondo) == 9 else 220
    rgb   = (255, 255, 255) if alpha else (0, 0, 0)
    if len(fondo) == 7:
        rgb = tuple(int(fondo[i:i + 2], 16) for i in (1, 3, 5))
    x = nar.get("x", 40); y = nar.get("y", 40)
    grosor = 3
    if nar.get("centro"):
        x = (ANCHO - nar.get("w", 700)) // 2
    if nar.get("h"):
        alto = nar["h"]
    tinta = (17, 17, 17, 255) if not nar.get("negro") else (255, 255, 255, 255)
    if not nar.get("sin_caja"):
        bbox = [x, y, x + nar.get("w", 470), y + alto]
        draw.rectangle(bbox, fill=rgb + (alpha,), outline=(0, 0, 0, 255), width=grosor)
        ty = y + 14
        for line in lineas:
            draw.text((x + 14, ty), line, font=font, fill=tinta)
            ty += int(pt * 1.35)
    else:
        # rótulo de corte: texto limpio, sin caja, centrado
        yt = y if y else 480
        ty = yt + 14
        for line in lineas:
            lw = draw.textlength(line, font=font)
            draw.text(((ANCHO - lw) / 2, ty), line, font=font, fill=tinta)
            ty += int(pt * 1.4)
    del draw

def dibujar_caja(base, rect, texto, usado=None):
    """Caja de narración anclada al pie del panel (sin cola)."""
    draw = ImageDraw.Draw(base, "RGBA")
    pt = 10
    font = fuente(pt)
    lineas, alto = caja_texto(draw, texto, font, pt, ANCHO - 52)
    alto += 14
    rect2 = [14, rect[1] + rect[3] - alto - 10, ANCHO - 14, rect[1] + rect[3] - 10]
    if rect2[1] < rect[1] + 6:
        rect2[1] = rect[1] + 6; rect2[3] = rect[1] + 6 + alto
    if usado:
        for r in usado:
            if not (rect2[2] < r[0] or rect2[0] > r[2] or rect2[3] < r[1] or rect2[1] > r[3]):
                rect2[1] -= alto + 10
                rect2[3] -= alto + 10
        usado.append(list(rect2))
    draw.rectangle(rect2, fill=(255, 255, 255, 235), outline=(0, 0, 0, 255), width=2)
    ty = rect2[1] + 8
    for line in lineas:
        draw.text((rect2[0] + 10, ty), line, font=font, fill=(15, 15, 15, 255))
        ty += int(pt * 1.3)
    del draw

def dibujar_sfx(base, rect, texto):
    """Marca sonora dibujada dentro del panel, grande y algo inclinada."""
    palabras = texto.split()
    linea = " ".join(palabras[:3])
    if len(palabras) > 3:
        linea += "…"
    pt = 34
    font = fuente(pt)
    capa = Image.new("RGBA", (ANCHO, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    lw = d.textlength(linea, font=font)
    d.text(((ANCHO - lw) / 2, 30), linea, font=font, fill=(60, 20, 20, 230))
    capa = capa.rotate(6, resample=Image.BICUBIC, expand=False)
    base.paste(capa, (0, rect[1] + 12), capa)
    del d, capa

def pos_globo(tag, pr):
    m = 12
    if tag == "arriba-izq":   return (pr[0] + m, pr[1] + m)
    if tag == "arriba-dcha":  return (pr[2] - BOL_MAX - m, pr[1] + m)
    if tag == "abajo-izq":    return (pr[0] + m, pr[3] - m)
    if tag == "abajo-dcha":   return (pr[2] - BOL_MAX - m, pr[3] - m)
    if tag == "centro-dcha":  return (pr[2] - BOL_MAX - m, (pr[1] + pr[3]) // 2)
    if tag == "centro-izq":   return (pr[0] + m, (pr[1] + pr[3]) // 2)
    return (pr[0] + m, pr[1] + m)

def punto_cola(tag, pr):
    cx = (pr[0] + pr[2]) // 2; cy = (pr[1] + pr[3]) // 2
    if tag == "abajo-dcha":   return (cx + 60, pr[3] - 10)
    if tag == "abajo-izq":    return (cx - 60, pr[3] - 10)
    if tag == "arriba-dcha":  return (cx + 60, pr[1] + 10)
    if tag == "arriba-izq":   return (cx - 60, pr[1] + 10)
    if tag == "izq":          return (pr[0] + 10, cy)
    if tag == "dcha":         return (pr[2] - 10, cy)
    if tag == "sal-dcha":     return (pr[2] + 20, cy)
    if tag == "sal-izq":      return (pr[0] - 20, cy)
    return (cx, pr[3] - 10)

def dibujar_globo(base, panel_rect, texto, globo, cola, usado):
    draw = ImageDraw.Draw(base, "RGBA")
    pt   = BOL_TAM
    font = fuente(pt)
    px, py = pos_globo(globo, panel_rect)
    bw = BOL_MAX
    lineas, alto = caja_texto(draw, texto, font, pt, bw - INSET * 2)
    alto = max(alto, int(pt * 1.8))
    rect = [px, py, px + bw, py + alto]
    # mover hacia abajo si choca con otro globo de la misma pantalla/panel
    for r in usado:
        if not (rect[2] < r[0] or rect[0] > r[2] or rect[3] < r[1] or rect[1] > r[3]):
            dy = r[3] - rect[1] + 10
            rect[1] += dy; rect[3] += dy
    # no salirse de la pantalla
    if rect[2] > ANCHO - 4: rect[0] -= rect[2] - (ANCHO - 4); rect[2] = ANCHO - 4
    if rect[1] < 4: rect[3] += 4 - rect[1]; rect[1] = 4
    if rect[3] > ALTO - 4: rect[1] -= rect[3] - (ALTO - 4); rect[3] = ALTO - 4
    draw.rounded_rectangle(rect, radius=18, fill=(255, 255, 255, 235),
                           outline=(0, 0, 0, 255), width=3)
    # cola
    tp = punto_cola(cola, panel_rect)
    # ancla de la cola en el borde mas cercano del globo
    ex = max(rect[0] + 20, min(tp[0], rect[2] - 20))
    ey = max(rect[1] + 20, min(tp[1], rect[3] - 20))
    draw.polygon([(ex, ey), (tp[0] - 8, tp[1]), (tp[0] + 8, tp[1])],
                 fill=(255, 255, 255, 235), outline=(0, 0, 0, 255))
    draw.line([(ex, ey), (tp[0], tp[1])], fill=(0, 0, 0, 255), width=3)
    lineas, _ = caja_texto(draw, texto, font, pt, bw - INSET * 2)
    ty = rect[1] + 10
    for line in lineas:
        lw = draw.textlength(line, font=font)
        draw.text(((rect[0] + rect[2]) // 2 - lw / 2, ty), line, font=font, fill=(20, 20, 20, 255))
        ty += int(pt * 1.35)
    usado.append(list(rect))
    del draw

def componer_pantalla(carpeta, m, dest, dialogo):
    validar(m)
    fondo = FONDO.get(m.get("bg", "blanco"), (255, 255, 255))
    base = Image.new("RGB", (ANCHO, ALTO), fondo)
    # fondo pintado (bg_img) a sangre si existe
    bgi = m.get("bg_img")
    if bgi:
        ruta = os.path.join(carpeta, bgi)
        if os.path.exists(ruta):
            if m.get("bg_img_fit"):
                base = resize_contener(Image.open(ruta), ANCHO, ALTO)
            else:
                base = resize_rellenar(Image.open(ruta), ANCHO, ALTO)
    rects = []
    y = 0
    npan = len(m["paneles"])
    if npan == 0:
        dibujar_narracion(base, m)
        base.save(dest, quality=95)
        return
    for i, ph in enumerate(m["paneles"]):
        y += m["gaps"][i]
        src = buscar_png(carpeta, m["n"], i)
        if src is None:
            src = buscar_png(carpeta, m["n"], None)
        if isinstance(src, list):
            src = src[i] if i < len(src) else src[0]
        if src:
            base.paste(resize_rellenar(Image.open(src), ANCHO, ph), (0, y))
        # marco negro del panel
        d = ImageDraw.Draw(base)
        d.rectangle([0, y, ANCHO - 1, y + ph - 1], outline=(0, 0, 0), width=MARCO)
        del d
        rects.append([y, y + ph])
        y += ph
    y += m["gaps"][npan]
    # marco de sangre en los cortes negros
    if m.get("marco_pantalla") or m.get("bg") == "negro de corte":
        d = ImageDraw.Draw(base)
        d.rectangle([0, 0, ANCHO - 1, ALTO - 1], outline=(0, 0, 0), width=MARCO)
        del d
    usado = []
    for df in dialogo:
        if df["pantalla"] == m["n"] and df["panel"] - 1 < len(rects):
            pr = [0, rects[df["panel"] - 1][0], ANCHO, rects[df["panel"] - 1][1]]
            dibujar_globo(base, pr, df["texto"], df.get("globo", "arriba-izq"),
                          df.get("cola", "abajo-dcha"), usado)
    cajas_usadas = []
    for fcaja in m.get("cajas", []):
        if fcaja["panel"] - 1 < len(rects):
            pr = [0, rects[fcaja["panel"] - 1][0], ANCHO, rects[fcaja["panel"] - 1][1]]
            dibujar_caja(base, pr, fcaja["texto"], cajas_usadas)
    for fsfx in m.get("sfx", []):
        if fsfx["panel"] - 1 < len(rects):
            pr = [0, rects[fsfx["panel"] - 1][0], ANCHO, rects[fsfx["panel"] - 1][1]]
            dibujar_sfx(base, pr, fsfx["texto"])
    dibujar_narracion(base, m)    # la narración va sobre los globos del fondo
    base.save(dest, quality=95)

def pdf_capitulo(cap, hacer_pdf):
    carpeta = os.path.join(IMG, "cap%02d" % cap)
    mpath = os.path.join(carpeta, "manifest.json")
    if not os.path.exists(mpath):
        print("  cap%02d: sin manifest.json" % cap)
        return 0
    man = json.load(open(mpath, encoding="utf-8"))
    outd = os.path.join(carpeta, "screens")
    os.makedirs(outd, exist_ok=True)
    paginas = []
    for m in man["screens"]:
        dest = os.path.join(outd, "cap%02d_s%02d.jpg" % (cap, m["n"]))
        componer_pantalla(carpeta, m, dest, man.get("dialogos", []))
        if hacer_pdf:
            paginas.append(Image.open(dest).convert("RGB"))
    if hacer_pdf:
        os.makedirs(SALIDA, exist_ok=True)
        pdf = os.path.join(SALIDA, "cap%02d.pdf" % cap)
        paginas[0].save(pdf, "PDF", resolution=120.0, save_all=True,
                        append_images=paginas[1:])
        print("  cap%02d '%s': %d pantallas -> %s" % (cap, man.get("titulo", ""), len(man["screens"]), os.path.basename(pdf)))
    else:
        print("  cap%02d '%s': %d pantallas listas" % (cap, man.get("titulo", ""), len(man["screens"])))
    return len(man["screens"])

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ayuda"
    hacer_pdf = "--pdf" in sys.argv
    if cmd == "cap":
        pdf_capitulo(int(sys.argv[2]), hacer_pdf)
    elif cmd == "todo":
        caps = sorted(int(re.search(r"cap(\d+)", d).group(1))
                      for d in os.listdir(IMG) if re.match(r"cap\d+$", d))
        for c in caps:
            pdf_capitulo(c, hacer_pdf)
    else:
        print(__doc__)