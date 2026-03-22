# Selenium Test: Headless-Fix für Media Web Viewer

## Problem
Aktuell startet der Selenium-Test ein sichtbares Browser-Fenster. Für CI, automatisierte Tests und lokale Runs sollte der Test im Headless-Modus laufen, damit keine Fenster geöffnet werden.

## Lösung
- Selenium-Tests müssen mit dem Headless-Flag gestartet werden.
- Beispiel für Chrome:
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,800')

browser = webdriver.Chrome(options=options)
```
- Für Firefox:
```python
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
```
- Prüfe, ob der Test runner (run_gui_tests.py) das Flag korrekt setzt.

## Status
- Headless-Flag in allen Selenium-Tests ergänzen
- CI und lokale Runs starten keine Fenster mehr

---
Letzte Aktualisierung: 11. März 2026
