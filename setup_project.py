#!/usr/bin/env python3
"""
Script de inicialización para Health Monitor
Configura el entorno de desarrollo automáticamente
"""
import os
import subprocess
import sys

def create_directories():
    """Crea directorios necesarios que no están en git"""
    directories = ['logs', 'logs/backups']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directorio creado: {directory}")

def install_dependencies():
    """Instala dependencias de Python"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        return False
    return True

def validate_installation():
    """Valida que todo esté instalado correctamente"""
    try:
        # Validar imports principales
        import yaml
        import flask
        import watchdog
        print("✅ Todas las librerías principales disponibles")
        # Validar configuración
        from utils.validate_config import validate_config
        if validate_config():
            print("✅ Configuración YAML válida")
        else:
            print("⚠️  Problemas en configuración YAML")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def main():
    print("🚀 Configurando Health Monitor...")
    create_directories()
    if not install_dependencies():
        print("❌ Falló la instalación de dependencias")
        return
    if validate_installation():
        print("\n✅ ¡Health Monitor configurado exitosamente!")
        print("\nPróximos pasos:")
        print("1. Ejecutar: python main.py")
        print("2. (Opcional) Frontend: cd frontend && python app.py")
    else:
        print("\n⚠️  Configuración completada con advertencias")

if __name__ == "__main__":
    main()
