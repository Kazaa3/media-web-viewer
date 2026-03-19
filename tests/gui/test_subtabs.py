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

def test_options_subtabs():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'system-registry-tab-trigger').click()
        time.sleep(0.2)
        for subtab_id in [
            'options-subtab-general',
            'options-subtab-tools',
            'options-subtab-environment',
        ]:
            subtab = driver.find_element(By.ID, subtab_id)
            subtab.click()
            time.sleep(0.2)
            assert subtab.is_displayed(), f"Options sub-tab {subtab_id} not visible after click"
    finally:
        teardown_browser(driver)

def test_reporting_subtabs():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'reporting-dashboard-tab-trigger').click()
        time.sleep(0.2)
        select = driver.find_element(By.ID, 'reporting-view-select')
        options = select.find_elements(By.TAG_NAME, 'option')
        for opt in options:
            select.click()
            opt.click()
            time.sleep(0.2)
            assert opt.is_displayed(), f"Reporting sub-tab {opt.get_attribute('value')} not visible after click"
    finally:
        teardown_browser(driver)
