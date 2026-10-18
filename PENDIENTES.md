# NPAD — PENDIENTES

> **Autor:** Sergio Grabiel Borbolla Verdecia
> Estado: 100/100 guiones validados. Separadores añadidos.

---

## Estado actual

- **100/100 capítulos** pasan `check_guion.py todo`.
- **Corpus:** 2747 pantallas · 5597 viñetas.
- **Separadores:** sección `## SEPARADOR` en el header de cada guion (fondo + texto centrado).
- **Rika:** kimono corto negro #14130F (resuelto, aplicado en 107 archivos).
- **Jumoji:** sin macrón (resuelto en 10 archivos).
- **ESCUDO:** errata corregida en ANCLA-CONSISTENCIA.txt.

---

## Hecho esta sesión

- Ropa de Rika unificada: kimono negro en estilo.txt, make_guion.py, guiones, biblia, heroes.txt.
- Separadores (páginas de transición) insertados en los 100 guiones.
- Erratas ESCODO→ESCUDO y Jūmoji→Jumoji corregidas.
- Sección "Elenco y enemigos de este capítulo" en todos los guiones.
- Color de enemigos = rango (no piel) corregido en generador y fichas.

---

## Pendiente

### 1. Unificar diseño cap01/cap02 con el resto
- cap01 y cap02 usan ancla **compacta** + sección `## Los textos` antes de viñetas.
- cap03–100 usan ancla **completa** (STITCH) + `## Globos` después de viñetas.
- Decidir: ¿pasar cap01/02 al diseño completo, o al revés?

### 2. Sección "Reglas de esta adaptación"
- Solo cap01/02 tienen `(cómo se hizo)`. Los demás solo `## Reglas de esta adaptación`.
- Unificar nombre de sección.

### 3. Sección "Semillas y metas"
- Solo 7 capítulos la tienen (06, 09–13, 15). Los demás no.
- Decidir si se añade a todos o se elimina de esos 7.

### 4. Libro .docx (aparcado; lo cierra el usuario en PC)
- Paginación real: modelo da ~335 páginas, WPS mostró 420.
- Limpiar 18 marcadores crudos `> **SEGUNDO GANCHO**` (caps 51–70).
- Re-bake de PAGEREF si cambia paginación.

---

## Pipeline

- Validador: `python3 check_guion.py todo` / `cap NN`
- Novela fuente: `Novela/novela_caps/capNN.txt`
- Guiones: `Guiones/capNN.txt`
- Ancla: `Guias/ANCLA-MAESTRA-NPAD.txt` + `Guias/estilo.txt`
- Fichas: `FICHAS-VISUALES.txt`, `Guias/ficha-capNN.txt`
- Stitch: generar imágenes con el ancla + descripción de cada viñeta
- Generador: `make_guion.py` (regenera caps 03,04,05,14,16-100)
