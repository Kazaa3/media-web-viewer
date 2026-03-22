## Artikel: Neue Selenium-Testfälle & Spracheinstellungen
**Datum:** 12. März 2026

- Ziel: Dokumentation der neuen Selenium-Testfälle mit Fokus auf Spracheinstellungen und Lokalisierung.

### Hintergrund
- Die GUI-Tests werden mit Selenium ausgeführt. Standardmäßig ist die Browser-Sprache auf Deutsch gesetzt, wodurch die Oberfläche in Deutsch erscheint.
- Für internationale Tests ist es sinnvoll, den Browser explizit auf Englisch zu stellen, aber die Anwendung weiterhin auf Deutsch zu testen.

### Vorgehen
- Selenium-Instanz wird mit englischer Browser-Sprache gestartet (z.B. via DesiredCapabilities oder Profile-Settings).
- Die Anwendung bleibt auf Deutsch, sodass Lokalisierungs- und Übersetzungslogik gezielt geprüft werden kann.
- Testfälle prüfen, ob die UI korrekt auf Deutsch bleibt, auch wenn die Browser-Sprache Englisch ist.
- Zusätzliche Checks für Sprachumschaltung und Lokalisierungs-Features.

### Vorteile
- Sicherstellung, dass die Anwendung unabhängig von der Browser-Sprache korrekt lokalisiert wird.
- Bessere Testabdeckung für internationale Nutzer und CI/CD-Umgebungen.

*Entry created: 12. März 2026*
---