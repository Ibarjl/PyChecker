# Configuración de Health Monitor

## Para agregar nuevos repositorios a monitorear

### 1. Editar archivo de configuración

Abre: `config/monitor_config.json`

### 2. Agregar nuevo repositorio

```json
{
    "repositorios": {
        "tu_app": {
            "nombre": "Mi Aplicación",
            "ruta_logs": "../mi-repositorio/logs/app.log",
            "descripcion": "Logs de mi aplicación"
        }
    }
}
```

### 3. Ejecutar Health Monitor

```bash
python main.py
```

Seleccionar opción 5: "Monitorear repositorios configurados"

## Ejemplos de rutas comunes

- **Repositorio local**: `../otro-repo/logs/app.log`
- **Directorio absoluto**: `/var/log/miapp/sistema.log`
- **Windows**: `C:/logs/aplicacion.log`
- **Subdirectorio**: `./logs/output.log`

## Troubleshooting

- **Archivo no encontrado**: Verificar que la ruta sea correcta
- **Sin permisos**: Verificar permisos de lectura del archivo
- **Archivo vacío**: El monitor esperará hasta que aparezcan logs nuevos
