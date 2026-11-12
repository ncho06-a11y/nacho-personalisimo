# %%
# Clase 11 - Leer la foto de un ticket con IA (API de Gemini) y pasarla a una tabla
#
# Antes de correrlo:
#   1. Sacar una clave gratis en https://aistudio.google.com ("Get API key")
#   2. Guardarla en data/clase11/clave_gemini.txt
#      (ese archivo NO se sube a GitHub: esta en el .gitignore)
#   3. La foto del ticket esta en data/clase11/ticket.jpg
#   4. pip install requests pandas
#
# Correr desde la carpeta del proyecto: python scripts/clase11_leer_ticket.py

import base64
import requests
import pandas as pd

RUTA = "data/clase11/"
CLAVE = open(RUTA + "clave_gemini.txt").read().strip()
FOTO = "ticket.jpg"
TIPO = "image/jpeg"
MODELO = "gemini-3.5-flash-lite"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"

INSTRUCCION = """Transcribí los ítems de este ticket de compra.
Respondé solo con una tabla CSV, sin ningún otro texto, con dos columnas:
descripcion,monto
- monto con punto decimal y sin separador de miles (1.250,00 se escribe 1250.00)
- no incluyas SUBTOTAL, IVA, TOTAL, EFECTIVO, CAMBIO ni TARJETA
- si algo no se puede leer, dejalo vacío; no lo inventes"""

# %%
# 1. La foto a base64 (texto), porque el JSON solo acepta texto
with open(RUTA + FOTO, "rb") as archivo:
    bytes_foto = archivo.read()
imagen_base64 = base64.b64encode(bytes_foto).decode("ascii")
print("La foto pesa", len(bytes_foto), "bytes; en base64 son", len(imagen_base64), "caracteres")

# %%
# 2. Armar el pedido y mandarlo (POST, con la clave en el encabezado)
cuerpo = {
    "contents": [{
        "parts": [
            {"text": INSTRUCCION},
            {"inline_data": {"mime_type": TIPO, "data": imagen_base64}},
        ]
    }],
    "generationConfig": {"temperature": 0},
}

respuesta = requests.post(URL, headers={"x-goog-api-key": CLAVE}, json=cuerpo, timeout=120)
print("Codigo de estado:", respuesta.status_code)   # 200 = bien
if respuesta.status_code != 200:
    print(respuesta.text)
    raise SystemExit("Fallo el pedido, mirar el codigo de estado")

# %%
# 3. Leer la respuesta y guardarla como CSV
datos = respuesta.json()
texto = datos["candidates"][0]["content"]["parts"][0]["text"]
texto = texto.replace("```csv", "").replace("```", "").strip()
print(texto)
print("Tokens de entrada:", datos["usageMetadata"]["promptTokenCount"],
      " tokens de salida:", datos["usageMetadata"]["candidatesTokenCount"])

with open(RUTA + "ticket_gemini.csv", "w", encoding="utf-8") as archivo:
    archivo.write(texto + "\n")

# %%
# 4. Controlar lo que devolvio la IA
# No alcanza con que "parezca bien": comparo con lo que dice el ticket.
tabla = pd.read_csv(RUTA + "ticket_gemini.csv")
control = pd.read_csv(RUTA + "ticket_control.csv")   # lo que dice el ticket, linea por linea
TOTAL_IMPRESO = 50.00                                 # el TOTAL que esta impreso en el ticket

print(tabla)
suma = tabla["monto"].sum()
print("Suma de los items:", suma, " TOTAL impreso:", TOTAL_IMPRESO)

if abs(suma - TOTAL_IMPRESO) < 0.01:
    print("La suma coincide con el total del ticket")
else:
    print("OJO: la suma NO coincide con el total, revisar a mano")

print("Misma cantidad de items que el ticket:", len(tabla) == len(control))
print("Mismos montos que el ticket:", sorted(tabla["monto"].tolist()) == sorted(control["monto"].tolist()))
# Cosas a mirar: que no meta el "Desc. Ley 19210" (-1.64) ni el "Pago total" (48.36)
# como si fueran items, y que no invente nada que no se lee.
