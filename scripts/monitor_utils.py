#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Monitoring Utilities
Handles process execution with hang detection, progress monitoring, and safe abortion.
"""

import subprocess
import time
import os
import signal
import sys
import psutil
from pathlib import Path
from typing import List, Optional, Callable, Dict


def print_monitor(message: str, category: str = "MONITOR"):
    """Print a monitor-specific status message."""
    icons = {"MONITOR": "🔍", "HANG": "🆘", "KILL": "💀", "ALIVE": "💓"}
    icon = icons.get(category, "•")
    print(f"{icon} {message}")

def kill_process_tree(pid: int):
    """Kill a process and all its children."""
    try:
        import psutil
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except: pass
        try:
            parent.kill()
        except: pass
    except (ImportError, Exception):
        # Fallback if psutil is missing or process gone
        try:
            os.kill(pid, signal.SIGKILL)
        except: pass

def run_monitored(
    cmd: List[str],
    cwd: Optional[str] = None,
    hang_timeout: int = 60,
    alive_interval: int = 15,
    on_output: Optional[Callable[[str], None]] = None,
    env: Optional[Dict[str, str]] = None,
    watch_files: Optional[List[str]] = None,
    watch_timeout: int = 120
) -> bool:
    """
    Run a command with hang detection.
    
    Args:
        cmd: Command and arguments.
        cwd: Working directory.
        hang_timeout: Seconds without output before considering it a hang.
        alive_interval: Seconds between "alive" markers if no output.
        on_output: Optional callback for each line of output.
        
    Returns:
        bool: True if process finished successfully, False on error or hang.
    """
    print_monitor(f"Starting monitored process: {' '.join(cmd)} (PID: pending)")
    
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    pid = process.pid
    print_monitor(f"Process started (PID: {pid})")
    
    last_output_time = time.time()
    last_alive_marker = time.time()
    
    # Watch file state
    watch_files_state = {}
    if watch_files:
        for f in watch_files:
            file_path = Path(f)
            if file_path.exists():
                watch_files_state[f] = file_path.stat().st_mtime
            else:
                watch_files_state[f] = 0.0
    
    try:
        fd = None
        if process.stdout is not None:
            try:
                import fcntl
                # Use getattr to avoid type checker issues with fileno
                fileno_func = getattr(process.stdout, 'fileno', None)
                if fileno_func:
                    fd = fileno_func()
                    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
            except (ImportError, AttributeError, Exception):
                # Non-critical: some platforms might not support fcntl
                pass


        while True:
            # Check for exit
            retcode = process.poll()
            
            # Try to read output
            line = ""
            if fd is not None and process.stdout:
                try:
                    line = process.stdout.readline()
                except IOError:
                    line = ""
            
            now = time.time()
                
            if now - last_output_time > hang_timeout:
                print_monitor(f"STDOUT HANG DETECTED! No activity for {int(now - last_output_time)}s.", "HANG")
                print_monitor(f"Aborting process tree (PID: {pid})...", "KILL")
                kill_process_tree(pid)
                return False
            
            # Check watched files
            if watch_files:
                for f in watch_files:
                    file_path = Path(f)
                    if file_path.exists():
                        mtime = file_path.stat().st_mtime
                        if mtime > watch_files_state[f]:
                            # File updated, reset watchdog
                            watch_files_state[f] = mtime
                            last_output_time = now
                        elif now - last_output_time > watch_timeout:
                             print_monitor(f"FILE WATCHDOG HANG! {f} stalled for {int(now - last_output_time)}s.", "HANG")
                             print_monitor(f"Aborting process tree (PID: {pid})...", "KILL")
                             kill_process_tree(pid)
                             return False
            
            # Print alive marker if needed
            if now - last_alive_marker > alive_interval:
                print_monitor(f"Process {pid} is still alive (no output for {int(now - last_output_time)}s).", "ALIVE")
                last_alive_marker = now
            
            # Small sleep to prevent busy waiting
            if not line:
                time.sleep(0.5)
            
            if retcode is not None:
                # Final check for remaining output
                if not line:
                    if retcode == 0:
                        print_monitor(f"Process {pid} finished successfully.", "MONITOR")
                        return True
                    else:
                        print_monitor(f"Process {pid} failed with exit code {retcode}.", "KILL")
                        return False
            
            if line:
                cb = on_output
                if cb is not None:
                    cb(line.strip())
                else:
                    print(f"  [output] {line.strip()}")
                last_output_time = now
                last_alive_marker = now
            
            # Safety break if process is gone but we missed it
            if process.poll() is not None:
                # One last attempt to read
                try:
                    out = process.stdout
                    cb = on_output
                    if out is not None:
                        line = out.readline()
                        if line: 
                            if cb is not None:
                                cb(line.strip())
                            else:
                                print(f"  [output] {line.strip()}")
                except Exception:
                    pass
                
                retcode = process.poll()
                return retcode == 0
                    
    except KeyboardInterrupt:
        print_monitor(f"Interrupted by user. Killing process {pid}...", "KILL")
        kill_process_tree(pid)
        raise
    except Exception as e:
        print_monitor(f"Unexpected error during monitoring: {e}", "KILL")
        kill_process_tree(pid)
        return False

if __name__ == "__main__":
    # Simple test: run a command that sleeps
    if len(sys.argv) > 1:
        run_monitored(sys.argv[1:])
    else:
        print("Usage: monitor_utils.py <cmd> <args>")
