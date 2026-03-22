# Logbuch: DVD-Erkennung & Medienobjekt-Handling (März 2026)

## Übersicht
Die Media-Library-App erkennt und behandelt DVD-Medien in drei Varianten, um maximale Kompatibilität und korrekte Wiedergabe zu gewährleisten.

---

## 1. DVD-Varianten
- **a) Einzelne .iso-Datei (Image):**
    - Wird direkt an VLC übergeben (ohne dvd://-Prefix).
    - Vorteil: Einfache Handhabung, keine Entpackung nötig.
- **b) Ungepackter Ordner mit VIDEO_TS-Struktur:**
    - Muss die nötigen IFO/BUP/VOB-Dateien enthalten.
    - Wird mit dvd://-Prefix an VLC übergeben.
    - Vorteil: Kompatibel mit DVD-Playback, aber Struktur muss vollständig sein.
- **c) Film-Objekt-Ordner (Name Jahr, Cover, ISO):**
    - Enthält Metadaten, Cover und meist eine .iso.
    - Wird als einzelnes Filmobjekt behandelt, die .iso für die Wiedergabe genutzt.
    - Vorteil: Zentrale Darstellung, Metadaten und Cover für UI.

---

## 2. Scan- und Playback-Logik
- Beim Scan:
    - Unterscheidung zwischen .iso, VIDEO_TS-Ordner und Film-Objekt-Ordner.
    - Film-Objekt-Ordner werden als "Film"-MediaItem indexiert.
- Playback:
    - .iso → VLC direkt (ohne dvd://)
    - VIDEO_TS-Ordner → VLC mit dvd://
    - Film-Objekt-Ordner → Metadaten anzeigen, .iso für Wiedergabe nutzen

---

## 3. Vorteile & Empfehlungen
- Alle Varianten werden korrekt erkannt und abgespielt.
- UI zeigt Cover, Jahr und weitere Metadaten für Film-Objekte.
- Empfehlung: Bei Problemen mit DVD-Ordnern prüfen, ob VIDEO_TS und die nötigen Dateien vorhanden sind.

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
