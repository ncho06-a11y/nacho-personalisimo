# %%
# Clase 10 - ¿Se ve el transito en la calidad del aire?
# Tres Cruces, junio de 2024: transito, NO2 y PM2.5
#
# Hago los pasos de la clase pero mas simple, con la tabla que ya viene armada por hora
# (data/transito_aire_junio2024.csv), asi no hace falta cargar los archivos por minuto
# ni calcular distancias. Al final de cada paso anoto que vi.
#
# Correr desde la carpeta del proyecto: python scripts/clase10_transito_y_aire.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datos = pd.read_csv("data/transito_aire_junio2024.csv", parse_dates=["hora"])

# me quedo con Tres Cruces, que es la que tiene mas transito medido cerca
df = datos[datos["estacion"] == "Tres Cruces"].copy()
df = df.set_index("hora").sort_index()
df = df[["transito", "no2", "pm25"]]

print("Horas con dato en Tres Cruces:")
print(df.notna().sum())

# %%
# PASO 3. Una semana de las tres series
semana = df["2024-06-04":"2024-06-10"]
fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
axes[0].plot(semana.index, semana["transito"])
axes[0].set_ylabel("Vehículos/hora")
axes[1].plot(semana.index, semana["no2"], color="brown")
axes[1].set_ylabel("NO2 (µg/m³)")
axes[2].plot(semana.index, semana["pm25"], color="orange")
axes[2].set_ylabel("PM2.5 (µg/m³)")
axes[0].set_title("Una semana en Tres Cruces, junio 2024", loc="left")
fig.tight_layout()
fig.savefig("graficos/clase10_semana.png")
plt.close(fig)
# Lo que vi: el transito sube de dia y baja de noche. El NO2 parece seguirlo.
# El PM2.5 tiene subidas que no coinciden con el transito.

# %%
# PASO 4. El dia tipico (perfil por hora), cada serie dividida por su promedio
df["hora_del_dia"] = df.index.hour
df["finde"] = df.index.dayofweek >= 5

perfil = df[~df["finde"]].groupby("hora_del_dia")[["transito", "no2", "pm25"]].mean()
perfil = perfil / perfil.mean()

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(perfil.index, perfil["transito"], marker="o", label="Tránsito")
ax.plot(perfil.index, perfil["no2"], marker="o", label="NO2")
ax.plot(perfil.index, perfil["pm25"], marker="o", label="PM2.5")
ax.axhline(1, color="grey", linewidth=0.8)
ax.set_title("Día típico de lunes a viernes (1 = su promedio)", loc="left")
ax.set_xlabel("Hora del día")
ax.set_ylabel("Relativo a su promedio")
ax.legend()
fig.savefig("graficos/clase10_perfil_horario.png")
plt.close(fig)
# Lo que vi: el NO2 tiene picos en las mismas horas que el transito (mañana y tarde).
# El PM2.5 tiene su pico de noche, cuando el transito ya bajo.

# %%
# PASO 5. Correlacion "cruda" (hora a hora)
r_no2 = df["transito"].corr(df["no2"])
r_pm = df["transito"].corr(df["pm25"])
print(f"\nCorrelacion cruda:  NO2 r = {r_no2:.2f}   PM2.5 r = {r_pm:.2f}")
# Lo que vi: el NO2 sube con el transito, el PM2.5 casi nada.
# Pero parte de esto es solo porque los dos tienen un ritmo diario.

# %%
# PASO 6. Desvios: a cada hora le resto lo habitual de esa hora (y tipo de dia)
desvios = pd.DataFrame(index=df.index)
for col in ["transito", "no2", "pm25"]:
    habitual = df.groupby(["finde", "hora_del_dia"])[col].transform("mean")
    desvios[col] = df[col] - habitual

r_no2_d = desvios["transito"].corr(desvios["no2"])
r_pm_d = desvios["transito"].corr(desvios["pm25"])
print(f"Correlacion de desvios:  NO2 r = {r_no2_d:.2f}   PM2.5 r = {r_pm_d:.2f}")
# Lo que vi: la r del NO2 baja bastante (mucho era el ritmo del dia), pero no es cero.

# %%
# PASO 7 y 9. ¿Con que demora? Correlacion con el transito de k horas antes
rezagos = range(0, 25)
r_k_no2 = []
r_k_pm = []
for k in rezagos:
    transito_antes = desvios["transito"].shift(k)   # el transito de k horas antes
    r_k_no2.append(desvios["no2"].corr(transito_antes))
    r_k_pm.append(desvios["pm25"].corr(transito_antes))

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(list(rezagos), r_k_no2, marker="o", label="NO2", color="brown")
ax.plot(list(rezagos), r_k_pm, marker="o", label="PM2.5", color="orange")
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("Contaminante ahora vs tránsito de k horas antes (desvíos)", loc="left")
ax.set_xlabel("k (horas antes)")
ax.set_ylabel("Correlación")
ax.legend()
fig.savefig("graficos/clase10_rezagos.png")
plt.close(fig)

k_no2 = int(np.nanargmax(r_k_no2))
k_pm = int(np.nanargmax(r_k_pm))
print(f"\nMejor rezago NO2: {k_no2} h (r = {r_k_no2[k_no2]:.2f})")
print(f"Mejor rezago PM2.5: {k_pm} h (r = {r_k_pm[k_pm]:.2f})")
# Lo que vi: el NO2 responde enseguida (1-2 horas) y despues se apaga.
# El PM2.5 tarda mucho mas: su maximo esta como medio dia despues.

# %%
# PASO 8. ¿Puede ser casualidad? Corro el transito dias enteros y comparo
def mejor_r(contaminante, transito):
    return max(contaminante.corr(transito.shift(k)) for k in range(0, 4))

real = mejor_r(desvios["no2"], desvios["transito"])
dias = len(desvios) // 24
al_azar = []
for d in range(3, dias - 2):
    corrido = pd.Series(np.roll(desvios["transito"].to_numpy(), 24 * d), index=desvios.index)
    al_azar.append(mejor_r(desvios["no2"], corrido))

mayores = sum(1 for r in al_azar if r >= real)
print(f"\nNO2: r real = {real:.2f}. Corridas al azar con r igual o mayor: {mayores} de {len(al_azar)}")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(al_azar, bins=10, color="lightgrey", edgecolor="grey", label="Tránsito corrido al azar")
ax.axvline(real, color="red", linewidth=2, label=f"Real: r = {real:.2f}")
ax.set_title("NO2: ¿la relación supera a la casualidad?", loc="left")
ax.set_xlabel("Mejor correlación (rezagos 0 a 3 h)")
ax.legend()
fig.savefig("graficos/clase10_azar.png")
plt.close(fig)
# Lo que vi: si la linea roja queda a la derecha de todas las barras, la relacion
# del NO2 con el transito no se explica por casualidad.

# %%
# PASO 10. Un modelo simple: lo habitual de la hora + lo que agrega el transito
def r2(medido, predicho):
    return 1 - ((medido - predicho) ** 2).sum() / ((medido - medido.mean()) ** 2).sum()

for col, k in [("no2", 1), ("pm25", 13)]:
    tabla = pd.DataFrame({
        "medido": df[col],
        "desvio": desvios[col],
        "transito_antes": desvios["transito"].shift(k),
    }).dropna()
    tabla["habitual"] = tabla["medido"] - tabla["desvio"]
    b, a = np.polyfit(tabla["transito_antes"], tabla["desvio"], 1)   # la recta
    tabla["modelo"] = tabla["habitual"] + a + b * tabla["transito_antes"]

    print(f"\n{col.upper()} (tránsito de {k} h antes):")
    print(f"  sube {1000 * b:.1f} µg/m³ por cada 1000 vehículos/hora de más")
    print(f"  R² solo lo habitual:      {r2(tabla['medido'], tabla['habitual']):.2f}")
    print(f"  R² habitual + tránsito:   {r2(tabla['medido'], tabla['modelo']):.2f}")
    print(f"  horas usadas: {len(tabla)}")

# Conclusion: el transito se ve en los dos contaminantes pero con ritmos distintos:
# el NO2 enseguida (sale del escape y se va rapido) y el PM2.5 como medio dia despues
# (se va juntando). Sumar el transito al modelo mejora lo que explica "lo habitual".
# Lo que el modelo no sabe (viento, lluvia, temperatura, otras fuentes) queda en el error.
