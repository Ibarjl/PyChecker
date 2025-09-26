import docker

def get_docker_logs(container_name: str, tail: int = 100) -> str:
    """
    Lee los últimos logs de un contenedor Docker.

    :param container_name: Nombre o ID del contenedor
    :param tail: Número de líneas de logs a recuperar
    :return: Logs como string
    """
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        logs = container.logs(
            tail=tail,
            stderr=True,
            stdout=True
        ).decode("utf-8", errors="replace")
        return logs
    except docker.errors.NotFound:
            return f"[ERROR] Contenedor '{container_name}' no encontrado. Verifica que el nombre sea correcto."
    except docker.errors.APIError as e:
            return f"[ERROR] Error de API Docker: {e}"
    except ConnectionError:
            return "[ERROR] No se puede conectar al daemon de Docker. ¿Está Docker ejecutándose?"
    except Exception as e:
            return f"[ERROR] Error inesperado obteniendo logs de {container_name}: {e}"

def stream_docker_logs(container_name: str):
    """
    Genera logs en streaming desde un contenedor Docker.

    :param container_name: Nombre o ID del contenedor
    :yield: Líneas de log en tiempo real
    """
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        for log in container.logs(stream=True, follow=True):
            yield log.decode("utf-8", errors="replace")
    except docker.errors.NotFound:
        yield f"[ERROR] Contenedor '{container_name}' no encontrado"
    except docker.errors.APIError as e:
        yield f"[ERROR] Error de API Docker: {e}"
    except ConnectionError:
        yield "[ERROR] No se puede conectar al daemon de Docker"
    except Exception as e:
        yield f"[ERROR] Error inesperado en streaming de {container_name}: {e}"

def restart_docker_container(container_name: str):
    """
    Reinicia un contenedor Docker usando su nombre o ID.
    """
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.restart()
        print(f"Contenedor Docker {container_name} reiniciado correctamente.")
    except Exception as e:
        print(f"Error al reiniciar contenedor Docker {container_name}: {e}")
