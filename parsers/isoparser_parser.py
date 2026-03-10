try:
    import pycdlib
    HAS_PYCDLIB = True
except ImportError:
    HAS_PYCDLIB = False

try:
    import isoparser
    HAS_ISOPARSER = True
except ImportError:
    HAS_ISOPARSER = False

from typing import Any
from pathlib import Path

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str, mode: str = 'lightweight') -> dict[str, Any]:
    """
    Parses ISO files using pycdlib or isoparser and extracts basic metadata.
    Handles both Path and file object, logs errors for corrupted files.
    """
    if file_type != ".iso":
        return tags
    
    tags['container'] = 'iso'
    tags['tagtype'] = 'iso'

    # Try pycdlib first (generally more robust/faster)
    if HAS_PYCDLIB:
        try:
            iso = pycdlib.PyCdlib()
            iso.open(str(path_obj))
            tags['pycdlib_volume_id'] = iso.get_volume_id().decode('utf-8', 'ignore').strip()
            # Basic file count from root
            tags['iso_files_count'] = len(iso.list_children(iso_path='/'))
            iso.close()
            return tags
        except Exception:
            pass

    # Fallback to isoparser
    if HAS_ISOPARSER:
        try:
            iso = isoparser.parse(str(path_obj))
            if hasattr(iso, 'volume_descriptors') and 'primary' in iso.volume_descriptors:
                tags['iso_volume_label'] = iso.volume_descriptors['primary'].volume_id
            
            all_files = list(iso.root.children) if hasattr(iso, 'root') else []
            tags['iso_files_count'] = len(all_files)
            tags['iso_file_list'] = [f.name for f in all_files][:10]
        except Exception as e:
            tags['iso_error'] = f"isoparser: {e}"
            
    return tags
