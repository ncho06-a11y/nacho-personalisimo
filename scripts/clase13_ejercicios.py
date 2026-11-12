# =============================================================================
# Clase 13. Tránsito y calidad del aire, junio de 2024 — Ejercicios resueltos
# Versión en Python (pandas + matplotlib + statsmodels)
# =============================================================================
#
# LA TABLA (transito_aire_junio2024.csv): una fila por estación y hora
#   estacion   estación de calidad de aire (tres estaciones)
#   hora       fecha y hora de la medición
#   transito   vehículos por hora cerca de la estación
#   no2        dióxido de nitrógeno, promedio de la hora (µg/m³)
#   pm25       material particulado fino, promedio de la hora (µg/m³)
#
# CÓMO SE USA ESTE ARCHIVO
#   Correr desde la raíz del proyecto (nacho-personalisimo). Los datos están en
#   data/ y los gráficos se guardan en graficos/.
#   El archivo está dividido en celdas con #%%. En VS Code cada celda se
#   corre con Shift + Enter, de arriba hacia abajo.
#
# Paquetes (instalar una sola vez, en la terminal):
#   pip install pandas numpy matplotlib statsmodels
# =============================================================================

#%%
# =============================================================================
# PREPARACIÓN
# =============================================================================
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# Para que print() muestre todas las columnas de una tabla, sin cortarla con "...".
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

RUTA = "data/transito_aire_junio2024.csv"
GRAFICOS = Path("graficos")
GRAFICOS.mkdir(exist_ok=True)

COL_TRANSITO = "#2E86AB"
COL_NO2      = "#7B4B2A"
COL_PM25     = "#D4A373"
COL_OSCURO   = "#5C3A21"

# ---- La tabla original -------------------------------------------------------
# parse_dates le dice a pandas que la columna hora es una fecha.
aire = pd.read_csv(RUTA, parse_dates=["hora"])

# ---- Variables nuevas --------------------------------------------------------
datos = aire.copy()

# La hora del día, de 0 a 23.
datos["h"] = datos["hora"].dt.hour

# dayofweek da el día de la semana: lunes = 0, ..., sábado = 5, domingo = 6.
# np.where(condición, valor_si_se_cumple, valor_si_no)
datos["tipo_dia"] = np.where(datos["hora"].dt.dayofweek >= 5,
                             "fin de semana", "lunes a viernes")

# isin() da True cuando h es alguno de los valores de la lista.
datos["hora_pico"] = np.where(datos["h"].isin([7, 8, 9, 17, 18, 19]),
                              "hora pico", "resto")

# pd.cut() corta h en intervalos: de 0 a 5, de 6 a 11, de 12 a 17, de 18 a 23.
# El resultado es una variable categórica que guarda el orden de las franjas.
datos["franja"] = pd.cut(datos["h"], bins=[-1, 5, 11, 17, 23],
                         labels=["madrugada", "mañana", "tarde", "noche"])

# Tránsito relativo: 1 es lo habitual de la estación, 2 es el doble.
# transform("mean") pone en cada fila el promedio de su estación.
datos["transito_rel"] = datos["transito"] / datos.groupby("estacion")["transito"].transform("mean")

datos["transito_miles"] = datos["transito"] / 1000
datos["log_pm25"] = np.log(datos["pm25"])

# ---- Promedios por estación y franja (para el ejercicio 3) -------------------
# observed=True: solo las combinaciones que aparecen en los datos.
por_franja = (datos.groupby(["estacion", "franja"], observed=True)
                   [["transito", "transito_rel", "no2", "pm25"]]
                   .mean()
                   .reset_index())
print(por_franja.round(1))

ESTACIONES = sorted(datos["estacion"].unique())

# ---- Tres Cruces, solo las horas con NO2 (para los ejercicios 4 a 7) ---------
# .copy() hace una tabla nueva, a la que después se le pueden agregar columnas.
tc = datos[(datos["estacion"] == "Tres Cruces") & datos["no2"].notna()].copy()

# smf.ols("y ~ x1 + x2", data=tabla) busca la recta, como lm() en R.
# Las filas con algún faltante en esas columnas quedan afuera.
modelo_tc3 = smf.ols("no2 ~ transito_miles + pm25", data=tc).fit()
print(modelo_tc3.params)
print(modelo_tc3.rsquared)          # 0,47


#%%
# =============================================================================
# EJERCICIO 1. FALTANTES
# =============================================================================
# Este código cuenta los faltantes de la tabla aire:
#
# faltantes = aire[["transito", "no2", "pm25"]].isna().groupby(aire["estacion"]).sum()
# print(faltantes)
#
# isna() pone True donde falta el dato. sum() cuenta los True de cada estación.
#
# 1. Copiar el código y cambiarlo para contar los faltantes de la tabla datos.
# 2. Agregar a la lista las variables nuevas: franja, tipo_dia, transito_rel
#    y log_pm25.
# 3. ¿Qué variable nueva tiene faltantes? ¿De dónde salen?
# -----------------------------------------------------------------------------

columnas = ["transito", "no2", "pm25", "franja", "tipo_dia", "transito_rel", "log_pm25"]
faltantes = datos[columnas].isna().groupby(datos["estacion"]).sum()
print(faltantes)

# 3. Solo log_pm25 tiene faltantes entre las variables nuevas, y son los mismos
#    que los de pm25 (0 en Curva de Maronias, 144 en Museo Romántico y 326 en
#    Tres Cruces). Si falta pm25 no se puede calcular su logaritmo: una variable
#    que se calcula a partir de otra hereda los faltantes de ella.


#%%
# =============================================================================
# EJERCICIO 2. ¿ESTÁ BIEN DEFINIDA LA HORA PICO?
# =============================================================================
# hora_pico marca las horas 7, 8, 9, 17, 18 y 19.
# El gráfico muestra el tránsito promedio de cada hora del día en Tres Cruces,
# de lunes a viernes. Las horas pico están en color oscuro.

print(datos["hora_pico"].value_counts())

semana_tc = datos[(datos["estacion"] == "Tres Cruces") &
                  (datos["tipo_dia"] == "lunes a viernes")]
por_hora = semana_tc.groupby(["h", "hora_pico"])["transito"].mean().reset_index()

# map() cambia cada valor por el color que le toca en el diccionario.
colores = por_hora["hora_pico"].map({"hora pico": COL_OSCURO, "resto": "lightgrey"})

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(por_hora["h"], por_hora["transito"], color=colores)
ax.set_title("Tránsito promedio por hora del día, Tres Cruces, lunes a viernes")
ax.set_xlabel("Hora del día (en color: hora pico)")
ax.set_ylabel("Vehículos por hora")
plt.savefig(GRAFICOS / "clase13_ej2_hora_pico_original.png", dpi=150)
plt.show()

# 1. Mirar el gráfico: ¿las barras oscuras son las más altas?
#    Anotar qué horas están mal clasificadas.
# 2. Crear en datos una variable nueva, con el nombre que elijan, que marque
#    las horas que según el gráfico tienen más tránsito.
# 3. Repetir el gráfico con la variable nueva en lugar de hora_pico.
# -----------------------------------------------------------------------------

# 1. No: las 7, las 18 y las 19 están marcadas como hora pico pero tienen menos
#    tránsito que las horas de 10 a 16. No hay dos picos: el tránsito es alto
#    todo el día, de 8 a 17.

# 2. Hay más de una respuesta válida. Una: las horas de 8 a 17.
datos["transito_alto"] = np.where((datos["h"] >= 8) & (datos["h"] <= 17),
                                  "tránsito alto", "resto")
print(datos["transito_alto"].value_counts())    # 900 tránsito alto y 1260 resto

# 3. El mismo código, cambiando hora_pico por transito_alto.
semana_tc = datos[(datos["estacion"] == "Tres Cruces") &
                  (datos["tipo_dia"] == "lunes a viernes")]
por_hora = semana_tc.groupby(["h", "transito_alto"])["transito"].mean().reset_index()
colores = por_hora["transito_alto"].map({"tránsito alto": COL_OSCURO, "resto": "lightgrey"})

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(por_hora["h"], por_hora["transito"], color=colores)
ax.set_title("Tránsito promedio por hora del día, Tres Cruces, lunes a viernes")
ax.set_xlabel("Hora del día (en color: tránsito alto)")
ax.set_ylabel("Vehículos por hora")
plt.savefig(GRAFICOS / "clase13_ej2_transito_alto.png", dpi=150)
plt.show()
# Ojo: en el diccionario de map() también hay que cambiar el nombre de la
# categoría. Si queda "hora pico", ninguna barra recibe el color oscuro.


#%%
# =============================================================================
# EJERCICIO 3. PM2.5 POR FRANJA HORARIA
# =============================================================================
# Este gráfico muestra el tránsito relativo por franja, una estación en cada
# panel. La línea punteada en 1 marca lo habitual de cada estación.

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
for ax, est in zip(axes, ESTACIONES):
    parte = por_franja[por_franja["estacion"] == est]
    ax.bar(parte["franja"].astype(str), parte["transito_rel"], color=COL_TRANSITO)
    ax.axhline(1, color="grey", linestyle="--")
    ax.set_title(est)
axes[0].set_ylabel("Tránsito relativo (1 = media de la estación)")
fig.suptitle("Tránsito por franja horaria, relativo a la media de la estación")
fig.tight_layout()     # acomoda los títulos para que no se pisen
plt.savefig(GRAFICOS / "clase13_ej3_transito_por_franja.png", dpi=150)
plt.show()

# La tabla por_franja también tiene el promedio de pm25.
#
# 1. Copiar el código del gráfico y cambiarlo para graficar pm25 en lugar de
#    transito_rel. Cambiar también el título, el nombre del eje y el color
#    (COL_PM25).
# 2. La línea punteada en 1 ya no tiene sentido: sacarla.
# 3. ¿En qué franja es máximo el PM2.5? ¿Es la misma que la del tránsito?
# -----------------------------------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
for ax, est in zip(axes, ESTACIONES):
    parte = por_franja[por_franja["estacion"] == est]
    ax.bar(parte["franja"].astype(str), parte["pm25"], color=COL_PM25)
    ax.set_title(est)
axes[0].set_ylabel("PM2.5 (µg/m³)")
fig.suptitle("PM2.5 promedio por franja horaria")
fig.tight_layout()
plt.savefig(GRAFICOS / "clase13_ej3_pm25_por_franja.png", dpi=150)
plt.show()

# 3. El tránsito es máximo de tarde; el PM2.5 es máximo de noche (en Tres
#    Cruces: 31,9 de noche contra 17,2 de tarde). No es la misma franja: el
#    PM2.5 de una franja no sigue al tránsito de esa misma franja.


#%%
# =============================================================================
# EJERCICIO 4. AGREGAR UNA VARIABLE AL MODELO
# =============================================================================
# El modelo modelo_tc3 explica el NO2 con el tránsito y el PM2.5:
#
# modelo_tc3 = smf.ols("no2 ~ transito_miles + pm25", data=tc).fit()
# print(modelo_tc3.params)
# print(modelo_tc3.rsquared)
#
# 1. Copiar el código y agregar la variable franja al modelo.
#    Guardarlo como modelo_tc4.
# 2. Mostrar los coeficientes y el R².
# 3. ¿Mejoró el R²? ¿Mucho o poco?
# -----------------------------------------------------------------------------

modelo_tc4 = smf.ols("no2 ~ transito_miles + pm25 + franja", data=tc).fit()
print(modelo_tc4.params)
print(modelo_tc4.rsquared)

# 3. El R² pasa de 0,47 a 0,49: mejora poco, aunque el modelo tiene tres
#    coeficientes más.
# Cómo leer los coeficientes de la franja: la madrugada es la referencia.
#   franja[T.noche] = 6,2 quiere decir que, a igual tránsito y PM2.5, una
#   hora de la noche tiene 6,2 µg/m³ más de NO2 que una de la madrugada.
#   (En R el mismo coeficiente se llama franjanoche.)


#%%
# =============================================================================
# EJERCICIO 5. UNA VARIABLE BINARIA A PARTIR DEL RESULTADO
# =============================================================================
# Para ver si cada coeficiente se distingue de cero:
#
# print(modelo_tc4.summary())
#
# De las tres franjas, solo la noche tiene un coeficiente que se distingue
# de cero.
#
# 1. Crear en tc la variable noche: vale 1 si la franja es "noche" y 0 si no.
#    Ayuda: np.where(condición, 1, 0)
# 2. Ajustar modelo_tc5 con transito_miles, pm25 y noche (sin franja).
# 3. Mostrar los coeficientes y el R². ¿Cuánto suma la noche?
# -----------------------------------------------------------------------------

print(modelo_tc4.summary())

tc["noche"] = np.where(tc["franja"] == "noche", 1, 0)

modelo_tc5 = smf.ols("no2 ~ transito_miles + pm25 + noche", data=tc).fit()
print(modelo_tc5.params)
print(modelo_tc5.rsquared)

# 3. La noche suma 3,8 µg/m³ de NO2 (coeficiente de noche), a igual tránsito y
#    PM2.5, respecto de cualquier otra franja. Con una sola variable binaria el
#    R² es 0,48: casi el mismo que con las tres franjas (0,49). Se pierde casi
#    nada con un modelo más simple.


#%%
# =============================================================================
# EJERCICIO 6. INTERACCIONES
# =============================================================================
# Este gráfico muestra la nube de Tres Cruces con un color por franja, y una
# recta para cada franja.

COL_FRANJA = {"madrugada": "#0072B2", "mañana": "#E69F00",
              "tarde": "#009E73", "noche": "#CC79A7"}

fig, ax = plt.subplots(figsize=(8, 5))
for f in ["madrugada", "mañana", "tarde", "noche"]:
    parte = tc[tc["franja"] == f]
    ax.scatter(parte["transito_miles"], parte["no2"], s=15, alpha=0.6,
               color=COL_FRANJA[f], label=f)
    # np.polyfit(x, y, 1) da la pendiente y la ordenada de la recta.
    pendiente, ordenada = np.polyfit(parte["transito_miles"], parte["no2"], 1)
    x = np.array([parte["transito_miles"].min(), parte["transito_miles"].max()])
    ax.plot(x, ordenada + pendiente * x, color=COL_FRANJA[f], linewidth=2)
ax.set_title("Tránsito y NO2 en Tres Cruces, por franja horaria")
ax.set_xlabel("Miles de vehículos por hora")
ax.set_ylabel("NO2 (µg/m³)")
ax.legend()
plt.savefig(GRAFICOS / "clase13_ej6_transito_no2_por_franja.png", dpi=150)
plt.show()
# Qué vemos: cada franja tiene su recta, y no son paralelas.

# Un modelo con interacción deja que la pendiente cambie según la franja.
# En la fórmula se escribe * en lugar de +:
#
# modelo_tc6 = smf.ols("no2 ~ transito_miles * franja", data=tc).fit()
#
# 1. Mirar el gráfico: ¿qué franja tiene la recta más empinada?
# 2. Crear en tc una variable binaria para esa franja: 1 si la hora es de
#    esa franja, 0 si no.
# 3. Ajustar modelo_tc7 con la interacción entre transito_miles y la
#    variable nueva. Mostrar los coeficientes y el R².
# -----------------------------------------------------------------------------

# 1. La madrugada tiene la recta más empinada: unos 2,9 µg/m³ de NO2 por cada
#    mil vehículos por hora, contra entre 0,5 y 1,1 en las otras franjas.
print({f: round(np.polyfit(tc.loc[tc["franja"] == f, "transito_miles"],
                           tc.loc[tc["franja"] == f, "no2"], 1)[0], 2)
       for f in ["madrugada", "mañana", "tarde", "noche"]})

# 2. Variable binaria para la madrugada.
tc["madrugada"] = np.where(tc["franja"] == "madrugada", 1, 0)

# 3. En la fórmula, transito_miles * madrugada equivale a transito_miles +
#    madrugada + transito_miles:madrugada.
modelo_tc7 = smf.ols("no2 ~ transito_miles * madrugada", data=tc).fit()
print(modelo_tc7.params)
print(modelo_tc7.rsquared)


#%%
# =============================================================================
# EJERCICIO 7. ¿QUÉ PASA EN LA TARDE?
# =============================================================================
# En el gráfico del ejercicio 6 los puntos de la tarde forman dos grupos
# separados.
#
# 1. Crear la tabla tarde con las filas de tc cuya franja es "tarde".
# 2. Copiar el código del gráfico del ejercicio 6 y cambiarlo para usar la
#    tabla tarde y colorear por tipo_dia en lugar de franja.
#    Ayuda: hay que cambiar la lista que recorre el for por
#    ["lunes a viernes", "fin de semana"], y armar un diccionario de colores
#    nuevo con esas dos categorías.
# 3. ¿Qué son los dos grupos?
# -----------------------------------------------------------------------------

tarde = tc[tc["franja"] == "tarde"].copy()

COL_TIPO_DIA = {"lunes a viernes": "#0072B2", "fin de semana": "#D55E00"}

fig, ax = plt.subplots(figsize=(8, 5))
for t in ["lunes a viernes", "fin de semana"]:
    parte = tarde[tarde["tipo_dia"] == t]
    ax.scatter(parte["transito_miles"], parte["no2"], s=15, alpha=0.6,
               color=COL_TIPO_DIA[t], label=t)
    pendiente, ordenada = np.polyfit(parte["transito_miles"], parte["no2"], 1)
    x = np.array([parte["transito_miles"].min(), parte["transito_miles"].max()])
    ax.plot(x, ordenada + pendiente * x, color=COL_TIPO_DIA[t], linewidth=2)
ax.set_title("Tránsito y NO2 en Tres Cruces, de tarde, por tipo de día")
ax.set_xlabel("Miles de vehículos por hora")
ax.set_ylabel("NO2 (µg/m³)")
ax.legend()
plt.savefig(GRAFICOS / "clase13_ej7_tarde_por_tipo_dia.png", dpi=150)
plt.show()

print(tarde.groupby("tipo_dia")[["transito", "no2"]].agg(["count", "mean"]).round(1))

# 3. Los dos grupos son los días de semana (lunes a viernes) y los fines de
#    semana. De lunes a viernes el tránsito de la tarde está entre 38 y 49 mil
#    vehículos por hora (NO2 promedio 50); los fines de semana, entre 21 y 39
#    mil (NO2 promedio 42). La franja "tarde" mezclaba dos situaciones
#    distintas, y por eso su nube no sigue una sola recta.
