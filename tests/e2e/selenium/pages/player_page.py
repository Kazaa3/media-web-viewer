from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class PlayerPage(BasePage):
    """Page Object für den Player-Tab."""
    
    MEDIA_ITEMS = (By.CSS_SELECTOR, "#media-list .media-item")
    
    def play_index(self, index):
        items = self.wait_for_element(self.MEDIA_ITEMS)
        self.driver.execute_script(f"document.querySelectorAll('#media-list .media-item')[{index}].scrollIntoView({{block: 'center'}});")
        time.sleep(1)
        self.driver.execute_script(f"document.querySelectorAll('#media-list .media-item')[{index}].click();")
        time.sleep(2)
