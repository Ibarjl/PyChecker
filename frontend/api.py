
"""
API real que se comunica con el backend del healthcheck
Ya no usa datos simulados - lee el estado real del sistema
"""

import json
import os
from datetime import datetime

# Ruta al archivo de estado compartido con el backend
ESTADO_PATH = os.path.join(os.path.dirname(__file__), "estado_actual.json")

def get_status():
    """
    Obtiene el estado real de los servicios desde el archivo compartido
    que actualiza el backend cuando ejecuta análisis
    """
    try:
        # Intentar leer el estado actual del archivo
        if os.path.exists(ESTADO_PATH):
            with open(ESTADO_PATH, 'r', encoding='utf-8') as f:
                estado_real = json.load(f)
            return estado_real
        else:
            # Si no existe el archivo, devolver estado por defecto
            return [
                {
                    "name": "Sistema de Monitoreo",
                    "status": "WAITING",
                    "last_error": "No se ha ejecutado ningún análisis aún",
                    "restarts_last_hour": 0,
                    "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
    except json.JSONDecodeError:
        # Si el archivo JSON está corrupto
        return [
            {
                "name": "Sistema de Monitoreo",
                "status": "ERROR",
                "last_error": "Error leyendo estado del sistema",
                "restarts_last_hour": 0,
                "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    except Exception as e:
        # Cualquier otro error
        return [
            {
                "name": "Sistema de Monitoreo",
                "status": "ERROR",
                "last_error": f"Error inesperado: {str(e)}",
                "restarts_last_hour": 0,
                "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

def get_system_info():
    """
    Función adicional para obtener información del sistema de monitoreo
    """
    return {
        "monitor_version": "1.0.0",
        "estado_file_exists": os.path.exists(ESTADO_PATH),
        "last_update": os.path.getmtime(ESTADO_PATH) if os.path.exists(ESTADO_PATH) else None
    }

# Este módulo simula la comunicación con el core healthcheck.
# Más adelante, se puede conectar a un socket, base de datos o API interna.

from datetime import datetime

# Ejemplo de estado simulado
def get_status():
    return [
        {
            "name": "Avionics",
            "status": "OK",
            "last_error": None,
            "restarts_last_hour": 1,
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "name": "Asset API",
            "status": "ERROR",
            "last_error": "ConnectionTimeout",
            "restarts_last_hour": 2,
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

