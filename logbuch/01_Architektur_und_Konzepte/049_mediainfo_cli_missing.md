# Logbuch-Eintrag: MediaInfo CLI fehlt

**Datum:** 13. März 2026

## MediaInfo CLI Status

- Die MediaInfo CLI (mediainfo) wurde im Backend als System-Tool integriert.
- Status, Pfad und Version werden im Environment-Status und der GUI angezeigt.
- Aktuelle Prüfung zeigt: MediaInfo CLI ist auf diesem System nicht installiert oder nicht im PATH verfügbar.

### Auswirkungen
- Funktionen zur Analyse von Mediendateien über die CLI stehen nicht zur Verfügung.
- Die Python-Bibliothek pymediainfo ist weiterhin nutzbar, sofern installiert.

### Lösungsvorschlag
- MediaInfo CLI kann nachinstalliert werden:
  ```bash
  sudo apt install mediainfo
  ```
- Nach Installation wird die CLI automatisch erkannt und im Status angezeigt.

---
