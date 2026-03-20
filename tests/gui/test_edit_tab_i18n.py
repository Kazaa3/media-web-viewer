import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

EDIT_I18N = [
    ("edit_title", "h2"),
    ("edit_subtitle", "p"),
    ("edit_form_title", "h3"),
    ("edit_btn_rename", "button"),
]

PLACEHOLDER_I18N = [
    ("edit_search_library_placeholder", "edit-search")
]

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

def test_edit_tab_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'crud-metadata-tab-trigger').click()
        time.sleep(0.2)
        for i18n_tag, tag in EDIT_I18N:
            el = driver.find_element(By.XPATH, f"//{tag}[@data-i18n='{i18n_tag}']")
            assert el.is_displayed(), f"Edit tab element {i18n_tag} not visible"
        for i18n_tag, input_id in PLACEHOLDER_I18N:
            inp = driver.find_element(By.ID, input_id)
            ph = inp.get_attribute('placeholder')
            assert ph is not None and len(ph) > 0, f"Edit tab input {input_id} missing placeholder"
    finally:
        teardown_browser(driver)
