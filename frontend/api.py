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
