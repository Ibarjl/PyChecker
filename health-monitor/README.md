# ⚠️ WORK IN PROGRESS

# Health Monitor

Sistema modular en Python para supervisar la salud de múltiples servicios desde contenedores Docker, pods de Kubernetes o ficheros, detectando errores críticos y reinicando servicios automáticamente. Incluye un frontend web para visualizar el estado de los servicios en tiempo real.

## Estructura del proyecto

```
health-monitor/
├─ main.py             # Orquestador principal del healthcheck
├─ config/
│   └─ monitor_config.json # Configuración de rutas de logs y parámetros generales
├─ config.yaml         # Configuración de programas, logs y límites de reinicio
├─ plugins/
│   ├─ avionics.py     # Plugin para Avionics
│   ├─ asset_api.py    # Plugin para Asset API
│   └─ ...             # Nuevos plugins en el futuro
├─ utils/
│   ├─ docker_utils.py # Funciones para leer logs de Docker
│   ├─ k8s_utils.py    # Funciones para leer logs de Kubernetes
│   ├─ file_utils.py   # Funciones para leer ficheros de logs
│   └─ config_loader.py # Utilidades para cargar configuración de logs
├─ frontend/
│   ├─ __init__.py     # Indica que es un paquete Python
│   ├─ app.py          # Servidor web principal
│   ├─ api.py          # Endpoints para obtener estado desde el core
│   ├─ templates/
│   │   └─ index.html  # Dashboard principal
│   └─ static/
│       ├─ style.css   # Estilos
│       └─ script.js   # JS para refrescar estado
├─ CONFIGURACION.md    # Guía para configurar y adaptar el monitor
└─ requirements.txt    # Dependencias del proyecto
```

## Requisitos

- Python 3.11+
- Docker
- Cluster Kubernetes
- Librerías (requirements.txt)

## Instalación

1. Clonar el repositorio

```
git clone https://gitlab.ngws.itbindra.es/ccanadasg/health-monitor.git
cd health-monitor
```

2. Crear un entorno virtual

```
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Instalar dependencias

```
pip install -r requirements.txt
```

## Acceso al frontend

```
python app.py
```

Acceder en el navegador a 127.0.0.1:5000/

# ⚠️ WORK IN PROGRESS
