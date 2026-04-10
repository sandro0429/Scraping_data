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