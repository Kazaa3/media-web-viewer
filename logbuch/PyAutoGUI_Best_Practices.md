# PyAutoGUI – Best Practices und Integration

## Übersicht
PyAutoGUI ist ein Python-Modul zur Automatisierung von Maus- und Tastaturaktionen sowie zur Bildschirmaufnahme. Es eignet sich für GUI-Tests, Automatisierung und Skripting.

## Installation
```bash
pip install pyautogui
```

## Typische Anwendungsfälle
- Automatisierte UI-Tests
- End-to-End-Tests von Desktop-Anwendungen
- Automatisierung von Routineaufgaben
- Screenshot-Erstellung und Bildvergleich

## Beispielcode
```python
import pyautogui

# Maus bewegen
pyautogui.moveTo(100, 200)

# Klick ausführen
pyautogui.click()

# Text eingeben
pyautogui.write('Hello, world!')

# Screenshot aufnehmen
screenshot = pyautogui.screenshot()
screenshot.save('screenshot.png')
```

## Best Practices
- Tests sollten reproduzierbar und robust sein (z.B. mit festen Koordinaten oder Bildabgleich).
- Wartezeiten (`pyautogui.sleep()`, `pyautogui.PAUSE`) nutzen, um Timing-Probleme zu vermeiden.
- Fehlerbehandlung einbauen (z.B. `pyautogui.FAILSAFE` aktivieren).
- Für CI/CD: Virtuelle Displays (z.B. Xvfb) nutzen, um Tests ohne echten Desktop auszuführen.
- Kombinierbar mit `pytest` für automatisierte Testläufe.

## Integration in Media Web Viewer
- GUI-Tests können mit PyAutoGUI automatisiert werden, z.B. für das Testen von Medienwiedergabe, Dateiauswahl und UI-Interaktionen.
- Siehe auch `logbuch/GUI_Test_Strategien.md` für weitere Testansätze (Playwright, Selenium, MCP-Agent).

## Hinweise
- PyAutoGUI ist plattformübergreifend, aber einige Funktionen können je nach OS variieren.
- Für fortgeschrittene Tests: Bildvergleich (`pyautogui.locateOnScreen`) und Multi-Monitor-Unterstützung.

---
**Weitere Ressourcen:**
- [PyAutoGUI Dokumentation](https://pyautogui.readthedocs.io/)
- [GUI_Test_Strategien.md](GUI_Test_Strategien.md)
