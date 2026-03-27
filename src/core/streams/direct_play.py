import bottle
import os
import logging
from pathlib import Path

log = logging.getLogger("streams.direct_play")

def handle_direct_play(file_path):
    """
    @brief Serves a media file directly for native browser playback.
    @details Leverages Bottle's static_file for full Range-header support.
    """
    if not os.path.exists(file_path):
        return bottle.HTTPError(404, "File not found")

    # Determine mimetype for Video.js compatibility
    mimetype = 'auto'
    ext = Path(file_path).suffix.lower()
    if ext == '.mkv':
        mimetype = 'video/x-matroska'
    elif ext == '.webm':
        mimetype = 'video/webm'
    elif ext == '.mp4':
        mimetype = 'video/mp4'

    log.info(f"[DirectPlay] Serving: {file_path}")
    
    return bottle.static_file(
        os.path.basename(file_path),
        root=os.path.dirname(file_path),
        mimetype=mimetype,
        download=False
    )
