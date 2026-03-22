# Erweiterung: Zentrale Konfiguration & Betriebsmodi

**Datum:** 15.03.2026

## 1. Zentrale Konfiguration für Index-Verzeichnisse
- Die Konfiguration für alle relevanten Index-Verzeichnisse (Browse-Dir, Bibliotheks-Dir, zusätzliche Bibliotheks-Dirs) wird zentral verwaltet.
- Die bisherige (verteilte) Konfiguration wird entfernt.
- Neue zentrale Config-Section:
  - **browse_dir:** Hauptverzeichnis für das Durchsuchen von Medien
  - **library_dir:** Hauptverzeichnis der Mediathek
  - **additional_library_dirs:** Liste weiterer Bibliotheksverzeichnisse
- Beispiel (config.json):
  ```json
  {
    "browse_dir": "/media/browse",
    "library_dir": "/media/library",
    "additional_library_dirs": ["/media/extra1", "/media/extra2"]
  }
  ```

## 2. Parser-Betriebsmodi: lightweight / full / ultimate
- Die Parser-Logik erhält einen Betriebsmodus-Schalter:
  - **lightweight:** Minimaler Metadaten-Scan, schnell, wenig Ressourcen
  - **full:** Standard-Scan, alle üblichen Metadaten und Checks
  - **ultimate:** Maximale Tiefe, alle verfügbaren Parser, ggf. mit Zusatzchecks
- Der Modus kann zentral in der Config gesetzt werden (z. B. `parser_mode: "full"`).
- Die Parser-Kette richtet sich dynamisch nach dem gewählten Modus.

## 3. App-Mode: Low Bandwidth / High-Performance
- Die Anwendung kann in verschiedene App-Modes geschaltet werden:
  - **Low Bandwidth:** Reduzierte Datenübertragung, z. B. weniger Detaildaten, kleinere Payloads
  - **High-Performance:** Volle Funktionalität, keine Bandbreitenoptimierung
- Der Modus kann zentral in der Config gesetzt werden (z. B. `app_mode: "low_bandwidth"`).

---

**Ergebnis:**
- Alle wichtigen Verzeichnisse und Betriebsmodi sind zentral konfigurierbar.
- Die Konfiguration ist übersichtlich, flexibel und unterstützt verschiedene Anwendungs- und Performance-Szenarien.
