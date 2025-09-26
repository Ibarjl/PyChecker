import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import sys

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/monitor_config.json')

class ConfigEditor:
    def __init__(self, master):
        self.master = master
        self.master.title('Editor de Configuración (configurá a tu gusto)')
        self.master.geometry('1100x600')  # Más ancho que largo
        self.master.configure(bg='#f2f2f2')
        self.load_config()
        self.create_widgets()

    def load_config(self):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def save_config(self):
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            messagebox.showinfo('Guardado', '¡Listo! Guardaste la configuración.')
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo guardar: {e}. Fijate si tenés permisos o si el archivo está abierto en otro programa.')

    def create_widgets(self):
        # Frame principal horizontal
        main_frame = tk.Frame(self.master, bg='#f2f2f2')
        main_frame.pack(fill='both', expand=True)

        # Frame izquierdo: menú y config
        left_frame = tk.Frame(main_frame, bg='#f2f2f2')
        left_frame.pack(side='left', fill='y', padx=20, pady=20)

        # Frame derecho: área de resultados
        right_frame = tk.Frame(main_frame, bg='#f2f2f2')
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=20)

        # Configuración general
        tk.Label(left_frame, text='Tiempo de espera (segundos):', bg='#f2f2f2', font=('Segoe UI', 10)).pack(anchor='w')
        self.timeout_var = tk.StringVar(value=str(self.config['configuracion_general']['timeout_archivo']))
        tk.Entry(left_frame, textvariable=self.timeout_var, width=18, font=('Segoe UI', 10)).pack(anchor='w', pady=2)

        tk.Label(left_frame, text='Codificación (encoding):', bg='#f2f2f2', font=('Segoe UI', 10)).pack(anchor='w')
        self.encoding_var = tk.StringVar(value=self.config['configuracion_general']['encoding'])
        tk.Entry(left_frame, textvariable=self.encoding_var, width=18, font=('Segoe UI', 10)).pack(anchor='w', pady=2)

        tk.Label(left_frame, text='¿Querés mostrar la hora en los logs?', bg='#f2f2f2', font=('Segoe UI', 10)).pack(anchor='w')
        self.timestamp_var = tk.BooleanVar(value=self.config['configuracion_general']['mostrar_timestamp'])
        tk.Checkbutton(left_frame, variable=self.timestamp_var, bg='#f2f2f2').pack(anchor='w', pady=2)

        # Botón para editar repositorios
        tk.Button(left_frame, text='Editá los repositorios', command=self.edit_repos, bg='#e0e0e0', font=('Segoe UI', 10)).pack(fill='x', pady=4)

        # Botón para guardar
        tk.Button(left_frame, text='Guardá los cambios', command=self.on_save, bg='#b2dfdb', font=('Segoe UI', 10, 'bold')).pack(fill='x', pady=4)

        # Separador visual
        tk.Label(left_frame, text='Acciones de monitoreo', bg='#f2f2f2', font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(16,4))

        # Botones de menú
        botones = [
            ('Leer logs de Docker', self.leer_logs_docker),
            ('Leer logs de Kubernetes', self.leer_logs_k8s),
            ('Leer logs de un fichero', self.leer_logs_archivo),
            ('Monitorear archivo en tiempo real', self.monitorear_archivo_realtime),
            ('Monitorear repositorios configurados', self.monitorear_repos_config),
            ('Monitorear aplicación externa', self.monitorear_app_externa),
            ('Ejecutar y monitorear programa', self.ejecutar_y_monitorear),
            ('Generar configuración automática', self.generar_config_auto),
            ('Monitoreo con plugin especializado', self.monitorear_plugin)
        ]
        for texto, comando in botones:
            tk.Button(left_frame, text=texto, command=comando, bg='#e0e0e0', font=('Segoe UI', 10)).pack(fill='x', pady=2)

        # Área de resultados (logs y outputs)
        self.result_text = tk.Text(right_frame, height=32, width=90, font=('Consolas', 11), bg='#ffffff', fg='#222')
        self.result_text.pack(fill='both', expand=True)

    # Métodos para cada acción del menú
    def leer_logs_docker(self):
        nombre = simpledialog.askstring('Docker', 'Nombre o ID del contenedor Docker:')
        if not nombre:
            self.result_text.insert(tk.END, 'No se ingresó ningún contenedor\n')
            return
        try:
            from utils.docker_utils import get_docker_logs
            logs = get_docker_logs(nombre, tail=50)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f'===== LOGS DOCKER =====\n{logs}\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error leyendo logs de Docker: {e}\n')

    def leer_logs_k8s(self):
        pod = simpledialog.askstring('Kubernetes', 'Nombre del pod:')
        namespace = simpledialog.askstring('Kubernetes', 'Namespace (default si vacío):') or 'default'
        if not pod:
            self.result_text.insert(tk.END, 'No se ingresó ningún pod\n')
            return
        try:
            from utils.k8s_utils import get_k8s_pod_logs
            logs = get_k8s_pod_logs(pod, namespace=namespace, tail=50)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f'===== LOGS KUBERNETES =====\n{logs}\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error leyendo logs de K8s: {e}\n')

    def leer_logs_archivo(self):
        ruta = simpledialog.askstring('Archivo', 'Ruta del fichero de logs:')
        if not ruta:
            self.result_text.insert(tk.END, 'No se ingresó ninguna ruta\n')
            return
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                logs = ''.join(f.readlines()[-50:])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f'===== LOGS ARCHIVO =====\n{logs}\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error leyendo archivo: {e}\n')

    def monitorear_archivo_realtime(self):
        ruta = simpledialog.askstring('Archivo', 'Ruta del fichero de logs a monitorear:')
        if not ruta:
            self.result_text.insert(tk.END, 'No se ingresó ninguna ruta\n')
            return
        try:
            from utils.file_utils import monitorear_log
            self.result_text.insert(tk.END, f'Monitoreando: {ruta}\nPresioná Ctrl+C para detener\n')
            monitorear_log(ruta)  # Esto debería actualizar el área de texto en tiempo real (requiere adaptación)
        except Exception as e:
            self.result_text.insert(tk.END, f'Error monitoreando archivo: {e}\n')

    def monitorear_repos_config(self):
        try:
            from config.config_loader import listar_repositorios_disponibles
            repos = listar_repositorios_disponibles()
            if not repos:
                self.result_text.insert(tk.END, 'No hay repositorios configurados\n')
                return
            texto = 'Repositorios disponibles:\n'
            for repo in repos:
                texto += f"- {repo['nombre']} | Ruta: {repo['ruta']} | {repo['descripcion']}\n"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, texto)
        except Exception as e:
            self.result_text.insert(tk.END, f'Error listando repositorios: {e}\n')

    def monitorear_app_externa(self):
        rutas = [
            '../otro-repositorio/logs/app.log',
            '../otro-repositorio/output.log',
            './logs/external.log',
            'C:/logs/sistema.log'
        ]
        texto = 'Rutas disponibles:\n'
        for i, ruta in enumerate(rutas, 1):
            texto += f'{i}. {ruta}\n'
        texto += f'{len(rutas)+1}. Escribir ruta personalizada\n'
        opcion = simpledialog.askinteger('Archivo externo', f'{texto}\nElegí una opción (1-{len(rutas)+1}):')
        if opcion and 1 <= opcion <= len(rutas):
            ruta_archivo = rutas[opcion-1]
        else:
            ruta_archivo = simpledialog.askstring('Archivo externo', 'Escribí la ruta completa:')
        if not ruta_archivo:
            self.result_text.insert(tk.END, 'No se ingresó ninguna ruta\n')
            return
        self.leer_logs_archivo_custom(ruta_archivo)

    def leer_logs_archivo_custom(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                logs = ''.join(f.readlines()[-50:])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f'===== LOGS ARCHIVO EXTERNO =====\n{logs}\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error leyendo archivo externo: {e}\n')

    def ejecutar_y_monitorear(self):
        ruta = simpledialog.askstring('Programa', 'Ruta completa al script Python (.py):')
        if not ruta or not os.path.exists(ruta):
            self.result_text.insert(tk.END, f'No se encontró el archivo: {ruta}\n')
            return
        self.result_text.insert(tk.END, f'Ejecutando: {ruta}\n')
        try:
            import subprocess
            proceso = subprocess.Popen(
                [sys.executable, ruta],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            for linea in iter(proceso.stdout.readline, ''):
                if linea:
                    self.result_text.insert(tk.END, linea)
            proceso.wait()
            self.result_text.insert(tk.END, f'Programa terminado con código: {proceso.returncode}\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error ejecutando programa: {e}\n')

    def generar_config_auto(self):
        self.result_text.insert(tk.END, 'Generando configuración automática...\n')
        try:
            from config.config_loader import generar_configuracion_automatica
            config = generar_configuracion_automatica()
            if config and config.get('repositorios'):
                texto = '\nRepositorios detectados:\n'
                for repo_id, repo_config in config['repositorios'].items():
                    texto += f"- {repo_config['nombre']} | Ruta: {repo_config['ruta_logs']}\n"
                self.result_text.insert(tk.END, texto)
            else:
                self.result_text.insert(tk.END, 'No se encontraron archivos .log para configurar\n')
        except Exception as e:
            self.result_text.insert(tk.END, f'Error generando configuración: {e}\n')

    def monitorear_plugin(self):
        self.result_text.insert(tk.END, 'Monitoreo con plugin especializado\n')
        opciones = ['Avionics', 'Asset API', 'Runtime']
        opcion = simpledialog.askinteger('Plugin', f'Seleccioná plugin:\n1. Avionics\n2. Asset API\n3. Runtime')
        archivo = simpledialog.askstring('Plugin', 'Ruta del archivo de logs:')
        if not opcion or not archivo:
            self.result_text.insert(tk.END, 'No se ingresó plugin o archivo\n')
            return
        try:
            if opcion == 1:
                from plugins.avionics import AvionicsMonitor
                monitor = AvionicsMonitor()
                plugin_name = 'Avionics'
            elif opcion == 2:
                from plugins.asset_api import AssetAPIMonitor
                monitor = AssetAPIMonitor()
                plugin_name = 'Asset API'
            elif opcion == 3:
                from plugins.runtime import RuntimeMonitor
                monitor = RuntimeMonitor()
                plugin_name = 'Runtime'
            else:
                self.result_text.insert(tk.END, 'Opción de plugin no válida\n')
                return
            with open(archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()[-50:]
            errores_criticos = 0
            warnings = 0
            errores = 0
            for linea in lineas:
                analisis = monitor.analizar_patron_log(linea.strip())
                if analisis['nivel'] == 'CRITICAL':
                    errores_criticos += 1
                elif analisis['nivel'] == 'ERROR':
                    errores += 1
                elif analisis['nivel'] == 'WARNING':
                    warnings += 1
            estado_salud = monitor.evaluar_salud_servicio(lineas)
            resumen = f"\n=== RESUMEN DEL ANÁLISIS ===\nEstado del servicio: {estado_salud}\nErrores críticos: {errores_criticos}\nErrores: {errores}\nWarnings: {warnings}\nLíneas analizadas: {len(lineas)}\n"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, resumen)
        except Exception as e:
            self.result_text.insert(tk.END, f'Error en monitoreo de plugin: {e}\n')

    def edit_repos(self):
        repos = self.config['repositorios']
        keys = list(repos.keys())
        choice = simpledialog.askstring('Repositorio', f'Escribí el nombre interno del repositorio que querés editar:\n{keys}')
        if choice and choice in repos:
            repo = repos[choice]
            nombre = simpledialog.askstring('Nombre', 'Nombre:', initialvalue=repo['nombre'])
            ruta_logs = simpledialog.askstring('Ruta de logs', '¿Dónde están los logs?', initialvalue=repo['ruta_logs'])
            descripcion = simpledialog.askstring('Descripción', 'Poné una descripción:', initialvalue=repo['descripcion'])
            if nombre: repo['nombre'] = nombre
            if ruta_logs: repo['ruta_logs'] = ruta_logs
            if descripcion: repo['descripcion'] = descripcion
        else:
            messagebox.showerror('Error', 'No encontré ese repositorio. Fijate que el nombre esté bien escrito.')

    def on_save(self):
        # Actualizar config antes de guardar
        self.config['configuracion_general']['timeout_archivo'] = int(self.timeout_var.get())
        self.config['configuracion_general']['encoding'] = self.encoding_var.get()
        self.config['configuracion_general']['mostrar_timestamp'] = self.timestamp_var.get()
        self.save_config()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditor(root)
    root.mainloop()
