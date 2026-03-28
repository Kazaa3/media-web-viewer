import os
import sys
import psutil
import signal
import fcntl
import time
from pathlib import Path
import logging

# Use a local logger or the app logger if available
log = logging.getLogger("app.process")

class ProcessController:
    """
    Centralized controller for MWV process lifecycle.
    Handles singleton locking, process discovery, and forceful cleanup.
    """
    
    def __init__(self, project_root: Path, app_data_dir: Path):
        self.project_root = project_root
        self.lock_file = app_data_dir / "mwv.lock"
        self._lock_handle = None

    def kill_stale_instances(self, current_pid: int = None):
        """Discovers and terminates only project-related MWV processes."""
        print("STDOUT: kill_stale_instances() starting...", flush=True)
        if current_pid is None:
            current_pid = os.getpid()
            
        # Specific patterns can be killed globally
        global_patterns = ["chromedriver", "playwright-browser"]
        # Generic patterns MUST be within project root
        project_patterns = ["main.py", "chromium", "suite_", "eel", "node", "python"]
        count = 0
        
        project_root_str = str(self.project_root).lower()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                pid = proc.info['pid']
                if pid == current_pid:
                    continue
                
                cmdline = proc.info.get('cmdline') or []
                cmd_str = " ".join(cmdline).lower()
                
                is_global_match = any(p in cmd_str for p in global_patterns)
                is_project_match = any(p in cmd_str for p in project_patterns)
                is_in_project = project_root_str in cmd_str
                
                if is_global_match or (is_project_match and is_in_project):
                    # SAFETY: Additional check to avoid killing common apps
                    if any(x in cmd_str for x in ["vscode", "discord", "slack", "chrome-extension"]):
                        continue
                        
                    log.info(f"[Process] Terminating project process: {proc.info['name']} (PID: {pid})")
                    proc.send_signal(signal.SIGTERM)
                    try:
                        proc.wait(timeout=0.5)
                    except psutil.TimeoutExpired:
                        proc.kill()
                    count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Explicit check for port 8345
        self.kill_by_port(8345)
        
        if count > 0:
            log.info(f"[Process] Cleaned up {count} stale processes.")
        return count

    def kill_by_port(self, port: int):
        """Kills any process listening on the specified port."""
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                try:
                    proc = psutil.Process(conn.pid)
                    log.info(f"[Process] Port {port} occupied by {proc.name()} (PID: {conn.pid}). Killing...")
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    def acquire_lock(self) -> bool:
        """Acquires the file-based singleton lock. Returns True if successful."""
        print(f"STDOUT: Locking {self.lock_file}...", flush=True)
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._lock_handle = open(self.lock_file, "a+")
            fcntl.lockf(self._lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # Write current PID
            self._lock_handle.seek(0)
            self._lock_handle.truncate()
            self._lock_handle.write(f"{os.getpid()}\n")
            self._lock_handle.flush()
            return True
        except BlockingIOError:
            return False
        except Exception as e:
            log.error(f"[Process] Lock acquisition error: {e}")
            return False

    def release_lock(self):
        """Releases the singleton lock."""
        if self._lock_handle:
            try:
                fcntl.lockf(self._lock_handle, fcntl.LOCK_UN)
                self._lock_handle.close()
            except:
                pass
            self._lock_handle = None

    def get_lock_owner(self) -> int:
        """Returns the PID of the current lock owner, or 0 if none."""
        if not self.lock_file.exists():
            return 0
        try:
            with open(self.lock_file, "r") as f:
                content = f.read().strip()
                return int(content) if content.isdigit() else 0
        except:
            return 0

    def cleanup_environment(self):
        """Forces a clean environment by killing everything and clearing locks."""
        log.info("[Process] Performing full environment cleanup...")
        self.kill_stale_instances()
        if self.lock_file.exists():
            try: self.lock_file.unlink()
            except: pass
        log.info("[Process] Cleanup complete.")
