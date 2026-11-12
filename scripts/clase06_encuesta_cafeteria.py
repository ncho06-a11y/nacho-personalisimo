# %%
# Clase 6 - Diseño de encuestas
# Armo la tabla que sale de mi cuestionario de la cafeteria (con respuestas inventadas)
# y declaro los tipos como dice el libro de codigos.
# Correr desde la carpeta del proyecto: python scripts/clase06_encuesta_cafeteria.py

import pandas as pd
import numpy as np

# %%
# 1. Respuestas inventadas de 5 personas
# La persona 3 marco "Nunca" en P1, entonces salto a P5: sus prod_, atencion y pago_ quedan NA
encuesta = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "frecuencia": ["1 a 3 veces", "Más de 8 veces", "Nunca", "4 a 8 veces", "1 a 3 veces"],
    "prod_cafe": [1, 1, np.nan, 0, 1],
    "prod_comida": [0, 1, np.nan, 1, 0],
    "prod_frias": [0, 0, np.nan, 1, 1],
    "prod_otros": [0, 0, np.nan, 0, 0],
    "atencion": [4, 5, np.nan, 3, 2],
    "pago_efectivo": [1, 0, np.nan, 1, 0],
    "pago_tarjeta": [0, 1, np.nan, 1, 0],
    "pago_transferencia": [0, 1, np.nan, 0, 1],
    "estudiante": ["Sí", "Sí", "No", "Sí", "Sí"],
    "edad": [20, 23, 45, np.nan, 19],   # la 4 no contesto la edad (no respuesta)
    "mejora": ["mas variedad", "precios", None, "mas rapido", None],
})

print("Columnas:", len(encuesta.columns))   # tienen que ser 13
print(encuesta)

# %%
# 2. Declarar los tipos (sale del libro de codigos)
encuesta["frecuencia"] = pd.Categorical(
    encuesta["frecuencia"],
    categories=["Nunca", "1 a 3 veces", "4 a 8 veces", "Más de 8 veces"],
    ordered=True,
)
encuesta["atencion"] = pd.Categorical(encuesta["atencion"], categories=[1, 2, 3, 4, 5], ordered=True)
encuesta["estudiante"] = encuesta["estudiante"] == "Sí"

print("\nTipos:")
print(encuesta.dtypes)

# %%
# 3. Faltantes: hay de dos tipos distintos
print("\nFaltantes por columna:")
print(encuesta.isna().sum())

# Los de prod_, atencion y pago_ son todos de la persona 3 (filtro, NA por diseño).
# El de edad es de la persona 4 (no respuesta).
# La tabla los muestra igual (NaN), por eso hay que anotarlo en el libro de codigos.
nunca = encuesta["frecuencia"] == "Nunca"
print("\nNA de atencion en los que dijeron Nunca:", encuesta.loc[nunca, "atencion"].isna().sum())
print("NA de atencion en el resto:", encuesta.loc[~nunca, "atencion"].isna().sum())

# %%
# 4. Algo simple con los datos: que se compra mas y como se paga
print("\nCuantos compraron cada producto:")
print(encuesta[["prod_cafe", "prod_comida", "prod_frias", "prod_otros"]].sum())

print("\nCuantos usaron cada medio de pago:")
print(encuesta[["pago_efectivo", "pago_tarjeta", "pago_transferencia"]].sum())
