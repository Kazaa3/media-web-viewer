#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI / CLI Utilities
# Eingabewerte: Progress / Totals
# Ausgabewerte: Dynamische Statusleiste im Terminal
# Testdateien: Keine
# KOMMENTAR: Hilfsklasse für Fortschrittsanzeigen in Terminal-Skripten.

"""
KATEGORIE: UI / CLI Utilities
ZWECK: Stellt eine wiederverwendbare Statusleiste für Konsolenanwendungen bereit.
VERWENDUNG: 
    from status_bar_utils import StatusBar
    with StatusBar("Lade Daten", total=100) as sb:
        for i in range(100):
            sb.update(i+1)
"""

import sys
import time

class StatusBar:
    def __init__(self, message, total=100, width=40):
        self.message = message
        self.total = total
        self.width = width
        self.start_time = time.time()
        self.current = 0

    def __enter__(self):
        self.update(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print() # New line after completion

    def update(self, current, status_text=""):
        self.current = current
        percent = (current / self.total) * 100
        filled = int(self.width * current // self.total)
        bar = '█' * filled + '-' * (self.width - filled)
        
        # Build status string
        sys.stdout.write(f'\r{self.message}: |{bar}| {percent:3.0f}% {status_text}')
        sys.stdout.flush()

if __name__ == "__main__":
    # Demo
    print("Demo der Statusleiste:")
    with StatusBar("Verarbeitung läuft", total=50) as sb:
        for i in range(51):
            time.sleep(0.05)
            sb.update(i, f"(Schritt {i}/50)")
