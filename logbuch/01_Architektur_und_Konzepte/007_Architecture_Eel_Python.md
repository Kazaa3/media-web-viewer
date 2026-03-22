# 02 Architektur & Strategie: Eel vs. Electron

**Datum:** 13.03.2026
**Kategorie:** Architektur, Strategie
**Status:** ARCHIVED

---

## Die Hybrid-Entscheidung

Warum haben wir "dict" nicht in Electron geschrieben? Oder klassisch in Tkinter?

### Warum Eel?
- **Python Power:** Wir wollten volle Kontrolle über das Dateisystem und Binaries (ffprobe, mutagen), ohne Node.js-Abhängigkeiten.
- **Chrome Native:** Wir nutzen das lokal installierte Chrome, was die Distribution (DEB/RPM) massiv vereinfacht und keinen 300MB-Runtime-Bloat verursacht.
- **Frontend-Flexibilität:** Wir können modernes CSS (Glassmorphism, Flexbox) nutzen, ohne die Python-Backend-Logik zu opfern.

### Die Alternative: Tkinter/Qt
Tkinter war "zu altbacken", Qt "zu schwerfällig". Die Entscheidung für Eel ermöglichte uns, die Benutzeroberfläche so zu gestalten, dass sie wie eine moderne Web-App aussieht, während das Backend in rekursivem Dateisystem-Management glänzt. 

---

**Kommentar:**
Das Hybrid-Modell Eel + Bottle hat sich als das "Nervenzentrum" des gesamten Projekts erwiesen.
