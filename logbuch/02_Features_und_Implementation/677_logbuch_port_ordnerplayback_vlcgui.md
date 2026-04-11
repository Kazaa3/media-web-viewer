# Logbuch: Port-Änderung, Ordner-Playback & VLC-GUI-Integration (März 2026)

## Zusammenfassung
Alle geplanten Verbesserungen für Port-Management, Ordner-Playback und die Integration externer Player in die GUI wurden erfolgreich umgesetzt. Die App ist jetzt robuster, benutzerfreundlicher und unterstützt mehr Medienvarianten.

---

## 1. Statischer Port 8345
- Standardport im Backend (main.py) und in allen Tests von 8080 auf 8345 geändert.
- Die App ist immer unter http://localhost:8345/app.html erreichbar – ideal für Bookmarks und parallele Instanzen.
- Bei Port-Konflikt: Warnung im Log, automatischer Fallback auf freien Port.

## 2. Ordner-Playback für MP4/MKV/AVI
- Die Logik in `resolve_dvd_bundle_path` wurde erweitert:
    - Wird ein Verzeichnis als "Filmobjekt" erkannt, das eine .mp4, .mkv oder .avi enthält (statt ISO/VIDEO_TS), wird diese Datei jetzt korrekt als Film abgespielt.
    - Drag & Drop und GUI-Auswahl funktionieren jetzt auch für "flache" Video-Ordner.

## 3. VLC Zwei Pop-Ups & GUI-Integration
- Das Problem mit doppelten VLC-Popups (python-vlc + cvlc) ist gelöst.
- Bei externem Playback (ISO/DVD):
    - Die Video-GUI blendet sich nicht mehr einfach aus, sondern zeigt einen klaren Hinweis "Extern Player aktiv" und "Das Video läuft nun in einem eigenen Fenster. Die GUI wartet hier".
    - Klick auf "VLC Beenden" (Stop) beendet das externe VLC-Fenster zuverlässig.
- Verbesserte Fehler- und Aktivitätsbenachrichtigungen in der Benutzeroberfläche.

---

## 4. Weitere Hinweise
- Die Web App ist ab sofort immer unter http://localhost:8345/app.html erreichbar.
- Alle Änderungen wurden getestet und funktionieren wie erwartet.

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
