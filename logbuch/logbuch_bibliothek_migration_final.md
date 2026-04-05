# Logbuch: Migration zum Unified Library Module (bibliothek.js)

**Datum:** 29. März 2026

---

## Ziel
Die Bibliothekslogik wurde in das neue zentrale Modul `bibliothek.js` überführt. Ziel war es, alle State- und Rendering-Funktionen an einer Stelle zu bündeln und versehentlich entfernte Legacy-Funktionen wiederherzustellen.

---

## Wichtige Änderungen
- **browse.js → bibliothek.js**: Alle Funktionen und State-Variablen aus browse.js wurden übernommen. browse.js ist nun obsolet.
- **Funktionserweiterung**: Die Legacy-Funktionen `scan(targetDir, clearDb)`, `refreshLibrary()`, `loadLibrary(retryCount)`, `loadEditItems()`, `renderEditList()`, `filterEditList()` wurden wiederhergestellt.
- **State Management**: Globale Variablen wie `allLibraryItems` und `coverflowItems` werden jetzt zentral initialisiert und verwaltet.
- **Integration**: app.html lädt jetzt bibliothek.js, alle Referenzen wurden angepasst. In app_core.js wurde ein Boot-Aufruf von `loadLibrary()` ergänzt.

---

## Fehler & Lessons Learned
- **Fehlende Funktionen**: Nach der ersten Refaktorisierung fehlten wichtige Funktionen (z.B. Scan, Edit-Listen). Diese wurden aus dem Legacy-Core rekonstruiert und in bibliothek.js integriert.
- **State-Initialisierung**: Es gab Inkonsistenzen bei der Initialisierung von State-Variablen, was zu "undefined"-Fehlern im UI führte. Die Initialisierung wurde vereinheitlicht.
- **Import-Reihenfolge**: Die Reihenfolge der Script-Imports in app.html ist kritisch, um globale Sichtbarkeit und Initialisierung zu gewährleisten.
- **Automatisierte Checks**: Syntax-Fehler wurden mit `node --check` frühzeitig erkannt und behoben.

---

## Python-Version: Finalentscheidung
- **Python 3.14.2** ist ab sofort die verbindliche Mindestversion für das Projekt.
- In `src/core/main.py` wurde ein strikter Versions-Check implementiert. Bei Abweichung wird automatisch ein Re-Exec in der .venv-Umgebung ausgelöst.
- Die Datei `.python-version` wurde im Projekt-Root hinterlegt, um die Version für Tools wie pyenv und VS Code zu erzwingen.
- Alle requirements.txt und Build-Skripte wurden auf Python 3.14.x abgestimmt.

---

## Verifikation
- **Automatisiert:** node --check web/js/bibliothek.js bestanden, keine "undefined"-Fehler in der Konsole.
- **Manuell:** Scan, Grid/Coverflow, Edit-Tab und Playback funktionieren wie erwartet.

---

**Fazit:**
Mit bibliothek.js existiert nun ein robustes, zentrales Modul für die Medienbibliothek. Die Python-Umgebung ist final auf 3.14.2 festgelegt und wird strikt durchgesetzt. Die Codebasis ist damit zukunftssicher und wartbar.