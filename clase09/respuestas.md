# Clase 9 — Respuestas para la bitácora

En clase se usaron los datos de ozono y PM2.5 de enero a abril de 2024, que no tengo en el
repo. Lo hice con `data/transito_aire_junio2024.csv`, que tiene el mismo problema: el NO2 se
mide solo en algunas estaciones y el PM2.5 en todas. Separé NO2 y PM2.5 como dos fuentes y
las uní por estación + hora (`ejercicio_union_y_graficos_por_grupo.py`).

**1. ¿Qué estaciones quedaron fuera de la unión y por qué?**

Museo Romántico, porque ahí no se mide NO2 y no tiene ninguna fila para aparear. Quedan 946
filas, que son todas las de NO2; se pierden 744 filas de PM2.5 (las 576 de Museo Romántico y
horas de Curva de Maroñas y Tres Cruces con PM2.5 pero sin NO2). No desaparecen: siguen en su
tabla.

**2. Con `left join` en lugar de `inner join`, ¿cuántas filas quedan? ¿Qué hay en la columna
de las que no aparearon?**

El left join se queda con todas las filas de la tabla de la izquierda:
- Con NO2 a la izquierda quedan 946 filas y ninguna con PM2.5 vacío, porque todas las horas
  con NO2 tenían PM2.5.
- Con PM2.5 a la izquierda quedan 1690 filas y 744 tienen el NO2 vacío (NaN): son las que no
  encontraron pareja.

Importa cuál tabla va a la izquierda.

**3. Cambiar los cortes a (-1, 6, 12, 19, 23) y rehacer los paneles: ¿qué cambia?**

| Franja | Cortes de la clase | Cortes nuevos |
|---|---|---|
| Madrugada | r = 0,59 (n = 234) | r = 0,53 (n = 273) |
| Mañana | r = 0,62 (n = 234) | r = 0,62 (n = 234) |
| Tarde | r = 0,53 (n = 238) | r = 0,53 (n = 279) |
| Noche | r = 0,60 (n = 240) | r = 0,72 (n = 160) |

La noche pasa a tener 4 horas y su correlación sube de 0,60 a 0,72, porque las 18 y 19 (mucho
tránsito) pasan a la tarde. Lo que se ve depende de dónde se corta: los cortes son una
decisión, no algo que viene en los datos.

Gráficos: `paneles_franjas.png` y `paneles_franjas_cortes_nuevos.png`.

**4. Dos tablas que se puedan unir y su clave**

- El conteo de tránsito y las mediciones de aire: clave estación + hora.
- Las pesadas de residuos con una tabla de circuitos de recolección: clave
  `nomenclatura_circuito` (o con una tabla de municipios, por `municipio`).
