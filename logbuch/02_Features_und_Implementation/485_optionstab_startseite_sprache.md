# UI-Verbesserung: Start-Seite & Sprache in Optionen-Tab

**Datum:** 15.03.2026

## Änderungen
- **Start-Seite umgezogen:** Die Auswahl für die Start-Seite befindet sich jetzt am Ende der linken Spalte im Optionen-Tab (nicht mehr im Video-Player-Tab).
- **Beschriftungen fixiert:**
  - Die Sprachauswahl ist jetzt mit „Sprache / Language“ beschriftet.
  - Die Start-Seiten-Auswahl ist mit „Start-Seite“ beschriftet.
- **Zentralisierung:** Beide Einstellungen sind im neuen Bereich „Allgemeine Einstellungen“ im Optionen-Tab zusammengefasst.
- **i18n ergänzt:** Der Schlüssel `options_start_page` wurde in `web/i18n.json` für Deutsch und Englisch ergänzt.
- **Struktur geprüft:** Die neue Struktur wurde durch den Integrationstest `tests/integration/ui/test_ui_structure.py` verifiziert und ist konsistent.

## Ergebnis
- Übersichtliche, zentralisierte Einstellungen für Sprache und Start-Seite im Optionen-Tab.
- Korrekte Beschriftungen und vollständige Lokalisierung.
- Layout und Funktionalität durch automatisierten Test abgesichert.
