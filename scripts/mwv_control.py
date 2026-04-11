#!/usr/bin/env python3
import sys
import os
import argparse
from pathlib import Path
import subprocess
import time

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Setup dummy logger for the manager
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("mwv_control")

def main():
    parser = argparse.ArgumentParser(description="MWV Control Utility")
    parser.add_argument("--start", action="store_true", help="Start the MWV application")
    parser.add_argument("--stop", action="store_true", help="Stop all MWV instances and browsers")
    parser.add_argument("--restart", action="store_true", help="Restart the MWV application")
    parser.add_argument("--clean", action="store_true", help="Perform deep cleanup (kill all stale processes)")
    parser.add_argument("--port", type=int, default=8345, help="Port to use (default: 8345)")
    args = parser.parse_args()

    # Import process manager lazily
    from src.core.process_manager import ProcessController
    
    # App Data Dir (standard location)
    app_data_dir = Path.home() / ".local" / "share" / "gui_media_web_viewer"
    if sys.platform == "win32":
        app_data_dir = Path(os.environ.get("APPDATA", ".")) / "gui_media_web_viewer"
    
    pm = ProcessController(PROJECT_ROOT, app_data_dir)

    if args.stop or args.restart or args.clean:
        log.info("Stopping all MWV-related processes...")
        pm.cleanup_environment()
        if args.stop:
            return

    if args.start or args.restart:
        log.info(f"Starting MWV on port {args.port}...")
        
        # Check if another instance is still locking (unlikely after cleanup)
        owner = pm.get_lock_owner()
        if owner:
            log.warning(f"Lock file still exists (Owner PID: {owner}). It may be stale.")
        
        env = os.environ.copy()
        env["MWV_PORT"] = str(args.port)
        
        try:
            # We use a detached process or just run it
            cmd = [sys.executable, str(PROJECT_ROOT / "src" / "core" / "main.py")]
            log.info(f"Executing: {' '.join(cmd)}")
            subprocess.Popen(cmd, env=env, start_new_session=True)
            log.info("MWV started successfully (background).")
        except Exception as e:
            log.error(f"Failed to start MWV: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
