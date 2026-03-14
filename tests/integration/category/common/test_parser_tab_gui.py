import pytest
pytest.importorskip("selenium")
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Annahme: Die App läuft lokal auf http://localhost:8000

def test_parser_tab_elements(browser):
    browser.get("http://localhost:8000")
    parser_tab = browser.find_element(By.ID, "parserTab")
    assert parser_tab is not None, "Parser-Tab fehlt im UI!"

    # Prüfe, ob die neuen Parser als Elemente gelistet sind
    parser_names = [
        "ffprobe_parser",
        "mutagen_parser",
        "mediainfo_parser",
        "m3u8_parser",
        "iso_parser"
    ]
    for name in parser_names:
        elem = browser.find_element(By.XPATH, f"//div[@id='parserTab']//span[contains(text(), '{name}')]" )
        assert elem is not None, f"Parser {name} fehlt im Parser-Tab!"
