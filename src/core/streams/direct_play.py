import bottle
import logging
import os
from pathlib import Path

log = logging.getLogger("streams.direct")

def serve_direct_media(file_path):
    """
    @brief Serves media files directly via Bottle for native browser playback.
    @param file_path Path to the media file.
    @return Bottle static_file response with Range support.
    """
    p = Path(file_path)
    if not p.exists():
        log.error(f"DirectPlay: File not found: {file_path}")
        return bottle.HTTPError(404, "File not found")

    # Detect MIME type
    mimetype = "video/mp4" # Default
    ext = p.suffix.lower()
    if ext == '.webm': mimetype = "video/webm"
    elif ext == '.mkv': mimetype = "video/x-matroska"
    elif ext == '.mp3': mimetype = "audio/mpeg"
    elif ext == '.wav': mimetype = "audio/wav"
    elif ext == '.m4a': mimetype = "audio/mp4"
    elif ext in ['.jpg', '.jpeg']: mimetype = "image/jpeg"
    elif ext == '.png': mimetype = "image/png"

    log.info(f"[DirectPlay] Serving: {p.name} as {mimetype}")
    # static_file handles Range requests (seeking) automatically
    return bottle.static_file(p.name, root=str(p.parent), mimetype=mimetype)
