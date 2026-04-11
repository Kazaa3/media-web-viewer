# Logbuch MS: AssertionError Fix & Media Library Recovery (v1.35.68)

## Zusammenfassung
- **AssertionError behoben:** Die Anwendung stürzte ab, weil set_log_level doppelt definiert war. Die Funktion wurde jetzt konsolidiert und korrekt exponiert.
- **Leere Mediathek:** Obwohl sich 57 Dateien im ./media-Verzeichnis befinden, war die Datenbank leer. Ursache: Ein abgebrochener Scan oder ein Reset während des Upgrades.

## Wiederherstellung der Mediathek
1. Anwendung starten.
2. Optionen (Zahnrad-Icon) öffnen.
3. Zum Debug-Tab (Käfer/Bug-Icon) wechseln.
4. Im Centralized Diagnostic Hub auf DIRECT SCAN klicken.
5. Die Bibliothek wird vollständig neu eingelesen und die Playlist befüllt.

## Änderungen im Detail
- **Duplicate Exposure Fixed:** Redundante set_log_level-Definitionen in src/core/main.py entfernt und vereinheitlicht.
- **Persistence Enabled:** Loglevel-Änderungen werden jetzt korrekt im PARSER_CONFIG gespeichert und auf alle internen Handler angewendet.
- **Ready for Hydration:** Medien im ./media-Ordner erkannt und bereit für erneuten Scan.

## Status
- System stabil, alle Fehlerquellen beseitigt.
- Mediathek kann per DIRECT SCAN im Diagnostic Hub wiederhergestellt werden.
