"""
Central Global Variables Test (DE/EN)

DE:
Testet, ob zentrale globale Variablen (z.B. Version, Name, Entwickler, Lizenz) im UI und Backend korrekt angezeigt werden.
EN:
Tests if central global variables (e.g. version, name, developer, license) are displayed correctly in UI and backend.

Usage:
    pytest tests/test_global_variables.py
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("http://localhost:8000")  # Adjust as needed
    yield driver
    driver.quit()

class TestGlobalVariables:
    def test_ui_global_variables(self, browser):
        """
        DE:
        Prüft, ob zentrale Variablen wie Version, Name, Entwickler, Lizenz im UI erscheinen.
        EN:
        Checks if central variables like version, name, developer, license appear in the UI.
        """
        # App title
        assert "Media Web Viewer" in browser.page_source
        # Version label
        version_label = browser.find_element(By.ID, "version-label").text
        assert version_label
        # Open imprint modal
        browser.find_element(By.ID, "imprint-link").click()
        body = browser.find_element(By.ID, "about-imprint-body").text
        assert "Media Web Viewer" in body
        assert "kazaa3" in body
        assert "GPL" in body
        assert "Version" in body or version_label
        browser.find_element(By.XPATH, "//button[@data-i18n='common_close']").click()

    def test_backend_global_variables(self):
        """
        DE:
        Prüft, ob zentrale Variablen im Backend korrekt zurückgegeben werden.
        EN:
        Checks if central variables are returned correctly from the backend.
        """
        # Example: call backend API (adjust as needed)
        import requests
        resp = requests.get("http://localhost:8000/api/imprint_info")  # Adjust endpoint
        data = resp.json()
        assert "version" in data
        assert "developer" in data
        assert data["developer"] == "kazaa3"
        assert "license" in data or "GPL" in data.get("license", "")
