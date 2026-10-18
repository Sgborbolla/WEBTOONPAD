#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
NOV = os.path.join(RAIZ, "Novela", "novela_caps")
OUT = os.path.join(RAIZ, "Guiones")
ESTILO = os.path.join(RAIZ, "Guias", "estilo.txt")

BAN = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\u0400-\u04ff]")

LAY = {
 "T1": ([1280], [0, 0]),
 "T2R": ([1200], [40, 40]),
 "T3R": ([570, 570], [40, 60, 40]),
 "T4R": ([380, 380, 380], [35, 35, 35, 35]),
 "T5": ([260], [0, 1020]),
}

NAMES = ["Goro", "Arashi", "Rika", "Tsukimi", "Ren", "Hayashi", "Yui",
         "Nakamura", "Kosuke", "Nomura", "Kiryu", "Futaki", "Saeri",
         "Tsuyoshi", "Jumoji", "Park", "Sato", "Tanaka", "Kobayashi"]

VERBS = (r"(?:dijo|preguntó|respondió|contestó|gritó|murmuró|añadió|agregó|"
         r"repitió|explicó|pidió|ordenó|siguió|empezó|terminó|suspiró|rezongó|"
         r"insistió|concluyó|anunció|advirtió|llamó|refunfuñó|masculló|farfulló|"
         r"balbuceó|tartamudeó|siseó|rugió|bramó|exclamó|susurró|replicó|objetó|"
         r"protestó|comentó|apuntó|recitó|silabeó|sentenció|zanjó|gruñó|chilló)")

PAT = [3, 2, 3, 1, 2, 3, 3, 2, 1, 3, 2, 3, 2, 1, 3, 2, 3, 3, 2, 1, 3, 2, 1, 2, 3, 2, 3]

IMPACT = ("golpe", "impacto", "sangre", "grito", "disparo", "puerta", "explosión",
          "crujió", "chasquido", "golpeó", "derribó", "rompió")
QUIET = ("silencio", "quieto", "quieta", "nada", "vacío", "vacía", "solo", "sola")

PROTAG = {
 "Goro": ("Goro Arashi", "195 cm, muy alto y ancho, calvo, quemadura vieja en el cuello; coraza de placas oxidadas, casco de obra sin visor, escudo industrial atado a la espalda (marca única), guantes de cuero con brasa naranja en el derecho; arma: maza/martillo industrial."),
 "Rika": ("Rika Tsukimi", "15 años, 158 cm, menuda; pelo rojo en coleta alta, cicatriz en la ceja izquierda; kimono corto negro con haori corto color hueso (marca única), vendas blancas en los antebrazos, sandalias de rejilla; velocidad."),
 "Ren": ("Ren Hayashi", "16 años aparentes, delgado y nervioso; amarillo chillón sobre negro, agujero en una manga, vendas en las muñecas, zapatillas de running; marca única: las vendas y el amarillo; velocidad."),
 "Yui": ("Yui Nakamura", "22 años, 172 cm, muy erguida; uniforme militar gris azulado con chaleco portaplacas, guantes claros, moño alto; arma: rifle de cerrojo (marca única)."),
}

ARCH = {
 "Carrilero": ("rango amarillo (línea), del tamaño de un caballo", "largo y bajo, corre en línea recta; embiste sin frenar."),
 "Embestidor": ("rango amarillo (línea), del tamaño de un caballo", "hombro grande, cabeza hundida, cuello casi nulo; embestida con el hombro."),
 "Lanzador": ("rango amarillo (línea), del tamaño de un caballo", "vertical, brazos largos, sin cuello visible; lanza desde lejos."),
 "Blindado": ("rango amarillo (línea), del tamaño de un caballo", "cuadrado, con placas, sin cuello; no se mueve, hay que rodearlo."),
 "Resucitado": ("rango amarillo (línea), del tamaño de un caballo", "encorvado, con un cuerpo humano debajo; se levanta, vuelve a caerse, se levanta otra vez."),
}

KW = ("kimono", "haori", "coraza", "armadura", "casco", "escudo", "maza", "martillo",
      "rifle", "guante", "botas", "abrigo", "chaqueta", "máscara", "gafas", "mono",
      "chaleco", "venda", "coleta", "pelo", "ojos", "piel", "quemadura", "cicatriz",
      "uniforme", "capa", "mochila", "bolsa", "amarillo", "negro", "gris", "azul",
      "rojo", "verde", "naranja", "alto", "bajo", "delgado", "grande", "pequeño",
      "tamaño", "silueta", "hombro", "cabeza", "cuello", "brazos", "encorvado")


def desc_sentences(text, needles, limit=2):
    out = []
    for s in re.split(r"(?<=[.!?…»])\s+", text):
        sl = s.strip()
        if not sl:
            continue
        low = sl.lower()
        if any(n in sl for n in needles) and any(k in low for k in KW):
            out.append(sl)
        if len(out) >= limit:
            break
    return out


def cast_section(text):
    L = []
    L.append("## Elenco y enemigos de este capítulo (según la novela)")
    L.append("")
    L.append("**Regla:** el bloque ANCLA manda para que cada personaje salga idéntico en")
    L.append("todos los capítulos; si la novela de ESTE capítulo describe algo distinto, se")
    L.append("respeta lo que dice la novela de este capítulo.")
    L.append("")
    L.append("**Protagonistas presentes** (ropa y armas fijas; ver ANCLA):")
    L.append("")
    for key, (nombre, rasgos) in PROTAG.items():
        ap = nombre.split()[0]
        if ap in text or nombre in text:
            L.append("- **%s** — %s" % (nombre, rasgos))
            for s in desc_sentences(text, [nombre, ap]):
                L.append("    - *En este capítulo (novela):* %s" % s)
    L.append("")
    L.append("**Enemigos de este capítulo** (arquetipo y rango según su nombre; más lo que diga la novela):")
    L.append("")
    L.append("*El color es el RANGO de peligro que les asignan los humanos, no el color de su piel.*")
    L.append("")
    found = False
    for key, (rango, forma) in ARCH.items():
        if key.lower() in text.lower():
            found = True
            L.append("- **%s** — %s; %s" % (key, rango, forma))
            for s in desc_sentences(text, [key]):
                L.append("    - *En este capítulo (novela):* %s" % s)
    if not found:
        L.append("- Ninguno con nombre en este capítulo (amenaza de fondo).")
    otros = []
    for col, puesto in (("verde", "exploración"), ("azul", "mínimo"), ("naranja", "subjefe"),
                        ("rojo", "jefe"), ("negro", "mando")):
        if col in text.lower():
            otros.append("%s (rango %s)" % (col, puesto))
    if otros:
        L.append("")
        L.append("**Otras alertas de peligro presentes:** " + ", ".join(otros) + ".")
    L.append("")
    L.append("---")
    L.append("")
    return L


def clean(s):
    return BAN.sub("", s)


def ancla_bloque():
    t = open(ESTILO, encoding="utf-8").read()
    m = re.search(r"```\n(.*?)\n```", t, re.S)
    return BAN.sub("", m.group(1)) if m else ""


def split_sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.!?…»])\s+", p.strip()) if s.strip()]


SHOTS = ["Primer plano", "Plano medio", "Plano detalle", "Primerísimo primer plano",
         "Plano americano", "Plano de bocas", "Contrapicado"]


def detect_speaker(ln, last):
    m = re.search(VERBS + r"\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)", ln)
    if m and m.group(1) in NAMES:
        return m.group(1)
    for nm in NAMES:
        if nm in ln:
            return nm
    return last


def parse_dialog(body):
    globo, attrib = body, ""
    m = re.search(r"\s+[—–]\s*(" + VERBS + r"\b.*)$", body)
    if not m:
        m = re.search(r",\s*(" + VERBS + r"\b.*)$", body)
    if m and m.start() > 0:
        globo, attrib = body[:m.start()].rstrip(" ,"), m.group(1).strip()
    globo = globo.strip().strip("«»").strip()
    attrib = attrib.strip()
    if attrib:
        attrib = attrib[0].upper() + attrib[1:]
    return globo, attrib


def beats_from(text):
    beats = []
    last = None
    for raw in text.splitlines():
        ln = clean(raw).strip()
        if not ln or ln.startswith("#") or ln.startswith("> **Autor"):
            continue
        if ln.startswith(">>>"):
            beats.append({"kind": "rotulo", "text": ln[3:].strip()})
            continue
        if ln.startswith("—") or ln.startswith("–"):
            body = ln.lstrip("—– ").strip()
            globo, attrib = parse_dialog(body)
            if not globo:
                globo, attrib = body, ""
            spk = detect_speaker(ln, last)
            beats.append({"kind": "dialog", "text": globo, "speaker": spk, "attrib": attrib})
            continue
        for nm in NAMES:
            if nm in ln:
                last = nm
        cur, wc = [], 0
        for s in split_sentences(ln):
            cur.append(s)
            wc += len(s.split())
            if wc >= 28:
                beats.append({"kind": "desc", "text": " ".join(cur)})
                cur, wc = [], 0
        if cur:
            beats.append({"kind": "desc", "text": " ".join(cur)})
    return beats


def tipo_for(k, beats):
    if k >= 3:
        return "T4R"
    if k == 2:
        return "T3R"
    t = " ".join(b.get("text", "") for b in beats).lower()
    if any(w in t for w in QUIET):
        return "T5"
    if any(w in t for w in IMPACT):
        return "T1"
    return "T2R"


def pack(beats):
    screens = []
    buf = []
    pi = 0
    for b in beats:
        if b["kind"] == "rotulo":
            if buf:
                screens.append(("vi", tipo_for(len(buf), buf), buf))
                buf = []
            screens.append(("rot", "T6", [b]))
            continue
        buf.append(b)
        if len(buf) == PAT[pi % len(PAT)]:
            screens.append(("vi", tipo_for(len(buf), buf), buf))
            buf = []
            pi += 1
    if buf:
        screens.append(("vi", tipo_for(len(buf), buf), buf))
    return screens


def build(n):
    src = os.path.join(NOV, "cap%02d.txt" % n)
    text = open(src, encoding="utf-8").read()
    lines = text.splitlines()
    titulo = lines[0].split("—", 1)[1].strip() if "—" in lines[0] else "Capítulo %d" % n
    beats = beats_from(text)
    screens = pack(beats)

    vnum = 0
    out_screens = []
    for kind, tipo, bs in screens:
        vns = []
        if kind == "vi":
            for _ in bs:
                vnum += 1
                vns.append(vnum)
        out_screens.append({"kind": kind, "tipo": tipo, "beats": bs, "vns": vns})

    n_vin = vnum
    n_pant = len(out_screens)
    globos = []
    cajas = []
    for idx, sc in enumerate(out_screens):
        if sc["kind"] == "rot":
            nxt = None
            for j in range(idx + 1, len(out_screens)):
                if out_screens[j]["vns"]:
                    nxt = out_screens[j]["vns"][0]
                    break
            if nxt is None and n_vin:
                nxt = n_vin
            cajas.append((nxt, sc["beats"][0]["text"]))
        else:
            for v, b in zip(sc["vns"], sc["beats"]):
                if b["kind"] == "dialog":
                    globos.append((v, b.get("speaker"), b["text"]))

    apariciones = []
    for _, spk, _ in globos:
        if spk and spk not in apariciones:
            apariciones.append(spk)
    personajes = ", ".join(apariciones) if apariciones else "Los cuatro transformados; vecinos del bloque"

    rotulos = [s["beats"][0]["text"] for s in out_screens if s["kind"] == "rot"]
    estructura = "Adaptación fiel de la novela, capítulo %d (%d rótulo%s de escena)." % (
        n, len(rotulos), "" if len(rotulos) == 1 else "s")
    fondo = rotulos[0] if rotulos else "Japón contemporáneo, día %d" % n

    enemigos = []
    for key in ARCH:
        if key.lower() in text.lower():
            enemigos.append("%s (rango amarillo)" % key)
    enemigos_txt = ", ".join(enemigos) if enemigos else "Ninguno con nombre; amenaza de fondo"

    ANCLA = ancla_bloque()
    L = []
    L.append("# CAPÍTULO %d — %s" % (n, titulo))
    L.append("> **Autor:** Sergio Grabiel Borbolla Verdecia")
    L.append("")
    L.append("## BLOQUE DE ANCLA STITCH — pegar tal cual al inicio")
    L.append("```")
    L.append(ANCLA)
    L.append("```")
    L.append("")
    L.extend(cast_section(text))
    L.append("> **Retícula:** `Guias/medidas-referencia.txt` §5. Pantallas de 800×1280.")
    L.append("> **Total:** %d pantallas de 800×1280 · %d viñetas · %d px de scroll" % (n_pant, n_vin, n_pant * 1280))
    L.append("")
    L.append("## Ficha")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    L.append("| Géneros | Ciencia ficción, terror de ciudad, catástrofe |")
    L.append("| Estructura | %s |" % estructura)
    L.append("| Fondo | %s |" % fondo)
    L.append("| Personajes con nombre | %s |" % personajes)
    L.append("| Enemigos visibles | %s |" % enemigos_txt)
    L.append("| Pantallas | %d |" % n_pant)
    L.append("| Viñetas | %d |" % n_vin)
    L.append("| Globos de diálogo | %d |" % len(globos))
    L.append("| Cajas de narración | %d |" % len(cajas))
    L.append("| SFX | gráfico |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Reglas de esta adaptación")
    L.append("")
    L.append("- **Mostrar, no contar.** La emoción se vuelve acción, pausa, objeto o encuadre.")
    L.append("- **Una acción visible por viñeta.** Nada de pensamientos que no se puedan dibujar.")
    L.append("- **Diálogo recortado** a lo esencial: cada globo cabe en hasta 3 líneas.")
    L.append("- **El gutter es tiempo:** los cierres y las dudas van tras un silencio (T5).")
    L.append("- **El impacto ocupa el panel más grande** (T1, a sangre).")
    L.append("- **Texto fuera del arte.** Globos, cajas y SFX se montan encima.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Mapa de pantallas")
    L.append("")
    L.append("| S | Tipo | Viñetas | Alturas | Gaps |")
    L.append("|---|---|---:|---|---|")
    for i, sc in enumerate(out_screens, 1):
        t = sc["tipo"]
        if t == "T6":
            L.append("| S%02d | T6 | 0 | — | rótulo |" % i)
        else:
            h, g = LAY[t]
            L.append("| S%02d | %s | %d | %s | %s |" % (
                i, t, len(h), "/".join(str(x) for x in h), "/".join(str(x) for x in g)))
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Las viñetas")
    L.append("")
    for i, sc in enumerate(out_screens, 1):
        if sc["kind"] == "rot":
            L.append("### S%02d · T6 · rótulo" % i)
            L.append("> **RÓTULO:** %s" % sc["beats"][0]["text"])
            L.append("")
            continue
        t = sc["tipo"]
        k = len(sc["vns"])
        L.append("### S%02d · %s · %d viñeta%s" % (i, t, k, "" if k == 1 else "s"))
        for v, b in zip(sc["vns"], sc["beats"]):
            if b["kind"] == "dialog":
                spk = b.get("speaker")
                att = b.get("attrib") or ""
                if att:
                    desc = "%s. %s" % (SHOTS[v % len(SHOTS)], att)
                else:
                    desc = "%s. %s habla." % (SHOTS[v % len(SHOTS)], spk if spk else "Alguien")
                L.append("**V%d.** %s" % (v, desc))
                L.append("> **GLOBO:** %s" % b["text"])
            else:
                L.append("**V%d.** %s" % (v, b["text"]))
            L.append("")
    L.append("---")
    L.append("")
    L.append("## Globos de diálogo (%d)" % len(globos))
    L.append("")
    L.append("| V | Personaje | Texto |")
    L.append("|---|---|---|")
    for v, spk, txt in globos:
        L.append("| V%d | %s | %s |" % (v, spk if spk else "—", txt))
    L.append("")
    L.append("## Cajas de narración (%d)" % len(cajas))
    L.append("")
    L.append("| V | Texto |")
    L.append("|---|---|")
    for v, txt in cajas:
        if v is None:
            continue
        L.append("| V%d | Rótulo: %s |" % (v, txt))
    L.append("")
    dst = os.path.join(OUT, "cap%02d.txt" % n)
    open(dst, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return n_pant, n_vin, len(globos), len(cajas)


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print("uso: make_guion.py 3 4 5 ...")
        return
    for a in args:
        n = int(a)
        p, v, g, c = build(n)
        print("cap%02d  %d pantallas · %d viñetas · %d globos · %d cajas" % (n, p, v, g, c))


if __name__ == "__main__":
    main()
