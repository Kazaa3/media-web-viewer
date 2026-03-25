# Logbuch-Eintrag

Datum: 25.03.2026

## Layout-Stabilisierung & Selenium-Test-Suite-Upgrade

### Zusammenfassung
- Layout-Probleme ("Phantom Sidebar", Zentrierung) in Logbuch- und Video-Tabs behoben.
- Selenium-Test-Suite um "PP Mode" (Performance Mode) und Session-Sync erweitert.

### Details

#### Layout-System-Stabilisierung
- Sidebar und Splitter werden in allen Nicht-Audio-Tabs per `display: none !important` entfernt, Flex-Berechnung ist korrekt.
- `#main-content-area` erhält in Management-Mode `width: 100%` und `margin-left: 0` für echtes Fullscreen.
- `tabMap`-IDs für Reporting, Video und Playlist korrigiert, keine leeren/broken Views mehr.

#### Selenium Suite Upgrade: "PP Mode" & Session Sync
- Neuer UI- und Backend-Flag für "PP Mode" (Performance Mode): Schnellere, robustere Navigation und DOM-Prüfung.
- Session-Attach: Nutzung von 127.0.0.1:9222 für aktive Browser-Session.
- Navigation-Selectoren aktualisiert: Korrekte DOM-IDs für alle Tab-Trigger-Buttons.
- DOM-Balance-Auditing: Test-Suite prüft jetzt auch komplexe Panels wie Logbuch und Video auf strukturelle Integrität.

### Geänderte Dateien
- `app.html`: `switchTab`-Logik, CSS-Layout, Selenium-UI-Flags
- `main.py`: Eel-Exposures für Selenium-Flags
- `test_selenium_session.py`: Button-Mappings, Performance Mode

---

*Automatisch generierter Logbucheintrag zur heutigen Layout-Stabilisierung und Test-Suite-Verbesserung.*
