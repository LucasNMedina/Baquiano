import serial
import serial.tools.list_ports
import datetime

def encontrar_puerto_tiquetera():
    """
    Busca automáticamente el puerto COM donde está el adaptador USB-Serial
    ignorando los puertos nativos fantasmas de la placa madre.
    """
    puertos = list(serial.tools.list_ports.comports())
    
    # 1. Buscamos estrictamente por palabras clave del chip del cable
    for p in puertos:
        descripcion = p.description.lower()
        if "prolific" in descripcion or "usb-to-serial" in descripcion or "ch340" in descripcion or "ftdi" in descripcion:
            return p.device
            
    # 2. Si no encuentra por nombre, pero hay puertos USB-Serial genéricos que NO sean el COM1 de la placa
    for p in puertos:
        # Filtramos el COM1 y strings comunes de puertos internos de Windows
        if p.device != "COM1" and "com1" not in p.description.lower():
            return p.device
        
    # Si no hay cables USB-Serial reales conectados, no inventamos ningún puerto
    return None

def imprimir_ticket_systel(lista_productos, total, puerto_com=None):
    """
    Envía el ticket condensado directamente a la tiquetera Systel GP-5890XIII.
    Si puerto_com es None, busca el puerto automáticamente.
    """
    try:
        # --- DETECCIÓN AUTOMÁTICA DEL PUERTO ---
        if puerto_com is None:
            puerto_com = encontrar_puerto_tiquetera()
            if puerto_com is None:
                print("Error: No se detectó ningún puerto COM activo.")
                return False
        
        print(f"Conectando a la tiquetera en el puerto: {puerto_com}")
        
        # 1. Abrimos la conexión con el puerto encontrado
        ser = serial.Serial(puerto_com, baudrate=9600, timeout=1)
        
        # --- COMANDOS ESC/POS NATIVOS ---
        TXT_RESET = b'\x1b\x40'          
        TXT_CENTRO = b'\x1b\x61\x01'     
        TXT_IZQUIERDA = b'\x1b\x61\x00'  
        TXT_DERECHA = b'\x1b\x61\x02'    
        TXT_NEGRITA_ON = b'\x1b\x45\x01' 
        TXT_NEGRITA_OFF = b'\x1b\x45\x00'
        
        # 2. Inicializar e imprimir Encabezado
        ser.write(TXT_RESET)
        ser.write(TXT_CENTRO + TXT_NEGRITA_ON + b"*** BAQUIANO ***\n" + TXT_NEGRITA_OFF)
        ser.write(b"Fiambreria & Almacen\n")
        ser.write(TXT_IZQUIERDA + b"--------------------------------\n")
        
        # 3. Detalle de Productos
        for prod in lista_productos:
            cant_str = f"{prod['cantidad']}x"
            nombre_str = prod['nombre'][:17].ljust(17) 
            precio_str = f"${prod['precio_total']:>9.2f}"
            
            linea = f"{cant_str:<4}{nombre_str}{precio_str}\n"
            ser.write(linea.encode('cp437')) 
            
        ser.write(b"--------------------------------\n")
        
        # 4. TOTAL
        ser.write(TXT_DERECHA + TXT_NEGRITA_ON)
        ser.write(f"TOTAL:   ${total:>10.2f}\n".encode('utf-8'))
        ser.write(TXT_NEGRITA_OFF)
        
        # 5. Pie de ticket con fecha y hora
        fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ser.write(TXT_CENTRO + f"\n{fecha_hora}\n\n".encode('utf-8'))
        
        ser.write(b"\n\n\n\n") 
        
        # 6. Cerrar el puerto de comunicación
        ser.close()
        return True
        
    except Exception as e:
        print(f"Error al imprimir en Systel: {e}")
        return False