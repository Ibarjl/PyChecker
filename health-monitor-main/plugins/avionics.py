from .base_monitor import BaseMonitor
import re

class AvionicsMonitor(BaseMonitor):
    def __init__(self):
        super().__init__()
        self.errores_criticos = [
            r"GPS.*SIGNAL.*LOST",
            r"ALTITUDE.*SENSOR.*FAULT",
            r"NAVIGATION.*ERROR",
            r"ENGINE.*TEMPERATURE.*CRITICAL",
            r"EMERGENCY.*LANDING"
        ]
        self.errores_warning = [
            r"GPS.*ACCURACY.*LOW",
            r"BATTERY.*LOW",
            r"SIGNAL.*WEAK",
            r"ALTITUDE.*WARNING"
        ]
