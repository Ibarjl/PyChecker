from kubernetes import client, config

def get_k8s_pod_logs(pod_name: str, namespace: str = "default", tail: int = 100) -> str:
    """
    Lee los últimos logs de un pod en Kubernetes.

    :param pod_name: Nombre del pod
    :param namespace: Namespace del pod
    :param tail: Número de líneas de logs a recuperar
    :return: Logs como string
    """
    try:
        # Cargar configuración según contexto
        try:
            config.load_incluster_config()  # Dentro del cluster
        except:
            config.load_kube_config()  # Localmente con kubectl configurado

        v1 = client.CoreV1Api()
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail,
            _preload_content=True
        )
        return logs
    except config.ConfigException:
            return "[ERROR] No se pudo cargar configuración de Kubernetes. ¿Tienes kubectl configurado?"
    except client.ApiException as e:
            if e.status == 404:
                return f"[ERROR] Pod '{pod_name}' no encontrado en namespace '{namespace}'"
            else:
                return f"[ERROR] Error de API Kubernetes: {e}"
    except Exception as e:
            return f"[ERROR] Error inesperado obteniendo logs de pod {pod_name}: {e}"
    except Exception as e:
            return f"[ERROR] No se pudieron obtener los logs del pod {pod_name}: {e}"


def stream_k8s_pod_logs(pod_name: str, namespace: str = "default"):
    """
    Genera logs en streaming desde un pod en Kubernetes.

    :param pod_name: Nombre del pod
    :param namespace: Namespace del pod
    :yield: Líneas de log en tiempo real
    """
    try:
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()

        v1 = client.CoreV1Api()
        resp = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            follow=True,
            _preload_content=False
        )
        for line in resp.stream():
            yield line.decode("utf-8", errors="replace")
    except config.ConfigException:
        yield "[ERROR] No se pudo cargar configuración de Kubernetes"
    except client.ApiException as e:
        if e.status == 404:
            yield f"[ERROR] Pod '{pod_name}' no encontrado en namespace '{namespace}'"
        else:
            yield f"[ERROR] Error de API Kubernetes: {e}"
    except Exception as e:
        yield f"[ERROR] Error inesperado en streaming de pod {pod_name}: {e}"

def restart_k8s_pod(pod_name: str, namespace: str = "default"):
    """
    Reinicia un pod de Kubernetes eliminándolo; el controlador lo recreará.
    """
    try:
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()

        v1 = client.CoreV1Api()
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"Pod Kubernetes {pod_name} eliminado. El controlador lo recreará automáticamente.")
    except Exception as e:
        print(f"Error al reiniciar pod {pod_name}: {e}")
