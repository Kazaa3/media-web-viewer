# Logbuch-Eintrag 52: Automated .deb Reinstallation Workflow

## Status
**Datum:** 2026-03-08  
**Version:** 1.3.1  
**Status:** ✅ Abgeschlossen  

## Problemstellung
Nach jeder Änderung am Code musste das .deb-Paket manuell deinstalliert und neu installiert werden, um die Änderungen zu testen. Dieser Prozess war fehleranfällig und zeitaufwändig:

1. Manuelles `sudo apt purge media-web-viewer`
2. Build mit `./build_deb.sh`
3. Manuelles `sudo dpkg -i media-web-viewer_*.deb`
4. Eventuell `sudo apt install -f -y` für Dependencies

## Lösung

### 1. Reinstall-Skript (`reinstall_deb.sh`)
Neues bash-Skript für automatisierte Reinstallation:

**Features:**
- ✅ Automatische Erkennung der aktuellen Version aus `VERSION` Datei
- ✅ Prüfung ob `.deb` Paket existiert (mit hilfreicher Fehlermeldung)
- ✅ Automatisches Purge des alten Pakets (falls installiert)
- ✅ Installation des neuen Pakets
- ✅ Automatische Dependency-Auflösung mit `apt install -f`
- ✅ Benutzerfreundliche Console-Ausgabe mit Emojis und Status-Updates

**Verwendung:**
```bash
# Nach dem Build einfach:
./reinstall_deb.sh
```

### 2. Test Suite (`tests/test_reinstall_deb.py`)
Umfassende Tests für die Reinstallation-Workflow:

**Test-Abdeckung:**
1. **Version Consistency Test** - Prüft `VERSION` ↔ `packaging/DEBIAN/control` Übereinstimmung
2. **Build Script Test** - Verifiziert Existenz und Ausführbarkeit von `build_deb.sh`
3. **Reinstall Script Test** - Verifiziert Existenz und Ausführbarkeit von `reinstall_deb.sh`
4. **Package Structure Test** - Inspiziert `.deb` Inhalt mit `dpkg-deb -c` auf essential files:
   - `./opt/media-web-viewer/main.py`
   - `./opt/media-web-viewer/requirements.txt`
   - `./usr/bin/media-web-viewer`
5. **Installation Status Test** - Zeigt aktuellen Installations-Status an
6. **Script Syntax Test** - Validiert bash-Syntax mit `bash -n`

**Test-Ergebnis:**
```
============================================================
📊 Test Results: 6 passed, 0 failed
============================================================
✅ All tests passed!
```

## Workflow-Verbesserung

### Vorher:
```bash
# 4 manuelle Schritte + Error-Handling
sudo apt purge media-web-viewer
./build_deb.sh
sudo dpkg -i media-web-viewer_1.3.1_amd64.deb
sudo apt install -f -y  # optional, bei Dependency-Problemen
```

### Nachher:
```bash
# 2 automatisierte Schritte
./build_deb.sh
./reinstall_deb.sh
```

## Integration im Entwicklungsprozess

### Typischer Dev-Workflow:
```bash
# 1. Code ändern
vim main.py

# 2. Lokalen Test (optional)
python tests/test_reinstall_deb.py

# 3. Build & Install
./build_deb.sh && ./reinstall_deb.sh

# 4. Produktionstest
media-web-viewer
```

### CI/CD Potential:
Das neue Test-Framework kann in automatisierte Build-Pipelines integriert werden:
- Pre-build validation (Version-Konsistenz)
- Post-build verification (Paket-Struktur)
- Syntax-Checks vor Deployment

## Technische Details

### Skript-Sicherheit
- ✅ `set -e` in allen bash-Skripten → Sofortiger Abbruch bei Fehler
- ✅ Existenz-Checks vor kritischen Operationen
- ✅ Sudo nur wo nötig (apt/dpkg Operationen)
- ✅ Hilfreiche Fehlermeldungen mit Exit Codes

### Test-Framework
- ✅ Python-basiert (konsistent mit Projekt)
- ✅ Keine externen Test-Dependencies (nutzt stdlib)
- ✅ Farbige Console-Ausgabe mit Emoji-Status-Indikatoren
- ✅ Exit Code 0/1 für CI-Integration

## Bekannte Einschränkungen
1. **Sudo-Passwort erforderlich** - `reinstall_deb.sh` benötigt sudo-Rechte für apt/dpkg
2. **Single-Architecture** - Aktuell nur `amd64` unterstützt
3. **Keine Rollback-Funktion** - Bei Fehler bleibt das Paket deinstalliert

## Ausblick / Todo
- [ ] Optional: Backup der alten Version vor Purge
- [ ] Optional: Rollback-Funktion bei fehlgeschlagener Installation
- [ ] Optional: Multi-Arch Support (arm64, etc.)
- [ ] Optional: Integration in `run.sh` für One-Command Setup

## Dateien

### Neu erstellt:
- `reinstall_deb.sh` - Automatisches Reinstallation-Skript (49 Zeilen)
- `tests/test_reinstall_deb.py` - Test Suite (178 Zeilen)

### Modifiziert:
- Keine (reine Addition zum Projekt)

## Zusammenfassung
Erfolgreiche Automatisierung des .deb Reinstallation-Workflows mit umfassender Test-Abdeckung. Spart Zeit und reduziert Fehler während der Entwicklung. Alle 6 Tests bestehen ✅.
