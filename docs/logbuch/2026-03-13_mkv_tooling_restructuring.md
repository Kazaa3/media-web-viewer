# Logbuch-Eintrag: MKV Tooling Display Restructuring

**Datum:** 13. März 2026

## Änderungen

### 1. MKV Tooling Display Restructuring
- MKV-Tool-Informationen im Environment-Bereich erweitert und neu strukturiert:
  - **pymkv:** Eigene Zeile mit Status und Version.
  - **mkvinfo:** Zeigt CLI-Version und Pfad separat.
  - **mkvmerge:** Neue Zeile mit CLI-Version und Pfad.

### 2. Backend Enhancements
- main.py: `_get_runtime_tools_status()` erkennt jetzt mkvmerge CLI und extrahiert die Version.
- Versionserkennung für mkvinfo und mkvmerge verbessert.

### 3. Localization and UI Sync
- Neue i18n-Keys: `env_label_pymkv`, `env_label_mkvmerge` in i18n.json.
- app.html: Drei separate Status-Elemente für pymkv, mkvinfo, mkvmerge.
- loadEnvironmentInfo(): JS-Funktion aktualisiert, um die Statusfelder individuell zu füllen.

### 4. Tool Version Extraction Fix
- MediaInfo CLI-Version wird jetzt korrekt angezeigt:
  - Regex sucht im gesamten Output.
  - Robusteres Pattern für Versionen wie 23.04.

## Verification Result
- Alle drei MKV-Tools (pymkv, mkvinfo, mkvmerge) werden im GUI mit Status und Version angezeigt.
- Detaillierte Übersicht über die MKV-Toolchain im Environment-Bereich.

---
