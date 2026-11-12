# %%
from pathlib import Path
import pandas as pd

# 1. Ruta raíz del proyecto (carpeta donde corrés el script/notebook)
BASE_DIR = Path.cwd()

# 2. Nombre del archivo a cargar (ajustá el mes si descargaste otro)
archivo = "rupe-julio-2026.csv"
ruta_csv = BASE_DIR / "data" / archivo

# 3. Verificar que el archivo existe antes de intentar cargarlo
if not ruta_csv.exists():
    disponibles = list((BASE_DIR / "data").glob("*")) if (BASE_DIR / "data").exists() else []
    raise FileNotFoundError(
        f"No se encontró el archivo en: {ruta_csv}\n"
        f"Archivos disponibles en data/: {disponibles}"
    )

# 4. Cargar el CSV probando encoding y separador automáticamente
#    (los datasets de catalogo.gub.uy suelen venir en latin-1 y separados por ';')
try:
    df = pd.read_csv(ruta_csv, encoding="utf-8", sep=None, engine="python")
except UnicodeDecodeError:
    df = pd.read_csv(ruta_csv, encoding="latin-1", sep=None, engine="python")

# 5. Inspección inicial de los datos
print(f"--- Archivo cargado exitosamente desde: {ruta_csv.name} ---")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
print(f"Columnas: {list(df.columns)}")
print(df.head())

# 6. Inspección adicional específica de este dataset (proveedores del Estado)
print("\n--- Cantidad de proveedores por estado ---")
print(df["estado_prov"].value_counts())

print("\n--- Top 10 departamentos con más proveedores ---")
print(df["departamento_prov"].value_counts().head(10))

print("\n--- Valores nulos por columna ---")
print(df.isnull().sum())