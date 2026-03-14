<!-- Category: Bug -->
<!-- Title_DE: Bekannte Probleme (Stand v1.3.4) -->
<!-- Title_EN: Known Issues (Status v1.3.4) -->
<!-- Summary_DE: Aktueller Stand der Fehlerbehebung und offene Punkte. -->
<!-- Summary_EN: Current status of bug fixes and open points. -->
<!-- Status: PLAN -->

# Bekannte Probleme (Stand v1.3.4)

## Behobene Probleme
- [x] Unnötige Konsolenausgaben beim Scan (jetzt hinter `db`-Flag).
- [x] Pfad-Konflikte nach Neuinstallation (Dokumentation für Reset hinzugefügt).
- [x] Fehlende System-Abhängigkeiten in der `.deb` (jetzt in `control` hinterlegt).
- [x] **v1.1.18/1.1.19 Highlights**:
    - [x] Umplatzierung der "Danger Zone" (Reset) in den Optionen.
    - [x] Interaktive News-Bar im Header.
    - [x] Vollständige Projekt-Dokumentation (`DOCUMENTATION.md`).
    - [x] Dynamisches und bilinguales Feature-Modal.
    - [x] Features Modal hat nicht automatisch die neusten EInträge (42 
fehlt)
- [x] Test-Tab-Sprung/Session-Abbruch durch Browser-Unload + mögliches Doppel-Fenster (Fix: `eel.start(..., mode=False)`, robuster Keepalive, UI-Trace). Siehe `logbuch/59_Test_Tab_Stability_and_Single_Window.md`.

## Offene Punkte
- [x] Globale Versionierung (zentrale Stelle statt 3 Dateien).
- [x] Versioneurung fehlt in doku
- [ ] Edit aktuaisuerng / bib
- [x] logbuch einträge filterung wenn header fehlt führt zu fehlenden einträgen
- [x] Sortierung neuer log einträge erfolgt bei abgescjlossen. neue sind aber noch offfen. neuen status einführen
- [x] -md ist kein uni code format
- Keine Medien in der Bibliothek. Füge Dateien über den Browser-Tab hinzu oder klicke "Scan Media". String in
- [ ] logtab. fixe elemente für tag felder auf gui
- [ ] Test: Verifizierung .deb mit Version
- [ ] Hörbuch Tag (Backend) muss vereinheitlicht werden.
- [ ] Parser-Optionen: "Filename" und "Container" Details noch auf Deutsch.
- [ ] Edit-Menü: Metadaten-Speicher-Popups automatisch ausblenden.
- [ ] Refresh im Edit-Menü nach Speichern verbessern.
- [ ] Standardsprache aus Systemsprache ermitteln.
- [ ] Parser Rewrite (Meilenstein Performance).
- [ ] Kein automatischer Refresh der UI bei Dateioperationen (manueller Scan nötig).
- [ ] Container Parser (mkv audio Erkennung via pymediainfo verbessern).
- [ ] Medienbibliothek: Skalierbarkeit (>10.000 Einträge).

<!-- lang-split -->

# Known Issues (Status v1.3.4)

## Fixed Issues
- [x] Unnecessary console output during scan (now behind `db` flag).
- [x] Path conflicts after re-installation (added documentation for reset).
- [x] Missing system dependencies in the `.deb` (now listed in `control`).
- [x] **v1.1.18/1.1.19 Highlights**:
    - [x] Relocation of "Danger Zone" in options.
    - [x] Interactive News Bar in header.
    - [x] Full project documentation (`DOCUMENTATION.md`).
    - [x] Dynamic and bilingual feature modal.

## Open Tasks
- [x] Global versioning system.
- [x] Eintrag gespeichert! noch deutsch nach logbook edit
- [ ] Logging file
- [x] debug flags
- [ ] Standardize audiobook tags in backend.
- [ ] No automatic UI refresh on file system changes.
- [ ] Scalability for very large libraries.