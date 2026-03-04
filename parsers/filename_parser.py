import re
from pathlib import Path

def parse(path, filename, tags=None, mode='lightweight'):
    if tags is None:
        tags = {
            'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
            'codec': '', 'size': '', 'tagtype': '', 'container': '',
            'has_art': 'No', 'title': '', 'artist': '', 'album': '',
            'date': '', 'genre': '', 'track': '', 'totaltracks': '',
            'disc': '', 'totaldiscs': ''
        }
    
    try:
        if not tags.get('size'):
            tags['size'] = f"{Path(path).stat().st_size / (1024 * 1024):.2f} MB"
    except Exception:
        pass
        
    working_filename = filename
    if not tags.get('track'):
        track_match = re.match(r"^(\d+)\s+(.*)", working_filename)
        if track_match:
            tags['track'] = str(int(track_match.group(1))) # Remove leading zeros
            working_filename = track_match.group(2)
            
    if " - " in working_filename:
        parts = working_filename.split(" - ", 1)
        if not tags.get('artist'):
            tags['artist'] = parts[0].strip()
        if not tags.get('title'):
            title = parts[1].rsplit(".", 1)[0].strip() if "." in parts[1] else parts[1].strip()
            tags['title'] = title
    else:
        if not tags.get('title'):
            title = working_filename.rsplit(".", 1)[0] if "." in working_filename else working_filename
            tags['title'] = title
        
    return tags
