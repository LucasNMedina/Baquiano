import win32print
import datetime

def buscar_tiquetera_automatica():
    """
    Recorre todas las impresoras instaladas en Windows y devuelve el nombre
    de la primera que encuentre que sea genérica (tiquetera).
    """
    try:
        # Le pedimos a Windows la lista de todas las impresoras locales
        impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        
        for impresora in impresoras:
            nombre_impresora = impresora[2]  # Índice 2 contiene el nombre en texto
            nombre_min = nombre_impresora.lower()
            
            # Si contiene 'generic', 'text' o 'only', encontramos la tiquetera (con o sin Copia 1)
            if "generic" in nombre_min or "text" in nombre_min or "only" in nombre_min:
                print(f"-> Tiquetera detectada automáticamente: {nombre_impresora}")
                return nombre_impresora
    except Exception as e:
        print(f"Error al buscar impresoras en Windows: {e}")
    
    # Si no encuentra ninguna, devuelve None
    return None

def imprimir_ticket_systel(lista_productos, total, nombre_impresora=None):
    """
    Envía el ticket formateado directamente a la tiquetera Systel GP-5890XIII
    utilizando detección automática de nombre y plan de emergencia.
    """
    try:
        # --- DETECCIÓN INTELIGENTE DE NOMBRE ---
        # Si no le pasamos un nombre específico, o si viene el genérico por defecto, busca de forma inteligente
        if nombre_impresora is None or nombre_impresora == "Generic / Text Only":
            nombre_detectado = buscar_tiquetera_automatica()
            if nombre_detectado:
                nombre_impresora = nombre_detectado
            else:
                # 🚨 PLAN DE EMERGENCIA ABSOLUTO: Si falló el "Generic", buscamos CUALQUIER tiquetera física activa
                print("⚠️ Alerta: No se encontró 'Generic'. Iniciando plan de emergencia...")
                try:
                    impresoras_locales = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
                    for imp in impresoras_locales:
                        nom = imp[2]
                        nom_min = nom.lower()
                        # Descartamos las virtuales de Windows para no mandar el ticket a un PDF o Fax
                        if "pdf" not in nom_min and "xps" not in nom_min and "fax" not in nom_min and "onenote" not in nom_min:
                            print(f"🚨 ¡Comodín de emergencia activado! Imprimiendo en: {nom}")
                            nombre_impresora = nom
                            break
                except Exception as err_emergencia:
                    print(f"Error en el plan de emergencia: {err_emergencia}")
                
                # Si todo, absolutamente todo falla, dejamos el de por defecto para intentar la conexión igual
                if not nombre_impresora or nombre_impresora == "Generic / Text Only":
                    nombre_impresora = "Generic / Text Only"

        print(f"Conectando a la tiquetera mediante Windows: {nombre_impresora}")
        
        # 1. Abrimos la conexión con la impresora de Windows
        hPrinter = win32print.OpenPrinter(nombre_impresora)
        
        try:
            # 2. Iniciamos el documento en la cola de Windows (Modo RAW para comandos ESC/POS)
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket Baquiano", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            
            # --- COMANDOS ESC/POS NATIVOS ---
            TXT_RESET = b'\x1b\x40'          
            TXT_CENTRO = b'\x1b\x61\x01'     
            TXT_IZQUIERDA = b'\x1b\x61\x00'  
            TXT_DERECHA = b'\x1b\x61\x02'    
            TXT_NEGRITA_ON = b'\x1b\x45\x01' 
            TXT_NEGRITA_OFF = b'\x1b\x45\x00'
            
            # 3. Inicializar e imprimir Encabezado
            win32print.WritePrinter(hPrinter, TXT_RESET)
            win32print.WritePrinter(hPrinter, TXT_CENTRO + TXT_NEGRITA_ON + b"*** BAQUIANO ***\n" + TXT_NEGRITA_OFF)
            win32print.WritePrinter(hPrinter, b"Fiambreria & Almacen\n")
            win32print.WritePrinter(hPrinter, TXT_IZQUIERDA + b"--------------------------------\n")
            
            # 4. Detalle de Productos
            for prod in lista_productos:
                cant_str = f"{prod['cantidad']}x"
                nombre_str = prod['nombre'][:17].ljust(17) 
                precio_str = f"${prod['precio_total']:>9.2f}"
                
                linea = f"{cant_str:<4}{nombre_str}{precio_str}\n"
                # Usamos cp437 o ascii limpio para evitar errores de caracteres
                win32print.WritePrinter(hPrinter, linea.encode('cp437', errors='ignore')) 
                
            win32print.WritePrinter(hPrinter, b"--------------------------------\n")
            
            # 5. TOTAL
            win32print.WritePrinter(hPrinter, TXT_DERECHA + TXT_NEGRITA_ON)
            linea_total = f"TOTAL:   ${total:>10.2f}\n"
            win32print.WritePrinter(hPrinter, linea_total.encode('ascii', errors='ignore'))
            win32print.WritePrinter(hPrinter, TXT_NEGRITA_OFF)
            
            # 6. Pie de ticket con fecha y hora
            fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            linea_fecha = f"\n{fecha_hora}\n\n"
            win32print.WritePrinter(hPrinter, TXT_CENTRO + linea_fecha.encode('ascii'))
            
            # 7. Avance de papel final para poder cortar
            win32print.WritePrinter(hPrinter, b"\n\n\n\n") 
            
            # 8. Cerrar página y documento de Windows
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            
            print("¡Ticket enviado a la tiquetera con éxito!")
            return True
            
        finally:
            # Nos aseguramos de liberar siempre el recurso de la impresora
            win32print.ClosePrinter(hPrinter)
            
    except Exception as e:
        print(f"Error crítico al imprimir en Systel: {e}")
        return False