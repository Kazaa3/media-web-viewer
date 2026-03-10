# Logbuch-Eintrag: Parser-Benchmark Vergleich

## Ziel
Alle verfügbaren Parser-Module (filename, container, mutagen, pymediainfo, ffprobe, ffmpeg, ebml, mkvparse, enzyme, pycdlib, pymkv, tinytag, eyed3, music-tag) werden auf die gleichen Mediendateien angewendet. Es werden Ausführungszeit, Metadaten und Fehler pro Datei und Parser verglichen.

## Vorgehen
- Benchmark-Skript im tests-Ordner: Führt alle Parser auf alle Dateien im media-Ordner aus.
- Ergebnisse: JSON-Datei mit Zeit, Metadaten und Fehler pro Datei und Parser.
- Ziel: Optimale Parser-Kombination für verschiedene Formate und Performance identifizieren.

## Ergebnisse (Beispiel)
- Die meisten Parser liefern für MP3 und M4B vollständige Metadaten, aber Geschwindigkeit und Fehler unterscheiden sich.
- Mutagen und pymediainfo sind für Audio schnell und robust, ffprobe liefert für Video und Kapitel die besten Ergebnisse.
- Tinytag und eyed3 sind für MP3 sehr schnell, aber weniger umfassend.
- ffmpeg ist als Fallback nützlich, aber langsam.

## Empfehlung
- Für Audio: Mutagen, pymediainfo, tinytag, eyed3.
- Für Video/Kapitel: ffprobe, enzyme, ebml, mkvparse.
- Für ISO: pycdlib.
- Für allgemeine Robustheit: Fallback auf ffmpeg.

## Testskript
- Siehe tests/benchmark_all_parsers.py
- Ergebnisse: tests/parser_benchmark_results.json

## Weiteres
- Fehler und Ausreißer werden im JSON protokolliert.
- Die optimale Parser-Kette kann je nach Dateityp angepasst werden.

---
10.03.2026
Automatischer Eintrag durch Benchmark-Tool.
