import sqlite3
from src.core.models import Producto

DB_PATH = "data/baquiano.db"

def inicializar_db():
    """Crea la tabla de productos si no existe al arrancar el programa."""
    conexion = sqlite3.connect(DB_PATH) #Creo la conexion de la db
    cursor = conexion.cursor() #Creo el mandatario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            precio REAL
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
    cursor.execute("SELECT code, name, precio FROM productos WHERE code = ?", (code,))
    resultado = cursor.fetchone()
    conexion.close

    if resultado:
        # Transformo la tupla de la DB en el objeto Producto
        return Producto(resultado[0], resultado[1], resultado[2])
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

