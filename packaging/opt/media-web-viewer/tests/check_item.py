import glob
from main import MediaItem
import sys
import os
[sys.path.append(os.path.join(d, 'site-packages'))
 for d in ['/usr/lib/python3/dist-packages', '/usr/local/lib/python3.10/dist-packages']]
files = glob.glob("media/*.mp*") + glob.glob("media/*.mkv") + glob.glob("media/*.we*")
for f in files:
    try:
        item = MediaItem(f, f)
        print(f"File: {f}")
        print(f"Tags: {item.tags}")
        print("-" * 50)
    except Exception as e:
        print(f"Failed on {f}: {e}")
