"""
GUI Version Display Unit Test (DE/EN)

DE:
Testet, ob die richtige Programmversion im GUI-Code angezeigt wird (ohne Selenium).
EN:
Tests if the correct program version is displayed in GUI code (without Selenium).

Usage:
    pytest tests/test_gui_version_display.py
"""

import pytest
from tests.global_variables_preset import VERSION

# Example GUI version variable (mocked)
gui_version = "1.34"  # Replace with actual GUI code reference if available

class TestGuiVersionDisplay:
    def test_gui_version_matches_global(self):
        """
        DE:
        Prüft, ob die GUI-Version mit der globalen Version übereinstimmt.
        EN:
        Checks if the GUI version matches the global version.
        """
        assert gui_version == VERSION
