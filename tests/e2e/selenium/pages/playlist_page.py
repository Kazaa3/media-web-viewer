from .base_page import BasePage
from selenium.webdriver.common.by import By

class PlaylistPage(BasePage):
    """Page Object für den Playlist-Tab."""
    
    # Locators
    TAB_BUTTON = (By.XPATH, "//button[contains(@onclick, \"switchTab('playlist'\")]")
    PLAYLIST_LIST = (By.ID, "playlist-list")
    ITEM_SELECTOR = (By.CSS_SELECTOR, "#playlist-list .media-item")
    HEADER_MOVE_UP = (By.ID, "pl-move-up")
    HEADER_MOVE_DOWN = (By.ID, "pl-move-down")
    
    def switch_to(self):
        self.click(self.TAB_BUTTON)
        self.wait_for_element(self.PLAYLIST_LIST)

    def get_items(self):
        return self.driver.find_elements(*self.ITEM_SELECTOR)

    def get_item_names(self):
        items = self.get_items()
        return [it.find_element(By.TAG_NAME, "strong").text for it in items]

    def move_current_up(self):
        self.click(self.HEADER_MOVE_UP)

    def move_current_down(self):
        self.click(self.HEADER_MOVE_DOWN)

    def get_playing_item_index(self):
        items = self.get_items()
        for idx, item in enumerate(items):
            if "playing" in item.get_attribute("class"):
                return idx
        return -1
