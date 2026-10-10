import os

novela='Novela/novela_caps/cap02.txt'
guion_out='Guiones/cap02.txt'

header = '''# CAPÍTULO 2 — "La primera puerta"

> **Retícula:** `medidas-referencia.txt` §5. Pantallas de 800×1280.
> **Fecha en la ficción:** lunes **15 de mayo de 2017**, 15:00 (Día 1, tarde). Presente: 2026 (9 años).
> **Bloques:** A = Turno de tarde (S01–S20) · B = Se abre la puerta (S21–S40) · C = El primer kaiyu (S41–S60)
> **Total:** 60 pantallas de 800×1280 · 120 viñetas · 76.800 px de scroll

## Ficha

| | |
|---|---|
| Géneros | Acción, tensión, realismo crudo |
| Estructura | Tensión creciente hasta primer encuentro |
| Fondo | Ward Sector 6, calle de bloque de trabajadores, asfalto, cemento, tuberías |
| Personajes con nombre | Goro, Kosuke, Nomura, Kiryu |
| Viñetas | 120 |
| Pantallas | 60 |
| Globos de diálogo | 80+ |
| Cajas narración | 20 |
| SFX | español solo gráfico |
| Transiciones | CORTE A: / FUNDIDO A: negro (cierre) |

> **Segundo gancho:** pantalla S36 (viñeta V71, ~33%) — la puerta metálica se abre del todo.
> **Nombres oficiales.** Cero inglés/kana/ideogramas. Cero HUD.
> **Cierre:** trama (T) — nadie sabe aún qué es un kaiyu.

'''
with open(guion_out,'w',encoding='utf-8') as f:
    f.write(header)
    f.write('\n## 2. DESARROLLO POR PANTALLAS\n\n')
    f.write('### BLOQUE A: Turno de tarde (S01–S20)\n\n')
    f.write('#### S01 · T1 · 1 viñeta (1280)\n- **V1.** Plano general. Ward Sector 6, bloque de trabajadores. Sol de tarde bajo.\n- **CAJAS:** `[CAJA:NARR] Sector 6. Turno de tarde.`\n\n')
    f.write('#### S02 · T2R · 2 viñetas (620,620)+gap 40\n- **V2.** Goro apoya espalda contra marco puerta servicio, brazos cruzados.\n- **V3.** **Goro:** —Cuatro y veinte... Cuatro y media abre el otro.\n\n')
    f.write('#### S03 · T3R · 2 viñetas (570,570)+gap 40\n- **V4.** **Goro:** —Seis y ahí se van todos. Menudo turno.\n- **V5.** Kosuke fuma en escalerilla, mira calle.\n\n')
print('ok')
