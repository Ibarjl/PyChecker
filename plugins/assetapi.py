import re
import json
from datetime import datetime
from typing import Dict, List, Optional

class AssetAPIMonitor:
    def __init__(self):
        self.errores_criticos = [
            r"DATABASE.*CONNECTION.*FAILED",
            r"HTTP.*5\d\d",
            r"AUTHENTICATION.*FAILED", 
            r"MEMORY.*LEAK.*DETECTED",
            r"TIMEOUT.*DATABASE"
        ]
        
        self.errores_warning = [
            r"HTTP.*4\d\d",
            r"SLOW.*QUERY",
            r"RATE.*LIMIT.*EXCEEDED",
            r"MEMORY.*USAGE.*HIGH"
        ]
    
    def detectar_error_critico(self, linea_log: str) -> bool:
        """Detecta errores críticos en logs de API"""
        for patron in self.errores_criticos:
            if re.search(patron, linea_log, re.IGNORECASE):
                return True
        return False
    
    def analizar_patron_log(self, linea_log: str) -> Dict:
        """Extrae información estructurada del log"""
        resultado = {
            "timestamp": self._extraer_timestamp(linea_log),
            "nivel": "INFO",
            "endpoint": None,
            "status_code": None,
            "tiempo_respuesta": None,
            "mensaje": linea_log.strip()
        }
        
        if self.detectar_error_critico(linea_log):
            resultado["nivel"] = "CRITICAL"
        elif any(re.search(w, linea_log, re.IGNORECASE) for w in self.errores_warning):
            resultado["nivel"] = "WARNING"
        elif "ERROR" in linea_log.upper():
            resultado["nivel"] = "ERROR"
        
        # Extraer datos HTTP
        http_match = re.search(r"(GET|POST|PUT|DELETE)\s+(/[^\s]*)\s+.*?(\d{3})", linea_log)
        if http_match:
            resultado["metodo"] = http_match.group(1)
            resultado["endpoint"] = http_match.group(2)
            resultado["status_code"] = int(http_match.group(3))
        
        tiempo_match = re.search(r"(\d+)ms", linea_log)
        if tiempo_match:
            resultado["tiempo_respuesta"] = int(tiempo_match.group(1))
        
        return resultado
    
    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        """Evalúa el estado de salud general del servicio API"""
        errores_criticos = 0
        errores_5xx = 0
        requests_total = 0
        
        for log in logs_recientes[-30:]:
            analisis = self.analizar_patron_log(log)
            
            if analisis["nivel"] == "CRITICAL":
                errores_criticos += 1
            
            if analisis["status_code"]:
                requests_total += 1
                if 500 <= analisis["status_code"] < 600:
                    errores_5xx += 1
        
        tasa_error = (errores_5xx / requests_total * 100) if requests_total > 0 else 0
        
        if errores_criticos >= 3 or tasa_error > 15:
            return "CRITICAL"
        elif errores_criticos >= 1 or tasa_error > 5:
            return "ERROR"
        elif tasa_error > 2:
            return "WARNING"
        else:
            return "OK"
    
    def ejecutar_accion_emergencia(self) -> bool:
        """Ejecuta acciones de emergencia para el servicio API"""
        try:
            print("EMERGENCIA API: Reiniciando servicios...")
            # Implementar comandos de reinicio específicos aquí
            return True
        except Exception as e:
            print(f"Error en acción de emergencia: {e}")
            return False
    
    def _extraer_timestamp(self, linea_log: str) -> Optional[str]:
        timestamp_match = re.search(r"\[([\d-]+\s[\d:]+)\]", linea_log)
        return timestamp_match.group(1) if timestamp_match else None
