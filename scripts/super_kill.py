#!/usr/bin/env python3
import psutil
import os
import time

def super_kill(project_path_fragment):
    # Identify current process and all ancestors to avoid suicide/agent-kill
    try:
        current_proc = psutil.Process()
        ancestor_pids = {p.pid for p in current_proc.parents()}
        ancestor_pids.add(os.getpid())
    except Exception:
        ancestor_pids = {os.getpid()}

    print(f"[SuperKill] Scanning for processes containing: '{project_path_fragment}'")
    print(f"[SuperKill] Excluding ancestor PIDs: {list(ancestor_pids)}")
    
    killed_count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.info['pid']
            if pid in ancestor_pids:
                continue
            
            # Explicitly skip antigravity/gemini processes
            name = (proc.info.get('name') or "").lower()
            cmdline = proc.info.get('cmdline') or []
            cmd_str = " ".join(cmdline).lower()
            
            if "antigravity" in name or "gemini" in name or "antigravity" in cmd_str or "gemini" in cmd_str:
                # print(f"[SuperKill] Skipping AI infrastructure process: {name} (PID {pid})")
                continue

            if project_path_fragment in " ".join(cmdline):
                print(f"[SuperKill] Terminating PID {pid}: {cmd_str[:100]}...")
                proc.terminate()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            print(f"[Warn] Error inspecting PID {proc.info.get('pid')}: {e}")
            
    if killed_count > 0:
        print(f"[SuperKill] Sent termination signals to {killed_count} processes. Waiting for cleanup...")
        time.sleep(2)
        
        # Double check and force kill if still alive
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                pid = proc.info['pid']
                if pid in ancestor_pids: 
                    continue
                
                name = (proc.info.get('name') or "").lower()
                cmdline = proc.info.get('cmdline') or []
                cmd_str = " ".join(cmdline).lower()

                if "antigravity" in name or "gemini" in name or "antigravity" in cmd_str or "gemini" in cmd_str:
                    continue

                if project_path_fragment in " ".join(cmdline):
                    print(f"[SuperKill] PID {pid} still alive. Sending SIGKILL...")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    else:
        print("[SuperKill] No stale processes found.")

if __name__ == "__main__":
    project_fragment = "gui_media_web_viewer"
    super_kill(project_fragment)
    print("[SuperKill] Done.")
