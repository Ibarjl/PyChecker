"""
Script para validar que la configuración YAML sea correcta
Útil para ejecutar antes de hacer deployment o cambios importantes
"""
import yaml
import sys

def validate_config(config_path="config.yaml"):
    """Valida que la configuración YAML sea estructuralmente correcta"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        # Validar estructura básica
        required_sections = ['servicios', 'general']
        for section in required_sections:
            if section not in config:
                print(f"❌ Sección requerida '{section}' no encontrada")
                return False
        # Validar plugins requeridos
        required_plugins = ['avionics', 'asset_api', 'runtime']
        for plugin in required_plugins:
            if plugin not in config['servicios']:
                print(f"⚠️  Plugin '{plugin}' no configurado")
        print("✅ Configuración YAML válida")
        return True
    except Exception as e:
        print(f"❌ Error validando configuración: {e}")
        return False

if __name__ == "__main__":
    valid = validate_config()
    sys.exit(0 if valid else 1)
