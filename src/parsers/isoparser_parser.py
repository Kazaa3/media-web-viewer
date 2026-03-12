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

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "ISO Parser",
        "description": "Extracts volume identifiers and file listings from ISO/Disk images using pycdlib or isoparser.",
        "supported_tags": ["container", "tagtype", "pycdlib_volume_id", "iso_files_count", "iso_volume_label"],
        "supported_codecs": ["iso", "bin", "img"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {}


def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    if filename is None:
        filename = path_obj.name
    """
    Parses ISO files using pycdlib or isoparser and extracts basic metadata.
    Handles both Path and file object, logs errors for corrupted files.
    """
    if file_type != ".iso":
        return tags

    from .format_utils import PARSER_CONFIG, SLOW_PARSERS
    is_slow = "isoparser" in SLOW_PARSERS or "pycdlib" in SLOW_PARSERS
    fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)

    if is_slow and mode != 'full' and fast_scan:
        return tags
    
    tags['container'] = 'iso'
    tags['tagtype'] = 'iso'

    # Try pycdlib first (generally more robust/faster)
    if HAS_PYCDLIB:
        try:
            iso = pycdlib.PyCdlib()
            iso.open(str(path_obj))
            pvd = iso.get_pvd()
            tags['pycdlib_volume_id'] = pvd.volume_identifier.decode('utf-8', 'ignore').strip() if pvd else "Unknown"
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
                pvd = iso.volume_descriptors['primary']
                # isoparser/pycdlib might use volume_id or volume_identifier
                tags['iso_volume_label'] = getattr(pvd, 'volume_id', getattr(pvd, 'volume_identifier', 'Unknown'))
            
            all_files = list(iso.root.children) if hasattr(iso, 'root') else []
            tags['iso_files_count'] = len(all_files)
            tags['iso_file_list'] = [f.name for f in all_files][:10]
        except Exception as e:
            tags['iso_error'] = f"isoparser: {e}"
            
    return tags
