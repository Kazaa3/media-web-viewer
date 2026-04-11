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
    # Support for .iso, .bin, and .img
    if file_type not in [".iso", ".bin", ".img"]:
        return tags
    
    import re
    year_pattern = re.compile(r'[\(\[\s]((?:19|20)\d{2})[\)\]\s]?')

    from .format_utils import PARSER_CONFIG, SLOW_PARSERS
    is_slow = "isoparser" in SLOW_PARSERS or "pycdlib" in SLOW_PARSERS
    fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)

    if is_slow and mode != 'full' and fast_scan:
        return tags
    
    tags['container'] = 'iso' if file_type == '.iso' else file_type[1:]
    tags['tagtype'] = 'disk_image'

    # Try pycdlib first (generally more robust/faster)
    if HAS_PYCDLIB:
        try:
            iso = pycdlib.PyCdlib()
            iso.open(str(path_obj))
            try:
                pvd = iso.get_pvd()
            except:
                pvd = None

            if pvd:
                vol_id = pvd.volume_identifier.decode('utf-8', 'ignore').strip() if hasattr(pvd.volume_identifier, 'decode') else str(pvd.volume_identifier).strip()
                tags['pycdlib_volume_id'] = vol_id
                if not tags.get('title'):
                    tags['title'] = vol_id
                
                # Try to extract year from volume_id
                ym = year_pattern.search(vol_id)
                if ym and not tags.get('year'):
                    tags['year'] = ym.group(1)

            # Basic file count from root
            try:
                tags['iso_files_count'] = len(iso.list_children(iso_path='/'))
            except: pass
            
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
                label = getattr(pvd, 'volume_id', getattr(pvd, 'volume_identifier', 'Unknown'))
                tags['iso_volume_label'] = label
                if not tags.get('title') or tags.get('title') == "Unknown":
                    tags['title'] = label
                
                # Try to extract year from label
                ym = year_pattern.search(str(label))
                if ym and not tags.get('year'):
                    tags['year'] = ym.group(1)
            
            all_files = list(iso.root.children) if hasattr(iso, 'root') else []
            tags['iso_files_count'] = len(all_files)
        except Exception as e:
            tags['iso_error'] = f"isoparser: {e}"
            
    return tags
