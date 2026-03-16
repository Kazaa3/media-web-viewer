import os
import time
import subprocess
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def benchmark_mode(name, cmd, timeout=10):
    """Simple benchmark for a playback mode command."""
    logging.info(f"--- Benchmarking Mode: {name} ---")
    start_time = time.time()
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait a bit for the process to settle
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            logging.info(f"[{name}] Successfully started and running.")
            latency = time.time() - start_time
            logging.info(f"[{name}] Start-up Latency: {latency:.2f}s")
            
            # Here we could measure CPU/Memory if needed
            
            process.terminate()
            return {"status": "ok", "latency": latency}
        else:
            stdout, stderr = process.communicate()
            logging.error(f"[{name}] Failed to start. Error: {stderr.decode()}")
            return {"status": "error", "error": stderr.decode()}
    except Exception as e:
        logging.error(f"[{name}] Exception: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    test_file = "media/Going Raw - JUDITA_169_OPTION.ISO" # Sample file
    if not os.path.exists(test_file):
        logging.warning(f"Test file {test_file} not found. Using a dummy if possible or skipping.")
    
    modes = [
        ("ffplay Standalone", ["ffplay", "-nodisp", "-autoexit", "-t", "5", test_file]),
        ("cvlc TS Stream", ["cvlc", test_file, "--sout", "#std{access=http,mux=ts,dst=:8099/}", "--no-video-title-show", "--loop"]),
    ]
    
    results = {}
    for name, cmd in modes:
        results[name] = benchmark_mode(name, cmd)
    
    logging.info("\nFinal Results:")
    for name, res in results.items():
        logging.info(f"{name}: {res}")
