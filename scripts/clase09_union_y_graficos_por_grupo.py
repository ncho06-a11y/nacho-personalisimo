# %%
# Clase 9 - Union de fuentes y graficos por grupo
# Hago lo de la clase (unir dos fuentes, color por grupo, boxplot, dispersion, paneles)
# y respondo las preguntas para la bitacora.
#
# En la clase se uso ozono y PM2.5 (ene-abr 2024). Esos archivos no los tengo en el repo,
# asi que uso data/transito_aire_junio2024.csv, que tiene el mismo problema:
# el NO2 se mide solo en algunas estaciones y el PM2.5 en todas.
# Separo esa tabla en dos fuentes (una de NO2 y otra de PM2.5) y las vuelvo a unir.
#
# Correr desde la carpeta del proyecto: python scripts/clase09_union_y_graficos_por_grupo.py

import pandas as pd
import matplotlib.pyplot as plt

datos = pd.read_csv("data/transito_aire_junio2024.csv", parse_dates=["hora"])

# %%
# 1. Una funcion para "cargar" cada contaminante (como cargar_aire() de la clase)
# Se queda con hora, estacion y la medicion, sin las filas sin dato.
def cargar_contaminante(tabla, columna):
    t = tabla[["hora", "estacion", columna]]
    t = t.dropna(subset=[columna])
    return t

no2 = cargar_contaminante(datos, "no2")
pm = cargar_contaminante(datos, "pm25")

print("Estaciones con NO2:", no2["estacion"].unique())
print("Estaciones con PM2.5:", pm["estacion"].unique())

# %%
# 2. Unir con inner join (solo quedan las filas que estan en las dos)
# La clave es estacion + hora.
aire = pd.merge(no2, pm, on=["estacion", "hora"], how="inner")

print("\nFilas NO2:", len(no2), " filas PM2.5:", len(pm), " filas unidas:", len(aire))
print("Filas por estacion despues de unir:")
print(aire["estacion"].value_counts())

# PREGUNTA 1: ¿Que estaciones quedaron fuera de la union y por que?
# Respuesta: queda afuera Museo Romántico, porque ahi no se mide NO2 (tiene 0 datos),
# entonces no tiene ninguna fila para aparear. Quedan 946 filas, que son todas las de NO2
# (cada hora con NO2 tambien tenia PM2.5). Lo que se pierde son 744 filas de PM2.5:
# las 576 de Museo Romántico y horas de Curva de Maroñas (65) y Tres Cruces (103)
# en las que habia PM2.5 pero no NO2. Esas filas no desaparecen: siguen en la tabla pm.

# %%
# 3. PREGUNTA 2: lo mismo con left join
# Primero con NO2 a la izquierda (como en la clase, que el ozono iba a la izquierda)
aire_left = pd.merge(no2, pm, on=["estacion", "hora"], how="left")
print("\nLeft join con NO2 a la izquierda:", len(aire_left), "filas,",
      aire_left["pm25"].isna().sum(), "con pm25 vacio")

# Despues al reves, con PM2.5 a la izquierda
aire_left2 = pd.merge(pm, no2, on=["estacion", "hora"], how="left")
print("Left join con PM2.5 a la izquierda:", len(aire_left2), "filas,",
      aire_left2["no2"].isna().sum(), "con no2 vacio")

# Respuesta: el left join se queda con TODAS las filas de la tabla de la izquierda.
# - Con NO2 a la izquierda quedan 946 filas, igual que el inner join, y ninguna con pm25
#   vacio, porque todas las horas con NO2 tenian PM2.5.
# - Con PM2.5 a la izquierda quedan 1690 filas y 744 tienen no2 vacio (NaN): son las que
#   no encontraron pareja, entre ellas todas las de Museo Romántico.
# O sea que importa cual tabla va a la izquierda.

# %%
# 4. Un color por estacion: las dos series en el tiempo
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
for est, d in no2.groupby("estacion"):
    ax1.plot(d["hora"], d["no2"], linewidth=0.5, label=est)
for est, d in pm.groupby("estacion"):
    ax2.plot(d["hora"], d["pm25"], linewidth=0.5, label=est)
ax1.set_title("NO2 y PM2.5 por hora, junio de 2024", loc="left")
ax1.set_ylabel("NO2 (µg/m³)")
ax2.set_ylabel("PM2.5 (µg/m³)")
ax1.legend(title="Estación")
ax2.legend(title="Estación")
fig.tight_layout()
fig.savefig("graficos/clase09_series_no2_pm25.png")
plt.close(fig)

# %%
# 5. Perfil horario: a que hora del dia hay mas de cada uno
datos["hora_del_dia"] = datos["hora"].dt.hour
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
for est, d in datos.groupby("estacion"):
    perfil = d.groupby("hora_del_dia")[["no2", "pm25"]].mean()
    if perfil["no2"].notna().any():
        ax1.plot(perfil.index, perfil["no2"], marker="o", markersize=3, label=est)
    ax2.plot(perfil.index, perfil["pm25"], marker="o", markersize=3, label=est)
ax1.set_title("NO2 (µg/m³)")
ax2.set_title("PM2.5 (µg/m³)")
for ax in (ax1, ax2):
    ax.set_xlabel("Hora del día")
    ax.set_xticks(range(0, 24, 3))
    ax.legend()
fig.suptitle("Promedio por hora del día, junio de 2024")
fig.tight_layout()
fig.savefig("graficos/clase09_perfil_horario.png")
plt.close(fig)

# %%
# 6. Boxplot: PM2.5 diario por estacion (la distribucion, no solo la media)
pm["dia"] = pm["hora"].dt.date
pm_dia = pm.groupby(["estacion", "dia"])["pm25"].mean().reset_index()
estaciones = pm_dia["estacion"].unique()
fig, ax = plt.subplots(figsize=(7, 5))
ax.boxplot([pm_dia.loc[pm_dia["estacion"] == e, "pm25"] for e in estaciones])
ax.set_xticks(range(1, len(estaciones) + 1))
ax.set_xticklabels(estaciones)
ax.set_title("PM2.5: distribución de la media diaria por estación, junio 2024", loc="left")
ax.set_ylabel("PM2.5 (µg/m³)")
fig.savefig("graficos/clase09_boxplot_pm25.png")
plt.close(fig)

# %%
# 7. Dispersion: ¿las horas con mas NO2 son las de mas PM2.5? (solo con la tabla unida)
r_global = aire["no2"].corr(aire["pm25"])
print("\nCorrelacion NO2 vs PM2.5 (todas las horas):", round(r_global, 2))

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(aire["pm25"], aire["no2"], s=5, alpha=0.4)
ax.set_xscale("log")
ax.set_title(f"NO2 vs PM2.5, medias horarias (r = {r_global:.2f})", loc="left")
ax.set_xlabel("PM2.5 (µg/m³, escala log)")
ax.set_ylabel("NO2 (µg/m³)")
fig.savefig("graficos/clase09_dispersion.png")
plt.close(fig)

# %%
# 8. Franjas horarias y paneles
def paneles_por_franja(cortes, nombres, archivo):
    tabla = aire.copy()
    tabla["franja"] = pd.cut(tabla["hora"].dt.hour, bins=cortes, labels=nombres)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
    for ax, franja in zip(axes.flatten(), nombres):
        d = tabla[tabla["franja"] == franja]
        r = d["no2"].corr(d["pm25"])
        ax.scatter(d["pm25"], d["no2"], s=5, alpha=0.4)
        ax.set_xscale("log")
        ax.set_title(f"{franja}   r = {r:.2f}   n = {len(d)}", fontsize=10)
        print(f"  {franja}: r = {r:.2f}, n = {len(d)}")
    fig.supxlabel("PM2.5 (µg/m³, escala log)")
    fig.supylabel("NO2 (µg/m³)")
    fig.tight_layout()
    fig.savefig(archivo)
    plt.close(fig)

print("\nCortes de la clase (-1, 5, 11, 17, 23):")
paneles_por_franja([-1, 5, 11, 17, 23],
                   ["madrugada (0-5)", "mañana (6-11)", "tarde (12-17)", "noche (18-23)"],
                   "graficos/clase09_paneles_franjas.png")

# PREGUNTA 3: cambiar los cortes a (-1, 6, 12, 19, 23)
print("\nCortes nuevos (-1, 6, 12, 19, 23):")
paneles_por_franja([-1, 6, 12, 19, 23],
                   ["madrugada (0-6)", "mañana (7-12)", "tarde (13-19)", "noche (20-23)"],
                   "graficos/clase09_paneles_franjas_cortes_nuevos.png")

# Respuesta: cambian los n de cada panel (la noche queda de 4 horas, n = 160, y la tarde
# de 7, n = 279) y cambian los r. Lo que mas cambia es la noche: pasa de r = 0.60 a
# r = 0.72. Las horas 18 y 19, que son de mucho transito, pasan de "noche" a "tarde".
# O sea que lo que se ve depende de donde se corta: los cortes son una decision,
# no algo que viene en los datos.

# %%
# 9. Guardar la tabla unida
aire.to_csv("data/aire_horario_no2_pm25.csv", index=False)

# %%
# PREGUNTA 4: con los datos del equipo, dos tablas que se puedan unir y su clave
# - El conteo de transito y las mediciones de aire: se unen por estacion + hora
#   (es justamente como esta armado transito_aire_junio2024.csv).
# - El RUPE (proveedores) con el diccionario del RUPE no se unen por filas: el
#   diccionario describe las columnas, no los proveedores.
# - Las pesadas de residuos se podrian unir con una tabla de circuitos de recoleccion
#   por la columna nomenclatura_circuito, o con una de municipios por municipio.
