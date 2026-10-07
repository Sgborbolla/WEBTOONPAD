# NPAD — Notas del proyecto

> Archivo de decisiones y pendientes. Se actualiza con cada avance.
> Fecha de la última actualización: 2026-10-07.

## Objetivo general

**Nippon Post-Apocalyptic Disaster (NPAD)**: serie de **varias temporadas**.
- **Primera temporada = caps 1-200** (documento rector: `Guias/arco-200.md`).
- Después de la temporada 1, la serie continúa con más temporadas hasta cruzar
  los **más de 30 años** de historia (el mundo kaiyu, los otros catálogos, la
  invasión en otros países, etc.) e historias nuevas.
- Dos salidas que avanzan **a la par** por capítulo:

1. **Novela** (fuente grande, extensa): `Novela/novela_caps/capNN.txt` -> un solo docx creciente `Novela/NPAD_NOVELA.docx`.
2. **Guiones webtoon**: `Guiones/capNN.md` en el formato detallado de `Guiiones/cap01.md` (modelo de referencia, 1019 líneas).

Regla del usuario: cada cosa que se haga/agregue en la novela, los capítulos `.md`
deben ajustarse en consecuencia ("los arreglos necesarios basándote en lo que hagas
en la novela").

## Decisiones de estilo de la novela (docx)

- **Portada de título (pág 2)** aprobada: título en letras normales **azul eléctrico `#1D3A8A`** subrayado, tamaño 88 (=44pt). Debajo **NPAD** (estilo Subtitle, 44=22pt, azul `#1D3A8A`). Luego línea **"TEMPORADA 1 · CAPÍTULOS 1 A 200"** (estilo SerieTag, 12pt, azul). Al final **"Autor: Sergio Grabiel Borbolla Verdecia"** (estilo Author, 34=17pt, azul `#24386E`).
- **Encabezados de capítulo**: ámbar `#B5701F`, subrayados, tamaño 38 (=19pt), centrados.
- **Salto de página**: `w:pageBreakBefore` + `w:keepNext` DENTRO del párrafo del título, en TODOS los títulos (el fallo anterior era ponerlo en un párrafo vacío posterior). Esto garantiza el encabezado al inicio de página también tras imágenes.
- **Neón 3D del título**: borrado definitivo (se eliminaron `titulo_neon.png` y `render_titulo.py`). Título va con letras normales.
- **Marca de agua: ELIMINADA del código** (`header1.xml`, `rId6/rId7`, `WATERMARK` y `header1_xml()` fuera de `make_docx.py`). Ya no hay marca en ninguna página. Se dejó de incrustar `watermark.png`.

## Imágenes e ilustraciones

- Estilo de las ilustraciones **dentro de la novela**: **crayón coreano/japonés** ("a crayón es más ideal").
- Marcador en la novela: línea propia `[IMG:img/archivo.png]` -> se incrusta con `wp:inline`, ancho 92% del área de texto, estilo `Caption` para pies (16px itálica gris).
- Generador: `Novela/gen_images.py` con **Pollinations** (`https://image.pollinations.ai/prompt/...?width=&height=&nologo=true&model=flux&seed=`) + reintentos (a veces responde **HTTP 402** o 524; reintentar con otra semilla).
- **IMPORTANTE (webtoon)**: Pollinations imprime en la esquina inferior derecha el logo/texto **"Made with Pollinations.ai"**. Ya se limpió en las 4 imágenes actuales patcheando la esquina con textura (detectar cluster por `ImageChops.subtract` vs blur). Guardar siempre `nologo=true` y limpiar nueva esquina antes de usarlas en la historieta.
- Semillas guardadas de las imágenes actuales: `img/cap01_portal.png` (sin logo), `img/cap01_batalla.png` (seed 65870), `img/cap03_calle.png` (seed 44057), `img/cap05_descarga.png` (seed 21736). Las de cap01 se re-descargaron para limpiar el logo.

## Canon obligatorio (mando `Guias/arco-200.md`)

- **Ren Hayashi — El Relámpago**; **Yui Nakamura — La Distancia** (rifle militar con **mira telescópica**, no escopeta). PROHIBIDO "Ren Ishida", "Yui Kurosawa", "La Sombra" (es un subjefe naranja) y "La Escopeta".
- **El Silencio = 14 min exactos** (04:58 -> 05:12, 15-may-2017). Cap6: **catorce puertas**, cierra pilot.
- **Cronología de los primeros 10 capítulos (corregida 2026-10-07):** Día 1 = lunes 15-may (caps 1-3; Silencio 04:58→05:12, presente 07:42); Día 2 = martes 16-may (caps 4-5); Día 3 = miércoles 17-may (cap06 madrugada 04:52-05:13, cap07 05:20-05:25, cap08 21:10 + alba del 18); Día 4 = jueves 18-may (cap09 10:40-19:30, cap10 21:45). Queda revertido el error previo de "día seis"/"18 de mayo = día seis": cap09 y cap10 son **día cuatro**.
- Cero inglés/kana/kanji/cirílico en la historieta; SFX en español. Japonés solo en el título corto de la portada.
- **Formato modelo de guion**: `Guiones/cap01.md`. Pain dogs:
- Goro sin guante desde el final del cap5 (lo arrojó tras la descarga que mató a Nomura Tatsuo).

## Canon puente — juego NPAD (repo `NipponPostApocalypticDisaster`, verificado 2026-10-07)

El repo compartido es el **videojuego** de NPAD (Godot 4 + C#, roguelite 2D vertical, 2 botones: ataque+dash).
Fuente de verdad del juego: `docs/diseño.md` (2080 l.) + `personajes.md`, `enemigos.md`, `AMBIENTES_STITCH.md`, `DESIGN.md`.

- **Mundo:** costa de Kantō, **Ward Noveno** = arcología de investigación de **40.000 personas**; **39 años** tras el **Silencio** (14 min) el tiempo se separó en **capas** por pisos; cada atrapado repite su último segundo. El único fin es llegar al **núcleo** y cerrar la fractura.
- **Los 4 Instantes (jugadores):** Rika **Tsukimi** — La Hoja (Ruptura 一閃斬 / Issen-zan); Goro **Arashi** — El Yunque (鉄槌 / Tettsui); Ren **Hayashi** — El Relámpago (疾雷 / Shirei); Yui **Nakamura** — **El Eco** (残響 / Zankyō, ondas radiales, **SIN rifle**). **DECISIÓN (2026-10-07):** el título canónico en novela/historieta es **"La Distancia"** (rifle con mira telescópica). **"El Eco" queda SOLO como nombre del personaje del juego** (rol radial, sin rifle). El "eco" como MOTIVO sigue siendo de Yui en la novela: cada disparo deja "el eco de la distancia" (el silencio tras el tiro). Rika y Goro añaden apellidos nuevos (Tsukimi, Arashi) frente a la novela actual.
- **Puentes aceptados con la novela (la novela = origen 2017; el juego = consecuencia 39 años después, se suceden, no compiten):**
  - En el juego Rika sube *"buscando a alguien"* («Lo que aún queda»). En la novela su hermana **Mio desapareció 9 años atrás** -> si Mio quedó atrapada en el Ward, la búsqueda de Rika en 2056 tiene a quién buscar.
  - Goro (juego): *"Yo puse estas puertas. Yo las cerraré por última vez."* — guardia del Ward; encaja con su papel en la caída de la novela.
  - El **Núcleo** (juego) es una fractura vertical entre capas de tiempo = el **"cielo que se cierra"** de la novel cap6. Mismo fenómeno.
- **Arte del juego:** pixel art 2D OVA desaturado, sprites 48×48 / 24 px en pantalla, 3/4 lateral, sin anti-alias; **ELEGIBLE** por forma y silueta en 200 ms; prohibidos neones `#00f0ff`/`#39ff14`/`#bd00ff`; `#ff2d6f` = peligro, `#ffc400` = recompensa, `#9afaf2` = reanimación (solo piso 5). Para la historieta webtoon **no aplicar** esta estética pixel: la historieta va en estilo coreano tipo Solo Leveling (escuela coreana), el pixel es identidad del juego.
- Enemigos canon (juego): Carrilero, Embestidor, Lanzador, Blindado, Resucitado + subjefes/jefes (El Portero, Los Gemelos, La Caldera, El Escribano, La Cirujana, El Núcleo).

## Plan de entrega — volúmenes de HISTORIETA (formato internacional)

- **Estándar internacional del género (verificado en web):** los manhwa/webtoon se entregan compilados en **volúmenes de ~10 capítulos** (p. ej. *Solo Leveling* en volúmenes, *Lookism* en 20+ tomos, light novels en volúmenes EPUB/PDF). El usuario adoptó este formato: **un PDF con 10 capítulos dentro**.
- **Regla de producción:** al completar cada hito de 10 capítulos, **DETENER la novela** y producir la **historieta webtoon** de esos 10 capítulos junto a los guiones `.md`, entregada como **PDF único con los 10 capítulos**. El siguiente hito de 10 (cap 11-20) se produce después de escribir la novela de esos capítulos. **El proceso se repite indefinidamente por temporadas** hasta atravesar los 30+ años de historia (la serie es larga; los volúmenes siguen saliendo).
- Próximo hito: al terminar la novela del **capítulo 10**, montar el **PDF de los capítulos 1-10** (novela ya hecha 1-10; historieta en base a los `.md`).
- **ESTADO 2026-10-07:** novela **DETENIDA** (caps 1-10 ✅). Se está montando el **PDF de historieta caps 1-10**. Volumen siguiente (caps 11-20) se produce tras escribir la novela de esos capítulos.

## Organización de carpetas (2026-10-07)

- `Guias/` — canon y lore (`arco-200.md`, `biblion.md`, `estilo.md`, etc.).
- `Guiones/` — CAP. `cap01.md` … `cap10.md` + `cap01_historia.txt` (movidos aquí desde la raíz).
- `Novela/` — generador `make_docx.py`, `gen_images.py`, `render_watermark.py` (inutilizado), `novela_caps/` (prosa cap01-06.txt), `img/` (ilustraciones crayón), `NPAD_NOVELA.docx`, `portada.png`, carpas `TXT/` y `DOCX/` (copias/HTML).
- **BORRADA** la carpeta `prompts/` y el `prompt-cap01.md` (ya no hacen falta).
- Raíz: scripts webtoon `maquetador.py`, `compositor.py`, lore suelto, `img/cap01/` (arte), `pdf/`, `temp_text.txt`.

## Progreso por capítulo

| Cap | Novela (`capNN.txt`) | Guion (`capNN.md`) | Notas |
|---|---|---|---|
| 1 | ✅ + batalla aérea | ✅ + batalla (Bloque A2, S29A-E) | ✅ portada Ren Hayashi/Yui Nakamura, rifle con mira telescópica; conteos corregidos: 79 pantallas · 136 viñetas · 12 SFX · 8 cajas (audit 2026-10-07) |
| 2 | ✅ | ⚠️ guion corto (formato resumen) | fecha añadida a la ficha: lunes 15-may |
| 3 | ✅ (imagen `cap03_calle`) | ⚠️ formato resumen | fecha añadida: lunes 15-may |
| 4 | ✅ | ⚠️ formato resumen | fecha añadida: martes 16-may |
| 5 | ✅ (imagen `cap05_descarga`) | ⚠️ formato resumen | fecha añadida: martes 16-may |
| 6 | ✅ prosa escrita (Día 3, catorce puertas) | ✅ guion 40 viñetas (ampliado: tejado, civiles contando, tanque, chincheta) | ✅ novela termina con quemaduras sin explicar (semilla cap18) · fecha añadida: miércoles 17-may |
| 7 | ✅ prosa escrita (`cap07.txt`, "Lo que quemó") | ✅ guion detallado (1444 l) | cronología corregida: ficha/caja/tabla pasan de "lunes 15" a "miércoles 17" (05:25) |
| 8 | ✅ prosa (`cap08.txt`, "Verde", 21:10 + epílogo al alba) | ✅ guion detallado (68 pantallas · 133 viñetas) | cronología corregida: "Lunes 15" → "Miércoles 17" (21:10); bloque G alineado con la novela |
| 9 | ✅ prosa (`cap09.txt`, "Nadie hace nada", 18-may, kaiyu amarillo) | ✅ guion detallado (68 pantallas · 131 viñetas) | corregido a "día cuatro terminó así" (era "día seis") y "tres días después del lunes" |
| 10 | ✅ prosa (`cap10.txt`, "La jauría", jueves 18, 21:45) | ✅ guion detallado (70 pantallas · 136 viñetas, reordenado V1-V136) | LOS TEXTOS auditados: 6 globos / 5 cajas / 9 SFX / 4 sonidos (se vaciaron números viejos); V115 gutter 0/1020 |
| 11-200 | ❌ | ❌ | a la par |

## Pendientes / próximos pasos

1. ✅ Corregir `Guiones/cap01.md` portada: Ren Hayashi — El Relámpago / Yui Nakamura — La Distancia. ✅
2. ✅ Ampliar `Guiones/cap06.md` con lo extra de la novela cap6.
3. Push a GitHub (`git@github.com:Sgborbolla/WEBTOONPAD.git`): commit pendiente con el QA completo (cronología Día 1-4, conteos cap01, LOS TEXTOS de cap10, docx a 10 caps, notas).
4. ✅ Capítulos 9-10 (novela + guion a la par). **Al completar el cap 10: DETENER la novela y montar el PDF de historieta con los 10 primeros capítulos** (formato internacional de volúmenes de ~10 caps).
5. Webtoon: **estilo de dibujo AÚN SIN DECIDIR** (usuario se inclina a coreano tipo Solo Leveling / Omniscient Reader; historieta en japonés con escuela coreana). Definir antes del arte.
6. ✅ Revisar del usuario: docx con 10 capítulos, imágenes incrustadas y encabezados corregidos (reconstruido 2026-10-07).
7. ✅ **Decidido (2026-10-07):** Yui Nakamura = **"La Distancia"** en novela/historieta (rifle con mira telescópica). "El Eco" queda solo en el juego. NO hay que tocar ninguna otra referencia: los guiones/novela ya usan "La Distancia"; las demás apariciones de "eco" son el sustantivo (echo), no el título.
8. ✅ **QA de consistencia 2026-10-07:** cap01 (viñetas consecutivas V1-V136, tablas = cuerpo, 12 SFX + 5 sonidos), cap10 (tablas LOS TEXTOS renumeradas, V115 gutter 0/1020), cap02-06 (fechas en ficha, ortografía/acentos, "cada certain"→"cada ciertos"), novelas (timestamps Día 1-4 consistentes).
9. **PLANEADO (no implementar en caps 1-10):** nuevo arco de enemigos para caps 11+ y biblia del mundo kaiyu (idioma, estilo de vida, jerarquías, capítulos ambientados en su mundo) — pendiente de redactar en `enemigos.md` / `kaiyu-world.md`.

## Notas de producción webtoon

- Las .md deben avanzar "a la par" de la novela, no después.
- Muchas batallas (solo, grupales, aéreas) para mantener acción y ver subir de rango, estilo historietas del género.
- Para la historieta no reutilizar las imágenes crayón de la novela sin limpiar primero el logo de Pollinations (o generarlas con `nologo=true` y verificar la esquina).