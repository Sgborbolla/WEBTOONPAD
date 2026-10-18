# -*- coding: utf-8 -*-
# Genera NPAD_NOVELA.docx a partir de los capitulos en prosa de novela_caps/
# Sin dependencias externas: usa solo la stdlib de Python (zip + xml).
# Uso: python3 make_docx.py

import os, re, sys, zipfile, datetime, struct, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE, "novela_caps")
OUT = os.path.join(BASE, "NPAD_NOVELA.docx")

TITULO = "Nippon Post-Apocalyptic Disaster"
SUBTITULO = "N P A D"
AUTOR = "Sergio Grabiel Borbolla Verdecia"
SERIE = "TEMPORADA 1 · CAPÍTULOS 1 A 100"

COVER = None
for cand in ("portada.png", "portada.jpg", "portada.jpeg"):
    p = os.path.join(BASE, cand)
    if os.path.exists(p):
        COVER = (p, cand.split(".")[-1])
        break

# Fondo de la pagina de titulo/autor: COLOR CALIDO SOLIDO (imagen llena)
# por decision del autor (2026-10-14). La pagina 2 va con fondo calido detras
# del titulo/autor, sin foto.
TITLE_BG = None
for cand in ("fondo-calido.png", "fondo-calido.jpg"):
    p = os.path.join(BASE, cand)
    if os.path.exists(p):
        TITLE_BG = (p, cand.split(".")[-1])
        break

TITLE_IMG = None

# Pagina en EMU (914400 por pulgada).
PAGE_W_EMU = int(11906 / 1440 * 914400)
PAGE_H_EMU = int(16838 / 1440 * 914400)
PAGE_TEXT_EMU = int((11906 - 2 * 1134) / 1440 * 914400)

IMAGES = []

def img_info(path):
    with open(path, "rb") as f:
        sig = f.read(8)
    if sig[:8] == b"\x89PNG\r\n\x1a\n":
        with open(path, "rb") as f:
            d = f.read(32)
        w, h = struct.unpack(">II", d[16:24])
        return "png", "image/png", w, h
    with open(path, "rb") as f:
        d = f.read(65536 * 8)
    i = 2
    while i < len(d):
        if d[i] != 0xFF:
            while i < len(d) and d[i] != 0xFF:
                i += 1
            continue
        while i < len(d) and d[i] == 0xFF:
            i += 1
        m = d[i]; i += 1
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xCA):
            h, w = struct.unpack(">HH", d[i + 3:i + 7])
            return "jpg", "image/jpeg", w, h
        ln = struct.unpack(">H", d[i:i + 2])[0]; i += ln
    return None

def cover_emu():
    return PAGE_W_EMU, PAGE_H_EMU

def cover_drawing_xml(sect=""):
    cx, cy = cover_emu()
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>'
            + sect + '</w:pPr>'
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="' + str(cx) + '" cy="' + str(cy) + '"/>'
            '<wp:docPr id="1" name="Portada"/>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic>'
            '<pic:nvPicPr><pic:cNvPr id="1" name="Portada"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="rId3"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + str(cx) + '" cy="' + str(cy) + '"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic>'
            '</a:graphicData></a:graphic>'
            '</wp:inline>'
            '</w:drawing></w:r></w:p>')

def bg_anchor_xml(cx, cy, rid="rId4"):
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:drawing>'
            '<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="0" '
            'behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
            '<wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
            '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
            '<wp:extent cx="' + str(cx) + '" cy="' + str(cy) + '"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:wrapNone/>'
            '<wp:docPr id="2" name="Fondo"/>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic>'
            '<pic:nvPicPr><pic:cNvPr id="2" name="Fondo"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="' + rid + '"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + str(cx) + '" cy="' + str(cy) + '"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic>'
            '</a:graphicData></a:graphic>'
            '</wp:anchor>'
            '</w:drawing></w:r></w:p>')

def title_img_xml():
    ext, _, w, h = img_info(TITLE_IMG)
    emu_w = int(PAGE_W_EMU * 0.60)
    emu_h = int(h / w * emu_w)
    return ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="' + str(emu_w) + '" cy="' + str(emu_h) + '"/>'
            '<wp:docPr id="3" name="TituloNeon"/>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic>'
            '<pic:nvPicPr><pic:cNvPr id="3" name="TituloNeon"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="rId5"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + str(emu_w) + '" cy="' + str(emu_h) + '"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic>'
            '</a:graphicData></a:graphic>'
'</wp:inline>'
             '</w:drawing></w:r></w:p>')

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def load_chapters():
    caps = []
    def cap_key(f):
        m = re.match(r"cap(\d+)", f, re.I)
        return (int(m.group(1)) if m else 1 << 30, f)
    for f in sorted(os.listdir(CAPS_DIR), key=cap_key):
        if f.lower().endswith(".txt"):
            with open(os.path.join(CAPS_DIR, f), encoding="utf-8") as fh:
                caps.append(fh.read())
    if not caps:
        sys.exit("No hay capitulos en novela_caps/")
    return caps

def parse_chapter(raw):
    lines = raw.splitlines()
    # El archivo empieza con el titulo de capitulo: # CAPÍTULO N — "Titulo"
    title = "Capítulo sin título"
    body = []
    for i, ln in enumerate(lines):
        if re.match(r"^#+\s*CAPÍTULO", ln, re.I):
            title = re.sub(r"^#+\s*", "", ln).strip()
            body = lines[i+1:]
            break
    return title, "\n".join(body).strip()

def paras_from_text(text):
    paras = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        m = re.match(r"^\[IMG:([^\]]+)\]$", block)
        if m:
            paras.append(("image", m.group(1)))
            continue
        if block.startswith(">>>"):
            paras.append(("scene", block[3:].strip()))
        elif block.startswith(">>"):
            paras.append(("center", block[2:].strip()))
        elif block.startswith(">"):
            continue
        else:
            for lp in block.split("\n"):
                lp = lp.strip()
                if lp.startswith(">"):
                    continue
                if lp:
                    paras.append(("normal", lp))
    return paras

def p_xml(kind, text, first="", tight=False):
    if kind == "image":
        global IMAGES
        p = os.path.join(BASE, text.strip())
        if not os.path.exists(p):
            return ""
        info = img_info(p)
        if not info:
            return ""
        ext, mime, w, h = info
        idx = len(IMAGES)
        rid = "rId" + str(8 + idx)
        media = "image" + str(5 + idx) + "." + ext
        IMAGES.append((p, rid, media))
        emu_w = int(PAGE_TEXT_EMU * 0.92)
        emu_h = int(h / w * emu_w)
        did = 20 + idx
        return ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr>'
                '<w:r><w:drawing>'
                '<wp:inline distT="0" distB="0" distL="0" distR="0">'
                '<wp:extent cx="' + str(emu_w) + '" cy="' + str(emu_h) + '"/>'
                '<wp:docPr id="' + str(did) + '" name="Ilustracion"/>'
                '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                '<pic:pic>'
                '<pic:nvPicPr><pic:cNvPr id="' + str(did) + '" name="Ilustracion"/><pic:cNvPicPr/></pic:nvPicPr>'
                '<pic:blipFill><a:blip r:embed="' + rid + '"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + str(emu_w) + '" cy="' + str(emu_h) + '"/></a:xfrm>'
                '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
                '</pic:pic>'
                '</a:graphicData></a:graphic>'
                '</wp:inline>'
                '</w:drawing></w:r></w:p>')
    if kind == "caption":
        return ('<w:p><w:pPr><w:pStyle w:val="Caption"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "title":
        return ('<w:p><w:pPr><w:pStyle w:val="Title"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "sub":
        return ('<w:p><w:pPr><w:pStyle w:val="Subtitle"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "author":
        return ('<w:p><w:pPr><w:pStyle w:val="Author"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "chapter":
        return ('<w:p><w:pPr><w:pStyle w:val="CapTitle"/>' + first +
                '<w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "serie":
        return ('<w:p><w:pPr><w:pStyle w:val="SerieTag"/><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "scene":
        t = '<w:spacing w:before="120" w:after="80"/>' if tight else ''
        return ('<w:p><w:pPr><w:pStyle w:val="SceneTag"/>' + t + '</w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "center":
        return ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    t = '<w:spacing w:after="80"/>' if tight else ''
    ppr = '<w:pPr><w:pStyle w:val="Novela"/>' + t + first + '</w:pPr>'
    return '<w:p>' + ppr + '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>'

def page_break_xml():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def style_para(style, text):
    return ('<w:p><w:pPr><w:pStyle w:val="' + style + '"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">' + esc(text) + '</w:t></w:r></w:p>')

def glossary_para(term, definition):
    return ('<w:p><w:pPr><w:pStyle w:val="GlosDef"/></w:pPr>'
            '<w:r><w:rPr><w:b/><w:color w:val="1D3A8A"/></w:rPr>'
            '<w:t xml:space="preserve">' + esc(term) + '</w:t></w:r>'
            '<w:r><w:t xml:space="preserve"> — ' + esc(definition) + '</w:t></w:r></w:p>')

def index_entry_xml(text, bk):
    fld = ('<w:r><w:tab/></w:r>'
           '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
           '<w:r><w:instrText xml:space="preserve"> PAGEREF ' + bk + ' \\h </w:instrText></w:r>'
           '<w:r><w:fldChar w:fldCharType="end"/></w:r>')
    return ('<w:p><w:pPr><w:pStyle w:val="IndexEntry"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">' + esc(text) + '</w:t></w:r>' + fld + '</w:p>')

def build_index_block(caps):
    out = ['<w:p><w:pPr><w:pStyle w:val="IndexTitle"/></w:pPr>'
           '<w:bookmarkStart w:id="2500" w:name="_Toc_indice"/>'
           '<w:r><w:t>ÍNDICE</w:t></w:r>'
           '<w:bookmarkEnd w:id="2500"/></w:p>']
    out.append(index_entry_xml("Índice", "_Toc_indice"))
    for i, c in enumerate(caps, 1):
        title, _ = parse_chapter(c)
        n = re.match(r"^CAPÍTULO\s+(\d+)", title, re.I)
        num = n.group(1) if n else str(i)
        rest = title.split("—", 1)[-1].strip().strip('"').strip()
        out.append(index_entry_xml("Capítulo " + num + " — " + rest, "_Toc_cap" + num))
    out.append(index_entry_xml("Apéndices y glosario", "_Toc_apendices"))
    return "".join(out)

GLOSARIO = [
    ("EL MUNDO KAIYU", [
        ("Kaiyu", "Nombre genérico de los enemigos. No son fauna suelta: son un ejército organizado de una civilización alienígena que llega desde «el cielo de abajo». Cada color equivale a un rango de combate."),
        ("El cielo de abajo", "Así llaman los kaiyu a su mundo de origen. Llegaron a la Tierra desde él a través de las brechas."),
        ("Ghar-Máth", "Planeta de origen de los kaiyu; gobernado por el rey tirano Kor'váth. También llamado «La Gran Matriz Abisal» o «El Núcleo Roto»."),
        ("Gar-Máth", "Variante con que los capítulos escriben Ghar-Máth. Es el mismo planeta."),
        ("El Abismo", "Nombre con que los humanos llaman al planeta kaiyu; también «El Mundo de Bestias»."),
        ("La Sima del Trono (Kor-Váth)", "Hemisferio superior de Ghar-Máth. Fortalezas colosales de obsidiana negra y metal pesado donde reside el rey tirano y opera el Mando Administrativo."),
        ("Las Tierras de Ceniza (X'vár-Má)", "Valles yermos e interminables con atmósfera de plasma gris y radiación térmica; principal escenario de la guerra civil kaiyu."),
        ("Los Tubos de Cría (Min-Rok)", "Subsuelos profundos donde se incuban masivamente las oleadas biológicas y se procesan recursos para las brechas dimensionales."),
        ("El Eje Fracturado", "Región central de Ghar-Máth donde la corteza se desgarró, abriendo las fisuras espaciales hacia la Tierra."),
        ("Calderos tectónicos", "Instalaciones monumentales que queman la energía del núcleo de Ghar-Máth para rasgar el tejido espacial."),
        ("Suministros kaiyu", "Subsistencia a base de gránulos de biomasa sintética y pasta de plasma refinado, racionados por el Mando. El agua líquida es un lujo escaso."),
        ("Leyes y castigos kaiyu", "Sin cárceles. La disidencia o el fallo táctico enfrenta el Tribunal de Fuego o la degradación biológica a explorador kamikaze (Zár-uk), sin retorno."),
        ("Cánticos de Abismo (Már-Rok)", "Coros colosales de bajas frecuencias e infrasonidos pectorales con que los kaiyu sincronizan sus tropas e intimidan al enemigo."),
        ("Tecnología kaiyu", "Bio-metal, circuitos de plasma y calderos tectónicos; instalaciones que queman la energía del núcleo para abrir las brechas."),
        ("Colapso dimensional", "Abrir muchas brechas a la vez (como en los 14 minutos de El Silencio) fractura el tejido espacial y colapsaría ambas dimensiones, destruyendo la Tierra y Ghar-Máth. Por eso la resistencia actúa desde dentro."),
    ]),
    ("LA LENGUA KAIKORU — FONÉTICA Y ESCRITURA", [
        ("Kaikoru", "Lengua de los kaiyu, «la Lengua de las Rocas Altas». No es conversacional: refleja su masa corporal, sus cámaras de resonancia torácica y la disciplina de un ejército en campaña. En la novela se transcribe con lectura española."),
        ("Emisión acústica", "Los kaiyu carecen de cuerdas vocales humanas; emiten infrasonidos desde cámaras masivas del tórax. Sacuden el suelo y el metal del entorno y pueden dañar el oído humano a corta distancia sin atacar."),
        ("Consonantes duras", "K, G, X, R, Z y Q se producen con el fondo de la garganta o el chasquido seco de mandíbulas y placas óseas; simbolizan el choque de elementos y la violencia del combate."),
        ("Vocales agudas (E, I)", "Raras y restringidas a protocolos de emergencia bélica, activación de bioelectricidad o dolor extremo ante fallas orgánicas."),
        ("Apóstrofo glotal (')", "Marca una interrupción absoluta del flujo de aire: el cierre hermético de una compuerta o un chasquido de mandíbula. Denota disciplina de silencio o autoridad estricta."),
        ("Escritura kaiyu", "Trazos rectos, ángulos afilados y surcos profundos grabados directamente sobre obsidiana, planchas de blindaje o cimientos, con garras o haces de plasma."),
    ]),
    ("LA LENGUA KAIKORU — ALFABETO", [
        ("A (ʌ)", "Vocal abierta de resonancia neutra; eco ambiental en túneles, estado base de la materia."),
        ("E (∤)", "Vocal cortada y aguda (línea fracturada); tensión energética, advertencias de plasma o fallas críticas."),
        ("I (⏚)", "Vocal vibrante vinculada a la agudeza sensorial y a la bioelectricidad en combate."),
        ("O (⬡)", "Vocal cavernosa y prolongada que resuena en las salas de mando; autoridad y espacio profundo."),
        ("U (⊔)", "Sonido prolongado y grave; masa biológica, peso de la corteza y antigüedad milenaria."),
        ("B (⊏)", "Explosiva que imita el choque frontal de placas de blindaje pesado."),
        ("C (⊓)", "K raspada por la fricción de superficies duras en labores de infraestructura."),
        ("D (◿)", "D pesada y seca; pisada de un titán sobre metal."),
        ("F (⎎)", "Exhalación brusca de aire caliente y vapor a presión a través de válvulas respiratorias."),
        ("G (Ϙ)", "Gutural profunda originada en el tórax; designa la fuerza bruta y el territorio."),
        ("H (⨅)", "Aspiración dura y prolongada; advertencia territorial antes del combate."),
        ("J (⟁)", "Fricativa áspera raspada en el paladar superior; comandos de ejecución."),
        ("K (⋕)", "K seca y cortante; impacto directo de una garra o un corte limpio."),
        ("L (⎿)", "Tono grave y sostenido; marca el compás en las marchas largas de infantería."),
        ("M (⎍)", "Zumbido nasal y pectoral de baja frecuencia; mensajes a distancia sin revelar la posición."),
        ("N (⎕)", "Hace vibrar las placas frontales del cráneo al registrar órdenes directas."),
        ("P (⊏)", "Chasquido labial seco por la expulsión repentina de aire comprimido."),
        ("Q (⍚)", "Cavernosa posterior, emitida desde la glotis profunda; reservada a mandos superiores."),
        ("R (⚡)", "Vibrante múltiple continua; gruñido sostenido de una horda en avance."),
        ("S (∿)", "Silbido corto y cortante; presión de vapor, fugas de plasma o sigilo táctico."),
        ("T (⊤)", "Chasquido dentario seco; precisión mecánica o cierre de compuertas."),
        ("V (⋁)", "Vibrante que usa la resonancia de membranas orgánicas."),
        ("W (⍾)", "Ua distorsionada; fricción marina, atmosférica o motores tectónicos."),
        ("X (╳)", "Sonido rudo y compuesto (KS / J); roce de armaduras pesadas en combate cerrado."),
        ("Y (☨)", "Y extendida que transporta resonancia a través de fallas tectónicas lejanas."),
        ("Z (⋞)", "Consonante eléctrica; descargas de plasma o bioelectricidad acumulada."),
        ("' (∣)", "Pausa glotal absoluta que interrumpe de golpe cualquier sonido: el cese de la vida o la disciplina del silencio."),
    ]),
    ("LA LENGUA KAIKORU — GRAMÁTICA Y AFIJOS", [
        ("Sintaxis kaikoru", "Rechaza la perspectiva subjetiva humana: todo se subordina a la función y al impacto material. La fórmula oracional es estricta."),
        ("Sufijo -k'sh", "Acción masiva, destructiva, de purga o avance incontenible de horda."),
        ("Sufijo -ro", "Identifica al emisor directo, oficial ejecutor o combatiente activo con capacidad de decisión."),
        ("Sufijo -uk", "Convierte una unidad singular en colectivo, horda o batallón unificado."),
        ("Sufijo -má (-mʌ)", "Origen, núcleo, matriz biológica o planeta de procedencia."),
        ("Prefijo Kor-", "Exclusivo de la casta gobernante, los altos mandos y el rey tirano (p. ej. Kor'váth)."),
        ("Prefijo Q'-", "Antepuesto a oficiales tácticos y subjefes de vanguardia (p. ej. Q'vár)."),
        ("Prefijo Zuk-", "Depredadores activos en la línea de choque o fuerzas de asalto."),
    ]),
    ("RANGOS Y CLASES MILITARES KAIYU", [
        ("Meritocracia militar", "La sociedad kaiyu se rige por una meritocracia ligada a los colores de peligro y a la función táctica."),
        ("Color de peligro", "El color es una alerta de peligrosidad, no decoración; el cuerpo del enemigo también lo delata. Nunca es amarillo chillón."),
        ("Verde · Exploración (Zár-uk)", "«Los que caminan solos / Vagabundos». Bestias solitarias del tamaño de un perro que cruzan las brechas sin órdenes complejas."),
        ("Azul · Mínimo (Min'vár)", "«Ruido menor / Sombra dispersa». Unidades pequeñas, del tamaño de un gato, que se camuflan en el caos del combate."),
        ("Amarillo · Línea (Ghar-t'rok)", "«Soldados de la marcha principal». Los cinco arquetipos de infantería, del tamaño de un caballo."),
        ("Naranja · Choque (X'vár-ro)", "«Brechadores del frente / Rompedores». Los seis subjefes de demolición táctica, del tamaño de un camión."),
        ("Rojo · Oficiales (Kor-zá)", "«Los que deciden la sangre». Los seis oficiales superiores con autonomía y juicio propio, del tamaño de un edificio pequeño."),
        ("Negro · Mando (Kor'váth-má)", "«El Trono y la Ley del Abismo». Los seis administradores supremos, mayores que un edificio, que dirigen la oleada global y el papeleo de la invasión."),
    ]),
    ("LOS CINCO ARQUETIPOS (AMARILLO)", [
        ("Carrilero", "Largo y bajo; corre en línea recta. Embiste sin frenar."),
        ("Embestidor", "Hombro grande, cabeza hundida y cuello casi nulo. Ataca con una embestida de hombro."),
        ("Lanzador", "Vertical, de brazos largos y sin cuello visible. Lanza desde lejos."),
        ("Blindado", "Cuadrado, con placas y sin cuello. No se mueve: hay que rodearlo."),
        ("Resucitado", "Encorvado, con un cuerpo humano debajo. Se levanta, vuelve a caerse y vuelve a levantarse."),
    ]),
    ("LOS SEIS SUBJEFES (NARANJA)", [
        ("Portero Encabezado", "Una puerta con patas. Camina lento. Es el primero de los grandes, el jefe del sector en el cap. 21."),
        ("Caldera", "Redondo, partido en dos mitades, humea."),
        ("Pry", "Alto y delgado, con muchos miembros."),
        ("Mirage", "No se ve; solo se ve el suelo donde va a aparecer."),
        ("Sombra larga", "Horizontal, pegada al suelo, sin patas."),
        ("Hielo negro", "Translúcido; se ve a través de él y no está donde parece."),
    ]),
    ("LOS SEIS JEFES (ROJO)", [
        ("Portero", "Un Portero Encabezado gigante; la primera vez se ve de frente. Junto al Portero Encabezado, es de los dos primeros grandes: uno prueba, el otro rompe."),
        ("Fuente", "Se abre y brota agua de una grieta."),
        ("Nido", "Múltiples, del tamaño de un nido; se mueven en grupo."),
        ("Asesor", "Racional; camina como una persona y habla con los suyos. Es el importante de la temporada 1 y el único que se detiene a mirar antes de decidir. Su primer sonido es «K'vár-uk» (cap. 24)."),
        ("Cenicero", "Sucio; deja ceniza y todo lo que toca se vuelve gris."),
        ("Anclaje", "No se mueve: es un punto fijo alrededor del cual se organiza la oleada."),
    ]),
    ("LOS SEIS ESCALONES NEGROS (NEGRO)", [
        ("Núcleo", "El más grande; va al fondo de la formación."),
        ("Archivista", "Recoge cosas; en la temporada 2 se ve que recoge documentos."),
        ("Asesor mayor", "Habla por los negros."),
        ("Fuente madre", "Por donde sale lo que no tiene forma."),
        ("Cenicero mayor", "Su zona se vuelve gris para siempre."),
        ("Anclaje madre", "El centro de la red."),
    ]),
    ("REGLAS DE LOS KAIYU Y LOS DE CUERPO HUMANO", [
        ("Reglas fijas de los kaiyu", "Vuelven enteros (no se queman); son feos y visibles (nadie puede disfrazarse de persona); no producen sonido propio (hay que turnarse para verlos); no hablan japonés; los de cuerpo humano se detienen a mirar."),
        ("Los de cuerpo humano", "Están repartidos por todos los colores, del verde al negro. No se distinguen por el color sino por la conducta: quien se detiene a mirar a un niño todavía recuerda; quien ataca a un vehículo y no a una persona es táctico; quien ataca a una persona primero ya no recuerda."),
        ("Anomalía de la memoria", "Los kaiyu de cuerpo humano o de mando avanzado (como el Asesor rojo o Vrak'thul) dudan o se detienen ante los niños porque conservan fragmentos de memoria y empatía de antes del colapso de su mundo."),
        ("Las cuatro siluetas (cap. 6)", "Lo que sale del edificio no son cuatro kaiyu, sino cuatro personas con un cuerpo encima; caminan como caminan las personas."),
        ("Diseño visual del kaiyu", "Silueta distinta por arquetipo; color de peligro en una parte del cuerpo, no en todo; doble borde en los enemigos grandes; el fondo nunca compite en contraste con el enemigo."),
        ("Amenazas de la temporada 1", "Entre 15 y 18 en total: 9-10 amarillas, 3 naranjas, 2 rojas y 1 omega."),
    ]),
    ("POLÍTICA, COLONIZACIÓN Y LA FACCIÓN REBELDE", [
        ("Colonización kaiyu", "La invasión de la Tierra no es un ataque por hambre de guerra: es un plan de colonización y migración forzada. Su mundo se muere y buscan asegurar la supervivencia de la especie. La conquista es el medio; la colonización es el fin."),
        ("Guerra civil kaiyu", "Una guerra interna enfrenta al régimen del rey tirano con un ejército de rebeldes."),
        ("La Sombra del Núcleo (Vár-Kor'váth)", "Facción rebelde kaiyu que rechaza la colonización destructiva de la Tierra y busca derrocar al rey tirano. La dirige Vrak'thul el Roto."),
        ("Vrak'thul el Roto", "Líder rebelde y prisionero que se deja capturar a propósito en la temporada 2. Más humanoide que su raza, con mandíbula fragmentada y cicatrices de plasma; aprende el idioma humano y revela la verdad para buscar una alianza con la OIDA y la NSF."),
        ("Células rebeldes", "Los Ojos del Abismo (informantes), los Rompedores de Cadenas (saboteadores de calderos) y el Consejo de Cicatrices (veteranos de guerra)."),
        ("Las Catacumbas de Óxido", "Refugios rebeldes en el Min-Rok profundo, donde la radiación crea sombras magnéticas invisibles a los sensores del Mando."),
        ("Estética rebelde", "Placas de metal arrancadas y remachadas a mano, marcadas con una línea vertical de ácido industrial; Vrak'thul viste harapos de lona industrial calcinada."),
    ]),
    ("FRASES EN KAIKORU", [
        ("K'vár-uk", "Pron. «K-vár-uk». «Aún recuerdo.» Primer sonido del Asesor (cap. 24, oficial rojo)."),
        ("Rok'má O-m'rok-k'sh… Zuk-ro k'zárr", "Pron. «Rok-má O-m-rok-kósh… Zuk-ro k-zarr». «Nuestro mundo agoniza… El Rey Tirano consume todo.» Testimonio del prisionero ante la OIDA."),
        ("T'rok-uk k'zárr-k'sh vár-má", "Pron. «T-rok-uk k-zarr-kósh var-má». «No venimos por guerra; venimos a colonizar su hogar.»"),
        ("Ghar-uk ráz-k'sh Kor'váth", "Pron. «Gar-uk rash-kósh Kor-váth». «El Mando reclamará la frontera.» Grito de mando de los Escalones Negros."),
        ("Q'vár-ro Gah! Zuk-uk mák-k'sh… Ghar-uk ráz!", "Pron. «Q-vár-ro Gah! Zuk-uk mak-kósh… Gar-uk rash!». «¡Atención, oficiales del frente! La horda de choque avanza… ¡Aplasten el sector!» Frecuencia táctica interceptada por la NSF."),
        ("O-vur kósh", "Pron. «O-vur kósh». «El vacío crece.» Se lo dice Vrak'thul a Rika en el cap. 55."),
    ]),
    ("LUGARES DE LA NOVELA", [
        ("Yokohama", "Ciudad portuaria de la prefectura de Kanagawa, al sur de Tokio (región de Kantō). Aquí arranca la historia y aquí está la base de la NSF."),
        ("Oyama", "Barrio del norte de Yokohama (frente centro). En él está la guardería donde la oleada ataca y donde se concentra el arco de Mio."),
        ("Guardería de Oyama", "Guardería del norte de Yokohama; al llegar la oleada quedan allí 47 niños y 13 adultos (cap. 60). Es el centro del arco de Mio."),
        ("Tokio", "Capital de Japón; sede del Estado Mayor y del mando de la operación. En su sala de planificación está el mapa de los catorce ataques (cap. 62)."),
        ("Tokukan", "Empresa privada de manejo de ambientes especiales, con archivo de planos en Yokohama; participó en la medición y contención de las puertas (cap. 55)."),
        ("Usui", "Paso de montaña entre Nagano y Gunma; «un codo de tierra que no vale nada» (cap. 53)."),
        ("Kiso", "Valle estrecho del suroeste de Nagano. Su municipalidad, convertida en refugio, guarda a 140 personas (cap. 59)."),
        ("Narai", "Antiguo pueblo de posta del valle de Kiso (Nagano), sobre la ruta Nakasendō; en el cap. 63 no ocurre nada."),
        ("Ueda", "Ciudad del este de Nagano; sede de un hospital de campaña atacado a propósito por los kaiyu (cap. 62)."),
        ("Matsumoto", "Ciudad de la prefectura de Nagano (región de Chūbu), frente centro; 180.000 habitantes. Cae en el cap. 71, «la ciudad gris»."),
        ("Azumino", "Llanura y valle alto de Nagano, junto a Matsumoto; frente centro (caps. 72-73)."),
        ("Omachi", "Ciudad del norte de Nagano, a los pies de los Alpes del Norte; se pierde en el cap. 73."),
        ("Hakuba", "Pueblo de los Alpes del Norte (Nagano), cerca de Omachi; se pierde en el cap. 73."),
        ("Norikura", "Monte y altiplano en el límite de Nagano y Gifu; frente centro al final de la temporada 3 (caps. 75, 92-95)."),
        ("Suwa", "Ciudad y lago del centro de Nagano; primer sitio donde aparece un negro con una oleada (cap. 65)."),
        ("Ina", "Llanura y valle del sur de Nagano; hacia allí avanza la oleada del cap. 66."),
        ("Misawa", "Ciudad y base aérea de la prefectura de Aomori (región de Tōhoku); frente norte (cap. 58)."),
        ("Tanzawa", "Cordillera montañosa al oeste de la prefectura de Kanagawa; frente capital en la temporada 4."),
        ("Miyagase", "Zona de montaña y lago en las colinas de Tanzawa (Kanagawa); escenario donde los cuatro quedan rodeados (caps. 82-85)."),
        ("Carretera 45 (Ruta Nacional 45)", "Carretera costera del Pacífico que cruza Miyagi y Aomori, en la región de Tōhoku."),
        ("Ward Noveno", "Recinto de la costa de Kantō donde el tiempo se separó en capas tras el Silencio (cap. 50). Mio Tsukimi sigue atrapada en su bucle, en el mismo segundo, desde hace nueve años."),
        ("Frentes", "Los sectores en que se organiza la defensa de Japón: capital (Kantō), centro (Nagano), norte (Tōhoku) y sur."),
    ]),
    ("CONCEPTOS Y OBJETOS DE LA NOVELA", [
        ("Apertura", "Fenómeno que conecta el mundo humano con Ghar-Máth a través de las puertas. También llamado Silencio."),
        ("Brecha", "Cada una de las aberturas. Se clasifican por categoría; una «brecha principal» es la de mayor tamaño."),
        ("Puerta", "Cada brecha, una vez estabilizada. Hay catorce puertas principales (igual que los catorce minutos del Silencio), siete de servicio y cuatro que no figuran en ningún catálogo porque las construyeron quienes no firmaban planos. Las catorce forman una sola puerta grande."),
        ("El Silencio", "La primera Apertura: catorce minutos exactos, de 04:58 a 05:12, del 15 de mayo de 2008. Un segundo Silencio ocurre el 15 de mayo de 2017 (cap. 1)."),
        ("Oleada", "La marea de kaiyu que avanza sobre un sector."),
        ("Catálogo", "El registro de amenazas de la invasión kaiyu. No tiene casilla para una persona: por eso la omega no figura en él."),
        ("Legajo", "El archivo de trece páginas del Estado Mayor; se abre en los caps. 49-50 y contiene, entre otras cosas, la orden de no avisar. La temporada 4 revela el legajo entero."),
        ("Los catorce ataques", "Los catorce sitios donde la oleada atacó civiles a propósito en el último mes (cap. 62). Todos en brechas de categoría dos y ninguno donde estaba desplegada la OIDA."),
        ("Portador", "Humano con una apertura alojada en el cuerpo. Escala de rangos: E, D, C, B, A y S."),
        ("Corte de Un Destello", "El poder de Rika. Corta un bucle (cap. 25) y con él saca a Mio sin matarla."),
        ("La Hoja", "El poder de corte de Rika; deja una estela."),
        ("El Yunque", "El poder de Goro: la brasa y el cono de fuego. Si no controla la descarga, quema a quien tenga cerca."),
        ("El Relámpago", "El poder de velocidad de Ren; tres cargas o estelas, de color amarillo. Se agota."),
        ("La Distancia", "El poder de largo alcance de Yui: ondas concéntricas y un rifle con mira telescópica."),
        ("Operador de puerta", "Personal que abre y cierra las puertas a mano; varios mueren en la tarea (caps. 67 y 99)."),
        ("Estado Mayor", "El mando militar japonés. Conocía la verdad sobre la omega desde antes del Silencio."),
        ("Base NSF", "La base de la Fuerza de Defensa Nacional en Yokohama; cuartel y punto de partida de los cuatro."),
    ]),
    ("LOS CUATRO PROTAGONISTAS", [
        ("Tsukimi Rika — La Hoja", "24 años (15 el día 1); 158 cm. Líder de la unidad. Su dash atraviesa a los enemigos y los daña, y se alimenta de la actividad: cuantas más bajas hace, más móvil es. Aprende a anticiparse: el cuerpo se mueve antes que la cabeza. Ruptura: Corte de Un Destello. Ancla: su madre, Shino; sin ella deja de anticipar. Su arco: nueve años entrenando un corte para salvar a su hermana Mio, no matarla."),
        ("Arashi Goro — El Yunque", "41 años (32 el día 1); 195 cm; guardia del Sector 6 del Ward. Su poder aguanta: una carga de dash tres veces más larga que las demás y un escudo industrial. Desarrolla la brasa del guante, un vapor radioactivo que quema a quien tenga cerca cuando pierde el control. Ruptura: Golpe de Yunque. Ancla: su vecino Tsumita Kosuke. Cumplió una orden que sabía que era mentira."),
        ("Hayashi Ren — El Relámpago", "25 años cronológicos, 19 aparentes; estudiante. Su poder es la velocidad: tres cargas de dash que nunca se agotan. Aprende a moverse entre huecos, no entre espacios sino entre momentos. Ruptura: Carga Relámpago. Ancla: quien lo espera en casa. Su arco: entró con 16, caminó por la fractura durante años y volvió con 19 sin recordarlo."),
        ("Nakamura Yui — La Distancia", "31 años (22 el día 1); 172 cm; médica del hospital de la frontera del Ward. Su poder es la distancia: un teletransporte corto y un rifle de cerrojo con mira telescópica. Aprende a oír el silencio tres segundos antes. Ruptura: Reverberación, ondas que cortan lo que se repite. Ancla: su cuaderno. Su arco: nunca supo si hizo bien en no dejar pasar a alguien. Interés amoroso: Amano Rei."),
    ]),
    ("PERSONAJES SECUNDARIOS", [
        ("Kurose Ken", "52 años; director de contención de la NSF. Redactó y firmó la orden de no avisar (el Legajo de trece páginas). Sabe de la omega desde el día 3 y no dice nada."),
        ("Watanabe Raishiro", "54 años; general y gobernador de la base. No tiene poder: manda por oficio. Recibió la orden de no avisar y no puede contestar por qué no se evacuó Yokohama (cap. 99)."),
        ("Amano Rei", "22 años; limpieza de la unidad, la que reparte el café. Interés amoroso de Yui; ve a los cuatro desde detrás del cristal en el cap. 25."),
        ("Tsumita Kosuke", "63 años; el vecino de Goro en el bloque de trabajadores del Ward. Cocina y le lleva comida; es el ancla de Goro."),
        ("Tsukimi Shino", "47 años; madre de Rika y de Mio. Es el ancla de Rika."),
        ("Mio Tsukimi", "19 años; hermana de Rika. Entró al Ward y no salió: sigue en el mismo segundo desde hace nueve años. Es la omega. No envejece ni habla."),
        ("Mitamura Setsuko", "74 años; vendedora de verdura. La primera civil que muere (cap. 3)."),
        ("Nomura Tatsuo", "49 años; trabajador de Tokukan que custodiaba puertas con Goro. Goro lo quema con su descarga en el cap. 5."),
        ("Kawano Shinichi", "38 años; sale del metro. Es al que los cuatro no pueden salvar."),
        ("Jumoji Tsuyoshi", "36 años; enfermero. Le cose el antebrazo a Rika (cap. 16)."),
        ("Tokura Jun", "41 años; jefe de limpieza. El primero que entra, el último que sale."),
        ("Kiryu Ryo", "30 años; operador de puerta. Trabaja con Goro."),
        ("Kobayashi Kotaro", "27 años; operador de puerta. El primero que intenta cerrar una y no puede."),
        ("Futaki Saeri", "24 años; auxiliar de archivo. La que escribe."),
        ("Hayakawa Saya", "31 años; piloto de helicóptero. Vuela tres veces ese día."),
        ("Aoki Ryuichi", "58 años; tendero. Comenta el clima y el precio del pescado."),
        ("Takanashi Tokuzo", "71 años; el de siempre en la esquina. No habla, solo está."),
        ("Miura Daigo", "35 años; capitán de la 3.ª Compañía de Tanques. No sabe qué son los kaiyu."),
        ("Shinozuka Ryo", "29 años; sargento de comunicaciones. Es el que dice «no se ve nada»."),
        ("Oda Sara", "26 años; con un niño pequeño. Se separan."),
        ("Sato y Junko", "El matrimonio del arranque del cap. 1: él deja el té a medias y no consiguen salir del edificio."),
        ("Kenji", "21 años; empleado del konbini de la esquina en el cap. 1. Sobrevive al primer kaiyu escondiéndose tras el mostrador."),
        ("Shiraishi", "El jefe del konbini en el cap. 1; sale de la trastienda con una escoba y no sobrevive."),
        ("Los que no tienen nombre", "Civiles del cap. 3, soldados de a pie, el resto de limpieza y enfermería, los operadores de puerta del fondo. Regla: se nombra a alguien solo si habla más de cinco líneas o si muere."),
    ]),
    ("ORGANIZACIONES Y GRUPOS", [
        ("NSF", "Fuerza de Defensa Nacional del Japón. El ejército al que pertenecen los cuatro y desde el que opera la contención en Yokohama."),
        ("OIDA", "Organización Internacional de Defensa contra las Aperturas. Coalición internacional formada tras el segundo Silencio; acuden Corea y Reino Unido. Se despliega en los frentes principales."),
        ("Tokukan", "Empresa privada de manejo de ambientes especiales, con archivo de planos en Yokohama. Construyó y midió las puertas: el contrato original hablaba de registrar, no de cerrar."),
        ("Estado Mayor", "El mando militar japonés. Aprobó la orden de no avisar y conocía la verdad sobre la omega desde antes del Silencio."),
        ("La unidad", "El equipo de los cuatro (Rika, Goro, Ren y Yui) con su equipo de limpieza y enfermería."),
        ("Equipo de limpieza", "Personal de apoyo de la unidad; entre ellos Amano Rei y Tokura Jun."),
        ("Sector 6 del Ward", "Zona del Ward cuya puerta de servicio custodiaba Goro; es la puerta que él selló la mañana del Silencio."),
    ]),
    ("PERSONAJES, ORGANIZACIONES Y TÉRMINOS", [
        ("Amano Rei", "Miembro del equipo de limpieza de la unidad; presencia recurrente en la base."),
        ("Anclaje", "Uno de los seis jefes rojos kaiyu. Su categoría de mando es la que sostiene las puertas."),
        ("Anclaje madre", "Uno de los seis Escalones Negros; versión superior del Anclaje."),
        ("Apertura", "Fenómeno que conecta el mundo humano con Ghar-Máth a través de las puertas. También llamado Silencio."),
        ("Arashi Goro", "«El Yunque». Portador de fuerza bruta de la unidad de Rika."),
        ("Archivista", "Uno de los seis Escalones Negros; guarda el registro de cada oleada."),
        ("Cenicero", "Uno de los seis jefes rojos kaiyu."),
        ("Cenicero mayor", "Uno de los seis Escalones Negros; versión superior del Cenicero."),
        ("Escalones Negros", "Los seis administradores de mando negro kaiyu, por encima de jefes y subjefes."),
        ("Ghar-Máth", "Planeta de origen de los kaiyu; gobernado por el rey tirano Kor'váth."),
        ("Gar-t-rok", "Rango de los kaiyu amarillos; depredadores de choque."),
        ("Hayashi Ren", "«El Relámpago». Portador de velocidad de la unidad de Rika."),
        ("Kaikoru", "Lengua de los kaiyu, transcrita con lectura española para el lector."),
        ("Kaiyu", "Nombre genérico de los enemigos; cada color equivale a un rango de combate."),
        ("Kor'váth", "Rey tirano de Ghar-Máth; origen de la oleada."),
        ("Kor-váth-má", "Rango de los kaiyu negros; mando máximo de una oleada."),
        ("Kor-zá", "Rango de los kaiyu rojos; jefes."),
        ("Kurose Ken", "Oficial de la NSF que conoce la verdad sobre la omega."),
        ("Min-vár", "Rango de los kaiyu azules."),
        ("Mio Tsukimi", "Hermana de Rika, atrapada al otro lado desde el primer Silencio. No envejece ni habla."),
        ("Nakamura Yui", "«La Distancia». Portadora de largo alcance de la unidad de Rika."),
        ("NSF", "Fuerza de Defensa Nacional del Japón."),
        ("Núcleo", "Uno de los seis Escalones Negros; núcleo de mando de la oleada."),
        ("OIDA", "Organización Internacional de Defensa contra las Aperturas."),
        ("Omega", "Categoría reservada. Mio Tsukimi es la omega; no figura en el catálogo."),
        ("Portador", "Humano con una apertura alojada en el cuerpo. Escala de rangos: E, D, C, B, A y S."),
        ("Silencio", "Nombre con que la población recuerda la primera Apertura (15 de mayo de 2008)."),
        ("Tokukan", "Empresa privada de manejo de ambientes especiales; empleada en las labores de contención."),
        ("Tsukimi Rika", "«La Hoja». Protagonista y líder de la unidad."),
        ("Vrak'thul", "Kaiyu prisionero que revela la verdad sobre Ghar-Máth y la oleada."),
        ("X-vár-ro", "Rango de los kaiyu naranjas; subjefes."),
        ("Zar-uk", "Rango de los kaiyu verdes; tropa de choque."),
    ]),
]

def build_glossary_block():
    out = [page_break_xml(),
           '<w:p><w:pPr><w:pStyle w:val="GlosTitle"/></w:pPr>'
           '<w:bookmarkStart w:id="2000" w:name="_Toc_apendices"/>'
           '<w:r><w:t>APÉNDICES</w:t></w:r>'
           '<w:bookmarkEnd w:id="2000"/></w:p>']
    out.append(style_para("GlosTitle", "GLOSARIO"))
    for section, entries in GLOSARIO:
        out.append(style_para("GlosSection", section))
        for term, definition in entries:
            out.append(glossary_para(term, definition))
    return "".join(out)

def build_document_body(caps):
    global IMAGES
    IMAGES = []
    HREF = ''
    out = []
    # --- Portada (foto) a sangre, seccion con margenes 0 ---
    # El corte de seccion va DENTRO del parrafo de la imagen (sin parrafo vacio
    # extra) para que no se genere una pagina en blanco entre portada y titulo.
    if COVER:
        sect_cover = ('<w:sectPr>' + HREF + '<w:pgSz w:w="11906" w:h="16838"/>'
                      '<w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>'
                      '</w:sectPr>')
        out.append(cover_drawing_xml(sect_cover))
    # --- Titulo (fondo + texto JUNTOS en la pagina 2) ---
    if TITLE_BG:
        out.append(bg_anchor_xml(PAGE_W_EMU, PAGE_H_EMU, "rId4"))
    out.append('<w:p><w:pPr><w:spacing w:before="2000"/></w:pPr></w:p>')
    if TITLE_IMG:
        out.append(title_img_xml())
        out.append('<w:p><w:pPr><w:spacing w:after="1200"/></w:pPr></w:p>')
    else:
        out.append(p_xml("title", TITULO))
        out.append(p_xml("sub", SUBTITULO))
        out.append('<w:p><w:pPr><w:spacing w:after="1200"/></w:pPr></w:p>')
    out.append(p_xml("serie", SERIE))
    out.append(p_xml("author", "Autor: " + AUTOR))
    # cierra la seccion del titulo (margenes 0: el fondo/foto van a sangre).
    # pgNumType start=1: la numeracion arranca en la pagina de autor (la portada
    # no se numera). footerReference: muestra el numero en esa primera pagina.
    out.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="0" w:lineRule="exact"/>'
               '<w:sectPr>' + HREF
               + '<w:footerReference w:type="default" r:id="rId2"/>'
               + '<w:footerReference w:type="even" r:id="rId2"/>'
               + '<w:pgSz w:w="11906" w:h="16838"/>'
               + '<w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="720" w:gutter="0"/>'
               + '<w:pgNumType w:start="1"/>'
               + '</w:sectPr></w:pPr></w:p>')
    # --- Índice (arranca en pagina nueva tras la pagina de titulo/autor) ---
    out.append(build_index_block(caps))
    for i, c in enumerate(caps, 1):
        title, text = parse_chapter(c)
        n = re.match(r"^CAPÍTULO\s+(\d+)", title, re.I)
        num = n.group(1) if n else str(i)
        # Salto de página EXPLÍCITO (w:br) al final del párrafo anterior:
        # w:pageBreakBefore lo ignoran Google Docs y varios visores móviles,
        # de ahí que los encabezados se "fueran" a otras páginas.
        # El capítulo 1 ya no arranca del corte de sección: ahora el índice va
        # delante, así que TODOS los capítulos llevan salto de página.
        j = len(out) - 1
        while j >= 0 and not out[j].endswith("</w:p>"):
            j -= 1
        if j >= 0:
            out[j] = out[j][:-len("</w:p>")] + '<w:r><w:br w:type="page"/></w:r></w:p>'
        brk = '<w:keepNext/><w:keepLines/>'
        tight = (i == len(caps))
        tsp = '<w:spacing w:after="240"/>' if tight else ''
        chap_title = "Capítulo " + num + " — " + title.split("—", 1)[-1].strip().strip('"')
        bid = 1000 + (int(num) if num.isdigit() else i)
        out.append('<w:p><w:pPr><w:pStyle w:val="CapTitle"/>' + brk + tsp + '</w:pPr>'
                   '<w:bookmarkStart w:id="' + str(bid) + '" w:name="_Toc_cap' + num + '"/>'
                   '<w:r><w:t>' + esc(chap_title) + '</w:t></w:r>'
                   '<w:bookmarkEnd w:id="' + str(bid) + '"/></w:p>')
        for kind, tk in paras_from_text(text):
            if kind == "normal" and tk.endswith("*"):
                out.append(p_xml("scene", tk, tight=tight))
            elif kind == "normal" and tk.startswith("**"):
                out.append(p_xml("center", tk.strip("*"), tight=tight))
            else:
                out.append(p_xml(kind, tk, tight=tight))
    # --- Apéndices y glosario (final del libro) ---
    out.append(build_glossary_block())
    return "".join(out)

def build_xml():
    caps = load_chapters()
    body = build_document_body(caps)
    return body, len(caps)

# ---------------- Estilos usados ----------------
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif" w:eastAsia="DejaVu Serif" w:cs="DejaVu Serif"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="es-ES"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:widowControl/><w:spacing w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Novela"><w:name w:val="Novela"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:line="360" w:lineRule="auto" w:after="120"/><w:ind w:firstLine="480"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="CapTitle"><w:name w:val="CapTitle"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="1440" w:after="480" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="B5701F"/><w:u w:val="single"/><w:sz w:val="38"/><w:szCs w:val="38"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="88"/><w:szCs w:val="88"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="44"/><w:szCs w:val="44"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Author"><w:name w:val="Author"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="24386E"/><w:u w:val="single"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="SerieTag"><w:name w:val="SerieTag"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="SceneTag"><w:name w:val="SceneTag"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="120"/></w:pPr><w:rPr><w:i/><w:color w:val="595959"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="160"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif"/><w:i/><w:color w:val="7F7F7F"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BodyEmpty"><w:name w:val="BodyEmpty"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:line="0" w:after="0"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="IndexTitle"><w:name w:val="IndexTitle"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="400" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="B5701F"/><w:u w:val="single"/><w:sz w:val="38"/><w:szCs w:val="38"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="IndexEntry"><w:name w:val="IndexEntry"/><w:basedOn w:val="Normal"/><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8787"/></w:tabs><w:spacing w:line="300" w:lineRule="auto" w:after="80"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="GlosTitle"><w:name w:val="GlosTitle"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="400" w:after="300" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="B5701F"/><w:u w:val="single"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="GlosTerm"><w:name w:val="GlosTerm"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="40" w:line="300" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="GlosDef"><w:name w:val="GlosDef"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="GlosSection"><w:name w:val="GlosSection"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="360" w:after="160" w:line="320" w:lineRule="auto"/><w:keepNext/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="B5701F"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
</w:styles>"""

FONT_REG = "/data/data/com.termux/files/usr/share/fonts/TTF"
FONT_TABLE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:font w:name="DejaVu Serif"><w:family w:val="roman"/>
<w:embedRegular r:id="rIdF1"/><w:embedBold r:id="rIdF2"/><w:embedItalic r:id="rIdF3"/>
</w:font>
<w:font w:name="DejaVu Sans"><w:family w:val="swiss"/>
<w:embedRegular r:id="rIdF4"/><w:embedBold r:id="rIdF5"/>
</w:font>
</w:fonts>"""

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="ttf" ContentType="application/x-font-ttf"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

def doc_rels_xml(img_ext, bg_ext=None):
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>\n'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>\n'
            '<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>\n'
            '<Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header2.xml"/>\n'
            '<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>\n'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.' + img_ext + '"/>\n')
    if bg_ext:
        rels += ('<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image2.' + bg_ext + '"/>\n')
    if TITLE_IMG:
        rels += ('<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image3.png"/>\n')
    for i, (p, rid, media) in enumerate(IMAGES):
        rels += ('<Relationship Id="' + rid + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/' + media + '"/>\n')
    rels += ('<Relationship Id="rIdF1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/DejaVuSerif.ttf"/>\n'
             '<Relationship Id="rIdF2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/DejaVuSerif-Bold.ttf"/>\n'
             '<Relationship Id="rIdF3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/DejaVuSerif-Italic.ttf"/>\n'
             '<Relationship Id="rIdF4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/DejaVuSans.ttf"/>\n'
             '<Relationship Id="rIdF5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/DejaVuSans-Bold.ttf"/>\n')
    rels += '</Relationships>'
    return rels

def footer_xml():
    marca = esc(TITULO + " · NPAD")
    rpr = ('<w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>'
           '<w:i/><w:color w:val="A6A6A6"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    rpr_page = ('<w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>'
                '<w:color w:val="7F7F7F"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"\n'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
            '<w:p><w:pPr><w:jc w:val="center"/>' + rpr + '</w:pPr>'
            '<w:r>' + rpr + '<w:t xml:space="preserve">' + marca + '</w:t></w:r>\n'
            '</w:p>\n'
            '<w:p><w:pPr><w:jc w:val="center"/>' + rpr_page + '</w:pPr>'
            '<w:r>' + rpr_page + '<w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r>' + rpr_page + '<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            '<w:r>' + rpr_page + '<w:fldChar w:fldCharType="end"/></w:r>'
            '</w:p>\n'
            '</w:ftr>')

def header_xml(text=None, align="center"):
    if text is None:
        text = AUTOR
    rpr = ('<w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>'
           '<w:i/><w:color w:val="7F7F7F"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:p><w:pPr><w:jc w:val=\"""" + align + """\"/>""" + rpr + """</w:pPr>
<w:r>""" + rpr + """<w:t xml:space="preserve">""" + esc(text) + """</w:t></w:r>
</w:p></w:hdr>"""

def header_odd_xml():
    return header_xml(TITULO, "right")

def header_even_xml():
    return header_xml(AUTOR, "left")

def settings_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:zoom w:percent="100"/>
<w:mirrorMargins/>
<w:defaultTabStop w:val="708"/>
<w:evenAndOddHeaders/>
<w:updateFields w:val="true"/>
<w:compat>
<w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
</w:compat>
</w:settings>"""

def main():
    body, ncaps = build_xml()
    final_header = ''
    now = datetime.datetime.utcnow().isoformat() + "Z"
    result = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<w:body>
{body}
 <w:sectPr>
 {final_header}
 <w:headerReference w:type="default" r:id="rId6"/>
 <w:headerReference w:type="even" r:id="rId8"/>
 <w:footerReference w:type="default" r:id="rId2"/>
 <w:footerReference w:type="even" r:id="rId2"/>
 <w:pgSz w:w="11906" w:h="16838"/>
 <w:pgMar w:top="1440" w:right="1418" w:bottom="1531" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>
 </w:sectPr>
</w:body></w:document>""".format(body=body, final_header=final_header)
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>""" + esc(TITULO) + """</dc:title>
<dc:creator>""" + esc(AUTOR) + """</dc:creator>
<cp:lastModifiedBy>""" + esc(AUTOR) + """</cp:lastModifiedBy>
<dc:language>es-ES</dc:language>
<dcterms:created xsi:type="dcterms:W3CDTF">""" + now + """</dcterms:created>
<cp:revision>1</cp:revision></cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>opencode NPAD novel builder</Application></Properties>"""
    img_ext = "jpg"
    bg_ext = None
    if COVER:
        img_ext = COVER[1]
    if TITLE_BG:
        bg_ext = TITLE_BG[1]
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", result)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/fontTable.xml", FONT_TABLE)
        z.writestr("word/_rels/document.xml.rels", doc_rels_xml(img_ext, bg_ext))
        z.writestr("word/footer1.xml", footer_xml())
        z.writestr("word/header1.xml", header_odd_xml())
        z.writestr("word/header2.xml", header_even_xml())
        z.writestr("word/settings.xml", settings_xml())
        if COVER:
            z.write(COVER[0], "word/media/image1." + img_ext)
        if TITLE_BG:
            z.write(TITLE_BG[0], "word/media/image2." + bg_ext)
        if TITLE_IMG:
            z.write(TITLE_IMG, "word/media/image3.png")
        for p, rid, media in IMAGES:
            z.write(p, "word/media/" + media)
        for fn in ("DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSerif-Italic.ttf",
                   "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
            z.write(os.path.join(FONT_REG, fn), "word/fonts/" + fn)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
    print("OK -> " + OUT + "  (" + str(ncaps) + " capitulos)")

if __name__ == "__main__":
    main()