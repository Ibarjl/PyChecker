import subprocess

def reinicio_simple():
    """
    Reinicio básico de los servicios monitoreados.
    Intenta reiniciar contenedores Docker llamados 'api_service', 'background_jobs' y 'ejemplo_app'.
    Si no hay Docker, solo muestra el mensaje.
    """
    print("[REINICIO] Ejecutando reinicio básico de los servicios...")
    servicios = ["api_service", "background_jobs", "ejemplo_app"]
    for servicio in servicios:
        try:
            print(f"[REINICIO] Reiniciando contenedor Docker: {servicio}")
            resultado = subprocess.run(["docker", "restart", servicio], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"[OK] {servicio} reiniciado correctamente.")
            else:
                print(f"[ERROR] No se pudo reiniciar {servicio}: {resultado.stderr.strip()}")
        except Exception as e:
            print(f"[ERROR] No se pudo ejecutar el reinicio de {servicio}: {e}")
    print("[REINICIO] Proceso básico finalizado.")
    return True
