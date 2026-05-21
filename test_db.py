import sqlite3

def guardar_producto_test(codigo, nombre, precio):
    # 1. Nos conectamos
    conexion = sqlite3.connect("data/baquiano.db")
    cursor = conexion.cursor()
    
    # 2. Preparamos la orden con los "?" para las variables
    orden_sql = "INSERT INTO productos (codigo, nombre, precio) VALUES (?, ?, ?)"
    
    try:
        # 3. Le pasamos la orden y una TUPLA con los datos reales en el mismo orden
        cursor.execute(orden_sql, (codigo, nombre, precio))
        
        # 4. ¡IMPORTANTÍSIMO! Guardamos los cambios. 
        # Si no ponés "commit", los datos se pierden al cerrar la conexión.
        conexion.commit()
        print(f"¡Producto '{nombre}' guardado con éxito!")
        
    except sqlite3.IntegrityError:
        # ¿Te acordás que le pusimos UNIQUE al código? 
        # Si intentás meter el mismo código de nuevo, va a saltar acá de una.
        print(error_msg := f"Error: El código '{codigo}' ya existe en la base de datos.")
        
    finally:
        # 5. Pase lo que pase, cerramos la conexión
        conexion.close()

def buscar_producto_test(codigo):
    # 1. Nos conectamos al mismo archivo
    conexion = sqlite3.connect("data/baquiano.db")
    cursor = conexion.cursor()
    
    orden_sql = "SELECT codigo, nombre, precio FROM productos WHERE codigo = ?"
    
    # 2. Le pedimos al cursor que busque
    cursor.execute(orden_sql, (codigo,)) # Acordate de la coma al final si es un solo dato en la tupla
    
    # 3. Le decimos al mandadero que nos entregue la fila encontrada
    resultado = cursor.fetchone()
    
    # 4. Cerramos la conexión
    conexion.close()
    
    # 5. Analizamos qué nos trajo
    if resultado:
        # Si encontró algo, 'resultado' es una tupla: (codigo, nombre, precio)
        print("\n--- ¡Producto Encontrado! ---")
        print(f"Código: {resultado[0]}")
        print(f"Nombre: {resultado[1]}")
        print(f"Precio: ${resultado[2]:.2f}")
        return resultado
    else:
        print(f"\nEl producto con código '{codigo}' no existe.")
        return None

# --- PROBAMOS LA FUNCIÓN ---
if __name__ == "__main__":
    # 1. Probamos buscar la manteca que agregamos en el paso anterior:
    buscar_producto_test("779000011111")
    
    # 2. Probamos buscar un código inventado que no existe:
    buscar_producto_test("999999999999")