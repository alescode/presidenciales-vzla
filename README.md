# Herramientas para analizar los datos de las elecciones presidenciales 2012 y 2013 en Venezuela

## Descripción del formato de los datos
Los datos se manejarán en formato CSV, con las siguientes columnas:

- `state_id`: identificador del *estado*
- `county_id`: identificador del *municipio*
- `township_id`: identificador de la *parroquia*
- `voting_center_id`: identificador del *centro* de votación
- `voting_table_id`: identificador de la *mesa* de votación
- `cne_new_code`: número que identifica los resultados de un *centro* de votación y aparece en la estructura del url en cne.gob.ve
- `table_number`: número de la mesa de votación en un centro particular; junto con el `cne_new_code` puede identificar inequívocamente a una mesa de votación en todo el país
- `candidato`: Maduro, Capriles, Sequera, Bolívar, Mora o Méndez
- `votos`: Número de votos obtenidos por el candidato

## Descripción de los archivos

`transform_format_2013.py` toma los datos generados por el scrapper que conseguimos
el 16 de abril (en carpeta otra-via) y los transforman al formato CSV descrito arriba.
