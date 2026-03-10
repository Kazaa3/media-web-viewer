from isoparser.iso import ISO  # isoparser requires 'six' package
from typing import Any
from pathlib import Path

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str, mode: str = 'lightweight') -> dict[str, Any]:
    """
    Parses ISO files using isoparser and extracts basic metadata.
    Handles both Path and file object, logs errors for corrupted files.
    """
    if file_type != ".iso":
        return tags
    try:
        # isoparser expects a file object, not a string
        with open(path_obj, 'rb') as f:
            iso = ISO(f)
            tags['iso_volume_label'] = iso.primary.volume_id
            tags['iso_files_count'] = len(list(iso.files()))
            tags['iso_file_list'] = [file.path for file in iso.files()][:10]  # Limit to 10 for preview
            tags['container'] = 'iso'
            tags['tagtype'] = 'iso'
    except Exception as e:
        tags['iso_error'] = f"isoparser: {e}"
    return tags
