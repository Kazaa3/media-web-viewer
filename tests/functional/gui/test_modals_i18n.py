import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

MODALS = [
    # (button_xpath, modal_id, close_xpath)
    ("//button[@data-i18n='btn_features']", "feature-status-modal", "//button[contains(@onclick, 'toggleFeatureStatus')]"),
    ("//button[@data-i18n='nav_flags']", "debug-flags-modal", "//button[contains(@onclick, 'toggleDebugMenu')]"),
    ("//button[@id='imprint-link']", "about-imprint-modal", "//button[contains(@onclick, 'closeAboutImprint')]"),
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

def test_modals_i18n():
    driver = setup_browser()
    try:
        for button_xpath, modal_id, close_xpath in MODALS:
            btn = driver.find_element(By.XPATH, button_xpath)
            assert btn.is_displayed(), f"Modal open button {button_xpath} not visible"
            btn.click()
            time.sleep(0.2)
            modal = driver.find_element(By.ID, modal_id)
            assert modal.is_displayed(), f"Modal {modal_id} not visible after open"
            # Check i18n attribute on open button if present
            i18n = btn.get_attribute("data-i18n")
            assert i18n is not None, f"Open button for modal {modal_id} missing data-i18n"
            # Close modal
            close_btn = driver.find_element(By.XPATH, close_xpath)
            close_btn.click()
            time.sleep(0.2)
    finally:
        teardown_browser(driver)
