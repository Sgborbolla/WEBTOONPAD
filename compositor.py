#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compositor.py — monta las pantallas y los PDF de "Los Catorce".

Stitch dibuja el arte. Este script pone la geometría: gutters exactos, marcos
negros, fondos pintados, cajas de narración y los PDF de 10 capítulos.

La IA no cuenta píxeles. Aquí sí.
"""
import json, os, re, shutil, subprocess, sys, glob
from pathlib import Path

FUENTE     = "DejaVu-Sans-Bold"
ANCHO      = 800
ALTO       = 1280
MARCO      = 2
FONDO      = {"blanco": "#ffffff", "gris pasado": "#2a2a2e", "negro de corte": "#000000"}
RAIZ       = os.path.dirname(os.path.abspath(__file__))
IMG        = os.path.join(RAIZ, "img")
SALIDA     = os.path.join(RAIZ, "pdf")

_MAGICK_CMD = None


def _find_magick():
    global _MAGICK_CMD
    if _MAGICK_CMD:
        return _MAGICK_CMD
    candidates = ["magick", "magick.exe", "convert", "convert.exe"]
    for c in candidates:
        found = shutil.which(c)
        if found:
            _MAGICK_CMD = found
            return _MAGICK_CMD
    # fallback
    for c in candidates:
        if c in ("magick", "convert"):
            _MAGICK_CMD = c
            return _MAGICK_CMD
    raise RuntimeError("No se encuentra 'magick' ni 'convert' en PATH")


def magick(*args):
    cmd = _find_magick()
    r = subprocess.run([cmd, *[str(a) for a in args]], capture_output=True)
    if r.returncode != 0:
        err = r.stderr.decode(errors="replace") if r.stderr else ""
        raise RuntimeError("magick fallo: " + err[:400])
    return r.stdout

def validar(m):
    """Comprueba que los gaps + paneles suman exactamente ALTO."""
    if not m["paneles"]:
        return                      # pantalla de color liso: sin paneles
    total = sum(m["paneles"]) + sum(m["gaps"])
    if total != ALTO:
        raise ValueError(f"geometria invalida: {total} != {ALTO}")

def buscar_png(carpeta, num, panel=None):
    if panel is None:
        p = os.path.join(carpeta, f"s{num:02d}.png")
        if os.path.exists(p):
            return p
        c = sorted(glob.glob(os.path.join(carpeta, f"s{num:02d}_p*.png")))
        return c if len(c) > 1 else (c[0] if c else None)
    p = os.path.join(carpeta, f"s{num:02d}_p{panel+1}.png")
    return p if os.path.exists(p) else None

def caja_narracion(m, dest, tmpd):
    """Dibuja la caja fina de narración con su texto, si la pantalla la tiene."""
    nar = m.get("narracion")
    if not nar:
        return
    lineas = nar["texto"].split("\n")
    cuerpo  = nar.get("pt", 26)
    alto_linea = int(cuerpo * 1.5)
    x = nar.get("x", 40); y = nar.get("y", 40)
    ancho_caja = nar.get("w", 470)
    # el alto lo decide el numero de lineas
    pad = 18
    alto_caja = alto_linea * len(lineas) + pad * 2
    if nar.get("h"):
        alto_caja = nar["h"]
    fondo_caja = nar.get("fondo", "#ffffffcc")
    tinta      = "#000000" if nar.get("negro") else nar.get("tinta", "#111111")
    grosor     = nar.get("grosor", 3)
    capa = os.path.join(tmpd, "narracion.png")

    if nar.get("centro"):
        # cartela: caja centrada y texto centrado dentro de ella
        ancho_texto = nar.get("w", ANCHO - 160)
        x0 = (ANCHO - ancho_texto) // 2
        y0 = nar.get("y", 520)
        magick(dest, "-gravity", "NorthWest", "-stroke", fondo_caja,
               "-strokewidth", str(grosor), "-fill", "none",
               "-draw", f"rectangle {x0},{y0} {x0+ancho_texto},{y0+alto_caja}",
               "-stroke", "none", "-fill", tinta, "-font", FUENTE,
               "-pointsize", str(cuerpo), "-gravity", "North",
               *sum([["-annotate", f"+0+{y0+pad+alto_linea*(i+1)-int(cuerpo*0.3)}", l]
                     for i, l in enumerate(lineas)], []),
               capa)
    else:
        magick(dest, "-gravity", "NorthWest", "-stroke", fondo_caja,
               "-strokewidth", str(grosor), "-fill", "none",
               "-draw", f"rectangle {x},{y} {x+ancho_caja},{y+alto_caja}",
               "-stroke", "none", "-fill", tinta, "-font", FUENTE,
               "-pointsize", str(cuerpo), "-gravity", "NorthWest",
               *sum([["-annotate", f"+{x+pad}+{y+pad+alto_linea*(i+1)-int(cuerpo*0.3)}", l]
                     for i, l in enumerate(lineas)], []),
               capa)
    os.replace(capa, dest)

def componer_pantalla(carpeta, m, dest):
    validar(m)
    fondo = FONDO[m.get("bg", "blanco")]
    partes = []
    faltantes = []
    tmpd = dest + ".part"
    os.makedirs(tmpd, exist_ok=True)

    # lienzo base con el fondo
    base = os.path.join(tmpd, "base.png")
    magick("-size", f"{ANCHO}x{ALTO}", f"canvas:{fondo}", base)

    npan = len(m["paneles"])
    if npan == 0:
        magick(base, "-quality", "95", dest)
        caja_narracion(m, dest, tmpd)
        shutil.rmtree(tmpd, ignore_errors=True)
        return
    y = 0
    for i, ph in enumerate(m["paneles"]):
        y += m["gaps"][i]
        src = buscar_png(carpeta, m["n"], i)
        if src is None:
            src = buscar_png(carpeta, m["n"], None)
        if isinstance(src, list):
            src = src[i] if i < len(src) else src[0]
        if not src:
            faltantes.append(i + 1)
            y += ph
            continue
        destino = os.path.join(tmpd, f"p{i+1}.png")
        magick(src, "-resize", f"{ANCHO}x{ph}!", "-gravity", "North",
               "-background", fondo, "-extent", f"{ANCHO}x{ph}", destino)
        partes.append((y, destino))
        # marco del panel, a la misma altura que el panel
        marco = os.path.join(tmpd, f"m{i+1}.png")
        magick("-size", f"{ANCHO}x{ph}", "xc:none", "-stroke", "black",
               "-strokewidth", str(MARCO), "-fill", "none",
               "-draw", f"rectangle {MARCO//2},{MARCO//2} {ANCHO-1-MARCO//2},{ph-1-MARCO//2}",
               marco)
        partes.append((y, marco))
        y += ph
    y += m["gaps"][npan]

    # fondo pintado de la pantalla, si lo hay
    bgi = m.get("bg_img")
    if bgi:
        ruta = os.path.join(carpeta, bgi)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"falta el fondo {bgi}")
        capa = os.path.join(tmpd, "bg.png")
        magick(ruta, "-resize", f"{ANCHO}x{ALTO}!", "-gravity", "North",
               "-background", fondo, "-extent", f"{ANCHO}x{ALTO}", capa)
        magick(base, capa, "-composite", base)

    # cada parte va a SU y. -composite secuencial: -geometry solo no basta,
    # porque la pagina virtual se fija al leer la imagen, no despues.
    args = [base]
    for (yy, ruta) in partes:
        args += [ruta, "-geometry", f"+0+{yy}", "-composite"]
    args += ["-background", fondo, "-alpha", "remove", "-quality", "95", dest]
    magick(*args)

    # marco negro de pantalla completa (solo en los cortes a sangre)
    if m.get("marco_pantalla"):
        magick(dest, "-stroke", "black", "-strokewidth", str(MARCO), "-fill", "none",
               "-draw", f"rectangle {MARCO//2},{MARCO//2} {ANCHO-1-MARCO//2},{ALTO-1-MARCO//2}",
               dest)

    caja_narracion(m, dest, tmpd)
    shutil.rmtree(tmpd, ignore_errors=True)
    if faltantes:
        raise FileNotFoundError(f"faltan los paneles {faltantes} de la pantalla {m['n']}")

def pdf_capitulo(cap):
    carpeta = os.path.join(IMG, f"cap{cap:02d}")
    mpath = os.path.join(carpeta, "manifest.json")
    if not os.path.exists(mpath):
        print(f"  cap{cap:02d}: sin manifest.json, salto")
        return 0
    man = json.load(open(mpath, encoding="utf-8"))
    outd = os.path.join(IMG, f"cap{cap:02d}", "screens")
    os.makedirs(outd, exist_ok=True)
    n = 0
    for m in man["screens"]:
        dest = os.path.join(outd, f"cap{cap:02d}_s{m['n']:02d}.jpg")
        try:
            componer_pantalla(carpeta, m, dest)
            n += 1
        except Exception as e:
            print(f"  cap{cap:02d} s{m['n']:02d}: {e}")
    pdf = os.path.join(SALIDA, f"cap{cap:02d}.pdf")
    os.makedirs(SALIDA, exist_ok=True)
    files = sorted(glob.glob(os.path.join(outd, "*.jpg")))
    if files:
        magick(*files, "-quality", "88", pdf)
    print(f"  cap{cap:02d} '{man.get('titulo','')}': {n}/{len(man['screens'])} pantallas -> {os.path.basename(pdf)}")
    return n

def pdf_bloque(desde, hasta):
    os.makedirs(SALIDA, exist_ok=True)
    pdfs = []
    for c in range(desde, hasta + 1):
        p = os.path.join(SALIDA, f"cap{c:02d}.pdf")
        if os.path.exists(p):
            pdfs.append(p)
    if not pdfs:
        print(f"bloque {desde}-{hasta}: nada que unir"); return
    dest = os.path.join(SALIDA, f"los-catorce_{desde:03d}-{hasta:03d}.pdf")
    magick(*pdfs, dest)
    mb = os.path.getsize(dest) / 1048576
    print(f"BLOQUE {desde}-{hasta}: {len(pdfs)} capitulos -> {os.path.basename(dest)} ({mb:.1f} MB)")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ayuda"
    if cmd == "cap":
        pdf_capitulo(int(sys.argv[2]))
    elif cmd == "bloque":
        pdf_bloque(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "todo":
        caps = sorted(int(re.search(r"cap(\d+)", d).group(1))
                      for d in os.listdir(IMG) if re.match(r"cap\d+$", d))
        for c in caps:
            pdf_capitulo(c)
        for i in range(0, len(caps), 10):
            pdf_bloque(caps[i], min(caps[i+9], caps[-1]))
    else:
        print(__doc__)
        print("  compositor.py cap N          monta el capitulo N")
        print("  compositor.py bloque A B     une los capitulos A..B en un PDF")
        print("  compositor.py todo           monta todo y agrupa de 10 en 10")
