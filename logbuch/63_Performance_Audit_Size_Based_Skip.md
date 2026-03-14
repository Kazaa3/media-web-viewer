# Logbuch-Eintrag: Build-Time Performance Audit – Size-Based Parser Optimization

## Ziel
Sicherstellung, dass speicherintensive Parser (pymediainfo, pycdlib, isoparser) bei großen ISO-Dateien (>500MB) automatisch übersprungen werden, um Performance-Audits zuverlässig und ressourcenschonend durchzuführen.

## Konzept & Umsetzung
- **Zentralisierte Skip-Logik:**
  - In `_extract_metadata_internal` wurde eine zentrale Logik implementiert, die für alle relevanten Parser (pymediainfo, pycdlib, isoparser) greift.
  - ISO-Dateien >500MB werden von diesen Parsern automatisch ausgeschlossen.
- **Performance Audit:**
  - Audit-Skript (`infra/build_system.py --audit-performance`) nutzt die neue Logik und kann große ISOs (z.B. 1.2GB) ohne Speicherprobleme verarbeiten.
  - Fortschritt und Skip-Entscheidungen werden im Audit-Log dokumentiert.
- **Code Cleanup:**
  - Doppelte oder verteilte pymediainfo-Logik wurde entfernt und in den zentralen Block verlagert.
  - Die Hauptschleife in `media_parser.py` wurde auf konsistente Skip-Logik geprüft.

## Verification Plan
- **Audit Execution:** Performance-Audit mehrfach ausgeführt, um die Stabilität und Geschwindigkeit bei großen ISOs zu bestätigen.
- **Log Review:** Skip-Entscheidungen und Parser-Bypass werden im Audit-Log korrekt ausgegeben.
- **Memory Monitoring:** Kein Speicherüberlauf oder Hänger bei großen Disk-Images.

## Status
Abgeschlossen – Performance-Audit ist jetzt robust, ressourcenschonend und für große Medienbestände geeignet.

## Stand
13. März 2026
