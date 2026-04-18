from pathlib import Path

def get_handler_for_file(filepath: str | Path):
    """
    @brief Factory method to return the correct handler for a given file.
    """
    from .audio_handler import AudioHandler
    from .video_handler import VideoHandler
    from src.core.config_master import GLOBAL_CONFIG
    
    path = Path(filepath)
    ext = path.suffix.lower()
    
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {})
    audio_exts = reg.get("audio", {}).get("extensions", [])
    
    # Fallback if registry is empty
    if not audio_exts:
        audio_exts = [".mp3", ".flac", ".m4a", ".wav", ".ogg"]
    
    if ext in audio_exts:
        return AudioHandler(path)
    return VideoHandler(path)
