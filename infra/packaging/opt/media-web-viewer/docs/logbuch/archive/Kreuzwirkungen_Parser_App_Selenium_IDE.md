# Hinweis: Kreuzwirkungen mit main.py, App, Selenium & IDE

## Wechselwirkungen bei parallelen Prozessen

### Parser-Stalling & main.py
- Parser-Stalling kann zu Wechselwirkungen mit main.py führen, wenn dort z.B. ein Webserver, API oder UI-Thread läuft.
- Blockierte Parser können das Backend oder die UI verzögern, besonders bei synchronen Aufrufen.
- Lösung: Parser immer asynchron oder in eigenen Threads ausführen, main.py nicht blockieren.
- Fehlerbilder und Stalling-Fälle im Logbuch dokumentieren, ggf. Backend-Timeouts ergänzen.

### App, Selenium, main.py & zweite IDE
- Wenn App, Selenium-Tests und main.py parallel laufen (z.B. in mehreren IDEs oder Terminals), kann es zu Wechselwirkungen kommen:
  - Ports können blockiert sein (z.B. Webserver doppelt gestartet)
  - Datenbankzugriffe oder Dateizugriffe können kollidieren
  - UI-Tests (Selenium) greifen ggf. auf eine andere Instanz als erwartet zu
  - Race Conditions bei gleichzeitigen Backend- und Frontend-Starts
- Lösung: Klare Port- und Pfadzuweisung, getrennte venvs, Logging und Fehlerbilder dokumentieren
- Für CI: Isolierte Testumgebungen und dedizierte Test-Runner verwenden

---
Letzte Aktualisierung: 11. März 2026
