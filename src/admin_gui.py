import customtkinter as ctk
import database as db
from models import Producto

# --- VENTANA EMERGENTE PARA AGREGAR PRODUCTO ---
class AgregarAPP(ctk.CTkToplevel):
    def __init__(self, parent, inventario):
        super().__init__(parent)
        self.title("Nuevo Producto")
        self.geometry("350x300")
        self.inventario = inventario

        # Esto hace que Florencia tenga que cerrar esta ventana antes de volver a tocar la principal
        self.grab_set()

        self.label_entrada = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.label_entrada.pack(pady = 5)

        #Lector codigo de barras
        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300, height=15)
        self.entrada_codigo.pack(pady = 5)

        self.label_nombre_producto = ctk.CTkLabel(self, text="Coloca el nombre del producto: ", font=("Arial", 15))
        self.label_nombre_producto.pack(pady = 5)

        #Entrada nombre
        self.entrada_nombre_producto = ctk.CTkEntry(self, placeholder_text="Yerba 'Playadito'", width=300, height=15)
        self.entrada_nombre_producto.pack(pady = 5)

        self.label_precio_producto = ctk.CTkLabel(self, text="Coloca el precio del producto: ", font=("Arial", 15))
        self.label_precio_producto.pack(pady = 5)

        #Entrada precio
        self.entrada_precio_producto = ctk.CTkEntry(self, placeholder_text="1500", width=300, height=15)
        self.entrada_precio_producto.pack(pady = 5)

        
        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.label_error.pack(pady = 5)

        #Boton agregar
        self.boton_finalizar = ctk.CTkButton(self, text="Guardar producto", command=self.add_product)
        self.boton_finalizar.pack(pady = 15)

    def add_product(self):
            codigo = self.entrada_codigo.get().strip()
            nombre = self.entrada_nombre_producto.get().strip()
            precio_texto = self.entrada_precio_producto.get().strip()

            #No dejar vacios
            if not codigo or not nombre or not precio_texto:
                self.label_error.configure(text="Todos los campos son obligatorios.")
                return

            try:
                 precio = float(precio_texto)
            except ValueError:
                self.label_error.configure(text="El valor en precio no es valido.")
                return
            
            if db.product_exist(self.inventario,codigo):
                self.label_error.configure(text="El producto ya existe en el sistema.")
            else:
                nuevo_producto = Producto(codigo, nombre, precio)
                self.inventario.append(nuevo_producto)
                db.save_file(self.inventario)

                print(f"¡{nombre} agregado con éxito!")
                self.destroy() # Cierra la ventanita automáticamente al terminar

# --- VENTANA EMERGENTE PARA AGREGAR PRODUCTO ---
class ModificarApp(ctk.CTkToplevel):
    def __init__(self, parent, inventario):
        super().__init__(parent)
        self.title("Modificar producto")
        self.geometry("350x250")
        self.inventario = inventario

        self.grab_set()

# --- VENTANA PRINCIPAL DE ADMINISTRACIÓN ---
class AdminAPP(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__()
        self.title(" Baquiano - Administración")
        self.geometry("500x400")
        self.inventario = db.load_file()

        self.label_bienvenida = ctk.CTkLabel(self, text="Bienvenida Florencia - ¿Qué hacemos hoy?", font=("Arial",14), text_color="orange")
        self.label_bienvenida.pack(pady = 5)

        self.boton_agregar_producto = ctk.CTkButton(self, text="Agregar Producto", command=self.abrir_ventana_agregar)
        self.boton_agregar_producto.pack(pady = 5)

        self.boton_modificar_producto = ctk.CTkButton(self, text="Modificar Producto", command=self.abrir_ventana_modificar)
        self.boton_modificar_producto.pack(pady = 5)

    def abrir_ventana_agregar(self):
        # Abrimos la ventana emergente pasándole el inventario actual
        AgregarAPP(self, self.inventario)
    
    def abrir_ventana_modificar(self):
        ModificarApp(self,self.inventario)

if __name__ == "__main__":
    app = AdminAPP()
    app.mainloop()
