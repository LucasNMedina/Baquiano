import json
from src.core.models import Producto

def save_file(list_products): #Guarda el archivo
    with open("data/inventory.json", "w") as archive:
        # Convierto cada objeto Producto a diccionario
        data_to_save = [p.to_dict() for p in list_products]

        #Guardo la lista de objetos en formato diccionario
        json.dump(data_to_save, archive, indent=4)
        print("file saved successfully")

def load_file(): #Carga el archivo
    try:
        with open("data/inventory.json", "r") as archive:
            data = json.load(archive)

            # Convertimos cada diccionario de nuevo en un objeto Producto
            return [Producto(d['codigo'], d['nombre'], d['precio']) for d in data]
    except FileNotFoundError:
        # Si el archivo no existe todavía, devolvemos una lista vacia
        return []
    except json.JSONDecodeError:
        # Si el archivo está vacío o corrupto, devolvemos una lista vacia
        return []
    
def product_exist(inventory_list, code):
    # Retorna True si el resultado no es None, de lo contrario False
    return get_product_by_code(inventory_list, code) is not None

def get_product_by_code(inventory_list, code):
    for p in inventory_list:
        if p.codigo == code:
            return p
    return None