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
            child.kill()
        parent.kill()
    except (ImportError, psutil.NoSuchProcess):
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
    env: Optional[Dict[str, str]] = None
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
    
    try:
        fd = None
        if process.stdout is not None:
            import fcntl
            fd = process.stdout.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


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
                print_monitor(f"HANG DETECTED! No output for {int(now - last_output_time)}s.", "HANG")
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
                if on_output:
                    on_output(line.strip())
                else:
                    print(f"  [output] {line.strip()}")
                last_output_time = now
                last_alive_marker = now
                    
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
