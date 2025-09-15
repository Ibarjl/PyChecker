"""
Plugin Runtime - Monitoreo de memoria, CPU y rendimiento del sistema
"""
import re
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from utils.reinicio_global import reinicio_simple

class RuntimeMonitor:
    def __init__(self):
        self.errores_criticos = [
            r"OUT.*OF.*MEMORY",
            r"MEMORY.*LEAK",
            r"STACK.*OVERFLOW",
            r"SEGMENTATION.*FAULT",
            r"DEADLOCK.*DETECTED"
        ]
        
        self.errores_warning = [
            r"MEMORY.*USAGE.*HIGH",
            r"CPU.*USAGE.*HIGH",
            r"DISK.*SPACE.*LOW",
            r"THREAD.*CONTENTION"
        ]
    
    def detectar_error_critico(self, linea_log: str) -> bool:
        for patron in self.errores_criticos:
            if re.search(patron, linea_log, re.IGNORECASE):
                return True
        return False
    
    def analizar_patron_log(self, linea_log: str) -> Dict:
        resultado = {
            "timestamp": self._extraer_timestamp(linea_log),
            "nivel": "INFO",
            "memoria_mb": None,
            "cpu_porcentaje": None,
            "mensaje": linea_log.strip()
        }
        
        if self.detectar_error_critico(linea_log):
            resultado["nivel"] = "CRITICAL"
        elif any(re.search(w, linea_log, re.IGNORECASE) for w in self.errores_warning):
            resultado["nivel"] = "WARNING"
        elif "ERROR" in linea_log.upper():
            resultado["nivel"] = "ERROR"
        
        # Extraer métricas
        memoria_match = re.search(r"MEMORY.*?(\d+)MB", linea_log)
        if memoria_match:
            resultado["memoria_mb"] = int(memoria_match.group(1))
        
        cpu_match = re.search(r"CPU.*?(\d+)%", linea_log)
        if cpu_match:
            resultado["cpu_porcentaje"] = int(cpu_match.group(1))
        
        return resultado
    
    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        errores_criticos = 0
        memoria_alta = 0
        
        for log in logs_recientes[-20:]:
            analisis = self.analizar_patron_log(log)
            
            if analisis["nivel"] == "CRITICAL":
                errores_criticos += 1
            
            if analisis["memoria_mb"] and analisis["memoria_mb"] > 8000:
                memoria_alta += 1
        
        if errores_criticos >= 2:
            return "CRITICAL"
        elif errores_criticos >= 1 or memoria_alta >= 5:
            return "ERROR"
        elif memoria_alta >= 2:
            return "WARNING"
        else:
            return "OK"
    
    def ejecutar_accion_emergencia(self) -> bool:
        try:
            print("EMERGENCIA RUNTIME: Reiniciando servicios...")
            reinicio_simple()
            print("Liberando memoria...")
            return True
        except Exception as e:
            print(f"Error en optimización: {e}")
            return False
    
    def _extraer_timestamp(self, linea_log: str) -> Optional[str]:
        timestamp_match = re.search(r"\[([\d-]+\s[\d:]+)\]", linea_log)
        return timestamp_match.group(1) if timestamp_match else None

# Mantener funciones existentes para compatibilidad
def cargar_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def obtener_ruta_log(config, repo_name):
    return config["repositorios"][repo_name]["ruta_logs"]

def leer_logs(ruta_logs):
    if not os.path.exists(ruta_logs):
        print(f"Error: No se encuentra el archivo {ruta_logs}")
        return None
    
    try:
        with open(ruta_logs, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error leyendo logs: {e}")
        return None

def registrar_evento(ruta_log, mensaje):
    timestamp = datetime.now().isoformat()
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")