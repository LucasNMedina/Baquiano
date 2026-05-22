import customtkinter as ctk
import src.core.database as db

class SalesAPP(ctk.CTkToplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.grab_set()
        self.title("Baquiano - Ventas")
        self.geometry("500x550")
        self.total_purchease = 0.0
        
        #Label código de barras
        self.lbl_entry_barcode = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.lbl_entry_barcode.pack(pady = 5)

        #Lector código de barras
        self.entry_barcode = ctk.CTkEntry(self, placeholder_text="Ej: 0123456748910", width=300)
        self.entry_barcode.pack(pady = 5)
        self.entry_barcode.bind("<Return>", self.sell_product)

        #Label de total
        self.lbl_total = ctk.CTkLabel(self, text=f"Total: ${self.total_purchease:.2f}", text_color="orange", font=("Arial", 25))
        self.lbl_total.pack(pady = 5)

        #Label muestra error
        self.lbl_error = ctk.CTkLabel(self, text="")
        self.lbl_error.pack(pady = 5)

        #TextBox de productos
        self.txtbox_product_list = ctk.CTkTextbox(self, width=450, height=300, font=("Arial", 20))
        self.txtbox_product_list.pack(pady = 5)
        self.txtbox_product_list.configure(state="disabled")

        #Botón de finalizar
        self.btn_finish = ctk.CTkButton(self, text="Finalizar venta", command=self.end_sale)
        self.btn_finish.pack(pady = 15)

    def sell_product(self, event):
        barcode = self.entry_barcode.get().strip()
        product = db.get_product_by_code(barcode)

        if db.product_exist(barcode):
            self.lbl_error.configure(text="")
            self.total_purchease += product.precio
            self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}")
            self.actualizar_textbox(product.nombre, product.precio)
            self.entry_barcode.delete(0, "end")
        elif barcode.startswith("+"):
            try:
                manual_price = float(barcode[1:])
                self.total_purchease += manual_price
                
                self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}")
                self.actualizar_textbox("Fiambreria", manual_price)
                self.entry_barcode.delete(0, "end")
            except ValueError:
                self.lbl_error.configure(text="Debés ingresar un monto valido.")
                self.entry_barcode.delete(0, "end")
        else:
            self.lbl_error.configure(text="El producto no existe.")
            self.entry_barcode.delete(0, "end")

    def end_sale(self):
        self.total_purchease = 0.0

        # Limpiar el Textbox:
        self.txtbox_product_list.configure(state="normal") # Habilitar
        self.txtbox_product_list.delete("1.0", "end")      # Borrar desde la línea 1, carácter 0 hasta el final 
        self.txtbox_product_list.configure(state="disabled") # Bloquear

        self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}")
        self.lbl_error.configure(text="¡Muchas Gracias por comprar!")
    
    def actualizar_textbox(self, nombre, precio):
        # Configuramos "normal" para podes escribir
        self.txtbox_product_list.configure(state="normal")

        # Insertamos al final con "end"
        self.txtbox_product_list.insert("end", f"{nombre} - ${precio:.2f}\n")

        #Se bloquea nuevamente
        self.txtbox_product_list.configure(state="disabled")
        
        #Hacer que el scrol baje solo
        self.txtbox_product_list.see("end")

if __name__ == "__main__":
    app = SalesAPP()
    app.mainloop()
