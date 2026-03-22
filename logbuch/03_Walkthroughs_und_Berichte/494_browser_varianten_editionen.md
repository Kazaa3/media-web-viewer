# Logbuch: Unterstützte Browser – Varianten & Editionen

**Datum:** 15.03.2026

## Übersicht unterstützter Browser
Die Media Web Viewer App unterstützt verschiedene Browser für die Web-Frontend-Anzeige und automatisierte Tests. Die wichtigsten Varianten und Editionen sind:

| Browser    | Varianten/Editionen         | Hinweise                                  |
|------------|-----------------------------|--------------------------------------------|
| Chrome     | Stable, Beta, Dev, Canary   | Weit verbreitet, beste Kompatibilität      |
| Chromium   | Open Source, Snap, Flatpak  | Basis für Chrome, oft in Linux-Umgebungen  |
| Firefox    | Stable, ESR, Developer, Nightly | Gute Web-Standards, Geckodriver für Tests |
| Firefox ESR| Extended Support Release    | Für Langzeitstabilität in Unternehmen      |
| Firefox Dev| Developer Edition           | Für Webentwicklung, neue Features zuerst   |
| Firefox Nightly | Nightly Build           | Schnellste Updates, experimentell          |
| Chrome Dev | Developer Edition           | Für frühe Feature-Tests                    |
| Chrome Canary | Canary Build              | Tägliche Updates, experimentell            |
| Edge       | Stable, Dev, Beta, Canary   | Chromium-basiert, optional unterstützt     |

## Hinweise zur Nutzung
- **Automatisierte Tests:**
  - Chrome/Chromium: Steuerung via ChromeDriver
  - Firefox: Steuerung via Geckodriver
- **Editionen:**
  - Dev/Canary/Nightly sind für frühe Feature-Tests und Debugging geeignet, aber nicht für den Produktivbetrieb empfohlen.
  - ESR/Stable werden für produktive Umgebungen empfohlen.
- **Linux:**
  - Chromium ist oft als Standardbrowser in vielen Linux-Distributionen verfügbar.
  - Snap/Flatpak-Editionen können abweichende Pfade/Verhalten haben.

## Kompatibilitätsmatrix (Beispiel)
| Feature                | Chrome | Chromium | Firefox | Firefox ESR | Dev/Canary/Nightly |
|------------------------|:------:|:--------:|:-------:|:-----------:|:------------------:|
| UI/Frontend            |   ✔️   |    ✔️    |   ✔️    |     ✔️      |        ✔️         |
| E2E-Tests (Selenium)   |   ✔️   |    ✔️    |   ✔️    |     ✔️      |        ✔️         |
| Media Playback         |   ✔️   |    ✔️    |   ✔️    |     ✔️      |        ✔️         |
| Debugging/Dev-Tools    |   ✔️   |    ✔️    |   ✔️    |     ✔️      |        ✔️         |

## Fazit
Die App ist mit allen gängigen Chrome-, Chromium- und Firefox-Editionen kompatibel. Für CI/CD und automatisierte Tests sollten stabile oder ESR-Versionen bevorzugt werden. Dev-/Nightly-Editionen sind für frühe Feature-Validierung und Debugging nützlich.
