# Kategorie: MediaItem Metadata Extraction
# Eingabewerte: AAC Dateien in /media
# Ausgabewerte: Samplerate, Bitrate, Dateigröße, Codec, TagType
# Testdateien: media/*.aac
# Kommentar: Gezielter Test der Metadaten-Extraktion für das AAC-Containerformat.

import os
import glob
from pathlib import Path
from main import MediaItem
import sys
sys.path.append('.')

for f in glob.glob('media/*.*'):
    name = os.path.basename(f)
    if not name.endswith('.aac'):
        continue
    m = MediaItem(name, Path(f))
    print(
        name, " | SRT: ", m.tags.get(
            'samplerate', 'MISSING'), " | BRT: ", m.tags.get(
            'bitrate', 'MISSING'), " | SIZ: ", m.tags.get(
                'filesize', 'MISSING'), " | CODEC: ", m.tags.get('codec'), " | TYPE: ", m.tags.get('tagtype'))
