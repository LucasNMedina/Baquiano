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

    def abrir_ventana_agregar(self):
        # Abrimos la ventana emergente pasándole el inventario actual
        AgregarAPP(self, self.inventario)
    #def agregar_producto():
if __name__ == "__main__":
    app = AdminAPP()
    app.mainloop()

"""
        #Lector codigo de barras
        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Escaneá el código de barras", width=300, height=15)
        self.entrada_codigo.pack(pady = 5)
"""