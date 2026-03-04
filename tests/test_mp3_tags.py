# Kategorie: Metadata Extraction (Mutagen)
# Eingabewerte: MP3 Dateien
# Ausgabewerte: ID3v2 Tags (TPE1, TDRC)
# Testdateien: media/sample.mp3
# Kommentar: Prüft die Extraktion von ID3-Tags mit der Mutagen-Bibliothek.

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

try:
    audio = MP3('media/sample.mp3')
    print("MP3 Artist:", audio.get('TPE1'))
    print("MP3 Year:", type(audio.get('TDRC')))
    
    # Check what kind of object they are
    art = audio.get('TPE1')
    if art:
        print("TPE1 [0]:", art[0])
except Exception as e:
    print(e)
