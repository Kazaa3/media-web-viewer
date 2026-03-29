import socket
import subprocess
import os
import sys
import time
import json
import signal
from pathlib import Path

def find_free_port():
    """Finds a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def start_managed_session(project_root):
    """Starts a managed Eel session on a dynamic port."""
    port = find_free_port()
    main_py = project_root / "src" / "core" / "main.py"
    
    # Environment variables for the child process
    env = os.environ.copy()
    env["MWV_PORT"] = str(port)
    env["MWV_DEBUG"] = "1"
    
    print(f"STDOUT: [Manager] Starting managed session on port {port}...", flush=True)
    
    # Start the child process
    # Use the same python executable as current process
    # Use -u for unbuffered output to catch spawning logs immediately
    process = subprocess.Popen(
        [sys.executable, "-u", str(main_py), "--debug"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(project_root)
    )
    
    url = f"http://localhost:{port}/app.html"
    session_data = {
        "port": port,
        "url": url,
        "pid": process.pid,
        "status": "starting"
    }

    # Wait for the "Frontend spawned" confirmation in the logs
    is_ready = False
    start_time = time.time()
    timeout = 30  # 30 seconds to boot
    
    try:
        while time.time() - start_time < timeout:
            line = process.stdout.readline()
            if not line:
                break
            print(f"STDOUT: [Session] {line.strip()}", flush=True)
            
            if "[Sync] Frontend spawned" in line or "Launching app.html" in line:
                is_ready = True
                session_data["status"] = "ready"
                print(f"STDOUT: [Manager] Session is READY at {url}", flush=True)
                break
            
            # Check if process died
            if process.poll() is not None:
                session_data["status"] = "failed"
                print(f"STDOUT: [Manager] Session FAILED (process died)", flush=True)
                break
    except Exception as e:
        print(f"STDOUT: [Manager] Error while waiting for spawn: {e}", flush=True)

    # Print final JSON for external consumers (Selenium/Playwright)
    print("STDOUT: [SESSION_METADATA_START]")
    print(json.dumps(session_data, indent=2))
    print("STDOUT: [SESSION_METADATA_END]")
    
    return process, session_data

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    proc, data = start_managed_session(PROJECT_ROOT)
    
    if data["status"] == "ready":
        print(f"\nManaged session is running at {data['url']}")
        print("Press Ctrl+C to terminate the session.")
        try:
            while proc.poll() is None:
                line = proc.stdout.readline()
                if line:
                    print(line.strip(), flush=True)
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nSTDOUT: [Manager] Terminating session...", flush=True)
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            print("STDOUT: [Manager] Session stopped.")
    else:
        print(f"\nFailed to start session: {data['status']}")
        proc.kill()
        sys.exit(1)
