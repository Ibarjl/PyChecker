import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/monitor_config.json')

class ConfigEditor:
    def __init__(self, master):
        self.master = master
        self.master.title('Editor de Configuración (configurá a tu gusto)')
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
        # Mostrar y editar timeout_archivo
        tk.Label(self.master, text='Tiempo de espera (segundos):').grid(row=0, column=0)
        self.timeout_var = tk.StringVar(value=str(self.config['configuracion_general']['timeout_archivo']))
        tk.Entry(self.master, textvariable=self.timeout_var).grid(row=0, column=1)

        # Mostrar y editar encoding
        tk.Label(self.master, text='Codificación (encoding):').grid(row=1, column=0)
        self.encoding_var = tk.StringVar(value=self.config['configuracion_general']['encoding'])
        tk.Entry(self.master, textvariable=self.encoding_var).grid(row=1, column=1)

        # Mostrar y editar mostrar_timestamp
        tk.Label(self.master, text='¿Querés mostrar la hora en los logs?').grid(row=2, column=0)
        self.timestamp_var = tk.BooleanVar(value=self.config['configuracion_general']['mostrar_timestamp'])
        tk.Checkbutton(self.master, variable=self.timestamp_var).grid(row=2, column=1)

        # Botón para editar repositorios
        tk.Button(self.master, text='Editá los repositorios', command=self.edit_repos).grid(row=3, column=0, columnspan=2)

        # Botón para guardar
        tk.Button(self.master, text='Guardá los cambios', command=self.on_save).grid(row=4, column=0, columnspan=2)

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
