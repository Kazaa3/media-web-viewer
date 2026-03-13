# Logbuch Eintrag 56: Milestone 2 – Modernisierung & Automatisierung (v1.35-dev)

**Datum:** 13. März 2026  
**Status:** In Planung 🏗️  
**Thema:** Neukonzeption der Test-Suite und Deployment-Pipeline.

## 1. Vision für Milestone 2
Nach dem erfolgreichen Abschluss von Milestone 1 (v1.34) mit Fokus auf grundlegende Stabilität und Transcoding, zielt Milestone 2 auf eine professionellere Entwicklungs-Infrastruktur ab. Wir wechseln von einem "Monolith-Test-Ansatz" zu einer mehrstufigen Validierungs-Architektur.

## 2. Geplante Änderungen

### Test-Klassifizierung
- **Unit (Tier 1)**: Schnelle, isolierte Tests ohne System-Tools.
- **Integration (Tier 2)**: Tests mit echten Abhängigkeiten (FFmpeg/VLC).
- **E2E/Release (Tier 3)**: Browser-Tests und Installer-Validierung.

### Branching-Modell
- Einführung des `develop`-Branch für tägliche Arbeit.
- `main` bleibt reserviert für Release-Reife Stände (Push to Main = Release Pipeline).

### Debian Automatisierung
- Überarbeitung der `.deb`-Build-Skripte zur Vermeidung von Rückständen (Staged Builds).
- Sicherstellung einer sauberen Deinstallation/Purge.

## 3. Akzeptanz-Kriterien
- [ ] Automatische Test-Selektion basierend auf der Test-Kategorie.
- [ ] Grüne Pipeline auf GitHub für `develop` (T1+T2) und `main` (T3).
- [ ] Keine Dateileichen unter `/opt/media-web-viewer` nach `apt purge`.

---
**Nächster Schritt:** Initiale Umstrukturierung der Test-Verzeichnisse und Update der GitHub Workflows.
