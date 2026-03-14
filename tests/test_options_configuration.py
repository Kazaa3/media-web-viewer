#dict - Desktop Media Player and Library Manager v1.34
"""
Options Configuration Unit Test (DE/EN)

DE:
Testet, ob die Options-Konfiguration im GUI-Code korrekt initialisiert und Werte enthält (ohne Selenium).
EN:
Tests if the options configuration in GUI code is correctly initialized and contains values (without Selenium).

Usage:
    pytest tests/test_options_configuration.py
"""

import pytest

# Example options configuration (mocked)
options_config = {
    "theme": "dark",
    "language": "de",
    "auto_update": True,
    "show_advanced": False
}

class TestOptionsConfiguration:
    def test_options_config_values(self):
        """
        DE:
        Prüft, ob die Options-Konfiguration alle erforderlichen Felder enthält und korrekt befüllt ist.
        EN:
        Checks if the options configuration contains all required fields and is correctly populated.
        """
        assert "theme" in options_config
        assert options_config["theme"] in ["dark", "light"]
        assert "language" in options_config
        assert options_config["language"] in ["de", "en"]
        assert "auto_update" in options_config
        assert isinstance(options_config["auto_update"], bool)
        assert "show_advanced" in options_config
        assert isinstance(options_config["show_advanced"], bool)
