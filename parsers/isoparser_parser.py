from isoparser import ISO
from typing import Any
from pathlib import Path

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], mode: str = 'lightweight') -> dict[str, Any]:
    """
    Parses ISO files using isoparser and extracts basic metadata.
    """
    if file_type != ".iso":
        return tags
    try:
        iso = ISO(str(path_obj))
        tags['iso_volume_label'] = iso.primary.volume_id
        tags['iso_files_count'] = len(list(iso.files()))
        tags['iso_file_list'] = [f.path for f in iso.files()][:10]  # Limit to 10 for preview
        tags['container'] = 'iso'
        tags['tagtype'] = 'iso'
    except Exception as e:
        tags['iso_error'] = str(e)
    return tags
