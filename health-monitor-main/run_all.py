import subprocess
import sys

main_proc = subprocess.Popen([sys.executable, "main.py"])
frontend_proc = subprocess.Popen([sys.executable, "-m", "frontend.app"])

try:
    main_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("Cerrando ambos procesos...")
    main_proc.terminate()
    frontend_proc.terminate()
