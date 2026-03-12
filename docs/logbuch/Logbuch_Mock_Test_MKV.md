# Mock-Test: MKV-Erzeugung

## Ziel
Automatisierte Tests für die Erzeugung von MKV-Dateien mit MKVToolNix, ohne echte Dateisystem-Operationen.

## Vorgehen
- Verwende Python `unittest.mock` für Subprocess- und Dateisystem-Mocks.
- Simuliere mkvmerge-Aufruf und prüfe, ob die Funktion korrekt arbeitet.

## Beispiel-Test
```python
import unittest
from unittest.mock import patch
from main import remux_mkvtool

class TestMKVErzeugung(unittest.TestCase):
    @patch('subprocess.run')
    def test_remux_mkvtool(self, mock_run):
        mock_run.return_value.returncode = 0
        result = remux_mkvtool('input.mkv', 'output.mkv')
        mock_run.assert_called_with(['mkvmerge', '-o', 'output.mkv', 'input.mkv'], check=True, capture_output=True)
        self.assertEqual(result, 'output.mkv')

if __name__ == '__main__':
    unittest.main()
```

## Vorteile
- Keine echten Dateien nötig
- Testet Logik und Fehlerbehandlung

## Hinweis: 0 MB-Dateien im Streaming-Test

- 0 MB (leere) MKV-Dateien sind für Streaming-Tests ungeeignet.
- Browser und Player erkennen sie als ungültig oder nicht abspielbar.
- Für automatisierte Tests sollten Dummy-Dateien mit minimalem, aber gültigem Container-Header erzeugt werden.
- Alternativ: Mock-Objekte und Subprocess-Mocks verwenden, um Dateigröße und Inhalt zu simulieren.

**Empfehlung:**
- Immer eine gültige, kleine MKV-Datei als Test-Asset verwenden (z. B. mit mkvmerge aus einem kurzen Video).
- Streaming-Logik auf Fehlerbehandlung für leere Dateien testen.

## MKVToolNix Parser

- MKVToolNix bietet mit `mkvinfo` und `mkvmerge` leistungsfähige Parser für MKV-Dateien.
- In Media Web Viewer kann ein Python-Wrapper (z. B. via `subprocess`) genutzt werden, um Metadaten, Tracks, Kapitel und Tags auszulesen.

**Beispiel:**
```python
import subprocess

def parse_mkv(file_path):
    result = subprocess.run(['mkvinfo', file_path], capture_output=True, text=True)
    return result.stdout
```

- Für automatisierte Tests: Parser-Funktionen mocken, um verschiedene MKV-Strukturen zu simulieren.
- Parser-Integration: Kombinierbar mit anderen Tools (ffprobe, mutagen) für umfassende Metadaten-Analyse.

**Empfehlung:**
- Parser modular halten, Fehlerbehandlung für ungültige oder leere Dateien implementieren.

---
