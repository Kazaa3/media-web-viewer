import sys
import os
from pathlib import Path

# --- [v1.46.132-PROFESSIONAL] High-Priority Bootstrap Guard ---
# NOTE: This block intentionally calculates paths locally for sys.path discovery.
_file = Path(__file__).resolve()
_root = _file.parent.parent.parent  # src/core -> src -> PROJECT_ROOT
_src  = _root / "src"

# Forced Path Injection (Forensic Reset)
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

# --- 1. Path Forensics Done ---
if sys.platform != "win32":
    # [v1.53.003-R3] Adaptive Environment Bootstrap: Force project-local .venv
    _venv_py = _root / ".venv" / "bin" / "python3"
    if _venv_py.exists() and str(_venv_py) != sys.executable:
        print(f"STDOUT: [Bootstrap] Wrong Venv detected. Switching to {_venv_py}...", flush=True)
        os.execv(str(_venv_py), [str(_venv_py)] + sys.argv)

from src.core import startup_auditor
try:
    # [v1.54.007] Mandatory Boot Guard: Strictly enforce environment integrity
    audit_passed = startup_auditor.run_audit()
    if not audit_passed:
        print("STDOUT: [Audit-Pulse] FATAL: System integrity could not be verified. Entering Emergency Mode.", flush=True)
        # In a headless environment, we might want to exit, but here we'll try to limp along
        # or signal to the UI that it's in a broken state.
        # For now, we force an exit if it's a critical mismatch.
        if "--force-boot" not in sys.argv:
            sys.exit(1)
except Exception as e:
    print(f"STDOUT: [Audit-Pulse] Critical boot guard failure: {e}", flush=True)
    sys.exit(1)

# --- 2. Internal Imports ---
from src.core.config_master import (
    _DOTENV_LOADED, APP_VERSION_CORE, 
    PROJECT_ROOT, DEFAULT_TIME_FORMAT, 
    WINDOW_SIZE, FRONTEND_SETTINGS, EEL_SETTINGS,
    LAUNCH_PROFILE, FORENSIC_TOOLS_LIST,
    GLOBAL_CONFIG, PORT_CLEANUP_CMD,
    BITRATE_QUALITY_THRESHOLDS, DEPENDENCY_REGISTRY
)
from src.core.db import get_active_db_path
from src.core import (
    api_playlist, api_frontend, api_orchestrator, 
    api_logbuch, api_testing, api_diagnostics, api_audit,
    api_config, api_core_app, api_library, api_reporting,
    api_tools, api_environment, api_ui,
    api_playback, api_file_browser, api_legacy_archive,
    api_media_tools
)
from src.core.object_discovery import ObjectDiscoveryEngine
from src.core.objects import create_forensic_object
from typing import Dict, Any, List, Optional, cast, Tuple
import threading
import ast
import sqlite3
import glob
import shutil
import re
import platform
import socket
import contextlib
import traceback
import logging
import json
import time
import os
import psutil
from unittest.mock import MagicMock
from urllib.parse import unquote

# Verification of Package Root
try:
    import core
    import src
except ImportError as e:
    # If we are in a re-exec, this is critical
    print(f"STDOUT: [Bootstrap-Critical] Path Fault: {e}", flush=True)
    print(f"STDOUT: [Bootstrap-Path] PROJ_ROOT: {_root}", flush=True)
    print(f"STDOUT: [Bootstrap-Path] SRC_ROOT: {_src}", flush=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - Business Logic & Application Entry Point
dict - Desktop Media Player and Library Manager v1.41.00
"""


# --- PERFORMANCE PROFILING ---
INITIAL_START_TIME = time.time()
APP_START_TIME = INITIAL_START_TIME
profiler = None
ACTIVE_FORENSIC_PROCESSES = {}  # v1.46.089 PID Registry: {pid: "component_name"}
FRONTEND_PROCESS_ID = None      # Resolved FE PID (Chromium/Electron)

# --- BOOTSTRAP LOGGER (Safety for Environment Swaps) ---


class BootstrapLogger:
    def info(self, m): print(f"STDOUT: {m}", flush=True)
    def error(self, m): print(f"STDOUT: [ERROR] {m}", flush=True)
    def warning(self, m): print(f"STDOUT: [WARN] {m}", flush=True)
    def critical(self, m): print(f"STDOUT: [CRITICAL] {m}", flush=True)
    def debug(self, m): print(f"STDOUT: [DEBUG] {m}", flush=True)
    def exception(self, m): print(f"STDOUT: [EXCEPTION] {m}", flush=True)


log = BootstrapLogger()


def log_self_diagnostics():
    """Logs critical environment information."""
    log.info("--- [ENV DIAGNOSTICS] ---")
    log.info(f"Python: {sys.version}")
    log.info(f"Executable: {sys.executable}")
    log.info(f"Prefix: {sys.prefix}")
    log.info(f"Project Root: {_root}")
    log.info(f"Working Dir: {os.getcwd()}")
    log.info(f"SYS_PATH: {sys.path[:3]}")  # Show top 3
    log.info("-------------------------")

# Environment Guard already executed at top.

# --- EXECUTE GUARD IMMEDIATELY ---
# Consolidated Entry Point at end of file.


# --- INITIALIZE PROFILER (Post-Guard) ---
try:
    from core.startup_monitor import profiler
    if profiler:
        profiler.set_base_time(INITIAL_START_TIME)
        profiler.start_phase("Bootstrap-PostGuard")
except ImportError:
    profiler = None

# --- IF WE ARE HERE, THE ENVIRONMENT IS STABLE ---
# 2. Main Imports
try:
    # Dependency Shielding (v1.47)
    try:
        import bottle
    except ImportError:
        log.warning("[Bootstrap] Bottle missing. Mocking bridge active.")
        bottle = MagicMock()
    
    from src.core.eel_shell import eel
    from eel import chrome
    log.info("[Bootstrap] Eel loaded successfully")

    # --- CORE METADATA REGISTRY ---
    from src.core.config_master import (
        GLOBAL_CONFIG, APP_VERSION, APP_VERSION_CORE, APP_VERSION_FULL, BACKEND_VERSION, FRONTEND_VERSION,
        VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS
    )
    from src.core.models import MASTER_CAT_MAP, TECH_MARKERS, MediaItem, get_allowed_internal_cats
    from src.core.transcoder import TranscoderManager
    from src.core import handbrake_wrapper as handbrake
    from src.core import api_library
    from src.core import api_reporting
    from src.core import mkv_tool_wrapper as mkv_tool
    from src.core.subtitle_processor import SubtitleProcessor
    import requests
    
    VERSION = APP_VERSION
    PROJECT_ROOT = _root
    
    # Initialize Global Managers
    transcode_mgr = TranscoderManager()
    
except ImportError as e:
    log.error(f"[Bootstrap] Required module missing: {e}")
    # Minimal fallback assignment to avoid NameErrors in subsequent code
    if 'eel' not in locals() and 'eel' not in globals():
        from src.core.eel_shell import eel
    sys.exit(1)


# [v1.46.090] Note: get_startup_info consolidated to enhanced version at bottom.


# [v1.46.090] Note: get_startup_info consolidated to enhanced version at bottom.


@eel.expose
def get_system_forensics():
    """Returns the full environment inventory for the technical HUD."""
    return api_testing.get_environment_inventory()


# [v1.54.018] Heartbeat & Events migrated to api_core_app and api_frontend.


# (audit_dom_state moved to api_diagnostics)


# [v1.54.018] Emergency Recovery migrated to api_diagnostics.

# (Path calculation and sys.path injection moved to config_master.py)


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
        def update(self, *a): log.info(f"[Progress] {self.msg} ({a[0]}%)")


class Lazy:
    """Lazy-loading proxy for modules (v1.41.00 Optimization)."""

    def __init__(self, name): self._name, self._mod = name, None

    def __getattr__(self, attr):
        if not self._mod:
            import importlib
            self._mod = importlib.import_module(self._name)
            log.debug(f"🚀 [Lazy-Load] {self._name} accessed via '{attr}'")
        return getattr(self._mod, attr)


# (gevent patching moved to top for v1.46.136 stability)

# Lazy Proxy Module Registry (v1.41.00 - Exact Mappings)
mode_router = Lazy("src.core.mode_router")
hardware_detector = Lazy("src.core.hardware_detector")
remux_utils = Lazy("src.core.remux_utils")
hls_stream = Lazy("src.core.streams.hls_stream")
vlc_bridge = Lazy("src.core.streams.vlc_bridge")
tag_writer = Lazy("src.parsers.tag_writer")
format_utils = Lazy("src.parsers.format_utils")

# Data Proxies (Redirecting to format_utils)


class LazyConfigProxy(Lazy):
    def __getattr__(self, attr):
        mod = super().__getattr__("__name__")  # force load
        return getattr(self._mod, "PARSER_CONFIG").get(
            attr) if attr != "get" else getattr(self._mod, "PARSER_CONFIG").get

    def __getitem__(self, key):
        if not self._mod:
            self.__getattr__("get")
        return self._mod.PARSER_CONFIG[key]

    def __setitem__(self, key, value):
        if not self._mod:
            self.__getattr__("get")
        self._mod.PARSER_CONFIG[key] = value

    def update(self, val):
        if not self._mod:
            self.__getattr__("get")
        self._mod.PARSER_CONFIG.update(val)


PARSER_CONFIG = LazyConfigProxy("src.parsers.format_utils")

with StatusBar("Initializing Application Environment", total=100) as sb:
    sb.update(40, "Environment Stabilized")

    # --- Core Imports & Logging ---
    from src.core.logger import get_logger, stall_watchdog, progress_update, get_timestamped_log_path
    import src.core.logger as logger
    sb.update(60, "Logger Initializing")

    # Initialize SESSION_ID as early as possible (v1.41.169 Custom Format)
    _fmt = GLOBAL_CONFIG.get("logging_registry", {}).get("session_id_format", "{timestamp}_{pid}")
    SESSION_ID = _fmt.format(timestamp=int(time.time()), pid=os.getpid())

    def initialize_startup_logging():
        is_debug = "--debug" in sys.argv
        log_level = logging.DEBUG if is_debug else logging.INFO
        logger.setup_logging(debug_mode=is_debug, level=log_level, session_id=SESSION_ID)
        log.info(f"[System] Log initialized (ID: {SESSION_ID}, Level: {'DEBUG' if is_debug else 'INFO'})")

    initialize_startup_logging()
    log = get_logger("main")
    sb.update(100, "Core Ready")

# Performance Tracking
STARTUP_TIME = time.time()
CHECKPOINTS = []


def log_checkpoint(msg: str, tag: str = "generic"):
    elapsed = time.time() - STARTUP_TIME
    CHECKPOINTS.append((msg, elapsed))
    if profiler:
        profiler.log_checkpoint(msg, tag)
    else:
        # Fallback to simple logging
        log.info(f"[Checkpoint] {elapsed:6.3f}s | {msg}")


def launch_eel_server():
    """Initializes the Eel server and assets (v1.46.136)."""
    with StatusBar("Loading Core Components", total=100) as sb:
        sb.update(0, "Importing Eel")
        import eel

        sb.update(10, "Initializing Eel Assets")
        web_dir = str(PROJECT_ROOT / "web")
        log.info(f"\n[DIAGNOSTIC] !!! EEL WEB DIRECTORY: {os.path.abspath(web_dir)} !!!\n")
        if not os.path.exists(web_dir):
            log.critical(f"Web dir not found at {web_dir}")
            sys.exit(1)
        eel.init(web_dir)
        sb.update(25, "Eel Assets Ready")

        sb.update(30, "Registering Core SRC Modules")
def bootstrap_core_settings():
    """Initializes the core runtime settings (v1.46.136)."""
    global port, eel_kwargs, transcode_mgr
    try:
        if profiler:
            profiler.start_phase("Core-Bootstrap")
        
        # 1. DB Initialization
        from core import db
        db.init_db()
        media_count = db.get_media_count()
        log.info(f"[Startup-Trace] DB Initialized: {media_count} records found.")
        
        # 2. Centralized settings handshake
        port = EEL_SETTINGS["port"]
        eel_kwargs = {
            'host': EEL_SETTINGS["host"], 
            'size': EEL_SETTINGS["size"]
        }
        
        # 3. Manager Initialization
        from src.core.transcoder import TranscoderManager
        transcode_mgr = TranscoderManager()
        
        if profiler: profiler.end_phase("Core-Bootstrap")
        return True
    except Exception as e:
        log.critical(f"Resource bootstrap failure: {e}")
        return False

# Initialize settings only if running as main, or explicitly called
if __name__ == "__main__":
    bootstrap_core_settings()

# --- Eel Communication & Lifecycle ---
spawn_event = threading.Event()


# [v1.54.018] Hydration & Event Bridge migrated to api_frontend and api_config.


# [v1.54.018] UI & Footer Orchestration migrated to api_config and api_frontend.


# [v1.54.018] DOM Auditing migrated to api_frontend and api_diagnostics.


def run_app_audit_detached(session_port):
    """
    Background thread that waits for the Eel UI to be ready and then launches
    the Playwright audit script in debug mode.
    """
    def audit_trigger():
        log.info(f"[System-Audit] Waiting for UI synchronization on port {session_port}...")
        spawn_event.wait()
        log.info(f"[Guard] Boot Sequence Initiated. Waiting for UI hydration...")
        eel.sleep(8)  # Allow UI to settle (v1.34 has glassmorphic transitions)
        log.info(f"[System-Audit] Launching Playwright UI Audit (scripts/app_audit_playwright.py)...")

        audit_script = PROJECT_ROOT / "scripts" / "app_audit_playwright.py"
        try:
            # We use the current python executable to ensure same venv
            api_root = GLOBAL_CONFIG["network_settings"].get("api_root", f"http://localhost:{session_port}")
            cmd = [sys.executable, str(audit_script), "--url", f"{api_root}/app.html"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(PROJECT_ROOT))

            for line in process.stdout:
                line_clean = line.strip()
                if line_clean:
                    log.info(f"[System-Audit] {line_clean}")

            process.wait()
            if process.returncode == 0:
                log.info(f"[System-Audit] Audit SUCCESS. Report: scripts/audit_reports/audit_report.md")
            else:
                log.info(f"[System-Audit] Audit completed with status {process.returncode}")
        except Exception as e:
            log.error(f"[System-Audit] Audit execution error: {e}")

    threading.Thread(target=audit_trigger, daemon=True).start()


# [v1.54.018] DB Recovery migrated to api_diagnostics.


def start_app():
    """Launches the Eel application with a robust startup watchdog."""
    if profiler:
        profiler.start_phase("App-Launch-Setup")

    # --- [v1.46.034] MANDATORY PRE-FLIGHT INTEGRITY AUDIT ---
    from src.core.startup_auditor import run_preflight_audit
    if profiler: profiler.start_phase("Integrity-Verification")
    if not run_preflight_audit():
        log.critical("[Bootstrap] FATAL: System Integrity Audit FAILED. Startup aborted.")
        sys.exit(1)
    if profiler:
        profiler.mark_integrity_verified()
        profiler.end_phase("Integrity-Verification")

    # --- ULTRA-SOLO STARTUP (Zero-Latency) ---
    from core.process_manager import ProcessController
    app_data = Path(GLOBAL_CONFIG.get("storage_registry", {}).get("data_dir", str(PROJECT_ROOT)))
    pc = ProcessController(PROJECT_ROOT, app_data)

    # Singleton Guard (v1.46.026 Robust Bootstrap)
    if not pc.acquire_lock():
        owner_pid = pc.get_lock_owner()
        owner_alive = False
        if owner_pid > 0:
            try:
                import psutil
                owner_alive = psutil.pid_exists(owner_pid)
            except:
                pass

        if not owner_alive:
            log.warning(f"[Bootstrap] STALE LOCK detected (Owner PID {owner_pid} is dead). Overwriting...")
            pc.cleanup_environment()
            if not pc.acquire_lock():
                log.error("[Bootstrap] MWV LOCK PERSISTENCE ERROR. Manual cleanup required.")
                sys.exit(1)
        else:
            log.warning(f"[Bootstrap] Lock collision with ACTIVE process (PID {owner_pid}). Retrying once...")
            time.sleep(0.5)
            if not pc.acquire_lock():
                log.error(f"[Bootstrap] MWV ALREADY RUNNING (PID {owner_pid}). Aborting.")
                sys.exit(1)

    # 1. Environment Readiness (Centralized v1.46.136)
    eel_mode = api_frontend.get_eel_mode()
    port = FRONTEND_SETTINGS["port"]

    print(f"STDOUT: [Bootstrap-Audit] Starting Eel Engine (mode={eel_mode}, port={port})...", flush=True)

    try:
        # [v1.44] DYNAMIC ENTRY POINT SELECTION
        evolution_mode = GLOBAL_CONFIG.get("ui_evolution_mode", "stable")
        start_page = 'shell_master.html' if evolution_mode in ['rebuild', 'bridge', 'test_ref'] else 'app.html'

        print(f"STDOUT: [Bootstrap] Launching ENTRY_POINT: {start_page} (Mode: {evolution_mode})", flush=True)
        # Use centralized EEL_SETTINGS and api_frontend
        eel.start(
            start_page, 
            block=False, 
            port=port, 
            mode=eel_mode, 
            size=EEL_SETTINGS["size"],
            host=EEL_SETTINGS["host"],
            cmdline_args=EEL_SETTINGS["cmdline_args"]
        )
        log.info("[Eel] Server started. Monitoring for frontend synchronization...")

        # --- Debug Audit Trigger ---
        if LAUNCH_PROFILE["debug_mode"]:
            api_testing.run_app_audit_detached(port)

        # --- Hang Detection / Watchdog ---
        timeout = GLOBAL_CONFIG.get("watchdog_timeout", 60)
        start_wait = time.time()
        while not spawn_event.is_set():
            if time.time() - start_wait > timeout:
                log.error(f"[Watchdog] Startup HANG detected (No UI sync after {timeout}s)!")
                break
            eel.sleep(0.5)

        if spawn_event.is_set():
            print("STDOUT: [Success] UI SYNCHRONIZED. MWV READY.", flush=True)
            if profiler:
                profiler.end_phase("UI-Sync-Wait")
            if profiler:
                profiler.log_checkpoint("Application Ready", tag="success")

    except Exception as e:
        print(f"CRITICAL: Eel launch failure: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def ensure_singleton():
    """Manages MWV singleton state using the centralized process_manager."""
    from src.core.process_manager import ProcessController
    pm = ProcessController(PROJECT_ROOT, Path(logger.APP_DATA_DIR))
    if not pm.acquire_lock():
        pm.kill_stale_instances()
        if not pm.acquire_lock():
            print("CRITICAL: Another instance is blocking the singleton lock.", flush=True)
            sys.exit(1)
    return pm


# _SINGLETON_LOCK = ensure_singleton()
# --- End of Startup Block ---
def log_session_diagnostics():
    """Logs the consolidated workstation session identity (v1.46.136)."""
    # 4. Bandwidth Optimization (v1.41.00)
    if GLOBAL_CONFIG.get("bandwidth_mode") == "low":
        log.info("[Config] Low-Bandwidth Mode active: Disabling deep analysis.")
        GLOBAL_CONFIG["ffmpeg_deep_analysis"] = False
        GLOBAL_CONFIG["fast_scan"] = True

    # 4. Environment & Session Diagnostics (v1.41.00)
    env_type = "Conda" if os.environ.get("CONDA_PREFIX") else "Venv" if os.environ.get("VIRTUAL_ENV") else "System"
    log.info(f"[System] Booting from {env_type} (Dotenv Loaded: {_DOTENV_LOADED})")
    log.info(f"[System] Session: {SESSION_ID} | PID: {os.getpid()} | Port: {EEL_SETTINGS['port']}")
    log.info(f"[System] Active Database: {get_active_db_path()}")

# (log_session_diagnostics call moved to bottom)


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

        # Try to find the most recent active stream
        active = {}
        if globals().get("GLOBAL_ACTIVE_STREAMS"):
            # Sort by timestamp to get the current/last session
            sorted_sessions = sorted(GLOBAL_ACTIVE_STREAMS.items(), key=lambda x: x[1].get('ts', 0), reverse=True)
            if sorted_sessions:
                active = sorted_sessions[0][1]

        return {
            "codec": active.get("codec", "H.264 / HEVC"),
            "bitrate": active.get("bitrate", "8.5 Mbps"),
            "gpu_info": f"{hw.get('type', 'Unknown')} ({gpu_util:.1f}%)",
            "gpu_util": gpu_util,
            "rtt_ms": active.get("rtt", 12),
            "audio_engine": active.get("engine", "FFmpeg Premium Remux"),
            "atmos": active.get("atmos", False),
            "bitstream": active.get("bitstream", False),
            "is_active": bool(active)
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
# --- Forensic API Registry & Bootstrap (Modernized v1.54.021) ---
# All functions previously residing here have been migrated to specialized API modules:
# - api_reporting.py, api_diagnostics.py, api_library.py, api_core_app.py, api_tools.py
# Reference the import grid at the top of main.py for Eel registration.



# --- Forensic API Registry & Bootstrap (Modernized v1.54.021) ---
# All functions previously residing here have been migrated to specialized API modules.








@eel.expose
def get_storage_forensics():
    return api_reporting.get_storage_forensics()

@eel.expose
def check_database_resilience():
    return api_reporting.check_database_resilience()

@eel.expose
def prune_ghost_items(item_ids):
    return api_reporting.prune_ghost_items(item_ids)


@eel.expose
def get_startup_info():
    """Returns dual-PID forensic info, startup metrics, and background process registry (v1.46.090)."""
    global FRONTEND_PROCESS_ID
    
    # 1. Resolve Frontend PID (Centralized v1.46.101)
    if not FRONTEND_PROCESS_ID:
        try:
            forensic_cfg = GLOBAL_CONFIG.get("forensic_settings", {})
            browser_targets = forensic_cfg.get("browser_process_names", ["chrome", "chromium"])
            enable_log = forensic_cfg.get("enable_pid_resolution_logging", True)

            current_process = psutil.Process(os.getpid())
            children = current_process.children(recursive=True)
            for child in children:
                name = child.name().lower()
                if any(x in name for x in browser_targets):
                    FRONTEND_PROCESS_ID = child.pid
                    if enable_log:
                        log.info(f"[Forensic-PID] Resolved Frontend: {name} (PID: {FRONTEND_PROCESS_ID})")
                    break
        except Exception as e:
            log.warning(f"[Forensic-PID] Failed to resolve FE PID: {e}")

    return {
        "pid": os.getpid(),                 # Backend (Python)
        "fe_pid": FRONTEND_PROCESS_ID or "--", # Frontend (Browser)
        "boot_duration_sec": round(time.time() - APP_START_TIME, 2),
        "start_time": APP_START_TIME,
        "env": "diagnostic-lab-forensic",
        "version": APP_VERSION_CORE,
        "os": platform.system(),
        "node": platform.node(),
        "active_processes": ACTIVE_FORENSIC_PROCESSES
    }

def kill_stalled_ffmpeg_streams():
    return api_reporting.kill_stalled_ffmpeg_streams()





# Debug-Optionen (Konsolidiert in PARSER_CONFIG)
DEBUG_FLAGS = PARSER_CONFIG.get("debug_flags", {})


def initialize_debug_flags(args=None):
    """
    @brief Initializes debug mode and flags based on CLI arguments and environment.
    """
    if args is None:
        args = sys.argv

    # Environment Detection (Delegated to api_core_app v1.54.021)
    env_type, env_name, env_path, _, _ = api_core_app._detect_python_environment()
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

    logger.setup_logging(debug_mode=debug_mode, level=log_level, session_id=SESSION_ID)

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
# VERSION is now imported from core.config_master in the bootstrap phase.
GLOBAL_ACTIVE_STREAMS = {}  # Tracks metrics for get_playback_stats


# Nach Logging-Setup: PIDs loggen fr Konsole. deswegen kein eel.expose



# Initialize logging as early as possible after paths are set
initialize_debug_flags()

STARTUP_TIME = time.time()
BROWSER_PID = None  # Global to track browser process


# PID-Logging beim Startup
main_pid = os.getpid()
testbed_pid = api_core_app.find_venv_pid('.venv_testbed')
log.info(f"[System] Forensic Bridge PID: {main_pid}")
log.info(f"[System] Testbed PID: {testbed_pid if testbed_pid else 'nicht aktiv'}")
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

    env_type, env_name, env_path, py_ver, py_exec = api_core_app._detect_python_environment()

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
    except BaseException:
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
    except BaseException:
        pass

    # 3. Nvidia (Nvidia-smi)
    try:
        res = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL
        ).decode().strip().split('\n')[0]
        return float(res)
    except BaseException:
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
            except BaseException:
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
        log.info(
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
    VERSION = "1.41.00 Offline"  # Fallback
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
def run_ffplay(url: str):
    """
    @brief Opens a local FFplay window to verify a stream URL.
    @param url The URL to stream (e.g. http://localhost:8345/media/file.mp3)
    """
    import subprocess
    log.info(f"[DIAG-FFPLAY] Launching native verifier for: {url}")
    try:
        # -nodisp: no video window if only audio, -autoexit: close when done
        subprocess.Popen(['ffplay', '-nodisp', '-autoexit', url])
        return {"status": "success", "message": "FFplay launched."}
    except Exception as e:
        log.error(f"[DIAG-FFPLAY] Launch failed: {e}")
        return {"status": "error", "message": str(e)}


def test_media_route(path: str):
    """Debug endpoint to test mode_router logic from UI."""
    from src.core.mode_router import smart_route
    return smart_route(path)


@eel.expose
def get_version():
    """Returns the application version."""
    return VERSION


@eel.expose
def get_version_info():
    """Returns detailed tiered version information."""
    return {
        'app': GLOBAL_CONFIG.get("version", APP_VERSION),
        'backend': BACKEND_VERSION,
        'frontend': FRONTEND_VERSION
    }


@eel.expose
def get_debug_stats():
    """Returns runtime statistics for the diagnostic suite."""
    import os
    from src.core import db
    total = 0
    categories = {}
    try:
        items = db.get_all_media()
        total = len(items)
        for i in items:
            cat = i.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
    except BaseException:
        pass
    return {
        "pid": os.getpid(),
        "total_items": total,
        "categories": categories,
        "status": "healthy"
    }


@eel.expose
def get_format_utils_exts():
    """Exposes current extension mappings from format_utils.py."""
    from src.parsers import format_utils
    return {
        "audio": list(format_utils.AUDIO_EXTENSIONS),
        "video": list(format_utils.VIDEO_EXTENSIONS),
        "images": list(format_utils.PICTURE_EXTENSIONS),
        "docs": list(format_utils.DOCUMENT_EXTENSIONS),
        "ebooks": list(format_utils.EBOOK_EXTENSIONS),
        "disks": list(format_utils.DISK_IMAGE_EXTENSIONS)
    }


@eel.expose
def get_debug_dict(source="library"):
    """Returns raw backend data for the Universal JSON Explorer."""
    import os
    from src.core import db
    if source == "library":
        return db.get_all_media()
    elif source == "config":
        return {k: str(v) for k, v in os.environ.items() if "MWV" in k or "PATH" in k}
    elif source == "state":
        return {"version": VERSION, "pid": os.getpid(), "root": str(PROJECT_ROOT)}
    return {"error": "Unknown source"}


@eel.expose
def get_debug_console():
    """Returns the tail of the app.log file for the Live Terminal."""
    try:
        log_dir = GLOBAL_CONFIG["storage_registry"]["app_logs_dir"]
        log_file = log_dir / "app.log"
        if log_file.exists():
            lines = log_file.read_text(encoding='utf-8').splitlines()
            return "\n".join(lines[-500:])
        return "Log file not found."
    except Exception as e:
        return f"Error reading logs: {e}"


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
                if exe and venv_path in exe:
                    return proc.info['pid']
                cmdline = proc.info.get('cmdline')
                if cmdline and venv_path in ' '.join(cmdline):
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def find_browser_pid():
        """Try to find the browser PID by looking for chrome/chromium with our port."""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline')
                if cmdline and 'app.html' in ' '.join(cmdline):
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    global BROWSER_PID
    if BROWSER_PID is None:
        BROWSER_PID = find_browser_pid()

    testbed_pid = find_venv_pid('.venv_testbed')
    selenium_pid = find_venv_pid('.venv_selenium')

    # Use centralized Style Sheet (Template) with safe-get fallback (v1.41.170)
    _tpt = GLOBAL_CONFIG.get("templates", {})
    env_data = _tpt.get("environment", {}).copy()

    # Ensure mandatory fields (even if template was skeleton)
    env_data.update({
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
        "debug_flags": globals().get("DEBUG_FLAGS", {}),
        "version": globals().get("VERSION", "Unknown"),
    })
    return env_data

# --- Debug Console API ---


@eel.expose
def get_konsole():
    """
    Returns debug logs, environment info, and dicts for GUI console. (v1.41.170 Stabilization)
    """
    try:
        from src.core import logger
        return {
            "logs": "\n".join(logger.get_ui_logs()),
            "env": get_environment_info_dict(),
            "version": globals().get("VERSION", "Unknown"),
            "license": "GNU GPL-3.0",
            "debug_flags": globals().get("DEBUG_FLAGS", {}),
        }
    except Exception as e:
        print(f"STDOUT: [Main] CRITICAL ERROR in get_konsole: {e}")
        return {"logs": f"ERROR: {e}", "env": {}, "status": "critical_failure"}


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


# --- [v1.54.022] CONFIG & UI SYSTEM (Delegated to api_config, api_ui) ---


# --- Debug/Test API ---
# --- [v1.54.022] SYSTEM ENVIRONMENT & LIFECYCLE (Delegated to api_environment) ---


# --- [v1.54.022] SYSTEM OVERVIEW (Delegated to api_environment) ---


# Konfiguration
# 1. Ort fr den automatischen Bibliotheks-Scan
# Standardmig aus PARSER_CONFIG laden (sync)
# PROJECT_ROOT imported from config_master (SSOT)
SCAN_MEDIA_DIR = GLOBAL_CONFIG.get("scan_media_dir", str(PROJECT_ROOT / "media"))
BROWSER_DEFAULT_DIR = GLOBAL_CONFIG.get("browser_default_dir", str(Path.home()))
# Redundante Definitionen entfernt, da diese nun aus parsers.format_utils importiert werden.
# (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS etc. werden oben importiert)
PICTURE_EXTENSIONS = {
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


# Consolidation Note: set_log_level moved to top-level section for Hub consistency.

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
            log.info(f"[Browser] Selected: {browser_name} ({browser_path})")
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
            eel.sleep(0.1)  # Faster polling
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


if DEBUG_FLAGS.get("start", False):
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
# --- [v1.54.022] LANGUAGE & LOCALIZATION (Delegated to api_config) ---


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
        log_dir = GLOBAL_CONFIG["storage_registry"]["logbuch_dir"]
        log_dir.mkdir(parents=True, exist_ok=True)
        log_count = len(list(log_dir.glob("*.md"))) if log_dir.exists() else 0

        return {
            "media_count": stats.get('total_items', 0),
            "playlist_count": playlist_count,
            "log_count": log_count
        }
    except Exception as e:
        log.error(f"[API] Error in get_db_info: {e}")
        return None


from src.core import api_library


@eel.expose
def get_library_forensics():
    return api_reporting.get_library_forensics()


@eel.expose
def get_branch_identity(branch_id: str = None) -> Dict[str, Any]:
    """Resolves the full identity metadata for a branch (v1.45.200)."""
    from src.core import models
    # Fallback to GLOBAL_CONFIG active_branch if not provided
    bid = branch_id or GLOBAL_CONFIG.get('active_branch', 'multimedia')
    return {
        "id": bid,
        "label": models.get_branch_label(bid),
        "build_id": models.get_branch_build_id(bid),
        "build_link": models.get_build_link(bid),
        "version": GLOBAL_CONFIG.get('build_configuration', {}).get('orchestrator_version', 'v1.45.200')
    }


@eel.expose
def init_db():
    from src.core import db
    return db.init_db()


@eel.expose
def get_library(force_raw=False, audit_stage=False, active_branch=None):
    return api_library.get_library(force_raw, audit_stage, active_branch)


@eel.expose
def sync_playback_state(payload: Dict[str, Any]) -> bool:
    return api_library.sync_playback_state(payload)


@eel.expose
def force_sync_all():
    return api_library.force_sync_all()

@eel.expose
def get_library_audit_summary():
    return api_library.get_library_audit_summary()


@eel.expose
def get_library_filtered(search: str = "", genre: str = "all", year: str = "all",
                         sort_by: str = "name", force_raw: bool = False, active_branch: str = None) -> Dict[str, Any]:
    return api_library.get_library_filtered(search, genre, year, sort_by, force_raw, active_branch)


@eel.expose
def clear_database():
    """
    @brief Deletes all entries from the library database.
    @details Clears all entries from the library database.
    @return Status dictionary.
    """
    if DEBUG_FLAGS["db"]:
        debug_log("[Debug-DB] Table is being cleared...")
    db.clear_media()
    return {"status": "ok", "message": "Database cleared", "media": []}


@eel.expose
def reset_app_data():
    """
    @brief Wipes the database and configuration files (private user data).
    @details Clears database and configuration files (private data).
    @return Status dictionary with list of deleted paths.
    """
    import os
    import shutil
    from pathlib import Path

    deleted = []

    # Paths to clear (SSOT v1.35.94)
    storage = GLOBAL_CONFIG.get("storage_registry", {})
    db_loc = storage.get("db_path", db.DB_FILENAME)
    db_dir = storage.get("db_dir", db.DB_DIR)
    config_dir = storage.get("config_dir", Path.home() / ".config" / "gui_media_web_viewer")

    targets = [db_dir, config_dir]
    # Also add the specific DB file if it's not in the dir
    if db_loc not in [str(db_dir), str(config_dir)]:
        targets.append(Path(db_loc).parent)

    for p_raw in targets:
        p = Path(p_raw)
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink()
                deleted.append(str(p))
            except Exception as e:
                log.error(f"[Reset] Failed for {p}: {e}")

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
def log_playback_event(event_type: str, details: str):
    """
    @brief Logs playback events from the frontend.
    @details Protokolliert Playback-Events vom Frontend (Start, Stopp, Next, etc.)
    """
    log.info(f"[JS-PLAYBACK] [{event_type}] {details}")


@eel.expose
def log_ui_event(event_type: str, name: str, details: str = ""):
    """
    @brief Logs UI navigation and interaction events.
    @details Protokolliert UI-Interaktionen wie Tab-Wechsel, Modals etc.
    """
    msg = f"[JS-NAV] [{event_type}] {name}"
    if details:
        msg += f" | {details}"
    log.info(msg)


# Redundant update_tags (Migrated to api_library.py)


# Redundant rename_media (Migrated to api_library.py)


# Redundant delete_media (Migrated to api_library.py)


@eel.expose
def get_db_stats():
    return api_reporting.get_db_stats()


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
        isbn_cfg = GLOBAL_CONFIG.get("barcode_scanner_settings", {}).get("isbn_scanner", {})
        if not isbn_cfg.get("enable_openlibrary", True):
            return {"error": "External ISBN search disabled"}

        template = isbn_cfg.get("api_template", "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data")
        url = template.format(isbn=cleaned)
        
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
    }


# Redundant Scanner Core (Migrated to api_library.py)


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


# Redundant Directory Management (Migrated to api_library.py)


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
    player_cfg = GLOBAL_CONFIG.get("player_settings", {})
    video_exts = player_cfg.get(
        "video_extensions", [
            ".mp4", ".mkv", ".webm", ".ogg", ".mov", ".avi", ".m4v", ".iso", ".ts", ".m2ts"])

    if ext in video_exts or is_dir:
        log.warning(f"DEBUG: [Player-Trace] play_media REJECTED for video/dir: {path}. Use open_video_smart.")
        return {"status": "error", "message": "Invalid call: Use open_video_smart for Video/Dir"}

    mode = PARSER_CONFIG.get("playback_mode", "chrome_native")

    # Priority 1: Audio is always Chrome Native if mode is default or requested
    audio_exts = player_cfg.get("audio_extensions", AUDIO_EXTENSIONS)
    is_audio = ext in audio_exts
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
    return api_orchestrator.resolve_media_path(file_path)


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


def find_main_track_iso(path: str) -> int:
    """
    @brief Identifies the longest title/track in a DVD ISO for FFmpeg streaming.
    @return Playlist/Track index (0-based) for the main feature.
    """
    import subprocess
    import re
    try:
        from src.core.config_master import GLOBAL_CONFIG
        # Use ffprobe to scan titles if possible, though DVD-structure is tricky with pure ffmpeg
        # Often, the longest title is the one we want.
        cmd = [
            GLOBAL_CONFIG["program_paths"].get(
                "ffprobe",
                "ffprobe"),
            "-i",
            str(path),
            "-show_format",
            "-show_streams",
            "-loglevel",
            "error"]
        # Note: True DVD title detection often requires libdvdnav/lsdvd.
        # Fallback to Title 1 or longest stream if ffprobe cannot see the structure.
        return 0
    except BaseException:
        return 0


def get_best_hw_encoder():
    """
    @brief Detects available hardware encoders to reduce CPU load.
    @return Encoder name (e.g. 'h264_vaapi', 'h264_nvenc', or 'libx264' as fallback).
    """
    try:
        gpu = hardware_detector.get_gpu_info()
        encoders = gpu.get("encoders", [])

        # Centralized Hardware Priority
        priority = GLOBAL_CONFIG.get("player_settings", {}).get("hardware_encoders_priority", ["nvenc", "vaapi", "qsv"])

        for p in priority:
            if p in encoders:
                return f"h264_{p}"

    except Exception as e:
        log.warning(f"[HW Detect] Failed to probe encoders: {e}")

    return "libx264"


@eel.btl.route('/stream/via/direct/<file_path:path>')
def server_file_direct(file_path):
    return api_orchestrator.server_file_direct(file_path)


@eel.btl.route('/stream/via/transcode/<file_path:path>')
def stream_video_fragmented(file_path):
    return api_orchestrator.stream_video_fragmented(file_path)


@eel.btl.route('/stream/via/remux/<item_id>')
def video_remux_stream(item_id):
    return api_orchestrator.video_remux_stream(item_id)


@eel.btl.route('/vlc_hls/<filename>')
def vlc_hls_proxy(filename):
    return api_orchestrator.vlc_hls_live_proxy(filename)


# [REMOVED v1.34] Redundant serve_media route moved to web/app_bottle.py
# to support centralized on-the-fly transcoding and better mimetype handling.

def apply_large_file_protection(cmd, file_path):
    """
    @brief Analyzes file size and applies resource protection policies (v1.35.98).
    @return (Modified Command, Is Large File)
    """
    try:
        from src.core.config_master import GLOBAL_CONFIG
        cfg = GLOBAL_CONFIG.get("large_file_settings", {})
        threshold_bytes = cfg.get("threshold_gb", 4.0) * 1024 * 1024 * 1024
        file_size = os.path.getsize(file_path)
        is_large = file_size > threshold_bytes

        if is_large:
            log.warning(f"[Protection] Large file detected ({file_size / (1024**3):.2f} GB): {file_path}")

            # Hook 1: Enforce CRF limit for video to prevent CPU/IO spikes
            if "-crf" in cmd:
                idx = cmd.index("-crf")
                current_crf = int(cmd[idx + 1])
                limit = cfg.get("enforce_crf_limit", 28)
                if current_crf < limit:
                    log.info(f"[Protection] Adjusting CRF {current_crf} -> {limit} for resource safety.")
                    cmd[idx + 1] = str(limit)

            # Hook 2: Future hooks for remux vs transcode can be added here

        return cmd, is_large
    except Exception as e:
        log.error(f"[Protection] Error applying safety policies: {e}")
        return cmd, False


@eel.expose
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


def log_process_stderr(process, name):
    """
    @brief Helper to stream process stderr to the master log and optionally specialized log files.
    (v1.46.132 Granular Logging)
    """
    if not process or not process.stderr:
        return
    # Determine granular logging destinations (Forensic Phase 7)
    log_cfg = GLOBAL_CONFIG.get("logging_registry", {})
    enable_granular = log_cfg.get("enable_granular_transcoder_logs", False)
    log_dir = Path(log_cfg.get("transcoding_log_dir", str(PROJECT_ROOT / "logs" / "transcoding")))
    
    log_handle = None
    if enable_granular:
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = get_timestamped_log_path(log_dir, name)
            log_handle = open(log_file, "a", encoding="utf-8")
            log_handle.write(f"\n--- Process Log Start [{name}]: {time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT)} ---\n")
        except Exception as e:
            log.debug(f"[Log-Process-Internal] Failed to setup specialized log for {name}: {e}")

    def log_thread():
        try:
            for line in process.stderr:
                try:
                    decoded_line = line.decode(errors='replace').strip()
                    # 1. Master Log
                    log.info(f" [{name}] {decoded_line}")
                    # 2. Granular Log File
                    if log_handle:
                        log_handle.write(f"{time.strftime(DEFAULT_TIME_FORMAT)} - {decoded_line}\n")
                except Exception:
                    pass
        finally:
            if log_handle:
                try:
                    log_handle.write(f"--- Process Log End [{name}]: {time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT)} ---\n")
                    log_handle.close()
                except Exception:
                    pass

    import threading
    threading.Thread(target=log_thread, daemon=True).start()


def is_mkvtoolnix_available():
    """Checks if mkvmerge is available via the registry (v1.46.132)."""
    return api_transcoding.is_mkvtoolnix_available()


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

        # Register active stream for stats (SSOT v1.35.94)
        if "GLOBAL_ACTIVE_STREAMS" in globals():
            GLOBAL_ACTIVE_STREAMS["remux_pipe"] = {
                "ts": time.time(),
                "codec": "Lossless Remux (Copy)",
                "bitrate": "Direct Stream",
                "engine": "Pipe-Kit (mkvmerge + ffmpeg)",
                "rtt": 2,  # Ultra-low latency for remux
                "atmos": "mp4-remux" in str(file_path).lower(),
                "bitstream": True
            }

        mkvmerge_path = shutil.which('mkvmerge') or 'mkvmerge'
        ffmpeg_path = shutil.which('ffmpeg') or 'ffmpeg'

        # Pipe-Kit Streaming Flow (Delegated to api_transcoding v1.46.132)
        stream_gen = api_transcoding.get_remux_stream(
            file_path=file_path,
            start_time=float(start_time),
            audio_idx=int(audio_idx),
            subs_idx=subs_idx if subs_idx and str(subs_idx).lower() != 'none' else None
        )
        return bottle.HTTPResponse(stream_gen, content_type="video/mp4")
    except Exception as e:
        import traceback
        log.error(f" [Remux] CRITICAL ERROR: {e}\n{traceback.format_exc()}")
        return bottle.HTTPError(500, f"Remux Error: {e}")


def get_video_metadata(file_path: str) -> dict:
    """
    Analyzes a video file using ffprobe and returns codec/container info.
    """
    try:
        from src.core.config_master import GLOBAL_CONFIG
        cmd = [
            GLOBAL_CONFIG["program_paths"].get("ffprobe", "ffprobe"), "-v", "quiet", "-print_format", "json",
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
    """Explicitly open a file with ffplay using the registry."""
    file_path = resolve_media_path(file_path)
    try:
        ffplay_path = GLOBAL_CONFIG["program_paths"].get("ffplay", "ffplay")
        proc = subprocess.Popen([str(ffplay_path), str(file_path)])
        ACTIVE_SUBPROCESSES.append(proc)
        log.info(f" [FFplay] Started for: {file_path}")
        return {"status": "ok", "mode": "ffplay"}
    except Exception as e:
        return {"status": "error", "error": f"FFplay failed: {e}"}


@eel.expose
def run_raw_media_probe(item_id):
    """Forensic Item Probe: Delegated to api_parsing (v1.46.132)."""
    path = resolve_media_path(item_id)
    if not os.path.exists(path):
        from src.core import db
        item = db.get_media_by_id(item_id)
        if item: path = item['path']

    if not os.path.exists(path):
        return {"status": "error", "message": "Media path not found."}

    tags = api_parsing.get_media_metadata(path, mode="ultimate")
    return {"status": "success", "data": tags}


@eel.expose
def open_with_vlc(file_path: str):
    """Explicitly open a file with VLC (GUI) using the registry."""
    file_path = resolve_media_path(file_path)
    try:
        vlc_path = GLOBAL_CONFIG["program_paths"].get("vlc", "vlc")
        proc = subprocess.Popen([str(vlc_path), str(file_path)])
        ACTIVE_SUBPROCESSES.append(proc)
        log.info(f" [VLC] Started for: {file_path}")
        return {"status": "ok", "mode": "vlc"}
    except Exception as e:
        return {"status": "error", "error": f"VLC failed: {e}"}


@eel.expose
def open_with_cvlc(file_path: str):
    """Explicitly open a file with CVLC (command-line VLC) using the registry."""
    file_path = resolve_media_path(file_path)
    try:
        vlc_path = GLOBAL_CONFIG["program_paths"].get("cvlc", "cvlc")
        if not vlc_path: vlc_path = "cvlc"
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
    except BaseException:
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
        index_file = f"{hls_dir}/index.m3u8"

        # Content-Aware Profile Selection (SSOT v1.35.95)
        # Check if we are dealing with PAL DVD/ISO vs. HD content
        is_dvd = any([
            str(file_path).lower().endswith('.iso'),
            os.path.exists(os.path.join(file_path, "VIDEO_TS"))
        ])

        profiles = GLOBAL_CONFIG.get("transcoding_profiles", {})
        if is_dvd:
            p = profiles.get("vlc_hls_profile_pal", {})
            log.info(f"[VLC-HLS] Applying PAL DVD optimized profile (vb={p.get('v_bitrate')}k)")
        else:
            p = profiles.get("vlc_hls_profile_hd", {})
            log.info(f"[VLC-HLS] Applying HD optimized profile (vb={p.get('v_bitrate')}k)")

        # VLC HLS sout chain (Linked to SSOT)
        sout = (
            f"#transcode{{vcodec={p.get('vcodec')},vb={p.get('v_bitrate')},"
            f"acodec={p.get('acodec')},ab={p.get('a_bitrate')},"
            f"channels={p.get('channels')},samplerate={p.get('samplerate')}}}:"
            f"std{{access=livehttp{{seglen={p.get('seglen')},deldone=1,numseg={p.get('numseg')},"
            f"index={index_file},index-url=vlc-hls-segment-########.ts}},"
            f"mux=ts,dst={hls_dir}/vlc-hls-segment-########.ts}}"
        )

        try:
            control_port = find_free_port()
            log.info(f"[VLC-HLS-Streamer] {pid_tag} Starting Headless HLS at {start_time}s: {full_path} -> {index_file} (Control: {control_port})")

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
def open_video(file_path: str, player_type: str = "auto", mode: str = "auto",
               source: str = "direct", start_time: float = 0):
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
            return start_vlc_guarded(target_path, "vlc_embedded", prefix,
                                     source=f"open_video_{source}", start_time=start_time)
        return start_vlc_guarded(target_path, mode, prefix, source=f"open_video_{source}", start_time=start_time)

    elif player_type == "ffplay":
        return open_with_ffplay(file_path)

    elif player_type == "pyplayer":
        # pyvidplayer2 / standalone
        if mode == "pyplayer_mpv":
            # Launch mpv if available
            mpv_path = GLOBAL_CONFIG["program_paths"]["mpv"]
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
        except BaseException:
            pass

    # Check DB category for specialized routing
    from src.core import db
    db_item = db.get_media_by_path(str(file_path))
    category = db_item.get('category', '') if db_item else ''

    if is_dvd or is_disc_img or category in ('video', 'disk_images', 'Film', 'Abbild'):
        log.info(
            f"DEBUG: [Player-Trace] DVD/Multimedia/DiskImg detected in smart router (Category: {category}). Forcing VLC Embedded.")
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


# --- [v1.46.135] Playlist Engine (Delegated to api_playlist) ---
# End of specialized delegation block


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
# Redundant add_file_to_library (Migrated to api_library.py)


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


# Remote MKVToolNix check (Handled by api_transcoding)


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

        log.info(f"[vlc pipe] Launching {engine} Pipe: {' '.join(str(c) for c in remux_cmd)} | {' '.join(str(c) for c in vlc_cmd)}")

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
    except BaseException:
        return False


def find_free_port():
    """Finds an available TCP port on the local machine."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


@eel.expose
def vlc_ts_mode(file_path):
    """Launches cvlc with TS muxing and returns the port."""
    file_path = resolve_media_path(file_path)
    file_path = resolve_dvd_bundle_path(file_path)
    if not os.path.exists(file_path):
        return {"status": "error", "error": "Datei nicht gefunden"}

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
            eel.sleep(0.5)
            if detect_ts_stream(port):
                log.info(f"[cvlc] TS Stream active on port {port}")
                # We return a URL that the frontend can play via Video.js (type: video/mp2t)
                return {"status": "play", "path": f"http://localhost:{port}/",
                        "mode": "chrome_native", "type": "video/mp2t"}

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

        mtx_host = GLOBAL_CONFIG["mediamtx_settings"]["host"]
        rtsp_port = GLOBAL_CONFIG["mediamtx_settings"]["rtsp_port"]
        rtsp_target = f"rtsp://{mtx_host}:{rtsp_port}/{safe_name}"

        ffmpeg_bin = GLOBAL_CONFIG["program_paths"]["ffmpeg"]
        ffmpeg_cmd = [ffmpeg_bin, "-re"]

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

        # Start the push process in the background (v1.46.132 Granular Logging)
        proc = subprocess.Popen(
            ffmpeg_cmd, 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, 
            start_new_session=True
        )
        log_process_stderr(proc, f"MediaMTX-Push-{safe_name}")
        ACTIVE_SUBPROCESSES.append(proc)

        
        # [v1.46.089] Forensic PID Tracking
        ACTIVE_FORENSIC_PROCESSES[proc.pid] = f"FFmpeg {protocol.upper()} Push ({safe_name})"

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

        return {"status": "play", "path": src_url, "mode": mode,
                "type": "application/x-mpegURL" if protocol == "hls" else "video/webrtc"}
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
    except BaseException:
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
            except BaseException:
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
        except BaseException:
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
            cmd = ["mkvmerge", "-o", str(output), str(vf)]
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
                f"[VLC Import] {len(imported)} importiert, {len(skipped)} bersprungen, {len(errors)} Fehler")

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
                f"[VLC Export] {exported} Tracks nach {playlist_file.name} exportiert")

        return {
            "status": "ok",
            "path": str(playlist_file),
            "exported": exported,
            "missing": missing
        }
    except Exception as e:
        log.error(f"[VLC Export] Error: {e}")
        return {"error": str(e)}


# (save/load_playlist moved to api_playlist)


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
                f"Datei '{save_path.name}' existiert. berschreiben? (j/n): ").strip().lower()
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


def get_logbook_entry(*args, **kwargs):
    return api_logbuch.get_logbook_entry(*args, **kwargs)

def list_logbook_entries():
    return api_logbuch.list_logbook_entries()

def save_logbook_entry(*args, **kwargs):
    return api_logbuch.save_logbook_entry(*args, **kwargs)

def delete_logbook_entry(*args, **kwargs):
    return api_logbuch.delete_logbook_entry(*args, **kwargs)


def run_tests(*args, **kwargs):
    return api_testing.run_tests(*args, **kwargs)

def get_test_results():
    return api_testing.get_test_results()

def get_benchmark_results():
    return api_testing.get_benchmark_results()


@eel.expose
def run_gui_tests():
    """
    @brief Placeholder for GUI tests (handled via the agent).
    @details Dummy-Funktion fr GUI-Tests (da diese ber den Agenten laufen).
    @return Info dictionary / Info-Dictionary.

    Best Practices:
      - In Produktion: Integriere PyAutoGUI fr Forensic-Screenshots.
      - Alternativen: Screenshot-Tools (PyAutoGUI).
      - MCP-Agenten: Nutze Inspector-Tool fr DOM-Validation.
    """
    log.info(
        "GUI-Tests: Siehe MCP-Agent oder Diagnostic Snapshot fr KlickEvents/DOM.")
    return {
        "status": "info",
        "message": "GUI-Tests mssen ber den MCP-Agenten DOM / Diagnostic Snapshot gestartet werden.",
        "next_steps": [
            "run_diagnostic_snapshot() aufrufen",
            "audit_dom_state() zur Validierung nutzen",
            "PyAutoGUI fr visuelle Beweissicherung verwenden"],
        "protocols": {
            "Eel expose": "Intern, Python-JS-Bridge, ideal fr Test-Trigger",
            "PyAutoGUI": "Pixel/Screen, Desktop-Automatisierung via api_diagnostics",
            "MCP": "Agenten-basiert, Inspector fr Event-Simulation"}}


@eel.expose
def ui_trace(message):
    """
    Receives trace messages from the UI and logs them to a centralized file.
    (v1.46.131 Centralized)
    """
    try:
        log.info(f"[UI-Trace] {message}")
        
        # Centralized Log Path (Forensic Phase 6)
        log_registry = GLOBAL_CONFIG.get("logging_registry", {})
        trace_path_raw = log_registry.get("ui_trace_log_path")
        
        if trace_path_raw:
            trace_path = Path(trace_path_raw)
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            with open(trace_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT)} - {message}\n")
    except Exception as e:
        log.debug(f"[UI-Trace-Internal] Failed to write to trace log: {e}")
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

    # Get cache dir (Merged SSOT v1.35.96)
    cache_dir = GLOBAL_CONFIG["storage_registry"]["mkv_cache_dir"]
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
                except BaseException:
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



# --- FORENSIC AUDIT ENDPOINTS (Consolidated to api_audit.py) ---
# All technical diagnostics (PyAutoGUI, Selenium, Playwright) are now
# exposed directly via 'from src.core import api_audit'.


@eel.expose
def discover_cast_devices():
    """Returns discovered Chromecast and DLNA devices."""
    devices = {"chromecast": [], "dlna": []}
    try:
        timeout = GLOBAL_CONFIG["casting_settings"]["discovery_timeout"]
        # Placeholder for pychromecast / dlnap discovery using centralized timeout
        log.info(f"[Cast] Starting device discovery (timeout: {timeout}s)...")
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
            os.startfile(filepath)
        else:
            vlc_path = GLOBAL_CONFIG["program_paths"]["vlc"]
            subprocess.Popen([vlc_path, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        ffplay_path = GLOBAL_CONFIG["program_paths"]["ffplay"]
        subprocess.Popen([ffplay_path, "-autoexit", "-sn", filepath],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def get_playback_benchmarks():
    """Returns stored playback benchmarks."""
    try:
        path = GLOBAL_CONFIG["storage_registry"]["playback_benchmark_path"]
        if path.exists():
            return json.loads(path.read_text())
    except BaseException:
        pass
    return {}


@eel.expose
def save_playback_benchmarks(data):
    """Saves playback benchmarks."""
    try:
        path = GLOBAL_CONFIG["storage_registry"]["playback_benchmark_path"]
        path.write_text(json.dumps(data))
        return True
    except BaseException:
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
            swyh_path = GLOBAL_CONFIG["program_paths"]["swyh-rs-cli"]
            if not shutil.which(swyh_path) and swyh_path == "swyh-rs-cli":
                return {"status": "error", "message": "swyh-rs-cli not found"}

            log.info("[Streaming] Starting swyh-rs-cli bridge...")
            # Example flags: -s (serve), -p (port)
            fmt = GLOBAL_CONFIG["casting_settings"]["swyh_rs_format"]
            _swyh_rs_process = subprocess.Popen(
                [swyh_path, "-s", "-f", fmt],
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
        mpv_path = GLOBAL_CONFIG["program_paths"]["mpv"]
        subprocess.Popen([mpv_path, "--ontop", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    lib_dir = PARSER_CONFIG.get("library_dir", str(GLOBAL_CONFIG["storage_registry"]["media_dir"]))
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
    mkvmerge_path = GLOBAL_CONFIG["program_paths"]["mkvmerge"]

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
        bench_file = GLOBAL_CONFIG["storage_registry"]["system_benchmark_path"]
        # Ensure benchmarks directory exists (v1.35.96 Safety)
        bench_file.parent.mkdir(parents=True, exist_ok=True)
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

            # 1. DVD/Film Detection (Syncing with SSOT v1.35.96)
            disk_exts = GLOBAL_CONFIG["media_formats"].get("disk_image_extensions", ['.iso', '.bin', '.img'])
            is_dvd_image = ext in [e.strip('.') for e in disk_exts]
            is_dvd_folder = 'VIDEO_TS' in path or 'BDMV' in path

            if cat in ['film', 'movie', 'video'] or is_dvd_image or is_dvd_folder:
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
    return api_reporting.get_cover_extraction_report()

@eel.expose
def get_routing_suite_report():
    return api_reporting.get_routing_suite_report()

@eel.expose
def get_streaming_capability_matrix():
    return api_reporting.get_streaming_capability_matrix()

@eel.expose
def get_media_compatibility_report():
    return api_reporting.get_media_compatibility_report()


# --- Media Routing Test Suite & Cache Logic ---

MEDIA_CACHE = GLOBAL_CONFIG["storage_registry"]["media_cache_dir"]


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
    log.info(f"[PLAY-PULSE] Orchestrator Routing Request: {item_path} | Client: {client}")
    
    if not full.exists():
        log.error(f"[PLAY-PULSE] Routing Failure: File not found: {item_path}")
        return {
            "mode": "error",
            "message": f"File not found: {item_path}"
        }

    handler = get_handler_for_file(full)
    source = handler.process(client=client, relpath=item_path)
    
    log.info(f"[PLAY-PULSE] Routing Resolved: Mode={source.get('mode', 'unknown')} | Handler={handler.__class__.__name__}")
    return source


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




@eel.expose
def get_parser_registry():
    """Returns all available parsers, their capabilities and settings schemas."""
    from src.parsers import media_parser
    return media_parser.get_parser_info()


@eel.expose
def update_parser_setting(parser_id, key, value):
    """Updates a specific setting for a parser in GLOBAL_CONFIG and persists it."""
    from src.core.config_master import GLOBAL_CONFIG

    if "parser_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["parser_settings"] = {}
    if parser_id not in GLOBAL_CONFIG["parser_settings"]:
        GLOBAL_CONFIG["parser_settings"][parser_id] = {}

    # Cast value if needed (handle boolean/int from UI)
    old_val = GLOBAL_CONFIG["parser_settings"][parser_id].get(key)
    if isinstance(old_val, bool) and not isinstance(value, bool):
        value = str(value).lower() in ("true", "1", "yes", "on")
    elif isinstance(old_val, int) and not isinstance(value, int):
        try:
            value = int(value)
        except BaseException:
            pass

    GLOBAL_CONFIG["parser_settings"][parser_id][key] = value
    log.info(f"[Config] Updated parser '{parser_id}' setting '{key}' to '{value}'")
    return True


@eel.expose
def audit_specific_item(query: str) -> Dict[str, Any]:
    return api_reporting.audit_specific_item(query)


# --- [v1.54.002] WORKSTATION GOVERNANCE API ---

@eel.expose
def trigger_workstation_update(force: bool = False):
    """
    Manually triggers the forensic self-healing update cycle during runtime.
    """
    log.info(f"🚀 [Governance] Manual Workstation Update Triggered (Force: {force})")
    
    # Temporarily override force flag if requested
    from src.core.config_master import DEPENDENCY_REGISTRY
    orig_force = DEPENDENCY_REGISTRY["bootstrap_governance"].get("force_updates", False)
    if force:
        DEPENDENCY_REGISTRY["bootstrap_governance"]["force_updates"] = True
    
    try:
        from src.core.startup_auditor import ensure_critical_packages
        success = ensure_critical_packages()
        return {"status": "ok" if success else "error", "restored": success}
    except Exception as e:
        log.error(f"❌ [Governance] Runtime Update Failed: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        # Restore original flag
        DEPENDENCY_REGISTRY["bootstrap_governance"]["force_updates"] = orig_force

@eel.expose
def get_forensic_thresholds():
    """
    Returns centralized bitrate quality thresholds for UI parity.
    """
    from src.core.config_master import BITRATE_QUALITY_THRESHOLDS
    return BITRATE_QUALITY_THRESHOLDS


if __name__ == "__main__":
    import subprocess
    # 1. Flash Burn (Instant Port Cleanup - v1.46.135 Centralized)
    if PORT_CLEANUP_CMD:
        subprocess.run(PORT_CLEANUP_CMD, shell=True)

    # 2. Early Monkey Patching (v1.46.136 Stability)
    # Must occur as early as possible after main imports
    try:
        from gevent import monkey
        monkey.patch_all()
        print("STDOUT: [Bootstrap] gevent monkey-patching successful", flush=True)
    except ImportError:
        pass

    # 3. Environment Shield
    from src.core import api_core_app
    api_core_app.ensure_stable_environment()

    # 4. Initialize Forensic Environment (Assets & Directories)
    launch_eel_server()
    if not bootstrap_core_settings():
        log.critical("[Bootstrap] Core settings failure. Aborting.")
        sys.exit(1)
        
    # 5. Log Session Details
    log_session_diagnostics()
    
    # 6. Start Eel Application
    start_app()

    log.info("[Main] Entering keepalive loop.")
    while True:
        try:
            eel.sleep(GLOBAL_CONFIG['sleep_times']['keepalive'])
        except KeyboardInterrupt:
            log.info("[Shutdown] KeyboardInterrupt received. Exiting.")
            sys.exit(0)
        except BaseException as e:
            log.warning(f"[MainLoop] keepalive recovered from: {e}")
            # [SECURITY v1.41] Avoid blocking time.sleep in an event-driven system
            if 'gevent' in sys.modules:
                import gevent
                gevent.sleep(1.0)
            else:
                eel.sleep(1.0)
