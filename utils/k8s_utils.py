<<<<<<< HEAD
"""
Utilidades para trabajar con Kubernetes de manera más robusta
"""

# Validación de dependencias de Kubernetes
try:
    from kubernetes import client, config
    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False
    print("⚠️  Kubernetes client no está disponible. Funcionalidad K8s deshabilitada.")
=======
from kubernetes import client, config
>>>>>>> rama_ibar

def get_k8s_pod_logs(pod_name: str, namespace: str = "default", tail: int = 100) -> str:
    """
    Lee los últimos logs de un pod en Kubernetes.
<<<<<<< HEAD
    Incluye validación de dependencias y mejor manejo de errores.
=======
>>>>>>> rama_ibar

    :param pod_name: Nombre del pod
    :param namespace: Namespace del pod
    :param tail: Número de líneas de logs a recuperar
    :return: Logs como string
    """
<<<<<<< HEAD
    if not K8S_AVAILABLE:
        return "[ERROR] Cliente de Kubernetes no está instalado. Ejecuta: pip install kubernetes"
    
    try:
        # Intentar cargar configuración según el contexto
=======
    try:
        # Cargar configuración según contexto
>>>>>>> rama_ibar
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
<<<<<<< HEAD
    except config.ConfigException:
        return "[ERROR] No se pudo cargar configuración de Kubernetes. ¿Tienes kubectl configurado?"
    except client.ApiException as e:
        if e.status == 404:
            return f"[ERROR] Pod '{pod_name}' no encontrado en namespace '{namespace}'"
        else:
            return f"[ERROR] Error de API Kubernetes: {e}"
    except Exception as e:
        return f"[ERROR] Error inesperado obteniendo logs de pod {pod_name}: {e}"
=======
    except Exception as e:
        return f"[ERROR] No se pudieron obtener los logs del pod {pod_name}: {e}"

>>>>>>> rama_ibar

def stream_k8s_pod_logs(pod_name: str, namespace: str = "default"):
    """
    Genera logs en streaming desde un pod en Kubernetes.
<<<<<<< HEAD
    Incluye validación mejorada.
=======
>>>>>>> rama_ibar

    :param pod_name: Nombre del pod
    :param namespace: Namespace del pod
    :yield: Líneas de log en tiempo real
    """
<<<<<<< HEAD
    if not K8S_AVAILABLE:
        yield "[ERROR] Cliente de Kubernetes no está disponible"
        return
    
=======
>>>>>>> rama_ibar
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
<<<<<<< HEAD
    except config.ConfigException:
        yield "[ERROR] No se pudo cargar configuración de Kubernetes"
    except client.ApiException as e:
        if e.status == 404:
            yield f"[ERROR] Pod '{pod_name}' no encontrado en namespace '{namespace}'"
        else:
            yield f"[ERROR] Error de API Kubernetes: {e}"
    except Exception as e:
        yield f"[ERROR] Error inesperado en streaming de pod {pod_name}: {e}"

def verificar_k8s_disponible() -> bool:
    """
    Verifica si Kubernetes está disponible y configurado
    
    :return: True si K8s está disponible, False en caso contrario
    """
    if not K8S_AVAILABLE:
        return False
    
    try:
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        
        v1 = client.CoreV1Api()
        v1.list_namespace(limit=1)  # Prueba básica
        return True
    except:
        return False
=======
    except Exception as e:
        yield f"[ERROR] No se pudo hacer streaming de logs del pod {pod_name}: {e}"
>>>>>>> rama_ibar
