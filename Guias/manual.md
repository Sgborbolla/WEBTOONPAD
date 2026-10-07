# MANUAL — cómo se hace esto

Todo lo que hay que saber para producir "NPAD" en formato webtoon
vertical. Las cifras vienen de las guías de publicación de la plataforma
(WEBTOON Canvas Resource Handbook), de las guías de acción y panelling de Clip
Studio y Multic, y de los estudios de lettering de sonido. `acciones.md` tiene el
detalle de combate; este archivo tiene el resto.

---

## 1. El formato. Esto no es negociable

| Parámetro | Valor |
|---|---|
| Ancho | **800 px**, obligatorio |
| Alto por imagen | **1280 px** como máximo |
| Formato | JPG, JPEG o PNG |
| Peso por imagen | 2 MB máximo |
| Peso por episodio | 20 MB, hasta 100 imágenes |
| Separación entre viñetas | 200 px mínimo |
| Viñetas visibles a la vez | 2 como máximo |

**Consecuencia directa:** un capítulo no es una imagen. Es una **pila de
imágenes de 800×1280** que el lector baja scrolleando. Si generás un capítulo de
36 viñetas en una sola imagen, la plataforma la va a cortar, redimensionar y
comprimir, y se pierde el texto.

### La unidad correcta

| Unidad | Qué es |
|---|---|
| **Panel / viñeta** | Un momento. Es lo que cuenta el guion |
| **Screen / pantalla** | Una imagen de 800×1280, o sea **1 o 2 viñetas** |
| **Episodio / capítulo** | 40 a 80 viñetas, 6000 a 12000 px de scroll |

Longitud por género, de las guías de plataforma:

| Género | Pantallas | Viñetas |
|---|---|---|
| Terror | 40-60 | 30-50 |
| Drama | 50-80 | 45-70 |
| **Acción (este) | 60-90 | 50-80 |
| Romance | 50-70 | 40-60 |

Los capítulos del piloto tienen 36: es un número de terror, no de acción. En los
capítulos de pelea hay que subir a 50-80. Esto está anotado capítulo por
capítulo en `mapa-peleas.md`.

### El largo se mide en scroll, no en viñetas

Una viñeta alta y atmosférica y una viñeta corta y rápida ocupan muy distinto. Un
capítulo de 60 viñetas scrollea 8000-10000 px. Los capítulos de los 100 tienen
que buscar ese número, no el de viñetas.

---

## 2. La estructura de cada capítulo

Tres actos dentro del capítulo. Siempre los tres.

| Acto | Viñetas | Qué hace |
|---|---|---|
| **1. Gancho** | 1-10 | Un golpe visual o una frase que pide explicación. **Los capítulos que abren despacio pierden al lector antes de la viñeta 5** |
| **2. Desarrollo** | 11-60 | Avanza la trama. Acá va la pelea o la conversación |
| **3. Cierre** | 10 últimas | Cliffhanger o beat emocional. Siempre una pregunta abierta |

### El punto de caída

Las plataformas miden dónde deja de leer la gente: **entre el 30% y el 40% del
capítulo**, más o menos la viñeta 20 de 60.

| | Cuántos pierden |
|---|---|
| Sin gancho intermedio | 30-40% de los que empezaron |
| Con gancho intermedio | 5-15% |

**Cada capítulo necesita un segundo gancho putting en el 30-40%.** Es una
revelación, una pregunta o un cambio de tono. En el piloto va en la viñeta 14 de
36, y está marcado en cada capítulo.

### Los dos tipos de cierre

| Tipo | Cómo | Cuándo |
|---|---|---|
| **Emocional** | Una relación gira, o alguien dice lo que no iba a decir | El que funciona mejor y el que aguanta |
| **De trama** | Una explosión, una revelación, un peligro | Cada 3 o 4 capítulos, no siempre |

Si los 100 capítulos cerraran con cliffhanger de trama, el cap 40 sería
predecible y el 60 estaría agotado. La regla: **dos de cada tres cierres son
emocionales.**

---

## 3. El guion se escribe como cine, no como comic impreso

Los guiones de webtoon no tienen números de página. Van directo de viñeta a
viñeta, con el plano declarado y la transición escrita.

El formato que usan los guionistas de webtoon:

```
VIÑETA 14
Plano: contrapicado
Escena: el pasillo del Ward
Acción: el hueco negro se abre dos metros más
SFX: (ninguno)
FUNDIDO A: la calle

VIÑETA 15
Plano: plano entero
...
```

Reglas del formato:

- **Número de viñeta**, nunca número de página
- **Encabezado de transición** en cada cambio: `CORTE A:` y `FUNDIDO A:`
- **Plano declarado** siempre: general, entero, americano, medio, primer plano,
  primerísimo, bocas, detalle, espaldas, contrapicado, picado, silueta, grupo,
  partida, a sangre, silencio
- **Una acción por viñeta.** Si la viñeta tiene dos acciones, son dos viñetas
- El diálogo va **escrito literal**, con la Indicación del tono entre paréntesis

Un guion de webtoon de 55 viñetas ronda las 1500-2000 palabras. Los nuestros van
a ser más largos porque cada viñeta lleva sus efectos.

---

## 4. El ritmo del capítulo

| Momento | Viñetas | Gutters | Viñetas |
|---|---|---|---|
| Gancho | 1-10 | 300-500 px | 1-2 por pantalla |
| Acción | wherever | **100-150 px** | 3-4 tiras finas seguidas |
| Conversación | wherever | 200-300 px | 1 por pantalla, entonada |
| Revelación | gancho intermedio | 400-600 px | 1 sola, a sangre |
| Pausa | después del impacto | 500-700 px | Mucho vacío |
| Cliffhanger | 10 últimas | 600-800 px | La última a sangre |

Reglas:

- **El gutter es tiempo.** 100 px es un latido. 800 px es un silencio antes de la
  revelación.
- **Todos los gutters iguales = presentación de diapositivas.** Se varyan a
  propósito.
- **Después de un impacto hay una viñeta quieta.** Sin ella, 26 viñetas de
  impacto son 26 viñetas iguales.

---

## 5. Los globos

| Tipo | Cuándo | Borde |
|---|---|---|
| Habla | Normal | Limpio, redondeado |
| Pensamiento | Solo los cuatro y omega | Nube |
| **Grito** | Gritan, no hablan | **Estrella, punta afilada** |
|-documento | Narrador del Sistema | Rectangular, texto de formulario |
| Teléfono | Radio, teléfono | Rectángulo con ondas |
| SFX grande | Onomatopeya de impacto | Estrella irregular, sin globo |

Reglas practices:

- **El borde irregular significa volumen alto.** Es la codificación estándar y el
  lector la lee sin aprenderla.
- Un grito son **una a cuatro palabras**, nunca una frase. Laexception son las
  líneas de pánico del cap 3, que van cortas y seguidas.
- **El balloon va cerca de la boca** y nunca encima del punto de impacto.
- Las cajas del narrador van arriba o abajo de la viñeta, nunca en medio.
- En las peleas, el globo **no tapa la cara ni el golpe**. Se mueve al lado.

---

## 6. La coherencia de personaje

Es el problema real de la historieta generada con IA. Lo que funciona:

| Técnica | Cómo |
|---|---|
| **Descripción corta y fija** | Siempre las mismas cinco líneas del ancla: físico, ropa, marca única, edad, color |
| **Una sola marca de ropa por personaje** | Es lo que permite reconocerlo en negro y blanco |
| **Repetir el mismo bloque literal** | El ancla se pega palabra por palabra en cada conversación |
| **Comparar con referencia** | Una hoja de referencia del personaje antes de cada temporada |
| **Describir la posición, no la acción** | "de espaldas, el escudo atado a la espalda" es más estable que "corriendo valeroso" |

Lo que no funciona:

- Describir la acción exacta del cuadro (Stitch improvisa el resultado)
- Pedir varios personajes en la misma imagen (los mezcla)
- Nombrar al personaje sin la descripción corta
- Cambiar de palabras para el mismo rasgo entre escenas

### La prueba de lectura

Antes de aprobar un capítulo, se miran cinco viñetas en negro y blanco. Si los
cuatro se distinguen solo por su marca, la página funciona. Si hay que adivinar
quién es, se regenera esa viñeta.

---

## 7. Sobre generación con Stitch

Lo que hace bien: composición, viñeta por viñeta, color plano, sombra dura.

Lo que no hace bien, y hay que diseñarle el trabajo alrededor:

| Problema | Solución |
|---|---|
| No mantiene 36 viñetas legibles en una imagen | Un prompt por pantalla, 1 o 2 viñetas |
| El texto sale mal si hay mucho | Máximo 3 globos por viñeta; el SFX va aparte |
| Se inventa el texto | El texto va literal en el prompt, línea por línea |
| Mezcla personajes en un panel | Un personaje o dos por viñeta, nunca cuatro |
| Se come los efectos | Los efectos van declarados por viñeta, no en bloque |
| Repite la composición | Cada viñeta declara un plano y una composición distintos |

### El prompt

Un prompt por pantalla, con esta forma:

```
CAP 03, pantalla 9 de 12. Viñeta 22.
Ancla NPAD aplicada.
PLANO: <declarado>
COMPOSICION: <regla de tercios, que queda en que lado, que se ve al fondo>
PERSONAJES: <descripción corta de cada uno, literal>
ACCION: <una sola accion>
EFECTOS: <líneas, forma, color, direccion>
SFX: <palabra en español> <contorno> <tamaño, encima de que>
GLOBO: <personaje, texto literal, donde>
GUTTER ARRIBA: <px>   GUTTER ABAJO: <px>
```

Y al final del capítulo, una vez:

```
SONIDOS DEL Capítulo: PUM (recto), CRAAACK (rasgado), ZAS (curvo),
GRRAAAH (a sangre). Ningun caracter japonés.
```

---

## 8. Los números de esta historieta

| | |
|---|---|
| Capítulos | 100 |
| Temporada 1 | 1-25 |
| Temporada 2 | 26-50 |
| Temporada 3 | 51-75 |
| Temporada 4 | 76-100 |
| Viñetas por capítulo | 30 a 80, según el tipo |
| Pantallas por capítulo | 25 a 50 |
| Scroll por capítulo | 6000 a 12000 px |
| Total de viñetas | entre 5000 y 6000 |
| Total de pantallas | entre 2800 y 3600 |

A 800 px de ancho, un capítulo de 36 viñetas de tamaño medio scrollea cerca de
6000 px. Es un capítulo corto. Los capítulos de acción, 70 viñetas, llegan a
11000 px.

---

## 9. La lista corta, para revisar

Cada capítulo, antes de generarse:

- [ ] ¿Tiene 40-80 viñetas? (30-50 si es terror, 50-80 si es acción)
- [ ] ¿Scrollea 6000-12000 px?
- [ ] ¿La primera viñeta pide explicación?
- [ ] ¿Hay un segundo gancho en el 30-40%?
- [ ] ¿El cierre es emocional o de trama? ¿Lleva tres seguidos de trama?
- [ ] ¿Las transiciones están escritas (`CORTE A:`)?
- [ ] ¿Un plano declarado por viñeta?
- [ ] ¿Una acción por viñeta?
- [ ] ¿Los gutters cambian de tamaño?
- [ ] ¿El impacto es el panel más grande?
- [ ] ¿Los SFX están en español y tocan la cosa que hizo el ruido?
- [ ] ¿Máximo 3 globos por viñeta?
- [ ] ¿Los cuatro se distinguen en blanco y negro?
- [ ] ¿Ningún sistema, barra, número, HUD ni LEVEL UP?
- [ ] ¿Ningún texto en inglés ni kana?
- [ ] ¿El capítulo anterior también era de pelea fuerte?

Si fallan tres, se reescribe el guion antes de generar. Regenerar imagen cuesta
más que corregir texto.