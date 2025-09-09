from utils.docker_utils import get_docker_logs
from utils.k8s_utils import get_k8s_pod_logs

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

def main():
    while True:
        print("\n📋 Menú HealthMonitor")
        print("1. Leer logs de Docker")
        print("2. Leer logs de Kubernetes")
        print("3. Leer logs de un fichero")
        print("4. Salir")

        choice = input("Elige una opción (1-4): ")

        if choice == "1":
            read_from_docker()
        elif choice == "2":
            read_from_k8s()
        elif choice == "3":
            read_from_file()
        elif choice == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, inténtalo de nuevo.")

if __name__ == "__main__":
    main()
