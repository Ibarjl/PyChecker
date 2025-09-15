<<<<<<< HEAD
# Configuración de Health Monitor

## Para agregar nuevos repositorios a monitorear

### 1. Editar archivo de configuración

Abre: `config/monitor_config.json`

### 2. Agregar nuevo repositorio
=======

# Configuración de Health Monitor

## ¿Cómo agregar o modificar repositorios para monitorear?

Tenés dos formas de hacerlo:

### Opción 1: Usá la aplicación de escritorio

Cuando arrancás Health Monitor con `python main.py`, se va a abrir automáticamente una app donde podés ver y editar la configuración de los repositorios de manera fácil y visual. Hacé los cambios que necesites y guardá.

### Opción 2: Editá el archivo a mano

Abrid el archivo: `config/monitor_config.json`
Agregá o modificá la sección de repositorios siguiendo este ejemplo:
>>>>>>> rama_ibar

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

<<<<<<< HEAD
### 3. Ejecutar Health Monitor

```bash
python main.py
```

Seleccionar opción 5: "Monitorear repositorios configurados"
=======
## ¿Cómo poner en marcha el monitoreo?

1. Ejecutá Health Monitor:

    ```bash
    python main.py
    ```

2. Hacé los cambios de configuración si lo necesitás (desde la app o a mano).
3. Elegí la opción correspondiente en el menú para monitorear los repositorios configurados.
>>>>>>> rama_ibar

## Ejemplos de rutas comunes

- **Repositorio local**: `../otro-repo/logs/app.log`
- **Directorio absoluto**: `/var/log/miapp/sistema.log`
- **Windows**: `C:/logs/aplicacion.log`
- **Subdirectorio**: `./logs/output.log`

<<<<<<< HEAD
## Troubleshooting

- **Archivo no encontrado**: Verificar que la ruta sea correcta
- **Sin permisos**: Verificar permisos de lectura del archivo
- **Archivo vacío**: El monitor esperará hasta que aparezcan logs nuevos
=======
## Problemas frecuentes y soluciones

- **Archivo no encontrado**: Fijate que la ruta sea correcta.
- **Sin permisos**: Revisá los permisos de lectura del archivo.
- **Archivo vacío**: El monitor va a esperar hasta que aparezcan logs nuevos.
>>>>>>> rama_ibar
