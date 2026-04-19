import os
import sys
import re
from pathlib import Path

def run_audit():
    core_dir = Path("src/core")
    if not core_dir.exists():
        print("src/core not found!")
        return
    
    all_exposed = {}
    
    # Scan all .py files in src/core
    for py_file in core_dir.glob("*.py"):
        try:
            content = py_file.read_text()
            exposed = re.findall(r"@eel\.expose\ndef\s+(\w+)", content)
            if exposed:
                all_exposed[py_file.name] = exposed
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
    
    print(f"--- Forensic Multi-Module Auditor (v1.54.022) ---")
    total_count = sum(len(funcs) for funcs in all_exposed.values())
    print(f"Total Unique Exposed Endpoints: {total_count}")
    
    for filename, funcs in sorted(all_exposed.items()):
        print(f"\n[{filename}] - {len(funcs)} endpoints")
        for i, func in enumerate(sorted(funcs), 1):
            print(f"  {i:03d}: {func}")
            
    return True

if __name__ == "__main__":
    run_audit()
