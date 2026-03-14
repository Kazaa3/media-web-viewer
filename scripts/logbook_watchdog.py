#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Monitoring / Documentation
# Eingabewerte: logbuch/ Verzeichnis, Git Status, System Metriken
# Ausgabewerte: Watchdog_Live_Log.md, Terminal Status
# Testdateien: Keine
# ERWEITERUNGEN (TODO): [ ] E-Mail Benachrichtigung bei Fehlern, [ ] Integration in GUI
# KOMMENTAR: Hintergrunddienst zur Überwachung der Projekt-Dokumentation und des Systemzustands.
# VERWENDUNG: python3 scripts/logbook_watchdog.py [--poll-interval 60] [--once]

"""
KATEGORIE: Monitoring / Documentation
ZWECK: Automatisches Erfassen von neuen Logbuch-Einträgen und Systemstatus.
EINGABEWERTE: Dateisystem-Events, Git CLI, psutil
AUSGABEWERTE: Fortschreibung der Watchdog_Live_Log.md
TESTDATEIEN: Keine
ERWEITERUNGEN (TODO): [ ] Auto-Git-Commit für Live-Log
KOMMENTAR: Stellt sicher, dass auch manuell hinzugefügte Logbücher erfasst werden.
VERWENDUNG: python3 scripts/logbook_watchdog.py start
"""

import os
import sys
import time
import argparse
import subprocess
import psutil
from datetime import datetime
from pathlib import Path

# --- Configuration ---
LOGBOOK_DIR = "logbuch"
LIVE_LOG_FILE = "Watchdog_Live_Log.md"
POLL_INTERVAL = 60 # Seconds

def get_git_info():
    """Extract Git status and latest commit."""
    try:
        commit = subprocess.check_output(["git", "log", "-1", "--format=%h: %s"], text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        # Ahead/Behind info
        status = subprocess.check_output(["git", "status", "-sb"], text=True).strip()
        return f"{branch} | {commit} ({status.splitlines()[0]})"
    except Exception as e:
        return f"Git not available: {e}"

def get_sys_health():
    """Get basic system health metrics."""
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"CPU: {cpu}% | RAM: {mem}% | Disk: {disk}%"

def get_logbooks(root):
    log_dir = Path(root) / LOGBOOK_DIR
    if not log_dir.exists():
        return set()
    return {f.name for f in log_dir.glob("*.md") if f.name != LIVE_LOG_FILE}

def update_live_log(root, new_files, git_info, health_info):
    live_log_path = Path(root) / LOGBOOK_DIR / LIVE_LOG_FILE
    
    first_run = not live_log_path.exists()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = []
    if first_run:
        lines.append("# Watchdog Live Log")
        lines.append("Automatisierte Überwachung der Projektaktivität.\n")
        lines.append("| Zeitstempel | Event / Status | Git | System |")
        lines.append("| :--- | :--- | :--- | :--- |")

    event = "Polling Update"
    if new_files:
        event = f"New Files: {', '.join(new_files)}"
    
    lines.append(f"| {timestamp} | {event} | {git_info} | {health_info} |")
    
    with open(live_log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Logbook Watchdog Service")
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL, help="Polling interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    root_dir = Path(__file__).parents[1]
    
    print(f"📡 Logbook Watchdog gestartet (Intervall: {args.poll_interval}s)")
    print(f"📁 Überwache: {root_dir / LOGBOOK_DIR}")
    
    known_files = get_logbooks(root_dir)
    
    try:
        while True:
            current_files = get_logbooks(root_dir)
            new_files = current_files - known_files
            
            git_info = get_git_info()
            health_info = get_sys_health()
            
            if new_files:
                print(f"✨ Neue Dateien erkannt: {new_files}")
            
            update_live_log(root_dir, new_files, git_info, health_info)
            
            known_files = current_files
            
            if args.once:
                print("✅ Einmaliger Durchlauf beendet.")
                break
                
            time.sleep(args.poll_interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Watchdog gestoppt.")

if __name__ == "__main__":
    main()
