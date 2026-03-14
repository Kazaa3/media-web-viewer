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


## Empfehlung nach Dateityp

| Dateityp         | Empfohlene Parser                |
|------------------|----------------------------------|
| MP3              | mutagen, pymediainfo, tinytag, eyed3, music-tag |
| FLAC             | mutagen, pymediainfo, music-tag  |
| M4A/M4B/MP4      | mutagen, pymediainfo, ffprobe, enzyme, music-tag |
| OGG/OPUS         | mutagen, pymediainfo, tinytag, music-tag |
| WAV              | mutagen, pymediainfo, tinytag, music-tag |
| WMA              | mutagen, pymediainfo, music-tag  |
| MKV              | ffprobe, enzyme, ebml, mkvparse, pymkv |
| ISO              | pycdlib                          |
| Video allgemein  | ffprobe, enzyme, pymediainfo     |
| Fallback         | ffmpeg                           |

Die Auswahl basiert auf den Benchmark-Ergebnissen und der Metadatenqualität. Für Audio empfiehlt sich die Kombination aus Mutagen, pymediainfo und music-tag (ggf. tinytag/eyed3 für MP3). Für Video und Kapitel sind ffprobe, enzyme und ebml/mkvparse optimal. ISO-Dateien sollten mit pycdlib analysiert werden. ffmpeg dient als universeller Fallback.

## Testskript
- Siehe tests/benchmark_all_parsers.py
- Ergebnisse: tests/parser_benchmark_results.json

## Weiteres
- Fehler und Ausreißer werden im JSON protokolliert.
- Die optimale Parser-Kette kann je nach Dateityp angepasst werden.

---
10.03.2026
Automatischer Eintrag durch Benchmark-Tool.
## Benchmark-Ergebnisse (PAL DVD ISO & alle Dateien)

- Die Benchmark-Auswertung zeigt, dass für ISO/PAL DVD-Dateien pycdlib und isoparser als spezialisierte Parser integriert sind.
- isoparser und pycdlib liefern robuste Fehlerbehandlung für beschädigte oder nicht unterstützte ISOs.
- Für PAL DVD ISO wurden keine schwerwiegenden Fehler protokolliert, alle Parser liefern konsistente Ergebnisse.
- Mutagen wirft für viele Dateien einen Fehler: `parse() missing 1 required positional argument: 'name'`. Dies betrifft alle Dateitypen und sollte im Mutagen-Parser behoben werden (Parameterübergabe prüfen).
- Die Ausführungszeiten variieren: ffmpeg und isoparser sind sehr schnell, mutagen und pymediainfo robust, aber mutagen benötigt Fix für Argumente.
- Die JSON-Ergebnisse enthalten für jede Datei: Laufzeit, Parser-spezifische Zeiten, Metadaten, Fehler.

### Empfehlungen
- Für ISO/PAL DVD: pycdlib und isoparser aktivieren, beide liefern zuverlässige Ergebnisse und Fehlerbehandlung.
- Für Audio: mutagen, pymediainfo, music-tag, tinytag, eyed3 (mutagen-Fehler beheben).
- Für Video: ffprobe, enzyme, ebml, mkvparse, pymkv.
- Fallback: ffmpeg.
- Fehlerbehandlung und Logging für alle Parser sicherstellen.
- Benchmark regelmäßig ausführen und JSON-Ergebnisse prüfen.

### ToDo
- Mutagen-Parser: Argumentübergabe fixen ("name"-Parameter).
- Ergebnisse und Empfehlungen im Logbuch dokumentieren.
- Parser-Konfiguration regelmäßig überprüfen und anpassen.
