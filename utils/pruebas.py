"""
Script de pruebas para verificar el funcionamiento del monitor de logs
"""

import time
import random
import threading
import os
from datetime import datetime
from file_utils import monitorear_log, MonitorLogSimple

def generar_logs_test(archivo_log="test.log", duracion_segundos=60):
    """
    Genera logs de prueba cada pocos segundos para simular una aplicación real
    
    Args:
        archivo_log (str): Nombre del archivo donde escribir los logs
        duracion_segundos (int): Cuánto tiempo generar logs (0 = infinito)
    """
    print(f"🔧 Generando logs en: {archivo_log}")
    if duracion_segundos > 0:
        print(f"⏰ Duración: {duracion_segundos} segundos")
    else:
        print("♾️  Duración: Infinita (Ctrl+C para detener)")
    
    mensajes = [
        "INFO: Aplicación iniciada correctamente",
        "DEBUG: Procesando solicitud de usuario #12345",
        "WARNING: Memoria alta detectada (85% uso)",
        "ERROR: Conexión a base de datos falló - reintentando...",
        "INFO: Usuario 'admin' autenticado exitosamente",
        "ERROR: Timeout en servicio externo (api.ejemplo.com)",
        "INFO: Operación de backup completada",
        "DEBUG: Cache invalidado correctamente",
        "WARNING: Disco con 90% de capacidad",
        "INFO: 15 usuarios conectados simultáneamente",
        "ERROR: Falló validación de datos en endpoint /api/users",
        "INFO: Tarea programada ejecutada exitosamente"
    ]
    
    try:
        # Crear o limpiar el archivo de logs
        with open(archivo_log, 'w', encoding='utf-8') as f:
            f.write(f"=== LOG INICIADO {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        
        tiempo_inicio = time.time()
        contador = 1
        
        while True:
            # Verificar si hemos alcanzado la duración límite
            if duracion_segundos > 0 and (time.time() - tiempo_inicio) >= duracion_segundos:
                break
            
            mensaje = random.choice(mensajes)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            linea_log = f"[{timestamp}] {mensaje} (#{contador:04d})\n"
            
            # Escribir al archivo
            with open(archivo_log, 'a', encoding='utf-8') as f:
                f.write(linea_log)
            
            print(f"✍️  Escribiendo: {linea_log.strip()}")
            contador += 1
            
            # Esperar entre 1 y 4 segundos antes del siguiente log
            time.sleep(random.uniform(1, 4))
            
    except KeyboardInterrupt:
        print(f"\n🛑 Generador de logs detenido (se escribieron {contador-1} líneas)")
    except Exception as e:
        print(f"❌ Error generando logs: {e}")

def prueba_monitor_basica():
    """
    Prueba básica: genera logs por 30 segundos mientras monitoreamos
    """
    archivo_test = "test_basico.log"
    
    print("🧪 === PRUEBA BÁSICA DEL MONITOR ===")
    print("Esta prueba:")
    print("1. Generará logs automáticamente por 30 segundos")
    print("2. El monitor debería mostrar cada nuevo log en tiempo real")
    print("3. Se detendrá automáticamente")
    print("=" * 50)
    
    # Eliminar archivo anterior si existe
    if os.path.exists(archivo_test):
        os.remove(archivo_test)
        print(f"🗑️  Archivo anterior {archivo_test} eliminado")
    
    # Iniciar generador en un hilo separado
    print("🚀 Iniciando generador de logs...")
    generador_thread = threading.Thread(
        target=generar_logs_test, 
        args=(archivo_test, 30),  # 30 segundos
        daemon=True
    )
    generador_thread.start()
    
    # Esperar un poco para que se cree el archivo
    time.sleep(2)
    
    print("👁️  Iniciando monitor...")
    try:
        monitorear_log(archivo_test)
    except KeyboardInterrupt:
        print("\n🛑 Prueba detenida por el usuario")
    
    # Limpiar archivo de prueba
    if os.path.exists(archivo_test):
        os.remove(archivo_test)
        print(f"🧹 Archivo de prueba {archivo_test} eliminado")

def prueba_monitor_interactiva():
    """
    Prueba interactiva: el usuario controla cuándo generar logs
    """
    archivo_test = "test_interactivo.log"
    
    print("🎮 === PRUEBA INTERACTIVA DEL MONITOR ===")
    print("En esta prueba:")
    print("1. El monitor estará vigilando un archivo")
    print("2. TÚ decidirás cuándo escribir logs")
    print("3. Verás aparecer los logs en tiempo real")
    print("=" * 50)
    
    # Crear archivo vacío
    with open(archivo_test, 'w', encoding='utf-8') as f:
        f.write(f"=== LOG INTERACTIVO INICIADO {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    print(f"📝 Archivo creado: {archivo_test}")
    print("🎯 Para agregar logs manualmente, abre otra terminal y ejecuta:")
    print(f"     echo '[INFO] Mi mensaje de prueba' >> {archivo_test}")
    print("👁️  Iniciando monitor (Ctrl+C para detener)...")
    
    try:
        monitorear_log(archivo_test)
    except KeyboardInterrupt:
        print("\n🛑 Monitor detenido")
    
    # Preguntar si eliminar archivo
    respuesta = input(f"\n🗑️  ¿Eliminar archivo de prueba {archivo_test}? (s/N): ")
    if respuesta.lower() == 's':
        os.remove(archivo_test)
        print("🧹 Archivo eliminado")

def prueba_con_archivo_existente():
    """
    Permite probar el monitor con un archivo que ya existe en el sistema
    """
    print("📁 === PRUEBA CON ARCHIVO EXISTENTE ===")
    print("Introduce la ruta de un archivo de logs existente")
    print("(por ejemplo: logs de aplicaciones, sistema, etc.)")
    print("=" * 50)
    
    ruta_archivo = input("📂 Ruta completa del archivo a monitorear: ").strip()
    
    if not ruta_archivo:
        print("❌ No se proporcionó ninguna ruta")
        return
    
    if not os.path.exists(ruta_archivo):
        print(f"❌ El archivo {ruta_archivo} no existe")
        return
    
    if not os.path.isfile(ruta_archivo):
        print(f"❌ {ruta_archivo} no es un archivo válido")
        return
    
    print(f"👁️  Monitoreando: {ruta_archivo}")
    print("💡 Modifica el archivo desde otra aplicación para ver los cambios")
    print("🛑 Presiona Ctrl+C para detener")
    
    try:
        monitorear_log(ruta_archivo)
    except KeyboardInterrupt:
        print("\n🛑 Monitor detenido")

def menu_pruebas():
    """
    Menú principal para elegir qué tipo de prueba realizar
    """
    while True:
        print("\n🧪 === MENÚ DE PRUEBAS PARA MONITOR DE LOGS ===")
        print("1. 🤖 Prueba básica (automática - 30 segundos)")
        print("2. 🎮 Prueba interactiva (manual)")
        print("3. 📁 Probar con archivo existente")
        print("4. 🔧 Solo generar logs de prueba")
        print("5. 🚪 Salir")
        print("=" * 50)
        
        opcion = input("Elige una opción (1-5): ").strip()
        
        if opcion == "1":
            prueba_monitor_basica()
        elif opcion == "2":
            prueba_monitor_interactiva()
        elif opcion == "3":
            prueba_con_archivo_existente()
        elif opcion == "4":
            archivo = input("Nombre del archivo de logs (default: test.log): ").strip()
            if not archivo:
                archivo = "test.log"
            duracion = input("Duración en segundos (0 = infinito): ").strip()
            try:
                duracion = int(duracion) if duracion else 60
            except ValueError:
                duracion = 60
            generar_logs_test(archivo, duracion)
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida, intenta de nuevo")

if __name__ == "__main__":
    menu_pruebas()
