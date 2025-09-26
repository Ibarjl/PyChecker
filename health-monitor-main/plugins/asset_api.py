from .base_monitor import BaseMonitor
import re

class AssetAPIMonitor(BaseMonitor):
    def __init__(self):
        super().__init__()
        self.errores_criticos = [
            r"DATABASE.*CONNECTION.*FAILED",
            r"HTTP.*5\d\d",
            r"AUTHENTICATION.*FAILED", 
            r"MEMORY.*LEAK.*DETECTED",
            r"TIMEOUT.*DATABASE"
        ]
        self.errores_warning = [
            r"HTTP.*4\d\d",
            r"SLOW.*QUERY",
            r"RATE.*LIMIT.*EXCEEDED",
            r"MEMORY.*USAGE.*HIGH"
        ]
