###############################################################################
# Kategorie: Selenium Playlist Page
# Eingabewerte: WebDriver, Playlist-Tab
# Ausgabewerte: Playlist-Aktionen, UI-Interaktion
# Testdateien: playlist_page.py
# Kommentar: Page Object für Playlist-Tab im Selenium-Test.
###############################################################################
"""
Selenium Playlist Page Object (DE/EN)
=====================================

DE:
Page Object für den Playlist-Tab im Selenium-Test.

EN:
Page object for the playlist tab in Selenium tests.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

from .base_page import BasePage
from selenium.webdriver.common.by import By

class PlaylistPage(BasePage):
    """
    DE:
    Page Object für den Playlist-Tab.

    EN:
    Page object for the playlist tab.
    """
    # Locators
    TAB_BUTTON = (By.XPATH, "//button[contains(@onclick, \"switchTab('playlist'\")]")
    PLAYLIST_LIST = (By.ID, "playlist-list")
    ITEM_SELECTOR = (By.CSS_SELECTOR, "#playlist-list .media-item")
    HEADER_MOVE_UP = (By.ID, "pl-move-up")
    HEADER_MOVE_DOWN = (By.ID, "pl-move-down")

    def switch_to(self):
        """
        DE:
        Wechselt zum Playlist-Tab.

        EN:
        Switches to the playlist tab.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        self.click(self.TAB_BUTTON)
        self.wait_for_element(self.PLAYLIST_LIST)

    def get_items(self):
        """
        DE:
        Gibt alle Playlist-Items zurück.

        EN:
        Returns all playlist items.
        Returns:
            list: Liste der WebElement-Items.
        """
        return self.driver.find_elements(*self.ITEM_SELECTOR)

    def get_item_names(self):
        """
        DE:
        Gibt die Namen aller Playlist-Items zurück.

        EN:
        Returns the names of all playlist items.
        Returns:
            list: Namen der Items.
        """
        items = self.get_items()
        return [it.find_element(By.TAG_NAME, "strong").text for it in items]

    def move_current_up(self):
        """
        DE:
        Verschiebt das aktuelle Item nach oben.

        EN:
        Moves the current item up.
        Returns:
            Keine.
        """
        self.click(self.HEADER_MOVE_UP)

    def move_current_down(self):
        """
        DE:
        Verschiebt das aktuelle Item nach unten.

        EN:
        Moves the current item down.
        Returns:
            Keine.
        """
        self.click(self.HEADER_MOVE_DOWN)

    def get_playing_item_index(self):
        """
        DE:
        Gibt den Index des aktuell spielenden Items zurück.

        EN:
        Returns the index of the currently playing item.
        Returns:
            int: Index des spielenden Items oder -1.
        """
        items = self.get_items()
        for idx, item in enumerate(items):
            if "playing" in item.get_attribute("class"):
                return idx
        return -1
