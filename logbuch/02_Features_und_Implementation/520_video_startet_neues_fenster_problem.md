# Logbuch: Video startet im neuen Chrome-Fenster statt im Webplayer

## Problem
- Beim Start eines Videos im Webplayer öffnet sich das Video in einem neuen Chrome-Fenster, anstatt im eingebetteten Player der Web-Oberfläche zu starten.

## Mögliche Ursachen
- Das Video wird per Link (`<a href="video.mp4" target="_blank">`) oder Download-Button geöffnet, nicht per `<video>`-Tag eingebettet.
- Im JavaScript wird `window.open()` oder ein ähnlicher Mechanismus verwendet, um das Video zu starten.
- Die Server-Response-Header (z.B. Content-Disposition) sind so gesetzt, dass der Browser das Video als Download oder externes Dokument behandelt.
- MIME-Typ ist nicht korrekt (z.B. nicht `video/mp4`), sodass der Browser das Video nicht einbetten kann.

## Lösungsideen
- Sicherstellen, dass das Video im HTML per `<video src="..." controls></video>` eingebettet wird.
- Im JavaScript keine `window.open()`- oder `target="_blank"`-Mechanismen für den Videostart verwenden.
- Server-Response-Header prüfen: `Content-Type` muss korrekt sein, `Content-Disposition` sollte nicht auf `attachment` stehen.
- Testen, ob das Problem browserübergreifend auftritt oder nur in Chrome.

## ToDo
- Video-Player-Implementierung im Frontend prüfen (HTML/JS)
- Server-Response-Header für Video-Requests kontrollieren
- Test mit verschiedenen Videoformaten und Browsern durchführen
- Logbuch-Eintrag bei Lösung aktualisieren

---

**Siehe auch:**
- web/, src/core/main.py, API-Endpoints für Medien
- Logbuch: Webplayer-Integration, MIME-Typen
