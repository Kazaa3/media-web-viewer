<!-- Category: Bug -->
<!-- Title_DE: Bekannte Probleme (Stand v1.1.18) -->
<!-- Title_EN: Known Issues (Status v1.1.18) -->
<!-- Summary_DE: Aktueller Stand der Fehlerbehebung und offene Punkte. -->
<!-- Summary_EN: Current status of bug fixes and open points. -->
<!-- Status: PLAN -->

# Bekannte Probleme (Stand v1.1.17)

## Behobene Probleme
- [x] Unnötige Konsolenausgaben beim Scan (jetzt hinter `db`-Flag).
- [x] Pfad-Konflikte nach Neuinstallation (Dokumentation für Reset hinzugefügt).
- [x] Fehlende System-Abhängigkeiten in der `.deb` (jetzt in `control` hinterlegt).
- [x] Testing & Logging

## Offene Punkte
- [ ] Globale Versionierung
- [ ] Hörbuch Tag muss weg
- [ ] Noch deutsch: Keine spezifischen Optionen für "Filename" verfügbar.
- [ ] Noch deutsch: Keine spezifischen Optionen für "Container Structure" verfügbar.
- [ ] Edit menu: Metadata saved! Popups später ausblenden / UI Umgestaltung
- [ ] im log Edit menu: Eintrag gespeichert!
- [ ] Refresh im Editmenü erfolgt nach schreiben nicht
- [ ] Enhancing Feature Modal and Navigation Bar
- [ ]  <!-- Category: Planung --> # Neuer Eintrag Tag in Formular deutsch
- [ ]  Console und Dict wieder tauschen / Mehr Dateiformate exposen / Datenbank intigrieren
- [ ]  Standardsprache aus Systemsprache ermitteln 
- [ ] Parser Rewrite
- [ ] Kein automatischer Refresh der UI, wenn Dateien im Dateisystem verschoben werden (manueller Scan nötig).
- [ ] Große Listen (Player-Tab) könnten bei >10.000 Einträgen eine Virtual-Scrolling Lösung vertragen.
- [ ] Container Parser falsch. Rüber zu pymediainfo. und hier mkv container erkennung für mkv audio Erkennung
- [ ] Speichern der Tags als String in der DB speichert nicht alle Tags, um Performance zu garantieren. Aber diese Tags müssen später für eine große Datenbank wiederherstellbar sein. Meilenstein Medienbibliothek
- [ ] Hinzufügen von Video- und Audio-Dateien zur Datenbank. 
    - [ ] Pflicht: m1a/alac, flac, mp3 
    - [ ] Opional: DSD 
- [ ] Weitere Datentypen hinzufügen. , wie Dokumente, E-Books, Bilder, Archive etc.
- [ ] ID-System für Medienelemente, die aus mehreren Objekten bestehen.
- [ ] Filmscraper
- [ ] GUI überarbeiten
- [ ] Gehört. Eher zu Features.
- [ ] Windows exe
- [ ] Weitere Datenquellen und Tools
- [ ] DOCUMENTATION
- [ ] Debug Flags

<!-- lang-split -->

# Known Issues (Status v1.1.15)

## Fixed Issues
- [x] Unnecessary console output during scan (now behind `db` flag).
- [x] Path conflicts after re-installation (added documentation for reset).
- [x] Missing system dependencies in the `.deb` (now listed in `control`).

## Open Tasks
- [ ] No automatic UI refresh when files are moved in the file system (manual scan required).
- [ ] Large lists (Player Tab) could use a virtual scrolling solution for >10,000 entries.