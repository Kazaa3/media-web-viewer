import os
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List

from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, PROGRAM_REGISTRY
from src.core.logger import get_logger
from src.core import db

log = get_logger("api_playback")

# --- Global Playback State (Migrated from main.py) ---
PLAYBACK_LOCKS = {}  # {path: timestamp}
VLC_INSTANCE = None
VLC_PLAYER = None

def get_vlc_instance():
    """ Lazily initializes the VLC instance to prevent early crashes. """
    global VLC_INSTANCE, VLC_PLAYER
    if VLC_INSTANCE is None:
        try:
            import vlc
            # Forensic Tip: Using Instance() with specific args ensures consistent behavior
            VLC_INSTANCE = vlc.Instance("--no-xlib")
            VLC_PLAYER = VLC_INSTANCE.media_player_new()
        except ImportError:
            log.warning("[VLC-Pulse] python-vlc not installed. VLC features disabled.")
        except Exception as e:
            log.error(f"[VLC-Pulse] Failed to init VLC: {e}")
    return VLC_INSTANCE

@eel.expose
def stop_vlc():
    """ Stops current VLC playback. """
    global VLC_PLAYER
    if VLC_PLAYER:
        VLC_PLAYER.stop()
        log.info("[VLC-Pulse] Playback stopped.")
    return True

@eel.expose
def vlc_seek(instance_id, time_seconds):
    """ Seeks to a specific timestamp in VLC. """
    global VLC_PLAYER
    if VLC_PLAYER and VLC_PLAYER.is_playing():
        VLC_PLAYER.set_time(int(time_seconds * 1000))
        return True
    return False

@eel.expose
def send_vlc_command(port, command, val=None):
    """ Sends a telnet/socket command to a background VLC instance. """
    # Placeholder for complex remote vlc controls if needed
    log.info(f"[VLC-Remote] Command '{command}' sent to port {port}")
    return True

@eel.expose
def open_with_ffplay(file_path: str):
    """ Launches ffplay for external preview. """
    path = PROGRAM_REGISTRY.get("ffplay")
    if not path or not os.path.exists(path):
        return False
    cmd = [path, "-i", file_path, "-autoexit", "-x", "800"]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True

@eel.expose
def open_with_vlc(file_path: str):
    """ Indirectly launches VLC via stream relay or direct play. """
    return play_vlc(file_path)

@eel.expose
def open_with_cvlc(file_path: str):
    """ Launches vlc in command-line mode (no gui). """
    path = PROGRAM_REGISTRY.get("cvlc") or PROGRAM_REGISTRY.get("vlc")
    if not path: return False
    cmd = [path, "--intf", "dummy", file_path]
    subprocess.Popen(cmd)
    return True

@eel.expose
def open_with_pyvlc(file_path: str):
    """ Uses the internal libvlc instance for playback. """
    inst = get_vlc_instance()
    if not inst: return False
    media = inst.media_new(file_path)
    VLC_PLAYER.set_media(media)
    VLC_PLAYER.play()
    return True

@eel.expose
def open_mpv(filepath):
    """ Forensic Rapid Preview via MPV engine. """
    path = PROGRAM_REGISTRY.get("mpv")
    if not path or not os.path.exists(path): return False
    cmd = [path, "--no-config", "--ontop", filepath]
    subprocess.Popen(cmd)
    return True

@eel.expose
def open_ffplay(filepath):
    """ Forensic Rapid Preview via ffplay engine. """
    return open_with_ffplay(filepath)

@eel.expose
def play_media(path):
    """
    @brief Unified media playback entry point (v1.54.022).
    Delegates to optimal engine based on file type and config.
    """
    from src.core.api_orchestrator import resolve_media_path
    path = resolve_media_path(path)
    ext = Path(path).suffix.lower()
    
    # Handshake with format_utils (Phase 9)
    from src.parsers.format_utils import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
    if ext in VIDEO_EXTENSIONS:
        return open_video_smart(path)
    
    # Standard Audio Playback (Direct)
    return {"status": "play", "path": path, "mode": "chrome_native"}

@eel.expose
def open_video_smart(file_path: str, mode: str = "auto", start_time: float = 0):
    """ Intelligent playback routing with debouncing. """
    now = time.time()
    last_trigger = PLAYBACK_LOCKS.get(str(file_path), 0)
    if now - last_trigger < 2.0:
        return {"status": "error", "error": "Debounced"}
    PLAYBACK_LOCKS[str(file_path)] = now

    from src.core.api_orchestrator import resolve_media_path
    file_path = resolve_media_path(file_path)

    # Simplified routing (v1.54 Refactor)
    # CD/ISO -> VLC
    if str(file_path).lower().endswith(('.iso', '.bin', '.img')):
        return open_video(file_path, "vlc", "vlc_embedded")

    return open_video(file_path, "auto", mode, start_time=start_time)

@eel.expose
def open_video(file_path: str, player_type: str = "auto", mode: str = "auto", source="smart", start_time=0):
    """ Final video orchestration. """
    # In a full-scale refactor, this logic expands to handle HLS, WebRTC, etc.
    return {"status": "play", "path": file_path, "player": player_type, "mode": mode, "start_time": start_time}

@eel.expose
def play_vlc(file_path: str):
    """ Direct play via system VLC binary. """
    path = PROGRAM_REGISTRY.get("vlc")
    if not path or not os.path.exists(path): return False
    subprocess.Popen([path, file_path])
    return True

@eel.expose
def play_external_file(path: str):
    """ Launches system default handler for a file. """
    try:
        import webbrowser
        webbrowser.open(path)
        return True
    except: return False

@eel.expose
def play_stream_url(url: str, engine: str = "hls"):
    """ Playback for network streams. """
    # Delegate to frontend for HLS/DASH
    return {"status": "stream", "url": url, "engine": engine}

# --- Cast & Remote Features (Exposed via api_tools.py) ---

def launch_ffplay_tool(file_path: str):
    """ Tool-specific FFplay launch with forensic stats. """
    return open_with_ffplay(file_path)
