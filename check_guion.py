#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_guion.py — valida un guion detallado contra el formato canónico.

Uso:
  python3 check_guion.py cap 6
  python3 check_guion.py todo
  python3 check_guion.py 2 3 4

Comprueba:
  1. Cabecera `**Total:** 60 pantallas ... · 120 viñetas · 76.800 px`.
  2. Filas de tabla | S | Tipo | Viñetas | Alturas | Gaps | -> S01..S60 exactos.
  3. Geometria: paneles + gaps == 1280 en cada pantalla (T6 sin paneles).
  4. Total de viñetas desde la geometria == 120.
  5. Encabezados ### Snn presentes para cada pantalla.
  6. Viñetas **Vn.** consecutivas 1..120 sin huecos ni duplicados.
  7. Conteos de LOS TEXTOS (globos/cajas) coherentes con su cabecera (N).
  8. Cero kana/kanji/hangul/cirilico. Cero ingles obvio en dialogos.
"""
import os, re, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
RE_ROW = re.compile(r"^\s*\|\s*(S\d+[A-Z]?)\s*\|\s*([^\|]+?)\s*\|\s*(\d+)\s*\|\s*([^\|]*?)\s*\|\s*([^\|]+?)\s*\|")
RE_V_HEAD = re.compile(r"^#{3,4}\s+S(\d+)[A-Z]?\s*·", re.M)
RE_V_NUM = re.compile(r"^\*\*[Vv](\d+)\.\*\*", re.M)
RE_SCRIPT = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\u0400-\u04ff]")
ENG = set("""the and with this that you your have has what when where they then from all are is not but for
will can could would should there here about into over under after before very just also each other""".split())


def geom(tipo, hstr, gstr):
    if tipo.upper().startswith("T6"):
        return [], []
    h = [int(x) for x in hstr.split("/") if x.strip().isdigit()]
    g = [int(x) for x in re.sub(r"[—\-].*$", "", gstr).replace(" ", "").split("/") if x.strip().isdigit()]
    return h, g


def rango_v(celda):
    m = re.match(r"^[vV](\d+)(?:\s*[-–]\s*[vV]?(\d+))?$", celda.strip())
    if not m:
        return []
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    if b < a:
        a, b = b, a
    return list(range(a, b + 1))


def contar_tabla(texto, heading):
    """Suma los V que declaran las filas bajo una cabecera ### Globos/Cajas..."""
    out = None
    for m in re.finditer(r"^#{2,4}\s+(" + heading + r"[^\n]*)$", texto, re.M):
        fin = texto.find("\n#", m.end())
        seg = texto[m.end(): fin if fin > 0 else len(texto)]
        total = 0
        for ln in seg.splitlines():
            if not ln.strip().startswith("|"):
                continue
            celdas = [c.strip() for c in ln.strip().strip("|").split("|")]
            if not celdas:
                continue
            vs = rango_v(celdas[0])
            if vs:
                total += len(vs)
        out = (out or 0) + total
    return out


def check(path, nombre):
    errs, warns = [], []
    t = open(path, encoding="utf-8").read()

    m = re.search(r"\*\*Total:\*\*\s*\**(\d+)\s*pantallas[^\n·]*·\s*\**(\d+)\s*viñetas", t)
    if not m:
        errs.append("cabecera **Total:** no encontrada")
        n_pant, n_vin = 60, 120
    else:
        n_pant, n_vin = int(m.group(1)), int(m.group(2))

    # 2/3/4 geometria desde tablas
    filas, seen = [], set()
    for i, ln in enumerate(t.splitlines(), 1):
        mm = RE_ROW.match(ln)
        if not mm:
            continue
        k = mm.group(1)
        if k in seen:
            continue
        seen.add(k)
        filas.append((i, k, mm.group(2).strip(), int(mm.group(3)),
                      mm.group(4).strip(), mm.group(5).strip()))

    if not filas:
        errs.append("sin filas de tabla | S | Tipo | ... (MAPA DE PANTALLAS)")

    suma_v = 0
    s_nums = []
    for (i, k, tipo, npan, hstr, gstr) in filas:
        s_nums.append(int(re.match(r"S(\d+)", k).group(1)))
        h, g = geom(tipo, hstr, gstr)
        if not tipo.upper().startswith("T6"):
            if not h:
                errs.append("L%d %s: alturas no numericas (%r)" % (i, k, hstr))
                continue
            tot = sum(h) + sum(g)
            if tot != 1280:
                errs.append("L%d %s %s: %d + %d = %d != 1280" % (i, k, tipo, sum(h), sum(g), tot))
            if len(h) != npan and npan:
                errs.append("L%d %s: dice %d viñetas pero la geometria tiene %d" % (i, k, npan, len(h)))
        suma_v += len(h)

    if filas:
        if sorted(s_nums) != list(range(1, n_pant + 1)):
            miss = [n for n in range(1, n_pant + 1) if n not in s_nums]
            dup = [n for n in set(s_nums) if s_nums.count(n) > 1]
            errs.append("S en tablas != S01..S%02d (faltan %s, repetidas %s)" % (n_pant, miss[:10], dup[:10]))
        if suma_v != n_vin:
            errs.append("viñetas desde geometria = %d, cabecera dice %d" % (suma_v, n_vin))

    # 5 encabezados ### Snn
    heads = [int(x) for x in RE_V_HEAD.findall(t)]
    faltan_head = [n for n in range(1, n_pant + 1) if n not in heads]
    if faltan_head:
        errs.append("sin encabezado ###/#### para pantallas: %s" % faltan_head[:12])

    # 6 numeracion de viñetas
    vs = [int(x) for x in RE_V_NUM.findall(t)]
    if not vs:
        errs.append("sin viñetas **Vn.**")
    else:
        if len(vs) != len(set(vs)):
            d = sorted({v for v in vs if vs.count(v) > 1})
            errs.append("viñetas duplicadas: %s" % d[:10])
        if sorted(set(vs)) != list(range(1, max(vs) + 1)):
            miss = [n for n in range(1, max(vs) + 1) if n not in set(vs)]
            errs.append("huecos en numeracion de viñetas: %s" % miss[:10])
        if max(vs) != n_vin:
            errs.append("ultima viñeta V%d, cabecera dice %d" % (max(vs), n_vin))
        orden = "OK" if vs == sorted(vs) else "desordenado (%s)" % vs
        if vs != sorted(vs):
            warns.append("orden de aparicion de Vn. %s" % orden)

    # 7 LOS TEXTOS
    for head, etiqueta in (("Globos", "globos"), ("Cajas", "cajas")):
        for mm in re.finditer(r"^#{2,4}\s+" + head + r"[^\n]*\((\d+)\)", t, re.M):
            decl = int(mm.group(1))
            real = contar_tabla(t[mm.start():], head)
            if real is not None and real != decl:
                errs.append("LOS TEXTOS: cabecera %s (%d) pero las filas suman %d" % (etiqueta, decl, real))

    # 8 scripts prohibidos
    for mm in RE_SCRIPT.finditer(t):
        linea = t.count("\n", 0, mm.start()) + 1
        errs.append("L%d: caracter prohibido %r" % (linea, mm.group()))
        break

    # 8b ingles en globos/cajas
    eng = set()
    for ln in t.splitlines():
        mm = re.match(r"^\s*\|\s*[vV]\d+(?:[-–][vV]?\d+)?\s*\|(.+)$", ln) or \
             re.match(r"^>\s*\*\*[^*]+:\*\*\s*(.+)$", ln)
        if not mm:
            continue
        for w in re.findall(r"[A-Za-zÁÉÍÓÚáéíóúñÑ']+", mm.group(1)):
            if w.lower() in ENG:
                eng.add(w.lower())
    if eng:
        errs.append("posible ingles en dialogos: %s" % sorted(eng))

    etiqueta = "OK  " if not errs else "FAIL"
    print("%s %s  (S=%d V=%d tabla=%d)" % (etiqueta, nombre, n_pant, n_vin, len(filas)))
    for e in errs:
        print("     - " + e)
    for w in warns:
        print("     ~ " + w)
    return not errs


def main():
    args = sys.argv[1:]
    caps = []
    if args and args[0] == "todo":
        caps = list(range(1, 31))
        args = []
    elif args and args[0] == "cap":
        caps = [int(args[1])]
        args = []
    else:
        caps = [int(x) for x in args if x.isdigit()]
    if not caps:
        caps = list(range(1, 31))
    ok = True
    for c in caps:
        p = os.path.join(RAIZ, "Guiones", "cap%02d.txt" % c)
        if not os.path.exists(p):
            print("---- cap%02d.txt no existe" % c)
            continue
        ok = check(p, "cap%02d" % c) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
