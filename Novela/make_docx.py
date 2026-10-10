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
SERIE = "TEMPORADA 1 · CAPÍTULOS 1 A 200"

COVER = None
for cand in ("portada.png", "portada.jpg", "portada.jpeg"):
    p = os.path.join(BASE, cand)
    if os.path.exists(p):
        COVER = (p, cand.split(".")[-1])
        break

TITLE_BG = None
for cand in ("titulo.png", "titulo.jpg"):
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

def cover_drawing_xml():
    cx, cy = cover_emu()
    return ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0"/></w:pPr>'
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
        else:
            for lp in block.split("\n"):
                lp = lp.strip()
                if lp:
                    paras.append(("normal", lp))
    return paras

def p_xml(kind, text, first=""):
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
        return ('<w:p><w:pPr><w:pStyle w:val="SceneTag"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    if kind == "center":
        return ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>')
    ppr = '<w:pPr><w:pStyle w:val="Novela"/>' + first + '</w:pPr>'
    return '<w:p>' + ppr + '<w:r><w:t>' + esc(text) + '</w:t></w:r></w:p>'

def build_document_body(caps):
    global IMAGES
    IMAGES = []
    HREF = ''
    out = []
    # --- Portada (foto) a sangre, seccion con margenes 0 ---
    if COVER:
        out.append(cover_drawing_xml())
        out.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="0" w:lineRule="exact"/>'
                   '<w:sectPr>' + HREF + '<w:pgSz w:w="11906" w:h="16838"/>'
                   '<w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>'
                   '</w:sectPr></w:pPr></w:p>')
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
    # cierra la seccion del titulo (sigue con margenes 0 y sin pie)
    out.append('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="0" w:lineRule="exact"/>'
               '<w:sectPr>' + HREF + '<w:pgSz w:w="11906" w:h="16838"/>'
               '<w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>'
               '</w:sectPr></w:pPr></w:p>')
    for i, c in enumerate(caps, 1):
        title, text = parse_chapter(c)
        n = re.match(r"^CAPÍTULO\s+(\d+)", title, re.I)
        num = n.group(1) if n else str(i)
        # Salto de página EXPLÍCITO (w:br) al final del párrafo anterior:
        # w:pageBreakBefore lo ignoran Google Docs y varios visores móviles,
        # de ahí que los encabezados se "fueran" a otras páginas.
        # El capítulo 1 no lleva salto: ya arranca tras el corte de sección
        # de la página de título (sectPr nextPage).
        if i > 1:
            j = len(out) - 1
            while j >= 0 and not out[j].endswith("</w:p>"):
                j -= 1
            if j >= 0:
                out[j] = out[j][:-len("</w:p>")] + '<w:r><w:br w:type="page"/></w:r></w:p>'
        brk = '<w:keepNext/><w:keepLines/>'
        out.append(p_xml("chapter", "Capítulo " + num + " — " + title.split("—", 1)[-1].strip().strip('"'), brk))
        for kind, tk in paras_from_text(text):
            if kind == "normal" and tk.endswith("*"):
                out.append(p_xml("scene", tk))
            elif kind == "normal" and tk.startswith("**"):
                out.append(p_xml("center", tk.strip("*")))
            else:
                out.append(p_xml(kind, tk))
    return "".join(out)

def build_xml():
    caps = load_chapters()
    body = build_document_body(caps)
    return body, len(caps)

# ---------------- Estilos usados ----------------
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif" w:eastAsia="DejaVu Serif" w:cs="DejaVu Serif"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="es-ES"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Novela"><w:name w:val="Novela"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:line="360" w:lineRule="auto" w:after="120"/><w:ind w:firstLine="480"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="CapTitle"><w:name w:val="CapTitle"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="600" w:after="400" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="B5701F"/><w:u w:val="single"/><w:sz w:val="38"/><w:szCs w:val="38"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="88"/><w:szCs w:val="88"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="44"/><w:szCs w:val="44"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Author"><w:name w:val="Author"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="24386E"/><w:u w:val="single"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="SerieTag"><w:name w:val="SerieTag"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/><w:b/><w:color w:val="1D3A8A"/><w:u w:val="single"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="SceneTag"><w:name w:val="SceneTag"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="120"/></w:pPr><w:rPr><w:i/><w:color w:val="595959"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="160"/></w:pPr><w:rPr><w:rFonts w:ascii="DejaVu Serif" w:hAnsi="DejaVu Serif"/><w:i/><w:color w:val="7F7F7F"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BodyEmpty"><w:name w:val="BodyEmpty"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:line="0" w:after="0"/></w:pPr></w:style>
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
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<w:p><w:pPr><w:jc w:val="center"/></w:pPr>
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
</w:p></w:ftr>"""

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
<w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="720" w:footer="720" w:gutter="0"/>
<w:footerReference r:id="rId2"/>
</w:sectPr>
</w:body></w:document>""".format(body=body, final_header=final_header)
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>""" + esc(TITULO) + """</dc:title>
<dc:creator>""" + esc(AUTOR) + """</dc:creator>
<cp:lastModifiedBy>""" + esc(AUTOR) + """</cp:lastModifiedBy>
<dc:language>es-ES</dc:language>
<dcterms:created xmlns:dcterms="http://purl.org/dc/terms/" xsi:type="dcterms:W3CDTF">""" + now + """</dcterms:created>
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