"""
Utilidades para cargar y manejar configuración de repositorios
"""
import json
import os

def cargar_configuracion_repositorios():
    """
    Carga la configuración de repositorios desde el archivo JSON
    """
    config_path = "config/monitor_config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado: {config_path}")
        return None
    except Exception as e:
        print(f"Error cargando configuración: {e}")
        return None

def listar_repositorios_disponibles():
    """
    Lista todos los repositorios configurados
    """
    config = cargar_configuracion_repositorios()
    if not config:
        return []
    
    repositorios = []
    for key, repo in config.get("repositorios", {}).items():
        repositorios.append({
            "id": key,
            "nombre": repo.get("nombre", key),
            "ruta": repo.get("ruta_logs", ""),
            "descripcion": repo.get("descripcion", "Sin descripción")
        })
    
    return repositorios

def detectar_logs():
    """
    Detecta archivos .log en directorios comunes
    """
    directorios = ["./logs", "../logs", "./", "../"]
    repositorios_detectados = {}
    
    for directorio in directorios:
        if os.path.exists(directorio):
            for archivo in os.listdir(directorio):
                if archivo.endswith(".log"):
                    repo_id = archivo.replace(".log", "")
                    repositorios_detectados[repo_id] = {
                        "nombre": f"Auto: {repo_id}",
                        "ruta_logs": os.path.join(directorio, archivo),
                        "descripcion": f"Detectado automáticamente en {directorio}"
                    }
    
    return repositorios_detectados

def generar_configuracion_automatica(config_path="config/monitor_config.json"):
    """
    Busca archivos .log y genera/actualiza monitor_config.json automáticamente
    """
    # Cargar configuración existente si existe
    config_existente = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_existente = json.load(f)
    
    # Detectar nuevos logs
    repositorios_detectados = detectar_logs()
    
    # Merge: mantener configuraciones manuales, agregar solo nuevos
    repositorios_finales = config_existente.get("repositorios", {})
    nuevos_agregados = 0
    
    for repo_id, repo_config in repositorios_detectados.items():
        if repo_id not in repositorios_finales:
            repositorios_finales[repo_id] = repo_config
            nuevos_agregados += 1
    
    # Configuración final
    config_final = {
        "repositorios": repositorios_finales,
        "configuracion_general": config_existente.get("configuracion_general", {
            "timeout_archivo": 30,
            "encoding": "utf-8",
            "mostrar_timestamp": True
        })
    }
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Guardar configuración
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_final, f, indent=4, ensure_ascii=False)
    
    print(f"Configuración actualizada en {config_path}")
    if nuevos_agregados > 0:
        print(f"Se agregaron {nuevos_agregados} repositorios nuevos")
    else:
        print("No se encontraron repositorios nuevos para agregar")
    
    return config_final