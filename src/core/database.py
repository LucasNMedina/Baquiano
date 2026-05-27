import sqlite3
import os
from src.core.models import Producto
#DB_PATH = "data/baquiano.db"

# 1. Averigua la ruta absoluta de la carpeta donde está este archivo (src/core/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Sube un nivel para salir de 'src/core' y llegar a la raíz del proyecto
PROYECTO_RAIZ = os.path.dirname(os.path.dirname(BASE_DIR))

# 3. Construye la ruta final apuntando a la carpeta data/ en la raíz
DB_PATH = os.path.join(PROYECTO_RAIZ, "data", "baquiano.db")

"""
# --- CONFIGURACIÓN DE RUTAS ABSOLUTAS (A prueba de fallos de OneDrive) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "baquiano.db")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
# -------------------------------------------------------------------------
"""

def inicializar_db():
    """Crea la tabla de productos si no existe al arrancar el programa."""
    conexion = sqlite3.connect(DB_PATH) #Creo la conexion de la db
    cursor = conexion.cursor() #Creo el mandatario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT,
            price REAL
        )
    """)
    conexion.commit() # Si no ponés "commit", los datos se pierden al cerrar la conexión.
    conexion.close() # Pase lo que pase, cerramos la conexión

def add_product_db(code, name, price):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO productos (code, name, price) VALUES(?, ?, ?)",
            (code, name, price)
        )
        conexion.commit()
        return True
    except sqlite3.IntegrityError: 
        return False # Devuelve False si el código ya existe
    finally:
        conexion.close()

def product_exist(code):
    """Retorna True si el producto existe en la base de datos."""
    return get_product_by_code(code) is not None

def get_product_by_code(code):
    """Busca un producto por su código y devuelve un objeto Producto (o None)."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT code, name, price FROM productos WHERE code = ?", (code,))
    result = cursor.fetchone()
    conexion.close()

    if result:
        # Transformo la tupla de la DB en el objeto Producto
        return Producto(result[0], result[1], result[2])
    return None

def delete_product_db(code):
    """Elimina un producto de la base de datos usando su código."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE code = ?", (code,))
        conexion.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conexion.close()

def update_product_db(code, new_name, new_price):
    """Actualiza el nombre y el precio de un producto usando su código."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE productos SET name = ?, price = ? WHERE code = ?", (new_name, new_price, code))
        conexion.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar en la DB: {e}")
        return False
    finally:
        conexion.close()