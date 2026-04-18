import eel
from src.core.ffprobe_analyzer import ffprobe_analyze # type: ignore
from src.core.logger import get_logger
log = get_logger("mode_router")

@eel.expose
def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 8+ primary streaming paths.
    @param file_path Path to the media file.
    @return Dictionary with 'mode' and 'info'.
    """
    log.info(f"[PLAY-PULSE] smart_route analysis started for: {file_path}")
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"[PLAY-PULSE] Routing fallback to direct_play due to analysis error: {info['error']}")
        return {"mode": "direct_play", "info": info}

    # 0. Load Configuration (v1.46.044 Integration)
    from src.core.config_master import GLOBAL_CONFIG
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    flags = reg.get("orchestration_flags", {})
    
    # Analysis
    codec = info.get('codec', 'unknown')
    container = info.get('container', 'unknown')
    resolution = info.get('resolution', 'SD')
    bitrate = info.get('bitrate_kbps', 0)
    
    # Defaults
    mode = 'hls_fmp4'
    
    # 1. Native Direct Play (Chrome compatible)
    if codec == 'h264' and container in ['mp4', 'mov', 'm4a', 'quicktime']:
        if resolution != "4K" and bitrate < 20000:
            mode = 'direct_play'
            
    # 2. MSE (H.264 / VP9 / AV1 in various containers)
    mse_threshold = flags.get("mse_threshold_mbps", 15) * 1000
    if resolution in ["SD", "720p", "1080p"] and bitrate < mse_threshold:
        if codec in ['h264', 'vp9', 'av1']:
            mode = 'mse'
            
    # 3. VLC Bridge (ISO / Heavy Containers / Atmos)
    if info.get('is_iso') or info.get('has_menus') or info.get('atmos') or container == 'ts':
        if flags.get("force_vlc_for_iso", True):
            mode = 'vlc_bridge'
        
    # 4. DASH (Experimental high-bitrate)
    dash_threshold = flags.get("dash_threshold_mbps", 30) * 1000
    if container == 'mpd' or (resolution == '4K' and bitrate > dash_threshold):
        mode = 'dash'
        
    # 5. MPV WASM (Interactive / libmpv features)
    if info.get('is_interactive') or (container == 'webm' and flags.get("prefer_mpv_wasm_for_webm", True)):
        mode = 'mpv_wasm'
 
    # 6. Fallback to Native External (Ultra high-end)
    mpv_native_threshold = flags.get("mpv_native_threshold_mbps", 50) * 1000
    if resolution == '4K' and bitrate > mpv_native_threshold:
        mode = 'mpv_native'

    log.info(f"[PLAY-PULSE] smart_route decision: {mode} | Codec: {codec} | Res: {resolution} (Config-Tuned)")
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
        'mpv_wasm': "libmpv zu Canvas (WASM / Interaktiv)",
        'mpv_native': "Externer MPV Player (Verlustfrei / 4K)",
        'vlc_native': "Externer VLC Player (Verlustfrei / ISO)",
        'dash': "Dynamic Adaptive Streaming over HTTP (High-End)",
        'webtorrent': "P2P WebTorrent Streaming (Dezentral)",
        'hls_native': "Natives HLS (Safari / Edge compatible)"
    }
    return mapping.get(mode, "Unbekannter Modus")
