import psutil
import time
from typing import Dict, Any, Optional
from src.core.eel_shell import eel

from src.core.config_master import (
    GLOBAL_CONFIG, PROGRAM_REGISTRY, 
    FORENSIC_TOOLS_LIST, 
    get_binary_version as _get_version_config
)
from src.core.logger import get_logger

log = get_logger("api_tools")

def get_tool_health_report() -> Dict[str, Any]:
    """
    Forensic Toolchain Diagnostics (v1.46.132).
    Checks availability and versions for all registered programs.
    """
    report = {}
    for name, path in PROGRAM_REGISTRY.items():
        if not path or not os.path.exists(path):
            state = "MISSING"
            version = "N/A"
        else:
            state = "OK"
            version = _get_version_config(path)
            
        report[name] = {
            "state": state,
            "path": path,
            "version": version
        }
    return report

def kill_stalled_forensic_processes(targets: Optional[list] = None):
    """
    Forcefully cleans up stalled FFmpeg, MKVMerge, or VLC processes.
    (Migrated from api_reporting v1.46.132)
    """
    if targets is None:
        targets = FORENSIC_TOOLS_LIST
        
    log.info(f"[Cleanup] Targeted forensic audit: killing stalled processes {targets}")
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = (proc.info['name'] or "").lower()
            cmdline = " ".join(proc.info['cmdline'] or []).lower()
            
            if any(t in name for t in targets) or any(t in cmdline for t in targets):
                if proc.info['pid'] != os.getpid():
                    proc.kill()
                    count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    log.info(f"[Cleanup] Terminated {count} forensic artifacts.")
    return count

def kill_stalled_ffmpeg_streams():
    """Specific hook for high-priority FFmpeg cleanup (v1.46.135)."""
    return kill_stalled_forensic_processes(['ffmpeg', 'ffprobe', 'ffplay'])

def super_kill():
    """Nuclear cleanup: Terminates ALL forensic tools and known browsers."""
    targets = FORENSIC_TOOLS_LIST + ['chrome', 'chromium', 'firefox', 'msedge']
    return kill_stalled_forensic_processes(targets)

def check_binary_available(name: str) -> bool:
    """Verifies if a specific tool is operational in the registry."""
    path = PROGRAM_REGISTRY.get(name)
    return path is not None and os.path.exists(path)

def get_detailed_tool_stats(name: str) -> Dict[str, Any]:
    """Returns granular metadata for a specific forensic binary."""
    path = PROGRAM_REGISTRY.get(name)
    if not path:
        return {"error": "Tool not registered"}
        
    stats = {
        "name": name,
        "path": path,
        "exists": os.path.exists(path),
        "size": os.path.getsize(path) if os.path.exists(path) else 0,
        "version": _get_version_config(path)
    }
    return stats

# --- Tool-Specific API Orchestration (Migrated/Expanded v1.54.020) ---

@eel.expose
def launch_ffplay(file_path: str):
    """
    Forensic Rapid Preview Pulse.
    Launches ffplay with high-fidelity stats and auto-exit.
    """
    path = PROGRAM_REGISTRY.get("ffplay")
    if not path or not os.path.exists(path):
        log.error("[Tool-Pulse] FFplay binary not found in registry.")
        return False
        
    cmd = [path, "-i", file_path, "-stats", "-autoexit", "-infowin"]
    log.info(f"[Tool-Pulse] Launching FFplay: {' '.join(cmd)}")
    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        log.error(f"[Tool-Pulse] FFplay launch failed: {e}")
        return False

@eel.expose
def discover_chromecast():
    """
    Scans the local network for Google Cast compatible devices.
    (v1.54.020 Forensic Discovery)
    """
    try:
        import pychromecast
        log.info("[Cast-Audit] Initiating Chromecast discovery pulse...")
        # Discovery usually takes a few seconds; we use a non-blocking scan if possible
        # or a short timeout for the technical HUD.
        chromecasts, browser = pychromecast.get_chromecasts()
        browser.stop_discovery()
        
        devices = []
        for cc in chromecasts:
            devices.append({
                "name": cc.name,
                "model": cc.model_name,
                "uuid": str(cc.uuid),
                "host": cc.host
            })
        
        log.info(f"[Cast-Audit] Discovery complete: {len(devices)} devices found.")
        return devices
    except ImportError:
        log.warning("[Cast-Audit] pychromecast NOT FOUND. Discovery disabled.")
        return []
    except Exception as e:
        log.error(f"[Cast-Audit] Discovery failure: {e}")
        return []

@eel.expose
def cast_to_device(device_uuid: str, file_path: str):
    """
    Casts a media asset to a specific Chromecast device.
    """
    try:
        import pychromecast
        chromecasts, browser = pychromecast.get_chromecasts()
        browser.stop_discovery()
        
        # Match device
        target = next((cc for cc in chromecasts if str(cc.uuid) == device_uuid), None)
        if not target:
            log.error(f"[Cast-Pulse] Target device {device_uuid} not found.")
            return False
            
        target.wait()
        mc = target.media_controller
        # Note: Chromecast usually requires a URL. We use the workstation's stream relay.
        # This requires the server to be reachable by the Chromecast.
        port = GLOBAL_CONFIG.get("network_settings", {}).get("port", 8345)
        host = GLOBAL_CONFIG.get("network_settings", {}).get("host", "localhost")
        if host == 'localhost':
            # Attempt to find local IP for external casting
            import socket
            hostname = socket.gethostname()
            host = socket.gethostbyname(hostname)
            
        stream_url = f"http://{host}:{port}/stream/via/direct/{file_path}"
        log.info(f"[Cast-Pulse] Casting to {target.name}: {stream_url}")
        
        # Simple MP4 cast
        mc.play_media(stream_url, 'video/mp4')
        mc.block_until_active()
        return True
    except Exception as e:
        log.error(f"[Cast-Pulse] Casting failure: {e}")
        return False
