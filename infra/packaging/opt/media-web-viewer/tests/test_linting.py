# Kategorie: Static Analysis (Linting & Typing)
# Eingabewerte: Source Code (.py)
# Ausgabewerte: Linting/Typing Ergebnisse
# Testdateien: main.py, db.py, models.py, parsers/*.py, web/*.py
# Kommentar: Führt Flake8 und Mypy zur Qualitätssicherung aus.
"""
Final walkthrough of the linting and type safety integration.
Confirms 100% PEP8 and mypy compliance across the core codebase.
"""

import subprocess
from pathlib import Path
import pytest


def test_flake8_linting():
    """Führt Flake8 Linting über das Projekt aus."""
    root_dir = Path(__file__).parent.parent

    # Prüfen ob flake8 installiert ist
    try:
        subprocess.run(["flake8", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("flake8 ist nicht installiert.")

    result = subprocess.run(
        ["flake8", "."],
        cwd=str(root_dir),
        capture_output=True,
        text=True
    )

    # Wir erlauben vorerst Warnings, aber loggen sie
    if result.returncode != 0:
        # Falls es kritische Fehler gibt, schlägt der Test fehl
        # Wir können hier spezifische Error-Codes filtern falls nötig
        # pytest.fail(f"Flake8 linting failed:\n{result.stdout}")
        print(f"\n[Flake8 Warnings/Errors]:\n{result.stdout}")
        # Optional: Test fehlschlagen lassen wenn gewünscht
        assert result.returncode == 0


def test_mypy_typing():
    """Führt Mypy Typ-Prüfung über das Projekt aus."""
    root_dir = Path(__file__).parent.parent

    # Prüfen ob mypy installiert ist
    try:
        subprocess.run(["mypy", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("mypy ist nicht installiert.")

    result = subprocess.run(
        ["mypy", "."],
        cwd=str(root_dir),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"\n[Mypy Typing Issues]:\n{result.stdout}")
        assert result.returncode == 0
