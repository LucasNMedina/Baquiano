import customtkinter as ctk
import database as db

class SalesAPP(ctk.CTkToplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.grab_set()
        self.title("Baquiano - Ventas")
        self.geometry("500x550")
        self.database = db.load_file()
        self.total_cuenta = 0.0
        
        self.label_entrada = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.label_entrada.pack(pady = 5)

        #Lector codigo de barras
        self.entrada_codigo = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300, height=15)
        self.entrada_codigo.pack(pady = 5)
        self.entrada_codigo.bind("<Return>", self.vender_producto)

        #Label de total
        self.label_total = ctk.CTkLabel(self, text=f"Total: ${self.total_cuenta:.2f}", text_color="orange", font=("Arial", 25))
        self.label_total.pack(pady = 5)

        self.label_mostrar_codigo = ctk.CTkLabel(self, text="")
        self.label_mostrar_codigo.pack(pady = 5)

        self.lista_compras = ctk.CTkTextbox(self, width=450, height=300, font=("Arial", 20))
        self.lista_compras.pack(pady = 5)
        self.lista_compras.configure(state="disabled")

        self.boton_finalizar = ctk.CTkButton(self, text="Finalizar venta", command=self.finalizar_venta)
        self.boton_finalizar.pack(pady = 15)

    def vender_producto(self, event):
        codigo = self.entrada_codigo.get().strip()

        if db.product_exist(self.database, codigo):
            producto = db.get_product_by_code(self.database, codigo)
            self.total_cuenta += producto.precio
            self.label_total.configure(text=f"Total: ${self.total_cuenta:.2f}")
            self.actualizar_textbox(producto.nombre, producto.precio)
            
            self.entrada_codigo.delete(0, "end")
        elif codigo.startswith("+"):
            try:
                monto_manual = float(codigo[1:])
                self.total_cuenta += monto_manual
                
                self.label_total.configure(text=f"Total: ${self.total_cuenta:.2f}")
                self.actualizar_textbox("Fiambreria", monto_manual)
                self.entrada_codigo.delete(0, "end")
            except ValueError:
                self.label_mostrar_codigo.configure(text="Debés ingresar un monto valido.")
                self.entrada_codigo.delete(0, "end")
        else:
            self.label_mostrar_codigo.configure(text="El producto no existe.")
            self.entrada_codigo.delete(0, "end")

    def finalizar_venta(self):
        self.total_cuenta = 0.0

        # Limpiar el Textbox:
        self.lista_compras.configure(state="normal") # Habilitar
        self.lista_compras.delete("1.0", "end")      # Borrar desde la línea 1, carácter 0 hasta el final 
        self.lista_compras.configure(state="disabled") # Bloquear

        self.label_total.configure(text=f"Total: ${self.total_cuenta:.2f}")
        self.label_mostrar_codigo.configure(text="¡Muchas Gracias por comprar!")
    
    def actualizar_textbox(self, nombre, precio):
        # Configuramos "normal" para podes escribir
        self.lista_compras.configure(state="normal")

        # Insertamos al final con "end"
        self.lista_compras.insert("end", f"{nombre} - ${precio:.2f}\n")

        #Se bloquea nuevamente
        self.lista_compras.configure(state="disabled")
        
        #Hacer que el scrol baje solo
        self.lista_compras.see("end")

if __name__ == "__main__":
    app = SalesAPP()
    app.mainloop()
