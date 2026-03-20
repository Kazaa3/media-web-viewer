import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Adjust the URL as needed for your test environment
APP_URL = "http://localhost:8000"  # or the correct port

def setup_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(APP_URL)
    return driver

def teardown_browser(driver):
    driver.quit()

def test_main_tabs():
    driver = setup_browser()
    try:
        tab_ids = [
            'active-queue-tab-trigger',
            'coverflow-library-tab-trigger',
            'indexed-sqlite-repository-tab-trigger',
            'filesystem-crawler-tab-trigger',
            'crud-metadata-tab-trigger',
            'system-registry-tab-trigger',
            'chain-config-tab-trigger',
            'telemetry-inspector-tab-trigger',
            'qa-validation-tab-trigger',
            'reporting-dashboard-tab-trigger',
            'documentation-journal-tab-trigger',
            'sequential-buffer-tab-trigger',
            'media-orchestrator-tab-trigger',
        ]
        for tab_id in tab_ids:
            tab = driver.find_element(By.ID, tab_id)
            tab.click()
            time.sleep(0.2)
            assert tab.is_displayed(), f"Tab {tab_id} not visible after click"
    finally:
        teardown_browser(driver)
