"""
Venv Activation Unit Test (DE/EN)

DE:
Testet, ob das Python venv korrekt aktiviert und erkannt wird.
EN:
Tests if the Python venv is correctly activated and detected.

Usage:
    pytest tests/test_venv_activation.py
"""

import pytest
import sys
import os

class TestVenvActivation:
    def test_venv_active(self):
        """
        DE:
        Prüft, ob das venv-Environment aktiv ist (per sys.prefix und VIRTUAL_ENV).
        EN:
        Checks if the venv environment is active (via sys.prefix and VIRTUAL_ENV).
        """
        assert hasattr(sys, "prefix")
        assert "venv" in sys.prefix or os.environ.get("VIRTUAL_ENV")
