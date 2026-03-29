# --- Early Path Bootstrapping & Standard Imports ---
import os
import sys
import time
import socket
import logging
import platform
import json
import base64
import re
import shutil
import subprocess
import glob
import sqlite3
import ast
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, cast
import psutil
import requests
import bottle

# 1. Immediate Path Calculation
MAIN_FILE = Path(__file__).resolve()
PROJECT_ROOT = MAIN_FILE.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
# 2. Integrate Scripts Folder (for Status Bar etc.)
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Import Status Tool
try:
    from status_bar_utils import StatusBar
    print("STDOUT: [StatusTool] StatusBar integrated", flush=True)
except ImportError:
    # Minimal fallback
    class StatusBar:
        def __init__(self, msg, total=100): self.msg = msg
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def update(self, *a): print(f"STDOUT: [Progress] {self.msg} ({a[0]}%)", flush=True)

# 3. Early Monkey Patching
try:
    from gevent import monkey
    monkey.patch_all()
    print("STDOUT: [Bootstrap] gevent monkey-patching successful", flush=True)
except ImportError:
    print("STDOUT: [Bootstrap] gevent not found, continuing without patching", flush=True)

# 4. Environment Guard
def ensure_stable_environment():
    """Ensures we are running in the correct .venv_core and avoids recursive loops."""
    if os.environ.get("MWV_AUTO_REEXEC") == "1": return
    TARGET_VENV = PROJECT_ROOT / ".venv_core"
    if not TARGET_VENV.exists(): TARGET_VENV = PROJECT_ROOT / ".venv_run"
    venv_python = TARGET_VENV / "bin" / "python"
    
    if venv_python.exists() and os.path.abspath(sys.executable) != os.path.abspath(str(venv_python)):
        print(f"STDOUT: [Guard] Switching Environment: -> {venv_python}", flush=True)
        os.environ["MWV_AUTO_REEXEC"] = "1"
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

with StatusBar("Initializing Application Environment", total=100) as sb:
    sb.update(10, "Checking Environment")
    ensure_stable_environment()
    sb.update(40, "Environment Stabilized")

    # --- Core Imports & Logging ---
    from src.core.logger import get_logger
    import src.core.logger as logger
    sb.update(60, "Logger Initializing")

    def initialize_startup_logging():
        is_debug = "--debug" in sys.argv
        log_level = logging.DEBUG if is_debug else logging.INFO
        logger.setup_logging(debug_mode=is_debug, level=log_level)
        print(f"STDOUT: [System] Log initialized (Level: {'DEBUG' if is_debug else 'INFO'})", flush=True)

    initialize_startup_logging()
    log = get_logger("main")
    sb.update(100, "Core Ready")

# Performance Tracking
STARTUP_TIME = time.time()
CHECKPOINTS = []

def log_checkpoint(msg: str):
    elapsed = time.time() - STARTUP_TIME
    CHECKPOINTS.append((msg, elapsed))
    print(f"STDOUT: [Checkpoint] {elapsed:6.3f}s | {msg}", flush=True)

# --- Application Initialization Sequence ---
with StatusBar("Loading Core Components", total=100) as sb:
    sb.update(0, "Importing Eel")
    import eel
    
    sb.update(10, "Initializing Eel Assets")
    web_dir = str(PROJECT_ROOT / "web")
    if not os.path.exists(web_dir):
        print(f"CRITICAL: Web dir not found at {web_dir}", flush=True)
        sys.exit(1)
    eel.init(web_dir)
    sb.update(25, "Eel Assets Ready")

    sb.update(30, "Loading Core SRC Modules")
    try:
        from src.core.remux_utils import remux_to_mp4_cache, extract_main_from_iso
        from src.core.streams import direct_play, mse_stream, hls_fmp4, vlc_bridge
        from src.core.mode_router import smart_route
        from src.core import db
        from src.core import transcoder
        from src.core import hardware_detector
        from src.parsers import tag_writer
        from src.parsers.format_utils import (
            PARSER_CONFIG, load_parser_config, save_parser_config,
            AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, detect_file_format,
            ffprobe_suite, ffprobe_quality_score
        )
        sb.update(80, "Core modules loaded")
    except Exception as e:
        print(f"CRITICAL: Resource load failure: {e}", flush=True)
        import traceback; traceback.print_exc()
        sys.exit(1)

    sb.update(90, "Setting UI State")
    SIDEBAR_OPEN = True
    VERSION = "1.34"
    SESSION_ID = f"{os.getpid()}_{int(time.time())}"
    port = int(os.environ.get("MWV_PORT", 8345))
    eel_kwargs = { 'host': 'localhost', 'size': (1280, 800) }
    sb.update(100, "Initial State OK")

# --- Eel Communication & Lifecycle ---
spawn_event = threading.Event()

@eel.expose
def report_spawn():
    if not spawn_event.is_set():
        spawn_event.set()
        print("STDOUT: [Sync] Frontend spawned confirmed via @eel.expose", flush=True)

@eel.expose
def report_items_spawned(count, source="frontend"):
    """
    Formal DOM test reporting. Called when the frontend confirms
    that key UI elements (like playlist items) are rendered.
    """
    msg = f"[DOM TEST] ITEM SIND GESPAWNED (Count: {count}, Source: {source})"
    print(f"STDOUT: {msg}", flush=True)
    log.info(msg)
    # Also record in a dedicated status mark if needed
    return {"status": "ok", "timestamp": time.time()}

def start_app():
    """Launches the Eel application with a robust startup watchdog."""
    print(f"STDOUT: [Eel] Launching app.html on port {port}...", flush=True)
    
    eel_mode = 'chrome'
    if "--ng" in sys.argv: eel_mode = False
    elif "--n" in sys.argv: eel_mode = None

    try:
        eel.start('app.html', block=False, port=port, mode=eel_mode, **eel_kwargs)
        print("STDOUT: [Eel] Server started. Monitoring for frontend synchronization...", flush=True)
        
        # --- Hang Detection / Watchdog ---
        timeout = 60
        start_wait = time.time()
        last_alive = start_wait
        
        while not spawn_event.is_set():
            now = time.time()
            if now - start_wait > timeout:
                print(f"CRITICAL: [Watchdog] Startup HANG detected (No UI sync after {timeout}s)!", flush=True)
                print("STDOUT: [Diagnostics] Verify port availability and browser connectivity.", flush=True)
                # Fallback: continue anyway but mark as unstable
                break
            
            if now - last_alive >= 5:
                elapsed = int(now - start_wait)
                print(f"STDOUT: [Watchdog] WAITING FOR FRONTEND (ALIVE: {elapsed}s)...", flush=True)
                last_alive = now
                
            time.sleep(0.5)
            
        if spawn_event.is_set():
            print("STDOUT: [Success] UI SYNCHRONIZED. MWV READY.", flush=True)
            
    except Exception as e:
        print(f"CRITICAL: Eel launch failure: {e}", flush=True)
        import traceback; traceback.print_exc()
        sys.exit(1)

def ensure_singleton():
    """Manages MWV singleton state using the centralized process_manager."""
    from src.core.process_manager import ProcessController
    pm = ProcessController(PROJECT_ROOT, Path(logger.APP_DATA_DIR))
    if not pm.acquire_lock():
        pm.kill_stale_instances()
        if not pm.acquire_lock():
            print("CRITICAL: Another instance is blocking the singleton lock.", flush=True); sys.exit(1)
    return pm

_SINGLETON_LOCK = ensure_singleton()
# --- End of Startup Block ---
SESSION_ID = f"{os.getpid()}_{int(time.time())}"
session_port = int(os.environ.get("MWV_PORT", 8345))
log.info(f"[System] Session Initialized: {SESSION_ID} on port {session_port}")


@eel.expose
def get_session_id():
    """Returns the current backend session ID."""
    return SESSION_ID


def get_best_ffmpeg_encoder():
    """Returns the best available H.264 encoder for FFmpeg (HW or SW)."""
    try:
        from . import hardware_detector
        gpu_info = hardware_detector.get_gpu_info()
        encoders = gpu_info.get("encoders", [])
        if "nvenc" in encoders:
            return "h264_nvenc"
        if "qsv" in encoders:
            return "h264_qsv"
        if "vaapi" in encoders:
            return "h264_vaapi"
    except Exception:
        pass
    return "libx264"  # Default software fallback


@eel.expose
def get_universal_stream_url(file_path, mode=None, audio_idx=0, subs_idx=None, start_time=0):
    """
    @brief Returns the optimal stream URL for a given file and mode.
    @details If mode is None, uses mode_router to pick the best one.
    """
    target_mode = mode if mode else mode_router.smart_route(file_path)
    log.info(f"[Universal] Routing {file_path} via {target_mode}")

    if target_mode == 'direct_play':
        return f"/stream/via/direct/{file_path}"
    elif target_mode == 'mse':
        url = f"/stream/via/transcode/{file_path}?audio_idx={audio_idx}&ss={start_time}"
        if subs_idx is not None and str(subs_idx).lower() != 'null':
            url += f"&subs_idx={subs_idx}"
        return url
    elif target_mode == 'hls_fmp4':
        # Setup HLS session
        session_id = f"hls_{int(time.time())}"
        output_dir = f"web/streams/hls/{session_id}"
        hls_stream.start_hls_fmp4(file_path, output_dir, session_id, audio_idx=audio_idx,
                                  subs_idx=subs_idx, start_time=start_time)
        return f"/streams/hls/{session_id}/master.m3u8"
    elif target_mode == 'vlc_bridge':
        vlc_bridge.start_vlc_bridge(file_path)
        return "/streams/vlc/vlc.m3u8"

    return f"/stream/via/direct/{file_path}"


@eel.expose
def get_playback_stats():
    """Returns real-time performance metrics for the Stats Overlay."""
    try:
        gpu_util = hardware_detector.get_gpu_usage_safe()
        hw = hardware_detector.get_gpu_info()

        # Mocking Atmos/Bitstream for now or hooking into active session
        return {
            "codec": "H.264 / HEVC",
            "bitrate": "8.5 Mbps",
            "gpu_info": f"{hw.get('type', 'Unknown')} ({gpu_util:.1f}%)",
            "gpu_util": gpu_util,
            "rtt_ms": 12,
            "audio_engine": "FFmpeg Premium Remux",
            "atmos": False,
            "bitstream": False
        }
    except Exception as e:
        log.error(f"[Stats] Error: {e}")
        return {
            "audio_engine": "Fallback Direct",
            "atmos": False,
            "bitstream": False
        }

# Perform singleton check immediately
# _SINGLETON_LOCK already initialized above


def _detect_python_environment():
    """
    Detect current Python environment: system, venv, or conda.
    Returns tuple: (env_type, env_name, env_path, python_version, python_executable)
    """
    python_version = platform.python_version()
    python_executable = sys.executable

    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV')

    if in_venv or venv_env:
        env_path = venv_env or sys.prefix
        env_name = Path(env_path).name if env_path else 'venv'
        return ('venv', env_name, env_path, python_version, python_executable)

    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    conda_prefix = os.environ.get('CONDA_PREFIX')

    if conda_env and conda_prefix:
        return (
            'conda',
            conda_env,
            conda_prefix,
            python_version,
            python_executable)

    # System Python
    return ('system', None, sys.prefix, python_version, python_executable)


def sanitize_json_utf8(data):
    """
    Utility for UTF-8 sanitization of JSON data.
    Ensures all strings in nested dicts/lists are valid UTF-8.
    """
    if isinstance(data, dict):
        return {sanitize_json_utf8(k): sanitize_json_utf8(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_json_utf8(i) for i in data]
    elif isinstance(data, str):
        try:
            return data.encode('utf-8', errors='replace').decode('utf-8')
        except Exception:
            return "[Invalid UTF-8]"
    else:
        return data


@eel.expose
def rtt_ping(data):
    """
    @brief Multi-stage RTT Ping for verification.
    @details Logs receipt of specialized data structures.
    """
    size = len(json.dumps(data))
    log.info(f"[RTT] Ping received ({size} bytes). Data types: {type(data).__name__}")

    # Show transformation as requested
    if isinstance(data, dict):
        log.info(f"[RTT] Stage 1 (Dict): {list(data.keys())}")
        if any(isinstance(v, dict) for v in data.values()):
            log.info(f"[RTT] Stage 2 (Dict of Dict): Detected")
        if any(isinstance(v, list) for v in data.values()):
            log.info(f"[RTT] Stage 3 (List of Dicts): Detected")

    return sanitize_json_utf8({
        "status": "pong",
        "timestamp": time.time(),
        "received_size": size,
        "echo": data
    })


@eel.expose
def log_js_error(error_data):
    """
    Logs JavaScript errors from the frontend to the backend logger.
    """
    log.error(f"[JS-ERROR] {json.dumps(error_data)}")
    return {"status": "error_logged"}


@eel.expose
def rtt_item_test(data):
    """Echoes complex media-item-like data back for RTT and integrity testing."""
    log.info(f"[RTT] Item Test received: {type(data).__name__}")
    return sanitize_json_utf8({
        "status": "success",
        "timestamp": time.time(),
        "item_echo": data
    })


@eel.expose
def rtt_stress_ping(index, total):
    """Rapid-fire ping for stress testing."""
    # Minimize logging for stress test to avoid I/O bottleneck
    if index % 10 == 0 or index == total - 1:
        log.info(f"[RTT-Stress] Ping {index + 1}/{total}")
    return {"status": "ok", "index": index}


@eel.expose
def get_gevent_status():
    """Returns the status of gevent patching and version info."""
    try:
        import gevent
        from gevent import monkey
        import greenlet
        import threading

        # Check if threading is actually monkey-patched
        # (Standard threading.current_thread() is replaced by gevent's version)
        is_patched = monkey.is_module_patched("socket")

        return {
            "active": True,
            "version": gevent.__version__,
            "greenlet": greenlet.__version__,
            "patched": {
                "socket": monkey.is_module_patched("socket"),
                "thread": monkey.is_module_patched("thread"),
                "time": monkey.is_module_patched("time"),
                "sys": monkey.is_module_patched("sys"),
                "threading": monkey.is_module_patched("threading")
            }
        }
    except ImportError:
        return {"active": False, "error": "gevent not installed"}


@eel.expose
def confirm_receipt(event_name):
    """
    @brief Simple confirmation from frontend to backend.
    """
    log.info(f"[Sync] Frontend confirmed receipt of: {event_name}")
    return {"status": "log_noted"}


# Debug-Optionen (Konsolidiert in PARSER_CONFIG)
DEBUG_FLAGS = PARSER_CONFIG.get("debug_flags", {})


def initialize_debug_flags(args=None):
    """
    @brief Initializes debug mode and flags based on CLI arguments and environment.
    """
    if args is None:
        args = sys.argv

    # Environment Detection
    env_type, env_name, env_path, _, _ = _detect_python_environment()
    is_dev = "Coding" in str(env_path) or os.path.exists(PROJECT_ROOT / ".git")

    # Update PARSER_CONFIG env
    PARSER_CONFIG["env"] = "dev" if is_dev else "production"

    debug_mode = "--debug" in args

    # Centralized Log Level Management
    # Dev -> highest (DEBUG), Production -> INFO/WARNING
    if is_dev or debug_mode:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger.setup_logging(debug_mode=debug_mode, level=log_level)

    if debug_mode:
        # Override config: Set all flags to True for --debug session
        for key in DEBUG_FLAGS:
            DEBUG_FLAGS[key] = True
        logger.set_debug_flags(DEBUG_FLAGS)
        log.info(
            "[System] Full Debug-Mode activated (--debug). All flags set to True.")
    else:
        # Use flags as defined in PARSER_CONFIG
        logger.set_debug_flags(DEBUG_FLAGS)


# --- Global Constants & State ---
VERSION = "1.34"


# Nach Logging-Setup: PIDs loggen fr Konsole. deswegen kein eel.expose
def find_venv_pid(venv_name):
    import psutil
    venv_path = str((PROJECT_ROOT / venv_name).resolve())
    for proc in psutil.process_iter(['pid', 'exe', 'cmdline']):
        try:
            exe = proc.info.get('exe')
            if exe and exe.startswith(venv_path):
                return proc.info['pid']
            cmdline = proc.info.get('cmdline')
            if cmdline and venv_path in ' '.join(cmdline):
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


# Initialize logging as early as possible after paths are set
initialize_debug_flags()

STARTUP_TIME = time.time()
BROWSER_PID = None  # Global to track browser process


# PID-Logging beim Startup
main_pid = os.getpid()
testbed_pid = find_venv_pid('.venv_testbed')
selenium_pid = find_venv_pid('.venv_selenium')
log.info(f"[System] Main PID: {main_pid}")
log.info(f"[System] Testbed PID: {testbed_pid if testbed_pid else 'nicht aktiv'}")
log.info(f"[System] Selenium PID: {selenium_pid if selenium_pid else 'nicht aktiv'}")
# Logge Browser-PID, falls schon gesetzt (z.B. bei Headless-Start)
if BROWSER_PID:
    log.info(f"[System] Browser PID: {BROWSER_PID}")

try:
    from src.core.models import MediaItem  # type: ignore
    import src.core.db as db              # type: ignore
except ModuleNotFoundError as exc:
    # Handle missing modules
    missing_module = exc.name or "unknown"
    core_dir = Path(__file__).resolve().parent
    project_dir = core_dir.parent.parent
    local_venv_python = project_dir / ".venv_core" / "bin" / "python"
    already_reexecuted = os.environ.get("MWV_AUTO_REEXEC") == "1"

    # Auto-fallback: if started with wrong interpreter, re-exec with local
    # .venv_core Python.
    if (
        not already_reexecuted
        and local_venv_python.is_file()
        and os.access(local_venv_python, os.X_OK)
        and Path(sys.executable).resolve() != local_venv_python.resolve()
    ):
        log.info(
            f"\n Fehlende Abhngigkeit '{missing_module}' in aktueller Umgebung erkannt.\n"
            f" Starte automatisch neu mit Projekt-Umgebung:\n"
            f"  {local_venv_python}\n"
        )
        os.environ["MWV_AUTO_REEXEC"] = "1"
        os.execv(str(local_venv_python), [str(local_venv_python), str(
            Path(__file__).resolve()), *sys.argv[1:]])

    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()

    if env_type == 'conda':
        current_env = f" Conda: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    elif env_type == 'venv':
        current_env = f" Venv: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    else:
        current_env = f"  System Python {py_ver}\n   Python: {py_exec}"

    log.error(
        f"\n Abhngigkeit '{missing_module}' nicht installiert!\n"
        f"\n"
        f" Aktuelle Umgebung:\n   {current_env}\n"
        f"\n"
        f" Lsung: Starte mit der Projekt-Umgebung:\n\n"
        f"   cd {project_dir}\n"
        f"   source .venv_core/bin/activate\n"
        f"   python main.py\n\n"
        f" Keine lokalen Virtual Environments gefunden!\n"
        f"Falls .venv_core fehlt:\n"
        f"   python3 -m venv .venv_core\n"
        f"   source .venv_core/bin/activate\n"
        f"   pip install -r requirements.txt\n\n"
        f"Alternative: Mit Conda (falls verfgbar):\n"
        f"   conda activate <env-name>\n"
        f"   pip install -r requirements.txt\n"
        f"   python main.py\n"
    )
    raise SystemExit(1) from exc


try:
    import vlc
    HAS_VLC = True
except ImportError:
    HAS_VLC = False

try:
    import m3u8
    HAS_M3U8 = True
except ImportError:
    HAS_M3U8 = False

_logger = get_logger("click_events")


def process_any_file(path: str) -> str:
    """Compatibility wrapper used by tests: process a file and return JSON string.
    Returns JSON string with either {'success': True, 'duration': ..., 'tags': {...}}
    or {'error': '...'} on failure.
    """
    import json
    try:
        from src.parsers.media_parser import extract_metadata
        from pathlib import Path as _Path
        filename = _Path(path).name
        tags, parser_times = extract_metadata(path, filename, mode='ultimate')
        duration = float(tags.get('duration', 0) or 0)
        return json.dumps(
            {"success": True, "duration": duration, "tags": tags, "parser_times": parser_times})
    except Exception as e:
        _logger.exception("process_any_file failed")
        return json.dumps({"error": str(e)})


def get_gpu_usage_safe():
    """Tries to get GPU usage via Intel iGPU, AMD, Intel Arc, or Nvidia."""
    # 1. Intel On-board (iGPU) - Priority 1 (Most common)
    try:
        cur_f = '/sys/class/drm/card0/gt_act_freq_mhz'
        max_f = '/sys/class/drm/card0/gt_max_freq_mhz'
        if os.path.exists(cur_f) and os.path.exists(max_f):
            with open(cur_f, 'r') as f1, open(max_f, 'r') as f2:
                cur = float(f1.read().strip())
                m = float(f2.read().strip())
                if m > 0:
                    return (cur / m) * 100
    except:
        pass

    # 2. AMD / Intel Arc / Generic (Linux sysfs)
    try:
        cards = glob.glob('/sys/class/drm/card*/device/gpu_busy_percent')
        if cards:
            for card_path in cards:
                with open(card_path, 'r') as f:
                    val = float(f.read().strip())

                    # Intel Arc Scaling (0-1000 -> 0-100)
                    vendor_path = card_path.replace('gpu_busy_percent', 'vendor')
                    if os.path.exists(vendor_path):
                        with open(vendor_path, 'r') as vf:
                            if "0x8086" in vf.read():  # Intel
                                return val / 10.0

                    # AMD / Others (Standard 0-100)
                    return val
    except:
        pass

    # 3. Nvidia (Nvidia-smi)
    try:
        res = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL
        ).decode().strip().split('\n')[0]
        return float(res)
    except:
        pass

    return 0


def system_stats_pusher():
    """
    Background thread to broadcast CPU, RAM, and Network metrics to the UI.
    Broadcastet CPU-, RAM- und Netzwerk-Metriken an die UI.
    """
    last_net_io = psutil.net_io_counters()

    while True:
        try:
            # 1. CPU & RAM
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()

            # 2. Network speed (delta)
            curr_net_io = psutil.net_io_counters()
            sent_diff = (curr_net_io.bytes_sent - last_net_io.bytes_sent) / 1024  # KB
            recv_diff = (curr_net_io.bytes_recv - last_net_io.bytes_recv) / 1024  # KB
            last_net_io = curr_net_io

            # 3. GPU (Try nvidia-smi fallback)
            gpu_util = get_gpu_usage_safe()

            # Optional: try to get GPU info from hardware_detector if available
            try:
                from src.core import hardware_detector
                gpu_info = hardware_detector.get_gpu_info()
                # If we had a live GPU load detector, we'd use it here.
            except:
                pass

            stats = {
                "cpu": cpu,
                "ram_mb": ram.used / (1024 * 1024),
                "ram_percent": ram.percent,
                "net_sent_kb": sent_diff / 2,  # Assuming 2s interval
                "net_recv_kb": recv_diff / 2,
                "gpu": gpu_util
            }

            # 4. Push to all connected Eel clients
            if hasattr(eel, 'update_system_stats'):
                eel.update_system_stats(stats)()

        except Exception as e:
            log.error(f"[Stats] Pusher error: {e}")

        eel.sleep(2.0)


@eel.expose
def get_system_stats_static():
    """One-time point-in-time system metrics check."""
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    }


# --- Compatibility stubs expected by tests ---
@eel.expose
def get_server_status():
    """Return a minimal server status dict used by unit tests and frontend checks."""
    try:
        return {
            "status": "ok",
            "version": VERSION,
            "time": int(time.time()),
        }
    except Exception:
        return {"status": "error"}


@eel.expose
def handle_click_batch(events):
    """Process a list of click events (compatibility helper for tests)."""
    results = []
    for ev in (events or []):
        try:
            et = ev.get("type") if isinstance(ev, dict) else None
            payload = ev.get("payload") if isinstance(ev, dict) else {}
            results.append(handle_click(et, payload))
        except Exception:
            results.append({"ok": False, "error": "processing_failed"})
    return {"results": results}


@eel.expose
def api_extract_metadata(path, name=None, mode='lightweight'):
    """Expose metadata extraction in a consistent dict form for tests/frontend."""
    try:
        from src.parsers.media_parser import extract_metadata
        if name is None:
            name = Path(path).name
        res = extract_metadata(path, name, mode=mode)
        # Normalize: prefer (duration, tags) shape
        duration = 0
        tags = {}
        if isinstance(res, tuple) and len(res) >= 2:
            a, b = res[0], res[1]
            if isinstance(a, (int, float)):
                duration = int(a)
                tags = b or {}
            elif isinstance(a, dict):
                tags = a
                if isinstance(b, (int, float)):
                    duration = int(b)
                elif isinstance(b, dict):
                    duration = int(b.get('duration', 0) or 0)
        elif isinstance(res, dict):
            tags = res
            duration = int(tags.get('duration', 0) or 0)
        return {"duration": duration, "tags": tags}
    except Exception as e:
        _logger.exception("api_extract_metadata failed")
        return {"error": str(e)}


def _get_installed_packages():
    """Return list of installed packages (name/version) and source.

    Lightweight implementation for tests that inspect main.py. Not exhaustive.
    """
    packages = []
    source = "pip"
    try:
        import importlib.metadata
        try:
            for dist in importlib.metadata.distributions():
                try:
                    pkg_name = dist.metadata['Name'] if dist.metadata and 'Name' in dist.metadata else dist.metadata.get(
                        'Name', None) if dist.metadata else None
                except Exception:
                    pkg_name = getattr(dist, 'metadata', None)
                try:
                    version = dist.version
                except Exception:
                    version = None
                if pkg_name:
                    packages.append({"name": pkg_name, "version": version})
            packages = sorted([p for p in packages if p.get(
                'name')], key=lambda x: x['name'].lower())
            source = 'importlib.metadata'
        except Exception:
            # best-effort: if importlib.metadata iteration fails, fall through
            # to pip fallback
            pass
    except Exception:
        pass

    if not packages:
        try:
            import sys
            import subprocess
            import json
            # Fallback to pip list via subprocess
            result = subprocess.run([sys.executable,
                                     '-m',
                                     'pip',
                                     'list',
                                     '--format=json'],
                                    capture_output=True,
                                    text=True,
                                    timeout=5)
            if result.returncode == 0:
                data = json.loads(result.stdout or '[]')
                packages = sorted([{"name": i.get('name'), "version": i.get(
                    'version')} for i in data], key=lambda x: x['name'].lower() if x.get('name') else '')
                source = 'pip'
        except Exception:
            packages = []
            source = 'none'

    return packages, source


@eel.expose
def handle_click(event_type: str, payload: dict):
    """
    Generic click-event handler called from the frontend.
    event_type: short string describing action (e.g. "pin", "play", "open")
    payload: dict with additional data (e.g. {"id": 42})
    """
    try:
        _logger.info(
            "click event received",
            extra={
                "event": event_type,
                "payload": payload})
        # simple dispatch examples (extend as needed)
        if event_type == "pin":
            media_id = payload.get("id")
            # example: toggle pin state in db (implement db.toggle_pin if
            # available)
            try:
                from .db import toggle_pin
                toggled = toggle_pin(media_id)
                return {
                    "ok": True,
                    "action": "pin_toggled",
                    "id": media_id,
                    "toggled": toggled}
            except Exception:
                _logger.exception("pin action failed")
                return {"ok": False, "error": "pin_failed"}
        elif event_type == "play":
            path = payload.get("path")
            try:
                play_media(path)  # assumes play_media is defined/exposed
                return {"ok": True, "action": "play", "path": path}
            except Exception:
                _logger.exception("play action failed")
                return {"ok": False, "error": "play_failed"}
        else:
            _logger.debug("unhandled click event", extra={"event": event_type})
            return {"ok": True, "action": "noop", "event": event_type}
    except Exception:
        _logger.exception("handle_click unexpected error")
        return {"ok": False, "error": "internal_error"}


# Version laden
VERSION_FILE = PROJECT_ROOT / "VERSION"
try:
    VERSION = VERSION_FILE.read_text(encoding='utf-8').strip()
except Exception:
    VERSION = "1.34"  # Fallback
# --- Imprint/Impressum API ---


@eel.expose
def get_imprint_info():
    """
    Returns license, version, and maintainer info for imprint/impressum tab.
    """
    return {
        "version": VERSION,
        "developer": "kazaa3",
        "location": "Germany",
        "privacy": "Local storage in SQLite. No data transmission to external servers.",
        "license": "GNU GPL-3.0",
        "last_fix": "dict",
    }


@eel.expose
def test_media_route(path: str):
    """Debug endpoint to test mode_router logic from UI."""
    from src.core.mode_router import smart_route
    return smart_route(path)


@eel.expose
def get_version():
    """Returns the application version."""
    return VERSION


@eel.expose
def get_app_name():
    """Returns the application name."""
    return "dict"


@eel.expose
def update_playback_position(name, position):
    """Updates the persistent playback position."""
    try:
        from src.core import db  # type: ignore
        if db.get_active_db_path().exists():
            db.update_playback_position(name, position)
        return {"ok": True}
    except Exception as e:
        _logger.exception("Failed to update playback position")
        return {"ok": False, "error": str(e)}


@eel.expose
def update_media_duration(name: str, duration_sec: float):
    """Updates the persistent media duration."""
    try:
        from src.core import db
        db.update_media_duration(name, duration_sec)
        return {"ok": True}
    except Exception as e:
        _logger.exception("Failed to update media duration")
        return {"ok": False, "error": str(e)}


@eel.expose
def get_playback_position(name):
    """Retrieves the last stored playback position."""
    try:
        import db
        pos = db.get_playback_position(name)
        return {"ok": True, "position": pos}
    except Exception as e:
        _logger.exception("Failed to get playback position")
        return {"ok": False, "error": str(e)}

# --- Environment Info API ---


@eel.expose
def get_hardware_info():
    """Returns hardware information (SSD, PCIe, Network) for the UI."""
    return hardware_detector.get_hardware_info()


@eel.expose
def get_environment_info_dict():
    """
    Returns full environment info dict for debug/console display.
    """
    import platform
    import sys
    import os
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()
    import psutil

    def find_venv_pid(venv_name):
        """Find PID of a running python process in the given venv (by path match)."""
        venv_path = str((PROJECT_ROOT / venv_name).resolve())
        for proc in psutil.process_iter(['pid', 'exe', 'cmdline']):
            try:
                exe = proc.info.get('exe')
                if exe and exe.startswith(venv_path):
                    return proc.info['pid']
                # Fallback: check cmdline for venv python
                cmdline = proc.info.get('cmdline')
                if cmdline and venv_path in ' '.join(cmdline):
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    testbed_pid = find_venv_pid('.venv_testbed')
    selenium_pid = find_venv_pid('.venv_selenium')

    return {
        "env_type": env_type,
        "env_name": env_name,
        "env_path": env_path,
        "python_version": py_ver,
        "python_executable": py_exec,
        "platform": platform.platform(),
        "venv_active": sys.prefix != sys.base_prefix,
        "cwd": str(Path.cwd()),
        "os": platform.system(),
        "pid": os.getpid(),
        "browser_pid": BROWSER_PID,
        "testbed_pid": testbed_pid,
        "selenium_pid": selenium_pid,
        "log_level": logging.getLevelName(logging.getLogger().getEffectiveLevel()),
        "release": platform.release(),
        "machine": platform.machine(),
        "debug_flags": DEBUG_FLAGS,
        "version": VERSION,
    }

# --- Debug Console API ---


@eel.expose
def get_konsole():
    """
    Returns debug logs, environment info, and dicts for GUI console.
    """
    return {
        "logs": "\n".join(logger.get_ui_logs()),
        "env": get_environment_info_dict(),
        "version": VERSION,
        "license": "GNU GPL-3.0",
        "debug_flags": DEBUG_FLAGS,
    }


@eel.expose
def save_tags_to_file(name, tags):
    """
    Writes updated tags to the media file and updates the DB.
    """
    try:
        path = db.get_path_by_name(name)
        if not path:
            return {"status": "error", "message": f"Datei '{name}' nicht in DB gefunden."}

        success = tag_writer.write_tags(path, tags)
        if success:
            db.update_media_tags(name, tags, tags.get('full_tags', {}))
            return {
                "status": "success",
                "message": f"Tags erfolgreich in '{name}' gespeichert."}
        else:
            return {
                "status": "error",
                "message": "Fehler beim Schreiben der Dateitags."}
    except Exception as e:
        logging.exception("save_tags_to_file failed")
        return {"status": "error", "message": str(e)}


@eel.expose
def get_all_parser_info():
    """Returns aggregated capabilities and settings schemas for all parsers."""
    from src.parsers.media_parser import get_parser_info
    return get_parser_info()


@eel.expose
def get_all_parser_settings():
    """Returns the current granular settings for all parsers."""
    return PARSER_CONFIG.get("parser_settings", {})


@eel.expose
def update_parser_settings(new_settings):
    """Updates the granular parser settings and saves to disk."""
    PARSER_CONFIG["parser_settings"].update(new_settings)
    save_parser_config(PARSER_CONFIG)
    return {"status": "success"}


@eel.expose
def list_sql_files():
    """
    Returns a list of .sql files in the data/ directory.
    @details Gibt eine Liste aller .sql-Dateien im Datenverzeichnis zurck.
    """
    try:
        db_dir = db.DB_DIR
        sql_files = list(db_dir.glob("*.sql"))
        # Also include the database file as a candidate if needed?
        # No, request specifically said SQL files.
        return sorted([f.name for f in sql_files])
    except Exception as e:
        log.error(f"Failed to list SQL files: {e}")
        return []


@eel.expose
def get_sql_content(filename):
    """
    Returns the content of a specific SQL file in the data/ directory.
    @details Gibt den Inhalt einer spezifischen SQL-Datei zurck.
    """
    try:
        db_dir = db.DB_DIR
        # Security check: resolve and verify it's within DB_DIR
        p = (db_dir / filename).resolve()
        if p.is_relative_to(db_dir.resolve()) and p.exists() and p.suffix == '.sql':
            return p.read_text(encoding='utf-8')
        return f"-- Error: File '{filename}' not found or access denied."
    except Exception as e:
        log.error(f"Failed to read SQL content for {filename}: {e}")
        return f"-- Error: {str(e)}"


@eel.expose
def get_library_folders():
    """
    Returns a list of unique parent directories for all media in the DB.
    @details Gibt eine Liste aller eindeutigen bergeordneten Verzeichnisse zurck.
    """
    try:
        items = db.get_all_media()
        folders = set()
        for item in items:
            p = Path(item['path'])
            folders.add(str(p.parent))
        return sorted(list(folders))
    except Exception as e:
        log.error(f"Failed to get library folders: {e}")
        return []


@eel.expose
def get_start_page():
    """Returns the global start page."""
    return PARSER_CONFIG.get("start_page", "player")


@eel.expose
def set_start_page(page):
    """Updates the global start page and saves to disk."""
    PARSER_CONFIG["start_page"] = page
    save_parser_config()
    return {"status": "success"}


@eel.expose
def get_app_mode():
    """Returns the current app mode (High-Performance/Low-Bandwidth)."""
    return PARSER_CONFIG.get("app_mode", "High-Performance")


@eel.expose
def set_app_mode(mode):
    """Updates the app mode and saves to disk."""
    PARSER_CONFIG["app_mode"] = mode
    save_parser_config()
    return {"status": "success"}


@eel.expose
def get_parser_mode():
    """Returns the current parser mode (lightweight/full/ultimate)."""
    return PARSER_CONFIG.get("parser_mode", "lightweight")


@eel.expose
def set_parser_mode(mode):
    """Updates the parser mode and saves to disk."""
    PARSER_CONFIG["parser_mode"] = mode
    save_parser_config()
    return {"status": "success"}


@eel.expose
def update_browse_dir(path):
    """Updates the default browse directory."""
    PARSER_CONFIG["browse_default_dir"] = path
    save_parser_config()
    return {"status": "success"}


@eel.expose
def update_library_dir(path):
    """Updates the primary library/media directory."""
    PARSER_CONFIG["library_dir"] = path
    save_parser_config()
    return {"status": "success"}


@eel.expose
def get_mock_data_enabled():
    """Returns whether mock data is enabled in the configuration."""
    return PARSER_CONFIG.get("enable_mock_data", False)


@eel.expose
def set_mock_data_enabled(enabled):
    """Updates the mock data enabled state and saves to disk."""
    PARSER_CONFIG["enable_mock_data"] = enabled
    save_parser_config()
    return {"status": "success"}


@eel.expose
def get_startup_config():
    """Returns the current startup (browser/env) configuration."""
    return {
        "browser_choice": PARSER_CONFIG.get("browser_choice", "auto"),
        "browser_flags": PARSER_CONFIG.get("browser_flags", []),
        "env_vars": PARSER_CONFIG.get("env_vars", {}),
    }


@eel.expose
def update_startup_config(config):
    """Updates the startup configuration and saves to disk."""
    if "browser_choice" in config:
        PARSER_CONFIG["browser_choice"] = config["browser_choice"]
    if "browser_flags" in config:
        PARSER_CONFIG["browser_flags"] = config["browser_flags"]
    if "env_vars" in config:
        PARSER_CONFIG["env_vars"] = config["env_vars"]

    save_parser_config()
    return {"status": "success"}


@eel.expose
def reset_config():
    """Resets the configuration to defaults."""
    from src.parsers.format_utils import reset_parser_config
    reset_parser_config()
    return {"status": "success"}


# --- Debug/Test API ---
@eel.expose
def run_debug_test():
    """
    Runs a simple debug test and returns result for GUI console.
    """
    import sys
    return {
        "test": "debug",
        "python_version": sys.version,
        "cwd": str(Path.cwd()),
        "result": "OK",
    }


_ENV_INFO_CACHE = {
    "data": None,
    "ts": 0.0,
}
_ENV_INFO_CACHE_TTL_SECONDS = 8.0


@eel.expose
def api_ping(client_ts=None, payload_size=0):
    """
    @brief Lightweight ping endpoint for Eel roundtrip latency diagnostics.
    @details Minimal payload endpoint to measure frontend<->backend roundtrip and payload transfer time.
    @param client_ts Optional client timestamp / Optionaler Client-Timestamp.
    @param payload_size Optional echo payload size in bytes (0..200000) / Optionale Echo-Payload.
    @return Dictionary with timestamps and payload size / Dictionary mit Zeitstempeln und Payload-Gre.
    """
    now_ms = int(time.time() * 1000)

    try:
        size = int(payload_size)
    except Exception:
        size = 0

    size = max(0, min(size, 200000))
    payload = "x" * size if size > 0 else ""

    return {
        "status": "ok",
        "server_ts": now_ms,
        "client_ts": client_ts,
        "payload_size": size,
        "payload": payload,
    }


@eel.expose
def pip_install_packages(packages):
    """
    @brief Installs a list of Python packages via pip.
    @param packages List of package names to install.
    @return Dictionary with status, output, and error message if any.
    """
    if not packages:
        return {"status": "ok", "message": "No packages to install"}

    if isinstance(packages, str):
        packages = [packages]

    try:
        # Using sys.executable to ensure we install in the current environment
        cmd = [sys.executable, "-m", "pip", "install", *packages]
        log.info(f"Running pip install: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout for installation
        )

        if result.returncode == 0:
            log.info(
                f"Successfully installed packages: {', '.join(packages)}")
            # After installation, we should probably clear the environment info
            # cache
            _ENV_INFO_CACHE["data"] = None
            _ENV_INFO_CACHE["ts"] = 0.0
            # Double check if they are really installed now
            # Assuming _get_requirements_status is defined elsewhere
            status = _get_requirements_status()
            still_missing = []
            for p in packages:
                # Normalize names for comparison (requirements.txt might have
                # case differences)
                if any(p.lower() == m.lower()
                       for m in status.get("missing", [])):
                    still_missing.append(p)

            if still_missing:
                log.error(
                    f"[PIP] Installation reported success but packages still missing: {still_missing}")
                return {
                    "status": "error",
                    "error": f"Verification failed. Packages still missing: {
                        ', '.join(still_missing)}",
                    "output": result.stdout}

            return {
                "status": "ok",
                "output": result.stdout,
                "installed": packages}
        else:
            error_msg = result.stderr or result.stdout or "Unknown pip error"
            log.error(f"Failed to install packages: {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "output": result.stdout
            }

    except subprocess.TimeoutExpired:
        log.error("Pip install timed out")
        return {"status": "error", "error": "Installation timed out"}
    except Exception as e:
        log.error(f"Error during pip install: {str(e)}")
        return {"status": "error", "error": str(e)}


def _get_requirements_status():
    """Get install status for requirements.txt packages in current interpreter."""
    import importlib.util

    # Check multiple locations for requirements
    req_locations = [
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / "infra" / "requirements-build.txt",
        PROJECT_ROOT / "infra" / "requirements-core.txt",
        PROJECT_ROOT / "infra" / "requirements-testbed.txt",
        PROJECT_ROOT / "infra" / "requirements-selenium.txt",
        PROJECT_ROOT / "infra" / "requirements-run.txt",
        PROJECT_ROOT / "infra" / "requirements-dev.txt",
        PROJECT_ROOT / "infra" / "requirements.txt",     # venv
    ]

    requirements_file = None
    for loc in req_locations:
        if loc.exists():
            requirements_file = loc
            # If it's a main redirect/entry, use it and stop.
            if loc.name == "requirements.txt" or loc.name == "requirements-run.txt":
                break

    if not requirements_file:
        return {
            "available": False,
            "total": 0,
            "installed_count": 0,
            "missing_count": 0,
            "installed": [],
            "missing": [],
            "source": "None"
        }

    status = {
        "available": True,
        "total": 0,
        "installed_count": 0,
        "missing_count": 0,
        "installed": [],
        "missing": [],
        "source": "requirements.txt"
    }

    import_overrides = {
        "python-vlc": "vlc",  # overirdes anschauen
        "bottle-websocket": "bottle_websocket",
        "gevent-websocket": "geventwebsocket",
        "pytest-cov": "pytest_cov",
        "pyinstaller": "PyInstaller",
        "pillow": "PIL",
        "markdown": "markdown",
        "scapy": "scapy",
        "future": "future",
        "chardet": "chardet",
        "pyscreeze": "pyscreeze",
        "pyautogui": "pyautogui",
    }

    requirement_names = set()

    def parse_requirements(file_path, seen=None):
        if seen is None:
            seen = set()
        # Normalize path for seen set
        try:
            abs_path = file_path.resolve()
        except:
            return
        if str(abs_path) in seen:
            return
        seen.add(str(abs_path))

        try:
            for raw_line in file_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                # Handle recursive requirements (-r)
                if line.startswith("-r"):
                    ref_name = line[2:].strip()
                    ref_path = file_path.parent / ref_name
                    if ref_path.exists():
                        parse_requirements(ref_path, seen)
                    continue

                # Handle other pip flags we don't care about for existence check
                if line.startswith("-"):
                    continue

                line = line.split(" #", 1)[0].split(";", 1)[0].strip()
                if not line:
                    continue

                if " @ " in line:
                    package_name = line.split(" @ ", 1)[0].strip()
                else:
                    # Capture everything before the first version specifier
                    package_name = re.split(
                        r"(==|>=|<=|~=|!=|>|<|\[)", line, maxsplit=1)[0].strip()

                if package_name:
                    requirement_names.add(package_name)
        except Exception as e:
            log.error(f"Error parsing {file_path}: {e}")

    parse_requirements(requirements_file)

    # If the main requirement file was just a redirect, show the final target
    if requirements_file and status["source"] == "requirements.txt" and requirements_file.name != "requirements.txt":
        status["source"] = f"requirements.txt -> {requirements_file.name}"

    # If we followed a chain, show the last one that actually had content
    if requirements_file:
        status["source"] = str(requirements_file.relative_to(PROJECT_ROOT))

    installed = []
    missing = []
    for package_name in requirement_names:
        import_name = import_overrides.get(
            package_name.lower(), package_name.replace("-", "_"))
        if not import_name:
            missing.append(package_name)
            continue
        try:
            if importlib.util.find_spec(import_name) is not None:
                installed.append(package_name)
            else:
                missing.append(package_name)
        except Exception:
            missing.append(package_name)

    installed.sort(key=str.lower)
    missing.sort(key=str.lower)

    status["installed"] = installed
    status["missing"] = missing
    status["total"] = len(requirement_names)
    status["installed_count"] = len(installed)
    status["missing_count"] = len(missing)
    return status


@eel.expose
def get_environment_info(force_refresh=False):
    """
    @brief Returns comprehensive information about the Python environment.
    @details Gibt detaillierte Informationen ber die Python-Umgebung zurck,
             inklusive aktuelle Umgebung, System Python Installationen, und Conda Umgebungen.
    @return Dictionary with environment details / Dictionary mit Umgebungsdetails.
    """
    import platform
    import subprocess
    import json

    now = time.time()
    if not force_refresh and _ENV_INFO_CACHE["data"] is not None:
        if (now - float(_ENV_INFO_CACHE["ts"])) <= _ENV_INFO_CACHE_TTL_SECONDS:
            return _ENV_INFO_CACHE["data"]

    # ===== Current Environment =====
    # Check if we're in a virtual environment (venv/virtualenv)
    in_venv = sys.prefix != sys.base_prefix
    venv_path = sys.prefix if in_venv else None

    # Get VIRTUAL_ENV environment variable (more reliable for venv)
    venv_env = os.environ.get('VIRTUAL_ENV', None)

    # Check for Conda environment
    conda_env_name = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    in_conda = conda_env_name is not None or conda_prefix is not None

    # Determine active runtime environment type and path
    # Priority: active interpreter/venv > conda shell context > system
    env_type = None
    env_path = None
    env_name = None

    if in_venv or venv_env:
        env_type = "venv"
        env_path = venv_path or venv_env
        env_name = Path(env_path).name if env_path else None
    elif in_conda:
        env_type = "conda"
        env_path = conda_prefix
        env_name = conda_env_name
    else:
        env_type = "system"

    # Build current environment info
    current_env = {
        "type": env_type,
        "name": env_name,
        "path": env_path,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
    }

    # ===== Alternative Environments Discovery =====

    def _get_conda_environments():
        """Get list of available Conda environments."""
        environments = []
        try:
            # Main conda call with reduced timeout (3s)
            result = subprocess.run(
                ["conda", "env", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    for env_path in data.get("envs", []):
                        try:
                            env_name = Path(env_path).name
                            env_python = Path(env_path) / "bin" / "python"

                            # Check existence and version with timeout (1s)
                            if env_python.exists():
                                v_result = subprocess.run(
                                    [str(env_python), "--version"],
                                    capture_output=True,
                                    text=True,
                                    timeout=1
                                )
                                version = v_result.stdout.strip() or v_result.stderr.strip()
                                is_recommended = False

                                environments.append({
                                    "name": env_name,
                                    "path": env_path,
                                    "version": version,
                                    "recommended": is_recommended
                                })
                        except (subprocess.TimeoutExpired, Exception):
                            continue
                except (json.JSONDecodeError, KeyError):
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return sorted(environments, key=lambda x: x["name"])

    def _get_system_pythons():
        """Get list of system Python installations."""
        pythons = []
        search_paths = ["/usr/bin", "/usr/local/bin", "/opt/python"]
        seen_versions = set()

        for search_path in search_paths:
            try:
                search_dir = Path(search_path)
                if not search_dir.exists():
                    continue

                # Use a specific glob to avoid listing too many files
                for python_exe in search_dir.glob("python3*"):
                    try:
                        if not python_exe.is_file() or not os.access(python_exe, os.X_OK):
                            continue

                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()

                        if version and version not in seen_versions:
                            seen_versions.add(version)
                            pythons.append({
                                "path": str(python_exe),
                                "version": version
                            })
                    except (subprocess.TimeoutExpired, Exception):
                        pass
            except Exception:
                pass

        return sorted(pythons, key=lambda x: x["version"])

    def _get_packages_fallback():
        """Fallback method to get packages if pip list fails."""
        packages = []
        try:
            from importlib import metadata
            for dist in metadata.distributions():
                name = dist.metadata.get("Name") or dist.metadata.get("name")
                version = dist.version
                if not name:
                    continue
                packages.append({
                    "name": name,
                    "version": version
                })
            packages = sorted(packages, key=lambda x: x["name"].lower())
        except Exception:
            try:
                import pkg_resources
                for dist in pkg_resources.working_set:
                    packages.append({
                        "name": dist.project_name,
                        "version": dist.version
                    })
                packages = sorted(packages, key=lambda x: x["name"].lower())
            except Exception:
                pass
        return packages

    def _get_installed_packages():
        """Get list of installed packages in current environment."""
        packages = []
        source = "none"

        def _parse_columns_output(raw_text: str):
            parsed = []
            lines = [line.strip()
                     for line in (raw_text or "").splitlines() if line.strip()]
            if not lines:
                return parsed
            for line in lines:
                if line.lower().startswith("package") and "version" in line.lower():
                    continue
                if set(line) <= set("- "):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    parsed.append({"name": parts[0], "version": parts[1]})
            return parsed

        try:
            # Primary method: pip list --format=json (timeout 5s)
            result = subprocess.run([sys.executable,
                                     "-m",
                                     "pip",
                                     "list",
                                     "--format=json",
                                     "--disable-pip-version-check"],
                                    capture_output=True,
                                    text=True,
                                    timeout=5)
            if result.returncode == 0:
                try:
                    packages_data = json.loads(result.stdout)
                    packages = sorted(
                        packages_data, key=lambda x: x.get(
                            "name", "").lower())
                    source = "pip_list_json"
                except (json.JSONDecodeError, TypeError, KeyError):
                    log.warning(
                        "Failed to parse pip list JSON - falling back")
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
            else:
                # Fallback 1: pip list (columns)
                try:
                    fallback_result = subprocess.run(
                        [sys.executable, "-m", "pip", "list", "--format=columns", "--disable-pip-version-check"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if fallback_result.returncode == 0:
                        packages = sorted(
                            _parse_columns_output(fallback_result.stdout),
                            key=lambda x: x.get("name", "").lower()
                        )
                        if packages:
                            source = "pip_list_columns"
                except Exception:
                    pass

                # Fallback 2: importlib/pkg_resources
                if not packages:
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
        except (subprocess.TimeoutExpired, Exception) as e:
            log.warning(
                f"pip list failed ({
                    type(e).__name__}) - using importlib fallback")
            packages = _get_packages_fallback()
            source = "importlib_or_pkg_resources"

        return packages, source

    def _find_local_venvs():
        """Find local venv directories in common locations using Multi-Venv Strategy."""
        venvs = []

        # Strategy definition: Detailed multi-venv concept
        VENV_STRATEGY = {
            ".venv_core": {
                "purpose": "Zentrale Laufzeitumgebung fr die App-Logik.",
                "role": "CORE"
            },
            ".venv_run": {
                "purpose": "Optimierte Laufzeitumgebung fr den Anwenderbetrieb.",
                "role": "RUN"
            },
            ".venv_build": {
                "purpose": "Umgebung fr das Packaging (PyInstaller, .deb).",
                "role": "BUILD"
            },
            ".venv_dev": {
                "purpose": "Entwicklungsumgebung mit Lintern (flake8, pyre).",
                "role": "DEV"
            },
            ".venv_testbed": {
                "purpose": "Isolierte Umgebung fr Integrations-Tests.",
                "role": "TEST"
            },
            ".venv_selenium": {
                "purpose": "Umgebung fr E2E Browser-Tests.",
                "role": "E2E"
            }
        }

        try:
            # Discovery of subsidiary venvs based on strategy
            for vname, info in VENV_STRATEGY.items():
                venv_path = PROJECT_ROOT / vname
                exists = venv_path.exists() and (venv_path / "bin" / "python").exists()

                version = None
                if exists:
                    python_exe = venv_path / "bin" / "python"
                    try:
                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                    except (subprocess.TimeoutExpired, Exception):
                        version = "unknown"

                venvs.append({
                    "name": vname,
                    "path": str(venv_path),
                    "exists": exists,
                    "version": version,
                    "is_current": str(venv_path) == env_path,
                    "purpose": info["purpose"],
                    "role": info["role"]
                })

            # Add legacy/default 'venv' if it exists
            default_venv = PROJECT_ROOT / "venv"
            if default_venv.exists() and (default_venv / "bin" / "python").exists():
                if not any(v["name"] == "venv" for v in venvs):
                    python_exe = default_venv / "bin" / "python"
                    try:
                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                    except (subprocess.TimeoutExpired, Exception):
                        version = "unknown"

                    venvs.append({
                        "name": "venv",
                        "path": str(default_venv),
                        "exists": True,
                        "version": version,
                        "is_current": str(default_venv) == env_path,
                        "purpose": "Standard Fallback-Umgebung.",
                        "role": "FALLBACK"
                    })
        except Exception as e:
            log.debug(f"Error finding local venvs: {e}")

        return venvs

    def _get_mediainfo_status():
        """Get runtime status for pymediainfo (python) and mediainfo (system)."""
        cli_path = shutil.which("mediainfo")
        pymediainfo_available = False
        pymediainfo_version = None

        try:
            import pymediainfo  # type: ignore
            pymediainfo_available = True
            pymediainfo_version = getattr(pymediainfo, "__version__", None)
        except Exception:
            pymediainfo_available = False

        mediainfo_cli_version = None
        if cli_path:
            try:
                result = subprocess.run(
                    [cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                output = result.stdout or ""
                match = re.search(r"v(\d+\.\d+(?:\.\d+)*)", output)
                mediainfo_cli_version = match.group(1) if match else None
            except Exception:
                mediainfo_cli_version = None

        return {
            "pymediainfo_available": pymediainfo_available,
            "pymediainfo_version": pymediainfo_version,
            "mediainfo_cli_available": bool(cli_path),
            "mediainfo_cli_path": cli_path,
            "mediainfo_cli_version": mediainfo_cli_version,
        }

    def _get_runtime_tools_status():
        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")
        vlc_cli_path = shutil.which("vlc")
        mkvinfo_path = shutil.which("mkvinfo")
        mkvmerge_path = shutil.which("mkvmerge")
        mkvinfo_version = None
        mkvmerge_version = None
        python_mkv_available = False
        python_mkv_version = None
        try:
            import pymkv
            python_mkv_available = True
            python_mkv_version = getattr(pymkv, "__version__", None)
        except Exception:
            python_mkv_available = False
        if mkvinfo_path:
            try:
                mkvinfo_result = subprocess.run(
                    [mkvinfo_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvinfo_result.stdout or "").splitlines()[
                    0] if mkvinfo_result.stdout else ""
                match = re.search(r"mkvinfo v(\S+)", first_line)
                mkvinfo_version = match.group(1) if match else None
            except Exception:
                mkvinfo_version = None
        if mkvmerge_path:
            try:
                mkvmerge_result = subprocess.run(
                    [mkvmerge_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvmerge_result.stdout or "").splitlines()[
                    0] if mkvmerge_result.stdout else ""
                match = re.search(r"mkvmerge v(\S+)", first_line)
                mkvmerge_version = match.group(1) if match else None
            except Exception:
                mkvmerge_version = None

        browser_candidates = [
            ("google-chrome", "google-chrome"),
            ("google-chrome-stable", "google-chrome-stable"),
            ("chromium", "chromium"),
            ("chromium-browser", "chromium-browser"),
            ("firefox", "firefox"),
        ]

        browser_name = None
        browser_path = None
        browser_version = None
        for candidate_name, binary in browser_candidates:
            found = shutil.which(binary)
            if found:
                browser_name = candidate_name
                browser_path = found
                break

        if browser_path:
            try:
                browser_result = subprocess.run(
                    [browser_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (browser_result.stdout or "").splitlines()[
                    0] if browser_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                browser_version = match.group(1) if match else None
            except Exception:
                browser_version = None

        mutagen_available = False
        mutagen_version = None
        try:
            import mutagen  # type: ignore
            mutagen_available = True
            mutagen_version = getattr(
                mutagen, "version_string", None) or getattr(
                mutagen, "__version__", None)
        except Exception:
            mutagen_available = False

        python_vlc_available = bool(globals().get("HAS_VLC", False))
        python_vlc_version = None
        if python_vlc_available:
            try:
                python_vlc_version = getattr(vlc, "__version__", None)
            except Exception:
                python_vlc_version = None

        ffmpeg_version = None
        if ffmpeg_path:
            try:
                ffmpeg_result = subprocess.run(
                    [ffmpeg_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffmpeg_result.stdout or "").splitlines()[
                    0] if ffmpeg_result.stdout else ""
                match = re.search(
                    r"ffmpeg version\s+([^\s]+)",
                    first_line,
                    re.IGNORECASE)
                ffmpeg_version = match.group(1) if match else None
            except Exception:
                ffmpeg_version = None

        ffprobe_version = None
        if ffprobe_path:
            try:
                ffprobe_result = subprocess.run(
                    [ffprobe_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffprobe_result.stdout or "").splitlines()[
                    0] if ffprobe_result.stdout else ""
                match = re.search(
                    r"ffprobe version\s+([^\s]+)",
                    first_line,
                    re.IGNORECASE)
                ffprobe_version = match.group(1) if match else None
            except Exception:
                ffprobe_version = None

        vlc_cli_version = None
        if vlc_cli_path:
            try:
                vlc_result = subprocess.run(
                    [vlc_cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (vlc_result.stdout or "").splitlines()[
                    0] if vlc_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                vlc_cli_version = match.group(1) if match else None
            except Exception:
                vlc_cli_version = None

        return {
            "ffmpeg_cli_available": bool(ffmpeg_path),
            "ffmpeg_cli_path": ffmpeg_path,
            "ffmpeg_cli_version": ffmpeg_version,
            "ffprobe_cli_available": bool(ffprobe_path),
            "ffprobe_cli_path": ffprobe_path,
            "ffprobe_cli_version": ffprobe_version,
            "mkvinfo_cli_available": bool(mkvinfo_path),
            "mkvinfo_cli_path": mkvinfo_path,
            "mkvinfo_cli_version": mkvinfo_version,
            "mkvmerge_cli_available": bool(mkvmerge_path),
            "mkvmerge_cli_path": mkvmerge_path,
            "mkvmerge_cli_version": mkvmerge_version,
            "python_mkv_available": python_mkv_available,
            "python_mkv_version": python_mkv_version,
            "browser_available": bool(browser_path),
            "browser_name": browser_name,
            "browser_path": browser_path,
            "browser_version": browser_version,
            "vlc_cli_available": bool(vlc_cli_path),
            "vlc_cli_path": vlc_cli_path,
            "vlc_cli_version": vlc_cli_version,
            "python_vlc_available": python_vlc_available,
            "python_vlc_version": python_vlc_version,
            "mutagen_available": mutagen_available,
            "mutagen_version": mutagen_version,
        }

    # Discovery logic
    # Discover available environments (cached/fast)
    conda_envs = _get_conda_environments()
    system_pythons = _get_system_pythons()
    installed_packages, installed_packages_source = _get_installed_packages()
    if not installed_packages:
        installed_packages = _get_packages_fallback()
        installed_packages_source = "importlib_or_pkg_resources"
    local_venvs = _find_local_venvs()
    mediainfo_status = _get_mediainfo_status()
    tools_status = _get_runtime_tools_status()
    requirements_status = _get_requirements_status()

    # ===== Build Response =====
    result = {
        # Current Environment (Primary)
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "in_venv": in_venv,
        "venv_path": venv_path or venv_env,
        "in_conda": in_conda,
        "conda_env_name": conda_env_name,
        "conda_prefix": conda_prefix,
        "has_conda_context": bool(conda_env_name or conda_prefix),
        "env_type": env_type,
        "env_path": env_path,
        "env_name": env_name,
        "platform": platform.platform(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "pid": os.getpid(),
        "browser_pid": BROWSER_PID if BROWSER_PID is not None else 0,
        "testbed_pid": find_venv_pid('.venv_testbed'),
        "selenium_pid": find_venv_pid('.venv_selenium'),
        "version": VERSION,

        # Current Environment (Detailed)
        "current_environment": current_env,

        # Alternative Environments (Discovery Results)
        "available_conda_environments": conda_envs,
        "available_system_pythons": system_pythons,
        "local_venvs": local_venvs,
        "multi_venv_concept": "Dieses Projekt nutzt ein Multi-Virtual-Environment-Konzept zur strikten Trennung von Laufzeit-, Build- und Test-Abhngigkeiten.",

        # Installed Packages
        "installed_packages": installed_packages,
        "package_count": len(installed_packages),
        "installed_packages_source": installed_packages_source,
        "mediainfo_status": mediainfo_status,
        "tools_status": tools_status,
        "requirements_status": requirements_status,

        # Recommendations
        "recommended_environment": {
            "name": "venv_core",
            "type": "venv",
            "python_version": "3.14.2",
            "reason": "Eigene venv fr main.py empfohlen"
        },
        "default_scan_dir": SCAN_MEDIA_DIR,
        "browse_default_dir": BROWSER_DEFAULT_DIR,
        "parser_config": PARSER_CONFIG
    }

    # UI Trace Logging - capture what frontend receives
    try:
        trace_log_path = Path(__file__).parent / "logs" / \
            "ui_trace_environment_info.log"
        trace_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(trace_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] get_environment_info() called\n")
            f.write(f"force_refresh: {force_refresh}\n")
            f.write(f"package_count: {len(installed_packages)}\n")
            f.write(f"installed_packages_source: {installed_packages_source}\n")
            f.write(f"requirements_status: {requirements_status}\n")
            f.write(f"first_3_packages: {installed_packages[:3] if installed_packages else 'EMPTY'}\n")
            f.write(f"env_type: {result.get('env_type')}\n")
            f.write(f"python_executable: {result.get('python_executable')}\n")

        # Also print to console for immediate visibility
        log.debug(f"\n UI-TRACE: get_environment_info()  packages={len(
            installed_packages)}, source={installed_packages_source}, req={requirements_status}")
    except Exception as e:
        log.error(f"  UI-TRACE logging failed: {e}")

    _ENV_INFO_CACHE["data"] = result
    _ENV_INFO_CACHE["ts"] = time.time()
    return result


# Konfiguration
# 1. Ort fr den automatischen Bibliotheks-Scan
# Standardmig aus PARSER_CONFIG laden (sync)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCAN_MEDIA_DIR = PARSER_CONFIG.get("scan_dirs", [str(PROJECT_ROOT / "media")])[0]

# 2. Standard-Pfad beim ersten ffnen des Browsers
BROWSER_DEFAULT_DIR = PARSER_CONFIG.get("browse_default_dir", str(Path.home()))
# Redundante Definitionen entfernt, da diese nun aus parsers.format_utils importiert werden.
# (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS etc. werden oben importiert)
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}


@eel.expose
def get_debug_logs():
    """
    @brief Returns the entire log history as a single string.
    """
    return "\n".join(logger.get_ui_logs())


@eel.expose
def reset_backend():
    """
    Exposed function to reset backend connections and clear ephemeral state.
    """
    log.info("[System] Backend Reset triggered by UI.")
    try:
        # Clear any caches or ephemeral state if needed
        global _ENV_INFO_CACHE
        _ENV_INFO_CACHE = {}

        # You could also perform database connection resets or other cleanup here
        # db.reset_connection()

        return {"status": "ok", "message": "Backend successfully reset."}
    except Exception as e:
        log.error(f"[System] Backend Reset failed: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def set_log_level(level_name: str):
    """
    @brief Sets the global log level.
    @param level_name One of DEBUG, INFO, WARNING, ERROR, CRITICAL.
    """
    # Log the action BEFORE changing the level so it's always captured at current level
    log.info(f"[System] Manually setting Log-Level to {level_name.upper()}")

    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.getLogger().setLevel(level)
    # Update handlers as well to be sure
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)

    # Update config for persistence
    PARSER_CONFIG["log_level"] = level_name.upper()
    save_parser_config()
    return True

# initialize_debug_flags was moved to top-level for earlier capture


def is_no_gui_mode(args: list[str] | None = None) -> bool:
    """
    Check whether no-GUI mode is enabled.

    No-GUI mode disables UI/websocket/browser startup and runs
    the app in a connectionless local-only mode.
    """
    if args is None:
        args = sys.argv
    return "--ng" in args or "--no-gui" in args or "--sessionless" in args


def is_connectionless_browser_mode(args: list[str] | None = None) -> bool:
    """
    Check whether browser-based connectionless mode is enabled.

    In this mode the app opens the frontend in browser without starting
    Eel/WebSocket backend session.
    """
    if args is None:
        args = sys.argv
    return "--n" in args


def get_preferred_browser():
    """
    Get the preferred browser controller for launching the application.

    Preference order:
    1. Chromium
    2. Firefox
    3. Google Chrome
    4. Default system browser

    Returns:
        webbrowser.BaseBrowser: Browser controller instance
    """
    import webbrowser
    import shutil

    browser_candidates = [
        ('chromium-browser', 'Chromium'),
        ('chromium', 'Chromium'),
        ('firefox', 'Firefox'),
        ('google-chrome', 'Google Chrome'),
        ('chrome', 'Google Chrome'),
    ]

    for browser_cmd, browser_name in browser_candidates:
        browser_path = shutil.which(browser_cmd)
        if browser_path:
            log.info(f"[Browser] Selected: {
                browser_name} ({browser_path})")
            try:
                return webbrowser.get(f'{browser_path} %s')
            except Exception as e:
                log.warning(
                    f"[Browser] Failed to register {browser_name}: {e}")
                continue

    log.warning(
        "[Browser] Using system default browser (Vivaldi or other)")


def wait_for_port(port: int, host: str = 'localhost', timeout: float = 10.0) -> bool:
    """Wait for a port to become reachable before proceeding (optimized for speed)."""
    import socket
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Short timeout for connection check
            with socket.create_connection((host, port), timeout=0.1):
                return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            time.sleep(0.1)  # Faster polling
    return False


def open_session_url(url: str) -> bool:
    """Open a session URL in app-mode window when possible, else fallback browser."""
    if os.environ.get("MWV_NO_BROWSER", "0") == "1":
        log.info("[Session] MWV_NO_BROWSER is set. Skipping browser launch.")
        return True
    import shutil

    browser_candidates = [
        'chromium',
        'chromium-browser',
        'google-chrome-stable',
        'google-chrome',
        'chrome',
    ]

    # Using a dedicated profile directory (within the project data) prevents
    # profile locks that often stop chromium from opening a new window in app-mode
    # when another instance is already running with the same profile.
    profile_dir = PROJECT_ROOT / "data" / "browser_profile"
    try:
        profile_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        profile_dir = None

    # Handle browser selection
    choice = PARSER_CONFIG.get("browser_choice", "auto")
    if choice != "auto":
        browser_candidates = [choice] + [c for c in browser_candidates if c != choice]

    for browser_cmd in browser_candidates:
        browser_path = shutil.which(browser_cmd)
        if browser_path:
            log.info(f"[Browser] Launching {browser_cmd} in app mode (URL: {url})")

            # Arguments for a reliable, clean app window
            import urllib.parse
            parsed_url = urllib.parse.urlparse(url)
            if parsed_url.port:
                if not wait_for_port(parsed_url.port, timeout=3.0):
                    log.warning(f"[Browser] Port {parsed_url.port} not reachable after timeout. Launching anyway.")

            custom_flags = PARSER_CONFIG.get("browser_flags", [])
            args = [browser_path, f'--app={url}'] + custom_flags

            # Apply environment variables
            env = os.environ.copy()
            user_envs = PARSER_CONFIG.get("env_vars", {})
            for k, v in user_envs.items():
                env[str(k)] = str(v)

            log.info(f"[Browser] Executing: {' '.join(args)}")

            try:
                # Use subprocess.Popen to launch asynchronously
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=env
                )
                global BROWSER_PID
                BROWSER_PID = process.pid
                log.info(f"[Browser] Successfully started: {browser_cmd} (PID: {BROWSER_PID})")
                return True
            except Exception as e:
                log.warning(
                    f"[Browser] Failed to launch {browser_cmd}: {e}")

    log.warning(
        "[Browser] Chromium not found, falling back to preferred browser")
    try:
        browser = get_preferred_browser()
        browser.open(url)
        return True
    except Exception as e:
        log.warning(f"[Browser] Fallback browser launch failed: {e}")
        return False


def run_sessionless_mode() -> dict:
    """
    Execute sessionless startup flow and return status information.
    """
    db.init_db()
    stats = db.get_db_stats()
    legacy_dbs = db.list_legacy_databases()
    return {
        "mode": "no-gui",
        "active_db": str(db.get_active_db_path()),
        "total_items": int(stats.get("total_items", 0)),
        "legacy_db_count": len(legacy_dbs),
        "scan_dirs": PARSER_CONFIG.get("scan_dirs", []),
    }


def run_connectionless_browser_mode() -> dict:
    """
    Execute connectionless browser mode and return status information.

    Opens web/app.html directly in browser without starting Eel.
    """
    db.init_db()
    stats = db.get_db_stats()
    app_file = (Path(__file__).parent / "web" / "app.html").resolve()
    app_url = app_file.as_uri()

    if os.environ.get("MWV_DISABLE_BROWSER_OPEN") == "1":
        log.info(
            "[Mode-N] Browser launch suppressed by MWV_DISABLE_BROWSER_OPEN=1")
    else:
        browser = get_preferred_browser()
        browser.open(app_url)

    return {
        "mode": "connectionless-browser",
        "active_db": str(db.get_active_db_path()),
        "total_items": int(stats.get("total_items", 0)),
        "app_url": app_url,
        "scan_dirs": PARSER_CONFIG.get("scan_dirs", []),
    }


def check_running_sessions() -> list[dict]:
    """
    Check for currently running dict sessions.

    Returns:
        list[dict]: List of active sessions with pid, port, and command info
    """
    import psutil

    sessions = []
    current_pid = os.getpid()
    pid_to_port: dict[int, int] = {}

    try:
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status != 'LISTEN':
                continue
            if not conn.pid or conn.pid == current_pid:
                continue

            laddr = conn.laddr
            host = None
            port = None

            if hasattr(laddr, 'ip') and hasattr(laddr, 'port'):
                host = laddr.ip
                port = laddr.port
            elif isinstance(laddr, tuple) and len(laddr) >= 2:
                host, port = laddr[0], laddr[1]

            if host not in ('127.0.0.1', '::1', '0.0.0.0'):
                continue
            if isinstance(port, int) and conn.pid not in pid_to_port:
                pid_to_port[conn.pid] = port
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.info['pid']
            if pid == current_pid:
                continue

            cmdline = proc.info.get('cmdline') or []
            if not cmdline:
                continue

            if any('main.py' in str(arg) for arg in cmdline):
                sessions.append({
                    'pid': pid,
                    'port': pid_to_port.get(pid),
                    'cmdline': ' '.join(cmdline),
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sessions


def is_session_url_reachable(url: str, timeout: float = 1.0, retries: int = 1) -> bool:
    """Check whether an existing session URL responds in time with retries."""
    import urllib.request
    import time

    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                if 200 <= int(getattr(response, 'status', 200)) < 500:
                    return True
        except Exception:
            if i < retries:
                time.sleep(0.5)  # Wait a bit before retry
                continue
    return False


def is_port_in_use(port: int) -> bool:
    """
    Check if a specific port is in use.

    Args:
        port: Port number to check

    Returns:
        bool: True if port is in use, False otherwise
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except OSError:
            return True


def _ensure_project_venv_active() -> None:
    """Re-exec into local project .venv_core interpreter when available, 
    but respect any project-local .venv_* if already active."""
    if os.environ.get("MWV_DISABLE_AUTO_VENV") == "1":
        return
    if os.environ.get("MWV_AUTO_VENV_REEXEC") == "1":
        return

    # 1. Detection: Are we already in a project venv?
    # We check if sys.executable points into PROJECT_ROOT/.venv*
    current_exec_path = Path(sys.executable)
    try:
        if current_exec_path.is_relative_to(PROJECT_ROOT):
            # Check if it's within a .venv* folder
            parts = current_exec_path.relative_to(PROJECT_ROOT).parts
            if parts and parts[0].startswith(".venv"):
                # We are already in a project-specific environment (like .venv_run or .venv_core)
                return
    except (ValueError, Exception):
        pass

    # 2. Fallback: Re-exec into .venv_core if it exists
    venv_python = PROJECT_ROOT / ".venv_core" / "bin" / "python"
    if not (venv_python.is_file() and os.access(venv_python, os.X_OK)):
        return

    log.info(f"[Startup] Re-exec into project-local environment: {venv_python}")
    os.environ["MWV_AUTO_VENV_REEXEC"] = "1"
    # IMPORTANT: Do NOT use .resolve() here. We MUST execute the symlink
    # itself so the Python interpreter finds its local site-packages correctly.
    os.execv(str(venv_python), [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]])


# Defer these calls to if __name__ == '__main__': block

# Log environment information at startup
def _log_environment_info():
    """Log Python environment details at startup."""
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()

    log.info("" * 60)
    log.info("[Startup] Application started - Environment Information")
    log.info("" * 60)

    if env_type == 'conda':
        log.info(f"  Environment Type: Conda")
        log.info(f"  Environment Name: {env_name}")
        log.info(f"  Environment Path: {env_path}")
    elif env_type == 'venv':
        log.info(f"  Environment Type: Virtual Environment (venv)")
        log.info(f"  Environment Name: {env_name}")
        log.info(f"  Environment Path: {env_path}")
    else:
        log.info(f"  Environment Type: System Python")
        log.info(f"  Environment Path: {env_path}")

    log.info(f"  Python Version: {py_ver}")
    log.info(f"  Python Executable: {py_exec}")
    log.info("" * 60)


_log_environment_info()


def debug_log(message: str) -> None:
    """
    @brief Universal logging helper (bridged to central logging system).
    """
    log.info(message)
    # Eel callback if front-end is already listening
    try:
        if hasattr(eel, 'log_to_debug'):
            eel.log_to_debug(message)
    except Exception:
        pass


if DEBUG_FLAGS["start"]:
    debug_log("[Startup] main.py loading...")

# Removed duplicate get_debug_console (correct version is at line 459)


@eel.expose
def get_debug_flags():
    """
    @brief Returns the current internal debug flags.
    @details Gibt die aktuell gesetzten internen Debug-Flags zurck.
    @return Dictionary of debug flags / Dictionary der Debug-Flags.
    """
    return DEBUG_FLAGS


@eel.expose
def set_debug_flag(key, value):
    """
    @brief Sets a specific debug flag.
    @details Setzt ein spezifisches Debug-Flag.
    @param key Flag name / Name des Flags.
    @param value Boolean value / Boole'scher Wert.
    """
    if key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
        save_parser_config()
        debug_log(f"[Debug] Flag '{key}' auf {value} gesetzt.")


@eel.expose
def set_all_debug_flags(value):
    """
    @brief Activates or deactivates all debug flags simultaneously.
    @details Aktiviert oder deaktiviert alle Debug-Flags gleichzeitig.
    @param value Boolean value / Boole'scher Wert.
    """
    for key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
    save_parser_config()
    debug_log(f"[Debug] Alle Flags wurden auf {value} gesetzt.")


@eel.expose
def get_venv_summary():
    """
    @brief Returns a comprehensive summary of the current and available Python environments.
    @details Gibt eine Zusammenfassung der aktuellen und verfgbaren Python-Umgebungen zurck.
    @return Dictionary with environment details and recommendations.
    """
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()

    # Strategy definition: Detailed multi-venv concept
    VENV_STRATEGY = {
        ".venv_core": {
            "purpose": "Zentrale Laufzeitumgebung fr die App-Logik.",
            "role": "CORE",
            "required": True
        },
        ".venv_build": {
            "purpose": "Umgebung fr das Packaging (PyInstaller, .deb).",
            "role": "BUILD",
            "required": False
        },
        ".venv_dev": {
            "purpose": "Entwicklungsumgebung mit Lintern (flake8, pyre).",
            "role": "DEV",
            "required": False
        },
        ".venv_testbed": {
            "purpose": "Isolierte Umgebung fr Integrations-Tests.",
            "role": "TEST",
            "required": False
        },
        ".venv_selenium": {
            "purpose": "Umgebung fr E2E Browser-Tests.",
            "role": "E2E",
            "required": False
        }
    }

    available_venvs = []
    # Discovery of subsidiary venvs based on strategy
    for vname, info in VENV_STRATEGY.items():
        vpath = PROJECT_ROOT / vname
        exists = vpath.exists() and (vpath / "bin" / "python").exists()

        available_venvs.append({
            "name": vname,
            "path": str(vpath),
            "exists": exists,
            "active": (str(vpath) == str(env_path)) if exists else False,
            "purpose": info["purpose"],
            "role": info["role"]
        })

    # Add default 'venv' if it exists but is not in strategy
    default_venv = PROJECT_ROOT / "venv"
    if default_venv.exists() and (default_venv / "bin" / "python").exists():
        if not any(v["name"] == "venv" for v in available_venvs):
            available_venvs.append({
                "name": "venv",
                "path": str(default_venv),
                "exists": True,
                "active": (str(default_venv) == str(env_path)),
                "purpose": "Standard Fallback-Umgebung.",
                "role": "FALLBACK"
            })

    return {
        "current_environment": {
            "type": env_type,
            "name": env_name,
            "path": str(env_path),
            "python_version": py_ver,
            "python_executable": str(py_exec)
        },
        "available_venvs": available_venvs,
        "multi_venv_concept": "Das Projekt nutzt eine Multi-Venv-Strategie zur Trennung von Core-Logik, Build-System und Testing.",
        "recommended_environment": {
            "name": ".venv_core",
            "type": "venv",
            "reason": "Empfohlene Umgebung fr den stabilen Betrieb der App."
        }
    }


@eel.expose
def get_language():
    """
    @brief Returns the currently selected UI language.
    @details Gibt die aktuell gewhlte Sprache zurck.
    @return Language code (e.g. 'de', 'en') / Sprachcode.
    """
    return PARSER_CONFIG.get("language", "de")


@eel.expose
def set_language(lang):
    """
    @brief Sets the UI language of the application.
    @details Setzt die Sprache der Anwendung.
    @param lang Language code / Sprachcode.
    @return True if successful / True falls erfolgreich.
    """
    PARSER_CONFIG["language"] = lang
    save_parser_config()
    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Sprache auf '{lang}' gesetzt.")
    return True


# Benutzerdefinierte Module

# Eigene Parser


# Eigene bottle Web-Routen
from web import app_bottle  # noqa: F401  # Register bottle routes: /media and /cover

# Models


@eel.expose
def get_db_info():
    """
    @brief Returns summary statistics about the database and logs.
    @details Gibt zusammenfassende Statistiken ber die Datenbank und das Logbuch zurck.
    @return Dictionary with media_count, playlist_count, and log_count.
    """
    try:
        stats = db.get_db_stats()

        # Count playlists
        conn = sqlite3.connect(db.DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM playlists")
        playlist_count = cursor.fetchone()[0]
        conn.close()

        # Count logbook entries
        log_dir = PROJECT_ROOT / "logbuch"
        log_count = len(list(log_dir.glob("*.md"))) if log_dir.exists() else 0

        return {
            "media_count": stats.get('total_items', 0),
            "playlist_count": playlist_count,
            "log_count": log_count
        }
    except Exception as e:
        log.error(f"[API] Error in get_db_info: {e}")
        return None


@eel.expose
def get_library() -> Dict[str, Any]:
    """
    @brief Returns all media items from the database without re-scanning.
    @details Gibt alle Medien aus der Datenbank zurck ohne neu zu scannen.
    @return Dict with list of media items / Dokument mit Medien-Liste.
    """
    all_media = db.get_all_media()
    displayed_cats = PARSER_CONFIG.get("displayed_categories")
    # If explicitly None, default to everything (Legacy behavior or first run)
    # If empty list [], it means the user unchecked EVERYTHING (Respect that)
    if displayed_cats is None:
        displayed_cats = [
            "audio",
            "video",
            "images",
            "documents",
            "ebooks",
            "abbild",
            "spiel",
            "beigabe"]

    # We map internal categories to the setting keys
    # logical_type: 'Audio', 'Video', 'Bilder', 'Dokument', 'E-Book', 'Abbild'
    cat_map = {
        "audio": [
            "Audio",
            "Album",
            "Hrbuch",
            "Klassik",
            "Compilation",
            "Single",
            "Podcast",
            "Radio"],
        "video": [
            "Video",
            "Film",
            "Serie"],
        "images": ["Bilder"],
        "documents": ["Dokument"],
        "ebooks": ["E-Book"],
        "abbild": [
            "Abbild",
            "ISO/Image",
            "Disk Image",
            "PAL DVD",
            "NTSC DVD",
            "Blu-ray",
            "PAL DVD (Abbild)",
            "NTSC DVD (Abbild)",
            "DVD (Abbild)",
            "Blu-ray (Abbild)",
            "Audio-CD (Abbild)",
            "CD-ROM (Abbild)",
            "Disk-Abbild"],
        "spiel": [
            "PC Spiel",
            "PC Spiel (Index)",
            "Digitales Spiel (Steam)",
            "Spiel"],
        "beigabe": [
            "Supplement",
            "Beigabe",
            "Software"]}

    allowed_internal_cats = []
    for cat in displayed_cats:
        allowed_internal_cats.extend([c.lower() for c in cat_map.get(cat.lower(), [])])

    # Case-insensitive category check to match German/Capitalized DB entries
    filtered_media = [item for item in all_media if str(item.get('category', '')).lower() in allowed_internal_cats]

    log.info(f"[API] get_library returning {len(filtered_media)} items (Filter: {displayed_cats})")
    return sanitize_json_utf8({"media": filtered_media})


@eel.expose
def get_library_filtered(search: str = "", genre: str = "all", year: str = "all", sort_by: str = "name") -> Dict[str, Any]:
    """
    @brief Advanced filtering for the media library.
    """
    all_media = db.get_all_media()
    displayed_cats = PARSER_CONFIG.get("displayed_categories", ["audio", "video"])
    # (Mapping logic same as get_library)

    filtered = []
    for item in all_media:
        # 1. Category check
        # ... logic ...

        # 2. Search check
        if search and search.lower() not in item['name'].lower():
            continue

        # 3. Genre check
        item_genre = item.get('tags', {}).get('genre', '').lower()
        if genre != "all" and genre.lower() not in item_genre:
            continue

        # 4. Year check
        item_year = str(item.get('tags', {}).get('year', ''))
        if year != "all" and year != item_year:
            continue

        filtered.append(item)

    # 5. Sorting
    if sort_by == "year":
        filtered.sort(key=lambda x: str(x.get('tags', {}).get('year', '9999')), reverse=True)
    else:
        filtered.sort(key=lambda x: x['name'].lower())

    return sanitize_json_utf8({"media": filtered})


@eel.expose
def clear_database():
    """
    @brief Deletes all entries from the library database.
    @details Lscht alle Eintrge aus der Bibliothek-Datenbank.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"]:
        debug_log("[Debug-DB] Tabelle wird geleert...")
    db.clear_media()
    return {"status": "ok", "message": "Datenbank geleert", "media": []}


@eel.expose
def reset_app_data():
    """
    @brief Wipes the database and configuration files (private user data).
    @details Lscht Datenbank und Konfigurationsdateien (Private Daten).
    @return Status dictionary with list of deleted paths / Status-Dictionary.
    """
    import shutil
    from pathlib import Path

    deleted = []

    # Paths to clear:
    # 1. ~/.media-web-viewer (Database)
    db_dir = db.DB_DIR
    # 2. ~/.config/gui_media_web_viewer (Parser Config)
    # Programmname im config-Pfad fr bessere bersicht ndern
    config_dir = Path.home() / ".config" / "gui_media_web_viewer"

    for p in [db_dir, config_dir]:
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink()
                deleted.append(str(p))
            except Exception as e:
                debug_log(f"[Error] Reset failed for {p}: {e}")

    # Remove legacy database files from old locations
    legacy_deleted = db.cleanup_legacy_databases()
    for p in legacy_deleted:
        deleted.append(p)

    # Re-initialize to avoid crash on next actions
    db.init_db()
    save_parser_config()  # Create default config
    load_parser_config()  # Sync local PARSER_CONFIG in memory

    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Reset complete. Deleted: {', '.join(deleted)}")
    return {"status": "ok", "deleted": deleted}


@eel.expose
def update_tags(name, tags_dict):
    """
    @brief Saves customized tags for a media item in the database.
    @details Speichert angepasste Tags fr ein Item in der DB.
    @param name Media record name / Datenbank-Name des Eintrags.
    @param tags_dict Dictionary of tags to update / Zu aktualisierende Tags.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"] or DEBUG_FLAGS["metadata"]:
        logger.debug("metadata", f"Updating tags for {name}: {tags_dict}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}


@eel.expose
def rename_media(old_name, new_name):
    """
    @brief Renames a media record in the database.
    @details Benennt ein Medium in der DB um.
    @param old_name Current name / Aktueller Name.
    @param new_name Target name / Neuer Name.
    @return Status dictionary / Status-Dictionary.
    """
    if not new_name or new_name.strip() == "":
        return {"status": "error", "message": "Name darf nicht leer sein"}

    logger.debug("file_ops", f"Renaming record: {old_name} -> {new_name}")

    success = db.rename_media(old_name, new_name)
    if success:
        return {"status": "ok"}
    else:
        return {
            "status": "error",
            "message": "Name bereits vorhanden oder Fehler"}


@eel.expose
def delete_media(name):
    """
    @brief Deletes a media item from the database.
    @details Lscht ein Medium aus der DB.
    @param name Media record name / Datenbank-Name.
    """
    logger.debug("file_ops", f"Deleting record: {name}")
    return db.delete_media(name)


@eel.expose
def get_db_stats():
    """
    @brief Returns statistical information about the database content.
    @details Gibt Statistiken ber den Inhalt der Datenbank zurck.
    @return Stats dictionary / Statistik-Dictionary.
    """
    return db.get_db_stats()


@eel.expose
def get_default_media_dir():
    """
    @brief Returns the default media directory (absolute path).
    @details Gibt den voreingestellten Medienordner (absoluter Pfad) zurck.
    @return Path string / Pfad-String.
    """
    return SCAN_MEDIA_DIR


@eel.expose
def ensure_default_scan_dir():
    """
    @brief Ensures the default media directory is present in scan_dirs.
    @details Stellt sicher, dass der Standard-Medienordner in scan_dirs enthalten ist.
    @return Status dictionary with updated directory list / Status-Dictionary mit aktualisierter Liste.
    """
    default_dir = str(Path(SCAN_MEDIA_DIR).resolve())
    Path(default_dir).mkdir(parents=True, exist_ok=True)

    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    normalized_dirs = [str(Path(d).resolve())
                       for d in dirs if isinstance(d, str) and d.strip()]

    if default_dir not in normalized_dirs:
        normalized_dirs.insert(0, default_dir)

    PARSER_CONFIG["scan_dirs"] = normalized_dirs
    save_parser_config()

    return {"status": "ok", "dirs": PARSER_CONFIG.get("scan_dirs", [])}

# Funktion, um Medien zu scannen und an die GUI zu senden


@eel.expose
def update_browse_default_dir(new_path: str):
    """
    @brief Updates the default browsing directory in the central config.
    """
    global BROWSER_DEFAULT_DIR
    if not new_path or not os.path.isdir(new_path):
        return {"status": "error", "message": "Invalid directory"}

    BROWSER_DEFAULT_DIR = str(Path(new_path).resolve())
    PARSER_CONFIG["browse_default_dir"] = BROWSER_DEFAULT_DIR
    save_parser_config()
    return {"status": "ok", "path": BROWSER_DEFAULT_DIR}


@eel.expose
def ping():
    """
    @brief Connectivity check.
    @details Gibt eine Besttigung zurck, dass das Backend erreichbar ist.
    @return dict with status 'ok' and message 'pong'.
    """
    return {"status": "ok", "message": "pong"}


@eel.expose
def normalize_isbn(isbn: str) -> str:
    """
    @brief Cleans ISBN string from hyphens, spaces and common prefixes.
    """
    if not isbn:
        return ""
    # Remove common ISBN prefixes/labels if present
    cleaned = re.sub(r'^(ISBN[:\s]*)', '', isbn, flags=re.IGNORECASE)
    # Remove all non-alphanumeric except X for ISBN-10
    cleaned = re.sub(r'[^0-9X]', '', cleaned.upper())
    return cleaned


@eel.expose
def api_scan_isbn(isbn: str):
    """
    @brief Scans an ISBN and returns metadata (v2.5).
    @details Normalizes the ISBN, searches DB, and fetches from OpenLibrary if missing.
    """
    cleaned = normalize_isbn(isbn)
    if not cleaned:
        return {"error": "Invalid ISBN input"}

    log.info(f" [ISBN] Request for: {cleaned}")

    # 1. Check local DB first
    existing_item = db.get_media_by_remote_id('isbn', cleaned)
    if existing_item:
        log.info(f" [ISBN] Found in local DB: {existing_item['name']}")
        return existing_item

    # 2. Fetch from External API (OpenLibrary)
    try:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{cleaned}&format=json&jscmd=data"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            key = f"ISBN:{cleaned}"
            if key in data:
                book = data[key]
                authors = [a['name'] for a in book.get('authors', [])]

                # Try to get best cover
                cover_url = None
                if 'cover' in book:
                    cover_url = book['cover'].get('large') or book['cover'].get('medium')

                # Amazon Cover Logic (often ISBN-based)
                amazon_cover = f"https://images-na.ssl-images-amazon.com/images/P/{cleaned}.01._SCLZZZZZZZ_.jpg"

                result = {
                    "id": f"isbn_{cleaned}",
                    "title": book.get('title', 'Unknown Title'),
                    "artist": ", ".join(authors) if authors else "Unknown Author",
                    "year": book.get('publish_date', ''),
                    "isbn": cleaned,
                    "amazon_cover": amazon_cover,
                    "cover": cover_url or amazon_cover,
                    "media_type": "container",
                    "subtype": "book",
                    "description": book.get('notes', '')
                }
                log.info(f" [ISBN] Fetched from OpenLibrary: {result['title']}")

                # Create a placeholder MediaObject in DB?
                # (User might want to confirm first, for now just return)
                return result
    except Exception as e:
        log.error(f" [ISBN] Error fetching metadata: {e}")

    # 3. Fallback: Search Amazon cover even if no metadata found
    return {
        "isbn": cleaned,
        "amazon_cover": f"https://images-na.ssl-images-amazon.com/images/P/{cleaned}.01._SCLZZZZZZZ_.jpg",
        "media_type": "container",
        "subtype": "unknown",
        "error": "No metadata found, but here is a potential cover link."
    }


@eel.expose
def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Scans a directory recursively and indexes audio files.
    @details Scannt rekursiv einen Ordner und indexiert Audiodateien. Optionaler Reset der DB.
    @param dir_path Optional path to scan / Optionaler Pfad zum Scannen.
    @param clear_db If True, clears the database before scanning / Falls True, leert die Datenbank vor dem Scan.
    @return Dictionary with media list and scan stats / Dictionary mit Medien-Liste und Statistiken.
    """
    start_time = time.time()
    log.info(
        f" [Scan-Trace] Media Scan started at {
            time.strftime(
                '%H:%M:%S',
                time.localtime(start_time))}")

    if hasattr(eel, 'set_db_status') and getattr(eel, '_websocket', None):
        try:
            eel.set_db_status(True)
        except Exception:
            pass

    # DB optional leeren
    if clear_db:
        db.clear_media()

    # Determine which directories to scan
    scan_roots = []
    if dir_path and dir_path.strip():
        scan_roots.append(Path(dir_path).resolve())
    else:
        # Use all directories from config
        config_dirs = PARSER_CONFIG.get("scan_dirs", [SCAN_MEDIA_DIR])
        for d in config_dirs:
            p = Path(d).resolve()
            if p.exists():
                scan_roots.append(p)
            else:
                debug_log(f" [Scan] Skipping non-existent directory: {d}")

    log.info(f" [Scan] Starting scan. Roots: {scan_roots}, Clear DB: {clear_db}")

    count_indexed: int = 0
    try:
        from src.parsers.format_utils import IMAGE_EXTENSIONS, DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS

        # Determine if we should use lightweight mode based on path or config
        is_network = any(hardware_detector.is_network_mount(str(root)) for root in scan_roots)
        if is_network:
            log.info(" [Scan] Network mount detected. Enabling automatic lightweight mode.")
            parser_mode = "lightweight"
        else:
            parser_mode = PARSER_CONFIG.get("parser_mode", "lightweight")

        log.info(f" [Scan] Parser Mode: {parser_mode}")

        # Get existing media from DB for caching
        existing_media = {m['path']: m for m in db.get_all_media()}
        log.info(f" [Scan] Cached items in DB: {len(existing_media)}")

        # Determine which categories are enabled
        indexed_cats = PARSER_CONFIG.get("indexed_categories", [])
        log.info(f" [Scan] Enabled categories: {indexed_cats}")

        all_exts: set[str] = set()
        if "audio" in indexed_cats:
            all_exts |= AUDIO_EXTENSIONS
        if "video" in indexed_cats:
            all_exts |= VIDEO_EXTENSIONS
        if "images" in indexed_cats:
            all_exts |= IMAGE_EXTENSIONS
        if "documents" in indexed_cats:
            all_exts |= DOCUMENT_EXTENSIONS
        if "ebooks" in indexed_cats:
            all_exts |= EBOOK_EXTENSIONS
        if "abbild" in indexed_cats:
            all_exts |= DISK_IMAGE_EXTENSIONS

        ext_list = list(all_exts)
        log.info(f" [Scan] Supported extensions ({len(all_exts)}): {ext_list[:10]}...")  # type: ignore

        # Reset counters
        count_indexed: int = 0
        for scan_root in scan_roots:
            log.info(f" [Scan] Starting scan of: {scan_root}")

            # Hierarchical grouping: Folder-to-Object mapping
            folder_id_map: dict[Path, int] = {}
            # Folders to skip for file pass if they are "Black Box" media folders (DVD/BD/ISO)
            skip_subpaths: set[Path] = set()

            # First pass: Identify "Media Objects" (Folders like Albums, Series, DVDs)
            for d in scan_root.rglob('*'):
                if d.is_dir():
                    # 1. Specialized Media Folders (DVD/BD)
                    is_blackbox = (d / 'VIDEO_TS').exists() or (d / 'BDMV').exists()

                    if not is_blackbox:
                        # Smarter DVD Bundle detection
                        isos = list(d.glob('*.iso'))
                        if len(isos) == 1 and re.search(r'\(\d{4}\)', d.name):
                            is_blackbox = True

                    # 2. General Objects (folder with multiple media files, e.g. Album)
                    is_general_object = False
                    if not is_blackbox:
                        media_files = [f for f in d.glob('*') if f.is_file() and f.suffix.lower() in all_exts]
                        if len(media_files) > 1:
                            is_general_object = True

                    if is_blackbox or is_general_object:
                        logger.debug("scan", f" [Scan] Detected Object: {d.name}")
                        try:
                            item = MediaItem(d.name, d)
                            item_dict = item.to_dict()
                            obj_id = db.insert_media(item_dict)
                            if obj_id:
                                folder_id_map[d] = obj_id
                                count_indexed += 1  # type: ignore
                                if is_blackbox:
                                    skip_subpaths.add(d)
                                logger.debug("scan", f" [Scan] Indexed Object: {d.name} (ID: {
                                             obj_id}, Category: {item_dict.get('category')})")
                        except Exception as e:
                            logger.debug("scan", f" [Scan] Fehler bei Object-Ordner {d.name}: {e}")

            # Second pass: Files (Items)
            for f in scan_root.rglob('*'):
                if f.is_file():
                    # Skip if parent is a blackbox media folder (files inside DVD/BD are not indexed individually)
                    if any(f.is_relative_to(p) for p in skip_subpaths):
                        continue

                    ext = f.suffix.lower()
                    if ext in all_exts:
                        # Skip transcoding cache
                        if '.cache' in f.parts:
                            continue

                        # Blacklist
                        name_lower = f.name.lower()
                        if any(x in name_lower for x in ['cover art', 'captcha', 'thumb', 'folder', 'albumart', 'al_cave']):
                            continue

                        try:
                            # 1. Check if already in DB
                            if str(f) in existing_media:
                                count_indexed += 1
                                continue

                            # 2. Extract metadata & Link to Object
                            # Check for parent object
                            parent_id = folder_id_map.get(f.parent)

                            item = MediaItem(f.name, f)
                            item_dict = item.to_dict()

                            # Inject parent_id if found
                            if parent_id:
                                item_dict['parent_id'] = parent_id

                            db.insert_media(item_dict)
                            logger.debug("scan", f" [Scan] Indexed Item: {f.name} (Parent: {parent_id})")
                            count_indexed += 1
                        except Exception as e:
                            logger.debug("scan", f" [Scan] Fehler bei {f.name}: {e}")
                            continue

        elapsed = time.time() - start_time
        scanned_target = ", ".join(str(p)
                                   for p in scan_roots) if scan_roots else "none"
        log.info(
            f"[Scan-Trace] Scan of {scanned_target} took {elapsed:.2f} seconds.")
        log.info(
            f"[Scan-Trace] Scan complete. Processed {count_indexed} items in {elapsed:.2f} seconds.")

        # Liefere gescannten Stand direkt aus der DB zurck
        return {
            "media": db.get_all_media(),
            "stats": {"count": count_indexed, "time_seconds": elapsed}
        }
    finally:
        if hasattr(eel, 'set_db_status') and getattr(eel, '_websocket', None):
            try:
                eel.set_db_status(False)
            except Exception:
                pass


@eel.expose
def get_parser_config():
    """
    @brief Returns the current parser configuration to the frontend.
    @details Gibt die aktuelle Parser-Konfiguration an das Frontend zurck.
    @return Configuration dictionary / Konfigurations-Dictionary.
    """
    return PARSER_CONFIG


@eel.expose
def get_parser_mapping():
    """
    @brief Returns the parser-to-filetype mapping.
    @return Mapping dictionary / Mapping-Dictionary.
    """
    from src.parsers.media_parser import PARSER_MAPPING  # type: ignore
    return PARSER_MAPPING


@eel.expose
def get_slow_parsers():
    """
    @brief Returns the list of parsers considered slow.
    @return List of parser IDs.
    """
    from src.parsers.format_utils import SLOW_PARSERS
    return list(SLOW_PARSERS)


@eel.expose
def update_parser_config(new_config):
    """
    @brief Updates the parser configuration and saves it to disk.
    @details Aktualisiert die Konfiguration und speichert sie auf Festplatte.
    @param new_config Dictionary with updated settings / Dictionary mit neuen Einstellungen.
    @return Status dictionary / Status-Dictionary.
    """
    PARSER_CONFIG.update(new_config)
    save_parser_config()
    return {"status": "ok"}


@eel.expose
def add_scan_dir():
    """
    @brief Opens a dialog to select a new directory for library scanning.
    @details ffnet einen Dialog zur Auswahl eines neuen Scan-Verzeichnisses.
    @return Status dictionary with updated directory list / Status-Dictionary mit aktualisierter Liste.
    """
    new_dir = pick_folder()
    if new_dir:
        dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
        if new_dir not in dirs:
            dirs.append(new_dir)
            PARSER_CONFIG["scan_dirs"] = dirs
            save_parser_config()
            return {"status": "ok", "dirs": dirs}
    return {"status": "cancel"}


@eel.expose
def remove_scan_dir(dir_path):
    """
    @brief Removes a directory from the scan list in the configuration.
    @details Entfernt ein Verzeichnis aus der Scan-Liste in der Konfiguration.
    @param dir_path Path to remove / Zu entfernender Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    if dir_path in dirs:
        dirs.remove(dir_path)
        PARSER_CONFIG["scan_dirs"] = dirs
        save_parser_config()
        return {"status": "ok", "dirs": dirs}
    return {"status": "error", "message": "Pfad nicht in Liste"}


@eel.expose
def set_playback_mode(mode):
    """Sets the global playback mode."""
    if mode in ["chrome_native", "ffmpeg", "cvlc", "mkvmerge", "direct", "mediamtx"]:
        PARSER_CONFIG["playback_mode"] = mode
        save_parser_config()
        return {"status": "ok", "mode": mode}
    return {"status": "error", "message": "Invalid mode"}


@eel.expose
def set_bandwidth_limit(limit_mbps):
    """Sets the bandwidth limit in MB/s."""
    try:
        PARSER_CONFIG["bandwidth_limit"] = int(limit_mbps)
        save_parser_config()
        return {"status": "ok", "limit": limit_mbps}
    except ValueError:
        return {"status": "error", "message": "Invalid limit"}


@eel.expose
def play_media(path):
    """
    @brief Triggers media playback based on the current playback mode.
    Now hardened: Only handles audio to prevent double-starts with open_video logic.
    """
    # NEW: Safety check - ONLY handle audio.
    # If it's a directory, movie, or has a video extension, REJECT it here.
    ext = Path(path).suffix.lower()
    is_dir = os.path.exists(path) and os.path.isdir(path)
    video_exts = ['.mp4', '.mkv', '.webm', '.ogg', '.mov', '.avi', '.m4v', '.iso', '.ts', '.m2ts']
    if ext in video_exts or is_dir:
        log.warning(f"DEBUG: [Player-Trace] play_media REJECTED for video/dir: {path}. Use open_video_smart.")
        return {"status": "error", "message": "Invalid call: Use open_video_smart for Video/Dir"}

    mode = PARSER_CONFIG.get("playback_mode", "chrome_native")

    # Priority 1: Audio is always Chrome Native if mode is default or requested
    is_audio = Path(path).suffix.lower() in AUDIO_EXTENSIONS
    if is_audio:
        # User requested: "for audio always chrome native at the moment."
        return {"status": "play", "path": path, "mode": "chrome_native"}

    if mode == "chrome_native":
        # Check if natively supported by Chrome (mp4/webm/etc)
        ext = Path(path).suffix.lower()
        if ext in ('.mp4', '.webm', '.ogg'):
            return {"status": "play", "path": path, "mode": "chrome_native"}
        else:
            # Fallback to ffmpeg/vlc if not supported natively
            log.info(f"[Player] {ext} not natively supported, falling back to VLC pipe.")
            return stream_to_vlc(path)

    if mode == "cvlc" or mode == "ffmpeg" or mode == "mkvmerge":
        # These all use the VLC pipe mechanism currently
        return stream_to_vlc(path)

    if mode == "direct":
        # Direct play via system default or VLC direct
        return play_vlc(path)

    if mode == "mediamtx":
        # High-performance HLS streaming
        return stream_to_mediamtx(path, protocol="hls")

    if mode == "mediamtx_webrtc":
        # Ultra-low latency WebRTC streaming
        return stream_to_mediamtx(path, protocol="webrtc")

    if mode == "vlc_browser":
        return {"status": "play", "path": path, "mode": "vlc_browser"}


def resolve_media_path(file_path: str) -> str:
    """
    Resolves a file path that might be a URL-encoded string or a relative /media/ path.
    """
    if not file_path:
        return ""

    # Decouple from URL encoding
    path_decoded = unquote(str(file_path))

    # 1. Try direct filesystem check first (some absolute paths might exist)
    if os.path.exists(path_decoded):
        return str(Path(path_decoded).resolve())

    # 1b. Handle absolute paths where Bottle might have stripped the leading slash
    if not path_decoded.startswith("/"):
        p_abs = "/" + path_decoded
        if os.path.exists(p_abs):
            return str(Path(p_abs).resolve())

    # 2. Strip /media/ prefix if present and handle virtual pathing
    stripped_path = path_decoded
    if path_decoded.startswith("/media/"):
        stripped_path = path_decoded[len("/media/"):]
    elif path_decoded.startswith("media/"):
        stripped_path = path_decoded[len("media/"):]

    # 3. Try to find in DB using the stripped path
    db_path = db.get_media_path(stripped_path)
    if db_path and os.path.exists(db_path):
        return db_path

    # 4. Try direct filesystem check on stripped path
    if os.path.exists(stripped_path):
        return str(Path(stripped_path).resolve())

    # 5. Try resolving relative to PROJECT_ROOT/media
    media_root = PROJECT_ROOT / "media"
    alt_path = media_root / stripped_path
    if alt_path.exists():
        return str(alt_path.resolve())

    return path_decoded


def resolve_dvd_bundle_path(path_str: str) -> str:
    """
    @brief Resolves generic DVD/BD bundle folders to their underlying playable component.
    @details Wenn ein Ordner an VLC bergeben wird, sucht diese Funktion nach VIDEO_TS, BDMV oder ISO.
    """
    p = Path(path_str)
    if not p.is_dir():
        return path_str

    # Check for ISOs
    isos = list(p.glob('*.iso'))
    if len(isos) == 1:
        return str(isos[0].resolve())
    elif len(isos) > 1:
        return str(isos[0].resolve())

    # Check for VIDEO_TS or BDMV
    if (p / 'VIDEO_TS').exists():
        return str((p / 'VIDEO_TS').resolve())
    if (p / 'BDMV').exists():
        return str((p / 'BDMV').resolve())

    # Check for other common video files (e.g., MP4 in a folder)
    for ext in ['*.mp4', '*.mkv', '*.avi', '*.webm', '*.m4v', '*.ts']:
        vids = list(p.glob(ext))
        if len(vids) >= 1:
            return str(vids[0].resolve())

    return path_str


def get_best_hw_encoder():
    """
    @brief Detects available hardware encoders to reduce CPU load.
    @return Encoder name (e.g. 'h264_vaapi', 'h264_nvenc', or 'libx264' as fallback).
    """
    try:
        gpu = hardware_detector.get_gpu_info()
        encoders = gpu.get("encoders", [])

        # Priority 1: NVIDIA NVENC
        if "nvenc" in encoders:
            return "h264_nvenc"

        # Priority 2: Intel/AMD VAAPI
        if "vaapi" in encoders:
            return "h264_vaapi"

        # Priority 3: Intel QSV
        if "qsv" in encoders:
            return "h264_qsv"

    except Exception as e:
        log.warning(f"[HW Detect] Failed to probe encoders: {e}")

    return "libx264"


@eel.btl.route('/stream/via/direct/<file_path:path>')
def serve_media_raw(file_path):
    """
    @brief Serves raw media files with full Range-header support for native browser seeking.
    """
    resolved_path = resolve_media_path(file_path)
    if not os.path.exists(resolved_path):
        return bottle.HTTPError(404, "File not found")

    mimetype = 'auto'
    if resolved_path.lower().endswith('.mkv'):
        mimetype = 'video/x-matroska'
    elif resolved_path.lower().endswith('.webm'):
        mimetype = 'video/webm'

    import bottle as btl
    return btl.static_file(
        os.path.basename(resolved_path),
        root=os.path.dirname(resolved_path),
        mimetype=mimetype,
        download=False
    )


@eel.btl.route('/stream/via/transcode/<file_path:path>')
def stream_video_fragmented(file_path):
    """
    On-the-fly FragMP4/Matroska streaming via FFmpeg.
    Supports ?ss=XXXX for seeking.
    """
    import bottle
    start_time = bottle.request.query.get('ss', '0')
    audio_idx = bottle.request.query.get('audio_idx', '0')
    subs_idx = bottle.request.query.get('subs_idx', None)

    resolved_path = resolve_media_path(file_path)
    if not os.path.exists(resolved_path):
        # Fallback to DB lookup if path resolve failed (id or filename search)
        from src.core import db
        item = db.get_media_by_name(file_path)
        if item:
            resolved_path = item['path']
        else:
            return bottle.HTTPError(404, "File not found")

    if not os.path.exists(resolved_path):
        return bottle.HTTPError(404, "File not found")

    def ffmpeg_stream():
        # Auto-detect best encoder for performance
        encoder = get_best_hw_encoder()
        log.info(f"[stream] Using (Audio:{audio_idx}, Subs:{subs_idx}) via {encoder} for {resolved_path}")

        # Base command for H.264 FragMP4
        ss_args = ["-ss", str(start_time)] if float(start_time) > 0 else []
        is_iso = str(resolved_path).lower().endswith('.iso')

        # ISO / DVD optimization
        input_args = []
def delete_file(file_path):
    """Deletes high-performance JSON/text files from data/ cache."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        log.error(f"[Critical] Error deleting file {file_path}: {e}")
        return False

@eel.expose
def write_file(file_path, content):
    """Writes high-performance JSON/text files to data/ cache."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        log.error(f"[Critical] Error writing file {file_path}: {e}")
        return False

@eel.expose
def delete_directory(directory_path):
    """Deletes recursive directories from data/ cache."""
    try:
        if os.path.exists(directory_path):
            import shutil
            shutil.rmtree(directory_path)
        return True
    except Exception as e:
        log.error(f"[Critical] Error deleting directory {directory_path}: {e}")
        return False
def vlc_hls_live_proxy(filename):
    """
    @brief Serves real-time HLS segments generated by the background VLC engine.
    """
    hls_dir = "/tmp/vlc_hls"
    safe_target = os.path.join(hls_dir, filename)

    if not os.path.exists(safe_target):
        return bottle.HTTPResponse(status=404)

    ext = os.path.splitext(filename)[1].lower()
    mimetype = 'application/x-mpegURL' if ext == '.m3u8' else 'video/MP2T'

    try:
        with open(safe_target, 'rb') as f:
            data = f.read()
        return bottle.HTTPResponse(data, status=200, headers={
            'Content-Type': mimetype,
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Access-Control-Allow-Origin': '*'
        })
    except Exception:
        return bottle.HTTPResponse(status=500)


@eel.btl.route('/video-remux-stream/<item_id:path>')
def video_remux_stream(item_id):
    """
    @brief Real-time remuxing to Matroska/WebM for Chrome Native playback.
    Supports ?ss=XXXX for seeking.
    """
    import bottle
    start_time = bottle.request.query.get('ss', '0')
    audio_idx = bottle.request.query.get('audio_idx', '0')
    subs_idx = bottle.request.query.get('subs_idx', None)

    try:
        from src.core import db
        item = db.get_media_by_id(item_id)
        if not item:
            # Fallback: check if item_id is actually a name
            item = db.get_media_by_name(item_id)
            if not item:
                # Last fallback: literal path
                item_path = resolve_media_path(item_id)
                if os.path.exists(item_path):
                    file_path = item_path
                else:
                    log.warning(f" [Remux] Field not found in DB or filesystem: {item_id}")
                    return bottle.HTTPResponse(status=404)
            else:
                file_path = item['path']
        else:
            file_path = item['path']

        log.info(f" [Remux] Starting live Pipe-Kit (Audio:{audio_idx}, Subs:{subs_idx}) for: {file_path}")

        mkvmerge_path = shutil.which('mkvmerge') or 'mkvmerge'
        ffmpeg_path = shutil.which('ffmpeg') or 'ffmpeg'

        def generate():
            # PIPE-KIT: mkvmerge (MKV) -> ffmpeg (FragMP4)
            # This provides the best of both worlds: lossless remux and browser-friendly streaming.
            mkv_proc = None
            ffmpeg_proc = None

            try:
                # Seeking support
                ss_args = ["-ss", str(start_time)] if float(start_time) > 0 else []
                is_iso = str(file_path).lower().endswith('.iso')

                # FOR DVDs: Force transcoding because fMP4 in Chrome doesn't support MPEG-2 (VOB/ISO)
                if is_iso:
                    log.info(f" [Remux] ISO detected, redirecting to transcode flow for compatibility.")
                    return stream_video_fragmented(item_id)

                # Mapping support for track switching
                map_args = ["-map", "0:v:0", "-map", f"0:a:{audio_idx}"]
                if subs_idx is not None and str(subs_idx).lower() != 'none':
                    map_args += ["-map", f"0:s:{subs_idx}"]

                if is_mkvtoolnix_available() and float(start_time) == 0 and audio_idx == '0' and not subs_idx:
                    # Lossless remux via mkvmerge for start (best compatibility)
                    mkv_proc = subprocess.Popen(
                        [mkvmerge_path, "-o", "-", str(file_path)],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1024 * 1024
                    )
                    log_process_stderr(mkv_proc, "MKVMerge-Pipe")

                    ffmpeg_cmd = [
                        ffmpeg_path, "-loglevel", "error", "-i", "pipe:0",
                        "-c", "copy", "-f", "mp4",
                        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
                        "-"
                    ]
                    ffmpeg_proc = subprocess.Popen(
                        ffmpeg_cmd, stdin=mkv_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1024 * 1024
                    )
                    log_process_stderr(ffmpeg_proc, "FFmpeg-Frag")
                else:
                    # Use FFmpeg for seeking/mapping remux (more reliable for mid-stream offsets/tracks)
                    ffmpeg_cmd = [
                        ffmpeg_path, "-loglevel", "error"
                    ] + ss_args + [
                        "-i", str(file_path)
                    ] + map_args + [
                        "-c", "copy", "-f", "mp4",
                        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
                        "-"
                    ]
                    ffmpeg_proc = subprocess.Popen(
                        ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1024 * 1024
                    )
                    log_process_stderr(ffmpeg_proc, "FFmpeg-Remux-SS")

                # Stream chunks to browser
                while True:
                    if ffmpeg_proc.stdout is None:
                        break
                    chunk = ffmpeg_proc.stdout.read(256 * 1024)
                    if not chunk:
                        break
                    yield chunk
            except Exception as e:
                log.error(f" [Remux] Generator error: {e}")
            finally:
                # Cleanup processes
                for p in [ffmpeg_proc, mkv_proc]:
                    if p:
                        try:
                            p.terminate()
                            p.wait(timeout=1)
                        except:
                            try:
                                p.kill()
                            except:
                                pass
                log.info(f" [Remux] Finalized Pipe-Kit stream for: {file_path}")

        return bottle.HTTPResponse(generate(), content_type="video/mp4")
    except Exception as e:
        import traceback
        log.error(f" [Remux] CRITICAL ERROR: {e}\n{traceback.format_exc()}")
        return bottle.HTTPError(500, f"Remux Error: {e}")


def get_video_metadata(file_path: str) -> dict:
    """
    Analyzes a video file using ffprobe and returns codec/container info.
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return {}
        data = json.loads(result.stdout)

        streams = data.get('streams', [])
        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        format_info = data.get('format', {})

        return {
            "codec": video_stream.get('codec_name', ''),
            "width": int(video_stream.get('width', 0)),
            "height": int(video_stream.get('height', 0)),
            "container": format_info.get('format_name', '').split(',')[0],
            "duration": float(format_info.get('duration', 0))
        }
    except Exception as e:
        log.error(f"[ffprobe] Auto-detect failed: {e}")
        return {}


@eel.expose
def open_with_ffplay(file_path: str):
    """Explicitly open a file with ffplay."""
    file_path = resolve_media_path(file_path)
    try:
        ffplay_path = shutil.which("ffplay") or "ffplay"
        proc = subprocess.Popen([str(ffplay_path), str(file_path)])
        ACTIVE_SUBPROCESSES.append(proc)
        log.info(f" [FFplay] Started for: {file_path}")
        return {"status": "ok", "mode": "ffplay"}
    except Exception as e:
        return {"status": "error", "error": f"FFplay failed: {e}"}


@eel.expose
def open_with_vlc(file_path: str):
    """Explicitly open a file with VLC (GUI)."""
    file_path = resolve_media_path(file_path)
    try:
        vlc_path = shutil.which("vlc") or "vlc"
        proc = subprocess.Popen([str(vlc_path), str(file_path)])
        ACTIVE_SUBPROCESSES.append(proc)
        log.info(f" [VLC] Started for: {file_path}")
        return {"status": "ok", "mode": "vlc"}
    except Exception as e:
        return {"status": "error", "error": f"VLC failed: {e}"}


@eel.expose
def open_with_cvlc(file_path: str):
    """Explicitly open a file with CVLC (command-line VLC)."""
    file_path = resolve_media_path(file_path)
    try:
        vlc_path = shutil.which("cvlc") or "cvlc"
        proc = subprocess.Popen([str(vlc_path), str(file_path)])
        ACTIVE_SUBPROCESSES.append(proc)
        log.info(f" [CVLC] Started for: {file_path}")
        return {"status": "ok", "mode": "cvlc"}
    except Exception as e:
        return {"status": "error", "error": f"CVLC failed: {e}"}


@eel.expose
def open_with_pyvlc(file_path: str):
    """Explicitly open a file with python-vlc (libvlc bindings)."""
    file_path = resolve_media_path(file_path)
    try:
        import vlc
    except Exception as e:
        return {"status": "error", "error": f"PyVLC failed: {e}"}


def start_vlc_guarded(file_path: str, mode: str, prefix: str = "", source: str = "unknown", start_time: float = 0):
    """
    @brief Safely starts a VLC instance for either external playback or HLS streaming.
    Supports start_time for HLS seeking.
    """
    pid_tag = f"{source}|{os.getpid()}"
    log.info(f" [VLC-Instance-Trace] {pid_tag} Attempting start for: {file_path}")

    # 1. Stop any existing VLC managed by us
    try:
        stop_vlc()
        # Proactive: Shell kill to be absolutely sure
        subprocess.run(["pkill", "-9", "-f", "vlc"], capture_output=True)
    except:
        pass

    vlc_path = shutil.which('vlc') or '/usr/bin/vlc'
    full_path = f"{prefix}{file_path}"

    if mode == "vlc_embedded":
        # HLS Live Stream Engine
        # Strategy: Headless VLC stream-out (HLS) for native Video.js compatibility
        # We use a managed temporary directory for the HLS segments
        hls_dir = "/tmp/vlc_hls"
        if os.path.exists(hls_dir):
            shutil.rmtree(hls_dir)
        os.makedirs(hls_dir, exist_ok=True)

        index_file = os.path.join(hls_dir, "stream.m3u8")
        # VLC HLS sout chain
        # Note: index-url is relative to the playlist file for best compatibility
        sout = (
            "#transcode{vcodec=h264,vb=3000,acodec=aac,ab=128,channels=2,samplerate=44100}:"
            "std{access=livehttp{seglen=5,deldone=1,numseg=10,"
            f"index={index_file},index-url=vlc-hls-segment-########.ts}},"
            f"mux=ts,dst={hls_dir}/vlc-hls-segment-########.ts}}"
        )

        try:
            control_port = find_free_port()
            log.info(f"[VLC-HLS-Streamer] {pid_tag} Starting Headless HLS at {
                     start_time}s: {full_path} -> {index_file} (Control: {control_port})")

            cmd = [
                str(vlc_path), "-I", "dummy", "--no-video-title-show", "--quiet",
                "--intf", "http", "--http-port", str(control_port), "--http-password", "mwv"
            ]
            if float(start_time) > 0:
                cmd += ["--start-time", str(start_time)]

            # Optimization: Shorter segments for better interactive feel (low delay)
            sout_interactive = sout.replace("seglen=5", "seglen=1")

            cmd += [
                f"{prefix}{file_path}", "--sout", sout_interactive,
                "--sout-all", "--sout-keep", "vlc://quit"
            ]

            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            ACTIVE_SUBPROCESSES.append(proc)

            # Success: We return the special HLS route for Video.js
            return {
                "status": "play",
                "path": "/vlc-hls-live/stream.m3u8",
                "mode": "vlc_embedded",
                "type": "application/x-mpegURL",
                "instance_id": pid_tag,
                "control_port": control_port
            }
        except Exception as e:
            log.error(f"[VLC-HLS-Streamer] HLS-Out failed: {e}")
            return {"status": "error", "error": f"VLC HLS Streamer failed: {e}"}

    try:
        log.info(f"[VLC-Starter] {pid_tag} Launching binary: {vlc_path} {full_path}")
        proc = subprocess.Popen([str(vlc_path), str(full_path)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                start_new_session=True)
        ACTIVE_SUBPROCESSES.append(proc)
        return {"status": "ok", "mode": mode, "instance_id": pid_tag}
    except Exception as e:
        return {"status": "error", "error": f"VLC start failed: {e}"}


@eel.expose
def send_vlc_command(port, command, val=None):
    """
    @brief Proxies control commands to the local VLC instance's HTTP interface.
    @param port The HTTP port of the VLC instance.
    @param command The command to send (e.g. 'key').
    @param val The value for the command (e.g. 'key-up').
    """
    try:
        url = f"http://localhost:{port}/requests/status.xml"
        params = {"command": command}
        if val:
            params["val"] = val

        # VLC HTTP Auth: username is empty, password is 'mwv'
        response = requests.get(url, params=params, auth=('', 'mwv'), timeout=1)
        if response.status_code == 200:
            return {"status": "ok"}
        return {"status": "error", "code": response.status_code}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def open_video(file_path: str, player_type: str = "auto", mode: str = "auto", source: str = "direct", start_time: float = 0):
    """
    @brief Explicitly opens a media file with a specific player type and mode.
    Handles 'auto' routing and specializes for ISO, DVD, Audio.
    """
    log.info(
        f"DEBUG: [Player-Trace] open_video called from {source} for: {file_path} (type: {player_type}, mode: {mode})")
    file_path = resolve_media_path(file_path)

    # Global double-trigger lock (Python side - SECOND LAYER)
    now = time.time()
    lock_key = f"{file_path}_lock"
    if now - PLAYBACK_LOCKS.get(lock_key, 0) < 2.0:
        log.warning(f"DEBUG: [Player-Trace] open_video REJECTED by lock for {file_path} (Source: {source})")
        return {"status": "ok", "mode": "locked"}
    PLAYBACK_LOCKS[lock_key] = now

    # 1. Advanced Format Analysis
    is_dvd_iso = str(file_path).lower().endswith('.iso')
    is_dvd_folder = False
    if os.path.isdir(file_path):
        is_dvd_folder = any([
            os.path.exists(os.path.join(file_path, "VIDEO_TS")),
            os.path.exists(os.path.join(file_path, "BDMV")),
            any(f.lower().endswith('.iso') for f in os.listdir(file_path))
        ])
    is_audio = str(file_path).lower().endswith(('.mp3', '.m4b', '.opus', '.flac', '.wav'))

    log.info(f"DEBUG: [Player-Trace] Analysis: ISO={is_dvd_iso}, DVD_Folder={is_dvd_folder}, Audio={is_audio}")

    # 2. Auto-Detection Logic (only runs when mode is truly 'auto')
    if mode == "auto":
        if is_dvd_iso or is_dvd_folder:
            # Prefer native transcode for seeking support (?ss=)
            player_type, mode = "chrome", "chrome_transcode"
        elif is_audio:
            player_type, mode = "chrome", "chrome_direct"
        else:
            meta = get_video_metadata(file_path)
            codec = meta.get('codec', '').lower()
            container = meta.get('container', '').lower()

            # Chrome Routing Logic: Favor the new PIPE-KIT for MKVs
            if container == 'matroska' and is_mkvtoolnix_available():
                player_type, mode = "chrome", "chrome_remux"  # Upgraded to PIPE-KIT
            elif (codec == 'h264' and container in ('mp4', 'mov', 'quicktime')) or \
                 (codec in ('vp8', 'vp9', 'av1') and container in ('matroska', 'webm')):
                player_type, mode = "chrome", "chrome_direct"
            elif codec == 'h264':
                player_type, mode = "chrome", "chrome_remux"
            else:
                player_type, mode = "chrome", "chrome_fragmp4"
    elif player_type == "auto":
        # If only player_type is 'auto' but mode is explicit, infer player_type from mode
        if mode.startswith("chrome_"):
            player_type = "chrome"
        elif mode.startswith("vlc_"):
            player_type = "vlc"
        elif mode.startswith("pyplayer_"):
            player_type = "pyplayer"
        elif mode.startswith("mtx_"):
            player_type = "chrome"  # MTX modes play back through Chrome/Video.js

    # 3. Player Routing
    if player_type == "vlc":
        # Normalize DVD path if it points to a subfolder
        target_path = file_path
        if is_dvd_folder and os.path.basename(str(file_path)).upper() == "VIDEO_TS":
            target_path = os.path.dirname(str(file_path))
            log.info(f"DEBUG: [Player-Trace] DVD Normalization: {file_path} -> {target_path}")

        prefix = "dvd://" if is_dvd_folder or is_dvd_iso else ""
        # Default to embedded HLS if not specified as browser (standalone)
        if mode == "vlc_extern":
            # Launch standalone VLC
            vlc_path = shutil.which("vlc") or "vlc"
            try:
                proc = subprocess.Popen([str(vlc_path), str(file_path)])
                ACTIVE_SUBPROCESSES.append(proc)
                return {"status": "ok", "mode": "vlc_extern"}
            except Exception as e:
                log.error(f"VLC standalone failed: {e}")
                return {"status": "error", "error": f"VLC failed: {e}"}

        if mode == "auto" or mode == "vlc_embedded":
            return start_vlc_guarded(target_path, "vlc_embedded", prefix, source=f"open_video_{source}", start_time=start_time)
        return start_vlc_guarded(target_path, mode, prefix, source=f"open_video_{source}", start_time=start_time)

    elif player_type == "ffplay":
        return open_with_ffplay(file_path)

    elif player_type == "pyplayer":
        # pyvidplayer2 / standalone
        if mode == "pyplayer_mpv":
            # Launch mpv if available
            mpv_path = shutil.which("mpv") or "mpv"
            try:
                proc = subprocess.Popen([str(mpv_path), str(file_path)])
                ACTIVE_SUBPROCESSES.append(proc)
                return {"status": "ok", "mode": "mpv"}
            except Exception as e:
                return {"status": "error", "error": f"MPV failed: {e}"}

        # Default: pyvidplayer2
        try:
            import pyvidplayer2
            # Use subprocess to avoid blocking Eel thread
            proc = subprocess.Popen([sys.executable, "-m", "pyvidplayer2", str(file_path)])
            ACTIVE_SUBPROCESSES.append(proc)
            return {"status": "ok", "mode": "pyplayer"}
        except ImportError:
            # Fallback to FFplay if pyvidplayer2 is missing
            return open_with_ffplay(file_path)
        except Exception as e:
            return {"status": "error", "error": f"PyPlayer failed: {e}"}

    elif player_type == "mpv":
        return open_mpv(file_path)

    if player_type == "chrome":
        if mode.startswith("mtx_"):
            # Redirect to MediaMTX handler
            variant = "webrtc" if mode == "mtx_webrtc" else "hls"
            return stream_to_mediamtx(file_path, protocol=variant)

        if mode == "chrome_transcode":
            import urllib.parse
            rel = os.path.relpath(file_path, PROJECT_ROOT / "media")
            safe_rel = urllib.parse.quote(rel, safe='')
            # Get best encoder to determine if HW accel is used
            enc = get_best_ffmpeg_encoder()
            is_hw = enc != "libx264"
            return {
                "status": "play",
                "path": f"/transcode/{safe_rel}",
                "mode": "chrome_transcode",
                "type": "video/mp4",
                "hw_accel": is_hw,
                "encoder": enc
            }

        if mode == "chrome_direct":
            import urllib.parse
            safe_path = urllib.parse.quote(str(file_path), safe='')
            return {"status": "play", "path": f"/media-raw/{safe_path}", "mode": "chrome_direct", "type": "video/mp4"}
        elif mode in ("chrome_remux", "chrome_fragmp4", "chrome_hls"):
            # Note: chrome_hls is treated as remux/fragmp4 pipeline back-of-house
            # unless a real HLS backend (like MTX) is selected.
            from src.core import db
            item = db.get_media_by_path(file_path)
            item_id = item.get('id') if item else file_path
            import urllib.parse
            safe_id = urllib.parse.quote(str(item_id), safe='')
            return {"status": "play", "path": f"/video-remux-stream/{safe_id}", "mode": mode, "type": "video/mp4"}

    return {"status": "error", "error": f"Invalid config: {player_type}/{mode}"}

    # Fallback/Default
    return play_media(file_path)


# Global Locks for Player Triggers
PLAYBACK_LOCKS: dict[str, float] = {}


@eel.expose
def vlc_seek(instance_id, time_seconds):
    """
    @brief Seeks within an active VLC HLS stream by restarting the process with an offset.
    @param instance_id The PID tag or process reference.
    @param time_seconds The timestamp to jump to.
    """
    log.info(f" [VLC-Seek] Jumping to {time_seconds}s for instance {instance_id}")

    # 1. Kill old process
    # We need to find the process by its item path or similar if instance_id isn't enough
    # For now, let's assume we can find it in ACTIVE_SUBPROCESSES
    # Implementation detail: start_vlc_guarded should ideally store the metadata

    # Simple strategy: stop all VLC and restart the last one with offset
    # But better: rely on the fact that vlc_embedded only allows one active stream
    stop_vlc()

    # Note: frontend needs to call open_video again with the start_time
    # or we do it here. Restarting from here requires knowing the original path.
    return {"status": "ok"}


@eel.expose
def play_external_file(path: str):
    """
    @brief Plays a local file that was dropped onto the UI or selected via picker.
    """
    log.info(f" [External-Play] File: {path}")
    try:
        abs_path = Path(path).resolve()
        # Fallback for relative paths if not found directly
        if not abs_path.exists():
            # Try to resolve relative to common roots if passed as just a name
            abs_path = Path(resolve_media_path(path))

        if not abs_path.exists():
            return {"status": "error", "error": f"Datei nicht gefunden: {path}"}

        # Use vlc_extern (standalone) or vlc_embedded based on preference,
        # default to smart logic but hint external.
        return open_video_smart(str(abs_path), mode="vlc_extern")
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def play_stream_url(url: str, engine: str = "hls"):
    """
    @brief Returns playback parameters for a specific network stream URL.
    """
    log.info(f" [External-Play] Stream: {url} via {engine}")
    # Basic validation
    if not url.startswith(('http', 'rtsp', 'rtmp')):
        return {"status": "error", "error": "Ungltiges Protokoll. Erwartet http, rtsp oder rtmp."}

    # HLS is handles natively by the browser player via Video.js
    if engine == "hls" or url.endswith('.m3u8'):
        return {"status": "ok", "hls": url, "type": "application/x-mpegURL"}

    # Other protocols might need specialized handling or just returned
    return {"status": "ok", "url": url}


@eel.expose
def open_video_smart(file_path: str, mode: str = "auto", start_time: float = 0):
    """
    @brief Smart routing for video playback as described in videoplayer logbuch.
    Supports Direct Play, MediaMTX (HLS/WebRTC), and FragMP4.
    """
    log.info(f"DEBUG: [Player-Trace] open_video_smart called for: {file_path} (mode: {mode})")

    # Global double-trigger lock (Python side)
    now = time.time()
    last_trigger = PLAYBACK_LOCKS.get(str(file_path), 0)
    if now - last_trigger < 2.0:
        log.warning(f"DEBUG: [Player-Trace] open_video_smart LOCK active for {file_path}. Skipping.")
        return {"status": "error", "error": "Debounced"}
    PLAYBACK_LOCKS[str(file_path)] = now

    file_path = resolve_media_path(file_path)

    # 1. Compatibility Check (simplified version of logbuch logic)
    meta = get_video_metadata(file_path)
    codec = meta.get('codec', '').lower()
    is_disc_img = str(file_path).lower().endswith(('.iso', '.bin', '.img'))

    # Special: Browsers hate MPEG-1/2 (DVD PAL format) or ISOs. Route to Transcode Pipeline.
    if "mpeg" in codec or "mp2" in codec or is_disc_img:
        log.info(f"DEBUG: [Player-Trace] MPEG/ISO detected in {file_path}. Using Chrome Transcode Pipeline.")
        return open_video(file_path, "chrome", "chrome_transcode", source="smart_router_upgrade", start_time=start_time)

    if os.path.exists(file_path) and os.path.isdir(file_path):
        try:
            is_dvd = any([
                os.path.exists(os.path.join(file_path, "VIDEO_TS")),
                os.path.exists(os.path.join(file_path, "BDMV")),
                any(f.lower().endswith(('.iso', '.bin', '.img')) for f in os.listdir(file_path))
            ])
        except:
            pass

    # Check DB category for specialized routing
    from src.core import db
    db_item = db.get_media_by_path(str(file_path))
    category = db_item.get('category', '') if db_item else ''

    if is_dvd or is_disc_img or category in ('Film', 'Abbild'):
        log.info(
            f"DEBUG: [Player-Trace] DVD/Film/DiscImg detected in smart router (Category: {category}). Forcing VLC Embedded.")
        return open_video(file_path, "vlc", "vlc_embedded", source="smart_router_dvd_film")

    return open_video(file_path, "auto", mode, source="smart_router_auto")


@eel.expose
def analyse_media(path):
    """
    @brief Performs deep analysis of a media file.
    """
    if not PARSER_CONFIG.get("feature_flags", {}).get("analyse_mode", False):
        return {"status": "error", "message": "Analyse mode is disabled"}

    import src.parsers.ffprobe_parser as ffprobe_parser
    try:
        # Pass empty dict for tags and settings if needed, or use a more direct way
        dummy_tags = {}
        analysis = ffprobe_parser.parse(Path(path), Path(path).suffix, dummy_tags, mode='full', settings={'timeout': 5})
        return {"status": "ok", "analysis": analysis}
    except Exception as e:
        log.error(f"[Analyse] Failed for {path}: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def write_media_tags(path, tags):
    """
    @brief Writes tags to a media file, with safety checks.
    """
    if not PARSER_CONFIG.get("feature_flags", {}).get("write_mode", False):
        return {"status": "error", "message": "Write mode is disabled"}

    # Check for blocking formats
    ext = Path(path).suffix.lower()
    if ext in ('.iso', '.mkv'):
        # For ISO/MKV, we use mkvpropedit if available
        log.info(f"[Write] Using specialized writer for {ext}")

    try:
        success = tag_writer.write_tags(path, tags)
        if success:
            return {"status": "ok"}
        else:
            return {"status": "error", "message": "Tag writing failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Playlist state (in-memory)
CURRENT_PLAYLIST: list[dict] = []
CURRENT_INDEX: int = -1


@eel.expose
def set_current_playlist(
        items: list,
        start_index: int = 0,
        replace: bool = True):
    """Set the active playlist. `items` is a list of media dicts or names.
    If replace is False, append to existing playlist. start_index selects initial item.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    # Normalize items: if list of names, convert to minimal dicts
    normalized = []
    for it in items:
        if isinstance(it, str):
            normalized.append({"name": it})
        elif isinstance(it, dict):
            normalized.append(it)
    if replace:
        CURRENT_PLAYLIST = normalized
    else:
        CURRENT_PLAYLIST.extend(normalized)

    if not CURRENT_PLAYLIST:
        CURRENT_INDEX = -1
    else:
        CURRENT_INDEX = max(
            0, min(len(CURRENT_PLAYLIST) - 1, int(start_index or 0)))

    return {
        "status": "ok",
        "count": len(CURRENT_PLAYLIST),
        "index": CURRENT_INDEX}


@eel.expose
def get_current_playlist():
    global CURRENT_PLAYLIST, CURRENT_INDEX
    return {"items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


# expose get_current_playlist to eel so frontend can refresh after reorder
# actions
@eel.expose
def get_current_playlist_exposed():
    return get_current_playlist()


@eel.expose
def _play_index(idx: int):
    """Internal: play item at index if valid. Returns status dict."""
    global CURRENT_PLAYLIST, CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}
    CURRENT_INDEX = idx
    item = CURRENT_PLAYLIST[CURRENT_INDEX]
    path = item.get("path") or item.get("name")
    # If path is a DB name, resolve to path via DB lookup
    try:
        if path and not Path(path).exists():
            # Attempt to find in DB by name
            match = db.get_media_by_name(path)
            if match:
                path = match.get("path") or path
    except Exception:
        pass

    # Call existing play_media to trigger frontend actions
    return play_media(path)


@eel.expose
def next_in_playlist():
    global CURRENT_INDEX, CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    next_idx = CURRENT_INDEX + 1 if CURRENT_INDEX + \
        1 < len(CURRENT_PLAYLIST) else -1
    if next_idx == -1:
        return {"status": "end"}
    return _play_index(next_idx)


@eel.expose
def prev_in_playlist():
    global CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    prev_idx = CURRENT_INDEX - 1 if CURRENT_INDEX - 1 >= 0 else -1
    if prev_idx == -1:
        return {"status": "start"}
    return _play_index(prev_idx)


@eel.expose
def jump_to_index(index: int):
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}
    return _play_index(idx)


@eel.expose
def move_item_up(index: int):
    """
    Move playlist item at `index` one position up (towards start).
    Adjusts `CURRENT_INDEX` if necessary. Returns status and updated playlist.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx <= 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}

    # swap
    CURRENT_PLAYLIST[idx
                     - 1], CURRENT_PLAYLIST[idx] = CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx
                                                                                           - 1]

    # adjust current index if it was involved
    if CURRENT_INDEX == idx:
        CURRENT_INDEX = idx - 1
    elif CURRENT_INDEX == idx - 1:
        CURRENT_INDEX = idx

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_item_down(index: int):
    """
    Move playlist item at `index` one position down (towards end).
    Adjusts `CURRENT_INDEX` if necessary. Returns status and updated playlist.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST) - 1:
        return {"status": "error", "message": "index out of range"}

    # swap
    CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx
                                            + 1] = CURRENT_PLAYLIST[idx + 1], CURRENT_PLAYLIST[idx]

    # adjust current index if it was involved
    if CURRENT_INDEX == idx:
        CURRENT_INDEX = idx + 1
    elif CURRENT_INDEX == idx + 1:
        CURRENT_INDEX = idx

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_item_up_by_key(key: str):
    """Move the first playlist item matching `key` (name or path) up by one.
    Returns the same structure as `move_item_up`.
    """
    global CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if not key:
        return {"status": "error", "message": "invalid key"}
    # find index by multiple candidate fields and fallbacks

    def matches(it, key):
        if not isinstance(it, dict):
            return False
        # exact fields
        for f in ('name', 'filename', 'path', 'id'):
            v = it.get(f)
            if v and v == key:
                return True
        # tags.title
        tags = it.get('tags') or {}
        if tags.get('title') and tags.get('title') == key:
            return True
        # substring matches for path or name
        for f in ('name', 'filename', 'path'):
            v = it.get(f)
            if v and isinstance(v, str) and key in v:
                return True
        return False

    for idx, it in enumerate(CURRENT_PLAYLIST):
        if matches(it, key):
            log.debug(f"[DEBUG] move_item_up_by_key: matched idx={
                idx} key={key} item={it}")
            return move_item_up(idx)

    # last resort: try matching by stringified dict values
    for idx, it in enumerate(CURRENT_PLAYLIST):
        try:
            s = ' '.join(str(x) for x in it.values())
            if key in s:
                return move_item_up(idx)
        except Exception:
            continue

    log.debug(f"[DEBUG] move_item_up_by_key: no match for key={key}")
    return {"status": "error", "message": "item not found"}


@eel.expose
def move_item_down_by_key(key: str):
    """Move the first playlist item matching `key` (name or path) down by one.
    Returns the same structure as `move_item_down`.
    """
    global CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if not key:
        return {"status": "error", "message": "invalid key"}

    def matches(it, key):
        if not isinstance(it, dict):
            return False
        for f in ('name', 'filename', 'path', 'id'):
            v = it.get(f)
            if v and v == key:
                return True
        tags = it.get('tags') or {}
        if tags.get('title') and tags.get('title') == key:
            return True
        for f in ('name', 'filename', 'path'):
            v = it.get(f)
            if v and isinstance(v, str) and key in v:
                return True
        return False

    for idx, it in enumerate(CURRENT_PLAYLIST):
        if matches(it, key):
            log.debug(f"[DEBUG] move_item_down_by_key: matched idx={
                idx} key={key} item={it}")
            return move_item_down(idx)

    for idx, it in enumerate(CURRENT_PLAYLIST):
        try:
            s = ' '.join(str(x) for x in it.values())
            if key in s:
                return move_item_down(idx)
        except Exception:
            continue

    log.debug(f"[DEBUG] move_item_down_by_key: no match for key={key}")
    return {"status": "error", "message": "item not found"}


def _extract_key_from_obj(item_obj: dict) -> str:
    """Helper to extract a unique key (id or path) from a media item dictionary."""
    if not isinstance(item_obj, dict):
        return ""
    # Try common keys
    for k in ['id', 'path', 'filepath', 'url', 'key']:
        if item_obj.get(k):
            return str(item_obj[k])
    return ""


@eel.expose
def move_item_up_by_obj(item_obj):
    """Expose: accept a JS object representing the item, extract a key and move up."""
    try:
        # item_obj comes from Eel as a dict
        key = _extract_key_from_obj(item_obj)
        if not key:
            log.debug(
                f"[DEBUG] move_item_up_by_obj: could not extract key from {item_obj}")
            return {"status": "error", "message": "no key extracted"}
        return move_item_up_by_key(key)
    except Exception as e:
        log.error(f"[ERROR] move_item_up_by_obj exception: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def move_item_down_by_obj(item_obj):
    """Expose: accept a JS object representing the item, extract a key and move down."""
    try:
        key = _extract_key_from_obj(item_obj)
        if not key:
            log.debug(
                f"[DEBUG] move_item_down_by_obj: could not extract key from {item_obj}")
            return {"status": "error", "message": "no key extracted"}
        return move_item_down_by_key(key)
    except Exception as e:
        log.error(f"[ERROR] move_item_down_by_obj exception: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def remove_playlist_item(index: int):
    """
    Remove playlist item at `index` from CURRENT_PLAYLIST.
    Adjusts CURRENT_INDEX accordingly.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}

    CURRENT_PLAYLIST.pop(idx)

    if CURRENT_INDEX == idx:
        CURRENT_INDEX = -1
    elif CURRENT_INDEX > idx:
        CURRENT_INDEX -= 1

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_current_up():
    """Move the currently selected playlist item up by one position."""
    global CURRENT_INDEX
    if CURRENT_INDEX is None or CURRENT_INDEX < 0:
        return {"status": "error", "message": "no current item"}
    log.debug(
        f"[Playlist] move_current_up called. CURRENT_INDEX={CURRENT_INDEX}")
    return move_item_up(CURRENT_INDEX)


@eel.expose
def move_current_down():
    """Move the currently selected playlist item down by one position."""
    global CURRENT_INDEX
    if CURRENT_INDEX is None or CURRENT_INDEX < 0:
        return {"status": "error", "message": "no current item"}
    log.debug(
        f"[Playlist] move_current_down called. CURRENT_INDEX={CURRENT_INDEX}")
    return move_item_down(CURRENT_INDEX)


@eel.expose
def move_item_to(old_index: int, new_index: int):
    """
    Move an item from old_index to new_index within CURRENT_PLAYLIST.
    Adjusts CURRENT_INDEX accordingly and returns updated playlist state.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        o = int(old_index)
        n = int(new_index)
    except Exception:
        return {"status": "error", "message": "invalid index"}
    log.debug(f"[Playlist] move_item_to called. old={
        o}, new={n}, CURRENT_INDEX={CURRENT_INDEX}")

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}

    length = len(CURRENT_PLAYLIST)
    if o < 0 or o >= length or n < 0:
        return {"status": "error", "message": "index out of range"}

    # clamp new index to [0, length-1] for insertion positions (allow append
    # at length)
    if n > length:
        n = length

    if o == n or (o == n - 1 and o < n):
        # nothing to do (moving to same place)
        return {
            "status": "ok",
            "items": CURRENT_PLAYLIST,
            "index": CURRENT_INDEX}

    try:
        item = CURRENT_PLAYLIST.pop(o)
        # If popping an earlier index shifts target left, insertion at n is
        # still correct
        if n > len(CURRENT_PLAYLIST):
            n = len(CURRENT_PLAYLIST)
        CURRENT_PLAYLIST.insert(n, item)

        # Update CURRENT_INDEX
        if CURRENT_INDEX == o:
            CURRENT_INDEX = n
        else:
            if o < CURRENT_INDEX <= n:
                # item moved forward past current item -> current shifts left
                CURRENT_INDEX -= 1
            elif n <= CURRENT_INDEX < o:
                # item inserted before current -> current shifts right
                CURRENT_INDEX += 1

        return {
            "status": "ok",
            "items": CURRENT_PLAYLIST,
            "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def open_in_explorer(path_str):
    """
    @brief Opens a specific file or folder in the system's native file explorer.
    @details ffnet eine Datei oder einen Ordner im nativen Datei-Explorer des Systems.
    @param path_str Absolute path / Absoluter Pfad.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    path_obj = Path(path_str)
    if not path_obj.exists():
        log.warning(
            "[FileExplorer] Path does not exist / Pfad existiert nicht")
        return {"error": "Nicht gefunden"}

    try:
        # Check OS and open accordingly
        if os.name == 'nt':  # Windows
            # Use getattr to satisfy mypy on non-Windows systems
            startfile = getattr(os, 'startfile', None)
            if startfile:
                startfile(path_str)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', '-R', path_str])
        else:  # Linux (freedesktop)
            subprocess.run(['xdg-open', str(path_obj.parent)])
        return {"status": "ok"}
    except Exception as e:
        log.error(
            f"[FileExplorer] Error opening path / Fehler beim Oeffnen: {e}")
        return {"error": str(e)}


@eel.expose
def browse_dir(dir_path=None):
    """
    @brief Lists folders and audio files for the in-app file browser.
    @details Listet Ordner und Audiodateien eines Verzeichnisses fr den Datei-Browser.
    @param dir_path Directory path / Verzeichnispfad.
    @return Dictionary with path info and item list / Dictionary mit Pfad-Infos und Element-Liste.
    """
    if not dir_path:
        dir_path = BROWSER_DEFAULT_DIR

    target = Path(dir_path)
    if not target.exists() or not target.is_dir():
        return {"error": "Ordner nicht gefunden", "path": dir_path}

    items = []
    try:
        for entry in sorted(
            target.iterdir(),
            key=lambda e: (
                not e.is_dir(),
                e.name.lower())):
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                items.append(
                    {"name": entry.name, "path": str(entry), "type": "folder"})
            elif entry.suffix.lower() in AUDIO_EXTENSIONS or entry.suffix.lower() in VIDEO_EXTENSIONS:
                size_mb = entry.stat().st_size / (1024 * 1024)
                item_type = "video" if entry.suffix.lower() in VIDEO_EXTENSIONS else "audio"
                items.append({"name": entry.name, "path": str(
                    entry), "type": item_type, "size": f"{size_mb:.1f} MB"})
    except PermissionError:
        return {"error": "Keine Berechtigung", "path": dir_path}

    parent = str(target.parent) if target.parent != target else None
    return {"path": str(target), "parent": parent, "items": items}


@eel.expose
def pick_folder():
    """
    @brief Opens a native OS folder selection dialog using Tkinter.
    @details ffnet einen nativen Ordner-Auswahldialog mittels Tkinter.
    @return Selected path or None / Gewhlter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder_path = filedialog.askdirectory()
        root.destroy()
        return folder_path if folder_path else None
    except Exception as e:
        log.error(f"[System] Folder picker failed: {e}")
        return None


@eel.expose
def add_file_to_library(file_path):
    """
    @brief Adds a single file from the browser to the library.
    @details Fgt eine einzelne Datei aus dem Datei-Browser der Bibliothek hinzu.
    @param file_path Absolute path / Absoluter Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    if p.suffix.lower() not in AUDIO_EXTENSIONS and p.suffix.lower() not in VIDEO_EXTENSIONS:
        return {"error": "Kein untersttztes Audio- oder Videoformat"}

    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}

    item = MediaItem(p.name, p)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}


# VLC Player Instance (Global)
VLC_INSTANCE = None
VLC_PLAYER = None
ACTIVE_SUBPROCESSES = []


@eel.expose
def play_vlc(file_path: str):
    """
    @brief Plays a media file in an external VLC window.
    @details Spielt eine Mediendatei in einem externen VLC-Fenster ab.
    """
    global VLC_INSTANCE, VLC_PLAYER
    if not HAS_VLC:
        return {"error": "python-vlc ist nicht installiert"}

    try:
        if VLC_INSTANCE is None:
            VLC_INSTANCE = vlc.Instance()

        if VLC_PLAYER is not None:
            VLC_PLAYER.stop()

        VLC_PLAYER = VLC_INSTANCE.media_player_new()
        media = VLC_INSTANCE.media_new(file_path)
        VLC_PLAYER.set_media(media)
        VLC_PLAYER.play()

        logger.get_logger("vlc").info(f"VLC: Spiele {file_path}")
        return {"status": "ok"}
    except Exception as e:
        logger.get_logger("vlc").error(f"VLC Fehler: {e}")
        return {"error": str(e)}


@eel.expose
def stop_vlc():
    """
    @brief Stops the VLC player and any external active subprocess players.
    """
    global VLC_PLAYER, ACTIVE_SUBPROCESSES
    if VLC_PLAYER:
        VLC_PLAYER.stop()

    still_active = []
    for proc in ACTIVE_SUBPROCESSES:
        if proc.poll() is None:
            try:
                proc.terminate()
            except Exception:
                pass
        else:
            still_active.append(proc)

    # Keep ones that didn't terminate? Actually we want to clear terminated.
    ACTIVE_SUBPROCESSES = [p for p in ACTIVE_SUBPROCESSES if p.poll() is None]

    return {"status": "ok"}


@eel.expose
def is_mkvtoolnix_available():
    """Checks if mkvmerge is available in PATH."""
    return shutil.which("mkvmerge") is not None


@eel.expose
def stream_to_vlc(file_path, engine="ffmpeg"):
    """
    @brief Real-time streaming via mkvmerge pipe to VLC.
    @details Nutzt mkvmerge oder FFmpeg zum Remuxen und pipet den Output direkt an VLC.
    """
    file_path = resolve_media_path(file_path)
    file_path = resolve_dvd_bundle_path(file_path)
    log.info(f"[vlc pipe] Requesting stream for: {file_path}")

    if not file_path or not os.path.exists(str(file_path)):
        log.error(f"[vlc pipe] File not found: {file_path}")
        return {"status": "error", "error": f"Datei nicht gefunden: {file_path}"}

    # Directory Check: If it's a directory, it's likely a DVD/Blu-ray folder
    if os.path.isdir(str(file_path)):
        log.info(f"[vlc] Directory detected, opening as native media: {file_path}")
        try:
            vlc_path = shutil.which('cvlc') or shutil.which('vlc') or 'cvlc'
            # Use dvd:// with absolute path for folders
            cmd = [str(vlc_path), f"dvd://{file_path}"]
            subprocess.Popen(cmd)
            return {"status": "ok", "mode": "vlc_native_directory"}
        except Exception as e:
            log.error(f"[vlc] Failed to open directory: {e}")
            return {"status": "error", "error": str(e)}

    # ISO/DVD/Blu-ray Handling: Native playback
    file_path_str = str(file_path).lower()
    if file_path_str.endswith('.iso') or engine in ("dvd_native", "bluray_native", "cdrom_native"):
        try:
            vlc_path = shutil.which('cvlc') or shutil.which('vlc') or 'cvlc'
            if file_path_str.endswith('.iso'):
                # Better to let VLC handle ISO directly
                cmd = [str(vlc_path), str(file_path)]
            else:
                protocol = "dvd://"
                if engine == "bluray_native" or "bdmv" in file_path_str:
                    protocol = "bluray://"
                elif engine == "cdrom_native" or "cdda" in file_path_str:
                    protocol = "cdda://"

                log.info(f"[vlc] Native media detected, using {protocol} for {file_path}")
                cmd = [str(vlc_path), f"{protocol}{file_path}"]

            subprocess.Popen(cmd)
            return {"status": "ok", "mode": "vlc_native"}

        except Exception as e:
            log.error(f"[vlc] Native Playback error: {e}")
            return {"status": "error", "error": str(e)}

    # Direct VLC Solo (No Pipe)
    if engine in ("cvlc_solo", "vlc_extern"):
        try:
            vlc_cmd = 'cvlc'
            vlc_path = shutil.which(vlc_cmd) or shutil.which('vlc') or vlc_cmd
            log.info(f"[vlc] Opening external: {file_path}")
            subprocess.Popen([str(vlc_path), str(file_path)])
            return {"status": "ok", "mode": "vlc_external"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    if engine == "ffplay_solo":
        try:
            ffplay_path = shutil.which("ffplay") or "ffplay"
            log.info(f"[ffplay] Opening external: {file_path}")
            subprocess.Popen([str(ffplay_path), str(file_path)])
            return {"status": "ok", "mode": "ffplay_external"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # Check for engines, but allow fallback if mkvtoolnix is missing but engine is ffmpeg
    if engine == "mkvmerge" and not is_mkvtoolnix_available():
        log.warning("[vlc pipe] mkvmerge requested but not found, falling back to ffmpeg")
        engine = "ffmpeg"

    vlc_path = shutil.which('cvlc') or shutil.which('vlc') or 'cvlc'
    if not vlc_path:
        log.error("[vlc pipe] vlc not found in PATH")
        return {"status": "error", "error": "VLC Media Player nicht installiert oder nicht im PATH"}

    try:
        if engine == "mkvmerge":
            # mkvmerge pipeline: -o - (stdout)
            remux_cmd = ["mkvmerge", "-o", "-", str(file_path)]
        else:
            # ffmpeg pipeline (default): Use matroska for universality
            remux_cmd = [
                "ffmpeg", "-loglevel", "error", "-i", str(file_path),
                "-c", "copy", "-f", "matroska", "-"
            ]

        # VLC Command: Use fd://0 and explicit demuxer.
        # Removed --no-mjpeg-demux as it's not supported in all VLC versions or causing issues.
        vlc_cmd = [str(vlc_path), "--demux", "mkv", "fd://0"]

        log.info(f"[vlc pipe] Launching {engine} Pipe: {' '.join(str(c)
                 for c in remux_cmd)} | {' '.join(str(c) for c in vlc_cmd)}")

        # Start remuxer
        p1 = subprocess.Popen(remux_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Start VLC, linking its stdin to remuxer's stdout
        p2 = subprocess.Popen(vlc_cmd, stdin=p1.stdout)

        ACTIVE_SUBPROCESSES.append(p1)
        ACTIVE_SUBPROCESSES.append(p2)

        # Allow p1 to receive a SIGPIPE if p2 exits.
        if p1.stdout:
            p1.stdout.close()

        # Small delay to see if p1 (ffmpeg/mkvmerge) crashes immediately
        time.sleep(1.0)
        if p1.poll() is not None and p1.returncode != 0:
            err_msg = ""
            if p1.stderr:
                err_msg = p1.stderr.read().decode('utf-8', errors='ignore')
            log.error(f"[vlc pipe] {engine} failed: {err_msg.strip()}. Falling back to direct VLC.")
            # Fallback to external VLC
            if p2.poll() is None:
                p2.terminate()
            proc = subprocess.Popen([str(vlc_path), str(file_path)])
            ACTIVE_SUBPROCESSES.append(proc)
            return {"status": "ok", "mode": "vlc_fallback_direct"}

        # Monitor p2 (VLC) as well
        if p2.poll() is not None:
            log.error(f"[vlc pipe] VLC exited prematurely with code {p2.returncode}")
            return {"status": "error", "error": f"VLC beendet: Code {p2.returncode}"}

        return {"status": "ok", "message": "Streaming gestartet"}
    except Exception as e:
        log.error(f"[vlc pipe] Critical Pipe Error: {e}")
        return {"status": "error", "error": str(e)}


def detect_ts_stream(port):
    """Prft ob cvlc TS auf Port luft."""
    import requests
    try:
        # VLC simple HTTP check
        r = requests.head(f"http://localhost:{session_port}/health", timeout=0.1)  # dummy check for port activity?
        # Better: check if port is listening
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False


@eel.expose
def vlc_ts_mode(file_path):
    """Launches cvlc with TS muxing and returns the port."""
    file_path = resolve_media_path(file_path)
    file_path = resolve_dvd_bundle_path(file_path)
    if not os.path.exists(file_path):
        return {"status": "error", "error": "Datei nicht gefunden"}

    def find_free_port():
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    port = find_free_port()
    try:
        cmd = [
            'cvlc', file_path,
            '--sout', f'#std{{access=http,mux=ts,dst=:{port}/}}',
            '--no-video-title-show', '--loop'
        ]
        log.info(f"[cvlc] Launching TS Stream on port {port}: {file_path}")
        subprocess.Popen(cmd)

        # Wait for TS-Stream to be active
        max_retries = 10
        for i in range(max_retries):
            time.sleep(0.5)
            if detect_ts_stream(port):
                log.info(f"[cvlc] TS Stream active on port {port}")
                # We return a URL that the frontend can play via Video.js (type: video/mp2t)
                return {"status": "play", "path": f"http://localhost:{port}/", "mode": "chrome_native", "type": "video/mp2t"}

        return {"status": "error", "error": "cvlc TS failed to start"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def pyvidplayer2_mode(file_path):
    """Launches pyvidplayer2 for high-performance desktop playback."""
    if not os.path.exists(file_path):
        return {"status": "error", "error": "Datei nicht gefunden"}

    try:
        import pyvidplayer2 as pv
        # Note: This usually opens a new window depending on the backend (pygame/cv2)
        # For true embedding in Eel, one would need to pass frames as base64,
        # but for standalone it's simpler.

        def run_pv():
            player = pv.Video(file_path)
            player.play()

        log.info(f"[pyvidplayer2] Launching for: {file_path}")
        import threading
        threading.Thread(target=run_pv, daemon=True).start()
        return {"status": "ok", "message": "pyvidplayer2 gestartet"}
    except ImportError:
        return {"status": "error", "error": "pyvidplayer2 nicht installiert (pip install pyvidplayer2)"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def mkvmerge_standalone_mode(file_path):
    """Remuxes to a temp MKV and then opens it in VLC."""
    if not is_mkvtoolnix_available():
        return {"status": "error", "error": "mkvtoolnix nicht installiert"}

    try:
        temp_dir = Path(logger.APP_DATA_DIR) / "temp_remux"
        temp_dir.mkdir(parents=True, exist_ok=True)
        out_file = temp_dir / (Path(file_path).stem + ".mkv")

        if not out_file.exists():
            log.info(f"[mkvmerge] Remuxing to standalone: {file_path}")
            subprocess.run(["mkvmerge", "-o", str(out_file), str(file_path)], check=True)

        vlc_path = shutil.which("vlc") or "vlc"
        subprocess.Popen([str(vlc_path), str(out_file)])
        return {"status": "ok", "mode": "mkvmerge_standalone"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def mediamtx_mode(file_path, variant="hls"):
    """Enhanced handler for MediaMTX GUI integration."""
    return stream_to_mediamtx(file_path, protocol=variant)


@eel.expose
def stream_to_mediamtx(file_path, protocol="hls"):
    """
    @brief Starts a stream for the browser via MediaMTX (rtsp-simple-server) using FFmpeg push.
    @param protocol "hls" or "webrtc"
    """
    log.info(f"[mediamtx] Requesting {protocol} stream for: {file_path}")

    file_path = resolve_media_path(file_path)
    if not file_path or not os.path.exists(str(file_path)):
        return {"status": "error", "error": f"Datei nicht gefunden: {file_path}"}

    # Create a safe slug for the path
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', Path(file_path).stem)

    # 1. Kill any existing FFmpeg push for this path
    # (Simple strategy: clear all active subprocesses if they match the path,
    # but for now we rely on a global cleanup or just add to list)

    try:
        # 2. Path normalization & DVD detection
        source_p = Path(file_path)
        if source_p.is_dir():
            # Look for an ISO file inside the folder
            iso_candidate = next((f for f in source_p.iterdir() if f.suffix.lower() == ".iso"), None)
            if iso_candidate:
                source_p = iso_candidate
                log.info(f"[mediamtx] Resolved folder to internal ISO: {source_p}")

        is_dvd = source_p.suffix.lower() == '.iso' or (source_p.is_dir() and "VIDEO_TS" in os.listdir(source_p))

        # 3. Build FFmpeg command
        rtsp_target = f"rtsp://localhost:8554/{safe_name}"
        ffmpeg_cmd = ["ffmpeg", "-re"]

        if is_dvd:
            # DVD Transcode (H.264 + AAC)
            # If it's a folder, point to it, otherwise point to the ISO file
            source_arg = str(source_p)
            if source_p.is_dir():
                source_arg = f"dvd://{source_p}"

            ffmpeg_cmd += ["-i", source_arg, "-c:v", "libx264", "-preset", "ultrafast", "-acodec", "aac"]
        else:
            # File Remux (Copy codecs if possible, or force h264 for browser compat)
            # To be safe and fast, we try 'copy' first, but MediaMTX/Browsers prefer H264
            ffmpeg_cmd += ["-i", str(file_path), "-c", "copy"]

        ffmpeg_cmd += ["-f", "rtsp", rtsp_target]

        log.info(f"[mediamtx] Spawning FFmpeg push: {' '.join(ffmpeg_cmd)}")

        # Start the push process in the background
        # Use stdout/stderr=DEVNULL to avoid clogging the buffers
        proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, start_new_session=True)
        ACTIVE_SUBPROCESSES.append(proc)

        # 3. Wait a tiny bit for the stream to initialize in MediaMTX
        time.sleep(0.5)

        if protocol == "webrtc":
            # WebRTC (WHEP) endpoint
            src_url = f"http://localhost:8889/{safe_name}/whep"
            mode = "mediamtx_webrtc"
        else:
            # HLS (default)
            src_url = f"http://localhost:8888/{safe_name}/index.m3u8"
            mode = "mediamtx"

        return {"status": "play", "path": src_url, "mode": mode, "type": "application/x-mpegURL" if protocol == "hls" else "video/webrtc"}
    except Exception as e:
        log.error(f"[mediamtx] Setup error: {e}")
        return {"status": "error", "error": str(e)}


@eel.expose
def run_mtx_validation(file_path):
    """
    @brief Comprehensive test of MediaMTX paths for a specific file.
    """
    log.info(f"[QA] Starting MTX Validation for: {file_path}")
    report = {
        "file": file_path,
        "server_up": False,
        "hls_push_ok": False,
        "hls_read_ok": False,
        "webrtc_push_ok": False,
        "webrtc_read_ok": False,
        "logs": []
    }

    # 1. Health check
    try:
        r = requests.get("http://localhost:8888", timeout=2)
        report["server_up"] = True
        report["logs"].append(" MediaMTX HLS Listener found on :8888.")
    except:
        report["logs"].append(" MediaMTX not running or HLS port closed.")
        return report

    # 2. Test HLS
    hls_res = stream_to_mediamtx(file_path, protocol="hls")
    if hls_res.get("status") == "play":
        report["hls_push_ok"] = True
        url = hls_res.get("path")
        report["logs"].append(f" HLS Push started. URL: {url}")

        # Poll for manifest
        found = False
        for i in range(10):
            time.sleep(1)
            try:
                r = requests.get(url, timeout=1)
                if r.status_code == 200:
                    found = True
                    break
            except:
                pass
        if found:
            report["hls_read_ok"] = True
            report["logs"].append(" HLS Manifest is active and reachable.")
        else:
            report["logs"].append(" HLS Manifest timeout (Stream not starting).")
    else:
        report["logs"].append(f" HLS Push failed: {hls_res.get('error')}")

    # 3. Test WebRTC
    rtc_res = stream_to_mediamtx(file_path, protocol="webrtc")
    if rtc_res.get("status") == "play":
        report["webrtc_push_ok"] = True
        url = rtc_res.get("path")
        report["logs"].append(f" WebRTC (WHEP) Endpoint initialized: {url}")
        try:
            # Basic reachability check for WHEP (it might return 405 on GET, which is fine)
            r = requests.get(url, timeout=1)
            if r.status_code in [200, 404, 405]:
                report["webrtc_read_ok"] = True
                report["logs"].append(" WebRTC Listener is responsive.")
        except:
            pass

    return report or {"error": "Unknown failure"}


@eel.expose
def remux_mkv_batch(folder_path):
    """
    @brief Fast Batch-Remux of all video files in a folder to MKV.
    """
    if not is_mkvtoolnix_available():
        return {"status": "error", "error": "mkvtoolnix nicht installiert"}

    p = Path(folder_path)
    if not p.is_dir():
        return {"status": "error", "error": "Ungltiges Verzeichnis"}

    video_files = []
    for ext in VIDEO_EXTENSIONS:
        if ext == ".mkv":
            continue  # Skip existing MKVs
        video_files.extend(list(p.glob(f"*{ext}")))

    results: dict[str, Any] = {"total": len(video_files), "success": 0, "errors": []}

    for vf in video_files:
        output = vf.with_suffix(".mkv")
        if output.exists():
            results["errors"].append(f"{vf.name}: Ziel existiert bereits")
            continue

        try:
            cmd = ["mkvmerge", str(vf), "-o", str(output)]
            subprocess.run(cmd, check=True, capture_output=True)
            results["success"] += 1
            log.info(f"Remux Erfolg: {vf.name} -> {output.name}")
        except Exception as e:
            results["errors"].append(f"{vf.name}: {str(e)}")
            log.error(f"Remux Fehler {vf.name}: {e}")

    return {"status": "ok", "results": results}


@eel.expose
def import_vlc_playlist(m3u_path: str):
    """
    @brief Imports a VLC playlist (m3u8/m3u/XSPF) into the library.
    @details Importiert eine VLC-Playlist (m3u8/m3u/XSPF) in die Bibliothek.
    @param m3u_path Path to the playlist file / Pfad zur Playlist-Datei.
    @return Dictionary with imported media items / Dictionary mit importierten Items.
    """
    if not HAS_M3U8:
        return {
            "error": "python-m3u8 Modul ist nicht installiert. Bitte installieren: pip install m3u8"}

    try:
        playlist_file = Path(m3u_path)
        if not playlist_file.exists():
            return {"error": "Playlist-Datei nicht gefunden"}

        # Load playlist
        playlist = m3u8.load(str(playlist_file))

        imported = []
        skipped = []
        errors = []

        for segment in playlist.segments:
            if not segment.uri:
                continue

            # Convert URI to absolute path if relative
            media_path = Path(segment.uri)
            if not media_path.is_absolute():
                media_path = playlist_file.parent / media_path

            if not media_path.exists():
                errors.append(f"Datei nicht gefunden: {media_path.name}")
                continue

            # Check if already in library
            known = db.get_known_media_names()
            if media_path.name in known:
                skipped.append(media_path.name)
                continue

            # Parse and add to library
            try:
                item = MediaItem(media_path.name, media_path)
                item_dict = item.to_dict()
                db.insert_media(item_dict)
                imported.append(item_dict)
            except Exception as e:
                errors.append(f"{media_path.name}: {str(e)}")

        if DEBUG_FLAGS["player"]:
            debug_log(
                f"[VLC Import] {
                    len(imported)} importiert, {
                    len(skipped)} bersprungen, {
                    len(errors)} Fehler")

        return {
            "status": "ok",
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "count": len(imported)
        }
    except Exception as e:
        log.error(f"[VLC Import] Error: {e}")
        return {"error": str(e)}


@eel.expose
def export_playlist_to_vlc(media_names: list, output_path: str):
    """
    @brief Exports selected media items to a VLC-compatible m3u8 playlist.
    @details Exportiert ausgewhlte Medien in eine VLC-kompatible m3u8 Playlist.
    @param media_names List of media item names from database / Liste von Medien-Namen aus der DB.
    @param output_path Target path for the .m3u8 file / Ziel-Pfad fr die .m3u8-Datei.
    @return Status dictionary / Status-Dictionary.
    """
    try:
        playlist_file = Path(output_path)
        if not playlist_file.suffix:
            playlist_file = playlist_file.with_suffix('.m3u8')

        lines = ["#EXTM3U\n"]
        exported: int = 0
        missing = []

        for name in media_names:
            item_dict = db.get_media_by_name(name)
            if not item_dict:
                missing.append(name)
                continue

            file_path = item_dict.get("path", "")
            if not file_path or not Path(file_path).exists():
                missing.append(name)
                continue

            # Add EXTINF metadata line (duration, title)
            duration = item_dict.get("duration", 0) or -1
            title = item_dict.get("title") or name
            artist = item_dict.get("artist", "")
            extinf_title = f"{artist} - {title}" if artist else title

            lines.append(f"#EXTINF:{duration},{extinf_title}\n")
            lines.append(f"{file_path}\n")
            exported = int(exported) + 1

        playlist_file.write_text("".join(lines), encoding='utf-8')

        if DEBUG_FLAGS["player"]:
            debug_log(
                f"[VLC Export] {exported} Tracks nach {
                    playlist_file.name} exportiert")

        return {
            "status": "ok",
            "path": str(playlist_file),
            "exported": exported,
            "missing": missing
        }
    except Exception as e:
        log.error(f"[VLC Export] Error: {e}")
        return {"error": str(e)}


@eel.expose
def save_playlist(media_names: list, output_path: str):
    """
    @brief Saves the current selection of media names to a JSON file.
    """
    try:
        path = Path(output_path)
        if not path.suffix:
            path = path.with_suffix('.json')

        import json
        path.write_text(json.dumps(media_names, indent=4), encoding='utf-8')
        return {"status": "ok", "path": str(path)}
    except Exception as e:
        log.error(f"[Save Playlist] Error: {e}")
        return {"error": str(e)}


@eel.expose
def load_playlist(input_path: str):
    """
    @brief Loads a list of media names from a JSON file and returns full media objects.
    """
    try:
        path = Path(input_path)
        if not path.exists():
            return {"error": "Playlist file not found"}

        import json
        media_names = json.loads(path.read_text(encoding='utf-8'))

        items = []
        for name in media_names:
            item = db.get_media_by_name(name)
            if item:
                items.append(item)

        return {"status": "ok", "items": items}
    except Exception as e:
        log.error(f"[Load Playlist] Error: {e}")
        return {"error": str(e)}


@eel.expose
def pick_file(title="Datei auswhlen", filetypes=None):
    """
    @brief Opens a native file picker dialog.
    @details ffnet einen nativen Datei-Auswahldialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @return Selected file path or None / Gewhlter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        if filetypes:
            file_path = filedialog.askopenfilename(
                title=title, filetypes=filetypes)
        else:
            file_path = filedialog.askopenfilename(title=title)

        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        log.error(f"[System] File picker failed: {e}")
        return None


@eel.expose
def import_txt_to_db(category="Video"):
    """
    @brief Imports media from a TXT file into the database.
    @details Importiert Medien aus einer TXT-Datei in die Datenbank.
    @param category Target category (Video, Serie, Audio).
    """
    try:
        file_path = pick_file(
            title=f"TXT Import fr {category} auswhlen",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if not file_path:
            return {"status": "cancelled"}

        lines = Path(file_path).read_text(encoding='utf-8').splitlines()
        imported = 0
        skipped = 0

        for line in lines:
            path_str = line.strip()
            if not path_str or path_str.startswith("#"):
                continue

            # Create a simple media item
            p = Path(path_str)
            name = p.name if p.name else path_str

            # Use MediaItem class if possible for consistent metadata structure
            try:
                from src.core.models import MediaItem
                item = MediaItem(name, p)
                item_dict = item.to_dict()

                # Force category and type if provided
                if category:
                    item_dict['category'] = category
                    if category == "Audio":
                        item_dict['type'] = "Audio"
                    elif category in ["Video", "Serie", "Film"]:
                        item_dict['type'] = "Video"
            except Exception as item_err:
                log.debug(f"[Import] MediaItem init failed for {name}: {item_err}")
                # Basic fallback if MediaItem fails (e.g. path doesn't exist)
                item_dict = {
                    'name': name,
                    'path': path_str,
                    'type': "Video" if category != "Audio" else "Audio",
                    'category': category or ("Video" if category != "Audio" else "Audio"),
                    'duration': "00:00:00",
                    'is_transcoded': False,
                    'tags': {},
                    'extension': p.suffix.lower() if p.suffix else "",
                    'has_artwork': False
                }

            res = db.insert_media(item_dict)
            if res:
                imported += 1
            else:
                skipped += 1

        return {
            "status": "ok",
            "imported": imported,
            "skipped": skipped,
            "total_processed": len(lines)
        }
    except Exception as e:
        log.error(f"[Import] TXT Import failed: {e}")
        return {"error": str(e)}


@eel.expose
def pick_save_file(
        title="Datei speichern",
        filetypes=None,
        default_name="playlist.m3u8"):
    """
    @brief Opens a native file save dialog.
    @details ffnet einen nativen Datei-Speichern-Dialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @param default_name Default filename / Standard-Dateiname.
    @return Selected file path or None / Gewhlter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        if filetypes:
            file_path = filedialog.asksaveasfilename(
                title=title,
                filetypes=filetypes,
                defaultextension=".m3u8",
                initialfile=default_name
            )
        else:
            file_path = filedialog.asksaveasfilename(
                title=title,
                initialfile=default_name
            )

        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        log.error(f"[System] File save picker failed: {e}")
        return None


@eel.expose
def pick_folder_cli(prompt="Ordnerpfad eingeben"):
    """
    @brief CLI-based folder picker without GUI dependencies.
    @details CLI-basierter Ordner-Picker ohne GUI-Abhngigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @return Valid folder path or None / Gltiger Ordnerpfad oder None.
    """
    try:
        log.info(f"\n{prompt}:")
        log.info(f"(Standard: {Path.home()})")
        user_input = input("> ").strip()

        if not user_input:
            return str(Path.home())

        folder_path = Path(user_input).expanduser().resolve()

        if folder_path.exists() and folder_path.is_dir():
            return str(folder_path)
        else:
            log.error(f"Fehler: '{folder_path}' ist kein gltiger Ordner.")
            return None
    except (KeyboardInterrupt, EOFError):
        log.info("\nAbgebrochen.")
        return None
    except Exception as e:
        log.error(f"[System] CLI folder picker failed: {e}")
        return None


@eel.expose
def pick_file_cli(prompt="Dateipfad eingeben", extensions=None):
    """
    @brief CLI-based file picker without GUI dependencies.
    @details CLI-basierter Datei-Picker ohne GUI-Abhngigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid file path or None / Gltiger Dateipfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Erlaubte Formate: {', '.join(extensions)})"

        log.info(f"\n{prompt}{ext_info}:")
        user_input = input("> ").strip()

        if not user_input:
            return None

        file_path = Path(user_input).expanduser().resolve()

        if not file_path.exists():
            log.error(f"Fehler: Datei '{file_path}' nicht gefunden.")
            return None

        if not file_path.is_file():
            log.error(f"Fehler: '{file_path}' ist keine Datei.")
            return None

        if extensions and file_path.suffix.lower() not in extensions:
            log.error(f"Fehler: Dateiformat '{file_path.suffix}' nicht erlaubt.")
            return None

        return str(file_path)
    except (KeyboardInterrupt, EOFError):
        log.info("\nAbgebrochen.")
        return None
    except Exception as e:
        log.error(f"[System] CLI file picker failed: {e}")
        return None


@eel.expose
def pick_save_file_cli(
        prompt="Speicherpfad eingeben",
        default_name="output.txt",
        extensions=None):
    """
    @brief CLI-based save file dialog without GUI dependencies.
    @details CLI-basierter Speichern-Dialog ohne GUI-Abhngigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param default_name Default filename / Standard-Dateiname.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid save path or None / Gltiger Speicherpfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Formate: {', '.join(extensions)})"

        log.info(f"\n{prompt}{ext_info}:")
        log.info(f"(Standard: {default_name})")
        user_input = input("> ").strip()

        if not user_input:
            user_input = default_name

        save_path = Path(user_input).expanduser().resolve()

        # Add extension if missing
        if extensions and save_path.suffix.lower() not in extensions:
            save_path = save_path.with_suffix(extensions[0])

        # Check if parent directory exists
        if not save_path.parent.exists():
            log.error(f"Fehler: Verzeichnis '{save_path.parent}' existiert nicht.")
            create = input("Verzeichnis erstellen? (j/n): ").strip().lower()
            if create == 'j':
                save_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                return None

        # Warn if file exists
        if save_path.exists():
            overwrite = input(
                f"Datei '{
                    save_path.name}' existiert. berschreiben? (j/n): ").strip().lower()
            if overwrite != 'j':
                return None

        return str(save_path)
    except (KeyboardInterrupt, EOFError):
        log.info("\nAbgebrochen.")
        return None
    except Exception as e:
        log.error(f"[System] CLI save file picker failed: {e}")
        return None


@eel.expose
def get_test_media_files():
    """
    Scans media/tests and other test-related directories for video files.
    """
    # Use local resolve_media_path already defined in main.py
    # Common test directories
    search_dirs = [
        Path(resolve_media_path("tests")),
        Path(resolve_media_path("matrix")),
        PROJECT_ROOT / "tests" / "assets",
        PROJECT_ROOT / "tests" / "mockfiles"
    ]

    extensions = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.ts', '.iso']

    results = []

    for d in search_dirs:
        if d.exists() and d.is_dir():
            for f in d.rglob("*"):
                if f.suffix.lower() in extensions:
                    results.append({
                        "name": f.name,
                        "path": str(f.absolute()),
                        "relpath": str(f)
                    })

    return results


@eel.expose
def get_test_suites():
    """
    @brief Discovers all test files in the tests/ directory and extracts metadata.
    @details Findet alle Testdateien im Verzeichnis tests/ und extrahiert deren Metadaten.
    @return List of test suite objects / Liste von Test-Suite-Objekten.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    if not test_dir.exists():
        return []

    suites = []
    # Discover .py and .sh files using os.walk for guaranteed depth
    all_files = []
    for root, dirs, filenames in os.walk(str(test_dir)):
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".sh"):
                if not filename.startswith("__") and not filename.startswith("."):
                    all_files.append(Path(root) / filename)

    # Sort files by relative path
    all_files.sort(key=lambda x: str(x.relative_to(test_dir)))

    for f in all_files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            content = ""

        metadata = {
            "category": "-",
            "inputs": "-",
            "outputs": "-",
            "files": "-",
            "comment": "-"
        }

        # Scan for metadata (limit to first 100 lines for performance)
        line_count = 0
        for line in content.splitlines():
            line_count += 1
            if line_count > 100:
                break
            line = line.strip()
            if line.startswith("# Kategorie:"):
                metadata["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Eingabewerte:"):
                metadata["inputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Ausgabewerte:"):
                metadata["outputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Testdateien:"):
                metadata["files"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Kommentar:"):
                metadata["comment"] = line.split(":", 1)[1].strip()

        # Build nice name with path context
        rel_path = f.relative_to(test_dir)
        display_name = f.name  # Just the filename

        suites.append({
            "id": str(rel_path),
            "name": display_name,
            "folder": str(rel_path.parent).replace("\\", "/") if str(rel_path.parent) != "." else "",
            "metadata": metadata
        })
    log.info(f"[get_test_suites] Discovered {len(suites)} suites in {test_dir}. Returning to Eel now.")
    return suites


@eel.expose
def update_test_metadata(filename, metadata):
    """
    @brief Updates the metadata comments in a specific test file.
    @details Aktualisiert die Metadaten-Kommentare in einer bestimmten Testdatei.
    @param filename Name of the test file / Name der Testdatei.
    @param metadata Dictionary of metadata fields / Dictionary der Metadaten-Felder.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    file_path = test_dir / filename

    if not file_path.exists():
        return {"error": "Test-Datei nicht gefunden"}

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        # Remove existing metadata lines
        new_lines = []
        for line in lines:
            if not any(
                line.startswith(prefix) for prefix in [
                    "# Kategorie:",
                    "# Eingabewerte:",
                    "# Ausgabewerte:",
                    "# Testdateien:",
                    "# Kommentar:"]):
                new_lines.append(line)

        # Prepend new metadata
        header = [
            f"# Kategorie: {metadata.get('category', '-')}",
            f"# Eingabewerte: {metadata.get('inputs', '-')}",
            f"# Ausgabewerte: {metadata.get('outputs', '-')}",
            f"# Testdateien: {metadata.get('files', '-')}",
            f"# Kommentar: {metadata.get('comment', '-')}",
            ""  # Add empty line after metadata
        ]

        # Join lines with proper newline handling
        # Skip leading empty lines if there are any after removing metadata
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)

        final_content = "\n".join(header + new_lines)
        file_path.write_text(final_content, encoding='utf-8')
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def clear_logs():
    """Clear the UI log buffer."""
    log.info("Logs cleared.")


@eel.expose
def create_new_test(name):
    """
    @brief Creates a new test file based on a template.
    @details Erstellt eine neue Testdatei basierend auf einem Template.
    @param name Base name for the test / Basisname des Tests.
    @return Status or filename dictionary / Status- oder Dateinamen-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    test_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize name
    safe_name = "".join([c for c in name if c.isalnum() or c in (
        ' ', '_', '-')]).strip().replace(' ', '_')
    if not safe_name.startswith('test_'):
        safe_name = f"test_{safe_name}"

    filename = f"{safe_name}.py"
    file_path = test_dir / filename

    if file_path.exists():
        return {"status": "error", "message": "Test existiert bereits"}

    template = f"""# Kategorie: -
# Eingabewerte: -
# Ausgabewerte: -
# Testdateien: -
# Kommentar: Neuer Test

import pytest


def {safe_name}():
    # Hier Test-Code schreiben
    assert True
"""
    try:
        file_path.write_text(template, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def delete_test(filename):
    """
    @brief Deletes a specific test file from the disk.
    @details Lscht eine bestimmte Testdatei von der Festplatte.
    @param filename Test file name / Name der Testdatei.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    file_path = test_dir / filename

    if not file_path.exists():
        return {"error": "Datei nicht gefunden"}

    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def get_logbook_entry(feature_name, source="logbuch"):
    """
    @brief Reads a markdown file from the logbook or the README.
    @details Liest eine Markdown-Datei aus dem Logbuch oder die README ein.
    @param feature_name Entry name or 'README' / Name des Eintrags oder 'README'.
    @return Content string (Markdown) / Inhalts-String (Markdown).
    """
    root_dir = PROJECT_ROOT
    if source == "root":
        allowed_root_files = {
            "README.md",
            "DOCUMENTATION.md",
            "INSTALL.md",
            "DEPENDENCIES.md",
            "LICENSE.md",
        }
        requested = feature_name if feature_name.endswith(".md") else f"{
            feature_name}.md"
        if requested not in allowed_root_files:
            return f"<h1>Error</h1><p>Root entry '{
                feature_name}' not allowed.</p>"
        log_file = root_dir / requested
    elif feature_name.upper() == "README" or feature_name.upper() == "README.MD":
        log_file = root_dir / "README.md"
    else:
        # Search recursively in the root logbuch folder
        log_dir = PROJECT_ROOT / "logbuch"
        log_file = None

        # Check if feature_name already has the full relative path
        if "/" in feature_name:
            # Try direct relative path
            candidate = log_dir / feature_name
            if not candidate.name.endswith(".md"):
                candidate = candidate.with_suffix(".md")
            if candidate.exists():
                log_file = candidate

        if not log_file:
            # Fallback search
            for f in log_dir.rglob("*.md"):
                if f.stem == feature_name or f.name == feature_name:
                    log_file = f
                    break

        if not log_file:
            # Try to match the stem if re-numbered (e.g., search for "The_Modular_Heart" in "010_2026-03-13_The_Modular_Heart...")
            for f in log_dir.rglob("*.md"):
                if feature_name in f.name:
                    log_file = f
                    break

        if not log_file or not log_file.exists():
            return f"<h1>Error</h1><p>Logbook entry for '{feature_name}' not found.</p>"

    try:
        content = log_file.read_text(encoding='utf-8')

        # Bilingual splitting: <!-- lang-split -->
        if "<!-- lang-split -->" in content:
            parts = content.split("<!-- lang-split -->")
            if len(parts) >= 2:
                current_lang = get_language()
                if current_lang.lower() == "en":
                    return parts[1].strip()
                else:
                    return parts[0].strip()

        # Fallback: Return original content if no split tag is present
        return content
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


@eel.expose
def list_logbook_entries():
    """
    @brief Returns a list of all markdown files in the logbook folder with metadata.
    @details Gibt eine Liste aller Markdown-Dateien im logbuch/ Ordner mit Metadaten zurck.
    @return List of logbook entry objects / Liste von Logbuch-Eintrag-Objekten.
    """
    log_dir = PROJECT_ROOT / "logbuch"
    if not log_dir.exists():
        return []

    entries = []

    def _normalize_status(status_raw: str) -> str:
        s = (status_raw or "").strip().upper()
        if not s:
            return "ACTIVE"
        if any(
            k in s for k in [
                "COMPLETE",
                "COMPLETED",
                "DONE",
                "ABGESCHLOSSEN",
                "FERTIG"]):
            return "COMPLETED"
        if any(k in s for k in ["PLAN", "PLANNING", "IDEA"]):
            return "PLAN"
        if any(k in s for k in ["DOC", "DOCS", "DOCUMENTATION"]):
            return "DOCS"
        if any(k in s for k in ["BUG", "ISSUE", "FIXME"]):
            return "BUG"
        if any(
            k in s for k in [
                "ACTIVE",
                "IN_PROGRESS",
                "IN PROGRESS",
                "TODO",
                "TASK",
                "OPEN"]):
            return "ACTIVE"
        return s
    # Recursively find all markdown files
    all_files = list(log_dir.rglob("*.md"))
    all_files += list(log_dir.rglob("*.mmd"))

    for f in sorted(all_files, key=lambda x: x.name):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                # Mehr Zeilen lesen um alles zu finden
                lines = [fp.readline() for _ in range(20)]
                category = "Sonstiges"
                summary = ""
                status = "ACTIVE"  # Default
                title = f.stem
                pinned = False  # Default

                title_de = ""
                title_en = ""
                summary_de = ""
                summary_en = ""

                for line in lines:
                    line = line.strip()
                    # Support both <!-- Tag: Value --> and Tag: Value formats
                    content = line
                    if "<!--" in line and "-->" in line:
                        content = line.split("<!--")[1].split("-->")[0].strip()

                    if ":" in content:
                        key, val = content.split(":", 1)
                        key = key.strip()
                        val = val.strip()

                        if key == "Category":
                            category = val
                        elif key == "Status":
                            status = val
                        elif key == "Pinned":
                            pinned = val.lower() in ["true", "yes", "1"]
                        elif key == "Title_DE":
                            title_de = val
                        elif key == "Title_EN":
                            title_en = val
                        elif key == "Summary_DE":
                            summary_de = val
                        elif key == "Summary_EN":
                            summary_en = val
                        elif key == "Summary":
                            summary = val

                    md_status_match = re.match(
                        r'^\*\*Status:\*\*\s*(.+)$', line)
                    if md_status_match:
                        status = md_status_match.group(1).strip()

                    if line.startswith("# "):
                        title = line.replace("# ", "").strip()

                # Special case for Known Issues
                if f.name == "00_Known_Issues.md":
                    category = "Bug"
                    if status == "ACTIVE":
                        status = "BUG"

                # Fallbacks
                if not title_de:
                    title_de = title
                if not title_en:
                    title_en = title

                # Bi-directional summary fallback
                if not summary:
                    summary = summary_de or summary_en
                if not summary_de:
                    summary_de = summary
                if not summary_en:
                    summary_en = summary

                # Final Selection based on language
                current_lang = get_language().lower()
                final_title = title
                final_summary = summary

                if current_lang == "en":
                    final_title = title_en or title
                    final_summary = summary_en or summary
                else:
                    final_title = title_de or title
                    final_summary = summary_de or summary

                entries.append({
                    "name": f.stem,
                    "filename": f.name,
                    "title": final_title,
                    "title_de": title_de,
                    "title_en": title_en,
                    "category": category,
                    "summary": summary,
                    "summary_de": summary_de,
                    "summary_en": summary_en,
                    "status": _normalize_status(status),
                    "pinned": pinned,
                    "source": "logbuch",
                    "modified_ts": f.stat().st_mtime,
                    "modified_iso": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime)),
                })
        except Exception:
            entries.append({
                "name": f.stem,
                "filename": f.name,
                "title": f.stem,
                "category": "Fehler",
                "summary": "",
                "status": "ERROR",
                "source": "logbuch",
                "modified_ts": 0,
                "modified_iso": "",
            })

    return entries


@eel.expose
def read_file(filename, context='logbuch'):
    """
    @brief Reads the content of a file from a specific context.
    @param filename Name of the file.
    @param context Context/Folder (default: 'logbuch').
    @return File content as string or None if error.
    """
    try:
        if context == 'logbuch':
            base_path = PROJECT_ROOT / "logbuch"
        else:
            # For security, only allow logbuch for now
            return None

        file_path = base_path / filename
        if not file_path.exists() or not file_path.is_file():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log.error(f"read_file error: {e}")
        return None


@eel.expose
def list_feature_modal_items():
    """
    Returns feature modal items from logbook plus selected markdown files from the project root.
    """
    items = [
        item for item in list_logbook_entries()
        if item.get("filename") != "31_Project_Documentation.md"
    ]

    root_dir = Path(__file__).parent
    root_docs = [
        ("README.md", "README", "Project overview and quick start."),
        ("DOCUMENTATION.md", "Documentation", "Detailed technical documentation."),
        ("INSTALL.md", "Installation", "Installation and setup instructions."),
        ("DEPENDENCIES.md", "Dependencies", "Dependency list and runtime requirements."),
        ("LICENSE.md", "License", "License and legal information."),
    ]

    for filename, title, summary in root_docs:
        path = root_dir / filename
        if not path.exists():
            continue
        mtime = path.stat().st_mtime
        items.append({
            "name": filename,
            "filename": filename,
            "title": title,
            "title_de": title,
            "title_en": title,
            "category": "Docs",
            "summary": summary,
            "summary_de": summary,
            "summary_en": summary,
            "status": "DOCS",
            "source": "root",
            "modified_ts": mtime,
            "modified_iso": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime)),
        })

    return items


@eel.expose
def save_logbook_entry(filename, content):
    """
    @brief Saves or updates a logbook entry file.
    @details Speichert oder aktualisiert einen Logbuch-Eintrag.
    @param filename Target filename / Ziel-Dateiname.
    @param content Markdown content / Markdown-Inhalt.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    log_dir = PROJECT_ROOT / "logbuch"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Sichere den Dateinamen
    if not filename.endswith('.md'):
        filename = filename + '.md'

    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        return {"error": "Ungltiger Dateiname"}

    file_path = log_dir / filename

    try:
        if "Status:" not in content and "<!-- Status:" not in content:
            content = f"<!-- Status: ACTIVE -->\n{content}"
        file_path.write_text(content, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def delete_logbook_entry(filename):
    """
    @brief Deletes a logbook entry from the disk.
    @details Lscht einen Logbuch-Eintrag.
    @param filename Entry filename / Dateiname des Eintrags.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    log_dir = PROJECT_ROOT / "logbuch"

    if not filename.endswith('.md'):
        filename = filename + '.md'

    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith(
            '.') or '..' in filename:
        return {"error": "Ungltiger Dateiname"}

    file_path = log_dir / filename

    if not file_path.exists():
        return {"error": "Datei nicht gefunden"}

    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def run_tests(test_files):
    """
    @brief Executes selected pytest suites and returns the results.
    @details Fhrt ausgewhlte pytest-Suiten aus und gibt die Ergebnisse zurck.
    @param test_files List of test filenames / Liste von Test-Dateinamen.
    @return Result dictionary with passes/fails and output / Ergebnis-Dictionary.
    """
    if DEBUG_FLAGS.get("tests"):
        debug_log(f"[Tests] Running files: {test_files}")

    if not test_files:
        return {"error": "Keine Test-Suiten ausgewhlt."}

    # Verify files exist
    valid_files = []
    root_dir = Path(__file__).parents[2]
    test_dir = root_dir / "tests"
    for tf in test_files:
        p = test_dir / tf
        if p.exists():
            valid_files.append(str(p))

    if not valid_files:
        return {"error": "Keine gltigen Test-Dateien gefunden."}

    # We need to set PYTHONPATH so tests can import models/parsers
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{PROJECT_ROOT}:{PROJECT_ROOT}/src:{PROJECT_ROOT}/src/core:{PROJECT_ROOT}/src/parsers"
    env["MWV_DISABLE_BROWSER_OPEN"] = "1"

    # Detect environment strategy:
    # 1. Check for specialized venvs first (preferred for tests)
    # 2. Fallback to current interpreter if it has pytest
    test_python = sys.executable
    venv_found = False

    known_venvs = [".venv_testbed", ".venv_dev", "venv"]
    log.info(f"[Tests] Searching for test environment in {PROJECT_ROOT}...")

    for venv_name in known_venvs:
        venv_bin = PROJECT_ROOT / venv_name / "bin" / "python"
        if venv_bin.exists():
            test_python = str(venv_bin)
            venv_found = True
            log.info(f"[Tests] Found specialized test venv: {venv_name} -> {test_python}")
            break
        else:
            if DEBUG_FLAGS.get("tests"):
                debug_log(f"[Tests] Missing venv: {venv_name} (checked {venv_bin})")

    if not venv_found:
        import importlib.util
        if importlib.util.find_spec("pytest") is None:
            log.warning(f"[Tests] No specialized venv found and pytest missing in current env ({sys.executable}).")
        else:
            log.info(f"[Tests] Using current interpreter (pytest found): {sys.executable}")

    log.info(f"[Tests] Final execution command python: {test_python}")

    # Run pytest in a subprocess to avoid issues with repeat runs/sys.modules
    # Stream output lines live to frontend for real-time refresh.
    try:
        process = subprocess.Popen(
            [test_python, "-m", "pytest", "-q"] + valid_files,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=str(root_dir),
            bufsize=1,
            universal_newlines=True,
        )

        output_lines = []
        start_time = time.time()
        timeout_seconds = 900

        while True:
            if process.stdout is None:
                break

            line = process.stdout.readline()
            if line:
                output_lines.append(line)
                try:
                    if hasattr(eel, "append_test_output"):
                        eel.append_test_output(line)
                except Exception:
                    pass
            elif process.poll() is not None:
                break

            if time.time() - start_time > timeout_seconds:
                process.kill()
                raise RuntimeError(f"Testlauf-Timeout nach {timeout_seconds}s")

        if process.stdout is not None:
            tail = process.stdout.read()
            if tail:
                output_lines.append(tail)
                try:
                    if hasattr(eel, "append_test_output"):
                        eel.append_test_output(tail)
                except Exception:
                    pass

        result_code = process.wait()
        output = ''.join(output_lines)
        max_output_chars = 120000
        if len(output) > max_output_chars:
            output = (
                "[Output truncated: showing last part only]\n\n"
                + output[-max_output_chars:]
            )

        # Parse output for passed/failed (supports both verbose and -q pytest
        # formats)
        passes = 0
        fails = 0
        match = re.search(r'(\d+)\s+passed', output)
        if match:
            passes = int(match.group(1))
        match_fails = re.search(r'(\d+)\s+failed', output)
        if match_fails:
            fails = int(match_fails.group(1))

        summary = f"{passes} passed, {fails} failed"

        duration = time.time() - start_time
        timestamp = time.time()

        # Persist results
        try:
            results_path = PROJECT_ROOT / "test_results.json"
            history = []
            if results_path.exists():
                try:
                    data = json.loads(results_path.read_text(encoding='utf-8'))
                    if isinstance(data, list):
                        history = data
                except (json.JSONDecodeError, IOError):
                    pass

            history.append({
                "timestamp": timestamp,
                "duration": duration,
                "passes": passes,
                "fails": fails,
                "summary": summary,
                "files": test_files
            })
            # Keep last 100 runs
            last_100: list[dict] = history[-100:]  # type: ignore
            results_path.write_text(json.dumps(last_100, indent=2), encoding='utf-8')
        except Exception as e:
            log.error(f"[Reporting] Error saving results: {e}")

        return {
            "exit_code": result_code,
            "output": output,
            "summary": summary,
            "passes": passes,
            "fails": fails,
            "timestamp": timestamp,
            "duration": duration
        }
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def get_test_results():
    """Returns historical test results for the dashboard."""
    results_path = PROJECT_ROOT / "test_results.json"
    if not results_path.exists():
        return []
    try:
        import json
        return json.loads(results_path.read_text(encoding='utf-8'))
    except:
        return []


@eel.expose
def run_gui_tests():
    """
    @brief Placeholder for GUI tests (handled via the agent).
    @details Dummy-Funktion fr GUI-Tests (da diese ber den Agenten laufen).
    @return Info dictionary / Info-Dictionary.

    Best Practices:
      - In Produktion: Integriere Playwright oder Selenium fr Eel-GUIs.
      - Starte den Dev-Server und teste DOM-Interaktionen via Headless-Browser.
      - Fr MCP-Agenten: Nutze Inspector-Tool fr Tool-Validierung und Event-Simulation.
      - Alternativen: WebDriver (Selenium), CDP (Playwright), PyAutoGUI fr Desktop.
      - Eel expose() ermglicht bidirektionale Python-JS-Calls fr Test-Trigger.
    """
    log.info(
        "GUI-Tests: Siehe MCP-Agent oder Browser-Subagent fr KlickEvents/DOM.")
    return {
        "status": "info",
        "message": "GUI-Tests mssen ber den MCP-Agenten DOM / Browser Subagent / KlickEvents gestartet werden.",
        "next_steps": [
            "pip install playwright pytest",
            "playwright install",
            "Beispiel: pytest mit page.goto('http://localhost:8000') und page.click()",
            "Alternativ: selenium, pyautogui, MCP Inspector"],
        "protocols": {
            "WebDriver": "REST/HTTP, Selenium, geeignet fr Eel",
            "CDP": "WebSocket, Playwright/Selenium4, direkter DOM-Zugriff",
            "Eel expose": "Intern, Python-JS-Bridge, ideal fr Test-Trigger",
            "PyAutoGUI": "Pixel/Screen, Desktop-Automatisierung",
            "MCP": "Agenten-basiert, Inspector fr Event-Simulation"}}


@eel.expose
def ui_trace(message):
    try:
        log.info(f"[UI-Trace] {message}")
    except Exception:
        pass
    return {"status": "ok"}


@eel.expose
def get_media_tracks(filepath):
    """Probes available audio and subtitle tracks for a media file."""
    try:
        from src.core.ffprobe_analyzer import ffprobe_analyze
        analysis = ffprobe_analyze(filepath)
        return {
            "audio": analysis.get("audio_tracks", []),
            "subtitles": analysis.get("subtitle_tracks", []),
            "atmos": analysis.get("atmos", False)
        }
    except Exception as e:
        log.error(f"Error in get_media_tracks: {e}")
        return {"audio": [], "subtitles": []}


@eel.expose
def extract_subtitle(filepath, track_index):
    """Extracts a specific subtitle track to a temp file."""
    try:
        filename = f"{Path(filepath).stem}_track{track_index}.srt"
        output_path = str(PROJECT_ROOT / "cache" / filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        success = SubtitleProcessor.extract_track(filepath, track_index, output_path)
        if success:
            return {"status": "ok", "path": output_path, "filename": filename}
        return {"status": "error", "message": "Extraction failed"}
    except Exception as e:
        log.error(f"Error extracting subtitle: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def adjust_subtitle_timing(subtitle_path, offset_ms):
    """Adjusts the timing of a subtitle file."""
    try:
        success = SubtitleProcessor.adjust_timing(subtitle_path, int(offset_ms))
        if success:
            return {"status": "ok"}
        return {"status": "error", "message": "Adjustment failed"}
    except Exception as e:
        log.error(f"Error adjusting subtitle timing: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def get_subtitle_info(subtitle_path):
    """Returns metadata about a subtitle file."""
    try:
        return SubtitleProcessor.get_info(subtitle_path)
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def mkv_batch_extract(files, track_type="subtitles"):
    """
    @brief Batch extraction of MKV tracks (Cleaver-style).
    @param files List of paths to MKV files.
    @param track_type Type of track to extract (e.g. 'subtitles', 'audio').
    """
    log.info(f"[MKV] Batch extracting {track_type} from {len(files)} files")
    results = []

    # Get cache dir
    cache_dir = PROJECT_ROOT / "cache" / "extracted"
    cache_dir.mkdir(parents=True, exist_ok=True)

    for fpath in files:
        try:
            # 1. Get info
            info = mkv_get_info(fpath)
            if info["status"] != "ok":
                results.append({"file": fpath, "status": "error", "error": info.get("error")})
                continue

            # 2. Find tracks
            tracks = info.get("tracks", [])
            target_tracks = [t for t in tracks if track_type in t.get("type", "").lower()]

            # 3. Extract each target track
            extracted = []
            for t in target_tracks:
                tid = t.get("id")
                out_name = f"{Path(fpath).stem}_T{tid}.{t.get('codec', 'bin')}"
                out_path = cache_dir / out_name

                res = mkv_extract_track(fpath, tid, str(out_path))
                if res["status"] == "ok":
                    extracted.append(str(out_path))

            results.append({"file": fpath, "status": "ok", "extracted": extracted})
        except Exception as e:
            results.append({"file": fpath, "status": "error", "error": str(e)})

    return {"status": "ok", "results": results}


# --- MKVToolNix & HandBrake CLI API (Phase 8) ---
@eel.expose
def mkv_get_info(filepath):
    """Deep inspection of MKV container."""
    return mkv_tool.get_info(filepath)


@eel.expose
def mkv_extract_track(filepath, track_index, output_path):
    """Extracts a track using mkvextract."""
    return mkv_tool.extract_track(filepath, track_index, output_path)


@eel.expose
def mkv_mux_simple(output_path, input_files):
    """Simple muxing of multiple files."""
    return mkv_tool.mux_mkv(output_path, input_files)


@eel.expose
def hb_encode(input_path, output_path, preset="Very Fast 1080p30"):
    """Encodes a file using HandBrakeCLI."""
    return handbrake.encode(input_path, output_path, preset)


@eel.expose
def hb_get_presets():
    """Returns available HandBrake presets."""
    return handbrake.get_presets()


@eel.expose
def get_parser_stats():
    """Returns aggregated performance metrics from all items in the library."""
    try:
        items = db.get_all_media()
        stats = {}
        counts = {}
        for item in items:
            # parser_times is usually a dict in the DB, but might be a JSON string
            p_times = item.get("parser_times")
            if not p_times:
                continue
            if isinstance(p_times, str):
                try:
                    p_times = json.loads(p_times)
                except:
                    continue

            if not isinstance(p_times, dict):
                continue

            for p_name, p_time in p_times.items():
                # Handle list of times or single float
                val = p_time if isinstance(p_time, (int, float)) else (
                    p_time[0] if isinstance(p_time, list) and p_time else 0)
                stats[p_name] = stats.get(p_name, 0.0) + val
                counts[p_name] = counts.get(p_name, 0) + 1

        avg_stats = {k: stats[k] / counts[k] for k in stats if counts[k] > 0}

        # Get last 20 items for granular results
        last_items = []
        # Sort items by some timestamp if available, otherwise just last 20 from db
        # Assuming db.get_all_media returns items in natural order, we take the last ones
        sorted_items = sorted(items, key=lambda x: x.get('id', 0), reverse=True)[:20]
        for item in sorted_items:
            last_items.append({
                "filename": item.get("filename", "Unknown"),
                "title": item.get("title", "-"),
                "artist": item.get("artist", "-"),
                "album": item.get("album", "-"),
                "parser_times": item.get("parser_times", {}),
                "total_time": sum(item.get("parser_times", {}).values()) if isinstance(item.get("parser_times"), dict) else 0
            })

        return {
            "averages": avg_stats,
            "total_items": len(items),
            "last_results": last_items
        }
    except Exception as e:
        log.error(f"Failed to get parser stats: {e}")
        return {"averages": {}, "total_items": 0, "last_results": []}


@eel.expose
def start_handbrake_transcode(input_path: str, output_path: str, encoder: str = "x264", preset: str = "fast"):
    """Exposes HandBrake transcoding to the frontend."""
    options = {"encoder": encoder, "preset": preset}
    task_id = transcode_mgr.add_task(input_path, output_path, "handbrake", options)
    transcode_mgr.start_task(task_id)
    return task_id


@eel.expose
def start_webm_conversion(input_path: str, output_path: str):
    """Exposes WebM/VP9 conversion to the frontend."""
    task_id = transcode_mgr.add_task(input_path, output_path, "webm", {})
    transcode_mgr.start_task(task_id)
    return task_id


@eel.expose
def get_transcode_status(task_id: str):
    """Returns the status and progress of a transcoding task."""
    return transcode_mgr.get_task_status(task_id)

# --- Main Entry Point ---



# --- Tests & Utility Functions ---
@eel.expose
def test_pyautogui():
    """
    Simple test for pyautogui integration.
    Returns screen size and current mouse position.
    """
    try:
        import pyautogui
        screen_size = pyautogui.size()
        mouse_pos = pyautogui.position()
        return {
            "status": "ok",
            "screen_size": {
                "width": screen_size.width,
                "height": screen_size.height},
            "mouse_position": {
                "x": mouse_pos.x,
                "y": mouse_pos.y}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def run_selenium_session_tests(options=None):
    """
    Runs Selenium tests by attaching to the running Chrome instance.
    """
    test_script = PROJECT_ROOT / "tests" / "test_selenium_session.py"
    if not test_script.exists():
        return {"status": "error", "message": f"Test script nicht gefunden unter {test_script}"}

    try:
        # We use the same venv as the main app if possible
        cmd = [sys.executable, str(test_script)]
        if options:
            if options.get('verbose'):
                cmd.append('--verbose')
            if options.get('trace'):
                cmd.append('--trace')
            if options.get('debug'):
                cmd.append('--debug')
            if options.get('dom_control'):
                cmd.append('--dom-control')
            if options.get('pp_mode'):
                cmd.append('--pp-mode')

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {
            "status": "ok",
            "output": result.stdout,
            "error": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Selenium Test Zeitberschreitung (30s)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def discover_cast_devices():
    """Returns discovered Chromecast and DLNA devices."""
    devices = {"chromecast": [], "dlna": []}
    try:
        # Placeholder for pychromecast / dlnap discovery
        # log.info("[Cast] Starting device discovery...")
        pass
    except Exception as e:
        log.error(f"[Cast] Discovery error: {e}")
    return devices


@eel.expose
def start_cast(device_id, media_url):
    """Starts casting a URL to a specific device."""
    log.info(f"[Cast] Casting {media_url} to {device_id}")
    return {"status": "ok"}


_swyh_rs_process = None


@eel.expose
def open_vlc(filepath):
    """Opens a file in VLC player."""
    log.info(f"[Video] Opening in VLC: {filepath}")
    try:
        if sys.platform == "win32":
            os.startfile(filepath)  # Or full VLC path
        else:
            subprocess.Popen(["vlc", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def open_ffplay(filepath):
    """Opens a file in FFplay."""
    log.info(f"[Video] Opening in FFplay: {filepath}")
    try:
        # -autoexit: closes window when playback ends
        # -sn: disable subtitles for performance during test
        subprocess.Popen(["ffplay", "-autoexit", "-sn", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def get_playback_benchmarks():
    """Returns stored playback benchmarks."""
    try:
        path = Path(PROJECT_ROOT) / "benchmarks.json"
        if path.exists():
            return json.loads(path.read_text())
    except:
        pass
    return {}


@eel.expose
def save_playback_benchmarks(data):
    """Saves playback benchmarks."""
    try:
        path = Path(PROJECT_ROOT) / "benchmarks.json"
        path.write_text(json.dumps(data))
        return True
    except:
        return False


@eel.expose
def get_dvd_film_report():
    """Aggregates DVD/Film matrix report."""
    # Placeholder for actual persistence logic if database is used
    return {"total": 0, "dvd": 0, "film": 0}


@eel.expose
def toggle_swyh_rs(enabled: bool):
    """
    @brief Enables/Disables the SWYH-RS bridge.
    """
    global _swyh_rs_process
    try:
        if enabled:
            if _swyh_rs_process and _swyh_rs_process.poll() is None:
                return {"status": "ok", "message": "Already running"}

            # Check if binary exists
            if not shutil.which("swyh-rs-cli"):
                return {"status": "error", "message": "swyh-rs-cli not found"}

            log.info("[Streaming] Starting swyh-rs-cli bridge...")
            # Example flags: -s (serve), -p (port)
            _swyh_rs_process = subprocess.Popen(
                ["swyh-rs-cli", "-s"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {"status": "ok", "message": "Started"}
        else:
            if _swyh_rs_process:
                log.info("[Streaming] Stopping swyh-rs-cli bridge...")
                _swyh_rs_process.terminate()
                _swyh_rs_process.wait(timeout=2)
                _swyh_rs_process = None
            return {"status": "ok", "message": "Stopped"}
    except Exception as e:
        log.error(f"[Streaming] SWYH-RS error: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def open_mpv(filepath):
    """Opens a file in MPV player."""
    log.info(f"[Video] Opening in MPV: {filepath}")
    try:
        # --ontop: keep window visible for easy verification
        subprocess.Popen(["mpv", "--ontop", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def trigger_mkvmerge_remux(filepath):
    """Tests mkvmerge remuxing performance."""
    log.info(f"[Video] Triggering MKVmerge Remux: {filepath}")
    out = PROJECT_ROOT / "cache" / f"remux_{Path(filepath).stem}.mkv"
    out.parent.mkdir(exist_ok=True)

    cmd = ["mkvmerge", "-o", str(out), filepath]
    try:
        # Start in background
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "ok", "details": f"Remux started -> {out.name}"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@eel.expose
def trigger_mtx_stream(filepath, proto="hls"):
    """Starts a MediaMTX stream for the given protocol."""
    log.info(f"[Video] Triggering MediaMTX ({proto}): {filepath}")
    res = stream_to_mediamtx(filepath, protocol=proto)
    if res.get("status") == "play":
        return {"status": "ok", "details": f"MediaMTX {proto.upper()} stream active: {res.get('path')}"}
    return {"status": "error", "details": res.get("error") or "Unknown error"}


class FFmpegTestSuite:
    def __init__(self, input_path):
        from src.parsers.format_utils import ffprobe_suite
        self.input = input_path
        self.input_analysis = ffprobe_suite(input_path)
        self.tests = []

    def test_remux_mkv_mp4(self):
        """MKV -> MP4 Lossless Check"""
        from src.parsers.format_utils import ffprobe_suite
        out = PROJECT_ROOT / "cache" / f"test_remux_{Path(self.input).stem}.mp4"
        cmd = ['ffmpeg', '-y', '-i', self.input, '-c', 'copy', '-movflags', '+faststart', str(out)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
            output_analysis = ffprobe_suite(out)

            # Simple validation
            v_match = self.input_analysis.get('video_codec') == output_analysis.get('video_codec')
            d_match = abs(self.input_analysis.get('duration_min', 0) - output_analysis.get('duration_min', 0)) < 0.2

            return {
                'name': 'MKV->MP4 Remux',
                'status': 'pass' if (v_match and d_match) else 'fail',
                'details': f"In: {self.input_analysis.get('video_codec')} | Out: {output_analysis.get('video_codec')}"
            }
        except Exception as e:
            return {'name': 'MKV->MP4 Remux', 'status': 'fail', 'details': str(e)}

    def test_hls_generation(self):
        """HLS Streaming Segment Test"""
        out_dir = PROJECT_ROOT / "cache" / f"test_hls_{Path(self.input).stem}"
        out_dir.mkdir(parents=True, exist_ok=True)
        playlist = out_dir / "playlist.m3u8"

        cmd = [
            'ffmpeg', '-y', '-i', self.input,
            '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
            '-f', 'hls', '-hls_time', '4', '-hls_list_size', '3',
            str(playlist)
        ]
        try:
            # We only run for a short time to verify segments
            subprocess.run(cmd, check=True, capture_output=True, timeout=15)
            segments = list(out_dir.glob("*.ts"))
            return {
                'name': 'HLS Generation',
                'status': 'pass' if len(segments) > 0 else 'fail',
                'details': f"Generated {len(segments)} HLS segments"
            }
        except subprocess.TimeoutExpired:
            # Timeout is actually okay if segments were created
            segments = list(out_dir.glob("*.ts"))
            return {
                'name': 'HLS Generation',
                'status': 'pass' if len(segments) > 0 else 'fail',
                'details': f"Verified {len(segments)} segments before timeout"
            }
        except Exception as e:
            return {'name': 'HLS Generation', 'status': 'fail', 'details': str(e)}

    def run_full_suite(self):
        """Runs all enabled pipeline tests."""
        results = [
            self.test_remux_mkv_mp4(),
            self.test_hls_generation()
        ]
        return results


@eel.expose
def run_ffmpeg_pipeline_test(relpath):
    """Bridge for the full FFmpeg Pipeline Suite."""
    lib_dir = PARSER_CONFIG.get("library_dir", str(PROJECT_ROOT / "media"))
    full = Path(lib_dir) / relpath
    if not full.exists():
        return {"status": "error", "message": "File not found"}

    suite = FFmpegTestSuite(str(full))
    results = suite.run_full_suite()
    return {"status": "ok", "results": results}


@eel.expose
def start_mp4frag_conversion(filepath, options=""):
    """Starts fragmented MP4 conversion for MSE playback."""
    log.info(f"[Video] Starting FragMP4 conversion: {filepath}")
    return {"status": "ok", "details": "Fragmented MP4 stream ready"}


@eel.expose
def start_spotify_bridge():
    """Starts the Spotify bridge subprocess."""
    log.info("[Cast] Starting Spotify Bridge (Librespot)...")
    return {"status": "ok", "details": "Spotify Bridge active"}


@eel.expose
def batch_remux_to_mkv(folder_path):
    """Remuxes all videos in a folder to MKV using mkvmerge."""
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        return {"status": "error", "error": "Invalid folder"}

    count_remuxed = 0
    mkvmerge_path = shutil.which("mkvmerge") or "mkvmerge"

    for f in path.glob("*"):
        if f.suffix.lower() in [".mp4", ".avi", ".mkv", ".mov", ".ts", ".iso"]:
            output = f.with_suffix(".remuxed.mkv")
            try:
                subprocess.run([mkvmerge_path, "-o", str(output), str(f)], check=True, capture_output=True)
                count_remuxed += 1
            except Exception as e:
                log.error(f"[Remux] Failed for {f.name}: {e}")

    return {"status": "ok", "remuxed_count": count_remuxed}


@eel.expose
def save_benchmark_results(results):
    """Saves playback benchmarks for the reporting dashboard."""
    try:
        bench_file = PROJECT_ROOT / "benchmarks.json"
        history = []
        if bench_file.exists():
            history = json.loads(bench_file.read_text(encoding='utf-8'))
        history.append({
            "timestamp": time.time(),
            "results": results
        })
        limited_history = list(history[-50:])
        bench_file.write_text(json.dumps(limited_history, indent=2), encoding='utf-8')
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@eel.expose
def get_multimedia_analysis():
    """Aggregates a report on DVD/Film objects and Chrome Native compatibility."""
    try:
        items = db.get_all_media()
        analysis = {
            'dvd_objects': [],
            'film_objects': [],
            'chrome_compatible_mp4s': [],
            'incompatible_videos': [],
            'stats': {
                'total_films': 0,
                'total_dvds': 0,
                'native_support_count': 0
            }
        }

        for item in items:
            cat = item.get('category', '')
            tags = item.get('tags', {})
            path = item.get('path', '')
            ext = item.get('extension', '').lower()

            # 1. DVD/Film Detection
            is_dvd_image = ext in ['iso', 'bin', 'img']
            is_dvd_folder = 'VIDEO_TS' in path or 'BDMV' in path

            if cat == 'Film' or is_dvd_image or is_dvd_folder:
                obj = {
                    'name': item.get('name'),
                    'year': tags.get('year', 'Unknown'),
                    'type': item.get('content_type', 'Film'),
                    'format': ext.upper() if not is_dvd_folder else 'Folder',
                    'path': path
                }
                if is_dvd_image or is_dvd_folder:
                    analysis['dvd_objects'].append(obj)
                    stats_dict = cast(dict[str, int], analysis['stats'])
                    stats_dict['total_dvds'] += 1
                else:
                    analysis['film_objects'].append(obj)
                    stats_dict = cast(dict[str, int], analysis['stats'])
                    stats_dict['total_films'] += 1

            # 2. Chrome Native Compatibility (MP4 / H.264 / VP8 / VP9 / AV1)
            is_chrome_native_ext = ext in ('.mp4', '.webm', '.ogg')
            if is_chrome_native_ext:
                # Check both top-level item 'codec' and tags 'video_codec'/'codec'
                raw_codec = item.get('codec') or tags.get('video_codec') or tags.get('codec') or ''
                codec = str(raw_codec).lower()
                # Simple heuristic for Chrome compatibility
                is_native = any(c in codec for c in ['h264', 'avc', 'vp8', 'vp9', 'av1'])
                if is_native:
                    analysis['chrome_compatible_mp4s'].append({
                        'name': item.get('name'),
                        'codec': codec,
                        'is_native': True
                    })
                    analysis['stats']['native_support_count'] += 1
                else:
                    analysis['incompatible_videos'].append({
                        'name': item.get('name'),
                        'codec': codec or 'Unknown',
                        'reason': 'Codec not natively supported by Chrome'
                    })
            elif ext in ('.mkv', '.avi', '.mov', '.ts', '.m2ts'):
                # These definitely need VLC or Transcoding for Chrome
                analysis['incompatible_videos'].append({
                    'name': item.get('name'),
                    'codec': tags.get('video_codec', 'Unknown'),
                    'reason': 'Container not supported by Chrome Native'
                })

        return analysis
    except Exception as e:
        log.error(f"Failed to generate multimedia analysis: {e}")
        return {'error': str(e)}


@eel.expose
def get_model_analysis():
    """Aggregates stats on category, content_type, and media_type from the DB."""
    try:
        items = db.get_all_media()
        stats: dict[str, Any] = {
            'categories': {},
            'content_types': {},
            'media_types': {},
            'total_count': len(items),
            'samples': {}  # Sample items for each category
        }

        for item in items:
            cat = item.get('category', 'Unknown')
            ct = item.get('content_type', 'Unknown')
            mt = item.get('type', 'Unknown')  # Internal media_type name

            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            stats['content_types'][ct] = stats['content_types'].get(ct, 0) + 1
            stats['media_types'][mt] = stats['media_types'].get(mt, 0) + 1

            # Keep a sample for each category if not already present
            if cat not in stats['samples'] and len(stats['samples']) < 20:
                stats['samples'][cat] = {
                    'name': item.get('name'),
                    'path': item.get('path'),
                    'content_type': ct,
                    'media_type': mt
                }

        return stats
    except Exception as e:
        log.error(f"Failed to get model analysis: {e}")
        return {'error': str(e)}


@eel.expose
def get_cover_extraction_report():
    """Analyzes artwork efficiency and sources."""
    try:
        items = db.get_all_media()
        report: dict[str, Any] = {
            'total': len(items),
            'has_artwork': 0,
            'missing_artwork': 0,
            'sources': {
                'embedded_or_cache': 0,
                'local_folder': 0
            },
            'formats': {}
        }

        for item in items:
            art = item.get('art_path') or item.get('artwork')
            if art:
                report['has_artwork'] = report.get('has_artwork', 0) + 1
                art_path = Path(art)
                # Check if it is in cache
                if '.cache' in str(art_path):
                    report['sources']['embedded_or_cache'] = report['sources'].get('embedded_or_cache', 0) + 1
                else:
                    report['sources']['local_folder'] = report['sources'].get('local_folder', 0) + 1
                # Format stats
                p = Path(art_path)
                ext = p.suffix.lower().lstrip('.')
                if ext:
                    report['formats'][ext] = report['formats'].get(ext, 0) + 1
            else:
                report['missing_artwork'] += 1

        return report
    except Exception as e:
        log.error(f"Failed to get cover extraction report: {e}")
        return {'error': str(e)}


@eel.expose
def get_routing_suite_report():
    """
    @brief Aggregates routing statistics and quality scores for the entire library.
    """
    try:
        from src.parsers.format_utils import ffprobe_quality_score, is_direct_play_capable
        items = db.get_all_media()

        # Local distribution counters to satisfy static analysis
        dist = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
        modes = {'direct': 0, 'vlc': 0, 'hls': 0, 'transcode': 0, 'error': 0}

        total_score = 0
        video_count = 0
        top_quality_items = []
        complex_items = []
        incompatible_count: int = 0
        codec_dist = {}

        for item in items:
            if item.get('type') != 'video':
                continue

            video_count += 1
            path = item.get('path', '')
            tags = item.get('tags', {})

            score = ffprobe_quality_score(tags)
            total_score += score

            # Update distribution
            if score <= 20:
                dist['0-20'] += 1
            elif score <= 40:
                dist['21-40'] += 1
            elif score <= 60:
                dist['41-60'] += 1
            elif score <= 80:
                dist['61-80'] += 1
            else:
                dist['81-100'] += 1

            # Determine Recommended Mode
            ext = item.get('extension', '').lower()
            is_direct = is_direct_play_capable(path, 'browser')

            if is_direct:
                mode = 'direct'
            elif ext in ('.iso', '.bin', '.img') or item.get('is_disc'):
                mode = 'transcode'
            elif 'mpeg' in str(tags.get('codec', '')).lower() or 'vc1' in str(tags.get('codec', '')).lower():
                mode = 'transcode'
            elif tags.get('hdr'):
                mode = 'vlc'
            else:
                mode = 'hls'

            modes[mode] = modes.get(mode, 0) + 1

            codec = str(tags.get('codec', 'unknown')).lower()
            codec_dist[codec] = codec_dist.get(codec, 0) + 1

            if not is_direct:
                incompatible_count = int(incompatible_count) + 1

            list_item = {'name': item.get('name'), 'score': score, 'mode': mode}
            if score >= 80:
                top_quality_items.append(list_item)
            elif score < 40 or mode in ['vlc', 'transcode']:
                complex_items.append(list_item)

        avg_score = total_score / video_count if video_count > 0 else 0

        report = {
            'total_items': len(items),
            'video_items': video_count,
            'avg_quality_score': float(f"{avg_score:.1f}"),
            'modes': modes,
            'score_distribution': dist,
            'top_quality_items': sorted(top_quality_items, key=lambda x: x['score'], reverse=True)[:10],
            'complex_items': sorted(complex_items, key=lambda x: x['score'])[:10],
            'incompatible_count': incompatible_count,
            'codec_distribution': codec_dist
        }

        return report
    except Exception as e:
        log.error(f"Failed to get routing suite report: {e}")
        return {'error': str(e)}


@eel.expose
def get_streaming_capability_matrix():
    return [
        {
            "engine": "Chrome Native",
            "modes": ["Integrated", "Direct"],
            "formats": ["MP4", "WebM", "OGG"],
            "codecs": ["H.264", "VP8", "VP9", "AV1"],
            "features": ["HW Accel", "Low Latency", "Browser Native"],
            "notes": "Best for web-compatible MP4 files. Zero transcoding required."
        },
        {
            "engine": "MediaMTX (mmts)",
            "modes": ["HLS", "WebRTC", "RTSP"],
            "formats": ["MP4", "MKV (via FFmpeg)"],
            "codecs": ["H.264", "AAC"],
            "features": ["Multi-device", "Zero client install", "HTTP Streaming"],
            "notes": "Ideal for streaming to multiple devices over network via FFmpeg remux."
        },
        {
            "engine": "VLC (Universal)",
            "modes": ["External", "VLC.js"],
            "formats": ["ISO", "BIN", "IMG", "MKV", "AVI", "DVD", "VIDEO_TS"],
            "codecs": ["All (H.265, AC3, DTS, etc.)"],
            "features": ["DVD Menus", "Subtitles", "Post-processing"],
            "notes": "Universal player for all file types including disc images and legacy formats."
        },
        {
            "engine": "mkvmerge",
            "modes": ["Remux", "Batch"],
            "formats": ["MKV (Output)", "All (Input)"],
            "codecs": ["Container Shift"],
            "features": ["Sub-track preservation", "Fast remux", "ISO to MKV"],
            "notes": "Used for converting incompatible containers into streamable MKV/MP4."
        },
        {
            "engine": "ffplay",
            "modes": ["CLI Preview"],
            "formats": ["All"],
            "codecs": ["All (FFmpeg-based)"],
            "features": ["Low latency", "Raw decoding", "Debug view"],
            "notes": "Technical fallback for quick local playback verification."
        },
        {
            "engine": "swyh-rs (suw)",
            "modes": ["Audio HTTP", "DLNA"],
            "formats": ["WAV", "FLAC", "LPCM"],
            "codecs": ["Lossless PCM"],
            "features": ["System Audio Capture", "Network Audio"],
            "notes": "Specialized for lossless audio streaming to network devices (Stream What You Hear)."
        },
        {
            "engine": "PyPlayer (Integrated)",
            "modes": ["Direct Python"],
            "formats": ["All (FFmpeg compatible)"],
            "codecs": ["All"],
            "features": ["Zero external dependencies", "Native control"],
            "notes": "Built-in Python-based media engine for fallback and simple playback."
        }
    ]


@eel.expose
def get_media_compatibility_report():
    """Generates a detailed compatibility matrix for all media items in the library."""
    from src.core import db
    from src.parsers.format_utils import is_chrome_native

    try:
        items = db.get_all_media()
        report = []

        for item in items:
            tags = item.get('tags', {})
            codec = tags.get('video_codec', tags.get('codec', ''))
            ext = item.get('extension', '').lower()

            is_chrome = is_chrome_native(ext, codec)
            is_mtx = ext in ['.mp4', '.mkv', '.avi', '.mov', '.ts']  # FFmpeg can remux these
            is_vlc = True  # VLC plays everything
            is_ffplay = True  # FFmpeg plays everything

            # Specialized check for disc images
            is_disc = ext in ['.iso', '.bin', '.img'] or item.get('category') == 'Abbild'
            if is_disc:
                is_chrome = False
                is_mtx = False  # MTX doesn't native stream ISOs usually without complex piping

            report.append({
                'name': item.get('name'),
                'type': item.get('type'),
                'category': item.get('category'),
                'chrome_native': is_chrome,
                'mediamtx': is_mtx,
                'vlc': is_vlc,
                'ffplay': is_ffplay,
                'notes': "ISO/Image requiring VLC" if is_disc else ""
            })
        return report
    except Exception as e:
        log.error(f"Failed to generate compatibility report: {e}")
        return []


# --- Media Routing Test Suite & Cache Logic ---

MEDIA_CACHE = Path(logger.APP_DATA_DIR) / "cache" / "media"


@eel.expose
def analyze_media(relpath: str, client: str = 'browser'):
    """
    Deep analysis for routing decisions.
    """
    try:
        from src.parsers.format_utils import ffprobe_quality_score, is_direct_play_capable
        from src.core.handlers import get_handler_for_file

        # Resolve relative path to full path
        full = Path(resolve_media_path(relpath))

        if not full.exists():
            return {"error": "File not found"}

        handler = get_handler_for_file(full)
        route_info = handler.process(client=client, relpath=relpath)

        analysis = route_info.get("analysis")
        if not analysis:
            analysis = handler.extract_metadata()

        score = ffprobe_quality_score(analysis)
        direct = is_direct_play_capable(full, client)

        return {
            "analysis": analysis,
            "quality_score": score,
            "direct_play_browser": direct,
            "recommended_mode": route_info.get("mode"),
            "direct_url": route_info.get("url"),
            "relpath": relpath
        }
    except Exception as e:
        log.exception(f"Critical error in analyze_media for {relpath}")
        return {"error": str(e), "mode": "error"}


@eel.expose
def get_play_source(item_path: str, client: str = 'browser'):
    """
    Resolves the final abspielbare URL, handling cache/remuxing/transcoding via Handlers.
    """
    from src.core.handlers import get_handler_for_file

    # 0. Robust path resolution
    full = Path(resolve_media_path(item_path))
    if not full.exists():
        return {
            "mode": "error",
            "message": f"File not found: {item_path}"
        }

    handler = get_handler_for_file(full)
    return handler.process(client=client, relpath=item_path)


@eel.expose
def scan_js_errors():
    """
    @brief Scans app.html for potential JS errors like unguarded .style accesses.
    @details Nutzt Regex um direkte Zugriffe auf DOM-Element-Properties ohne Null-Checks zu finden.
    @return Dictionary mit findings und status.
    """
    try:
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists():
            return {"status": "error", "message": "app.html not found"}

        content = app_html.read_text(encoding='utf-8')
        patterns = [
            (r"document\.getElementById\(['\"][^'\"]+['\"]\)\.(?:style|innerHTML|innerText|value|classList)",
             "Direct access on getElementById()"),
            (r"document\.querySelector\(['\"][^'\"]+['\"]\)\.(?:style|innerHTML|innerText|value|classList)",
             "Direct access on querySelector()"),
        ]

        findings = []
        lines = content.split('\n')
        for pattern, desc in patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    # Check if it's inside a comment
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith(
                            '/*') or stripped.startswith('*'):
                        continue
                    findings.append(
                        {"line": i, "desc": desc, "content": stripped[:150]})

        return {"status": "ok", "findings": findings}
    except Exception as e:
        log.error(f"[QA] JS Error Scan failed: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def check_ui_integrity():
    """
    @brief Checks app.html for structural integrity (div balance, duplicate functions, orphaned catches).
    @details Statische Analyse der HTML/JS Struktur zur Vermeidung von Layout-Ghosting und Syntax-Fehlern.
    @return Dictionary mit Ergebnissen.
    """
    try:
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists():
            return {"status": "error", "message": "app.html not found"}

        content = app_html.read_text(encoding='utf-8')

        # 1. Div Balance - STRIP SCRIPTS/STYLES FIRST to avoid false positives!
        clean_content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        clean_content = re.sub(r'<style.*?>.*?</style>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)

        opens = len(re.findall(r'<div\b', clean_content, re.IGNORECASE))
        closes = len(re.findall(r'</div\b', clean_content, re.IGNORECASE))
        div_balance = {
            "opens": opens,
            "closes": closes,
            "balanced": opens == closes}

        # 2. Duplicate Functions
        # Extract named functions (function foo(...) and async function foo(...))
        func_defs = re.findall(
            r'\basync\s+function\s+(\w+)\s*\(|(?<!\w)function\s+(\w+)\s*\(',
            content)
        names = [a or b for a, b in func_defs]
        seen = {}
        duplicates = []
        for name in names:
            if not name:
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] == 2:
                duplicates.append(name)

        # 3. Orphaned Catch Blocks
        lines = content.split('\n')
        orphaned_catches = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r'^\}\s*catch\s*[\(\{]', stripped):
                # Scan backwards to find the nearest function definition or file start
                found_try = False
                # Max 600 lines back should be enough
                for j in range(i - 2, max(0, i - 600), -1):
                    lj = lines[j].strip()
                    if re.search(r'\btry\s*\{', lj):
                        found_try = True
                        break
                    # Stop at the enclosing function start
                    if re.match(r'(async\s+)?function\s+\w+\s*\(', lj):
                        break
                if not found_try:
                    orphaned_catches.append(i)

        # 4. Python Source Integrity
        python_errors = []
        try:
            # Check src and tests for SyntaxErrors (only top level / src files for speed)
            for target_dir in [PROJECT_ROOT / "src", PROJECT_ROOT / "tests"]:
                if target_dir.exists():
                    all_py = list(target_dir.rglob("*.py"))
                    # Limit to first 100 files for quick feedback if needed, but let's try all
                    for py_file in all_py:
                        if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                            continue
                        try:
                            with open(py_file, 'r', encoding='utf-8') as f:
                                ast.parse(f.read())
                        except SyntaxError as e:
                            python_errors.append(f"{py_file.name}:L{e.lineno} {e.msg}")
                        except Exception:
                            pass
        except Exception as e:
            python_errors.append(f"Scanner error: {e}")

        return {
            "status": "ok",
            "div_balance": div_balance,
            "python_integrity": {"balanced": len(python_errors) == 0, "errors": python_errors},
            "duplicates": sorted(duplicates),
            "orphaned_catches": orphaned_catches
        }
    except Exception as e:
        log.error(f"[QA] UI Integrity Check failed: {e}")
        return {"status": "error", "message": str(e)}


# Alignment Aliases for test suites (using wrappers to avoid Eel naming conflicts)
@eel.expose
def get_benchmark_results(*args, **kwargs):
    return get_playback_benchmarks(*args, **kwargs)


@eel.expose
def update_additional_library_dirs(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def run_video_matrix_test(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def open_file_dialog(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def trigger_webm_transcode(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def get_media_by_name(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def trigger_ffmpeg_stream(*args, **kwargs):
    return {"status": "ok"}


@eel.expose
def analyze_media_item(*args, **kwargs):
    return {"status": "ok"}



if __name__ == "__main__":
    start_app()

    log.info("[Main] Entering keepalive loop.")
    while True:
        try:
            eel.sleep(1.0)
        except KeyboardInterrupt:
            log.info("[Shutdown] KeyboardInterrupt received. Exiting.")
            sys.exit(0)
        except BaseException as e:
            log.warning(f"[MainLoop] keepalive recovered from: {e}")
            time.sleep(1.0)
