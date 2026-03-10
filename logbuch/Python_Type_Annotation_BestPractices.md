# Python Type-Annotationen & Best Practices (.md)

## Übersicht
Type-Annotationen verbessern Lesbarkeit, Fehlerdiagnose und Codequalität – besonders mit Pylance und Flake8. Hier die wichtigsten Typen, Dict-Varianten und Tools.

---

## Type-Annotationen (PEP 484)
- **Funktion:**
  ```python
  def add(a: int, b: int) -> int:
      return a + b
  ```
- **Variable:**
  ```python
  x: float = 3.14
  name: str = "Media"
  ```
- **Optional:**
  ```python
  from typing import Optional
  def get_title(meta: dict) -> Optional[str]:
      return meta.get('title')
  ```

---

## Dict-Typen
- **Standard Dict:**
  ```python
  from typing import Dict
  meta: Dict[str, str] = {'title': 'Song', 'artist': 'Max'}
  ```
- **Nested Dict:**
  ```python
  from typing import Dict, Any
  features: Dict[str, Any] = {'mfcc': [0.1, 0.2], 'meta': {'title': 'Song'}}
  ```
- **TypedDict (PEP 589):**
  ```python
  from typing import TypedDict
  class MetaDict(TypedDict):
      title: str
      artist: str
  meta: MetaDict = {'title': 'Song', 'artist': 'Max'}
  ```

---

## Weitere Typen
- **List:**
  ```python
  from typing import List
  tracks: List[str] = ['Intro', 'Outro']
  ```
- **Tuple:**
  ```python
  from typing import Tuple
  size: Tuple[int, int] = (1920, 1080)
  ```
- **Union:**
  ```python
  from typing import Union
  value: Union[int, str] = 42
  ```

---

## Bugfix: (Hörbuch) hinter Auto bei Hörbücher

### Problem
- Bei Hörbüchern wird im Index/Anzeige "Auto" statt "Hörbuch" angezeigt.

### Lösung
- Typen-Erkennung anpassen: Wenn Dateiendung oder Metadaten auf Hörbuch hindeuten, Typ explizit auf "Hörbuch" setzen.
- Im UI und Index "Hörbuch" korrekt anzeigen.

### Beispiel-Code (Python)
```python
def detect_type(file_path):
    ext = Path(file_path).suffix.lower()
    if ext in ['.m4b', '.aax', '.aa', '.mp3'] and 'audiobook' in str(file_path).lower():
        return 'hörbuch'
    # ...restliche Typen...
```

### ToDo
- Test: Scan mit Hörbuch-Dateien
- UI-Feedback für "Hörbuch"-Typ
- Dokumentation im Indexierungs-Logbuch

---

## Flake8 & Typ-Checks
- **Flake8:** Linter für Style, Fehler, Typen
  ```bash
  pip install flake8
  flake8 myfile.py
  ```
- **mypy:** Statische Typprüfung
  ```bash
  pip install mypy
  mypy myfile.py
  ```
- **Pylance:** Echtzeit-Typprüfung in VS Code

---

## Best Practices
- Immer Typen für Funktionen und Variablen angeben
- TypedDict für strukturierte Dicts
- Optional/Union für flexible Typen
- Flake8/mypy regelmäßig nutzen
- Docstrings für Funktionen ergänzen

---

**Fragen/Feedback:**
- Weitere Beispiele für TypedDict, Union oder Flake8-Konfiguration gewünscht?
