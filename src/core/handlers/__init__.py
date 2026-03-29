from pathlib import Path

def get_handler_for_file(filepath: str | Path):
    """
    @brief Factory method to return the correct handler for a given file.
    """
    from .audio_handler import AudioHandler
    from .video_handler import VideoHandler
    
    path = Path(filepath)
    ext = path.suffix.lower()
    audio_exts = [".mp3", ".flac", ".m4a", ".wav", ".ogg", ".aac", ".wma", ".ape", ".dsd"]
    
    if ext in audio_exts:
        return AudioHandler(path)
    return VideoHandler(path)
