class Producto:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    #Lo convierto en diccionario para poder guardar el archivo JSON
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio
        }

    def __str__(self):
        return f"Codigo: {self.code}\nProducto: {self.name} - Precio: ${self.price:.2f}"