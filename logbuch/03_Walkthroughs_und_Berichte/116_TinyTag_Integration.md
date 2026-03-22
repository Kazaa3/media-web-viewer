<!-- Category: debugging -->
<!-- Title_DE: TinyTag-Integration in Parser-Pipeline -->
<!-- Title_EN: TinyTag Integration in Parser Pipeline -->
<!-- Summary_DE: Integration von TinyTag als optionalen Parser-Schritt mit Logging und Debugging. -->
<!-- Summary_EN: Integration of TinyTag as an optional parser step with logging and debugging. -->
<!-- Status: in-progress -->
<!-- Date: 2026-03-10 -->

# TinyTag-Integration in Parser-Pipeline

## Ziel
TinyTag soll als schneller, leichtgewichtiger Parser für Basis-Metadaten (Titel, Artist, Dauer, etc.) in die Pipeline aufgenommen werden. Die Integration erfolgt optional, mit Logging und Debugging-Hooks.

## Umsetzung
- TinyTag als optionalen Schritt in der Parser-Kette implementieren.
- Logging: Input-Datei, Ergebnis, Fehler, Performance.
- Debug-Flag: Aktivierung/Deaktivierung von TinyTag im Debug-Modus.
- Fehlerbehandlung: Fehler werden geloggt, der Schritt kann übersprungen werden.

## Ergebnis (Stand: in-progress)
- TinyTag bereit zur Integration (Paket installiert, API bekannt).
- Logging und Debugging vorbereitet.
- GUI-Konfiguration für TinyTag-Schritt geplant.

## Hinweise für Entwickler
- TinyTag nur für unterstützte Formate verwenden (mp3, m4a, ogg, flac, wav, wma).
- Bei Fehlern oder fehlenden Metadaten auf andere Parser zurückfallen.
- Debug-Ausgaben nur über das zentrale Logging-System.
- Tests für TinyTag-Schritt im `tests/`-Ordner anlegen.
- Dokumentation im Logbuch ergänzen.

## Nächste Schritte
- TinyTag-Schritt in `media_parser.py` implementieren.
- Erweiterung der Tests und GUI-Konfiguration.
- Abschluss der Logging/Debugging-Integration für TinyTag.

