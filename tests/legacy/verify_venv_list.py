import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path("/home/xc/#Coding/gui_media_web_viewer/src/core")))

import main

# Mock requirements status to avoid errors
def mock_get_requirements_status():
    return {"available": False}

main._get_requirements_status = mock_get_requirements_status

# Call get_environment_info
info = main.get_environment_info()

print("Local Venvs Found:")
for venv in info.get("local_venvs", []):
    print(f" - {venv['name']} (Role: {venv.get('role')}, Purpose: {venv.get('purpose')})")

found_run = any(v["name"] == ".venv_run" for v in info.get("local_venvs", []))
if found_run:
    print("\nSUCCESS: .venv_run found in local_venvs list.")
else:
    print("\nFAILURE: .venv_run NOT found in local_venvs list.")
    sys.exit(1)
