import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

# Mapping of tab IDs to their i18n nav tags
TAB_I18N = [
    ("active-queue-tab-trigger", "nav_player"),
    ("coverflow-library-tab-trigger", "nav_library"),
    ("indexed-sqlite-repository-tab-trigger", "nav_item"),
    ("filesystem-crawler-tab-trigger", "nav_file"),
    ("crud-metadata-tab-trigger", "nav_edit"),
    ("system-registry-tab-trigger", "nav_options"),
    ("chain-config-tab-trigger", "nav_parser"),
    ("telemetry-inspector-tab-trigger", "nav_debug"),
    ("qa-validation-tab-trigger", "nav_tests"),
    ("reporting-dashboard-tab-trigger", "nav_reporting"),
    ("documentation-journal-tab-trigger", "nav_logbook"),
    ("sequential-buffer-tab-trigger", "nav_playlist"),
    ("media-orchestrator-tab-trigger", "nav_video"),
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

def test_all_tabs_with_i18n():
    driver = setup_browser()
    try:
        for tab_id, nav_tag in TAB_I18N:
            tab = driver.find_element(By.ID, tab_id)
            assert tab.is_displayed(), f"Tab {tab_id} is not visible"
            # Check i18n attribute
            i18n = tab.get_attribute("data-i18n")
            assert i18n == nav_tag, f"Tab {tab_id} has wrong i18n tag: {i18n} != {nav_tag}"
            tab.click()
            time.sleep(0.15)
            assert tab.is_displayed(), f"Tab {tab_id} not visible after click"
    finally:
        teardown_browser(driver)
