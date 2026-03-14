"""
Console Execution Test (DE/EN)

DE:
Testet, ob ein Konsolenbefehl korrekt ausgeführt wird und die erwartete Ausgabe liefert.
EN:
Tests if a console command executes correctly and returns the expected output.

Usage:
    pytest tests/test_console_execution.py
"""

import pytest
import subprocess

class TestConsoleExecution:
    def test_echo_command(self):
        """
        DE:
        Führt den 'echo'-Befehl aus und prüft, ob die Ausgabe korrekt ist.
        EN:
        Executes the 'echo' command and checks if the output is correct.
        """
        result = subprocess.run(["echo", "Media Web Viewer"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Media Web Viewer" in result.stdout

    def test_python_version(self):
        """
        DE:
        Führt 'python --version' aus und prüft, ob die Ausgabe die Python-Version enthält.
        EN:
        Executes 'python --version' and checks if the output contains the Python version.
        """
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Python" in result.stdout or result.stderr
