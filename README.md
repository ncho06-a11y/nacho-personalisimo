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
│   ├── clase02/ ... clase05/
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

### Clase 7 (17/09) — Carga de datos, rutas y transformación: ozono en Montevideo

**Qué vimos:** rutas que funcionan en cualquier computadora (buscar la raíz del
proyecto, como `here::here()` en R, y armar las rutas desde ahí), limpieza de texto mal codificado, fechas con `parse_dates` y `.dt`,
agregación (minutal → horaria → diaria → mensual), media móvil de 8 horas, días sobre
el umbral de la OMS, rachas y patrones de faltantes (explícitos e implícitos).

**Lo que hice:** `scripts/ozono_carga_y_transformacion.py`
Gráfico: `graficos/ozono_figure_1.png`

> Nota: este script necesita `data/o3_01_2024_04_2024.csv`, que no está subido al
> repositorio (es pesado). Hay que bajarlo y ponerlo en `data/` para correrlo.

### Clase 12 (13/10) — Tránsito y calidad del aire

**Qué vimos:** crear variables nuevas (hora, tipo de día, franja horaria, tránsito
relativo, logaritmos), faltantes que se heredan, promedios por grupo y regresión
lineal con `statsmodels`.

**Lo que hice:** `scripts/clase12_ejercicios.py` — los 7 ejercicios resueltos con
las respuestas comentadas en el código.
Gráficos: `graficos/clase12_*.png`

**Datos:** `data/transito_aire_junio2024.csv`
