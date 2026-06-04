import serial
import datetime

def imprimir_ticket_systel(lista_productos, total, puerto_com="COM3"):
    """
    Envía el ticket condensado directamente a la tiquetera Systel GP-5890XIII.
    Solo incluye los productos, el total de la compra y la fecha/hora.
    """
    try:
        # 1. Abrimos la conexión con el puerto Serial (9600 baudios es el estándar de Systel)
        ser = serial.Serial(puerto_com, baudrate=9600, timeout=1)
        
        # --- COMANDOS ESC/POS NATIVOS ---
        TXT_RESET = b'\x1b\x40'          # Limpia el búfer y resetea la impresora
        TXT_CENTRO = b'\x1b\x61\x01'     # Alinear al centro
        TXT_IZQUIERDA = b'\x1b\x61\x00'  # Alinear a la izquierda
        TXT_DERECHA = b'\x1b\x61\x02'    # Alinear a la derecha
        TXT_NEGRITA_ON = b'\x1b\x45\x01' # Activar negrita
        TXT_NEGRITA_OFF = b'\x1b\x45\x00'# Desactivar negrita
        
        # 2. Inicializar e imprimir Encabezado
        ser.write(TXT_RESET)
        ser.write(TXT_CENTRO + TXT_NEGRITA_ON + b"*** BAQUIANO ***\n" + TXT_NEGRITA_OFF)
        ser.write(b"Fiambreria & Almacen\n")
        ser.write(TXT_IZQUIERDA + b"--------------------------------\n") # 32 guiones para papel de 58mm
        
        # 3. Detalle de Productos
        # Estructura de 32 caracteres: Cant (4) + Detalle (17) + Precio (11)
        for prod in lista_productos:
            cant_str = f"{prod['cantidad']}x"
            # Limitamos el nombre a 17 letras para que no se pase al renglón de abajo y desalinee
            nombre_str = prod['nombre'][:17].ljust(17) 
            precio_str = f"${prod['precio_total']:>9.2f}"
            
            linea = f"{cant_str:<4}{nombre_str}{precio_str}\n"
            # Usamos cp437 para que imprima bien la 'ñ' y los acentos en la tiquetera
            ser.write(linea.encode('cp437')) 
            
        ser.write(b"--------------------------------\n")
        
        # 4. TOTAL (Destacado en negrita y alineado a la derecha)
        ser.write(TXT_DERECHA + TXT_NEGRITA_ON)
        ser.write(f"TOTAL:   ${total:>10.2f}\n".encode('utf-8'))
        ser.write(TXT_NEGRITA_OFF)
        
        # 5. Pie de ticket con fecha y hora
        fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ser.write(TXT_CENTRO + f"\n{fecha_hora}\n\n".encode('utf-8'))
        
        # Avanzar el papel para que pase la línea de corte física de la máquina
        ser.write(b"\n\n\n\n") 
        
        # 6. Cerrar el puerto de comunicación
        ser.close()
        return True
        
    except Exception as e:
        print(f"Error al imprimir en Systel: {e}")
        return False