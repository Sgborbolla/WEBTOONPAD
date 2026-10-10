#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webtoon_estilo.py — CARD DE ESTILO CANÓNICA DE LOS CATORCE (Estilo A).

Según STYLE EXEMPLAR (flic.art export, modo 01) + Hoja de personajes (04) +
paleta canónica de la serie. Se aplica a TODAS las pantallas generadas.
"""
from PIL import Image, ImageStat

# --- métricas canónicas: paneles azul-marino/índigo (Style Exemplar ZIP), cel-shading ---
REF_MEAN = (60, 52, 70)
REF_STD  = (55, 48, 46)

# Paleta canónica de la serie (Style Exemplar)
ROJO_RIKA   = "#B71C1C"
AMARILLO_REN = "#FFFF00"
HUESO       = "#F2F0EC"
MINE        = "#FFF9C4"
GRIS_B      = "#2A2A2E"
ACERO       = "#6B5D4F"

PALETA_HEX = [HUESO, ROJO_RIKA, AMARILLO_REN, MINE, ACERO, GRIS_B]

ESTILO_ARTE = (
    "Korean manhwa webtoon illustration in Solo Leveling cinematic mood, "
    "matte dark navy and indigo color palette, cel-shaded two-tone, heavy "
    "clean ink lineart, semi-real painterly rendering, cold desaturated light, "
    "subtle film grain, dramatic high contrast, vertical webtoon panel 9:16, "
    "illustration not photograph, no photography, no glamour, no fashion, no "
    "beauty portrait, no selfie, no bokeh, no text, no letters, no logo, no watermark"
)

ESCENA_VACIA = (
    "completely empty scene, no people, no characters, wide establishing shot, "
    "abandoned ruined post-apocalyptic japanese city, dark navy and indigo "
    "palette, cold overcast light, long shadows, silent and desolate"
)

DESC_KI = "post-apocalyptic ruined japanese city, dark navy and indigo palette, cold overcast light"

# --- fichas de personaje/entidad (Hoja de personajes, modo 04) -----------
# se añaden al prompt cuando la viñeta menciona al personaje, para que el
# diseño sea el MISMO en los 200+ capítulos.
PERSONAJES = {
    "rika": ("Rika Tsukimi, small girl 158cm with long bright red hair in a high ponytail, "
             "serious piercing eyes, small eyebrow scar, white bone haori #F2F0EC over a black "
             "striped kimono with wide black obi, bandaged forearms, holding a katana"),
    "mine": ("Mine Hoshino, small vulnerable child with black hair and straight fringe, big eyes, "
             "pale yellow apron #FFF9C4 over a white blouse"),
    "goro": ("Goro Arashi, huge tall bald man 195cm, square jaw, short beard, rusty industrial steel "
             "armor plates, round shield on his back, yellow construction helmet, crossed gauntleted arms"),
    "ren":  ("Ren Hayashi, slim young man 172cm with messy black hair, bright yellow jacket #FFFF00 "
             "with high hood over black hoodie, hand bandages, nervous expression"),
    "yui":  ("Yui Nakamura, tall woman 172cm with very long straight black hair in a high ponytail, "
             "grey-blue jumpsuit, black tactical vest, white gloves, wooden bolt-action sniper rifle on her back"),
    "shino": ("Shino Tsukimi, young man with dark hair, pale serious face, black jackets, katana"),
    "kaiyu": ("kaiyu monster, tall non-human black muscular silhouette with glowing yellow biomechanical "
              "lines and joints and a dark circle in the torso, menacing"),
    "absorvente": ("kaiyu monster type, smooth black silhouette, glowing yellow lines, absorbing posture"),
    "arcilla": ("kaiyu monster type, grey clay-like black body, half melted, yellow joints"),
    "plegador": ("kaiyu monster type, tall thin black figure, folded limbs, yellow biomechanical seams"),
    "gancho": ("kaiyu monster type, dark hook-armed silhouette with yellow seams"),
    "linea": ("kaiju monster, colossal black silhouette barely visible among clouds, tiny glowing yellow lines"),
}

AMB = "noir devastated Japanese city ruin, cold grey and blue light, cinematic long shadows"

def desc_personajes(texto):
    """Devuelve las fichas de personajes/entidades que se mencionan en la ixdx viñeta."""
    t = texto.lower()
    out = []
    orden = ["rika", "mine", "goro", "ren", "yui", "shino",
             "absorvente", "arcilla", "plegador", "gancho", "linea", "kaiyu"]
    for k in orden:
        if k in t or k == "kaiyu" and "kaiyu" in t:
            d = PERSONAJES.get(k)
            if d and d not in out:
                out.append(d)
    return out


def estilo():
    return ESTILO_ARTE


def grade(im):
    """Lleva el tono de cada página al rango canónico (paneles oscuros, alto contraste)."""
    im = im.convert("RGB")
    stat = ImageStat.Stat(im)
    mean_in = tuple(stat.mean)
    std_in = tuple(v ** 0.5 for v in stat.var)
    px = im.load()
    W, H = im.size
    tab = []
    for c in range(3):
        si = max(std_in[c], 1e-6)
        t = []
        for v in range(256):
            nv = (v - mean_in[c]) * (REF_STD[c] / si) + REF_MEAN[c]
            t.append(max(0, min(255, int(nv))))
        tab.append(t)
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            px[x, y] = (tab[0][r], tab[1][g], tab[2][b])
    return im


if __name__ == "__main__":
    for k, v in PERSONAJES.items():
        print(k, "->", v[:60])