import sys; sys.path.append('.')
from main import MediaItem
from pathlib import Path
import glob
import os

for f in glob.glob('media/*.*'):
    name = os.path.basename(f)
    m = MediaItem(name, Path(f))
    print(name, " | SRT: ", m.tags.get('samplerate', 'MISSING'), " | BRT: ", m.tags.get('bitrate', 'MISSING'), " | SIZ: ", m.tags.get('filesize', 'MISSING'))
