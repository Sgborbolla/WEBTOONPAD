# TIPS DE WEBTOON — todo lo que hay que saber

Consolidado de las guías de publicación de la plataforma (WEBTOON Canvas Resource
Handbook y Creator 101), las guías de producción de Clip Studio, Lemoon Studio,
HoneyToon, battlebadgers, Multic, Comistitch, los tutoriales de speed lines de
Walter Ostlie, los estudios de lettering de sonido (Serifs Up, Matt Durand, el
paper de semiótica visual de Robin Engstrom) y el análisis de los storyboards de
los artistas de acción coreanos (Jinggae, *The S-Classses That I Raised*, *Trophy
Husband*, *The Hero Returns*).

Cada sección dice de dónde sale. Los números no son opinión: son lo que la
plataforma exige o lo que la guía midió.

---

## 1. El pipeline completo

Este es el orden real de un estudio. La columna de la derecha es lo que hace esta
historieta, porque se genera con IA.

| Etapa | Qué hace el estudio | Qué hacemos nosotros |
|---|---|---|
| 1 | **Outline**: un párrafo por capítulo, con el cliffhanger al final | `mapa-peleas.md` y el guion de temporada |
| 2 | **Guion**: viñeta por viñeta, con posición, expresión, acción, escenario y **todo** el diálogo | `capNN.md`, en formato cine |
| 3 | **Biblia de arte**: proporciones faciales, peinados, cuerpos, ropa, paleta, y **todas las expresiones** de cada personaje recurrente, en varios ángulos | `heroes.md` + `refs-hojas.md` |
| 4 | **Storyboard**: bocetos sueltos que deciden encuadre, posición, expresión y dónde va el globo | El prompt de cada viñeta |
| 5 | **Inking** | — (lo hace el modelo) |
| 6 | **Fondos** | Declarados en el prompt, o assets fijos |
| 7 | **Color** | Declarado en el ancla: color plano, cel, paleta fija |
| 8 | **Lettering**: globos, tamaño, posición, y los efectos | Texto literal en el prompt |
| 9 | **Revisión editorial**: narrativa, calidad visual, cumplimiento | La checklist de `manual.md` |
| 10 | **Publicación** | Recorte a 800×1280 |

**Lo que nunca se saltea: el paso 2, escribir el guion.** El error más común de
quien empieza es abrir el dibujo y hacer páginas. Acorta el retrabajo a la mitad.

### Sobre producir 100 capítulos

| | Horas por semana |
|---|---|
| Solo, a mano, 60 viñetas | 30-40 h de arte |
| Solo, con asistencia de IA, 60 viñetas | ~12 h |
| Estudio | 15-25 h equipo |

A 36-70 viñetas por capítulo y 100 capítulos, la historieta entera son entre 5000
y 6000 viñetas. Eso es un trabajo de años a ritmo profesional, o de varios años a
un ritmo que no se sostiene. El riesgo real no es escribir la historia: es quemarse en
el cap 30.

**Recomendación de las guías:** ritmo semanal constante de 60 viñetas y Episodes
de 50-80 viñetas, no bloques de caps atrasados. Si el ritmo no se sostiene, se bajan
las viñetas por capítulo, no se sube la pausa.

---

## 2. Formato: los números que la plataforma impone

| Parámetro | Valor |
|---|---|
| Ancho | 800 px (fijo) |
| Alto por imagen | 1280 px máx |
| Se dibuja al doble | **1600×2560** |
| Separación entre viñetas | 200 px mínimo |
| Peso por imagen | 2 MB |
| Peso por episodio | 20 MB, hasta 100 imágenes |
| Viñetas visibles simultáneas | 2 máximo |
| Formato de archivo | JPG, JPEG, PNG |
| Tamaño de portada | 690×690 (1200×1200 mejor) |
| Tamaño de letra de diálogo | 12 a 30 px |

Sobre lo del doble: si se dibuja a 2x, la legibilidad a 800 px se mantiene al
reducir. Es la recomendación explícita de las guías de formato.

### Sobre el recorte automático

La plataforma **recorta y comprime solo** lo que pase de 800×1280, y avisa con un
popup. Puede partir la imagen en varias, bajar la calidad, o cambiar el formato.
Si se quiere control total: subir dentro de los límites.

Esto significa que generar un capítulo entero en una sola imagen grande es
peor: la plataforma lo destroza. **Un capítulo es una pila de imágenes de
800×1280, una o dos viñetas cada una.**

---

## 3. Estructura del capítulo

### Tres actos, siempre

| Acto | Viñetas | Función |
|---|---|---|
| Gancho | 1-10 | Un golpe visual o una frase que pide explicación |
| Desarrollo | 11-60 | Avanza todo |
| Cierre | 10 últimas | Cliffhanger o beat emocional |

La regla más dura: **los capítulos que abren despacio pierden al lector antes de
la viñeta 5.** El primer panel tiene que tener algo que pide explicación.

### El punto donde se cae la gente

| Punto | Comportamiento |
|---|---|
| 30-40% del capítulo (~viñeta 20 de 60) | Mayor abandono |
| Sin segundo gancho ahí | Pierde 30-40% de los que empezaron |
| Con segundo gancho ahí | Pierde 5-15% |

**Cada capítulo lleva un segundo gancho en el 30-40%.** Una revelación, una
pregunta, un cambio de tono. En el piloto va en la viñeta 14 de 36 y está marcado
en cada archivo.

### Los dos cierres

| Tipo | Cuándo | Nota |
|---|---|---|
| Emocional | 2 de cada 3 | Una relación gira, o alguien dice lo que no iba a decir |
| De trama | 1 de cada 3 | Peligro, revelación, explosión |

El cliffhanger emocional rinde más y aguanta mejor. **El cliffhanger de trama
constante cansa.** La guía lo dice así: "cliffhangersConstant exhaust readers".

### Final del episodio

| Tipo | Cuándo |
|---|---|
| Cliffhanger | Acelera hacia el final |
| Resolución | Frena hacia el final |
| Pivote | Ritmo medio hasta la revelación |
| Eco | Cierre lento, contemplativo |

Los capítulos que terminan en un cliffhanger demasiado manipulative después de varios.
El cap 100 de esta historieta termina en "eco": una página y un epitafio.

---

## 4. Ritmo y gutter

El gutter es tiempo, no decoración.

| Gutter | Sensación | Cuándo |
|---|---|---|
| 50-100 px | Rapidísimo | Puñetazos, persecuciones |
| 100-150 px | Rápido | Acción |
| 200-300 px | Latido | Reacción, frase que tiene que caer |
| 300-500 px | Lento | Beat emocional |
| 400-600 px | Cambio de escena | Exterior-interior, día-noche |
| 600-800 px | Antes de la revelación | Cliffhanger |

**Todos los gutters iguales = presentación de diapositivas.** Se varyan.

### Reglas de ritmo

- Momentoscallados necesitan espacio. Acción va rápido.
- Acción: viñetas cortas y rápidas. Emoción: viñetas altas con espacio vacío.
- Se cambia el ritmo **deliberadamente**: un capítulo alterna.
- Al planear, sumar 1000-2500 px extra de alto para tener margen de ritmo.

---

## 5. Tipos de viñeta

| Tipo | Función |
|---|---|
| Rectangular estándar | Escena normal, conversación |
| **Vertical alta** | Elemento imponente: edificios, caídas. El formato webtoon la usa muchísimo |
| Horizontal ancha | Paisaje, grupo, línea de tiempo |
| **Establecimiento** | Contexto: lugar, hora, clima |
| **Splash** | Momento importante, clímax. Ocupa la página |
| Inserto | Detalle pequeño sobre otra viñeta |
| Partida | Dos escenas en un cuadro |
| A sangre | Sin marco. Máxima intensidad |
| **De silencio** | Casi vacía. Pausa emocional |

El flujo es **de arriba abajo, de izquierda a derecha**, a diferencia del manga.

---

## 6. Composición y legibilidad

La claridad es el requisito número uno: **el lector tiene que entender qué está
pasando todo el tiempo**.

| Se controla | Cómo |
|---|---|
| Ángulos legibles | La acción se entiende en una mirada |
| Posición clara del personaje | Uno al frente, el resto atrás |
| **Dirección de luz consistente** | La misma escena, la misma dirección |
| Flujo de viñetas fácil | La vista va donde tiene que ir |
| Regla de tercios | Elementos clave en los tercios, no al centro |

Herramientas que las guías recomiendan:

- **Modelos 3D** para mantener ángulos consistentes
- **Vista lateral con referencias fijadas**, para tener siempre la referencia a la vista
- **Vista previa móvil** para ver cómo queda en el teléfono
- **Rejilla de perspectiva** en el storyboard, para fijar altura de cámara

### Encuadre

| Plano | Uso |
|---|---|
| General | Ciudad, edificio entero. Contexto |
| Entero | Cuerpo completo de pie |
| Americano | De las rodillas para arriba |
| Medio | De la cintura para arriba. Conversación |
| Primer plano | Cabeza y hombros. Emoción |
| Primerísimo | La cara llena el cuadro. Impacto emocional |
| Bocas | Solo la boca hablando |
| Detalle | Un ojo, una mano, un arma, un pie, un sello |
| Espaldas | Espalda y nuca, mirando lejos |
| Contrapicado | Desde abajo. La figura enorme |
| Picado | Desde arriba. La figura pequeña |
| Silueta | Figura negra contra luz |
| Grupo | Varias personas juntas |
| Partida | Dos escenas |

### La regla de los 180 grados

Si A ataca de izquierda a derecha, sigue así. Romper el eje desorienta. El corte
de eje se hace **una vez**, con un plano entero de por medio.

---

## 7. Globos y lettering

| Tipo | Cuándo | Borde |
|---|---|---|
| Habla | Normal | Redondeado limpio, cola a la boca |
| Pensamiento | Solo cuatro y omega | Nube |
| **Grito** | Grita, no habla | **Estrella afilada** |
| Documento | Narrador del Sistema | Rectángulo, texto de formulario |
| SFX | Efecto de sonido | Estrella irregular o sin globo |

Reglas:

- **Borde irregular = volumen alto.** Es la codificación estándar. El lector la
  lee sin aprenderla.
- Tamaño de letra: 12-30 px. Más chico no se lee scrolleando; más grande tapa
  el dibujo.
- Orden de lectura de los globos: de arriba abajo dentro de la viñeta.
- No sobrecargar los globos de texto.
- Consistencia de tamaño, fuente y estilo en todo el episodio.
- **El efecto de sonido a veces es solo texto en negrita, sin globo.**

---

## 8. Efectos de sonido

Tratados como tipografía display. Es lo único de la viñeta que es palabra,
imagen y evento a la vez.

| Propiedad | Codifica | Cómo |
|---|---|---|
| Peso y tamaño | Volumen | Más grande y grueso = más fuerte. Doblar el tamaño se lee como mucho más, no el doble |
| Contorno | Textura | Recto y anguloso = impacto, metal, hueso. Curvo afilado = líquido. Roto = destrucción |
| Dirección e inclinación | Velocidad | En la línea de viaje = se mueve con la cosa. Diagonal fuerte = más rápido |
| Perspectiva | Profundidad | Hundido hacia un punto de fuga = el sonido viene de lejos |
| Contorno negro | Legibilidad | Permite ponerlo sobre fondos ruidosos |
| Extrusión | Masa | Los golpes pesados casi siempre llevan una |
| Baseline irregular | Vibración | Letras giradas y desalineadas |
| Arte encima | Integración | El efecto pisa el dibujo, no flota al lado |

Técnicas de lettering que funcionan (de Matt Durand, sobre *Extremity*):

1. **Solapar con el arte**: el dibujo pasa por encima de la tipografía. Reduce
   la fricción y hace que el efecto se funda con la imagen
2. **Múltiples fuentes**: cada sonido con la fuente que lo representa, no una
   fuente única
3. **Trazo**: separa el efecto del fondo y permite cambiar de color
4. **No uniformidad**: letras superpuestas, rotadas, baseline desplazada. Nada
   suena recto

Reglas de smartest:

- **El uso tiene que ser desigual.** Varias viñetas sin efecto y una que domina.
- **El efecto toca o solapa la cosa que hizo el ruido.** Flotando al lado se
  vuelve un subtítulo.
- **Se omite a propósito** cuando la imagen ya muestra el golpe.
- Las convenciones de onomatopeya son **idioma-específicas**. Lo que funciona en
  inglés no funciona igual en español, y hay repertorios distintos para cada
  cultura. Los gion y los gitaigo del japonés cubren estados sin sonido (silencio,
  brillo, tensión) que en español se resuelven con viñeta vacía.
- **En esta historieta: cero kana, cero ideogramas.** Efectos en español.

---

## 9. Combate

Desarrollo completo en `acciones.md`. Lo esencial de las guías:

### La anatomía

```
Anticipación → Ataque en movimiento → IMPACTO → Reacción → Consecuencia
```

El impacto es lo único que importa, y es el panel más grande.

### Líneas de velocidad

| Tipo | Para qué |
|---|---|
| Paralelas | Velocidad lateral o diagonal |
| Radiales / focus | Impacto, salida de página |
| Guionadas | Potencia, rotura, velocidad extrema |

Tres reglas que las guías advierten explícitamente:

- **No overuse.** Si todas las viñetas tienen líneas, ninguna tiene impacto
- **Apuntan a algo importante.** Una línea que lleva la vista al fondo equivocado
  arruina el golpe
- **La densidad codifica el estado**: ralo controlado, denso extremo, caótico
  pérdida de control

Trucos: borrar en blanco rompe la línea negra da energía; dibujar en capa aparte
permite pasar las líneas por encima del personaje; líneas blancas a través de
las sombras funcionan.

### Trucos de panel

Panel solapado, marco roto, corte diagonal, viñeta fragmentada, renglones
staccato, viñeta de pausa. En las peleas es donde la retícula cuadrada se
destruye.

### El error de todos los golpes iguales

**Cada golpe se ve igual: mismo tamaño de panel, mismas líneas, mismos SFX.**
La pelea se vuelve monótona.

La solución es **jerarquizar los golpes por importancia**:

| Golpe | Tamaño de viñeta |
|---|---|
| Menor | Viñeta chica, 1 línea |
| Significativo | Viñeta media |
| Punto de giro | Página entera |
| Finalizador | Doble página (con moderación) |

### El golpe falso

 experienced lectores esperan el impact frame después de la anticipación. Se puede
subvertir: cortar antes del impacto, o mostrar el después. Una vez cada diez.

---

## 10. Color y luz

El color es herramienta narrativa, no decoración.

| | |
|---|---|
| Tonos cálidos y ricos | Momentos passions, luz de tarde |
| Fríos y desaturados | Tensión, drama, misterio |
| Dirección de luz | Consistente por escena. La misma escena, la misma dirección |
| Última pasada | Brillos especulares, efectos atmosféricos, glow, **motion blur** |
| Paleta | Fijada en la biblia de arte, seguida al pie de la letra |

Para esta historieta: color plano, sombreado en dos tonos, sin degradados suaves,
sin ruido. El ancla ya lo fija.

---

## 11. Biblia de arte: la pieza que más importa aquí

Es lo que un estudio entero crea antes de dibujar. Define:

- Proporciones faciales exactas
- Peinados
- Tipos de cuerpo
- Ropa firma
- **Paleta de color**
- **Un rango amplio de expresiones** para cada personaje recurrente
- **Vistas múltiples**: frontal, lateral, tres cuartos

Todo eso en **assets reutilizables**: cejas, formas de ojo, pestañas, mechones,
cicatrices, accesorios, sets de expresiones.

Para una historieta de 100 capítulos generada con IA, esta biblia es lo único
que garantiza que el personaje 1 y el personaje 100 se parezcan. Los prompts
completos están en `refs-hojas.md`.

### Moodboard

Toda historieta seria tiene uno. Preguntas que responde:

1. ¿Qué personajes existentes se parecen al mío?
2. ¿Qué personas reales definen su aspecto?
3. ¿Cuál es su vibra: protagonista, antagonista, morally grey?
4. ¿Qué personajes míos favoritos lo inspiraron?
5. ¿Qué caras, criaturas, formas o universos me interesan?

### La prueba de lectura

Antes de aprobar: mirar cinco viñetas en blanco y negro. Si los personajes se
distinguen solo por su marca, la página funciona. Si hay que adivinar, se
rehace.

---

## 12. Sobre generación con IA

No hay guía oficial para esto porque es nuevo, pero las limitaciones se deducen
de las guías humanas y se prueban fácil:

| Problema | Solución de diseño |
|---|---|
| No mantiene muchas viñetas legibles en una imagen | Un prompt por pantalla; 1 o 2 viñetas por pantalla |
| El texto falla si hay mucho | Máximo 3 globos por viñeta; SFX aparte |
| Se inventa el texto | Texto literal, línea por línea, en el prompt |
| Mezcla personajes en un panel | Uno o dos por viñeta, nunca cuatro |
| Repite composición | Cada viñeta declara plano y composición distintos |
| Se come los efectos | Efectos declarados por viñeta, no en bloque |
| Consistencia de personaje | Biblia de arte + descripción corta fija |
| Multiusuario | No: una persona o dos por viñeta |

### Lo que hacen los storyboards de acción coreanos

De *The S-Classes que I Raised*, *Trophy Husband* y *The Hero Returns*:

- **Los thumbnails se colorean por función**: un color para personajes, otro
  para fondos, otro para líneas de acción, otro para efectos. Es una capa de
  información, no decoración
- **El color indica el tipo de poder.** Hielo azul, electricidad amarilla. En esta
  historieta: Goro naranja, Rika hueso, Ren amarillo, Yui gris azulado
- **El color del contorno del personaje cambia entre paneles** para separar
- **Rejilla de perspectiva en el thumbnail**, para fijar la altura de cámara
- **Las líneas de focus ya aparecen en el thumbnail**, no al final
- **Los globos van puestos desde el thumbnail**, con el texto dentro
- Los paneles van numerados, corresponden a un guion
- Los equipos de arte siguen los thumbnails "como ley"

Ese detalle del color por función es el más útil para nosotros: **el prompt
declara el color de cada capa de la viñeta**, y el modelo pinta de acuerdo.

---

## 13. Lo que mata una historieta

| | |
|---|---|
| Abrir con una escena lenta | Se pierde al lector antes de la viñeta 5 |
| Relleno | 40 viñetas estiradas a 60 se sienten. Mejor 45 que 60 |
| Comprimir | 80 viñetas en 50 se sienten como vértigo. Mejor partir en dos |
| Cliffhanger constante | Agota |
| Gutters iguales | Ritmo plano |
| Todos los golpes iguales | Pelea monótona |
| Personajes sin marca | Ni se distinguen en B/N |
| Texto chico | Ilegible scrolleando |
| Eje rotado | El lector no entiende la acción |
| Líneas en todas partes | Nada tiene impacto |

---

## 14. Los diez tips que más rinden

Si solo se pueden aplicar diez cosas:

1. **Escribir el guion antes de dibujar.** Nunca al revés
2. **Primer panel con algo que pida explicación**
3. **Segundo gancho en el 30-40% del capítulo**
4. **Dos de cada tres cierres emocionales**
5. **Gutters variados, y el gutter grande antes de la revelación**
6. **El impacto es la viñeta más grande**
7. **Las líneas de velocidad solo en 3 o 4 viñetas por pelea**
8. **Los SFX tocan la cosa que hizo el ruido, y en español**
9. **Descripción corta y fija por personaje, pegada literal en cada prompt**
10. **Probar en blanco y negro antes de aprobar**

---

## Fuentes

- WEBTOON Canvas Resource Handbook y Creator 101 (formato, gutter, peso)
- Clip Studio Tips: Webtoon Panelling, 5 Tips to Speed Up Webtoon Production, Work
  Like a Real Webtoon Studio (SIENNAMI), Creating Comic Book Sound Effects
- Lemoon Studio: los 5 pasos de un episodio webtoon
- HoneyToon: cómo se hacen los webtoons, del guion a la publicación
- battlebadgers.co.uk: manual del creador para Webtoon
- Multic: guía de acción, estructura de capítulos, longitud de episodios
- Comistitch: guía de panelling vertical y gutter como tiempo
- Nicole Finch: análisis de storyboards de acción coreanos
- Walter Ostlie: speed lines, tres tipos
- Serifs Up: efectos de sonido como tipografía display
- Matt Durand: estudios de lettering sobre *Extremity*
- Robin Engstrom: semiótica de las onomatopeyas en cómic
- Ben Witherington III: ritmo en webtoon
- Alyssa Villaire: cómo se guionizan los capítulos de webtoon
- Comicory: longitud de episodio y punto de abandono