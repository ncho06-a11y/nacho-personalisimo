# %%
# Clase 5 - Seudocodigo
# Ejercicio: pasar de seudocodigo a codigo en Python
# Correr desde la carpeta del proyecto: python clase05/ejercicio_seudocodigo.py

import pandas as pd
from pathlib import Path

# %%
# EJERCICIO 1: Filtrar temperaturas
#
# Seudocodigo de la clase:
#   INICIO Filtrar_Temperaturas
#       DEFINIR temperaturas = [18, 22, 15, 25, 30]
#       CREAR vector_filtrado VACIO
#       PARA CADA temp EN temperaturas
#           SI temp > 20 ENTONCES
#               AGREGAR temp A vector_filtrado
#           FIN SI
#       FIN PARA
#       IMPRIMIR vector_filtrado
#   FIN Filtrar_Temperaturas

# Version 1: igual que el seudocodigo, paso por paso con un for
temperaturas = [18, 22, 15, 25, 30]

vector_filtrado = []

for temp in temperaturas:
    if temp > 20:
        vector_filtrado.append(temp)

print("Temperaturas mayores a 20 (con for):", vector_filtrado)

# Version 2: lo mismo en una linea (comprension de listas, como en la clase)
vector_filtrado2 = [temp for temp in temperaturas if temp > 20]
print("Temperaturas mayores a 20 (en una linea):", vector_filtrado2)

# %%
# EJERCICIO 2: Ingesta con control de encoding
#
# Seudocodigo de la clase:
#   INICIO Ingesta_Datos
#       IMPRIMIR "Lectura de CSV..."
#       INTENTAR
#           Cargar CSV en 'df_raw' (UTF-8)
#       SI FALLA POR CODIFICACION ENTONCES
#           IMPRIMIR "[AVISO]: Error UTF-8, reintentando con latin-1..."
#           Cargar CSV en 'df_raw' (latin-1)
#       FIN INTENTAR
#   FIN Ingesta_Datos
#
# Lo pruebo con el diccionario del RUPE, que viene en latin-1 (tiene tildes rotas en UTF-8)

ruta_csv = Path("data") / "diccionario_datos_rupe.csv"

print("\nLectura de CSV...")

try:
    df_raw = pd.read_csv(ruta_csv, encoding="utf-8", sep=";")
except UnicodeDecodeError:
    print("[AVISO]: Error UTF-8, reintentando con latin-1...")
    df_raw = pd.read_csv(ruta_csv, encoding="latin-1", sep=";")

print(df_raw.head())

# %%
# EJERCICIO 3 (inventado por mi para practicar): seudocodigo propio
#
#   INICIO Contar_Calurosos
#       DEFINIR temperaturas = [18, 22, 15, 25, 30]
#       DEFINIR contador = 0
#       PARA CADA temp EN temperaturas
#           SI temp > 20 ENTONCES
#               SUMAR 1 A contador
#           FIN SI
#       FIN PARA
#       IMPRIMIR "Dias calurosos:", contador
#       IMPRIMIR "Promedio:", suma de temperaturas / cantidad
#   FIN Contar_Calurosos

contador = 0
for temp in temperaturas:
    if temp > 20:
        contador = contador + 1

print("\nDias calurosos:", contador)
print("Promedio:", sum(temperaturas) / len(temperaturas))
