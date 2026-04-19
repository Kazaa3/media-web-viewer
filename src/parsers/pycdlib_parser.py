from pathlib import Path
from typing import Any
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("parser_pycdlib")

def get_capabilities() -> dict[str, Any]:
    return {
        "name": "PyCdlib",
        "description": "Deep ISO/Disk image analysis using the pycdlib library. Identifies DVD, Blu-ray, and volume metadata.",
        "supported_tags": [
            "pycdlib_volume_id", "pycdlib_publisher", "pycdlib_application", 
            "pycdlib_has_joliet", "pycdlib_is_dvd", "pycdlib_is_bluray"
        ],
        "supported_codecs": ["iso", "bin", "img"]
    }

def get_settings_schema() -> dict[str, Any]:
    return {}

def parse(path_obj: Path, file_type: str, tags: dict[str, Any], filename: str | None = None, mode: str = 'lightweight', settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    @brief Extracts ISO metadata using the pycdlib library.
    """
    if file_type not in [".iso", ".bin", ".img"]:
        return tags

    if filename is None:
        filename = path_obj.name
    if settings is None:
        settings = {}

    try:
        import pycdlib
        iso = pycdlib.PyCdlib()
        iso.open(str(path_obj))
        
        def safe_str(val):
            if val is None: return ""
            if hasattr(val, 'text'): val = val.text
            if hasattr(val, 'decode'): return val.decode('utf-8', 'replace').strip()
            return str(val).strip()

        # Volume Identifiers
        try:
            pvd = iso.pvd
            if pvd:
                tags['pycdlib_volume_id'] = safe_str(pvd.volume_identifier)
                tags['pycdlib_publisher'] = safe_str(pvd.publisher_identifier)
                tags['pycdlib_application'] = safe_str(pvd.application_identifier)
                tags['pycdlib_preparer'] = safe_str(pvd.preparer_identifier)
                try:
                    cdate = pvd.volume_creation_date
                    if hasattr(cdate, 'year') and cdate.year > 0:
                        tags['pycdlib_creation_date'] = f"{cdate.year:04d}-{cdate.month:02d}-{cdate.dayofmonth:02d} {cdate.hour:02d}:{cdate.minute:02d}:{cdate.second:02d}"
                except Exception as ce:
                    log.debug(f"[PyCdlib] Creation date error for {filename}: {ce}")
        except Exception as pe:
            log.debug(f"[PyCdlib] PVD error for {filename}: {pe}")

        # Structural Info
        tags['pycdlib_has_joliet'] = iso.has_joliet()
        tags['pycdlib_has_rock_ridge'] = iso.has_rock_ridge()
        tags['pycdlib_has_udf'] = iso.has_udf()
        
        # Content Detection
        try:
            children = list(iso.list_children(iso_path='/'))
            for c in children:
                ident = c.file_identifier() if callable(c.file_identifier) else c.file_identifier
                ident_str = safe_str(ident).upper()
                if 'VIDEO_TS' in ident_str: tags['pycdlib_is_dvd'] = True
                if 'BDMV' in ident_str: tags['pycdlib_is_bluray'] = True
                if 'DVD_RTAV' in ident_str: tags['pycdlib_is_dvd_vr'] = True
                if 'HVDVD_TS' in ident_str: tags['pycdlib_is_hvdvd'] = True
        except Exception as le:
            log.debug(f"[PyCdlib] Child list error for {filename}: {le}")

        iso.close()
    except ImportError:
        log.debug(f"[PyCdlib] Library not installed, skipping.")
    except Exception as e:
        log.error(f"[PyCdlib-Parser] Failed for {filename}: {e}", exc_info=True)

    return tags

