"""
Impressum/Imprint Modal Content Test (DE/EN)

DE:
Testet, ob der Impressum/Imprint-Modal korrekten Inhalt anzeigt (Version, Entwickler, Lizenz).
EN:
Tests if the Impressum/Imprint modal displays correct content (version, developer, license).

Usage:
    pytest tests/test_imprint_modal.py
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
    driver.get("http://localhost:{port}")  # Adjust as needed
    yield driver
    driver.quit()

class TestImprintModal:
    def test_imprint_modal_content(self, browser):
        """
        DE:
        Öffnet den Impressum-Modal und prüft, ob Version, Entwickler, Lizenz, Name angezeigt werden.
        EN:
        Opens the imprint modal and checks if version, developer, license, and name are displayed.
        """
        # Open modal
        browser.find_element(By.ID, "imprint-link").click()
        modal = browser.find_element(By.ID, "about-imprint-modal")
        assert modal.is_displayed()
        body = browser.find_element(By.ID, "about-imprint-body")
        text = body.text
        assert "Media Web Viewer" in text  # Name
        assert "kazaa3" in text            # Developer
        assert "GPL" in text               # License
        assert "Version" in text or browser.find_element(By.ID, "version-label").text  # Version
        # Close modal
        browser.find_element(By.XPATH, "//button[@data-i18n='common_close']").click()
        assert not modal.is_displayed()
