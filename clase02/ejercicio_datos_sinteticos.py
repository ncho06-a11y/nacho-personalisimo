# %%
# Clase 2 - Generacion de datos (caja negra / DGP)
# Ejercicio: armar el dataframe de la caja negra y hacer datos sinteticos
# Correr desde la carpeta del proyecto: python clase02/ejercicio_datos_sinteticos.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# 1. El diccionario con lo que anotamos en la dinamica
datos_caja = {
    "objeto_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "textura": ["suave", "rugoso", "poroso", "suave", "rugoso", "suave", "poroso", "rugoso", "suave", "poroso"],
    "rigidez": ["blando", "rígido", "medio", "blando", "rígido", "rígido", "blando", "medio", "medio", "blando"],
    "num_aristas": [0, 8, 0, 4, 12, 0, 0, 6, 4, 0],
    "peso_estimado_g": [45.0, 120.5, 15.0, 85.0, 210.0, 35.0, 18.5, 95.0, 70.0, 22.0],
    "certeza_observador": [5, 4, 3, 5, 4, 2, 4, 3, 4, 3],
}

# %%
# 2. Lo paso a dataframe
df = pd.DataFrame(datos_caja)

# textura es nominal (no tiene orden)
df["textura"] = df["textura"].astype("category")
# rigidez es ordinal (blando < medio < rigido)
df["rigidez"] = pd.Categorical(df["rigidez"], categories=["blando", "medio", "rígido"], ordered=True)

print("Estructura:")
df.info()
print(df.head())

# %%
# 3. Bootstrap: saco 100 filas con reemplazo de las 10 que tengo
np.random.seed(42)
df_bootstrap = df.sample(n=100, replace=True).reset_index(drop=True)

print("\nBootstrap, cuantas veces salio cada objeto:")
print(df_bootstrap["objeto_id"].value_counts().sort_index())

# %%
# 4. Sintetico parametrico: invento 500 pesos con una normal
mu = df["peso_estimado_g"].mean()
sigma = df["peso_estimado_g"].std()
print("\nmedia:", round(mu, 1), " desvio:", round(sigma, 1))

pesos = np.random.normal(loc=mu, scale=sigma, size=500)
print("pesos negativos o cero antes de corregir:", (pesos <= 0).sum())

# un peso no puede ser negativo, asi que lo dejo en 1 como minimo
pesos = np.clip(pesos, a_min=1.0, a_max=None)

df_sintetico = pd.DataFrame({"peso_estimado_g": pesos, "tipo": "Sintético"})
print(df_sintetico.describe())

# %%
# 5. Sinteticos de variables no continuas (categoricas)
# Lo mas simple: contar que proporcion hay de cada categoria y sortear con esas proporciones
prop_textura = df["textura"].value_counts(normalize=True)
print("\nproporciones de textura:")
print(prop_textura)

textura_sint = np.random.choice(prop_textura.index, size=500, p=prop_textura.values)

prop_rigidez = df["rigidez"].value_counts(normalize=True)
rigidez_sint = np.random.choice(prop_rigidez.index, size=500, p=prop_rigidez.values)

# una binaria: tiene aristas o no (si/no)
prop_aristas = (df["num_aristas"] > 0).mean()
print("proporcion con aristas:", prop_aristas)
tiene_aristas_sint = np.random.rand(500) < prop_aristas

df_sintetico["textura"] = textura_sint
df_sintetico["rigidez"] = rigidez_sint
df_sintetico["tiene_aristas"] = tiene_aristas_sint

print("\ncomparo textura real vs sintetica:")
print(pd.DataFrame({
    "real": df["textura"].value_counts(normalize=True),
    "sintetico": pd.Series(textura_sint).value_counts(normalize=True),
}).round(2))

# %%
# 6. Grafico: pesos reales vs sinteticos
plt.hist(df_sintetico["peso_estimado_g"], bins=30, alpha=0.6, density=True, label="Sintético (500)")
plt.hist(df["peso_estimado_g"], bins=10, alpha=0.6, density=True, label="Real (10)")
plt.xlabel("peso estimado (g)")
plt.ylabel("densidad")
plt.title("Pesos reales vs sinteticos")
plt.legend()
plt.savefig("clase02/pesos_real_vs_sintetico.png")
print("\ngrafico guardado en clase02/pesos_real_vs_sintetico.png")

# %%
# 7. Conclusion (lo que vi)
# - El bootstrap no inventa nada nuevo, solo repite los 10 objetos que ya habia.
# - La normal si inventa pesos nuevos, pero como el desvio es grande salen pesos
#   negativos que no existen; por eso hay que cortarlos en 1.
# - Los datos reales parecen tener varios grupos (objetos livianos y pesados), y
#   la normal los mezcla en una sola campana: eso son los datos "fantasma" de la clase.
# - Las categorias sinteticas respetan las proporciones, pero se sortean por separado,
#   asi que se pierde la relacion entre variables (ej: rugoso con rigido).
