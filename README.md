# Introducción a la Ciencia de Datos

Repositorio del curso Introducción a la Ciencia de Datos — FCEE, Universidad de Montevideo.

Cada clase tiene su carpeta con el material de la clase, los ejercicios resueltos, los
gráficos y las respuestas.

## Organización

```
clase02/ ... clase13/   una carpeta por clase
data/                   datos que usan los ejercicios (csv)
guias/                  guías de instalación
```

## Cómo correr los ejercicios

1. Instalar los paquetes (una sola vez):

   ```bash
   pip install pandas numpy matplotlib statsmodels requests
   ```

   Si `pip` no se reconoce: `py -m pip install ...` en Windows o `python3 -m pip install ...`
   en Mac (ver `guias/python_pip_no_reconocido.pdf`).

2. Correr los scripts desde la carpeta principal del repositorio, por ejemplo:

   ```bash
   python clase02/ejercicio_datos_sinteticos.py
   ```
