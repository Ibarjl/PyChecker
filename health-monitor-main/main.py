import os
import importlib
import yaml
import time
import json
import argparse
from utils.docker_utils import get_docker_logs, stream_docker_logs, restart_docker_container
from utils.k8s_utils import get_k8s_pod_logs, stream_k8s_pod_logs, restart_k8s_pod

STATE_FILE = "state/restart_state.json"
HEALTH_FILE = "state/health_status.json"

def get_class_name(plugin_name: str) -> str:
    mapping = {
        "asset_api": "AssetAPIMonitor",
        "runtime": "RuntimeMonitor",
        "avionics": "AvionicsMonitor"
    }
    return mapping.get(plugin_name, ''.join(p.capitalize() for p in plugin_name.split('_')) + "Monitor")

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def save_health(health):
    os.makedirs(os.path.dirname(HEALTH_FILE), exist_ok=True)
    with open(HEALTH_FILE, "w") as f:
        json.dump(health, f, indent=2)

def restart_service(service):
    source = service.get("source")
    if source == "docker":
        container_id = service.get("container_id")
        if container_id:
            restart_docker_container(container_id)
    elif source == "kubernetes":
        pod_name = service.get("pod_name")
        namespace = service.get("namespace", "default")
        if pod_name:
            restart_k8s_pod(pod_name, namespace)

def get_logs(service, tail=100):
    if service["source"] == "docker":
        container_id = service.get("container_id")
        if container_id:
            return get_docker_logs(container_id, tail=tail)
    elif service["source"] == "kubernetes":
        pod_name = service.get("pod_name")
        namespace = service.get("namespace", "default")
        if pod_name:
            return get_k8s_pod_logs(pod_name, namespace, tail=tail)
    elif service["source"] == "file":
        file_path = service.get("file_path")
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return "".join(f.readlines()[-tail:])
    return ""

def instantiate_plugin(plugin_name: str):
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        class_name = get_class_name(plugin_name)
        cls = getattr(module, class_name)
        return cls()
    except Exception as e:
        print(f"[ERROR] No se pudo instanciar plugin {plugin_name}: {e}")
        return None

def run_healthcheck():
    """Healthcheck normal: solo ficheros"""
    config = load_config()
    health_status = {}

    for service in config.get("services", []):
        if service["source"] != "file":
            continue  # Saltar docker/k8s

        name = service["name"]
        plugin_name = service["plugin"]
        print(f"\nRevisando {name}")

        logs = get_logs(service, tail=100)
        monitor = instantiate_plugin(plugin_name)
        if not monitor:
            continue

        healthy = monitor.check_logs(logs)
        error_message = None

        if healthy:
            print(f"{name} está sano.")
        else:
            print(f"{name} tiene errores críticos.")
            error_message = "Error detectado en logs"

        health_status[name] = {
            "status": "healthy" if healthy else "error",
            "last_checked": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": error_message,
            "restarted": False,
            "logs": "\n".join(logs.splitlines()[-20:])
        }

    save_health(health_status)

def run_healthcheck_streaming(duration_seconds=120):
    """Healthcheck streaming: solo Docker/Kubernetes"""
    config = load_config()
    state = load_state()
    health_status = {}

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        for service in config.get("services", []):
            if service["source"] not in ["docker", "kubernetes"]:
                continue  # Saltar ficheros

            name = service["name"]
            plugin_name = service["plugin"]
            monitor = instantiate_plugin(plugin_name)
            if not monitor:
                continue

            logs = ""
            try:
                if service["source"] == "docker":
                    container_id = service.get("container_id")
                    if container_id:
                        for line in stream_docker_logs(container_id):
                            logs += line
                            if time.time() - start_time >= duration_seconds:
                                break
                elif service["source"] == "kubernetes":
                    pod_name = service.get("pod_name")
                    if pod_name:
                        for line in stream_k8s_pod_logs(pod_name, service.get("namespace", "default")):
                            logs += line
                            if time.time() - start_time >= duration_seconds:
                                break
            except Exception as e:
                print(f"[WARNING] Error obteniendo logs de {name}: {e}")
                continue

            healthy = monitor.check_logs(logs)
            restarted = False
            error_message = None

            if not healthy:
                print(f"{name} tiene errores críticos. Se reiniciará el servicio.")
                error_message = "Error detectado en logs"
                now = time.time()
                max_restarts = service.get("max_restarts", 3)
                window = service.get("time_window_minutes", 60) * 60
                history = state.get(name, [])
                history = [t for t in history if now - t < window]

                if len(history) < max_restarts:
                    print(f"Reiniciando {name}...")
                    restart_service(service)
                    history.append(now)
                    state[name] = history
                    restarted = True
                else:
                    print(f"Se alcanzó el límite de reinicios para {name} en {window/60} minutos.")

            health_status[name] = {
                "status": "healthy" if healthy else "error",
                "last_checked": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": error_message,
                "restarted": restarted,
                "logs": "\n".join(logs.splitlines()[-20:])
            }

        save_state(state)
        save_health(health_status)

    save_health(health_status)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Monitor")
    parser.add_argument("--mode", choices=["file", "streaming"], required=True,
                        help="Modo de ejecución: file (solo ficheros) o streaming (docker/k8s)")
    parser.add_argument("--duration", type=int, default=120,
                        help="Duración del streaming en segundos (solo para modo streaming)")
    args = parser.parse_args()

    if args.mode == "file":
        run_healthcheck()
    elif args.mode == "streaming":
        run_healthcheck_streaming(duration_seconds=args.duration)
