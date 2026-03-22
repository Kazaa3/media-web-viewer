# Dateitypen: Video im Media Web Viewer

**Datum:** 12. März 2026

---

## Übersicht der unterstützten Video-Dateitypen

Der Media Web Viewer erkennt und behandelt verschiedene Video-Dateitypen und -Strukturen, um maximale Kompatibilität und optimale Benutzerführung zu gewährleisten.

---

### 1. ISO-Dateien
- **Beschreibung:** Disk-Images von DVDs/Blu-rays.
- **Hinweis:**
  - ISO-Dateien werden nicht mit dem internen Player verknüpft.
  - Ein Klick auf ein ISO-Item führt zur Videoengine im Videoplayer-Reiter.
  - Chromium-basierte Browser (z.B. Chrome) können keine ISOs abspielen.

### 2. Entpackte ISO-Ordner
- **Beschreibung:** Ordnerstruktur einer entpackten ISO mit VIDEO_TS oder BDMV.
- **Erkennung:**
  - Spezielle Ordnerstrukturen werden erkannt und als Filmordner behandelt.
  - Zusätzliche Metadaten und Navigationsmöglichkeiten.

### 3. Filmordner mit Metadatenstruktur
- **Beschreibung:** Ordner mit Videodateien und zugehörigen Metadaten (z.B. .nfo, Poster, Subtitles).
- **Vorteile:**
  - Verbesserte Anzeige und Navigation im UI.
  - Automatische Zuordnung von Zusatzinformationen.

### 4. MKV-transkodierte Videos
- **Beschreibung:** Videos, die aus ISO oder anderen Quellen in das MKV-Format transkodiert wurden.
- **Vorteile:**
  - Hohe Kompatibilität mit Direct Play und Streaming.
  - Optimierte Qualität und Speicherbedarf.

---

## Workflow zur Dateityp-Erkennung
1. ISO/Ordner/Filmordner/MKV werden beim Scan erkannt.
2. ISO-Items werden nicht direkt abgespielt, sondern an die Videoengine weitergeleitet.
3. Filmordner und entpackte ISOs bieten erweiterte Metadaten und Navigationsoptionen.
4. MKV-Videos werden bevorzugt für Direct Play und Streaming genutzt.

---

*Entry created: 12. März 2026*
