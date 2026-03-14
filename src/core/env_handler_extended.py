#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# env_handler_extended.py - Environment Handler (Batch & Extended)

Dieses Modul erweitert die Validierung und das Management der Projektumgebung um Batch- und Pip-Installationsfunktionen.

Features:
- Batch-Validierung von Python-Paketen und System-Binaries
- Automatisierte Pip-Installation fehlender Pakete
- Erweiterte Logging- und Fehlerbehandlung
- Unterstützung für CI/CD, venv, Conda
- Nutzung als CLI-Tool für Umgebungschecks

Verwendung:
- Für Desktop- und CI/CD-Integrationen, nicht für Browser-Frontend.

"""

import sys
import os
import subprocess
import logging
from typing import List

logger = logging.getLogger("env_handler_extended")

def batch_validate_and_install(packages: List[str]) -> None:
    """
    Prüft, ob die angegebenen Python-Pakete installiert sind.
    Installiert fehlende Pakete automatisch via pip.
    """
    for pkg in packages:
        try:
            __import__(pkg)
            logger.info(f"Paket '{pkg}' ist installiert.")
        except ImportError:
            logger.warning(f"Paket '{pkg}' fehlt. Installation wird versucht...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)
            logger.info(f"Paket '{pkg}' wurde installiert.")

if __name__ == "__main__":
    # Beispiel: Batch-Validierung und Installation
    batch_validate_and_install(["eel", "bottle", "mutagen", "pymediainfo", "gevent", "psutil", "m3u8"])
