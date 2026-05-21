import customtkinter as ctk
from src.gui.admin_gui import AdminAPP
from src.gui.sales_gui import SalesAPP

class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Baquiano - Sistema integrado")
        self.geometry("400x250")

        # Centrar la ventana en la pantalla
        self.resizable(False, False)

        # Título de bienvenida principal
        self.label_titulo = ctk.CTkLabel(self, text="BAQUIANO", font=("Arial", 24, "bold"), text_color="orange")
        self.label_titulo.pack(pady=20)

        self.label_subtitulo = ctk.CTkLabel(self, text="Seleccione el módulo con el que va a trabajar:", font=("Arial", 13))
        self.label_subtitulo.pack(pady=5)

        # Botón para ir a la pantalla de Ventas / Caja
        self.boton_ventas = ctk.CTkButton(self, text="🛒 Módulo de Ventas (Caja)", font=("Arial", 14), width=250, height=40, fg_color="#2b719e", command=self.abrir_ventas)
        self.boton_ventas.pack(pady=10)

        # Botón para ir a la pantalla de Administración
        self.boton_admin = ctk.CTkButton(self, text="⚙️ Módulo de Administración", font=("Arial", 14), width=250, height=40, fg_color="#de7a22", command=self.abrir_administracion)
        self.boton_admin.pack(pady=10)

    def abrir_ventas(self):
        # 1. Ocultamos el menú principal para que no estorbe
        self.withdraw()
        
        # 2. Abrimos la ventana de ventas
        ventana_ventas = SalesAPP()
        
        # 3. Truco mágico: Cuando Florencia cierre ventas, el menú vuelve a aparecer
        ventana_ventas.protocol("WM_DELETE_WINDOW", lambda: self.volver_al_menu(ventana_ventas))

    def abrir_administracion(self):
        # 1. Ocultamos el menú principal
        self.withdraw()
        
        # 2. Abrimos tu ventana de administración que testeamos recién
        ventana_admin = AdminAPP()
        
        # 3. Cuando cierre administración, el menú vuelve a aparecer
        ventana_admin.protocol("WM_DELETE_WINDOW", lambda: self.volver_al_menu(ventana_admin))

    def volver_al_menu(self, ventana_hija):
        # Destruimos la ventana que se estaba usando (ventas o admin)
        ventana_hija.destroy()
        # Hacemos visible el menú principal de nuevo
        self.deiconify()

if __name__ == "__main__":
    # Configuramos el estilo visual general del sistema
    ctk.set_appearance_mode("System")  # Toma el color del sistema (Claro/Oscuro)
    ctk.set_default_color_theme("blue") # Tema azul por defecto
    
    app = MenuPrincipal()
    app.mainloop()