# Task: Pipeline and Reporting Integration

**Datum:** 13.03.2026
**Autor:** Copilot

## Aufgabenübersicht

1. **SyntaxError beheben**
   - Fix in `src/core/env_handler.py`
2. **StatusBar-Integration**
   - Implementiere `scripts/status_bar_utils.py`
   - Integriere StatusBar in `infra/build_system.py`
3. **Management Reports**
   - Lege `build/management_reports/` an
   - Konsolidiere Benchmark- und Audit-Reports
   - Integriere Report-Uploads in alle GitHub Actions (ci-main, ci-dev, release)
4. **Build Pipeline Readiness**
   - Überprüfe und optimiere Build-Test-Gate in `build_system.py`
   - Korrigiere Testpfade in `release.yml`
   - Richte branch-spezifische JSON-Konfigurationsdeployment ein
   - Implementiere Build-Metadaten-Injektion und bedingte DB-Persistenz
   - Verifiziere, dass alle Test-Tiers mit Reporting lokal bestehen
5. **Release-Dokumentation**
   - Finalisiere Release-Doku und Management Reporting System
   - Dokumentiere Reporting-System in walkthrough.md
6. **Branching & Merge Repair**
   - Untersuche Branch-Status und fehlende Dateien
   - Merge milestone1-pre-release → meilenstein-1-mediaplayer
   - Löse Merge-Konflikte, stelle kritische Dateien wieder her
   - Projektstand auf Version 1.34 angleichen
7. **Performance Audit Integration**
   - Performance-Audit mit size-aware extraction erneut ausführen
   - JSON-Report-Generierung verifizieren
   - Sicherstellen, dass CI/CD-Artifact-Upload funktioniert
8. **Main Branch Synchronization (v1.34 Release)**
   - Stabilisiere meilenstein-1-mediaplayer (v1.34 verified)
   - Merge in main, Konflikte lösen, Build-Gate erneut ausführen
   - Push/Pull Request zu origin main

## Weitere Aufgaben
- Medien-Typ-Konfiguration synchronisieren (`web/config.main.json`, `web/config.develop.json`)
- Build-Differenzierung (Main=Audio, Dev=All)
- Defaults in `src/parsers/format_utils.py` bereinigen
- cat_map in `src/core/main.py` für "PC Games" und "Supplements" erweitern
- Kategorie-Filterung im UI prüfen
- Clean Database für Release Builds erzwingen
- BRANCH von `build_system.py` an `build_deb.sh` übergeben
- `data/` vom Debian-Paket-Staging ausschließen
- postrm purge-Logik für leere/fehlende Branches als Release behandeln
- Frischen Scan bei Release-Installation verifizieren

---

**Fazit:**
Diese Aufgabenliste bildet die Grundlage für die finale Stabilisierung, Reporting-Integration und Release-Vorbereitung des Media Web Viewer v1.34.
