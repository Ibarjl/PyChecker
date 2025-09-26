from .base_monitor import BaseMonitor

class RuntimeMonitor(BaseMonitor):
    def __init__(self):
        super().__init__()
        self.errores_criticos = [
            r"OUT.*OF.*MEMORY",
            r"MEMORY.*LEAK",
            r"STACK.*OVERFLOW",
            r"SEGMENTATION.*FAULT",
            r"DEADLOCK.*DETECTED"
        ]
        self.errores_warning = [
            r"MEMORY.*USAGE.*HIGH",
            r"CPU.*USAGE.*HIGH",
            r"DISK.*SPACE.*LOW",
            r"THREAD.*CONTENTION"
        ]