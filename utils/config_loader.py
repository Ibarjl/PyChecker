"""
Utilidades para cargar y manejar configuración de repositorios
Versión mejorada con rutas más robustas y mejor manejo de errores
"""
import json
import os

# Definir rutas de manera más robusta
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "config", "monitor_config.json")

def cargar_configuracion_repositorios(config_path=None):
    """
    Carga la configuración de repositorios desde el archivo JSON
    Ahora acepta un path personalizado y usa rutas más robustas
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    
    try:
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Si el archivo no existe, crear uno básico
        if not os.path.exists(config_path):
            print(f"Archivo de configuración no encontrado: {config_path}")
            print("Creando configuración por defecto...")
            crear_configuracion_por_defecto(config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
        
    except json.JSONDecodeError as e:
        print(f"Error en formato JSON del archivo de configuración: {e}")
        return None
    except Exception as e:
        print(f"Error cargando configuración: {e}")
        return None

def crear_configuracion_por_defecto(config_path):
    """
    Crea un archivo de configuración por defecto si no existe
    """
    config_por_defecto = {
        "repositorios": {
            "ejemplo_app": {
                "nombre": "Aplicación de Ejemplo",
                "ruta_logs": "./logs/ejemplo.log",
                "descripcion": "Archivo de ejemplo para demostración"
            }
        },
        "configuracion_general": {
            "timeout_archivo": 30,
            "encoding": "utf-8",
            "mostrar_timestamp": True
        }
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_por_defecto, f, indent=4, ensure_ascii=False)
        print(f"Configuración por defecto creada en: {config_path}")
    except Exception as e:
        print(f"Error creando configuración por defecto: {e}")

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
    Versión mejorada que busca en más ubicaciones
    """
    directorios = [
        "./logs", 
        "../logs", 
        "./", 
        "../",
        "./var/log",
        "/var/log",  # Solo en sistemas Unix
        "./tmp"
    ]
    
    repositorios_detectados = {}
    
    for directorio in directorios:
        try:
            if os.path.exists(directorio) and os.path.isdir(directorio):
                for archivo in os.listdir(directorio):
<<<<<<< HEAD
                    if archivo.endswith(".log"):
=======
        # Funciones para cargar y validar la configuración (usá esto para traer la config y chequear que esté todo bien)
>>>>>>> rama_ibar
                        repo_id = archivo.replace(".log", "")
                        ruta_completa = os.path.abspath(os.path.join(directorio, archivo))
                        repositorios_detectados[repo_id] = {
                            "nombre": f"Auto: {repo_id}",
                            "ruta_logs": ruta_completa,
                            "descripcion": f"Detectado automáticamente en {directorio}"
                        }
        except PermissionError:
            # Saltamos directorios sin permisos
            continue
        except Exception as e:
            print(f"Error explorando directorio {directorio}: {e}")
            continue
    
    return repositorios_detectados

def generar_configuracion_automatica(config_path=None):
    """
    Busca archivos .log y genera/actualiza monitor_config.json automáticamente
    Versión mejorada con mejor manejo de rutas
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    
    # Cargar configuración existente si existe
    config_existente = cargar_configuracion_repositorios(config_path) or {}
    
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
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_final, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Configuración actualizada en {config_path}")
        if nuevos_agregados > 0:
            print(f"📂 Se agregaron {nuevos_agregados} repositorios nuevos")
        else:
            print("ℹ️  No se encontraron repositorios nuevos para agregar")
        
        return config_final
    except Exception as e:
        print(f"❌ Error guardando configuración: {e}")
        return None