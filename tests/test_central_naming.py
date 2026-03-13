"""
Central Naming Convention Test (DE/EN)

DE:
Testet, ob zentrale Namenskonventionen (z.B. Media Web Viewer, logbuch-feature-modal, about-imprint-modal) im UI und Code korrekt verwendet werden.
EN:
Tests if central naming conventions (e.g. Media Web Viewer, logbuch-feature-modal, about-imprint-modal) are used correctly in UI and code.

Usage:
    pytest tests/test_central_naming.py
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

class TestCentralNaming:
    def test_app_title_and_modals(self, browser):
        """
        DE:
        Prüft, ob zentrale Namen wie 'Media Web Viewer', 'about-imprint-modal', 'logbuch-feature-modal' korrekt im UI erscheinen.
        EN:
        Checks if central names like 'Media Web Viewer', 'about-imprint-modal', 'logbuch-feature-modal' appear correctly in the UI.
        """
        # App title
        assert "Media Web Viewer" in browser.page_source
        # Imprint modal
        browser.find_element(By.ID, "imprint-link").click()
        assert browser.find_element(By.ID, "about-imprint-modal").is_displayed()
        browser.find_element(By.XPATH, "//button[@data-i18n='common_close']").click()
        # Logbuch feature modal (example selector, adjust as needed)
        browser.find_element(By.ID, "logbuch-feature-link").click()
        assert browser.find_element(By.ID, "logbuch-feature-modal").is_displayed()
        browser.find_element(By.XPATH, "//button[@data-i18n='common_close']").click()
