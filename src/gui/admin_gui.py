import customtkinter as ctk
import src.core.database as db
from src.core.models import Producto

# --- VENTANA EMERGENTE PARA AGREGAR PRODUCTO ---
class AgregarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nuevo Producto")
        self.geometry("350x340")

        # Esto hace que tenga que cerrar esta ventana antes de volver a tocar la principal
        self.grab_set()

        self.lbl_barcode = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.lbl_barcode.pack(pady = 5)

        #Lector codigo de barras
        self.entry_barcode = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entry_barcode.pack(pady = 5)

        self.lbl_product_name = ctk.CTkLabel(self, text="Coloca el nombre del producto: ", font=("Arial", 15))
        self.lbl_product_name.pack(pady = 5)

        #Entrada nombre
        self.entry_product_name = ctk.CTkEntry(self, placeholder_text="Yerba 'Playadito'", width=300)
        self.entry_product_name.pack(pady = 5)

        self.lbl_product_price = ctk.CTkLabel(self, text="Coloca el precio del producto: ", font=("Arial", 15))
        self.lbl_product_price.pack(pady = 5)

        #Entrada precio
        self.entry_product_price = ctk.CTkEntry(self, placeholder_text="1500", width=300)
        self.entry_product_price.pack(pady = 5)

        self.lbl_result_info = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.lbl_result_info.pack(pady = 5)

        #Boton agregar
        self.btn_finish = ctk.CTkButton(self, text="Guardar producto", command=self.add_product)
        self.btn_finish.pack(pady = 5)

        self.btn_back = ctk.CTkButton(self, text="Volver", command=self.back_to_menu)
        self.btn_back.pack(pady = 2)

        self.after(100, self.entry_barcode.focus)
    def add_product(self):
            code = self.entry_barcode.get().strip()
            name = self.entry_product_name.get().strip().capitalize()
            price_txt = self.entry_product_price.get().strip()

            #No dejar vacios
            if not code or not name or not price_txt:
                self.lbl_result_info.configure(text="Todos los campos son obligatorios.", text_color="red")
                return

            try:
                price = float(price_txt)
                if price <= 0:
                    self.lbl_result_info.configure(text="El precio debe ser un número mayor a 0.", text_color="red")
                    return
            except ValueError:
                self.lbl_result_info.configure(text="El valor en precio no es valido.", text_color="red")
                return
            
            exito = db.insert_product_db(code, name, price)
            if exito:
                self.lbl_result_info.configure(text="Producto guardado correctamente.", text_color="green")
                self.entry_barcode.delete(0, "end")
                self.entry_product_name.delete(0, "end")
                self.entry_product_price.delete(0, "end")

                self.entry_barcode.focus()
            else:
                self.lbl_result_info.configure(text="El producto ya existe en el sistema.", text_color="red")

    def back_to_menu(self):
        self.destroy()

# --- VENTANA EMERGENTE PARA MODIFICAR PRODUCTO ---
class ModificarApp(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modificar producto")
        self.geometry("350x360")
        self.grab_set()

        self.product_to_modify = None

        self.lbl_modify = ctk.CTkLabel(self, text="Escaneá el producto que queres modificar", font=("Arial",12, "bold"))
        self.lbl_modify.pack(pady = 5)

        self.entry_barcode = ctk.CTkEntry(self, width=300)
        self.entry_barcode.pack(pady = 5)
        self.entry_barcode.bind("<Return>", self.modify_product)

        self.lbl_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.lbl_error.pack(pady = 5)

        self.frame_modify = ctk.CTkFrame(self, fg_color="transparent")

        #Solo creo los labels pero todavia no lo muestro
        self.lbl_ask = ctk.CTkLabel(self.frame_modify, text="¿Qué deseas modificar del producto? ", font=("Arial", 12))
        self.lbl_name = ctk.CTkLabel(self.frame_modify, text="", font=("Arial", 12))
        self.entry_name = ctk.CTkEntry(self.frame_modify, width=200)
        self.lbl_price = ctk.CTkLabel(self.frame_modify, text="", font=("Arial", 12))
        self.entry_price = ctk.CTkEntry(self.frame_modify, width=200)
    
        self.btn_save_product = ctk.CTkButton(self.frame_modify, text="Guardar producto", command=self.finalizar_modificacion)
    
        #hago aparecer los labels
        self.lbl_ask.pack(pady = 2)          
        self.lbl_name.pack(pady = 5)
        self.entry_name.pack(pady = 1)
        self.lbl_price.pack(pady = 5)
        self.entry_price.pack(pady = 1)
        self.btn_save_product.pack(pady = 5)

        self.btn_back = ctk.CTkButton(self, text="Volver", command=self.volver_atras)
        self.btn_back.pack(pady = 2, side="bottom")

        self.after(100, self.entry_barcode.focus)
    def modify_product(self, event):
        barcode = self.entry_barcode.get().strip()
        self.product_to_modify = db.get_product_by_code(barcode)

        if self.product_to_modify:
            self.lbl_error.configure(text="")
            self.lbl_name.configure(text=f"Nombre : {self.product_to_modify.name}")
            self.lbl_price.configure(text=f"Precio : ${self.product_to_modify.price}")

            self.entry_name.delete(0, "end")
            self.entry_price.delete(0, "end")

            self.frame_modify.pack(pady = 5, fill="x")
        else:
            self.lbl_error.configure(text="El producto no se encuentra en la base de datos.", text_color="red")
            self.frame_modify.pack_forget()

        self.entry_barcode.delete(0, "end")
        self.entry_barcode.focus()

    def finalizar_modificacion(self):
        if not self.product_to_modify:
            self.lbl_error.configure(text="Primero debes escanear un producto válido.", text_color="red")
            return
        
        # 1. Recuperamos el código del producto que se buscó
        barcode = self.product_to_modify.code

        # 2. Leemos los entry
        new_name = self.entry_name.get().strip().capitalize()
        new_price_txt = self.entry_price.get().strip()

        # Usamos validación: Si no escribió nada en ningún lado, avisamos
        if not new_name and not new_price_txt:
            self.lbl_error.configure(text="Al menos uno de los campos debe ser cambiado.")
            return
        
        # Si dejó el nombre vacío, se queda con el que ya tenía antes
        if not new_name:
            new_name = self.product_to_modify.name

        # Si dejó el precio vacío, se queda con el de antes. Si escribió, lo validamos
        if new_price_txt:
            try:
                new_price = float(new_price_txt)
                if new_price <= 0:
                    self.lbl_error.configure(text="El precio debe ser un número mayor a 0.", text_color="red")
                    return
            except ValueError:
                self.lbl_error.configure(text="El valor en precio no es válido.")
                return
        else:
            new_price = self.product_to_modify.price

        if db.update_product_db(barcode, new_name, new_price):
            self.frame_modify.pack_forget()
            self.entry_name.delete(0, "end")
            self.entry_price.delete(0, "end")
            self.lbl_error.configure(text="Producto actualizado correctamente.", text_color="green")
            self.entry_barcode.focus()
        else:
            self.lbl_error.configure(text="Error al guardar en la base de datos.", text_color="red")

    def volver_atras(self):
        self.destroy()
# --- VENTANA EMERGENTE PARA ELIMINAR PRODUCTO ---
class EliminarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eliminar producto")
        self.geometry("350x285")
        self.grab_set()

        self.product_to_eliminate = None

        self.lbl_modify = ctk.CTkLabel(self, text="Escaneá el producto que queres eliminar", font=("Arial",12))
        self.lbl_modify.pack(pady = 5)

        self.entry_barcode = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entry_barcode.pack(pady = 5)
        self.entry_barcode.bind("<Return>", self.ventana_eliminar)

        self.lbl_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.lbl_error.pack(pady = 5)

        self.frame_confirm_elimination = ctk.CTkFrame(self, fg_color="transparent")

        self.lbl_product_name = ctk.CTkLabel(self.frame_confirm_elimination, text="", font=("Arial", 12, "bold"))
        self.lbl_product_price = ctk.CTkLabel(self.frame_confirm_elimination, text="", font=("Arial", 12, "bold"))
        self.btn_eliminate = ctk.CTkButton(self.frame_confirm_elimination, text="Eliminar", command=self.eliminar_producto)

        self.lbl_product_name.pack(pady = 1)
        self.lbl_product_price.pack(pady = 1)
        self.btn_eliminate.pack(pady = 5)

        self.btn_back = ctk.CTkButton(self, text="Volver", command=self.volver_atras)
        self.btn_back.pack(pady = 15, side="bottom")
        
        self.after(100, self.entry_barcode.focus)
    def ventana_eliminar(self, event):
        barcode = self.entry_barcode.get()
        self.product_to_eliminate = db.get_product_by_code(barcode)

        if self.product_to_eliminate:
            self.lbl_error.configure(text="")

            self.lbl_product_name.configure(text=f"Nombre : {self.product_to_eliminate.name}")
            self.lbl_product_price.configure(text=f"Precio : {self.product_to_eliminate.price}")
        
            self.frame_confirm_elimination.pack(pady = 5, fill="x")
        else:
            self.lbl_error.configure(text="El producto no se encuentra en la base de datos.", text_color="red")
            self.frame_confirm_elimination.pack_forget()
        self.entry_barcode.delete(0, "end")
        self.entry_barcode.focus()    

    def eliminar_producto(self):
        barcode = self.product_to_eliminate.code
        if db.delete_product_db(barcode):
            self.frame_confirm_elimination.pack_forget()
            self.lbl_error.configure(text="Producto eliminado correctamente.", text_color="green")
            self.entry_barcode.focus()
        else:
            self.lbl_error.configure(text="Error al intentar eliminar de la base de datos.", text_color="red")
    
    def volver_atras(self):
        self.destroy()

# --- VENTANA EMERGENTE PARA MOSTRAR PRODUCTO ---
class MostrarAPP(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        #--- CONFIGURO LA VENTANA --- 
        self.title("Mostrar producto")
        self.geometry("350x250")
        self.resizable(False, False)
        self.grab_set()
        self.product_to_show = None

        self.lbl_modify = ctk.CTkLabel(self, text="Escaneá el producto que queres mostrar", font=("Arial",12))
        self.lbl_modify.pack(pady = 5)

        self.entry_barcode = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entry_barcode.pack(pady = 5)
        self.entry_barcode.bind("<Return>", self.ventana_mostrar)

        self.lbl_error = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.lbl_error.pack(pady = 5)
        
        #LA "CAJA INVISIBLE" (Frame) para los datos del producto.
        self.frame_data = ctk.CTkFrame(self, fg_color="transparent")

        self.lbl_product_name = ctk.CTkLabel(self.frame_data, text="", font=("Arial", 12, "bold"))
        self.lbl_product_price = ctk.CTkLabel(self.frame_data, text="", font=("Arial", 12, "bold"))

        self.lbl_product_name.pack(pady = 2)
        self.lbl_product_price.pack(pady = 2)

        # 1. EL CAMBIO CLAVE: El botón nace apuntando a la ventana (self)
        self.btn_back = ctk.CTkButton(self, text="Volver", command=self.volver_atras)
        # 2. Se empaqueta ACÁ MISMO fijándose abajo de todo. Ya no se mueve más.
        self.btn_back.pack(pady = 15, side="bottom")

        self.after(100, self.entry_barcode.focus)
    def ventana_mostrar(self, event):
        barcode = self.entry_barcode.get()
        self.product_to_show = db.get_product_by_code(barcode)

        if self.product_to_show:
            self.lbl_error.configure(text="")

            self.lbl_product_name.configure(text=f"Nombre: {self.product_to_show.name}")
            self.lbl_product_price.configure(text=f"Precio: {self.product_to_show.price}")

            # El .pack() acá hace aparecer la caja con todo lo que tiene adentro
            self.frame_data.pack(pady=5, fill="x")
        else:
            # Si NO existe: ESCONDEMOS la caja con .pack_forget() y mostramos error
            self.frame_data.pack_forget()
            self.lbl_error.configure(text="El producto no se encuentra en la base de datos.")
        self.entry_barcode.delete(0, "end")
        self.entry_barcode.focus()
    
    def volver_atras(self):
        self.destroy()

# --- VENTANA PRINCIPAL DE ADMINISTRACIÓN ---
class AdminAPP(ctk.CTkToplevel):
    def __init__(self, parent=None, fg_color = None, **kwargs):
        super().__init__(parent)
        self.title(" Baquiano - Administración")
        self.geometry("400x210")

        self.lbl_title = ctk.CTkLabel(self, text="Administración de productos", font=("Arial",16), text_color="orange")
        self.lbl_title.pack(pady = 5)

        self.btn_add_product = ctk.CTkButton(self, text="Agregar Producto", command=self.abrir_ventana_agregar)
        self.btn_add_product.pack(pady = 5)

        self.btn_modify_product = ctk.CTkButton(self, text="Modificar Producto", command=self.abrir_ventana_modificar)
        self.btn_modify_product.pack(pady = 5)

        self.btn_eliminate_product = ctk.CTkButton(self, text="Eliminar Producto", command=self.abrir_ventana_eliminar)
        self.btn_eliminate_product.pack(pady = 5)

        self.btn_show_product = ctk.CTkButton(self, text="Mostrar Producto", command=self.abrir_ventana_mostrar)
        self.btn_show_product.pack(pady = 5)

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
