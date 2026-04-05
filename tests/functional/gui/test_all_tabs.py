import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

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

def test_all_tabs_visible_and_clickable():
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
            assert tab.is_displayed(), f"Tab {tab_id} is not visible"
            tab.click()
            time.sleep(0.15)
            assert tab.is_displayed(), f"Tab {tab_id} not visible after click"
    finally:
        teardown_browser(driver)
