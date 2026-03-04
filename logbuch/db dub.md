Datenbank-Duplikate Fix
Die Ursache für Duplikate in der Datenbank lag im Transcoding-Ordner media/.cache/. Wenn Dateien für den Browser on-the-fly transkodiert (z.B. ALAC zu FLAC) und dort gespeichert wurden, hat der nächste "Scan Media" Vorgang diese transkodierten Versionen ebenfalls gefunden und als komplett neue Lieder indexiert.

Lösung: main.py überspringt jetzt während des rekursiven Scannens (rglob) alle Ordner, die .cache im Pfad enthalten. Dadurch bleibt die Datenbank sauber und führt genau die Ursprungsdateien auf.

Zentralisierte Formatierungslogik: Sämtliche Formatierungsregeln für Codecs, Bit-Tiefen und Sample-Raten wurden in die neue Datei parsers/format_utils.py ausgelagert.

Konfigurierbare Parser-Kette: Die Ausführungsreihenfolge der Metadaten-Parser (Mutagen, MediaInfo, FFmpeg, Dateiname, Container) ist nun vollständig über das Optionen-Menü per Drag-and-Drop konfigurierbar und ein-/ausschaltbar. Die Konfiguration wird persistent in einer config.json (~/.config/gui_media_web_viewer/parser_config.json) gespeichert.

Optionen-Layout mit "Spielereien": Der Datei-Browser (Tkinter native Picker) wurde in eine neue rechte Spalte namens "✨ Spielereien" im Optionen-Tab verschoben. Das Optionen-Tab nutzt nun ein übersichtliches Zwei-Spalten-Layout.

Workflow-Verbesserung: Nach der Auswahl eines Ordners in den Spielereien springt die App automatisch zurück zum Browser-Tab.

Verfeinerte Bit-Tiefen für PCM (WAV): 24-Bit PCM wird nun korrekt als 24 Bit (s32) angezeigt.

Beispielausgaben:

PCM_S16LE | 16 Bit (s16) | 44.1 kHz
PCM_S24LE | 24 Bit (s32) | 44.1 kHz
mp3 | 16 Bit (lossy) | 44.1 kHz
ogg | 16 Bit (lossy) | 44.1 kHz
