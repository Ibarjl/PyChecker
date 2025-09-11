import os
import sys
import logging
import time
import json


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

consola_logger = logging.StreamHandler(sys.stdout)
logger.addHandler(consola_logger)

def cargar_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def obtener_ruta_log(config, repo_name):
    return config["repositorios"][repo_name]["ruta_logs"]


def leer_logs(ruta_logs):
    if not os.path.exists(ruta_logs):
        logger.error(f"No es posible encontrar {ruta_logs}")
        return None

    try:
        with open(ruta_logs, "r", encoding="utf-8") as fpath:
            return fpath.read()
    except Exception as e:
        logger.exception(f"Excepción encontrada: {e}")
        return None
    


def monitorear_servicio(ruta_log, timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        contenido = leer_logs(ruta_log)
        if contenido and "ERROR" in contenido:
            print("¡Error detectado en el servicio!")
            break
        time.sleep(5)
    print("Monitoreo finalizado.")


def registrar_evento(ruta_log, mensaje):
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")