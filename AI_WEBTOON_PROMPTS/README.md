# AI WEBTOON PROMPTS

Carpeta con mini-prompts para generar arte webtoon con IA por lotes (2–3 pantallas consecutivas).

## Filosofía
- Generar por pantalla completa (864×1536), NO por viñeta suelta.
- Dejar globos/bocadillos VACÍOS. El texto lo pone `maquetador.py` desde el guion.
- Sin letras, logotipo, marcas, onomatopeyas con texto.
- Mantener continuidad entre pantallas del lote (luz, color, diseño personajes).
- Seguir geometría exacta del guion (T1/T2R/T3R/T4R/T5 + gutters).
- Trabajar lote a lote: aprobar → generar siguiente.

## Estructura
- `capNN_loteXX_sXX_sYY.md` → prompt listo para IA de imagen (ChatGPT/GPT-Image, Midjourney, Ideogram, Flux, etc).

## Flujo
1. Copiar contenido del archivo de lote a la IA.
2. Pedir que genere las N pantallas (SXX.png, SYY.png...) 864×1536.
3. Guardar en `img/capNN/pag_sXX.png` con ese nombre exacto.
4. Comprobar continuidad y espacios para globos.
5. Pasar al siguiente lote.
