import os
import sys
import re
from pathlib import Path

def audit_main_py():
    main_py = Path("src/core/main.py")
    if not main_py.exists():
        print("main.py not found!")
        return
    
    content = main_py.read_text()
    exposed = re.findall(r"@eel\.expose\ndef\s+(\w+)", content)
    
    print(f"--- Forensic Startup Auditor (v1.54.022) ---")
    print(f"Total Exposed Endpoints in main.py: {len(exposed)}")
    for i, func in enumerate(exposed, 1):
        print(f" [{i:03d}] {func}")

if __name__ == "__main__":
    audit_main_py()
