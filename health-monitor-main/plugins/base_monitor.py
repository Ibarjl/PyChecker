import re
from typing import Dict, List, Optional
from utils.reinicio_global import reinicio_simple

class BaseMonitor:
    """
    Clase base para todos los monitores de servicios.
    Define métodos comunes: check_logs, analizar_patron_log, detectar_error_critico,
    evaluar_salud_servicio, ejecutar_accion_emergencia.
    """
    def __init__(self):
        self.errores_criticos: List[str] = []
        self.errores_warning: List[str] = []

    def _extraer_timestamp(self, linea_log: str) -> Optional[str]:
        timestamp_match = re.search(r"\[([\d-]+\s[\d:]+)\]", linea_log)
        return timestamp_match.group(1) if timestamp_match else None

    def detectar_error_critico(self, linea_log: str) -> bool:
        """
        Args:
            linea_log (str): Línea de log a analizar.
        Returns:
            bool: True si se detecta un error crítico en la línea de log(linea_log), False en caso contrario.
        Es decir si la lista de errores se encuentra con un string que coincide devuelve true, 
        si esta bien y no encuentra coincidencias devuelve false
        """
        for patron in self.errores_criticos:
            if re.search(patron, linea_log, re.IGNORECASE):
                return True
        return False

    def check_logs(self, logs: str) -> bool:
        """
        Args:
            logs(str): Puede ser una linea o un conjunto de líneas (logs)
        Revisa los logs completos y retorna True si el servicio está sano,
        False si hay algún error crítico.
        """
        for line in logs.splitlines():
            if self.detectar_error_critico(line):
                return False
        return True


    def analizar_patron_log(self, linea_log: str) -> Dict:
        """
        Devuelve un dict con información relevante de la línea de log.
        """
        resultado = {
            "timestamp": self._extraer_timestamp(linea_log),
            "nivel": "INFO",
            "mensaje": linea_log.strip()
        }
        if self.detectar_error_critico(linea_log):
            resultado["nivel"] = "CRITICAL"
        elif any(re.search(w, linea_log, re.IGNORECASE) for w in self.errores_warning):
            resultado["nivel"] = "WARNING"
        elif "ERROR" in linea_log.upper():
            resultado["nivel"] = "ERROR"
        return resultado

    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        errores_criticos = 0
        warnings = 0
        for log in logs_recientes[-30:]:
            analisis = self.analizar_patron_log(log)
            if analisis["nivel"] == "CRITICAL":
                errores_criticos += 1
            elif analisis["nivel"] == "WARNING":
                warnings += 1
        if errores_criticos >= 3:
            return "CRITICAL"
        elif errores_criticos >= 1:
            return "ERROR"
        elif warnings >= 3:
            return "WARNING"
        return "OK"

    def ejecutar_accion_emergencia(self) -> bool:
        """
        Ejecuta acciones de emergencia para el servicio.
        """
        try:
            print("Acción de emergencia ejecutada.")
            reinicio_simple()
            return True
        except Exception as e:
            print(f"Error en acción de emergencia: {e}")
            return False

