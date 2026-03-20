import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

APP_URL = "http://localhost:8000"

FILTER_CHIPS = [
    "filter_all", "filter_audio", "filter_video", "filter_images", "cat_documents", "cat_ebooks", "cat_film", "cat_serie", "cat_album", "cat_soundtrack", "cat_playlist", "cat_podcast", "cat_compilation", "cat_single", "cat_klassik", "cat_abbild", "cat_spiel"
]

SUBCATEGORY_OPTIONS = [
    "filter_sub_all", "filter_audiobooks", "filter_podcasts", "filter_albums", "filter_soundtracks", "filter_playlists", "filter_others"
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

def test_library_filter_chips_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'coverflow-library-tab-trigger').click()
        time.sleep(0.2)
        for i18n_tag in FILTER_CHIPS:
            chip = driver.find_element(By.XPATH, f"//button[@data-i18n='{i18n_tag}']")
            assert chip.is_displayed(), f"Filter chip {i18n_tag} not visible"
    finally:
        teardown_browser(driver)

def test_library_subcategory_select_i18n():
    driver = setup_browser()
    try:
        driver.find_element(By.ID, 'coverflow-library-tab-trigger').click()
        time.sleep(0.2)
        select = driver.find_element(By.ID, 'library-subcategory-filter')
        options = select.find_elements(By.TAG_NAME, 'option')
        found_tags = [opt.get_attribute('data-i18n') for opt in options]
        for i18n_tag in SUBCATEGORY_OPTIONS:
            assert i18n_tag in found_tags, f"Subcategory option {i18n_tag} missing"
    finally:
        teardown_browser(driver)
