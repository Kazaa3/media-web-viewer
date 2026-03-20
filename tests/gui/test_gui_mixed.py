import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

def test_tab_and_modal_interaction():
    driver = setup_browser()
    try:
        # Test switching tabs
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
            time.sleep(0.1)
            assert tab.is_displayed(), f"Tab {tab_id} not visible after click"
        # Test modals
        driver.find_element(By.XPATH, "//button[@data-i18n='btn_features']").click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'feature-status-modal')
        assert modal.is_displayed(), "Feature Status modal not visible"
        driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleFeatureStatus')]").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[@data-i18n='nav_flags']").click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'debug-flags-modal')
        assert modal.is_displayed(), "Debug Flags modal not visible"
        driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleDebugMenu')]").click()
        time.sleep(0.2)
        driver.find_element(By.ID, 'imprint-link').click()
        time.sleep(0.2)
        modal = driver.find_element(By.ID, 'about-imprint-modal')
        assert modal.is_displayed(), "About/Imprint modal not visible"
    finally:
        teardown_browser(driver)

def test_options_and_reporting_subtabs():
    driver = setup_browser()
    try:
        # Options subtabs
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
        # Reporting subtabs
        driver.find_element(By.ID, 'reporting-dashboard-tab-trigger').click()
        time.sleep(0.2)
        for subtab_id in [
            'reporting-subtab-overview',
            'reporting-subtab-logs',
            'reporting-subtab-export',
        ]:
            subtab = driver.find_element(By.ID, subtab_id)
            subtab.click()
            time.sleep(0.2)
            assert subtab.is_displayed(), f"Reporting sub-tab {subtab_id} not visible after click"
    finally:
        teardown_browser(driver)
