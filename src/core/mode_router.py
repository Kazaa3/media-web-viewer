# Specialized logger
from src.core.ffprobe_analyzer import ffprobe_analyze # type: ignore
from src.core.logger import get_logger
log = get_logger("mode_router")

def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 8+ primary streaming paths.
    @param file_path Path to the media file.
    @return Dictionary with 'mode' and 'info'.
    """
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"Routing fallback to direct_play due to analysis error: {info['error']}")
        return {"mode": "direct_play", "info": info}

    # Final Decision
    codec = info.get('codec', 'unknown')
    container = info.get('container', 'unknown')
    resolution = info.get('resolution', 'SD')
    
    mode = 'hls_fmp4'
    if codec == 'h264' and container in ['mp4', 'mov', 'm4a', 'quicktime']:
        if resolution != "4K":
            mode = 'direct_play'
    elif info.get('is_iso') or info.get('has_menus') or info.get('atmos'):
        mode = 'vlc_bridge'
    elif resolution in ["SD", "720p", "1080p"]:
        mode = 'mse'

    return {
        "mode": mode,
        "info": info
    }

def get_mode_description(mode):
    """
    @brief Returns a human-readable description and tech-stack for the mode.
    """
    mapping = {
        'direct_play': "Direkte Dateiübertragung (Chrome Native)",
        'mse': "FFmpeg fMP4 zu MSE (Ultra-Low-Latency)",
        'hls_fmp4': "FFmpeg fMP4 zu HLS (Universal)",
        'vlc_bridge': "VLC HLS zu MSE (Interaktiv / Menüs)",
        'mpv_wasm': "libmpv zu Canvas (WASM / Interaktiv)"
    }
    return mapping.get(mode, "Unbekannter Modus")
