import sys; sys.path.append('.')
from main import MediaItem
from pathlib import Path
import glob
import os

for f in glob.glob('media/*.*'):
    name = os.path.basename(f)
    if not name.endswith('.aac'): continue
    m = MediaItem(name, Path(f))
    print(name, " | SRT: ", m.tags.get('samplerate', 'MISSING'), " | BRT: ", m.tags.get('bitrate', 'MISSING'), " | SIZ: ", m.tags.get('filesize', 'MISSING'), " | CODEC: ", m.tags.get('codec'), " | TYPE: ", m.tags.get('tagtype'))
