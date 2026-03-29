# Logbuch: Dateimanager-Umstrukturierung – Multi-Window & Folder Views

**Datum:** 17. März 2026

## Ziel: Dateimanager als "File / Datei" mit mehreren Fenstern und Ordneransichten

### Änderungen & Umsetzung

- Der Dateimanager wird als "File / Datei"-Tab geführt.
- Mehrere Fenster/Ansichten möglich:
  - Hauptansicht: Übersicht aller Dateien und Ordner
  - Ordneransicht: Separate Fenster für einzelne Ordner (z.B. DVD-Strukturen, Musik-Alben)
  - Detailansicht: Metadaten, Tags, Pfad, Artwork
- UI-Logik:
  - Tabs/Sub-Tabs für verschiedene Fenster und Ordner
  - Flexibles Layout für parallele Navigation und Vergleich
  - Drag & Drop zwischen Fenstern/Ordnern möglich
- CSS/JS:
  - Dynamische Container für mehrere Ansichten
  - Responsive Design für Desktop und Tablet
- Lokalisierung:
  - i18n.json um neue Fenster/Ordner-Labels erweitert

---

## Verifikationsplan

- Manuelle Verifikation:
  - Mehrere Fenster/Ordner öffnen und navigieren
  - Drag & Drop testen
  - Metadaten und Artwork prüfen
  - Tab- und Sub-Tab-Namen in Deutsch/Englisch kontrollieren

---

Weitere Details siehe vorherige Logbuch-Einträge und walkthrough.md.
