###############################################################################
# Kategorie: Selenium Player Page
# Eingabewerte: WebDriver, Index
# Ausgabewerte: Player-Aktionen, UI-Interaktion
# Testdateien: player_page.py
# Kommentar: Page Object für Player-Tab im Selenium-Test.
###############################################################################
"""
Selenium Player Page Object (DE/EN)
===================================

DE:
Page Object für den Player-Tab im Selenium-Test.

EN:
Page object for the player tab in Selenium tests.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class PlayerPage(BasePage):
    """
    DE:
    Page Object für den Player-Tab.

    EN:
    Page object for the player tab.
    """
    MEDIA_ITEMS = (By.CSS_SELECTOR, "#media-list .media-item")

    def play_index(self, index):
        """
        DE:
        Spielt das Medien-Item am angegebenen Index ab.

        EN:
        Plays the media item at the given index.
        Args:
            index: Index des abzuspielenden Items.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        items = self.wait_for_element(self.MEDIA_ITEMS)
        self.driver.execute_script(f"document.querySelectorAll('#media-list .media-item')[{index}].scrollIntoView({{block: 'center'}});")
        time.sleep(1)
        self.driver.execute_script(f"document.querySelectorAll('#media-list .media-item')[{index}].click();")
        time.sleep(2)
