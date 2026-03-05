# Kategorie: FFprobe Duration Extraction
# Eingabewerte: ALAC Dateien
# Ausgabewerte: Dauer in Sekunden (stdout)
# Testdateien: media/sample.alac
# Kommentar: Schneller Funktionstest für FFprobe zum Auslesen der Spieldauer von ALAC-Dateien.

import subprocess
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "media/sample.alac"], capture_output=True, text=True).stdout.strip())
