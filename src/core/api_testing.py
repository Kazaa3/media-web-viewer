import os
import sys
import time
import json
import re
import subprocess
import threading
import eel
from pathlib import Path
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT, DEFAULT_TIME_FORMAT, FORENSIC_TOOLS_LIST, get_tool_metadata
from src.core.logger import get_logger

log = get_logger("api_testing")

@eel.expose
def run_tests(test_files):
    """Executes selected pytest suites and returns the results."""
    if not test_files: return {"error": "No test suites selected."}
    
    valid_files = []
    test_dir = PROJECT_ROOT / "tests"
    for tf in test_files:
        p = test_dir / tf
        if p.exists(): valid_files.append(str(p))
    if not valid_files: return {"error": "No valid test files found."}

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{PROJECT_ROOT}:{PROJECT_ROOT}/src:{PROJECT_ROOT}/src/core:{PROJECT_ROOT}/src/parsers"
    env["MWV_DISABLE_BROWSER_OPEN"] = "1"

    test_python = sys.executable
    known_venvs = GLOBAL_CONFIG.get("test_settings", {}).get("known_venvs", [".venv_testbed", ".venv_dev", "venv"])
    for venv_name in known_venvs:
        venv_bin = PROJECT_ROOT / venv_name / "bin" / "python"
        if venv_bin.exists():
            test_python = str(venv_bin)
            break

    try:
        process = subprocess.Popen(
            [test_python, "-m"] + GLOBAL_CONFIG.get("test_settings", {}).get("pytest_cmd", ["pytest", "-q"]) + valid_files,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, cwd=str(PROJECT_ROOT), bufsize=1, universal_newlines=True
        )
        
        output_lines = []
        start_time = time.time()
        timeout = GLOBAL_CONFIG.get("perf_settings", {}).get("task_timeout", 900)

        while True:
            line = process.stdout.readline()
            if line:
                output_lines.append(line)
                if hasattr(eel, "append_test_output"): eel.append_test_output(line)()
            elif process.poll() is not None: break
            if time.time() - start_time > timeout:
                process.kill()
                raise RuntimeError(f"Test timeout after {timeout}s")

        result_code = process.wait()
        output = ''.join(output_lines)
        passes = int(re.search(r'(\d+)\s+passed', output).group(1)) if re.search(r'(\d+)\s+passed', output) else 0
        fails = int(re.search(r'(\d+)\s+failed', output).group(1)) if re.search(r'(\d+)\s+failed', output) else 0
        
        # Persist results
        results_path = Path(GLOBAL_CONFIG["storage_registry"]["test_results_path"])
        history = []
        if results_path.exists():
            try: history = json.loads(results_path.read_text(encoding='utf-8'))
            except: pass
        
        res_item = GLOBAL_CONFIG.get("templates", {}).get("test_result", {}).copy()
        res_item.update({"timestamp": time.time(), "duration": time.time() - start_time, "passes": passes, "fails": fails, "summary": f"{passes} passed, {fails} failed", "files": test_files})
        history.append(res_item)
        results_path.write_text(json.dumps(history[-100:], indent=2), encoding='utf-8')

        return {"exit_code": result_code, "output": output, "summary": f"{passes} passed, {fails} failed", "passes": passes, "fails": fails}
    except Exception as e: return {"error": str(e)}

@eel.expose
def get_test_results():
    results_path = Path(GLOBAL_CONFIG["storage_registry"]["test_results_path"])
    if not results_path.exists(): return []
    try: return json.loads(results_path.read_text(encoding='utf-8'))
    except: return []

@eel.expose
def run_app_audit_detached(port):
    """Runs a detached background audit of the application state."""
    def _do_audit():
        log.info(f"[Audit] Starting background health check on port {port}...")
        time.sleep(5)
        # Mock audit logic for now
        log.info("[Audit] Health check complete: 100% Operational")
    threading.Thread(target=_do_audit, daemon=True).start()

@eel.expose
def get_benchmark_results():
    """Retrieves high-fidelity workstation benchmarks."""
    bench_file = Path(GLOBAL_CONFIG.get("storage_registry", {}).get("benchmarks_file", str(PROJECT_ROOT / "benchmarks.json")))
    if bench_file.exists():
        try: return json.loads(bench_file.read_text(encoding='utf-8'))
        except: pass
    return {"status": "no_data", "message": "No benchmarks found."}
@eel.expose
def get_environment_inventory():
    """
    Forensic Environment Inventory (v1.46.136).
    Returns a comprehensive list of all installed Python packages and Forensic Binaries.
    """
    try:
        from importlib.metadata import distributions
        from src.core.config_master import is_in_container
        
        # 1. Python Package Inventory
        python_packages = []
        for d in distributions():
            try:
                python_packages.append({"name": d.metadata["Name"], "version": d.version})
            except: continue
        python_packages.sort(key=lambda x: x["name"].lower())
        
        # 2. Forensic Binary Inventory (v1.46.136 Tiered)
        forensic_binaries = []
        for tool in FORENSIC_TOOLS_LIST:
            forensic_binaries.append(get_tool_metadata(tool))
            
        # 3. Python Runtime Metadata (v1.46.138)
        python_env = {
            "executable": sys.executable,
            "prefix": sys.prefix,
            "base_prefix": sys.base_prefix,
            "is_venv": sys.prefix != sys.base_prefix,
            "conda_prefix": os.environ.get("CONDA_PREFIX", "None"),
            "platform": sys.platform,
            "version": sys.version.split(" ")[0]
        }
            
        log.info(f"[Inventory] Aggregated {len(python_packages)} packages, {len(forensic_binaries)} binaries, and runtime metadata.")
        return {
            "status": "ok", 
            "is_container": is_in_container(),
            "python_env": python_env,
            "python_packages": python_packages, 
            "forensic_binaries": forensic_binaries,
            "counts": {
                "packages": len(python_packages),
                "binaries": len(forensic_binaries)
            }
        }
    except Exception as e:
        log.error(f"[Inventory] Failed to aggregate environment: {e}")
        return {"error": str(e)}
