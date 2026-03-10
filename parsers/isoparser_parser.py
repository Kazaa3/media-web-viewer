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
        import isoparser
        iso = isoparser.parse(str(path_obj))
        # primary is an attribute of the ISO object in isoparser 0.3
        if hasattr(iso, 'volume_descriptors') and 'primary' in iso.volume_descriptors:
            tags['iso_volume_label'] = iso.volume_descriptors['primary'].volume_id
        
        # files() returns a generator of record objects
        all_files = list(iso.root.children) if hasattr(iso, 'root') else []
        tags['iso_files_count'] = len(all_files)
        tags['iso_file_list'] = [f.name for f in all_files][:10]
        tags['container'] = 'iso'
        tags['tagtype'] = 'iso'
    except Exception as e:
        tags['iso_error'] = f"isoparser: {e}"
    return tags
