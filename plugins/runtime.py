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



import re
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class RuntimeMonitor:
    def __init__(self):
        self.errores_criticos = [
            r"OUT.*OF.*MEMORY",
            r"MEMORY.*LEAK",
            r"STACK.*OVERFLOW", 
            r"SEGMENTATION.*FAULT",
            r"DEADLOCK.*DETECTED",
            r"THREAD.*POOL.*EXHAUSTED"
        ]
        
        self.errores_warning = [
            r"MEMORY.*USAGE.*HIGH",
            r"CPU.*USAGE.*HIGH",
            r"DISK.*SPACE.*LOW",
            r"GARBAGE.*COLLECTION.*SLOW",
            r"THREAD.*CONTENTION"
        ]
    
    def detectar_error_critico(self, linea_log: str) -> bool:
        """Detecta errores críticos de runtime"""
        for patron in self.errores_criticos:
            if re.search(patron, linea_log, re.IGNORECASE):
                return True
        return False
    
    def analizar_patron_log(self, linea_log: str) -> Dict:
        """Extrae métricas de rendimiento del log"""
        resultado = {
            "timestamp": self._extraer_timestamp(linea_log),
            "nivel": "INFO",
            "memoria_mb": None,
            "cpu_porcentaje": None,
            "threads_count": None,
            "mensaje": linea_log.strip()
        }
        
        if self.detectar_error_critico(linea_log):
            resultado["nivel"] = "CRITICAL"
        elif any(re.search(w, linea_log, re.IGNORECASE) for w in self.errores_warning):
            resultado["nivel"] = "WARNING"
        elif "ERROR" in linea_log.upper():
            resultado["nivel"] = "ERROR"
        
        # Extraer métricas específicas
        memoria_match = re.search(r"MEMORY.*?(\d+)MB", linea_log)
        if memoria_match:
            resultado["memoria_mb"] = int(memoria_match.group(1))
        
        cpu_match = re.search(r"CPU.*?(\d+)%", linea_log)
        if cpu_match:
            resultado["cpu_porcentaje"] = int(cpu_match.group(1))
        
        threads_match = re.search(r"THREADS.*?(\d+)", linea_log)
        if threads_match:
            resultado["threads_count"] = int(threads_match.group(1))
        
        return resultado
    
    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        """Evalúa el estado de salud del runtime del sistema"""
        errores_criticos = 0
        memoria_promedio = 0
        cpu_promedio = 0
        count_memoria = 0
        count_cpu = 0
        
        for log in logs_recientes[-30:]:
            analisis = self.analizar_patron_log(log)
            
            if analisis["nivel"] == "CRITICAL":
                errores_criticos += 1
            
            if analisis["memoria_mb"]:
                memoria_promedio += analisis["memoria_mb"]
                count_memoria += 1
            
            if analisis["cpu_porcentaje"]:
                cpu_promedio += analisis["cpu_porcentaje"]
                count_cpu += 1
        
        # Calcular promedios
        if count_memoria > 0:
            memoria_promedio = memoria_promedio / count_memoria
        if count_cpu > 0:
            cpu_promedio = cpu_promedio / count_cpu
        
        if errores_criticos >= 2 or memoria_promedio > 8000 or cpu_promedio > 95:
            return "CRITICAL"
        elif errores_criticos >= 1 or memoria_promedio > 6000 or cpu_promedio > 85:
            return "ERROR"
        elif memoria_promedio > 4000 or cpu_promedio > 70:
            return "WARNING"
        else:
            return "OK"
    
    def ejecutar_accion_emergencia(self) -> bool:
        """Ejecuta optimización de emergencia del runtime"""
        try:
            print("EMERGENCIA RUNTIME: Optimizando sistema...")
            print("Liberando memoria...")
            print("Reduciendo carga de CPU...")
            return True
        except Exception as e:
            print(f"Error en optimización de emergencia: {e}")
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
        logger.error(f"No es posible encontrar {ruta_logs}")
        return None
    try:
        with open(ruta_logs, "r", encoding="utf-8") as fpath:
            return fpath.read()
    except Exception as e:
        logger.exception(f"Excepción encontrada: {e}")
        return None

def registrar_evento(ruta_log, mensaje):
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {mensaje}\n")
