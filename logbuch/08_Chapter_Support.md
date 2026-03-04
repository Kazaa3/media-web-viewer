<!-- Category: Parser -->

Audiobook Chapter Support
Das Ziel ist es, für Hörbücher (M4B, MKV, etc.) die hinterlegten Kapitel-Metadaten auszulesen und in der Weboberfläche übersichtlich anzuzeigen.

Proposed Changes
1. 
parsers/ffmpeg_parser.py
FFmpeg liest beim Standard-Aufruf (ffmpeg -i) bereits automatisch alle Kapitel aus und formatiert sie in die Standardausgabe (Stderr).

[MODIFY] 
parsers/ffmpeg_parser.py
Wir fügen einen regulären Ausdruck (Regex) hinzu, der nach Textblöcken wie Chapter #0:X: start ... und der dazugehörigen title-Metadaten-Zeile sucht.
Ausgelesene Kapitel werden als Liste von Dictionarys ([{'title': '...', 'start': 100.0, 'end': 200.0}]) in das 
tags
-Wörterbuch unter dem Schlüssel chapters gespeichert.
Die Speicherung in die SQLite-Datenbank geschieht automatisch, da das gesamte 
tags
-Wörterbuch als JSON-Feld gespeichert wird.
2. 
web/app.html
Die ausgelesenen Kapitel müssen für den Benutzer sichtbar gemacht werden.

[MODIFY] 
web/app.html
Im Seitenmenü (sb-fileinfo) wird eine Abfrage eingebaut: if (tags.chapters && tags.chapters.length > 0).
Falls Kapitel vorhanden sind, wird eine kleine strukturierte Liste oder Tabelle unterhalb der Format-Infos generiert.
Jedes Kapitel zeigt seinen Titel und, idealerweise, seinen Startzeitpunkt (formatiert in hh:mm:ss) an.
Verification Plan
Automated Tests
Ausführen des 
tests/benchmark_parsers.py
 auf einer 
.m4b
 Datei, um zu verifizieren, dass das Dictionary chapters erfolgreich gefüllt ist.
Manual Verification
Datenbank zurücksetzen und Server neustarten (
main.py
).
Anklicken eines Hörbuches (z.B. "Adam Grant - Nonkonformisten.m4b") in der GUI.
Prüfen, ob die Kapitelübersicht fehlerfrei und optisch passend in der Seitenleiste gerendert wird.

Comment
Ctrl+Alt+M
