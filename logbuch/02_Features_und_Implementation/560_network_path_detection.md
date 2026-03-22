# Logbuch: Erkennung von SMB- und Netzwerkpfaden (2026-03-15)

**Datum:** 2026-03-15

## Feature: Automatische Erkennung von Netzwerkpfaden (SMB, NFS, etc.)
- **Ziel:**
  - Netzwerkpfade (z.B. SMB/CIFS, NFS, AFP, WebDAV) automatisch erkennen und im UI sowie Backend speziell behandeln.
- **Umsetzungsvorschlag:**
  - Pfad-Parsing: Prüfen, ob ein Pfad mit `smb://`, `\\`, `/mnt/smb/`, `/Volumes/`, `nfs://` oder ähnlichen Mustern beginnt.
  - Für Windows: UNC-Pfade (`\\server\share\...`) erkennen.
  - Für Linux/macOS: Mountpoints und Protokollpräfixe auswerten.
  - Im UI Netzwerkpfade optisch hervorheben (z.B. Icon, Tooltip "Netzlaufwerk erkannt").
  - Backend kann für Netzwerkpfade spezielle Timeouts, Caching oder Bandbreitenlimits setzen.
- **Vorteile:**
  - Bessere Performance und Fehlerbehandlung bei Zugriff auf Netzlaufwerke.
  - Nutzer werden auf mögliche Latenzen oder Offline-Status hingewiesen.
  - Grundlage für gezielte Optimierungen (z.B. Low Bandwidth Modus nur für Netzwerkpfade aktivieren).

## Beispiel (Python):
```python
from pathlib import Path

def is_network_path(path):
    p = str(path)
    return (
        p.startswith('smb://') or
        p.startswith('nfs://') or
        p.startswith('afp://') or
        p.startswith('webdav://') or
        p.startswith('\\\\') or  # Windows UNC
        p.startswith('/mnt/smb/') or
        p.startswith('/Volumes/')
    )
```

## Ergebnis
- Netzwerkpfade werden automatisch erkannt und können gezielt behandelt werden.
- Die Anwendung ist robuster und benutzerfreundlicher im Umgang mit verschiedenen Speicherorten.

---

*Letzte Änderung: 2026-03-15*
