<<<<<<< HEAD
"""
Utilidades para trabajar con Docker de manera más robusta
"""

# Primero intentamos importar Docker y manejamos si no está disponible
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    print("⚠️  Docker no está disponible. Funcionalidad Docker deshabilitada.")
=======
import docker
>>>>>>> rama_ibar

def get_docker_logs(container_name: str, tail: int = 100) -> str:
    """
    Lee los últimos logs de un contenedor Docker.
<<<<<<< HEAD
    Ahora incluye validación de dependencias y manejo específico de errores.
=======
>>>>>>> rama_ibar

    :param container_name: Nombre o ID del contenedor
    :param tail: Número de líneas de logs a recuperar
    :return: Logs como string
    """
<<<<<<< HEAD
    if not DOCKER_AVAILABLE:
        return "[ERROR] Docker no está instalado en este sistema. Instala Docker para usar esta funcionalidad."
    
=======
>>>>>>> rama_ibar
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        logs = container.logs(
            tail=tail,
            stderr=True,
            stdout=True
        ).decode("utf-8", errors="replace")
        return logs
<<<<<<< HEAD
    except docker.errors.NotFound:
        return f"[ERROR] Contenedor '{container_name}' no encontrado. Verifica que el nombre sea correcto."
    except docker.errors.APIError as e:
        return f"[ERROR] Error de API Docker: {e}"
    except ConnectionError:
        return "[ERROR] No se puede conectar al daemon de Docker. ¿Está Docker ejecutándose?"
    except Exception as e:
        return f"[ERROR] Error inesperado obteniendo logs de {container_name}: {e}"
=======
    except Exception as e:
        return f"[ERROR] No se pudieron obtener los logs del contenedor {container_name}: {e}"

>>>>>>> rama_ibar

def stream_docker_logs(container_name: str):
    """
    Genera logs en streaming desde un contenedor Docker.
<<<<<<< HEAD
    Incluye validación mejorada de errores.
=======
>>>>>>> rama_ibar

    :param container_name: Nombre o ID del contenedor
    :yield: Líneas de log en tiempo real
    """
<<<<<<< HEAD
    if not DOCKER_AVAILABLE:
        yield "[ERROR] Docker no está disponible en este sistema"
        return
    
=======
>>>>>>> rama_ibar
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        for log in container.logs(stream=True, follow=True):
            yield log.decode("utf-8", errors="replace")
<<<<<<< HEAD
    except docker.errors.NotFound:
        yield f"[ERROR] Contenedor '{container_name}' no encontrado"
    except docker.errors.APIError as e:
        yield f"[ERROR] Error de API Docker: {e}"
    except ConnectionError:
        yield "[ERROR] No se puede conectar al daemon de Docker"
    except Exception as e:
        yield f"[ERROR] Error inesperado en streaming de {container_name}: {e}"

def verificar_docker_disponible() -> bool:
    """
    Función utilitaria para verificar si Docker está disponible y funcionando
    
    :return: True si Docker está disponible, False en caso contrario
    """
    if not DOCKER_AVAILABLE:
        return False
    
    try:
        client = docker.from_env()
        client.ping()  # Prueba básica de conectividad
        return True
    except:
        return False
=======
    except Exception as e:
        yield f"[ERROR] No se pudo hacer streaming de logs del contenedor {container_name}: {e}"
>>>>>>> rama_ibar
