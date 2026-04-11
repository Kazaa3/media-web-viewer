<!-- Title_DE: GUI-Test-Strategien für Media Web Viewer -->
<!-- Title_EN: GUI Test Strategies for Media Web Viewer -->
<!-- Summary_DE: Übersicht und Best Practices für automatisierte GUI-Tests mit Eel/Bottle, Playwright, Selenium, MCP-Agenten und PyAutoGUI. -->
<!-- Summary_EN: Overview and best practices for automated GUI testing with Eel/Bottle, Playwright, Selenium, MCP agents, and PyAutoGUI. -->
<!-- Category: Tests -->
<!-- Status: ACTIVE -->

# GUI-Test-Strategien für Media Web Viewer

## Überblick
Die Media Web Viewer App nutzt Eel/Bottle für das Backend und eine browserbasierte GUI. GUI-Tests werden nicht direkt im Backend ausgeführt, sondern über Agenten oder Browser-Automatisierung.

## Best Practices
- **Playwright**: Moderne, schnelle Browser-Automatisierung. Empfohlen für Eel-GUIs.
- **Selenium**: Klassischer WebDriver-Ansatz, breiter Browser-Support.
- **PyAutoGUI**: Desktop-Automatisierung für pixelgenaue Tests.
- **MCP-Agenten**: Für AI-basierte Event-Simulation und Tool-Validierung.

## Beispiel-Setup
```bash
pip install playwright pytest
playwright install
```

## Beispiel Playwright-Test
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.click("#my-button")
    browser.close()
```

## Protokoll-Vergleich
| Protokoll      | Netzwerk | DOM-Zugriff | Python-Support | Eel geeignet |
|---------------|----------|-------------|---------------|-------------|
| WebDriver     | REST     | Indirekt    | Selenium      | Hoch        |
| CDP           | WebSocket| Direkt      | Playwright    | Sehr hoch   |
| Eel expose    | Intern   | Voll        | Eingeboren    | Perfekt     |
| MCP           | AI-Agent | Semantic    | Inspector     | Mittel      |
| PyAutoGUI     | Pixel    | Screen      | PyAutoGUI     | Desktop     |

## Empfehlungen
- Für Eel: Playwright oder Selenium für browserbasierte Tests.
- Für Desktop: PyAutoGUI für einfache Fenster-Checks.
- Für AI/Agenten: MCP-Inspector für Event-Simulation.

## Nächste Schritte
- Integration von Playwright/Selenium in CI/CD.
- Erweiterung der Dummy-Funktion im Backend für Test-Trigger.
- Dokumentation und Beispiele im logbuch ergänzen.

---
*Letzte Aktualisierung: 10. März 2026*