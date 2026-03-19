import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

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

def test_modals():
    driver = setup_browser()
    try:
        # Feature Status Modal
        driver.find_element(By.XPATH, "//button[@data-i18n='btn_features']").click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'feature-status-modal')
        assert modal.is_displayed(), "Feature Status modal not visible"
        driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleFeatureStatus')]").click()
        time.sleep(0.2)
        # Debug Flags Modal
        driver.find_element(By.XPATH, "//button[@data-i18n='nav_flags']").click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'debug-flags-modal')
        assert modal.is_displayed(), "Debug Flags modal not visible"
        driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleDebugMenu')]").click()
        time.sleep(0.2)
        # About/Imprint Modal
        driver.find_element(By.ID, 'imprint-link').click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'about-imprint-modal')
        assert modal.is_displayed(), "About/Imprint modal not visible"
        driver.find_element(By.XPATH, "//button[contains(@onclick, 'closeAboutImprint')]").click()
        time.sleep(0.2)
    finally:
        teardown_browser(driver)
