#!/usr/bin/env python3
"""
scripts/test_gui_structure_selenium.py

Kombinierte Selenium- und Strukturtests für die GUI:
- Öffnet app.html im Browser (lokal oder via Server)
- Prüft mit Selenium, ob alle Haupt-Tabs und UI-Elemente sichtbar sind
- Nutzt zusätzlich gui_validator.py, um die DIV-/Tag-Struktur zu prüfen
- Gibt eine kombinierte Übersicht für CI/Debugging
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess
import sys
from pathlib import Path

def run_gui_validator(html_path):
    result = subprocess.run([sys.executable, 'scripts/gui_validator.py', html_path], capture_output=True, text=True)
    print("\n[gui_validator.py Output]")
    print(result.stdout)
    return result.returncode == 0

def test_tabs_and_elements(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        # Prüfe Haupt-Tabs
        for tab_id in ["tab-options", "tab-library", "tab-player"]:
            tab = driver.find_element(By.ID, tab_id)
            assert tab.is_displayed(), f"Tab {tab_id} nicht sichtbar!"
        # Prüfe ISBN-Scan-Button
        scan_btn = driver.find_element(By.ID, "scan-isbn-btn")
        assert scan_btn.is_displayed(), "Scan ISBN Button nicht sichtbar!"
        print("[Selenium] Alle Haupt-Tabs und Scan-Button sichtbar.")
    finally:
        driver.quit()

def main():
    html_path = "web/app.html"
    url = "file://" + str(Path(html_path).resolve())
    print(f"Starte Selenium- und Strukturtest für {url}\n")
    run_gui_validator(html_path)
    test_tabs_and_elements(url)
    print("\nAlle Tests abgeschlossen.")

if __name__ == "__main__":
    main()
