import unittest
import os
import sqlite3
from src.core.database import inicializar_db, insert_product_db, get_product_by_code, update_product_db, delete_product_db
from src.core.models import Producto

class TestDataBase(unittest.TestCase):
    # 1. SETUP: Esta función se ejecuta AUTOMÁTICAMENTE antes de cada prueba.
    # Es ideal para preparar un entorno limpio.
    def setUp(self):
        inicializar_db()
        # Aseguramos limpiar cualquier residuo borrando un código de prueba
        delete_product_db("999999")
    
    # 2. TEARDOWN: Se ejecuta AUTOMÁTICAMENTE al finalizar cada prueba.
    # Sirve para limpiar la mugre que hayamos dejado.
    def tearDown(self):
        delete_product_db("999999")

    # 3. PRUEBA 1: Testear si un producto se inserta y se lee correctamente
    def test_insertar_y_obtener_producto(self):
        # Creamos un producto ficticio de prueba
        nuevo_producto = Producto("999999", "Yerba de Test", 1250.50)
        
        # Ejecutamos la función de tu base de datos
        resultado_insercion = insert_product_db(nuevo_producto.code, nuevo_producto.name, nuevo_producto.price)
        
        # Verificamos que haya devuelto True (inserción exitosa)
        self.assertTrue(resultado_insercion)
        
        # Ahora intentamos buscarlo
        producto_recuperado = get_product_by_code("999999")
        
        # Afirmamos (Assert) que el producto NO debe ser None
        self.assertIsNotNone(producto_recuperado)
        # Afirmamos que el nombre recuperado debe ser idéntico al que guardamos
        self.assertEqual(producto_recuperado.name, "Yerba de Test")
        self.assertEqual(producto_recuperado.price, 1250.50)

    # 4. PRUEBA 2: Testear si la actualización de precios funciona
    def test_actualizar_precio_producto(self):
        # Insertamos primero el producto base
        prod = Producto("999999", "Azúcar de Test", 800.00)
        insert_product_db(prod.code, prod.name, prod.price)
        
        # Ejecutamos tu función de actualización a un precio nuevo
        resultado_update = update_product_db("999999", "Azúcar de Test", 950.00)
        self.assertTrue(resultado_update)
        
        # Volvemos a consultar para comprobar el cambio
        prod_modificado = get_product_by_code("999999")
        self.assertEqual(prod_modificado.price, 950.00)

    # 5. PRUEBA 3: Testear qué pasa si buscamos un código que NO existe
    def test_producto_inexistente_devuelve_none(self):
        producto_fantasma = get_product_by_code("0000000000000")
        # Tu función database.py debe retornar None si no lo encuentra
        self.assertIsNone(producto_fantasma)

    # 6. TEST 4: Verifica que el sistema RECHACE precios negativos o cero
    def test_precio_negativo_devuelve_false(self):
        # Intentamos insertar un precio inválido
        resultado = insert_product_db("999999", "Yerba Maldita", -50.00)
        
        # Nuestra hipótesis es que DEBE devolver False (no se debe guardar)
        self.assertFalse(resultado)
        
        # Comprobamos que efectivamente NO se haya guardado en la DB
        producto = get_product_by_code("999999")
        self.assertIsNone(producto)
# Este bloque permite ejecutar el script directamente desde la consola
if __name__ == "__main__":
    unittest.main()