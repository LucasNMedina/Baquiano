import customtkinter as ctk
import src.core.database as db
from src.services.ticket_printer import imprimir_ticket_systel

class SalesAPP(ctk.CTkToplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.title("Baquiano - Ventas")
        self.geometry("500x550")
        self.grab_set()

        self.total_purchease = 0.0
        self.productos_actuales = [] #para el ticket

        #Label código de barras
        self.lbl_entry_barcode = ctk.CTkLabel(self, text="Escaneá el código de barras: ", font=("Arial", 15))
        self.lbl_entry_barcode.pack(pady = 5)

        #Lector código de barras
        self.entry_barcode = ctk.CTkEntry(self, width=300)
        self.entry_barcode.pack(pady = 5)
        self.entry_barcode.bind("<Return>", self.sell_product)

        # --- NUEVO COMPONENTE: CHECKBOX PARA EL TICKET ---
        self.check_ticket_var = ctk.BooleanVar(value=True) # Activado por defecto
        self.checkbox_ticket = ctk.CTkCheckBox(
            self, 
            text="¿Imprimir Ticket?", 
            variable=self.check_ticket_var,
            font=("Arial", 14)
        )
        self.checkbox_ticket.pack(pady = 5, side="bottom")

        self.btn_end_sale = ctk.CTkButton(self, text="Terminar Venta", command=self.end_sale, font=("Arial", 14, "bold"))
        self.btn_end_sale.pack(pady = 10, side="bottom")

        self.lbl_error = ctk.CTkLabel(self, text="")
        self.lbl_error.pack(pady = 5, side="bottom")

        self.lbl_total = ctk.CTkLabel(self, text=f"Total: ${self.total_purchease:.2f}", text_color="orange", font=("Arial", 25, "bold"))
        self.lbl_total.pack(pady = 10, side="bottom")

        self.txtbox_product_list = ctk.CTkTextbox(self, width=450, height=300, font=("Arial", 20))
        self.txtbox_product_list.configure(state="disabled")
        self.txtbox_product_list.pack(pady = 5, fill="both", expand=True)

        self.after(100, self.entry_barcode.focus) #Esto es para darle tiempo a cargue todo los componentes
        self.btn_end_sale.bind("<Return>", lambda event: self.end_sale())
    def sell_product(self, event):
        barcode = self.entry_barcode.get().strip()
        product = db.get_product_by_code(barcode)

        if product:
            self.lbl_error.configure(text="")
            self.total_purchease += product.price
            self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}")
            self.update_textbox(product.name, product.price)

            # Guardamos el producto en nuestra lista para el ticket (cantidad fija 1 por escaneo)
            self.productos_actuales.append({
                "cantidad": 1,
                "nombre": product.name,
                "precio_total": product.price
            })

            self.entry_barcode.delete(0, "end")
        elif barcode.startswith("."):
            try:
                manual_price = float(barcode[1:])
                
                if manual_price <= 0:
                    self.lbl_error.configure(text="El monto debe ser mayor a 0.", text_color="red")
                    self.entry_barcode.delete(0, "end")
                    return
                
                self.total_purchease += manual_price
                
                self.lbl_error.configure(text="")
                self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}")
                self.update_textbox("Fiambreria", manual_price)

                # Guardamos la venta manual en nuestra lista para el ticket
                self.productos_actuales.append({
                    "cantidad": 1,
                    "nombre": "Fiambreria",
                    "precio_total": manual_price
                })

                self.entry_barcode.delete(0, "end")
            except ValueError:
                self.lbl_error.configure(text="Debés ingresar un monto valido.", text_color = "red")
                self.entry_barcode.delete(0, "end")
        else:
            self.lbl_error.configure(text="El producto no existe.", text_color = "red")
            self.entry_barcode.delete(0, "end")

        self.entry_barcode.focus()

    def end_sale(self):
        if self.btn_end_sale.cget("text") == "Terminar Venta":
            if self.total_purchease == 0:
                self.lbl_error.configure(text="No hay productos en la venta actual.", text_color="red")
                return
            
            # --- MANDAR A IMPRIMIR SI EL CHECKBOX ESTÁ ACTIVO ---
            if self.check_ticket_var.get():
                # Cambiá "COM3" por el puerto real que use la Systel en el mostrador
                exito_ticket = imprimir_ticket_systel(self.productos_actuales, self.total_purchease, puerto_com="COM3")
                if not exito_ticket:
                    # Si falla por un cable desconectado o puerto apagado, avisa en rojo pero te deja continuar
                    self.lbl_error.configure(text="Error de tiquetera. Venta guardada igualmente.", text_color="red")
            
            self.entry_barcode.configure(state="disabled")
            self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}", text_color="green")
            #self.lbl_error.configure(text="Venta registrada. Presioná para continuar.", text_color="green")

            # Si no hubo error previo de ticket, mostramos el éxito común
            if self.lbl_error.cget("text") == "":
                self.lbl_error.configure(text="Venta registrada. Presioná para continuar.", text_color="green")

            self.btn_end_sale.configure(text="Nueva Venta")
        
        else:
            self.total_purchease = 0.0
            self.productos_actuales = []
            self.entry_barcode.configure(state="normal")
            
            self.lbl_total.configure(text=f"Total: ${self.total_purchease:.2f}", text_color="orange")
            self.lbl_error.configure(text="")

            #TextBox
            self.txtbox_product_list.configure(state="normal") # Habilitar
            self.txtbox_product_list.delete("1.0", "end")      # Borrar desde la línea 1, carácter 0 hasta el final 
            self.txtbox_product_list.configure(state="disabled") # Bloquear

            self.btn_end_sale.configure(text="Terminar Venta")

            self.entry_barcode.delete(0, "end")
            self.entry_barcode.focus()

    def update_textbox(self, name, price):
        # Configuramos "normal" para podes escribir
        self.txtbox_product_list.configure(state="normal")

        # Insertamos al final con "end"
        self.txtbox_product_list.insert("end", f"{name} - ${price:.2f}\n")

        #Se bloquea nuevamente
        self.txtbox_product_list.configure(state="disabled")
        
        #Hacer que el scrol baje solo
        self.txtbox_product_list.see("end")

if __name__ == "__main__":
    app = SalesAPP()
    app.mainloop()
