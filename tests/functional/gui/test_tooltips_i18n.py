import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

TOOLTIP_BUTTONS = [
    ("fb-refresh-btn", "Refresh"),
]

def setup_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(APP_URL)
    return driver

def teardown_browser(driver):
    driver.quit()

def test_tooltip_buttons():
    driver = setup_browser()
    try:
        for btn_id, expected_title in TOOLTIP_BUTTONS:
            btn = driver.find_element(By.ID, btn_id)
            title = btn.get_attribute('title')
            assert title is not None and len(title) > 0, f"Button {btn_id} missing title attribute"
    finally:
        teardown_browser(driver)
