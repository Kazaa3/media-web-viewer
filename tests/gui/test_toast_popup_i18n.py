import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

TOAST_CONTAINER_ID = "toast-container"
TOAST_CLASS = "toast"

# This test assumes a toast can be triggered via JS for test purposes

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

def test_toast_popup_i18n():
    driver = setup_browser()
    try:
        # Trigger a toast via JS (example: window.showTestToast)
        driver.execute_script("if(window.showTestToast){window.showTestToast('test_i18n_key');}")
        time.sleep(0.5)
        container = driver.find_element(By.ID, TOAST_CONTAINER_ID)
        assert container.is_displayed(), "Toast container not visible"
        toasts = container.find_elements(By.CLASS_NAME, TOAST_CLASS)
        for toast in toasts:
            i18n = toast.get_attribute('data-i18n')
            assert i18n is not None, "Toast popup missing data-i18n"
    finally:
        teardown_browser(driver)
