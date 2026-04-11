import os
import signal
import subprocess
import time

def super_kill():
    print("[SUPER-KILL] Hard-purging all main.py processes...")
    try:
        # Find all python processes running main.py
        cmd = "ps aux | grep 'main.py' | grep -v 'grep' | awk '{print $2}'"
        pids = subprocess.check_output(cmd, shell=True).decode().split()
        
        for pid in pids:
            print(f"[KILL] Terminating PID: {pid}")
            try:
                os.kill(int(pid), signal.SIGKILL)
            except:
                pass
        
        # Also kill anything on port 8345
        print("[PURGE] Clearing Port 8345...")
        subprocess.run("fuser -k 8345/tcp", shell=True, stderr=subprocess.DEVNULL)
        
        print("[SUCCESS] All ghosts purged. You can now restart the app.")
    except Exception as e:
        print(f"[ERROR] Kill failed: {e}")

if __name__ == "__main__":
    super_kill()
