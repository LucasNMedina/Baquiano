import sqlite3
import os
import logging
from src.core.models import Producto

# --- CONFIGURACIÓN DE RUTAS ABSOLUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # src/core/
PROYECTO_RAIZ = os.path.dirname(os.path.dirname(BASE_DIR)) # baquiano/
DATA_DIR = os.path.join(PROYECTO_RAIZ, "data")             # baquiano/data/
DB_PATH = os.path.join(DATA_DIR, "baquiano.db")            # baquiano/data/baquiano.db
LOG_PATH = os.path.join(DATA_DIR, "baquiano.log")

# Crea la carpeta 'data' en la raíz si no existe, previniendo errores de SQLite
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# CONFIGURACIÓN DEL CEREBRO DEL LOGGER
# Le decimos dónde guardar, qué nivel mínimo registrar y el formato de la línea
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.ERROR, # Registra desde ERROR para arriba (ignora INFO y DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8' # Para que no tenga problemas con los acentos o la 'ñ'
)

def inicializar_db():
    """Crea la tabla de productos si no existe al arrancar el programa."""
    try:
        with sqlite3.connect(DB_PATH) as conexion: #Creo la conexion de la db
            cursor = conexion.cursor() #Creo el mandatario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    name TEXT,
                    price REAL
                )
            """)
    except sqlite3.Error as e:
        logging.critical(f"Error crítico al inicializar la base de datos: {e}")

def add_product_db(code, name, price):
        try:
            with sqlite3.connect(DB_PATH) as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO productos (code, name, price) VALUES(?, ?, ?)",
                    (code, name, price)
                )
                return True
        except sqlite3.IntegrityError: 
            return False # Devuelve False si el código ya existe
        except sqlite3.Error as e:
            logging.error(f"Error al insertar producto (Código: {code}): {e}")
            return False

def product_exist(code):
    """Retorna True si el producto existe en la base de datos."""
    return get_product_by_code(code) is not None

def get_product_by_code(code):
    """Busca un producto por su código y devuelve un objeto Producto (o None)."""
    try:
        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT code, name, price FROM productos WHERE code = ?", (code,))
            result = cursor.fetchone()

            if result:
                # Transformo la tupla de la DB en el objeto Producto
                return Producto(result[0], result[1], result[2])
    except sqlite3.Error as e:
        logging.error(f"Error al consultar producto (Código: {code}): {e}")
    return None

def delete_product_db(code):
    """Elimina un producto de la base de datos usando su código."""
    try:
        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE code = ?", (code,))
            return True
    except sqlite3.Error as e:
        logging.error(f"Error al borrar producto (Código: {code}): {e}")
        return False

def update_product_db(code, new_name, new_price):
    """Actualiza el nombre y el precio de un producto usando su código."""
    try:
        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute("UPDATE productos SET name = ?, price = ? WHERE code = ?", (new_name, new_price, code))
            return True
    except sqlite3.Error as e:
            logging.error(f"Error al actualizar producto (Código: {code}): {e}")
    return False