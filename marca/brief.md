# Brief de marca: Senda Consultora

Ronda 1 · exploración de territorios · octubre 2026

## Lo que sabemos

- Consultora integral nueva, con tres focos: **desarrollo comercial**, **investigación de mercado** y **automatización con IA**.
- Nombre: **Senda**. Una senda es un camino angosto, hecho por el paso de la gente más que por una obra. Es más chica e íntima que "camino" o "ruta", y viene de la misma raíz que "sendero".

## Supuestos (a validar)

1. Clientes: pymes y empresas medianas de Argentina / LATAM, dueños y gerentes comerciales, no grandes corporaciones.
2. El equipo es chico y la relación es cercana: el cliente trabaja con las personas, no con "la firma".
3. Canales principales: LinkedIn, propuestas e informes en PDF, presentaciones, web simple, firma de mail. Poco impreso.
4. Quien va a aplicar la marca en el día a día no es diseñador (Canva, Google Slides, Docs).
5. No hay presupuesto inicial para tipografías pagas: todo el sistema debe funcionar con fuentes libres.

## Tensiones que la identidad tiene que resolver

- **Datos / personas**: la investigación y la IA piden rigor; la venta consultiva pide calidez.
- **Artesanal / automatizado**: se automatizan procesos, pero el diagnóstico se hace a mano y en el terreno.
- **Chica / integral**: una consultora nueva que ofrece mucho tiene que verse enfocada, no dispersa.

## Código visual del rubro (del que hay que salir)

Azul corporativo + gris, flechas ascendentes, brújulas, montañas, redes de nodos, degradés violeta "IA", sans genéricas (Montserrat, Poppins), fotos de stock de reuniones. Para un nombre como Senda, la trampa obvia es el camino en perspectiva hacia el horizonte.

## Territorios propuestos

| | Territorio | Oración-concepto |
|---|---|---|
| A | Líneas de deseo | Senda encuentra los caminos que tus clientes ya recorren, aunque nadie los haya diseñado. |
| B | Marcas de sendero | Senda no entrega un mapa: marca el camino, paso a paso, para que el equipo lo recorra solo. |
| C | Apacheta | Cada dato es una piedra; apilados, marcan el rumbo. |

Detalle visual de cada uno en `marca/territorios/`.

## Devolución ronda 1 (rechazada)

- No gustaron los territorios conceptuales (líneas de deseo, marcas de sendero, apacheta): se sintieron poco tecnológicos.
- **Logo pedido:** monograma con un juego geométrico sobre la **S** (referencias: S partida en dos piezas con canal diagonal; S de dos gotas con cuña).
- **Color pedido:** duotonos planos, fuertes e identificables, con aire tecnológico (referencias: royal blue + crema, bosque + lima, rojo cálido + azul espacio + blanco).
- Tipografía de las referencias: grotesca extendida y pesada.

Ronda 2 en `marca/territorios/senda-ronda-2.html`.

## Devolución ronda 3

- S favoritas: **Bisel** y **Contrapeso**.
- Paletas: **Bosque** primero, **Señal** segunda. Sin decidir todavía.
- Escritura del nombre: probar **SENDA** y **Senda**.
- Tipografía pedida: **bold, elegante y formal**. En ronda 4 se proponen Spectral, Bodoni Moda, Red Hat Display e Instrument Sans (condensada).

Ronda 4 en `marca/territorios/senda-ronda-4.html`.

## Decisiones (ronda 4)

- S: **Bisel**.
- Nombre: **Senda** (mayúscula inicial).
- Descriptor: **CONSULTORA** debajo, en mayúsculas, Red Hat Display Regular, mismo ancho que "Senda".
- Tipografía: **Red Hat Display** (Red Hat Text para textos largos).
- Paleta: **Señal**, con dudas sobre el rojo (se lee naranja). En ronda 5 se proponen Rojo puro, Carmín y Granate.
- La S tiene que medir el alto del bloque de texto completo.

Geometría del logo en `marca/logo/geometria.json`, generada con `marca/herramientas/construir_logo.py`.

## Preguntas abiertas para vos

1. ¿Quién es el cliente ideal en concreto (rubro, tamaño, cargo de quien contrata)?
2. ¿Cuál de los tres focos va a traer más facturación el primer año?
3. ¿La marca va a firmar como equipo ("Senda") o va a haber caras visibles?
4. ¿Tres consultoras o marcas que admires y tres que te parezcan exactamente lo que no querés ser?
5. ¿Hay alguna palabra o idea que te parezca que *tiene* que estar?

## Propuesta final (aprobada)

- **Símbolo:** S **Contrapeso** (dos medios círculos con barra, una pieza girada 180° respecto de la otra).
- **Nombre:** "Senda", Red Hat Display ExtraBold, interletrado −25.
- **Bajada:** "CONSULTORA", Red Hat Display Medium, 20% del nombre, mismo ancho que "Senda", interlineado 115%.
- **Composición:** S de 1,4 × el alto del bloque de texto, centrada; separación 0,85 × la barra.
- **Paleta Fiordo:** pizarra #16232B (fondo principal), niebla #E4EEF0, verde mar #075056, naranja #FF5B04 (la S).
- **Tipografía:** Red Hat Display (títulos) y Red Hat Text (textos).

Archivos finales en `marca/logo/final/` (SVG) y `marca/logo/final/png/` (PNG), generados con `marca/herramientas/logo_final.py`.
Manual en `marca/manual/senda-manual-de-marca.html`.

## Arquitectura de marca: Senda Estudio

- La unidad de implementación de IA se llama **Senda Estudio**. Mismo logo y mismos parámetros que la consultora; solo cambia la bajada: **ESTUDIO** en lugar de CONSULTORA, al mismo ancho que "Senda".
- Reparto: **Senda Consultora** diagnostica y recomienda (desarrollo comercial, investigación de mercado). **Senda Estudio** diseña y construye (IA y automatizaciones).
- Color que lidera: la consultora, pizarra; el estudio, verde mar con el logo en niebla.
- La palabra "estudio" queda reservada para la unidad. La investigación se llama "investigación de mercado", nunca "estudios de mercado".
- Frase de apoyo mientras el nombre se instala: "Diseñamos e implementamos IA en tu negocio".
- Archivos: `marca/logo/final/senda-estudio-*.svg` y sus PNG. La corta y el monograma son compartidos.
