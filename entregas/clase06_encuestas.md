# Clase 6 — Diseño de encuestas: ejercicios

## Ejercicio 1: de la tabla al cuestionario (cafetería de la facultad)

La idea es escribir el cuestionario que da la tabla que pidieron
(`id`, `frecuencia`, `prod_*`, `atencion`, `pago_*`, `estudiante`, `edad`, `mejora`).

---

**Encuesta sobre la cafetería de la facultad**

Hola, estamos haciendo una encuesta corta para saber cómo es el servicio de la cafetería
y qué se podría mejorar. Lleva unos 2 minutos.

Las respuestas son anónimas y se usan solo para este trabajo del curso
(Ley 18.331 de datos personales). Podés dejar de responder cuando quieras.

☐ Acepto participar

Instrucciones: marcá con una X. Donde dice "marcá todas", podés marcar más de una.

---

**P1.** En los últimos 30 días, ¿cuántas veces compraste algo en la cafetería?
☐ Nunca  ☐ 1 a 3 veces  ☐ 4 a 8 veces  ☐ Más de 8 veces
→ **Si marcaste "Nunca", pasá a la P5.**

**P2.** En los últimos 30 días, ¿qué compraste en la cafetería? (marcá todas)
☐ Café  ☐ Comida  ☐ Bebidas frías  ☐ Otros

**P3.** En los últimos 30 días, ¿cómo calificarías la atención?
1 Muy mala · 2 · 3 · 4 · 5 Muy buena

**P4.** En los últimos 30 días, ¿cómo pagaste en la cafetería? (marcá todas)
☐ Efectivo  ☐ Tarjeta  ☐ Transferencia

**P5.** ¿Sos estudiante de esta facultad?
☐ Sí  ☐ No

**P6.** ¿Qué mejorarías de la cafetería?
_______________________________

**P7.** ¿Cuántos años tenés?  ____ años

Gracias por responder.

---

### De qué columna sale cada pregunta

| Pregunta | Tipo de pregunta | Columnas | Tipo de variable |
|---|---|---|---|
| (automático) | — | `id` | entero |
| P1 | opción única con orden | `frecuencia` | ordinal |
| P2 | selección múltiple (4 opciones) | `prod_cafe`, `prod_comida`, `prod_frias`, `prod_otros` | binarias |
| P3 | escala 1 a 5 | `atencion` | ordinal |
| P4 | selección múltiple (3 opciones) | `pago_efectivo`, `pago_tarjeta`, `pago_transferencia` | binarias |
| P5 | sí / no | `estudiante` | binaria |
| P6 | abierta | `mejora` | texto |
| P7 | número | `edad` | cuantitativa |

**7 preguntas → 13 columnas.**

Cosas que revisé:
- Todas las preguntas sobre la cafetería dicen "en los últimos 30 días".
- Después de P1 hay un filtro: si es "Nunca", salta a P5. Por eso `prod_*`, `atencion`
  y `pago_*` quedan en NA para esas personas, pero por diseño (faltante estructural),
  no porque no quisieran contestar.
- Productos y medios de pago son de "marcá todas", no hay una opción "Ambos".
- La escala de atención tiene los extremos con nombre y va de peor (1) a mejor (5).
- La edad va al final porque es un dato más personal.

---

## Ejercicio 2 (para la bitácora): preguntas con problemas

**1. ¿Está conforme con lo que gasta en comida y en transporte?**
- Problema: pregunta dos cosas a la vez (tiene una "y"). Si estoy conforme con la comida
  pero no con el transporte, no sé qué contestar.
- Arreglada: dos preguntas.
  - *En los últimos 30 días, ¿qué tan conforme está con lo que gastó en comida?* 1 Nada conforme … 5 Muy conforme
  - *En los últimos 30 días, ¿qué tan conforme está con lo que gastó en transporte?* 1 Nada conforme … 5 Muy conforme
- Variable: 2 columnas ordinales (`conforme_comida`, `conforme_transporte`).

**2. ¿No le parece que gasta demasiado en salidas?**
- Problema: está armada para que contestes "sí" (induce la respuesta) y tiene una negación,
  así que contestar "no" es confuso.
- Arreglada: *¿Cuánto gastó en salidas en los últimos 30 días? $ ____*
- Variable: 1 columna cuantitativa (`gasto_salidas`). Si se pregunta por tramos, sería ordinal.

**3. ¿Cuánto gastó últimamente en ropa?**
- Problema: "últimamente" no dice cuánto tiempo. Cada uno va a pensar en otro período.
- Arreglada: *¿Cuánto gastó en ropa en los últimos 30 días? $ ____*
- Variable: 1 columna cuantitativa (`gasto_ropa`).

**4. Gasto en transporte: ☐ $0 a $1.000 ☐ $1.000 a $3.000 ☐ $3.000 a $6.000**
- Problema: los tramos se pisan (1.000 y 3.000 están en dos casillas) y no hay opción
  para más de 6.000.
- Arreglada: *¿Cuánto gastó en transporte en los últimos 30 días?*
  ☐ Nada ☐ Hasta $1.000 ☐ $1.001 a $3.000 ☐ $3.001 a $6.000 ☐ Más de $6.000
- Variable: 1 columna ordinal (`gasto_transporte`).

**5. ¿Cómo paga sus gastos? ☐ Efectivo ☐ Tarjeta ☐ Ambos ☐ Transferencia**
- Problema: "Ambos" muestra que se puede pagar de más de una forma, así que en realidad es
  selección múltiple. Además "Ambos" no dice cuáles dos (¿y si uso transferencia también?).
- Arreglada: *En los últimos 30 días, ¿con qué medios pagó sus gastos? (marque todas)*
  ☐ Efectivo ☐ Tarjeta ☐ Transferencia
- Variable: 3 columnas binarias (`pago_efectivo`, `pago_tarjeta`, `pago_transferencia`).

**6. (Primera pregunta) ¿Cuál es el ingreso mensual exacto de su hogar?**
- Problema: es una pregunta sensible y está al principio, así que mucha gente va a abandonar
  la encuesta. Además pedir el monto "exacto" es difícil de saber y de querer contestar.
- Arreglada: moverla al final y con tramos:
  *¿En cuál de estos tramos está el ingreso mensual de su hogar?*
  ☐ Hasta $30.000 ☐ $30.001 a $60.000 ☐ $60.001 a $100.000 ☐ Más de $100.000 ☐ Prefiero no contestar
- Variable: 1 columna ordinal (`ingreso_hogar`). "Prefiero no contestar" se codifica aparte,
  distinto de dejarla en blanco.
