# Arquitectura del Health Monitor

## Visión General

Health Monitor utiliza una arquitectura modular basada en plugins que permite monitorear diferentes tipos de servicios de manera especializada.

## Componentes Principales

### Core System (`main.py`)

El orquestador principal que coordina todos los componentes y proporciona la interfaz de usuario por consola.

### Sistema de Plugins (`plugins/`)

Cada plugin especializado hereda un patrón común:

- `analizar_patron_log()` - Procesa líneas de log individuales
- `evaluar_salud_servicio()` - Determina el estado general del servicio
- `ejecutar_accion_emergencia()` - Realiza acciones correctivas automáticas

**Plugins Actuales:**

- **Avionics** - Sistemas de navegación y vuelo
- **Asset API** - APIs REST y servicios web
- **Runtime** - Memoria, CPU y rendimiento del sistema

### Frontend Web (`frontend/`)

Interfaz web construida con Flask que proporciona visualización en tiempo real del estado de los servicios.

### Utilidades (`utils/`)

Funciones reutilizables para interactuar con Docker, Kubernetes, y sistemas de archivos.

## Configuración

### config.yaml

Configuración principal que define límites y parámetros por servicio. Permite personalizar el comportamiento sin modificar código.

### config/monitor_config.json

Configuración de repositorios específicos a monitorear, incluyendo rutas de logs y descripciones.

## Extensibilidad

### Agregar un Nuevo Plugin

1. Crear `plugins/nuevo_plugin.py`
2. Implementar la clase con los métodos requeridos
3. Agregar configuración en `config.yaml`
4. Integrar en `main.py`

### Ejemplo de Estructura de Plugin

```python
class NuevoPlugin:
    def analizar_patron_log(self, linea_log: str) -> Dict:
        # Procesar línea individual
        pass
    
    def evaluar_salud_servicio(self, logs_recientes: List[str]) -> str:
        # Determinar estado: "OK", "WARNING", "ERROR", "CRITICAL"
        pass
    
    def ejecutar_accion_emergencia(self) -> bool:
        # Acciones correctivas automáticas
        pass
```
