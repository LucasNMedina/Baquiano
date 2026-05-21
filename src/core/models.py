class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    #Lo convierto en diccionario para poder guardar el archivo JSON
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio
        }

    def __str__(self):
        return f"Codigo: {self.codigo}\nProducto: {self.nombre} - Precio: ${self.precio:.2f}"