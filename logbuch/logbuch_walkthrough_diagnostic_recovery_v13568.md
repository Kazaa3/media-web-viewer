# Logbuch: Diagnostic Hub Expansion & Real-Time Scanner Instrumentation (v1.35.68)

## Key Improvements
- **Diagnostic Log Terminal:**
  - VS Code-Style Dark Terminal im Debug-Tab (Options Panel).
  - Streamt Live-Updates vom Backend-Scanner direkt ins UI.

- **Granulare Instrumentierung:**
  - **Extension Discovery:** Zeigt, welche Dateitypen gesucht werden (z.B. .mp3, .mkv).
  - **Folder Traversal:** Loggt jeden betretenen Ordner.
  - **Match/Skip Logic:** Meldet, welche Dateien gematcht oder übersprungen werden (inkl. Grund, z.B. Black Box DVD-Folder).
  - **DB Insertion:** Bestätigt erfolgreiche Datenbank-Commits für jedes Item.
  - **Normalized Extension Matching:** Alle Dateiendungen werden vor dem Vergleich in Kleinbuchstaben umgewandelt, um Case-Sensitivity-Probleme (z.B. FILE.MP3) zu vermeiden.

## Dokumentation
- Siehe walkthrough_diagnostic_recovery.md für eine Schritt-für-Schritt-Anleitung und Beispiel-Logs.

## Next Steps
1. App starten und zu Options > Debug navigieren.
2. DIRECT SCAN klicken.
3. Im Live Scan Activity Terminal erscheinen jetzt alle Scan-Schritte ("Inspecting matching file...", "Successfully Indexed...").
4. Bleibt der Zähler bei 0, liefert das Terminal exakte Hinweise, an welchem Schritt es scheitert.

## Status
- **Stabilisiert:** Volle Transparenz im Scan-Prozess, Case-Sensitivity-Fix integriert.
- **Bereit für weitere Fehleranalyse und Recovery.**
