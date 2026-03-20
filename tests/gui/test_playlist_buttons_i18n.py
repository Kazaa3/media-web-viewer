import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

PLAYLIST_BUTTONS = [
    "pl_save", "pl_load", "pl_shuffle", "pl_clear", "pl_move_up", "pl_move_down"
]

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

def test_playlist_buttons_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'sequential-buffer-tab-trigger').click()
        time.sleep(0.2)
        for i18n_tag in PLAYLIST_BUTTONS:
            btn = driver.find_element(By.XPATH, f"//span[@data-i18n='{i18n_tag}']")
            assert btn.is_displayed(), f"Playlist button {i18n_tag} not visible"
    finally:
        teardown_browser(driver)
