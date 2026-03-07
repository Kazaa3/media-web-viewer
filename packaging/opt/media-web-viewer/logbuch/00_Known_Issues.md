<!-- Category: Planning -->
<!-- Title_DE: Bekannte Probleme (Stand v1.1.15) -->
<!-- Title_EN: Known Issues (Status v1.1.15) -->
<!-- Summary_DE: Aktueller Stand der Fehlerbehebung und offene Punkte. -->
<!-- Summary_EN: Current status of bug fixes and open points. -->
<!-- Status: PLAN -->

# Bekannte Probleme (Stand v1.1.17)

## Behobene Probleme
- [x] Unnötige Konsolenausgaben beim Scan (jetzt hinter `db`-Flag).
- [x] Pfad-Konflikte nach Neuinstallation (Dokumentation für Reset hinzugefügt).
- [x] Fehlende System-Abhängigkeiten in der `.deb` (jetzt in `control` hinterlegt).

## Offene Punkte
- [ ] Hörbuch Tag muss weg
- [ ] Kein automatischer Refresh der UI, wenn Dateien im Dateisystem verschoben werden (manueller Scan nötig).
- [ ] Große Listen (Player-Tab) könnten bei >10.000 Einträgen eine Virtual-Scrolling Lösung vertragen.

<!-- lang-split -->

# Known Issues (Status v1.1.15)

## Fixed Issues
- [x] Unnecessary console output during scan (now behind `db` flag).
- [x] Path conflicts after re-installation (added documentation for reset).
- [x] Missing system dependencies in the `.deb` (now listed in `control`).

## Open Tasks
- [ ] No automatic UI refresh when files are moved in the file system (manual scan required).
- [ ] Large lists (Player Tab) could use a virtual scrolling solution for >10,000 entries.