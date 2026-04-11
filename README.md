# TAREA N°1
# Scraping Data - Resultados Admisión UNMSM 2026-II
# ¿Qué hace el proyecto?
Este proyecto extrae automáticamente los resultados del examen de admisión de la Universidad Nacional Mayor de San Marcos (UNMSM) 2026-II desde su página oficial. Utiliza Selenium para navegar por cada carrera y superar la paginación de DataTables completa, puesto que por defecto solo muestra 50 registros. Adicionalmente, consolida toda la información en un único archivo Excel.

## ¿Cómo instalar las dependencias?

Requiere Python 3.8+ y Google Chrome instalado. Pra ello, se corre "pip install selenium pandas openpyxl webdriver-manager" en el terminal. 

## ¿Cómo ejecutar el script?

Se puede ejecutar seleccionando y click en la parte superior (en el simbolo para correr) o correr en la terminal lo siguiente "python scraper.py". 

## Flujo de trabajo del script (paso a paso)
 
### Paso 1 — Abrir el navegador
La función `crear_driver()` abre una ventana de Chrome controlada por Python usando Selenium. `webdriver-manager` se encarga de descargar automáticamente el driver correcto según tu versión de Chrome, sin configuración manual.
 
### Paso 2 — Obtener la lista de carreras
La función `obtener_carreras()` navega a la página principal de resultados:
`https://admision.unmsm.edu.pe/Website20262/A/A.html`
 
Ahí busca todos los enlaces que apuntan a `results.html` dentro de la tabla. Cada enlace corresponde a una carrera (Administración, Medicina, Derecho, etc.). Extrae el nombre y la URL de cada una. En total se obtienen aproximadamente 111 carreras.
 
### Paso 3 — Entrar a cada carrera y mostrar TODOS los registros
Para cada carrera, la función `extraer_datos_carrera()`:
 
1. Navega a la URL de la carrera.
2. Espera a que la tabla HTML se cargue completamente.
3. Llama a `mostrar_todos_los_registros()`, que ejecuta JavaScript directamente en la página para cambiar la paginación de DataTables de 50 a **todos** los registros (`page.len(-1)`). Este es el paso clave, ya que sin esto solo se obtendrían los primeros 50 postulantes por carrera.
 
### Paso 4 — Extraer los datos de la tabla
Una vez que todos los registros son visibles, el script recorre cada fila (`<tr>`) de la tabla y extrae las 6 columnas de cada celda (`<td>`): Código, Apellidos y Nombres, Escuela, Puntaje, Mérito E.P. y Observación. Además agrega una columna extra "Carrera" para identificar a qué escuela pertenece cada postulante.
 
### Paso 5 — Acumular y guardar en Excel
Los datos de todas las carreras se acumulan en una sola lista. Al finalizar el recorrido, se convierten en un DataFrame de pandas y se exportan a `output/resultados_sanmarcos.xlsx` usando openpyxl como motor de escritura.
 
### Paso 6 — Cerrar el navegador
El bloque `finally` garantiza que Chrome se cierre siempre, incluso si ocurre un error durante la ejecución.
 
## Manejo de errores
 
El script usa bloques `try/except` en dos niveles:
- **Por carrera**: si una carrera falla, se imprime el error y se continúa con la siguiente sin detener el script.
- **General**: si ocurre un error crítico, se cierra Chrome correctamente gracias al `finally`.
 
## ¿Qué contiene la salida?
 
El archivo `output/resultados_sanmarcos.xlsx` contiene las siguientes columnas:
 
| Columna | Descripción |
|---------|-------------|
| Código | Código del postulante |
| Apellidos y Nombres | Nombre completo |
| Escuela | Escuela profesional |
| Puntaje | Puntaje obtenido |
| Mérito E.P | Mérito en la escuela profesional |
| Observación | Estado (ALCANZÓ VACANTE, AUSENTE, etc.) |
| Carrera | Nombre de la carrera (agregado por el script) |

## Tarea 2: API REST — Base de datos de videojuegos RAWG

### ¿Qué hace?
Consume la API de RAWG para extraer, analizar y comparar datos de videojuegos. Incluye exploración general, análisis por categorías, comparaciones entre plataformas/géneros/años, y exportación a CSV.

### Flujo de trabajo
1. **Configuración** — Se crea un cliente `RAWGClient` que encapsula las llamadas a la API y cuenta las solicitudes realizadas.
2. **Parte A** — Consulta el total de juegos registrados en RAWG.
3. **Parte B** — Obtiene los 5 mejores juegos por Metacritic y los 10 mejores en Steam.
4. **Parte C** — Compara plataformas (PC vs PS5), géneros (Action, RPG, Puzzle, Strategy), años (2015, 2020, 2023), y exporta los top 20 a CSV.
5. **Parte D** — Reflexiones y conclusiones personales sobre los datos obtenidos.

### Cómo ejecutar
1. Obtén tu API key en https://rawg.io/apidocs
2. Pégala en la variable `API_KEY` dentro del notebook
3. Ejecuta todas las celdas del notebook `api/tarea_rawg_api.ipynb`

### Salida
El archivo `api/output/top20_rawg.csv` contiene los 20 mejores juegos con: name, rating, metacritic, release_date, main_genre.

## Estructura del repositorio

```
Scraping_data/
├── scraper.py                        # Script principal (Tarea 1)
├── README.md                         # Este archivo
├── output/
│   └── resultados_sanmarcos.xlsx     # Excel con resultados UNMSM
├── api/
│   ├── tarea_rawg_api.ipynb          # Notebook (Tarea 2)
│   └── output/
│       └── top20_rawg.csv            # CSV top 20 juegos
└── video/
    └── link.txt                      # Enlace al video explicativo

