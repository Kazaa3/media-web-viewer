import subprocess
import time
import socket
import sys
import os

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def launch_and_verify():
    print("--- Starting Forensic Workstation Frontend Verification ---")
    project_root = os.getcwd()
    venv_python = os.path.join(project_root, ".venv", "bin", "python3")
    main_py = os.path.join(project_root, "src", "core", "main.py")
    
    if not os.path.exists(venv_python):
        print(f"[ERROR] Virtual environment not found at {venv_python}")
        sys.exit(1)

    print(f"[INFO] Launching app with: {venv_python}")
    # Start the process in the background
    process = subprocess.Popen(
        [venv_python, main_py],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=project_root
    )
    
    # Wait for the port to open
    port = 8345
    print(f"[INFO] Waiting for port {port} to open...")
    success = False
    for i in range(20):
        if is_port_open(port):
            print(f"[OK] Port {port} is OPEN!")
            success = True
            break
        time.sleep(1)
        if process.poll() is not None:
            print("[ERROR] Subprocess exited early!")
            print(process.stdout.read())
            break
    
    if success:
        print("[SUCCESS] Forensic Workstation Frontend is up and serving!")
    else:
        print("[FAIL] Frontend failed to start within timeout.")
        if process.poll() is None:
            process.terminate()
    
    # Cleanup (terminate the app)
    if process.poll() is None:
        process.terminate()
        print("[INFO] Cleanup: Subprocess terminated.")

if __name__ == "__main__":
    launch_and_verify()
