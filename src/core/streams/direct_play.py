import bottle
import os
from pathlib import Path
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Modernized)
log = get_logger("streams_direct")

def handle_direct_play(file_path):
    """
    @brief Serves a media file directly for native browser playback.
    @details Leverages Bottle's static_file for full Range-header support.
    """
    if not os.path.exists(file_path):
        log.error(f"[DirectPlay] File not found: {file_path}")
        return bottle.HTTPError(404, "File not found")

    # Pull configuration (Phase 9 Centralization)
    reg = GLOBAL_CONFIG.get("parser_registry", {})
    mime_map = reg.get("mimetype_map", {
        '.mkv': 'video/x-matroska',
        '.webm': 'video/webm',
        '.mp4': 'video/mp4'
    })
    
    ext = Path(file_path).suffix.lower()
    mimetype = mime_map.get(ext, 'auto')

    log.info(f"[DirectPlay] Serving: {os.path.basename(file_path)} as {mimetype}")
    
    return bottle.static_file(
        os.path.basename(file_path),
        root=os.path.dirname(file_path),
        mimetype=mimetype,
        download=False
    )

