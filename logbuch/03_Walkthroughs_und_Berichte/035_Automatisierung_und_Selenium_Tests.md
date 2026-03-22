<!-- Category: Documentation -->
<!-- Title_DE: Automatisierung & Selenium-Tests -->
<!-- Title_EN: Automation & Selenium Tests -->
<!-- Summary_DE: Absicherung der Benutzeroberfläche: Selenium E2E-Tests, Headless-Testing mit xvfb und automatisierte UI-Validierung. -->
<!-- Summary_EN: Securing the user interface: Selenium E2E tests, headless testing with xvfb and automated UI validation. -->
<!-- Status: ACTIVE -->

# Automatisierung & Selenium-Tests

## Qualität durch Automation
Ein komplexes Frontend wie das von **dict - Web Media Player & Library** erfordert mehr als nur manuelle Tests. Um sicherzustellen, dass jede Änderung an der GUI oder dem Backend die User-Experience nicht beeinträchtigt, haben wir eine umfassende Test-Automatisierung implementiert.

## Selenium: Das Auge des Testers
Wir nutzen **Selenium WebDriver**, um echte Nutzer-Interaktionen im Browser zu simulieren. Unsere Tests decken kritische Pfade ab:
- **Playback-Check:** Startet ein Lied und prüft, ob der Audio-Status auf `playing` wechselt.
- **Playlist-Interaktion:** Testet das Verschieben von Titeln per Drag-and-Drop und das Entfernen von Items.
- **Navigation:** Validiert, ob der Wechsel zwischen den Tabs (Library, Player, Settings) korrekt funktioniert und die Zustände erhalten bleiben.

## Headless Testing & CI
Da unsere Tests oft in Umgebungen ohne echten Monitor laufen (z.B. auf GitHub Actions), setzen wir auf **Headless-Technologien**:
- **xvfb (X Virtual Framebuffer):** Simuliert einen grafischen Bildschirm im Arbeitsspeicher.
- **Firefox/Geckodriver:** Unsere primäre Test-Plattform, die eine hohe Konformität zu Webstandards garantiert.

## Test-Resilienz
Um "flaky tests" zu vermeiden, haben wir Best Practices implementiert:
- **Explicit Waits:** Anstatt fester Pausen (`sleep`) wartet das System gezielt auf das Erscheinen von Elementen.
- **Isolierte Umgebungen:** Jeder Testlauf nutzt eine eigene temporäre Instanz der Anwendung und der Datenbank (`venv_selenium`).
- **Screenshot-Logging:** Bei Fehlern erstellt das System automatisch ein Bildschirmfoto des Browsers zur schnellen Fehlerdiagnose.

*Automatisierung ist für uns kein Luxus, sondern die Garantie, dass dict jeden Tag so stabil läuft wie am ersten.*

<!-- lang-split -->

# Automation & Selenium Tests

## Quality through Automation
A complex frontend like that of **dict - Web Media Player & Library** requires more than just manual tests. To ensure that every change to the GUI or backend does not affect the user experience, we have implemented comprehensive test automation.

## Selenium: The Eye of the Tester
We use **Selenium WebDriver** to simulate real user interactions in the browser. Our tests cover critical paths:
- **Playback Check:** Starts a song and checks whether the audio status changes to `playing`.
- **Playlist Interaction:** Tests moving titles via drag-and-drop and removing items.
- **Navigation:** Validates whether the switch between tabs (Library, Player, Settings) works correctly and states are maintained.

## Headless Testing & CI
Since our tests often run in environments without a real monitor (e.g., on GitHub Actions), we rely on **headless technologies**:
- **xvfb (X Virtual Framebuffer):** Simulates a graphic screen in memory.
- **Firefox/Geckodriver:** Our primary test platform, which guarantees high conformity to web standards.

## Test Resilience
To avoid "flaky tests", we have implemented best practices:
- **Explicit Waits:** Instead of fixed pauses (`sleep`), the system waits specifically for elements to appear.
- **Isolated Environments:** Each test run uses its own temporary instance of the application and the database (`venv_selenium`).
- **Screenshot Logging:** In the event of errors, the system automatically creates a screenshot of the browser for quick fault diagnosis.

*For us, automation is not a luxury, but the guarantee that dict runs as stably every day as it did on the first.*
