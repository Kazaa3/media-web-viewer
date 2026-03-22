<!-- Category: Feature -->
<!-- Status: COMPLETED -->
<!-- Title (DE): Versions-Konsistenztest über zentrale VERSION-Datei -->
<!-- Title (EN): Version Consistency Test from Central VERSION file -->
<!-- Summary (DE): Neuer pytest-Test prüft zentrale Versionsableitung aus VERSION und erkennt alte Versionsnummern in kritischen Dateien -->
<!-- Summary (EN): New pytest test validates central version derivation from VERSION and detects stale version numbers in critical files -->

# Versions-Konsistenztest über zentrale VERSION-Datei

**Version:** 1.2.23  
**Datum:** 8. März 2026  
**Status:** ✅ COMPLETED

## Übersicht

Es wurde ein dedizierter Test ergänzt, der die aktuelle Soll-Version aus der Datei `VERSION` liest und anschließend prüft, ob zentrale Stellen im Projekt konsistent auf diese Version referenzieren.

Zusätzlich erkennt der Test veraltete `.deb`-Beispiele in der Dokumentation.

## Implementierung

### Neue Testdatei
- `tests/test_version_consistency.py`

### Enthaltene Prüfungen
1. **SemVer-Validierung von `VERSION`**
   - Erwartet Format `MAJOR.MINOR.PATCH` (z. B. `1.2.23`)

2. **Konsistenzprüfung zentraler Dateien**
   - `main.py`: Fallback-Version entspricht `VERSION`
   - `packaging/DEBIAN/control`: `Version:` entspricht `VERSION`
   - `DOCUMENTATION.md`: `**Version:**` entspricht `VERSION`
   - `DOCUMENTATION.md`: `**Current Version:**` entspricht `VERSION`

3. **Stale-Version-Erkennung in `.deb`-Beispielen**
   - Prüft alle Vorkommen von `media-web-viewer_X.Y.Z_amd64.deb`
   - Schlägt fehl, wenn alte Versionsnummern gefunden werden

## Ergebnis

Beim ersten Lauf wurde ein alter Wert erkannt:
- `media-web-viewer_1.2.21_amd64.deb` in `DOCUMENTATION.md`

Dieser Eintrag wurde auf `1.2.23` korrigiert. Danach war der Testlauf erfolgreich:

```bash
source .venv/bin/activate
pytest -q tests/test_version_consistency.py
# 3 passed
```

## Nutzen

- Verhindert versehentliche alte Versionsnummern nach Release-Updates
- Erzwingt die zentrale Versionsführung über `VERSION`
- Reduziert manuelle Release-Fehler in Doku und Packaging-Metadaten

## Geänderte Dateien

- `tests/test_version_consistency.py` (neu)
- `DOCUMENTATION.md` (Korrektur veraltetes `.deb`-Beispiel)

## Hinweis für zukünftige Releases

Bei jeder Versionserhöhung zuerst `VERSION` aktualisieren, danach diesen Test ausführen:

```bash
pytest -q tests/test_version_consistency.py
```

So wird sichergestellt, dass keine alten Versionsreferenzen im Projekt verbleiben.
