import customtkinter as ctk
import src.core.database as db
from src.core.models import Producto

# --- VENTANA EMERGENTE PARA AGREGAR PRODUCTO ---
class AgregarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nuevo Producto")
        self.geometry("350x300")

        # Esto hace que tenga que cerrar esta ventana antes de volver a tocar la principal
        self.grab_set()

        self.label_entrada = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.label_entrada.pack(pady = 5)

        #Lector codigo de barras
        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entrada_codigo.pack(pady = 5)

        self.label_nombre_producto = ctk.CTkLabel(self, text="Coloca el nombre del producto: ", font=("Arial", 15))
        self.label_nombre_producto.pack(pady = 5)

        #Entrada nombre
        self.entrada_nombre_producto = ctk.CTkEntry(self, placeholder_text="Yerba 'Playadito'", width=300)
        self.entrada_nombre_producto.pack(pady = 5)

        self.label_precio_producto = ctk.CTkLabel(self, text="Coloca el precio del producto: ", font=("Arial", 15))
        self.label_precio_producto.pack(pady = 5)

        #Entrada precio
        self.entrada_precio_producto = ctk.CTkEntry(self, placeholder_text="1500", width=300)
        self.entrada_precio_producto.pack(pady = 5)

        
        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.label_error.pack(pady = 5)

        #Boton agregar
        self.boton_finalizar = ctk.CTkButton(self, text="Guardar producto", command=self.add_product)
        self.boton_finalizar.pack(pady = 5)

    def add_product(self):
            code = self.entrada_codigo.get().strip()
            name = self.entrada_nombre_producto.get().strip().capitalize()
            price_txt = self.entrada_precio_producto.get().strip()

            #No dejar vacios
            if not code or not name or not price_txt:
                self.label_error.configure(text="Todos los campos son obligatorios.")
                return

            try:
                 price = float(price_txt)
            except ValueError:
                self.label_error.configure(text="El valor en precio no es valido.")
                return
            
            exito = db.add_product_db(code, name, price)
            if exito:
                self.destroy()
            else:
                self.label_error.configure(text="El producto ya existe en el sistema.")

# --- VENTANA EMERGENTE PARA MODIFICAR PRODUCTO ---
class ModificarApp(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modificar producto")
        self.geometry("350x100")
        self.producto_a_modificar = None

        self.grab_set()

        self.label_modificar = ctk.CTkLabel(self, text="Escaneá el producto que queres modificar", font=("Arial",12))
        self.label_modificar.pack(pady = 5)

        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entrada_codigo.pack(pady = 5)
        self.entrada_codigo.bind("<Return>", self.modificar_producto)

        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.label_error.pack(pady = 5)

        #Solo creo los labels pero todavia no lo muestro
        self.label_consulta = ctk.CTkLabel(self, text="¿Qué deseas modificar del producto? ", font=("Arial", 12))
        self.label_nombre = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nuevo nombre", width=200, height=15)
        self.label_precio = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.entry_precio = ctk.CTkEntry(self, placeholder_text="Nuevo precio", width=200, height=15)
    
        self.boton_finalizar = ctk.CTkButton(self, text="Guardar producto", command=self.guardar_cambios)
    
    def modificar_producto(self, event):
        codigo = self.entrada_codigo.get()
        self.producto_a_modificar = db.get_product_by_code(codigo)

        if self.producto_a_modificar:
            self.geometry("350x325")
            self.label_error.configure(text="")
            self.label_error.pack()

            #hago aparecer los labels
            self.label_consulta.pack(pady = 2)
            
            #---Nombre---
            self.label_nombre.configure(text=f"Nombre : {self.producto_a_modificar.nombre}")
            self.label_nombre.pack(pady = 5)
            self.entry_nombre.pack(pady = 1)

            #---Precio---
            self.label_precio.configure(text=f"Precio : ${self.producto_a_modificar.precio}")
            self.label_precio.pack(pady = 5)
            self.entry_precio.pack(pady = 1)

            #--Boton--
            self.boton_finalizar.pack(pady = 10)
            self.entrada_codigo.configure(state="disabled")
        else:
            self.label_error.configure(text="El producto no se encuentra en la base de datos.")
            self.entrada_codigo.delete(0, "end")
            self.entrada_codigo.focus()

    def guardar_cambios(self):
        nuevo_nombre = self.entry_nombre.get().strip().capitalize()
        nuevo_precio_texto = self.entry_precio.get()

        if not nuevo_nombre and not nuevo_precio_texto:
            self.label_error.configure(text="Al menos uno de los campos debe ser cambiado.")
            return
        
        # 2. Si escribió un nombre nuevo, lo actualizamos
        if nuevo_nombre:
            self.producto_a_modificar.nombre = nuevo_nombre

        # 3. Si escribió un precio nuevo, lo validamos e intentamos actualizarlo
        if nuevo_precio_texto:
            try:
                self.producto_a_modificar.precio = float(nuevo_precio_texto)
            except ValueError:
                self.label_error.configure(text="El valor en precio no es válido.")
                return
            
        self.destroy()

# --- VENTANA EMERGENTE PARA ELIMINAR PRODUCTO ---
class EliminarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eliminar producto")
        self.geometry("350x100")
        self.producto_a_eliminar = None

        self.grab_set()

        self.label_modificar = ctk.CTkLabel(self, text="Escaneá el producto que queres eliminar", font=("Arial",12))
        self.label_modificar.pack(pady = 5)

        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entrada_codigo.pack(pady = 5)
        self.entrada_codigo.bind("<Return>", self.ventana_eliminar)

        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.label_error.pack(pady = 5)

        self.label_nombre_producto = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.label_precio_producto = ctk.CTkLabel(self, text="", font=("Arial", 12))

        self.boton_eliminar = ctk.CTkButton(self, text="Eliminar", command=self.eliminar_producto)

    def ventana_eliminar(self, event):
        codigo = self.entrada_codigo.get()
        self.producto_a_eliminar = db.get_product_by_code(codigo)

        if self.producto_a_eliminar:
            self.label_error.configure(text="")
            self.geometry("350x250")

            self.label_nombre_producto.configure(text=f"Nombre : {self.producto_a_eliminar.nombre}")
            self.label_nombre_producto.pack(pady = 1)

            self.label_precio_producto.configure(text=f"Precio : {self.producto_a_eliminar.precio}")
            self.label_precio_producto.pack(pady = 1)

            self.boton_eliminar.pack(pady = 5)
            self.entrada_codigo.configure(state="disabled")
        else:
            self.label_error.configure(text="El producto no se encuentra en la base de datos.")
            self.entrada_codigo.delete(0, "end")
            self.entrada_codigo.focus()

    def eliminar_producto(self):
        codigo = self.producto_a_eliminar.codigo
        db.delete_product_db(codigo)
        self.destroy()

# --- VENTANA EMERGENTE PARA MOSTRAR PRODUCTO ---
class MostrarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Mostrar producto")
        self.geometry("350x150")
        self.producto_a_mostrar = None

        self.grab_set()

        self.label_modificar = ctk.CTkLabel(self, text="Escaneá el producto que queres mostrar", font=("Arial",12))
        self.label_modificar.pack(pady = 5)

        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entrada_codigo.pack(pady = 5)
        self.entrada_codigo.bind("<Return>", self.ventana_mostrar)

        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.label_error.pack(pady = 5)
        
        self.label_nombre_producto = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.label_precio_producto = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.boton_volver = ctk.CTkButton(self, text="Volver", command=self.volver_atras)

    def ventana_mostrar(self, event):
        codigo = self.entrada_codigo.get()
        if not db.product_exist(codigo):
            self.label_error.configure(text="El producto no se encuentra en la base de datos.")
            self.entrada_codigo.delete(0, "end")
            self.entrada_codigo.focus()
        else:
            self.producto_a_mostrar = db.get_product_by_code(codigo)
            self.label_error.configure(text="")
            self.geometry("350x225")

            self.label_nombre_producto.configure(text=f"Nombre: {self.producto_a_mostrar.nombre}")
            self.label_nombre_producto.pack(pady = 2)

            self.label_precio_producto.configure(text=f"Precio: {self.producto_a_mostrar.precio}")
            self.label_precio_producto.pack(pady = 2)

            self.boton_volver.pack(pady = 5)
            self.entrada_codigo.configure(state="disabled")

    def volver_atras(self):
        self.destroy()

# --- VENTANA PRINCIPAL DE ADMINISTRACIÓN ---
class AdminAPP(ctk.CTkToplevel):
    def __init__(self, parent=None, fg_color = None, **kwargs):
        super().__init__(parent)
        self.title(" Baquiano - Administración")
        self.geometry("400x210")

        self.label_bienvenida = ctk.CTkLabel(self, text="Administración de productos", font=("Arial",16), text_color="orange")
        self.label_bienvenida.pack(pady = 5)

        self.boton_agregar_producto = ctk.CTkButton(self, text="Agregar Producto", command=self.abrir_ventana_agregar)
        self.boton_agregar_producto.pack(pady = 5)

        self.boton_modificar_producto = ctk.CTkButton(self, text="Modificar Producto", command=self.abrir_ventana_modificar)
        self.boton_modificar_producto.pack(pady = 5)

        self.boton_eliminar_producto = ctk.CTkButton(self, text="Eliminar Producto", command=self.abrir_ventana_eliminar)
        self.boton_eliminar_producto.pack(pady = 5)

        self.boton_mostrar_producto = ctk.CTkButton(self, text="Mostrar Producto", command=self.abrir_ventana_mostrar)
        self.boton_mostrar_producto.pack(pady = 5)

    def abrir_ventana_agregar(self):
        # Abrimos la ventana emergente pasándole el inventario actual
        AgregarAPP(self)
    
    def abrir_ventana_modificar(self):
        ModificarApp(self)

    def abrir_ventana_eliminar(self):
        EliminarAPP(self)

    def abrir_ventana_mostrar(self):
        MostrarAPP(self)

if __name__ == "__main__":
    app = AdminAPP()
    app.mainloop()
