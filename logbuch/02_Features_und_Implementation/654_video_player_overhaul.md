# Video Player Overhaul: Neue Funktionen, Öffnen mit & Streaming/Datei-Unterstützung

**Datum:** 18.03.2026

## Überblick
Mit dem großen Video-Player-Overhaul erhält der Media Web Viewer eine umfassend modernisierte und flexiblere Videowiedergabe. Im Fokus stehen die Unterstützung verschiedener Dateitypen, neue Streaming-Optionen und ein verbessertes "Öffnen mit"-Verhalten für lokale und entfernte Medienquellen.

---

## 1. "Öffnen mit"-Funktion: Flexibilität beim Medienstart
- Medien können direkt aus dem Dateisystem per "Öffnen mit Media Web Viewer" gestartet werden.
- Die App erkennt automatisch den Medientyp (Video, Audio, Playlist) und wählt den passenden Player-Modus.
- Unterstützung für Drag & Drop von Dateien in die Oberfläche.
- Verbesserte Fehlerbehandlung bei nicht unterstützten oder beschädigten Dateien.

## 2. Unterschiedliche Streaming- und Datei-Unterstützung
### Lokale Dateien
- Direkte Wiedergabe von gängigen Videoformaten (MP4, MKV, AVI, MOV, u.a.).
- Unterstützung für Untertitel und Kapitel (sofern im Container vorhanden).
- Optimierte Performance für große Dateien und hohe Bitraten.

### Netzwerk-Streaming
- Unterstützung für HTTP/HTTPS-Streams (z.B. MP4, HLS/m3u8, DASH).
- SMB/NFS (Netzwerkfreigaben) werden erkannt und können direkt abgespielt werden.
- Fortschrittliche Fehlerbehandlung bei Netzwerkunterbrechungen.

### Erweiterte Formate & Spezialfälle
- Experimentelle Unterstützung für exotische Formate (z.B. DVD-ISOs, Blu-ray-Ordnerstrukturen).
- Automatische Fallback-Strategien, falls ein Format nicht direkt unterstützt wird (z.B. Transcoding via FFmpeg).

## 3. Verbesserte Benutzeroberfläche & Bedienung
- Modernisiertes Player-UI mit intuitiven Steuerelementen.
- Schneller Wechsel zwischen Datei- und Streaming-Modus.
- Anzeige von Metadaten, Cover-Art und technischen Details während der Wiedergabe.
- "Weiter ab letzter Position"-Funktion für angefangene Videos.

## 4. Technische Highlights
- Modularer Backend-Parser erkennt und verarbeitet verschiedene Medienquellen.
- Fehlerrobuste Pipeline: Bei Problemen mit einem Format wird automatisch ein alternativer Pfad versucht.
- Optimierte Integration mit VLC und FFmpeg für maximale Kompatibilität.

---

## Fazit
Der Video-Player-Overhaul macht den Media Web Viewer zu einem vielseitigen und robusten Tool für unterschiedlichste Medienquellen. Egal ob lokale Datei, Netzwerkstream oder exotisches Format – die App bietet maximale Flexibilität und Komfort beim Medienkonsum.

---

*Siehe auch: Parser-Pipeline, Netzwerk-Streaming, Medienformat-Unterstützung in der Projektdokumentation.*
