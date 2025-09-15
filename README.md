
# Comenzá a usar

Seguí estos pasos para arrancar con Health Monitor:

1. Abrí una terminal en la carpeta raíz del proyecto (donde está el archivo main.py).
2. Yo creé un entorno virtual (pero cada uno que se sienta libre de hacer lo que quiera):

```bash
python -m venv .venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Instalá las dependencias necesarias:

```bash
pip install -r requirements.txt
```

4. Ejecutá el archivo principal:

```bash
python main.py
```

5. Al iniciar, se va a abrir automáticamente la aplicación de escritorio para que configures lo que necesites. Hacé los cambios y guardá.
6. Usá el menú que aparece en la terminal para consultar logs o acceder a otras funciones.
7. Si querés ver el estado en tiempo real desde la web, ejecutá:

```bash
python frontend/app.py
```

Abrí tu navegador y entrá en 127.0.0.1:5000/

# Health Monitor

Este proyecto te ayuda a supervisar y cuidar el estado de diferentes servicios y aplicaciones, ya sea que estén en contenedores Docker, en Kubernetes o simplemente como archivos de registro. Podés ver el estado en tiempo real desde una página web y también modificar la configuración fácil con una pequeña aplicación de escritorio incluida.

## ¿Qué podés hacer con Health Monitor?

- Mirá el estado de tus servicios y aplicaciones en tiempo real.
- Consultá los registros (logs) para saber qué está pasando.
- Configurá qué se monitorea y cómo, usando una app sencilla.
- Ampliá el sistema con nuevos complementos (plugins) según lo que necesites.

## ¿Cómo está organizado?

El proyecto está dividido en carpetas, cada una con una función específica:

- **config/**: Acá están los archivos de configuración. Podés editarlos a mano o usar la app de escritorio para hacerlo más fácil.
- **frontend/**: Tiene la parte visual y la web donde ves el estado de los servicios.
- **logs/**: Acá se guardan los registros generados por los servicios monitoreados.
- **plugins/**: Complementos que permiten agregar nuevas funciones o conectar con otros sistemas.
- **utils/**: Herramientas y scripts que ayudan al funcionamiento general, como el editor de configuración.

## ¿Cómo lo usás?

1. Instala Python 3.11 o superior en tu computadora.
2. Instala las dependencias que están en el archivo `requirements.txt`.
3. Ejecuta el archivo principal `main.py`. Al iniciar, se abrirá automáticamente la app para editar la configuración.
4. Usa el menú para consultar logs o el frontend web para ver el estado en tiempo real.

## ¿Quién puede usarlo?

Este sistema está pensado para que cualquier persona pueda supervisar sus servicios, sin importar si tiene experiencia técnica o no. La configuración y el uso son sencillos y directos.

---
Si tienes dudas sobre alguna carpeta o función, revisa el archivo `README.md` dentro de cada carpeta para más detalles.

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
