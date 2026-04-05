# Logbuch: Fehlerbehandlung – Defekte Dateien & ISO-Images (2026-03-15)

**Datum:** 2026-03-15

## Problemstellung
Beim Einlesen defekter Mediendateien oder ISO-Images kann das Programm blockieren oder hängen bleiben. Dies betrifft insbesondere Parser, die auf fehlerhafte Container, beschädigte Sektoren oder inkompatible Formate stoßen.

## Maßnahmen & Empfehlungen
- **Fehlerquellen:**
  - Defekte Audio-/Videodateien (CRC-Fehler, unvollständige Downloads, beschädigte Container)
  - ISO-Images, die nicht gemountet oder gelesen werden können
  - Parser, die auf Endlosschleifen oder Timeouts laufen
- **Empfohlene Fehlerbehandlung:**
  - Alle Datei- und ISO-Leseoperationen mit try/except-Block absichern
  - Timeouts für externe Tools (ffprobe, mutagen, vlc, etc.) setzen
  - Fehlerhafte Dateien im UI und Logbuch als "defekt" markieren, nicht blockierend behandeln
  - Parser-Fehler und IO-Exceptions explizit loggen (inkl. Dateiname und Exception-Text)
  - Optional: Defekte Dateien in eine separate Liste aufnehmen ("Fehlerhafte Medien")

## Beispiel (Python):
```python
try:
    # Datei öffnen/parsen
    ...
except (IOError, OSError, Exception) as e:
    logger.error(f"Fehler beim Lesen: {file_path}: {e}")
    # Datei als defekt markieren, ggf. im UI anzeigen
```

## Ergebnis
Das Programm bleibt bei defekten Dateien und ISO-Images reaktionsfähig. Fehler werden sauber abgefangen, dokumentiert und im UI sichtbar gemacht. Keine Blockade oder Hänger mehr durch fehlerhafte Medien.

---

*Letzte Änderung: 2026-03-15*
