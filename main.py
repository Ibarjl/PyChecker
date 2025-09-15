<<<<<<< HEAD
import os
import subprocess
import sys
import json
from datetime import datetime
from utils.docker_utils import get_docker_logs
from utils.k8s_utils import get_k8s_pod_logs
from utils.file_utils import monitorear_log
from utils.config_loader import listar_repositorios_disponibles, generar_configuracion_automatica

# Definir rutas de manera más robusta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "monitor_config.json")
ESTADO_PATH = os.path.join(BASE_DIR, "frontend", "estado_actual.json")

def actualizar_estado_sistema(servicios_estado):
    """
    Actualiza el estado del sistema para que el frontend pueda leerlo
    Esta función crea el puente de comunicación entre backend y frontend
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ESTADO_PATH), exist_ok=True)
        
        # Escribir estado actual
        with open(ESTADO_PATH, 'w', encoding='utf-8') as f:
            json.dump(servicios_estado, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error actualizando estado del sistema: {e}")

def read_from_docker():
    container_name = input("Nombre/ID del contenedor Docker: ")
=======

import subprocess
import sys
import os
from utils.docker_utils import get_docker_logs
from utils.k8s_utils import get_k8s_pod_logs
def launch_config_editor():
    editor_path = os.path.join(os.path.dirname(__file__), 'utils', 'config_editor.py')
    subprocess.Popen([sys.executable, editor_path])


def read_from_docker():
    container_name = input("Nombre o ID del contenedor Docker: ")
>>>>>>> rama_ibar
    logs = get_docker_logs(container_name, tail=50)
    print("\n===== LOGS DOCKER =====")
    print(logs)

def read_from_k8s():
    pod_name = input("Nombre del pod en Kubernetes: ")
<<<<<<< HEAD
    namespace = input("Namespace (default si vacío): ") or "default"
=======
    namespace = input("Namespace (si no ponés nada, es 'default'): ") or "default"
>>>>>>> rama_ibar
    logs = get_k8s_pod_logs(pod_name, namespace=namespace, tail=50)
    print("\n===== LOGS KUBERNETES =====")
    print(logs)

def read_from_file():
<<<<<<< HEAD
    file_path = input("Ruta del fichero de logs: ")
    mostrar_logs_archivo(file_path)

def monitor_file_realtime():
    file_path = input("Ruta del fichero de logs a monitorear: ")
    monitorear_archivo(file_path)

def monitor_external_app():
    rutas_comunes = [
        "../otro-repositorio/logs/app.log",
        "../otro-repositorio/output.log", 
        "./logs/external.log",
        "C:/logs/sistema.log"
    ]
    print("Rutas disponibles:")
    for i, ruta in enumerate(rutas_comunes, 1):
        print(f"{i}. {ruta}")
    print(f"{len(rutas_comunes) + 1}. Escribir ruta personalizada")
    opcion = input(f"Elige una opción (1-{len(rutas_comunes) + 1}): ")
    if opcion.isdigit() and 1 <= int(opcion) <= len(rutas_comunes):
        ruta_archivo = rutas_comunes[int(opcion) - 1]
    else:
        ruta_archivo = input("Escribe la ruta completa: ")
    monitorear_archivo(ruta_archivo)

def monitor_configured_repos():
    repositorios = listar_repositorios_disponibles()
    if not repositorios:
        print("Error: No hay repositorios configurados")
        print("Edita config/monitor_config.json para agregar repositorios")
        return
    print("Repositorios disponibles:")
    for i, repo in enumerate(repositorios, 1):
        print(f"{i}. {repo['nombre']}")
        print(f"   Ruta: {repo['ruta']}")
        print(f"   {repo['descripcion']}")
        print()
    print(f"{len(repositorios) + 1}. Ruta personalizada")
    opcion = input(f"Elige una opción (1-{len(repositorios) + 1}): ")
    if opcion.isdigit() and 1 <= int(opcion) <= len(repositorios):
        repo_seleccionado = repositorios[int(opcion) - 1]
        ruta_archivo = repo_seleccionado['ruta']
        print(f"Monitoreando: {repo_seleccionado['nombre']}")
        print(f"Archivo: {ruta_archivo}")
    else:
        ruta_archivo = input("Escribe la ruta completa: ")
    monitorear_archivo(ruta_archivo)

def mostrar_logs_archivo(file_path):
    """
    Muestra las últimas 50 líneas de un archivo de log
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logs = "".join(f.readlines()[-50:])
        print("\n===== LOGS FICHERO =====")
        print(logs)
    except Exception as e:
        print(f"[ERROR] No se pudieron leer los logs del fichero {file_path}: {e}")

def monitorear_archivo(file_path):
    """
    Monitorea un archivo en tiempo real
    """
    if not file_path.strip():
        print("Error: No se proporcionó ninguna ruta")
        return
    print(f"Monitoreando: {file_path}")
    print("Presiona Ctrl+C para volver al menú")
    try:
        monitorear_log(file_path)
    except KeyboardInterrupt:
        print("\nVolviendo al menú principal...")
    except Exception as e:
        print(f"Error monitoreando archivo: {e}")

def execute_and_monitor():
    """
    Ejecuta otro programa Python y captura su output en tiempo real
    """
    ruta_programa = input("Ruta completa al script Python (.py): ")
    
    if not os.path.exists(ruta_programa):
        print(f"Error: No se encontró el archivo: {ruta_programa}")
        return
    
    print(f"Ejecutando: {ruta_programa}")
    print("Presiona Ctrl+C para detener")
    
    try:
        proceso = subprocess.Popen(
            [sys.executable, ruta_programa],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        for linea in iter(proceso.stdout.readline, ''):
            if linea:
                print(linea.strip())
        
        proceso.wait()
        print(f"Programa terminado con código: {proceso.returncode}")
        
    except KeyboardInterrupt:
        print("\nDeteniendo programa externo...")
        proceso.terminate()
        proceso.wait()
    except Exception as e:
        print(f"Error ejecutando programa: {e}")

def generate_auto_config():
    """
    Genera configuración automática detectando archivos .log
    """
    print("Generando configuración automática...")
    print("Buscando archivos .log en directorios comunes...")
    
    try:
        config = generar_configuracion_automatica()
        
        if config and config.get("repositorios"):
            print("\nRepositorios detectados:")
            for repo_id, repo_config in config["repositorios"].items():
                print(f"- {repo_config['nombre']}")
                print(f"  Ruta: {repo_config['ruta_logs']}")
        else:
            print("No se encontraron archivos .log para configurar")
            
    except Exception as e:
        print(f"Error generando configuración: {e}")

def monitorear_con_plugin_especializado():
    """
    Monitoreo con análisis especializado por tipo de servicio
    NOTA: Esta es la versión consolidada que incluye toda la funcionalidad
    """
    print("\n=== MONITOREO CON PLUGINS ESPECIALIZADOS ===")
    print("1. Avionics - Sistemas de navegación y vuelo")
    print("2. Asset API - APIs REST y servicios web") 
    print("3. Runtime - Memoria, CPU y rendimiento")
    
    opcion = input("Seleccione plugin (1-3): ")
    archivo = input("Ruta del archivo de logs: ")
    
    try:
        # CORRECCIÓN: Usar nombres consistentes en minúsculas para todos los imports
        if opcion == "1":
            from plugins.avionics import AvionicsMonitor
            monitor = AvionicsMonitor()
            plugin_name = "Avionics"
        elif opcion == "2":
            from plugins.assetapi import AssetAPIMonitor  # Corregido: siempre minúsculas
            monitor = AssetAPIMonitor()
            plugin_name = "Asset API"
        elif opcion == "3":
            from plugins.runtime import RuntimeMonitor
            monitor = RuntimeMonitor()
            plugin_name = "Runtime"
        else:
            print("Error: Opción no válida")
            return
        
        print(f"\nAnalizando con plugin {plugin_name}")
        print(f"Archivo: {archivo}")
        
        if not os.path.exists(archivo):
            print(f"Error: Archivo no encontrado - {archivo}")
            return
        
        # Leer y analizar logs
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()[-50:]
        
        errores_criticos = 0
        warnings = 0
        errores = 0
        
        print(f"\nAnalizando {len(lineas)} líneas de log...")
        print("-" * 60)
        
        for linea in lineas:
            linea = linea.strip()
            if linea:
                analisis = monitor.analizar_patron_log(linea)
                
                if analisis["nivel"] == "CRITICAL":
                    errores_criticos += 1
                    print(f"CRITICO: {linea[:70]}...")
                elif analisis["nivel"] == "ERROR":
                    errores += 1
                    print(f"ERROR: {linea[:70]}...")
                elif analisis["nivel"] == "WARNING":
                    warnings += 1
                    print(f"WARNING: {linea[:70]}...")
        
        print("-" * 60)
        
        # Evaluación final
        estado_salud = monitor.evaluar_salud_servicio(lineas)
        
        print(f"\n=== RESUMEN DEL ANÁLISIS ===")
        print(f"Estado del servicio: {estado_salud}")
        print(f"Errores críticos: {errores_criticos}")
        print(f"Errores: {errores}")
        print(f"Warnings: {warnings}")
        print(f"Líneas analizadas: {len(lineas)}")
        
        # Actualizar estado del sistema para el frontend
        estado_para_frontend = [
            {
                "name": plugin_name,
                "status": estado_salud,
                "last_error": f"{errores_criticos} críticos, {errores} errores" if errores_criticos + errores > 0 else None,
                "restarts_last_hour": 0,
                "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        actualizar_estado_sistema(estado_para_frontend)
        
        # Acción de emergencia si es necesario
        if estado_salud in ["CRITICAL", "ERROR"]:
            print(f"\nSe detectaron problemas graves en el sistema.")
            respuesta = input("¿Ejecutar acción de emergencia? (s/N): ")
            
            if respuesta.lower() == 's':
                print(f"\nEjecutando acción de emergencia para {plugin_name}...")
                exito = monitor.ejecutar_accion_emergencia()
                print("Acción completada" if exito else "Error en acción de emergencia")
            else:
                print("Acción de emergencia cancelada")
        
        # Opción de monitoreo continuo
        if estado_salud == "OK":
            respuesta = input(f"\n¿Iniciar monitoreo continuo? (s/N): ")
            if respuesta.lower() == 's':
                print("Iniciando monitoreo continuo... (Ctrl+C para detener)")
                monitorear_log(archivo)
        
    except ImportError as e:
        print(f"Error importando plugin: {e}")
        print("Asegúrate de que todos los archivos de plugins estén en su lugar.")
    except Exception as e:
        print(f"Error durante análisis: {e}")

def main():
    while True:
        print("\nMenú HealthMonitor")
        print("1. Leer logs de Docker")
        print("2. Leer logs de Kubernetes") 
        print("3. Leer logs de un fichero")
        print("4. Monitorear archivo en tiempo real")
        print("5. Monitorear repositorios configurados")
        print("6. Monitorear aplicación externa")
        print("7. Ejecutar y monitorear programa")
        print("8. Generar configuración automática")
        print("9. Monitoreo con plugin especializado")
        print("10. Salir")

        choice = input("Elige una opción (1-10): ")
=======
    file_path = input("Ruta del archivo de logs: ")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logs = "".join(f.readlines()[-50:])
        print("\n===== LOGS DEL ARCHIVO =====")
        print(logs)
    except Exception as e:
        print(f"[ERROR] No pude leer los logs del archivo {file_path}: {e}")

def main():
    # Lanzar el editor de configuración al inicio
    launch_config_editor()
    while True:
        print("\n📋 Menú HealthMonitor")
        print("1. Mirá los logs de Docker")
        print("2. Leer logs de Kubernetes")
        print("3. Leer logs de un fichero")
        print("4. Salir")

        choice = input("Elige una opción (1-4): ")
>>>>>>> rama_ibar

        if choice == "1":
            read_from_docker()
        elif choice == "2":
            read_from_k8s()
        elif choice == "3":
            read_from_file()
        elif choice == "4":
<<<<<<< HEAD
            monitor_file_realtime()
        elif choice == "5":
            monitor_configured_repos()
        elif choice == "6":
            monitor_external_app()
        elif choice == "7":
            execute_and_monitor()
        elif choice == "8":
            generate_auto_config()
        elif choice == "9":
            monitorear_con_plugin_especializado()
        elif choice == "10":
            print("Cerrando Health Monitor...")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()
=======
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, inténtalo de nuevo.")

if __name__ == "__main__":
    main()
>>>>>>> rama_ibar
