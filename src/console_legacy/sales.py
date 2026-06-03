import src.core.database as db
import os
import sys
from pathlib import Path

# --- BLINDAJE DE RUTA --- 
# Encuentra la raíz 'baquiano/' para que Python localice 'src' sin importar cómo se ejecute
RAIZ_PROYECTO = str(Path(__file__).resolve().parent.parent.parent)
if RAIZ_PROYECTO not in sys.path:
    sys.path.append(RAIZ_PROYECTO)

while True:
    os.system("cls") #Limpio pantalla para cada venta
    total_cuenta = 0

    while True:
        codigo_producto = input("\nEscanea producto (u 'ok' para cobrar): ")

        if codigo_producto.lower() == "ok":
            print("Muchas gracias!")
            print(f"TOTAL FINAL: {total_cuenta}")
            input("\nPresiona Enter para el siguiente cliente...") # Pausa para que el cajero vea el total
            break
        elif codigo_producto.startswith("."):
            try:
                # Quitamos el '+' y convertimos el resto a número
                monto_manual = float(codigo_producto[1:]) 
                total_cuenta += monto_manual
                print(f"   Añadido fiambreria: ${monto_manual:.2f}")
                print(f"   SUBTOTAL: ${total_cuenta:.2f}")
            except ValueError:
                print("Error: Después del '+' debes colocar un número válido.")
        elif db.product_exist(codigo_producto):
            producto = db.get_product_by_code(codigo_producto)
            print(f"Producto: {producto.name} - Precio: ${producto.price}")
            total_cuenta += producto.price
            print(f"   SUBTOTAL: ${total_cuenta}")
        else:
            print("Producto no encontrado.")