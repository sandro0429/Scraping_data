# TAREA N°1
import pandas as pd
import time
import os

# Herramientas de selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def crear_driver():
    """Crea y configura el driver de Chrome."""
    options = Options()
    # options.add_argument("--headless")  # Descomentar para ejecución sin ventana
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def obtener_carreras(driver):
    """Extrae la lista de carreras y sus URLs desde la página principal."""
    url_principal = "https://admision.unmsm.edu.pe/Website20262/A/A.html"
    driver.get(url_principal)
    time.sleep(3)
 
    enlaces = driver.find_elements(By.CSS_SELECTOR, "table a[href*='results.html']")
    carreras = []
    for enlace in enlaces:
        nombre = enlace.text.strip()
        href = enlace.get_attribute("href")
        if nombre and href:
            carreras.append({"nombre": nombre, "url": href})
    
    print(f"Se encontraron {len(carreras)} carreras.")
    return carreras

def mostrar_todos_los_registros(driver):
    """Cambia DataTables para mostrar TODOS los registros en vez de solo 50."""
    try:
        # Intentar cambiar el selector de longitud a -1 (Todos)
        driver.execute_script("""
            var table = $('table.dataTable').DataTable();
            table.page.len(-1).draw();
        """)
        time.sleep(2)
    except Exception:
        try:
            # Alternativa: seleccionar "Todos" del dropdown
            select = driver.find_element(By.CSS_SELECTOR, "select[name*='_length']")
            for option in select.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") == "-1" or option.text.lower() in ["todos", "all"]:
                    option.click()
                    time.sleep(2)
                    break
        except Exception:
            # Última alternativa: forzar con JS el select
            try:
                driver.execute_script("""
                    var sel = document.querySelector("select[name*='_length']");
                    if (sel) {
                        sel.value = '-1';
                        sel.dispatchEvent(new Event('change'));
                    }
                """)
                time.sleep(2)
            except Exception as e:
                print(f"  ⚠ No se pudo cambiar paginación: {e}")
 
 
def extraer_datos_carrera(driver, url_carrera, nombre_carrera):
    """Extrae todos los postulantes de una carrera específica."""
    try:
        driver.get(url_carrera)
        
        # Esperar a que la tabla se cargue
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        time.sleep(2)
 
        # Mostrar todos los registros (no solo los primeros 50)
        mostrar_todos_los_registros(driver)
 
        # Extraer filas de la tabla
        filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        datos = []
 
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            if len(celdas) >= 6:
                registro = {
                    "Código": celdas[0].text.strip(),
                    "Apellidos y Nombres": celdas[1].text.strip(),
                    "Escuela": celdas[2].text.strip(),
                    "Puntaje": celdas[3].text.strip(),
                    "Mérito E.P": celdas[4].text.strip(),
                    "Observación": celdas[5].text.strip(),
                    "Carrera": nombre_carrera
                }
                datos.append(registro)
 
        print(f"  ✔ {nombre_carrera}: {len(datos)} postulantes extraídos")
        return datos
 
    except Exception as e:
        print(f"  ✖ Error en {nombre_carrera}: {e}")
        return []
 
 
def main():
    """Función principal que ejecuta todo el proceso de scraping."""
    # Crear carpeta de salida
    os.makedirs("output", exist_ok=True)
 
    print("=" * 60)
    print("SCRAPER - Resultados Admisión UNMSM 2026-II")
    print("=" * 60)
 
    driver = crear_driver()
    todos_los_datos = []
 
    try:
        # Paso 1: Obtener lista de carreras
        carreras = obtener_carreras(driver)
 
        # Paso 2: Iterar por cada carrera
        for i, carrera in enumerate(carreras, 1):
            print(f"\n[{i}/{len(carreras)}] Procesando: {carrera['nombre']}")
            datos = extraer_datos_carrera(driver, carrera["url"], carrera["nombre"])
            todos_los_datos.extend(datos)
 
        # Paso 3: Guardar en Excel
        if todos_los_datos:
            df = pd.DataFrame(todos_los_datos)
            ruta_excel = "output/resultados_sanmarcos.xlsx"
            df.to_excel(ruta_excel, index=False, engine="openpyxl")
            print(f"\n{'=' * 60}")
            print(f"✔ Archivo guardado: {ruta_excel}")
            print(f"✔ Total de registros: {len(todos_los_datos)}")
            print(f"✔ Total de carreras procesadas: {len(carreras)}")
            print(f"{'=' * 60}")
        else:
            print("\n⚠ No se extrajeron datos.")
 
    except Exception as e:
        print(f"\n✖ Error general: {e}")
 
    finally:
        driver.quit()
        print("Driver cerrado.")
 
 
if __name__ == "__main__":
    main()