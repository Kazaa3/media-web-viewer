# Fix: Logging-Fehler & UI-Optimierung (VLC/Optionen)

**Datum:** 15.03.2026

## Fehlerbehebung (Logging)
- **AttributeError behoben:** Die Methode `logger.get_ui_logger()` existierte nicht und führte in `play_vlc` zu einem Absturz.
- **Fix:** Alle Vorkommen wurden auf die korrekte Methode `logger.get_logger("vlc")` umgestellt.
- **Stabilität:** Fehler beim Starten des VLC-Players werden jetzt sauber abgefangen und sowohl im Backend-Log (app.vlc) als auch im UI-Logbuch protokolliert.

## UI & UX Optimierungen
- **Video-Player Tab:** Der Startseiten-Selector wurde aus dem Header entfernt, das Layout ist aufgeräumter.
- **Optionen-Tab:**
  - Start-Seite und Sprache sind jetzt zentral unter „Allgemeine Einstellungen“.
  - Alle Optionen haben klare Labels.
  - Übersetzungen für `options_start_page` wurden in `web/i18n.json` ergänzt.
- **Test-Absicherung:** Das Backend startet fehlerfrei und die UI-Struktur ist durch den Integrationstest `tests/integration/ui/test_ui_structure.py` abgesichert.

## Ergebnis
- Logging und Fehlerbehandlung im VLC-Kontext sind robust.
- Die UI ist übersichtlich, konsistent und internationalisiert.
- Die Anwendung läuft stabil in der lokalen Umgebung.
