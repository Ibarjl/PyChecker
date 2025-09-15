"""
Plugin Avionics - Monitoreo de sistemas de navegación y vuelo

Ejemplo educativo:
Puedes cargar parámetros desde un archivo YAML usando:
    from utils.yaml_config import get_config_for_plugin
    self.config = get_config_for_plugin('avionics')
    self.max_reinicios = self.config.get('max_reinicios_por_hora', 3)
    self.timeout = self.config.get('timeout_verificacion_segundos', 30)
    self.umbral_criticos = self.config.get('umbral_errores_criticos', 2)
Así puedes modificar la configuración sin cambiar el código fuente.
"""
import re
from datetime import datetime
from typing import Dict, List, Optional
from utils.reinicio_global import reinicio_simple

class AvionicsMonitor:
    def __init__(self):
        # MODIFICA AQUÍ: Puedes cargar patrones y parámetros desde YAML
        try:
            from utils.yaml_config import get_config_for_plugin
            self.config = get_config_for_plugin('avionics')
            self.errores_criticos = self.config.get('errores_criticos', [
                r"GPS.*SIGNAL.*LOST",
                r"ALTITUDE.*SENSOR.*FAULT",
                r"NAVIGATION.*ERROR",
                r"ENGINE.*TEMPERATURE.*CRITICAL",
                r"EMERGENCY.*LANDING"
            ])
            self.errores_warning = self.config.get('errores_warning', [
                r"GPS.*ACCURACY.*LOW",
                r"BATTERY.*LOW",
                r"SIGNAL.*WEAK",
                r"ALTITUDE.*WARNING"
            ])
            self.max_reinicios = self.config.get('max_reinicios_por_hora', 3)
            self.timeout = self.config.get('timeout_verificacion_segundos', 30)
            self.umbral_criticos = self.config.get('umbral_errores_criticos', 2)
        except ImportError:
            # Si no existe utils.yaml_config, usa valores por defecto
            self.errores_criticos = [
                r"GPS.*SIGNAL.*LOST",
                r"ALTITUDE.*SENSOR.*FAULT",
                r"NAVIGATION.*ERROR",
                r"ENGINE.*TEMPERATURE.*CRITICAL",
                r"EMERGENCY.*LANDING"
            ]
            self.errores_warning = [
                r"GPS.*ACCURACY.*LOW",
                r"BATTERY.*LOW",
                r"SIGNAL.*WEAK",
                r"ALTITUDE.*WARNING"
            ]
            self.max_reinicios = 3
            self.timeout = 30
            self.umbral_criticos = 2
    
    def detectar_error_critico(self, linea_log: str) -> bool:
        # Usa patrones configurables para detectar errores críticos
        for patron in self.errores_criticos:
            if re.search(patron, linea_log, re.IGNORECASE):
                return True
        return False
    
    def analizar_patron_log(self, linea_log: str) -> Dict:
        # Procesa una línea de log y extrae información relevante
        resultado = {
            "timestamp": self._extraer_timestamp(linea_log),
            "nivel": "INFO",
            "componente": "UNKNOWN",
            "gps_lat": None,
            "gps_lon": None,
            "altitud": None,
            "mensaje": linea_log.strip()
        }
        if self.detectar_error_critico(linea_log):
            resultado["nivel"] = "CRITICAL"
        elif any(re.search(w, linea_log, re.IGNORECASE) for w in self.errores_warning):
            resultado["nivel"] = "WARNING"
        elif "ERROR" in linea_log.upper():
            resultado["nivel"] = "ERROR"
        # Identificar componente
        componentes = ["GPS", "ALTITUDE", "ENGINE", "NAVIGATION"]
        for comp in componentes:
            if comp in linea_log.upper():
                resultado["componente"] = comp
                break
        # Extraer coordenadas GPS
        gps_match = re.search(r"LAT:([+-]?\d*\.?\d+).*LON:([+-]?\d*\.?\d+)", linea_log)
        if gps_match:
            resultado["gps_lat"] = float(gps_match.group(1))
            resultado["gps_lon"] = float(gps_match.group(2))
        return resultado
    
    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        # Determina el estado general del sistema usando parámetros configurables
        errores_criticos = 0
        warnings = 0
        gps_disponible = False
        for log in logs_recientes[-20:]:
            if self.detectar_error_critico(log):
                errores_criticos += 1
            elif any(re.search(w, log, re.IGNORECASE) for w in self.errores_warning):
                warnings += 1
            if "GPS" in log and "OK" in log:
                gps_disponible = True
        if errores_criticos >= self.umbral_criticos:
            return "CRITICAL"
        elif errores_criticos >= 1 or not gps_disponible:
            return "ERROR"
        elif warnings >= 3:
            return "WARNING"
        else:
            return "OK"
    
    def ejecutar_accion_emergencia(self) -> bool:
        # Realiza acciones correctivas automáticas
        try:
            print("EMERGENCIA AVIONICA: Activando protocolo de seguridad...")
            reinicio_simple()
            print("Enviando alerta a torre de control...")
            return True
        except Exception as e:
            print(f"Error en protocolo de emergencia: {e}")
            return False
    
    def _extraer_timestamp(self, linea_log: str) -> Optional[str]:
        timestamp_match = re.search(r"\[([\d-]+\s[\d:]+)\]", linea_log)
        return timestamp_match.group(1) if timestamp_match else None