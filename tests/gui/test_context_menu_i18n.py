import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

# IDs/classes for context menu
CONTEXT_MENU_CLASS = "custom-context-menu"
CONTEXT_MENU_ITEM_CLASS = "context-menu-item"

# Example: Right-click on a grid item or fallback to body

def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(APP_URL)
    return driver

def teardown_browser(driver):
    driver.quit()

def test_context_menu_items_i18n():
    driver = setup_browser()
    try:
        # Try to open context menu by right-clicking on body (fallback)
        webdriver.ActionChains(driver).context_click(driver.find_element(By.TAG_NAME, 'body')).perform()
        time.sleep(0.2)
        menu = driver.find_element(By.CLASS_NAME, CONTEXT_MENU_CLASS)
        assert menu.is_displayed(), "Context menu not visible"
        items = menu.find_elements(By.CLASS_NAME, CONTEXT_MENU_ITEM_CLASS)
        for item in items:
            i18n = item.get_attribute('data-i18n')
            assert i18n is not None, "Context menu item missing data-i18n"
    finally:
        teardown_browser(driver)
