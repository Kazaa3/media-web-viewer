import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

# Subtab mapping: (id, i18n)
LIBRARY_SUBTABS = [
    ("lib-tab-btn-coverflow", "lib_tab_coverflow"),
    ("lib-tab-btn-grid", "lib_tab_grid"),
    ("lib-tab-btn-details", "lib_tab_details"),
]

OPTIONS_SUBTABS = [
    ("options-subtab-general", "options_subtab_general"),
    ("options-subtab-tools", "options_subtab_tools"),
    ("options-subtab-environment", "options_subtab_environment"),
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

def test_library_subtabs_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'coverflow-library-tab-trigger').click()
        time.sleep(0.2)
        for subtab_id, i18n_tag in LIBRARY_SUBTABS:
            subtab = driver.find_element(By.ID, subtab_id)
            assert subtab.is_displayed(), f"Library subtab {subtab_id} not visible"
            assert subtab.get_attribute("data-i18n") == i18n_tag, f"Library subtab {subtab_id} wrong i18n tag"
            subtab.click()
            time.sleep(0.15)
            assert subtab.is_displayed(), f"Library subtab {subtab_id} not visible after click"
    finally:
        teardown_browser(driver)

def test_options_subtabs_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'system-registry-tab-trigger').click()
        time.sleep(0.2)
        for subtab_id, i18n_tag in OPTIONS_SUBTABS:
            subtab = driver.find_element(By.ID, subtab_id)
            assert subtab.is_displayed(), f"Options subtab {subtab_id} not visible"
            assert subtab.get_attribute("data-i18n") == i18n_tag, f"Options subtab {subtab_id} wrong i18n tag"
            subtab.click()
            time.sleep(0.15)
            assert subtab.is_displayed(), f"Options subtab {subtab_id} not visible after click"
    finally:
        teardown_browser(driver)
