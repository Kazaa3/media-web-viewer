import sys
from pathlib import Path
import os

# Mock eel before importing main
class MockEel:
    def expose(self, func):
        return func

sys.modules['eel'] = MockEel()

# Add src to path
project_root = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.append(str(project_root))

# Mock other imports that might fail or cause side effects
sys.modules['src.core.env_handler'] = type('Mock', (), {'validate_safe_startup': lambda: None})

import src.core.main as main

def test_discovery():
    print("Testing recursive test discovery...")
    suites = main.get_test_suites()
    print(f"Found {len(suites)} test suites.")
    
    for s in suites:
        print(f"- {s['id']} ({s['name']})")
        # Check if id contains subfolders
        if "/" in s['id'] or "\\" in s['id']:
            print(f"  [OK] Recursive match: {s['id']}")

if __name__ == "__main__":
    test_discovery()
