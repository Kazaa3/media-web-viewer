"""
Logbuch Feature Modal Content Test (DE/EN)

DE:
Testet, ob der Feature-Modal im Logbuch korrekten Inhalt anzeigt (Kategorie, Status, Titel, Zusammenfassung).
EN:
Tests if the logbuch feature modal displays correct content (category, status, title, summary).

Usage:
    pytest tests/test_logbuch_feature_modal.py
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

class TestLogbuchFeatureModal:
    def test_logbuch_feature_modal_content(self, browser):
        """
        DE:
        Öffnet den Feature-Modal im Logbuch und prüft, ob Kategorie, Status, Titel und Zusammenfassung angezeigt werden.
        EN:
        Opens the logbuch feature modal and checks if category, status, title, and summary are displayed.
        """
        # Open logbuch feature modal (example selector, adjust as needed)
        browser.find_element(By.ID, "logbuch-feature-link").click()
        modal = browser.find_element(By.ID, "logbuch-feature-modal")
        assert modal.is_displayed()
        body = browser.find_element(By.ID, "logbuch-feature-body")
        text = body.text
        assert "Feature" in text         # Category
        assert "COMPLETED" in text or "ACTIVE" in text  # Status
        assert "Modal" in text          # Title
        assert "Summary" in text or "Zusammenfassung" in text  # Summary
        # Close modal
        browser.find_element(By.XPATH, "//button[@data-i18n='common_close']").click()
        assert not modal.is_displayed()
