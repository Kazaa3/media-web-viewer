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
    api_media_tools, api_subtitles, api_streaming, api_parsing
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


# --- CORE API EXPOSURE BRIDGE ---
# NOTE: Function definitions have been migrated to the following specialized modules:
# api_config, api_environment, api_ui, api_library, api_orchestrator, api_playback,
# api_file_browser, api_media_tools, and api_legacy_archive.
#
# DO NOT ADD NEW BUSINESS LOGIC HERE. Use the appropriate api_*.py module.


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
\n# --- CORE API EXPOSURE BRIDGE ---\n# All functional logic from lines 515-5599 has been moved to api_legacy_archive.py\n# and specialized domain API modules (api_library, api_playback, etc.)\n# to satisfy the v1.54.022 'Forensic Core Slimming' requirement.\n\n
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
