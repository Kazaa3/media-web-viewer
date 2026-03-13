#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Basic / Utils
# Eingabewerte: None
# Ausgabewerte: Port status, app status, selenium drivers
# Testdateien: None
# Kommentar: Gemeinsame Test-Utilities und Selenium-Helper.

import socket
import pytest
pytest.importorskip("selenium")
import logging
import time
import os
import sys
import psutil
import requests
from pathlib import Path
from requests.exceptions import ConnectionError, Timeout
from selenium.common.exceptions import StaleElementReferenceException

def is_port_open(port):
    """Checks if a port is open on localhost."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False

def wait_for_app(port, timeout=45):
    """Waits for the app to be reachable on the given port."""
    start_time = time.time()
    url = f"http://localhost:{port}/app.html"
    print(f"Waiting for app at {url} (timeout={timeout}s)...")
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                print(f"App reachable on port {port}.")
                return True
        except (ConnectionError, Timeout):
            pass
        time.sleep(1)
    print(f"App NOT reachable on port {port} after {timeout}s.")
    return False

def find_running_project_sessions():
    """Finds running main.py sessions belonging to this project."""
    sessions = []
    current_pid = os.getpid()
    project_root = Path(__file__).parents[3].parent
    
    try:
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status != 'LISTEN' or not conn.pid or conn.pid == current_pid:
                continue
            try:
                proc = psutil.Process(conn.pid)
                cmdline = proc.cmdline() or []
                is_this_project = False
                for token in cmdline:
                    token_clean = token.strip("'\"")
                    if token_clean.endswith('src/core/main.py'):
                        try:
                            token_path = Path(token_clean).resolve()
                            if project_root in token_path.parents or token_path.parent == project_root:
                                is_this_project = True
                                break
                        except: pass
                if is_this_project:
                    sessions.append({'pid': conn.pid, 'port': conn.laddr.port})
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
    except Exception as e:
        print(f"Error scanning sessions: {e}")
    return sessions

def manage_app_instance(preferred_port=None):
    """Prioritizes existing project sessions."""
    sessions = find_running_project_sessions()
    if sessions:
        best = sessions[0]
        if preferred_port:
            for s in sessions:
                if s['port'] == preferred_port:
                    best = s
                    break
        print(f"Using EXISTING project session (PID {best['pid']}) on port {best['port']}.")
        return None, True, best['port']
    if preferred_port and is_port_open(preferred_port):
        return None, True, preferred_port
    if os.environ.get("MWV_ONLY_EXISTING_SESSION") == "1":
        return "FAIL", False, None
    return "START_NEW", False, preferred_port or 8005

def robust_action(driver, action_func, retries=10, delay=1.0):
    from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
    last_ex = None
    for i in range(retries):
        try:
            result = action_func()
            if result is not None:
                return result
            return
        except (StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException) as e:
            last_ex = e
            print(f"Robust action retry {i+1}/{retries} due to {type(e).__name__}")
            time.sleep(delay)
    if last_ex:
        raise last_ex

def save_screenshot(driver, name):
    """Saves a screenshot for debugging."""
    shot_dir = Path(__file__).parents[3] / "tests/artifacts/screenshots"
    shot_dir.mkdir(parents=True, exist_ok=True)
    path = shot_dir / f"{name}_{int(time.time())}.png"
    driver.save_screenshot(str(path))
    print(f"Screenshot saved to {path}")
    return str(path)
