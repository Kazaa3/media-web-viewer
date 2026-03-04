<!-- Category: Tests -->

Ich habe die gewünschten Erweiterungen für den Tests-Reiter umgesetzt und die fehlenden Dokumentationen ergänzt.

1. Bearbeitbare Test-Metadaten
In der GUI (Reiter "Tests") findest du nun bei jeder Test-Suite einen ✏️ Bearbeiten-Button.

Beim Klicken öffnet sich ein Modal, in dem du Kategorie, Eingabewerte, Ausgabewerte, Testdateien und den Kommentar direkt ändern kannst.
Die Änderungen werden sofort in die entsprechende 

.py
-Datei im 

tests/
-Ordner zurückgeschrieben (als Kommentar-Header), sodass sie persistent bleiben.
2. Ergänzte Test-Beschreibungen
Ich habe die folgenden Test-Dateien mit detaillierten Beschreibungen und Metadaten versehen:

Test	Datei	Kategorie
Eel	

test_eel.py
Eel / Bottle Integration
MP3 Tags	

test_mp3_tags.py
Metadata Extraction (Mutagen)
Parse	

test_parse.py
Parser Benchmark
Parse2	

test_parse2.py
MediaItem Extraction (AAC Fokus)
PCM	

test_pcm.py
Audio Bit-Depth Test
Route Debug	

test_route_debug.py
Routing & URL Encoding Debug
Route Debug2	

test_route_debug2.py
Direct Path Routing Test
Stream	

test_stream.py
FFprobe Duration Extraction
Technische Umsetzung:
Backend (

main.py
): Neue Funktion 

update_test_metadata
 hinzugefügt, die die Python-Dateien einliest, die alten Metadaten-Header entfernt und die neuen einfügt.
Frontend (

app.html
): Edit-Modal für Tests implementiert und die 

loadTestSuites
-Funktion erweitert, um das Bearbeiten zu ermöglichen.
Damit sind nun sowohl die Medien-Metadaten als auch die Test-Dokumentationen vollständig über die Benutzeroberfläche editierbar.
