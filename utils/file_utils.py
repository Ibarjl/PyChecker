"""
Clase que se encargará de leers archivo logs
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonitorLogSimple(FileSystemEventHandler):
    def __init__(self, ruta_completa_archivo):
        # Guardamos la ruta del archivo que queremos monitorear
        self.archivo_objetivo = ruta_completa_archivo
        
        # Esta variable mantiene nuestra posición actual en el archivo
        # Piénsalo como un marcapáginas en un libro
        self.posicion_actual = 0
        
        # Si el archivo ya existe cuando empezamos, nos posicionamos al final
        # Esto significa que solo veremos logs NUEVOS, no los históricos
        if os.path.exists(self.archivo_objetivo):
            with open(self.archivo_objetivo, 'r', encoding='utf-8') as archivo:
                archivo.seek(0, 2)  # El "2" significa "ir al final del archivo"
                self.posicion_actual = archivo.tell()  # tell() nos dice dónde estamos
                print("Archivo encontrado. Esperando nuevos logs...")
        else:
            print(f"Archivo {self.archivo_objetivo} no existe. Esperando...")
    
    def on_modified(self, event):
        """
        Esta función se ejecuta automáticamente cada vez que watchdog detecta
        que algo cambió en el directorio. Es como un "callback" o "gancho"
        """
        # Solo nos importa si el archivo que cambió es exactamente el que queremos
        # y si no es un directorio (sino un archivo real)
        if event.src_path == self.archivo_objetivo and not event.is_directory:
            self.leer_contenido_nuevo()
    
    def leer_contenido_nuevo(self):
        """
        Esta función lee solo las líneas que se agregaron desde la última vez
        que revisamos el archivo
        """
        try:
            with open(self.archivo_objetivo, 'r', encoding='utf-8') as archivo:
                # Vamos a nuestra posición guardada (nuestro marcapáginas)
                archivo.seek(self.posicion_actual)
                
                # Leemos todas las líneas desde esa posición hasta el final
                lineas_nuevas = archivo.readlines()
                
                # Procesamos cada línea nueva
                for linea in lineas_nuevas:
                    linea_limpia = linea.strip()  # Quitamos espacios y saltos de línea
                    if linea_limpia:  # Solo procesamos líneas que no están vacías
                        self.mostrar_nueva_linea(linea_limpia)
                
                # Actualizamos nuestro marcapáginas para la próxima vez
                self.posicion_actual = archivo.tell()
                
        except FileNotFoundError:
            # El archivo fue eliminado mientras lo estábamos leyendo
            print("El archivo desapareció. Esperando a que reaparezca...")
        except PermissionError:
            # No tenemos permisos para leer el archivo
            print("Sin permisos para leer el archivo")
    
    def mostrar_nueva_linea(self, contenido):
        """
        Aquí decides qué hacer con cada línea nueva del log.
        Por ahora solo la mostramos, pero podrías:
        - Filtrar solo errores
        - Guardarla en una base de datos  
        - Enviar una alerta por email
        - etc.
        """
        timestamp = time.strftime("%H:%M:%S")  # Hora actual
        print(f"[{timestamp}] {contenido}")

def monitorear_log(ruta_archivo):
    """
    Función principal que configura todo el sistema de monitoreo
    """
    # Necesitamos separar el directorio del nombre del archivo
    # porque watchdog monitorea directorios, no archivos individuales
    directorio = os.path.dirname(ruta_archivo)
    
    # Si no especificamos directorio, asumimos el directorio actual
    if not directorio:
        directorio = "."
    
    print(f"Monitoreando: {ruta_archivo}")
    print("Presiona Ctrl+C para detener")
    
    # Creamos nuestro monitor personalizado
    monitor = MonitorLogSimple(ruta_archivo)
    
    # Creamos el observador que va a estar pendiente de cambios
    observador = Observer()
    
    # Le decimos al observador que vigile el directorio y use nuestro monitor
    observador.schedule(monitor, directorio, recursive=False)
    
    # Iniciamos la vigilancia
    observador.start()
    
    try:
        # Mantenemos el programa corriendo hasta que el usuario lo detenga
        while True:
            time.sleep(1)  # Pausa pequeña para no consumir CPU innecesariamente
            
    except KeyboardInterrupt:
        print("\nDeteniendo monitor...")
        observador.stop()
        
    # Esperamos a que el observador termine limpiamente
    observador.join()
    print("Monitor detenido correctamente")

# Para usar el monitor, simplemente llama:
# monitorear_log("ruta/completa/a/tu/archivo.log")