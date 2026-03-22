# Logbuch: Anpassung der Cover Items – Seitenverhältnis nach Medientyp

**Datum:** 17. März 2026

## Ziel: Dynamische Cover-Größe und Seitenverhältnis je nach Medientyp

### Änderungen & Umsetzung

- Cover-Items werden dynamisch angepasst:
  - **Audio/CD:** Rechteckiges Format (z.B. 1:1 oder 4:3), orientiert an echten CD-Covern
  - **Film/Video:** Hochkant oder 16:9, je nach typischem Seitenverhältnis
  - **Online Stores:** Unterstützung für weitere Formate (z.B. quadratisch, Banner, Portrait)
- Logik im Frontend:
  - Seitenverhältnis und Größe werden anhand des File-Typs (audio, video, image, disk) gesetzt
  - CSS-Klassen und Container werden dynamisch zugewiesen
  - Optionale Anpassung für Artwork aus Online-Quellen
- Ziel: Realistische Darstellung, bessere UX und optische Differenzierung

---

## Verifikationsplan

- Manuelle Verifikation:
  - Verschiedene Medientypen in der Bibliothek prüfen
  - Seitenverhältnis und Größe der Cover-Items vergleichen
  - Darstellung auf verschiedenen Bildschirmgrößen testen

---

Weitere Details siehe vorherige Logbuch-Einträge und Testskripte.
