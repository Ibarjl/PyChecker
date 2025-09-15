<<<<<<< HEAD
"""
Aplicación Flask mejorada con mejor manejo de imports y rutas
"""

from flask import Flask, render_template, jsonify
import os

# Import mejorado - más explícito sobre el módulo
from . import api  # Import relativo explícito

# Configuración más robusta de Flask
app = Flask(__name__)

# Configurar ruta de templates de manera más robusta
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/")
def index():
    """
    Página principal del dashboard
    """
    status = api.get_status()
    system_info = api.get_system_info()
    return render_template("index.html", status=status, system_info=system_info)

@app.route("/api/status")
def api_status():
    """
    Endpoint JSON para obtener solo el estado de los servicios
    Útil para actualizaciones vía AJAX
    """
    return jsonify(api.get_status())

@app.route("/api/system")
def api_system():
    """
    Endpoint para información del sistema de monitoreo
    """
    return jsonify(api.get_system_info())

if __name__ == "__main__":
    print("🌐 Iniciando Health Monitor Dashboard...")
    print("📍 Accede a: http://127.0.0.1:5000/")
    print("🔄 API Status: http://127.0.0.1:5000/api/status")
    app.run(host="0.0.0.0", port=5000, debug=True)
=======
from flask import Flask, render_template
from api import get_status

app = Flask(__name__)

@app.route("/")
def index():
    status = get_status()
    return render_template("index.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> rama_ibar
