class Producto:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def __str__(self):
        return f"Codigo: {self.code}\nProducto: {self.name} - Precio: ${self.price:.2f}"