# Introducción a la Ciencia de Datos — repositorio de Nacho

Curso de Introducción a la Ciencia de Datos, FCEE, Universidad de Montevideo
(prof. Joselina Davyt-Colo). Acá está todo lo que fui haciendo en clase y en las tareas.

## Cómo está organizado

```
nacho-personalisimo/
├── README.md        <- este archivo (con la bitácora)
├── data/            <- los datos (csv)
├── scripts/         <- mi código en Python
├── graficos/        <- los gráficos que salen de los scripts
├── material/        <- material de la profe (slides y guías)
│   ├── clase02/ ... clase10/
│   └── guias/
└── entregas/        <- respuestas entregadas
```

## Cómo correr los scripts

1. Instalar los paquetes (una sola vez):

   ```bash
   pip install pandas numpy matplotlib statsmodels
   ```

   Si `pip` no se reconoce, usar `py -m pip install ...` en Windows o
   `python3 -m pip install ...` en Mac (ver `material/guias/python_pip_no_reconocido.pdf`).

2. Abrir la carpeta del proyecto en VS Code y correr los scripts **desde la raíz**
   (porque buscan los datos en `data/`). Por ejemplo:

   ```bash
   python scripts/clase02_datos_sinteticos.py
   ```

   También se pueden correr celda por celda (`# %%`) con Shift + Enter.

---

## Bitácora

### Clase 2 (18/08) — Generación de datos (caja negra / DGP)

**Qué vimos:** los datos no "existen", se construyen midiendo. Todo dataset sale de un
Proceso Generador de Datos (DGP) que es como una caja negra: solo vemos lo que sale.
Hicimos la dinámica de tocar objetos sin verlos y anotar variables de distintos tipos:
nominales (textura), ordinales (rigidez), numéricas discretas (aristas), continuas (peso)
y metadatos (certeza del observador). Después vimos datos simulados vs sintéticos,
bootstrap (muestreo con reemplazo) y generación paramétrica con una normal, y sus
limitaciones (reality gap, sesgo, datos "fantasma").

**Lo que hice:**
- `scripts/clase02_tarea_objetos.py` — tarea: el dataframe con los objetos que tocamos
  en clase, con `forma` y `textura` como categóricas y `rigidez` como ordinal.
- `scripts/clase02_datos_sinteticos.py` — ejercicio: armar el dataframe de la caja,
  hacer bootstrap a 100 filas, generar 500 pesos sintéticos con una normal, generar
  categóricas y una binaria sintéticas con las proporciones reales, y comparar.
  Gráfico: `graficos/clase02_pesos_real_vs_sintetico.png`.

**Lo que aprendí:** el bootstrap solo repite lo que ya hay; la normal inventa valores
nuevos pero salen pesos negativos (hay que cortarlos) y mezcla grupos distintos en una
sola campana. Sortear cada variable por separado pierde la relación entre ellas.

**Material:** `material/clase02/`

### Clase 3 (01/09) — Fundamentos (objetos, tipos y errores)

**Qué vimos:** formas de ejecutar código (línea, archivo, celda) y por qué importa el
orden; cómo leer un error (`NameError`, `TypeError`, `FileNotFoundError`); vectores,
listas, tipos de datos, funciones vs métodos y rutas relativas.

**Lo que hice:** el cuestionario de opción múltiple de la clase.
- Respuestas: `entregas/clase03_fundamentos_respuestas.pdf`

**Material:** `material/clase03/` (slides en `.qmd` y `.html`)

### Clase 4 (03/09) — Carga de datos y flujo de análisis

**Qué vimos:** el flujo de un análisis de datos (importar → ordenar → transformar /
visualizar / modelar → comunicar): ingesta, perfilado (*data profiling*), limpieza,
exploración (EDA), transformación y entrega de resultados. Tipos de carga (completa e
incremental), formatos de origen (CSV, Excel, JSON, XML, Parquet, APIs), el rol de
PostgreSQL y el debate de si Excel es una base de datos (no lo es: no tiene tipos
estrictos ni integridad, y tiene un límite de filas).

**Lo que hice (práctica de carga y perfilado):** cargar un CSV con rutas relativas
(`pathlib`), verificar que el archivo existe, y hacer un primer perfilado: dimensiones,
id, faltantes y duplicados.
- `scripts/rupe_exploracion.py` — carga del RUPE (proveedores del Estado, julio 2026)
  probando encoding y separador; proveedores por estado y por departamento; faltantes.
- `scripts/residuos_carga_y_profiling.py` — carga de las pesadas de la estación de
  transferencia de residuos 2023 (1222 filas, 41 columnas); valores únicos para buscar
  un id, faltantes, vacíos y duplicados.

**Datos:** `data/rupe-julio-2026.csv`, `data/diccionario_datos_rupe.csv`,
`data/cantidad_de_residuos_en_la_estacion_de_transferencia_2023.csv`

**Material:** `material/clase04/`

### Clase 5 — Seudocódigo

**Qué vimos:** un programa es una serie de pasos en orden. El seudocódigo sirve para
pensar la lógica (y qué hacer si algo falla) antes de pelearse con la sintaxis de
Python. Ejemplo: leer un CSV en UTF-8 y, si falla, reintentar con latin-1.

**Lo que hice:** `scripts/clase05_seudocodigo.py`
- Ejercicio 1: pasar a Python el seudocódigo de filtrar temperaturas mayores a 20,
  primero con un `for` paso por paso y después en una línea. Resultado: `[22, 25, 30]`.
- Ejercicio 2: la ingesta con control de encoding, probada con el diccionario del RUPE
  (falla en UTF-8 y lo lee bien con latin-1).
- Ejercicio 3: un seudocódigo propio (contar días calurosos y sacar el promedio) y su código.

**Material:** `material/clase05/`

### Clase 6 — Diseño de encuestas

**Qué vimos:** cuándo conviene hacer una encuesta; fuentes de datos (preferencias
declaradas, reveladas y huella digital); la regla de **diseñar la tabla antes que el
formulario**; operacionalización (concepto → dimensión → indicador → pregunta → variable);
niveles de medición (nominal, ordinal, intervalo, razón); validez y confiabilidad;
fuentes de error (cobertura, muestreo, no respuesta, medición); tipos de pregunta y qué
columnas generan (la selección múltiple da una binaria por opción); redacción (una idea
por pregunta, lenguaje neutro, período de referencia, categorías exhaustivas y
excluyentes); preguntas filtro y faltantes estructurales; libro de códigos; y datos
personales según la Ley 18.331.

**Lo que hice:**
- `entregas/clase06_encuestas.md`:
  - Ejercicio 1: el cuestionario completo para la cafetería de la facultad (título,
    introducción, consentimiento, instrucciones, preguntas y cierre). 7 preguntas →
    13 columnas, con filtro después de la P1.
  - Ejercicio 2 (para la bitácora): las 6 preguntas con problemas. Para cada una, el
    problema, la pregunta arreglada y qué variable genera:

    | # | Problema | Variable que genera |
    |---|---|---|
    | 1 | Pregunta dos cosas a la vez | 2 ordinales (escala 1–5) |
    | 2 | Induce la respuesta y tiene negación | 1 cuantitativa (o ordinal si es por tramos) |
    | 3 | No tiene período de referencia | 1 cuantitativa |
    | 4 | Tramos que se pisan y no cubren todo | 1 ordinal |
    | 5 | Selección múltiple disfrazada ("Ambos") | 3 binarias |
    | 6 | Sensible, exacta y al principio | 1 ordinal (por tramos, al final) |

- `scripts/clase06_encuesta_cafeteria.py` — armo la tabla que sale de mi cuestionario con
  respuestas inventadas, declaro los tipos según el libro de códigos y muestro que hay dos
  tipos de faltantes (por el filtro y por no respuesta) que en la tabla se ven igual.

**Material:** `material/clase06/`

### Clase 7 (17/09) — Carga de datos, rutas y transformación: ozono en Montevideo

**Qué vimos:** rutas que funcionan en cualquier computadora (buscar la raíz del
proyecto, como `here::here()` en R, y armar las rutas desde ahí), limpieza de texto mal codificado, fechas con `parse_dates` y `.dt`,
agregación (minutal → horaria → diaria → mensual), media móvil de 8 horas, días sobre
el umbral de la OMS, rachas y patrones de faltantes (explícitos e implícitos).

**Lo que hice:** `scripts/ozono_carga_y_transformacion.py`
Gráfico: `graficos/ozono_figure_1.png`

**Material:** `material/clase07/`

> Nota: este script necesita `data/o3_01_2024_04_2024.csv`, que no está subido al
> repositorio (es pesado). Hay que bajarlo y ponerlo en `data/` para correrlo.

### Clase 8 — Visualización básica: las partes de un gráfico

**Qué vimos:** las partes de un gráfico (datos, geometría —líneas, puntos, barras—,
ejes y escalas, etiquetas, título y fuente) usando de ejemplo el gráfico del ozono de la
clase 7, y cómo corregirlo con `matplotlib`.

**Lo que hice:** `scripts/clase08_partes_de_un_grafico.py`
- Rehice el gráfico original y anoté qué está mal: el eje x muestra 1.0, 1.5, 2.0… en vez
  de meses; "Fecha" y "Valores" no dicen qué se mide ni en qué unidad; el eje y empieza en
  24 y exagera la caída; no tiene fuente; el título no dice que es un promedio.
- Mi versión corregida: meses con nombre, eje y desde 0, unidad (µg/m³), valor en cada
  punto, título claro y fuente.
- Apliqué lo mismo a otro dataset: toneladas por tipo de residuo en la estación de
  transferencia (barras horizontales porque los nombres son largos). Casi todo, unas
  7.400 toneladas, es residuo domiciliario.

Gráficos: `graficos/clase08_ozono_original.png`, `graficos/clase08_ozono_corregido.png`,
`graficos/clase08_residuos_por_tipo.png`

**Material:** `material/clase08/`

### Clase 9 — Unión de fuentes y gráficos por grupo

**Qué vimos:** convertir en función un bloque que se repite (cargar y limpiar cada
archivo); unir dos fuentes con una clave (estación + hora) y ver qué se pierde con un
*inner join* frente a un *left join*; un color por grupo con leyenda; perfil por hora del
día; boxplot; dispersión entre dos variables y correlación; cortar la hora en franjas y
mirar la misma pregunta en varios paneles.

**Lo que hice:** `scripts/clase09_union_y_graficos_por_grupo.py`. En clase se usó ozono
y PM2.5 de enero a abril, archivos que no tengo en el repo. Lo hice con
`transito_aire_junio2024.csv`, que tiene el mismo problema: el NO2 se mide solo en
algunas estaciones y el PM2.5 en todas. Separé NO2 y PM2.5 como dos fuentes y las uní.

**Preguntas para la bitácora:**
1. *¿Qué estaciones quedaron fuera de la unión y por qué?* Museo Romántico, porque ahí
   no se mide NO2 y no tiene filas para aparear. Quedan 946 filas, todas las de NO2; se
   pierden 744 de PM2.5 (las 576 de Museo Romántico y horas de las otras dos estaciones
   con PM2.5 pero sin NO2). No desaparecen: siguen en su tabla.
2. *¿Y con left join?* Se queda con todas las filas de la tabla de la izquierda. Con NO2
   a la izquierda quedan 946 y ninguna con PM2.5 vacío. Con PM2.5 a la izquierda quedan
   1690 y 744 tienen el NO2 vacío (NaN): son las que no encontraron pareja.
3. *¿Qué cambia con los cortes (-1, 6, 12, 19, 23)?* Cambia cuántas horas hay en cada
   panel y la correlación: la noche pasa a tener 4 horas y su r sube de 0,60 a 0,72,
   porque las 18 y 19 (mucho tránsito) pasan a la tarde. Lo que se ve depende de dónde
   se corta.
4. *Dos tablas que se puedan unir y su clave:* el conteo de tránsito y las mediciones de
   aire, por estación + hora. Las pesadas de residuos se podrían unir con una tabla de
   circuitos por `nomenclatura_circuito`.

Gráficos: `graficos/clase09_*.png`

**Material:** `material/clase09/`

### Clase 10 — ¿Se ve el tránsito en la calidad del aire?

**Qué vimos:** una investigación paso a paso con el conteo vehicular, el NO2 y el PM2.5
de junio de 2024: dónde se mide y qué estación elegir; mirar una semana; el día típico;
la correlación "cruda"; sacar el ciclo diario (desvíos respecto de lo habitual de cada
hora); correlación con el tránsito de *k* horas antes (rezagos); comparar con el azar
corriendo el tránsito días enteros; y un modelo simple: *lo habitual de la hora + lo que
agrega el tránsito*.

**Lo que hice:** `scripts/clase10_transito_y_aire.py`. Los pasos de la clase, más simples,
con la tabla por hora de Tres Cruces (`data/transito_aire_junio2024.csv`). Resultados:

| | NO2 | PM2.5 |
|---|---|---|
| Correlación cruda con el tránsito | 0,59 | −0,02 |
| Correlación sin el ciclo diario | 0,20 | −0,02 |
| Mejor rezago | 2 h (r = 0,23) | 13 h (r = 0,18) |
| R² solo lo habitual de la hora | 0,47 | 0,19 |
| R² habitual + tránsito | 0,50 | 0,22 |

- Casi toda la correlación cruda del NO2 era el ritmo del día, pero queda algo: con el
  tránsito corrido al azar, ninguna de las 25 corridas llega a la correlación real.
- El NO2 responde enseguida al tránsito (sale del escape y se va rápido); el PM2.5 tarda
  como medio día (se va juntando), por eso su pico es de noche.
- Lo que el modelo no explica es lo que no pusimos: viento, lluvia, temperatura y otras
  fuentes.

Gráficos: `graficos/clase10_*.png`

**Material:** `material/clase10/`

### Clase 12 (13/10) — Tránsito y calidad del aire

**Qué vimos:** crear variables nuevas (hora, tipo de día, franja horaria, tránsito
relativo, logaritmos), faltantes que se heredan, promedios por grupo y regresión
lineal con `statsmodels`.

**Lo que hice:** `scripts/clase12_ejercicios.py` — los 7 ejercicios resueltos con
las respuestas comentadas en el código.
Gráficos: `graficos/clase12_*.png`

**Datos:** `data/transito_aire_junio2024.csv`
