# Logbuch: VLC 3.0.23 Vetinari – Fehleranalyse & Hinweise (2026-03-15)

**Datum:** 2026-03-15

## Systemumgebung
- **VLC-Version:** 3.0.23 Vetinari (revision 3.0.23-2-0-g79128878dd)

## Beobachtete Log-Ausgaben
```
[000055c59119c550] main libvlc: VLC wird mit dem Standard-Interface ausgeführt. Benutzen Sie 'cvlc', um VLC ohne Interface zu verwenden.
[00007f8bdc001170] mjpeg demux error: cannot peek
```

## Analyse & Hinweise
- **Standard-Interface:**
  - VLC wurde mit GUI gestartet. Für Headless-/Serverbetrieb empfiehlt sich der Start mit `cvlc` (ohne grafische Oberfläche).
- **mjpeg demux error: cannot peek:**
  - Dieser Fehler tritt auf, wenn VLC einen MJPEG-Stream nicht korrekt einlesen kann (z.B. bei beschädigten Streams, inkompatiblen Quellen oder Netzwerkproblemen).
  - In der Regel ist dies ein Warnhinweis und blockiert die Wiedergabe anderer Formate nicht, kann aber auf fehlerhafte oder nicht unterstützte MJPEG-Quellen hindeuten.

## Empfehlungen
- Für automatisierte oder serverseitige Nutzung immer `cvlc` statt `vlc` verwenden.
- Bei wiederholten "cannot peek"-Fehlern die Quelle/Datei prüfen (z.B. auf Integrität, Format, Netzwerkzugriff).
- Fehler im Logbuch dokumentieren und ggf. als Warnung im UI anzeigen, falls die Wiedergabe betroffen ist.

---

*Letzte Änderung: 2026-03-15*
