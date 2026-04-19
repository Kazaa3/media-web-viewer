import os
import time
import shutil
import threading
try:
    import bottle as btl
except ImportError:
    from unittest.mock import MagicMock
    btl = MagicMock()
    log_err = lambda x: print(f"[DependencyShield] Bottle not found. Mocking {x}")
    btl.HTTPResponse = MagicMock()
    btl.HTTPError = MagicMock()
    btl.static_file = MagicMock()
    btl.request = MagicMock()
from pathlib import Path
from urllib.parse import unquote
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT, DEFAULT_TIME_FORMAT
from src.core.logger import get_logger, get_timestamped_log_path
from src.core import db, api_transcoding, api_core_app

log = get_logger("api_orchestrator")

def resolve_media_path(file_path: str) -> str:
    """Resolves a file path that might be a URL-encoded string or a relative /media/ path."""
    path_decoded = unquote(str(file_path))
    p_obj = Path(path_decoded).expanduser()
    path_normalized = str(p_obj)

    if p_obj.exists(): return str(p_obj.resolve())
    if not path_normalized.startswith("/"):
        p_abs = Path("/" + path_normalized)
        if p_abs.exists(): return str(p_abs.resolve())

    stripped_path = path_normalized
    prefixes = GLOBAL_CONFIG.get("player_settings", {}).get("media_prefixes", ["/media/", "media/"])
    for prefix in prefixes:
        if path_normalized.startswith(prefix):
            stripped_path = path_normalized[len(prefix):]
            break

    db_path = db.get_media_path(stripped_path)
    if db_path and Path(db_path).exists(): return db_path

    p_stripped = Path(stripped_path)
    if p_stripped.exists(): return str(p_stripped.resolve())
    return path_normalized

def log_process_stderr(process, name):
    """Refactored granular logging for background processes (FFmpeg, VLC, etc.)."""
    if not process or not process.stderr: return
    log_cfg = GLOBAL_CONFIG.get("logging_registry", {})
    if not log_cfg.get("enable_granular_transcoder_logs", False): return
    
    log_dir = Path(log_cfg.get("transcoding_log_dir", str(PROJECT_ROOT / "logs" / "transcoding")))
    log_handle = None
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = get_timestamped_log_path(log_dir, name)
        log_handle = open(log_path, "a", encoding="utf-8")
        log_handle.write(f"\n--- Process Log Start [{name}]: {time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT)} ---\n")
    except Exception as e:
        log.debug(f"[Orchestrator] Failed to setup specialized log for {name}: {e}")

    def log_thread():
        try:
            for line in process.stderr:
                try:
                    decoded = line.decode(errors='replace').strip()
                    log.info(f" [{name}] {decoded}")
                    if log_handle:
                        log_handle.write(f"{time.strftime(DEFAULT_TIME_FORMAT)} - {decoded}\n")
                except Exception: pass
        finally:
            if log_handle:
                try:
                    log_handle.write(f"--- Process Log End [{name}]: {time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT)} ---\n")
                    log_handle.close()
                except Exception: pass

    threading.Thread(target=log_thread, daemon=True).start()

# --- Bottle Routes (Media Delivery Pipeline) ---

def server_file_direct(file_path):
    """Serves local media files directly via the Eel/Bottle bridge."""
    log.info(f"[Orchestrator] Direct Stream Request: {file_path}")
    resolved = resolve_media_path(file_path)
    if not os.path.exists(resolved):
        return btl.HTTPResponse(status=404, body=f"File not found: {resolved}")

    # Dynamic MIME Resolution
    ext = os.path.splitext(resolved)[1].lower()
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {})
    mimetype = reg.get("audio", {}).get("mime_map", {}).get(ext) or reg.get("video", {}).get("mime_map", {}).get(ext, 'auto')
    
    return btl.static_file(os.path.basename(resolved), root=os.path.dirname(resolved), mimetype=mimetype, download=False)

def stream_video_fragmented(file_path):
    """On-the-fly FragMP4/Matroska streaming via FFmpeg."""
    start_time = btl.request.query.get('ss', '0')
    audio_idx = btl.request.query.get('audio_idx', '0')
    subs_idx = btl.request.query.get('subs_idx', None)

    resolved = resolve_media_path(file_path)
    if not os.path.exists(resolved):
        item = db.get_media_by_name(file_path)
        if item: resolved = item['path']
        else: return btl.HTTPError(404, "File not found")

    return api_transcoding.get_transcode_stream(
        resolved_path=resolved,
        start_time=float(start_time),
        audio_idx=int(audio_idx),
        subs_idx=subs_idx if subs_idx and str(subs_idx).lower() != 'none' else None
    )

def video_remux_stream(item_id):
    """Real-time remuxing to Matroska/WebM for Chrome Native playback."""
    start_time = btl.request.query.get('ss', '0')
    audio_idx = btl.request.query.get('audio_idx', '0')
    subs_idx = btl.request.query.get('subs_idx', None)

    item = db.get_media_by_id(item_id) or db.get_media_by_name(item_id)
    file_path = item['path'] if item else resolve_media_path(item_id)
    
    if not os.path.exists(file_path): return btl.HTTPResponse(status=404)

    log.info(f" [Orchestrator] Starting remux for: {file_path}")
    
    return btl.HTTPResponse(
        api_transcoding.get_remux_stream(
            file_path=file_path,
            start_time=float(start_time),
            audio_idx=int(audio_idx),
            subs_idx=subs_idx if subs_idx and str(subs_idx).lower() != 'none' else None
        ),
        content_type="video/mp4"
    )

def vlc_hls_live_proxy(filename):
    """Serves real-time HLS segments generated by background VLC."""
    hls_dir = "/tmp/vlc_hls"
    target = os.path.join(hls_dir, filename)
    if not os.path.exists(target): return btl.HTTPResponse(status=404)
    ext = os.path.splitext(filename)[1].lower()
    mimetype = 'application/x-mpegURL' if ext == '.m3u8' else 'video/MP2T'
    try:
        with open(target, 'rb') as f: data = f.read()
        return btl.HTTPResponse(data, status=200, headers={'Content-Type': mimetype, 'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    except Exception: return btl.HTTPResponse(status=500)
