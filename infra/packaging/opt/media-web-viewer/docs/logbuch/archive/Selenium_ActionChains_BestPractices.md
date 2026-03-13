# Selenium Action Chains – Best Practices & Beispiele

## Übersicht
Selenium Action Chains ermöglichen komplexe Maus- und Tastatur-Interaktionen, wie Drag & Drop, Multi-Select, Hover und mehr. Ideal für UI-Tests im Media Web Viewer.

## Installation
```bash
pip install selenium
```

## Beispiel: Drag & Drop
```python
from selenium.webdriver import ActionChains
from selenium import webdriver

browser = webdriver.Chrome()
source = browser.find_element(By.ID, 'drag-source')
target = browser.find_element(By.ID, 'drop-target')

actions = ActionChains(browser)
actions.click_and_hold(source)
actions.move_to_element(target)
actions.release(target)
actions.perform()
```

## Weitere Aktionen
- `actions.move_by_offset(x, y)` – Maus an Offset bewegen
- `actions.double_click(element)` – Doppelklick
- `actions.context_click(element)` – Rechtsklick
- `actions.send_keys(Keys.ENTER)` – Tastatur-Events

## Best Practices
- Immer `actions.perform()` am Ende aufrufen
- Wartezeiten (`WebDriverWait`) für UI-Updates einbauen
- Für Drag & Drop: `click_and_hold`, `move_to_element`, `release`
- Für Multi-Select: `key_down(Keys.CONTROL)`, `click(element)`, `key_up(Keys.CONTROL)`

## Status
- Action Chains für Drag & Drop und komplexe UI-Tests nutzen
- Beispiele und Workflow dokumentiert

---

# Selenium & venv: Verhalten bei parallelem main.py
#
# - Selenium verwendet die aktive Python-Umgebung (venv), in der der Test ausgeführt wird.
# - Wird main.py zusätzlich geöffnet, laufen beide Prozesse unabhängig, teilen aber die venv.
# - Konflikte können auftreten, wenn main.py einen Webserver startet und Selenium darauf zugreifen soll – Adresse/Port müssen stimmen.
# - Für isolierte Tests: venv aktivieren, main.py starten (falls Backend benötigt), dann Selenium-Test ausführen.
# - Kurz: Selenium nutzt die aktive venv, parallele main.py-Prozesse sind möglich, aber erfordern ggf. abgestimmte Ports und Pfade.

---

# Doppel-venv für Selenium & main.py: Sinn und Anwendung
#
# - Eine doppelte venv macht Sinn, wenn Selenium-Tests und main.py komplett isoliert laufen sollen.
# - Vorteil: Keine Paket-Konflikte, getrennte Abhängigkeiten, parallele Entwicklung/Tests.
# - Anwendung: Zwei venvs anlegen (z.B. .venv_selenium und .venv_main), jeweils separat aktivieren und starten.
# - Selenium-Tests können so unabhängig von main.py laufen, z.B. mit eigenen Webdriver-Versionen oder Testpaketen.
# - Für CI: Separate venv für Test-Runner, Backend und Frontend.

---

Letzte Aktualisierung: 11. März 2026
