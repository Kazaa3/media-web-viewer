# Import-Shadowing vermeiden & Test-`venv` einrichten

Kurz: Dieses Dokument beschreibt zwei häufige Probleme beim lokalen Entwickeln und Testen
von `Media Web Viewer`: (1) wie man verhindert, dass externe oder `packaging/`-Kopien
Lokalmodule überschreiben (Import-Shadowing) und (2) wie ein isoliertes Test-`venv`
für deterministische Integrationstests eingerichtet wird.

## 1) Import-Shadowing (Symptom & Ursachen)
- Symptom: Tests importieren nicht den Quellcode aus dem Arbeitsverzeichnis, sondern eine
  andere Kopie (z.B. `/packaging/opt/media-web-viewer`), was zu unerwartetem Verhalten
  oder veralteten APIs führt.
- Ursache: `sys.path` enthält Ordner, die vorgelagerte Kopien des Projekts enthalten
  (z.B. aus Packagingschritten oder systemweiten Installationen).

## 2) Schnelle Checks zum Erkennen von Shadowing
- In einem aktivierten venv ausführen:
```bash
python -c "import main; print(main.__file__)"
python -c "import models; print(models.__file__)"
```
Wenn der Pfad außerhalb des Projektordners liegt (z.B. `/packaging/`), gibt es Shadowing.

## 3) Sofortmaßnahmen (lokal, ohne CI-Änderungen)
- 1) Präfix-Pfad in `PYTHONPATH`/`sys.path`: vor lokalen Imports sicherstellen, dass
  das Projektverzeichnis ganz vorne steht: `export PYTHONPATH=$(pwd):$PYTHONPATH`.
- 2) Verwende `pip install -e .` im Entwickler-venv, damit Imports `site-packages`-Mechaniken
  umgehen und auf die Arbeitskopie verweisen:
```bash
source .venv/bin/activate
pip install -e .
```
- 3) Entferne oder verschiebe problematische packaging-Ordner aus `sys.path` temporär.
  Beispiel (in `conftest.py` vor Test-Imports):
```python
import sys, os
root = os.path.abspath(os.path.dirname(__file__) + '/..')
if root not in sys.path:
    sys.path.insert(0, root)
# optional: remove known packaging paths
sys.path = [p for p in sys.path if '/packaging/opt/media-web-viewer' not in p]
```

## 4) Dauerhafte Prävention in Test-Läufen
- Ergänze `pytest.ini` oder `conftest.py`, damit Tests standardmäßig das Projekt-Root
  priorisieren. Beispiel `conftest.py`-Snippet siehe oben.
- Füge in `pytest.ini` ggf. `testpaths = tests` hinzu, um Discovery auf das Testverzeichnis zu
  begrenzen und ungewollte Install-Imports zu vermeiden.

## 5) Best Practices
- Immer `pip install -e .` in Entwicklerumgebungen, nicht `pip install .` aus dem Source-Tree.
- Vermeide permanente Kopien des Projektes in globalen `site-packages` oder in `/opt`.
- Verwende `python -m pip uninstall <pkg>` um alte global installierte Versionen zu entfernen.

## 6) Test-`venv` für deterministische Integrationstests
Ziel: eine saubere, wiederholbare Umgebung mit pinned Test-Dependencies.

Empfohlener Ablauf:
```bash
# clean venv für tests anlegen
python -m venv .venv-test
source .venv-test/bin/activate

# (optional) upgrade pip
pip install --upgrade pip

# installiere die dev/test-abhängigkeiten (siehe `requirements-test.txt`)
pip install -r requirements-test.txt

# installiere das Paket editable, damit lokale Quelländerungen genutzt werden
pip install -e .

# tests ausführen
pytest -q
```

### Inhalt von `requirements-test.txt` (Beispiel)
- mutagen==x.y.z
- pymediainfo==a.b.c
- pytest==7.x.y
- selenium==<versionspec>
- ffmpeg-python==<versionspec>  # optional helper

Wenn native Binaries (ffmpeg/ffprobe, mkvmerge) benötigt werden, werden diese
entweder über das CI-Image/Container installiert oder lokal über das OS-Paketmanagement:
```bash
# Debian/Ubuntu Beispiel
sudo apt-get update && sudo apt-get install -y ffmpeg mkvtoolnix
```

## 7) CI-Empfehlung
- Erstelle ein dediziertes Test-Image (Docker) oder erweitere CI-Runner um die
  native Binaries und `pip install -r requirements-test.txt` vor dem Testlauf.
- Alternativ: Markiere Integrationstests mit `@pytest.mark.integration` und führe
  diese nur in der Integration-Stage mit spezifizierter Infrastruktur aus.

## 8) Troubleshooting Tipps
- Wenn ein Import anders ist als erwartet, drucke `module.__file__` und `sys.path`.
- Prüfe `pip list` in deinem test-venv; entferne konfliktäre globale Installs.
- Verwende `python -m pip uninstall <pkg>` und dann `pip install -e .` erneut.

---

Datei erstellt: docs/IMPORT_SHADOWING_AND_TEST_VENV.md
