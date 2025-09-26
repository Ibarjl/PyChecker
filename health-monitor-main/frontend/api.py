from flask import Blueprint, jsonify
import os
import json

bp = Blueprint("api", __name__)

HEALTH_FILE = os.path.join("state", "health_status.json")

def load_health():
    """
    Carga el estado de salud actual desde health_status.json
    """
    if not os.path.exists(HEALTH_FILE):
        return {}
    with open(HEALTH_FILE, "r") as f:
        return json.load(f)

@bp.route("/health", methods=["GET"])
def get_health():
    """
    Endpoint para obtener el estado de los servicios
    """
    health = load_health()
    return jsonify(health)
