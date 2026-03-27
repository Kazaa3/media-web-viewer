# =============================================================================
# Kategorie: Selenium Base Page
# Eingabewerte: WebDriver, Locator
# Ausgabewerte: Element-Objekte, Screenshots
# Testdateien: base_page.py
# Kommentar: Basis-Klasse für Page Objects im Selenium-Test.
# =============================================================================
"""
Selenium Base Page Object (DE/EN)
=================================

DE:
Basis-Klasse für Page Objects im Selenium-Test.

EN:
Base class for page objects in Selenium tests.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class BasePage:
    """
    DE:
    Basis-Klasse für alle Page Objects.

    EN:
    Base class for all page objects.
    """
    def __init__(self, driver):
        """
        DE:
        Initialisiert den WebDriver und Timeout.

        EN:
        Initializes WebDriver and timeout.
        Args:
            driver: Selenium WebDriver-Instanz.
        """
        self.driver = driver
        self.timeout = 30

    def wait_for_element(self, locator):
        """
        DE:
        Wartet auf das Vorhandensein eines Elements.

        EN:
        Waits for presence of an element.
        Args:
            locator: Selenium-Locator-Tuple.
        Returns:
            WebElement: Gefundenes Element.
        Raises:
            TimeoutException: Wenn Element nicht gefunden.
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click_element(self, locator):
        """
        DE:
        Wartet auf Klickbarkeit und klickt das Element.

        EN:
        Waits for element to be clickable and clicks it.
        Args:
            locator: Selenium-Locator-Tuple.
        Returns:
            Keine.
        Raises:
            TimeoutException: Wenn Element nicht klickbar.
        """
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def get_text(self, locator):
        """
        DE:
        Gibt den Text eines Elements zurück.

        EN:
        Returns the text of an element.
        Args:
            locator: Selenium-Locator-Tuple.
        Returns:
            str: Text des Elements.
        """
        element = self.wait_for_element(locator)
        return element.text

    def take_screenshot(self, name):
        """
        DE:
        Speichert einen Screenshot im selenium_artifacts-Verzeichnis.

        EN:
        Saves a screenshot in the selenium_artifacts directory.
        Args:
            name: Dateiname für den Screenshot.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        artifact_dir = os.path.join(os.path.dirname(__file__), '../../..', "selenium_artifacts")
        if not os.path.exists(artifact_dir):
            os.makedirs(artifact_dir)
        path = os.path.join(artifact_dir, f"{name}.png")
        self.driver.save_screenshot(path)
        print(f"Screenshot saved to: {path}")
