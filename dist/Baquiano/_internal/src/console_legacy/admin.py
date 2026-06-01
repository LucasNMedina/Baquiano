import src.core.database as db
from src.core.models import Producto
import sys
from pathlib import Path

# --- BLINDAJE DE RUTA --- 
# Encuentra la raíz 'baquiano/' para que Python localice 'src' sin importar cómo se ejecute
RAIZ_PROYECTO = str(Path(__file__).resolve().parent.parent.parent)
if RAIZ_PROYECTO not in sys.path:
    sys.path.append(RAIZ_PROYECTO) #python -m src.console_legacy.admin   

#Funciones
def menu(): #Muestra el menú
    print("---Sistema 'Baquiano'---")
    print("1.Agregar producto")
    print("2.Modificar producto")
    print("3.Eliminar producto")
    print("4.Mostrar producto")
    print("5.Salir")

def get_menu_number(): #Obtiene un número y lo devuelve
    while True:
        try:
            num = int(input("Elegí una opción: "))
            return num
        except ValueError:
            print("Debes colocar un número.")

def validate_menu(range_a, range_b): #Valida que la respuesta del menú sea correcta y la devuelve
    while True:
        answer = get_menu_number()
        if answer >= range_a and answer <= range_b:
            return answer
        else:
            print("Opción fuera de rango.")

def get_price(): #Obtiene un precio y lo devuelve
    while True:
        try:
            num = float(input("Colocá el precio del producto: "))
            return num
        except ValueError:
            print("El precio es incorrecto.")


def add_product():
    product_barcode = input("Escaneá el código de barras del nuevo producto: ")
    product_to_add = db.get_product_by_code(product_barcode)

    if product_to_add:
        print("El producto ya se encuentra en la base de datos.")
    else:
        product_name = input("Ingresa el nombre del producto: ").strip().capitalize()
        product_price = get_price()

        db.insert_product_db(product_barcode, product_name, product_price)
        print("Producto agregado correctamente.")

def remove_product(): #Elimina un producto de la lista
    barcode = input("Escaneá el producto que queres borrar: ")
    product_to_eliminate = db.get_product_by_code(barcode)

    if product_to_eliminate is None:
        print("El producto no se encuentra en la base de datos.")
    else:
        print(f"Producto: {product_to_eliminate.name} - Precio: ${product_to_eliminate.price}")
        confirmate = input("Desea eliminar S/N: ").strip().lower()
        if confirmate == "s":
            db.delete_product_db(product_to_eliminate.code)
            print("Producto eliminado correctamente.")
        else:
            print("Volviendo al menú")

def modification_menu(product):
    print()
    print(product)
    print()
    print("---Que desea modificar?---")
    print("1.Nombre del producto")
    print("2.Precio del producto")
    print("3.Volver al menú principal")

def modification_name(product):
    new_name = input("Ingrese el nuevo nombre del producto: ").strip().capitalize()
    db.update_product_db(product.code, new_name, product.price)
    print("El nombre del producto se modifico correctamente.")

def modification_price(product):
    new_price = get_price()
    db.update_product_db(product.code, product.name, new_price)
    print("El precio del producto se modifico correctamente.")

def modify_product():
    barcode = input("Escaneá el código del producto a modificar: ")
    product_to_modify = db.get_product_by_code(barcode)

    if product_to_modify is None:
        print("Producto no encontrado.")
    else:
        modification_menu(product_to_modify)
        rta = validate_menu(1,3)
        match rta:
            case 1:
                modification_name(product_to_modify)
            case 2:
                modification_price(product_to_modify)
            case 3:
                print("Volviendo al menú principal")

def show_product(): #Muestra los productos en la lista
    barcode = input("Escaneá el código de barras: ")
    product_to_show = db.get_product_by_code(barcode)

    if product_to_show is None:
        print("El producto no se encuentra en la base de datos.")
    else:
        print(product_to_show)

#Fin funciones
while True:
    menu()
    rta = validate_menu(1,5)

    match rta:
        case 1:
            add_product()
        case 2:
            modify_product()
        case 3:
            remove_product()
        case 4:
            show_product()
        case 5:
            print("Saliendo del programa.")
            break
        case _: # El guion bajo es el "comodín" (opción por defecto)
            print("Opción inválida.")