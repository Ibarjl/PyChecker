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
    except Exception as e:
        return f"[ERROR] No se pudieron obtener los logs del contenedor {container_name}: {e}"


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
    except Exception as e:
        yield f"[ERROR] No se pudo hacer streaming de logs del contenedor {container_name}: {e}"
