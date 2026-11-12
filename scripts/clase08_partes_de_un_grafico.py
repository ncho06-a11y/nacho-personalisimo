# %%
# Clase 8 - Visualizacion basica: las partes de un grafico
# Ejercicio: ver que esta mal en el grafico del ozono de la clase 7 y corregirlo.
# Despues hago un grafico nuevo con otro dataset aplicando lo mismo.
# Correr desde la carpeta del proyecto: python scripts/clase08_partes_de_un_grafico.py

import matplotlib.pyplot as plt
import pandas as pd

# media mensual de ozono (ene-abr 2024), los valores de la clase
ozono_mes = pd.DataFrame({
    "mes": [1, 2, 3, 4],
    "o3_medio_mes": [29.1, 35.5, 24.0, 25.7],
})

# %%
# 1. El grafico del que partimos (asi estaba en la clase 7)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ozono_mes["mes"], ozono_mes["o3_medio_mes"], color="blue", linewidth=2)
ax.scatter(ozono_mes["mes"], ozono_mes["o3_medio_mes"], color="red", s=60, zorder=3)
ax.set_title("Concentración de Ozono en el ambiente, por mes, 2024")
ax.set_xlabel("Fecha")
ax.set_ylabel("Valores")
fig.savefig("graficos/clase08_ozono_original.png")
plt.close(fig)

# %%
# 2. Que esta mal (lo que encontre):
#  - Eje x: pone 1.0, 1.5, 2.0, 2.5... y no hay "mes 1.5". Tendrian que ser los meses (Ene, Feb...).
#  - "Fecha" no dice nada: son meses de 2024.
#  - "Valores" no dice que se mide ni en que unidad (es ozono en µg/m³).
#  - El eje y empieza en 24, entonces la caida de feb a mar parece enorme
#    (casi de arriba a abajo del grafico) y en realidad es de 35 a 24.
#  - No dice de donde salen los datos.
#  - El titulo no aclara que es un promedio mensual.
#  - Linea azul y puntos rojos: dos colores para lo mismo, no aporta.

# %%
# 3. Mi version corregida
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ozono_mes["mes"], ozono_mes["o3_medio_mes"], color="steelblue", linewidth=2, marker="o")

# meses con nombre en vez de 1.0, 1.5, ...
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(["Ene", "Feb", "Mar", "Abr"])

# eje y desde 0 para no exagerar las diferencias
ax.set_ylim(0, 40)

# pongo el valor arriba de cada punto
for mes, valor in zip(ozono_mes["mes"], ozono_mes["o3_medio_mes"]):
    ax.text(mes, valor + 1, str(valor), ha="center")

ax.set_title("Ozono en Montevideo: promedio mensual, enero a abril de 2024", loc="left")
ax.set_xlabel("Mes (2024)")
ax.set_ylabel("Ozono (µg/m³)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#e5e5e5")
fig.text(0.99, 0.01, "Fuente: datos de ozono de la clase 7 (Montevideo).",
         ha="right", fontsize=8, color="gray")
fig.savefig("graficos/clase08_ozono_corregido.png")
plt.close(fig)

# %%
# 4. Lo mismo con otro dataset: residuos que entraron a la estacion de transferencia
residuos = pd.read_csv("data/cantidad_de_residuos_en_la_estacion_de_transferencia_2023.csv")

# sumo el peso neto por tipo de residuo y lo paso de kilos a toneladas
toneladas = residuos.groupby("tipo_residuo_desc")["peso_neto"].sum() / 1000
toneladas = toneladas.sort_values()
print("Toneladas por tipo de residuo:")
print(toneladas.round(1))

# barras horizontales porque los nombres son largos
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(toneladas.index, toneladas.values, color="steelblue")
for i, valor in enumerate(toneladas.values):
    ax.text(valor + 50, i, f"{valor:,.0f} t", va="center")

ax.set_title("Casi todo lo que llega es residuo domiciliario", loc="left")
ax.set_xlabel("Toneladas (peso neto)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.99, 0.01, "Fuente: pesadas en la estación de transferencia, noviembre-diciembre 2023.",
         ha="right", fontsize=8, color="gray")
fig.tight_layout()
fig.savefig("graficos/clase08_residuos_por_tipo.png")
plt.close(fig)

print("\nGraficos guardados en graficos/ (clase08_*.png)")
