from pathlib import Path

def parse(path, filename, tags=None):
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
        
    if " - " in filename:
        parts = filename.split(" - ", 1)
        if not tags.get('artist'):
            tags['artist'] = parts[0].strip()
        if not tags.get('title'):
            title = parts[1].rsplit(".", 1)[0].strip() if "." in parts[1] else parts[1].strip()
            tags['title'] = title
    else:
        if not tags.get('title'):
            title = filename.rsplit(".", 1)[0] if "." in filename else filename
            tags['title'] = title
        
    return tags
