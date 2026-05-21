import database as db
from models import Producto
#Funciones
def menu(): #Muestra el menú
    print("---Sistema 'Baquiano'---")
    print("1.Agregar producto")
    print("2.Modificar producto")
    print("3.Eliminar producto")
    print("4.Mostrar productos")
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

def get_product(inventory_list): #Obtiene los datos para el producto y lo devuelve creado
    produc_codigo = input("Escaneá el código de barras: ")

    if db.product_exist(inventory_list, produc_codigo):
        print("El producto ya se encuentra agregado.")
        return None

    produc_nombre = input("Colocá el nombre del producto: ").strip().capitalize()
    produc_precio = get_price()

    #Devuelvo el producto ya creado
    return Producto(produc_codigo, produc_nombre, produc_precio)

def add_product(inventory_list):
    product = get_product(inventory_list)
    if product:
        inventory_list.append(product)
        print(f"{product.nombre} agregado correctamente!")
        db.save_file(inventory_list)

def request_and_get_product_by_code(inventory_list): #Busca un producto en la lista 
    code = input("Escaneá el codigo del producto: ")
    return db.get_product_by_code(inventory_list, code)

def remove_product(inventory_list): #Elimina un producto de la lista
    p = request_and_get_product_by_code(inventory_list)
    if p is None:
        print("Producto no encontrado.")
    else:
        inventory_list.remove(p)
        print(f"Producto '{p.nombre}' eliminado exitosamente.")
    db.save_file(inventory_list)

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
    product.nombre = new_name
    print("El producto se modifico correctamente.")

def modification_price(product):
    new_price = get_price()
    product.precio = new_price
    print("El producto se modifico correctamente.")

def modify_product(inventory_list):
    p = request_and_get_product_by_code(inventory_list)
    if p is None:
        print("Producto no encontrado.")
    else:
        modification_menu(p)
        rta = validate_menu(1,3)
        match rta:
            case 1:
                modification_name(p)
                db.save_file(inventory_list)
            case 2:
                modification_price(p)
                db.save_file(inventory_list)
            case 3:
                print("Volviendo al menú principal")

def show_products(inventory_list): #Muestra los productos en la lista
    if not inventory_list:
        print("No hay productos para mostrar.")
    else:
        for p in inventory_list:
            print(p)

#Fin funciones
inventario = db.load_file()
while True:
    menu()
    rta = validate_menu(1,5)

    match rta:
        case 1:
            add_product(inventario)
        case 2:
            modify_product(inventario)
        case 3:
            remove_product(inventario)
        case 4:
            show_products(inventario)
        case 5:
            print("Saliendo del programa.")
            db.save_file(inventario)
            break
        case _: # El guion bajo es el "comodín" (opción por defecto)
            print("Opción inválida.")