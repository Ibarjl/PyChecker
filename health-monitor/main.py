import os
import subprocess
import sys
from utils.docker_utils import get_docker_logs
from utils.k8s_utils import get_k8s_pod_logs
from utils.file_utils import monitorear_log
from utils.config_loader import listar_repositorios_disponibles, generar_configuracion_automatica

def read_from_docker():
    container_name = input("Nombre/ID del contenedor Docker: ")
    logs = get_docker_logs(container_name, tail=50)
    print("\n===== LOGS DOCKER =====")
    print(logs)

def read_from_k8s():
    pod_name = input("Nombre del pod en Kubernetes: ")
    namespace = input("Namespace (default si vacío): ") or "default"
    logs = get_k8s_pod_logs(pod_name, namespace=namespace, tail=50)
    print("\n===== LOGS KUBERNETES =====")
    print(logs)

def read_from_file():
    file_path = input("Ruta del fichero de logs: ")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logs = "".join(f.readlines()[-50:])
        print("\n===== LOGS FICHERO =====")
        print(logs)
    except Exception as e:
        print(f"[ERROR] No se pudieron leer los logs del fichero {file_path}: {e}")

def monitor_file_realtime():
    """
    Monitorea un archivo específico en tiempo real
    """
    file_path = input("Ruta del fichero de logs a monitorear: ")
    
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

def monitor_external_app():
    """
    Monitorea logs de una aplicación externa usando rutas predefinidas
    """
    # Configurar rutas comunes donde otras apps guardan logs
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
    
    try:
        if opcion.isdigit() and 1 <= int(opcion) <= len(rutas_comunes):
            ruta_archivo = rutas_comunes[int(opcion) - 1]
        else:
            ruta_archivo = input("Escribe la ruta completa: ")
        
        print(f"Monitoreando: {ruta_archivo}")
        monitorear_log(ruta_archivo)
        
    except KeyboardInterrupt:
        print("\nVolviendo al menú principal...")

def monitor_configured_repos():
    """
    Monitorea repositorios configurados en el archivo de configuración
    """
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
    
    try:
        if opcion.isdigit() and 1 <= int(opcion) <= len(repositorios):
            repo_seleccionado = repositorios[int(opcion) - 1]
            ruta_archivo = repo_seleccionado['ruta']
            print(f"Monitoreando: {repo_seleccionado['nombre']}")
            print(f"Archivo: {ruta_archivo}")
        else:
            ruta_archivo = input("Escribe la ruta completa: ")
        
        monitorear_log(ruta_archivo)
        
    except KeyboardInterrupt:
        print("\nVolviendo al menú principal...")

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
        # Ejecutar el programa y capturar su output
        proceso = subprocess.Popen(
            [sys.executable, ruta_programa],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Leer output línea por línea en tiempo real
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
        print("9. Salir")

        choice = input("Elige una opción (1-9): ")

        if choice == "1":
            read_from_docker()
        elif choice == "2":
            read_from_k8s()
        elif choice == "3":
            read_from_file()
        elif choice == "4":
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
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, inténtalo de nuevo.")

if __name__ == "__main__":
    main()