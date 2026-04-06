# Logbuch v1.37.47 – Pathlib vs. os.path Performance

**Datum:** 2026-04-06

## Einordnung: Pathlib vs. os.path

### 1. Objekt-Overhead
- **os.path:** Arbeitet direkt mit Strings und nutzt C-Funktionen. Sehr schnell, minimaler Overhead.
- **pathlib:** Objektorientiert, jeder Path(...) erzeugt ein Python-Objekt. Etwas langsamer, da Methoden aufgerufen werden.

### 2. Benchmark (Beispiel)
- 100.000 Pfad-Operationen:
  - `os.path.exists()`: ca. 0.1–0.2 Sekunden
  - `Path.exists()`: ca. 0.4–0.6 Sekunden
- Faktor: pathlib ist ca. 2–5x langsamer, aber immer noch im Sub-Sekundenbereich.

### 3. Warum pathlib trotzdem nutzen?
- **Sicherheit:** Path.resolve() und Path.joinpath() behandeln Sonderzeichen (#, Leerzeichen) automatisch korrekt. Kein manuelles Escaping nötig.
- **Robustheit:** Pfad-Komposition mit `/`-Operator verhindert Fehler durch fehlende Slashes.
- **Lesbarkeit:** Code ist klarer und wartbarer.

### 4. Praxis-Benchmark (dein System)
```python
import os
import time
from pathlib import Path
iterations = 50000
test_path = "/home/xc/#Coding/gui_media_web_viewer/src/core/main.py"
# os.path
start = time.time()
for _ in range(iterations):
    os.path.exists(test_path)
    os.path.dirname(test_path)
os_time = time.time() - start
# pathlib
start = time.time()
for _ in range(iterations):
    p = Path(test_path)
    p.exists()
    p.parent
pathlib_time = time.time() - start
print(f"OS Path: {os_time:.4f}s")
print(f"Pathlib: {pathlib_time:.4f}s")
print(f"Faktor:  {pathlib_time/os_time:.1f}x")
```

### 5. Fazit
- Für typische Anwendungsfälle (z.B. resolve_media_path beim Laden/Abspielen) ist der Unterschied vernachlässigbar (Mikrosekunden).
- **Empfehlung:** pathlib ist die sicherere und modernere Wahl, besonders bei "unbequemen" Zeichen wie # im Pfad.

---
**Status:** Pathlib-Umstellung ist performant und erhöht die Robustheit der App (v1.37.47)
