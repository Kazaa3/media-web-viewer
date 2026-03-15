# Logbuch: Fehlerbehandlung – Blockierende Kopiervorgänge & Dateizugriff (2026-03-15)

**Datum:** 2026-03-15

## Problemstellung
Kopiervorgänge (z.B. große Dateiübertragungen, System- oder Netzwerk-Copy-Prozesse) können den Zugriff auf Mediendateien blockieren. Das führt dazu, dass das Programm beim Versuch, solche Dateien zu lesen, ebenfalls blockiert oder sehr langsam wird. Besonders kritisch ist dies bei Netzwerkpfaden, USB-Medien oder parallelen Systemoperationen.

## Maßnahmen & Empfehlungen
- **Fehlerquellen:**
  - Datei wird gerade kopiert oder von einem anderen Prozess exklusiv gehalten
  - Netzwerk- oder USB-Laufwerke mit langsamer oder unterbrochener Verbindung
  - System-Locks (z.B. Windows: "Datei wird verwendet")
- **Empfohlene Fehlerbehandlung:**
  - Vor dem Lesen prüfen, ob die Datei exklusiv geöffnet werden kann (sofern OS unterstützt)
  - Timeouts und asynchrone Zugriffsversuche für Dateioperationen nutzen
  - IO-Operationen in separaten Threads/Prozessen ausführen, um das Hauptprogramm nicht zu blockieren
  - Fehler und Zugriffsprobleme im Logbuch und UI anzeigen (z.B. "Datei wird gerade kopiert oder ist gesperrt")
  - Optional: Retry-Mechanismus mit Backoff für temporär blockierte Dateien

## Beispiel (Python):
```python
import os
import time

def is_file_accessible(path, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with open(path, 'rb'):
                return True
        except (IOError, OSError):
            time.sleep(0.5)
    return False
```

## Ergebnis
Das Programm bleibt auch bei blockierten oder kopierten Dateien reaktionsfähig. Zugriffsprobleme werden erkannt, sauber abgefangen und dem Nutzer gemeldet. Keine Hänger mehr durch System- oder Netzwerk-Locks.

---

*Letzte Änderung: 2026-03-15*
