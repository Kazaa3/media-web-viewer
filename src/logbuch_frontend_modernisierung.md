# Logbuch – Frontend Optimization & Modernization (Meilenstein 1)

## Datum
30. März 2026

## Ziel
Optimierung und Modernisierung der Frontend-Struktur der App (app.html), um die Ladezeiten zu verbessern, die Wartbarkeit zu erhöhen und ein modernes, hochwertiges UI-Design (Glassmorphism) einzuführen.

## Geplante Änderungen
- **app.html**: Reduktion auf ein Skeleton mit globalen Komponenten (Header, Main, Footer, Sidebar). Statische Tab-Inhalte werden durch Platzhalter-Divs ersetzt. Inline-SVGs werden entfernt und durch eine externe SVG-Sprite (icons.svg) ersetzt.
- **icons.svg**: Auslagerung aller SVG-<symbol>-Definitionen aus app.html.
- **fragments/**: Auslagerung der Tab-Inhalte in einzelne HTML-Fragmente:
  - player_queue.html (Audio Player / Queue)
  - filesystem_browser.html (Dateibrowser)
  - library_explorer.html (Bibliothek/Coverflow)
  - item_inventory.html (SQLite-Repository)
  - playlist_manager.html (Playlist-Editor)
  - metadata_editor.html (Metadaten-Editor)
  - system_governance.html (Systemeinstellungen)
  - diagnostics_suite.html (Logs/Tests)
- **FragmentLoader**: Registrierung und dynamisches Nachladen aller Fragmente.
- **ui_nav_helpers.js**: Anpassung von switchTab für fragmentiertes Laden und Initialisierungshooks pro Fragment.
- **Design**: Umstellung auf Glassmorphic-Design mit modernen Farben und Animationen.

## Offene Fragen
- Schriftart: Google Fonts (z.B. Inter, Outfit) oder System-Default für Offline-Kompatibilität?
- Primäres Theme: Dunkles oder helles Glassmorphic-Design?

## Verifizierungsplan
- Automatisierte UI-Tests (js/ui_test_suite.js) für Tab-Switching und Interaktionen.
- Prüfung auf Konsolenfehler (Fragment-Loading, SVGs).
- Manuelle Überprüfung der Tabs, UI-Konsistenz und SVG-Icons.

## Status
Warten auf User-Feedback zu Schriftart und Theme. Umsetzung nach Freigabe.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
