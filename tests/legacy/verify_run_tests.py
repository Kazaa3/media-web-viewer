import sys
from pathlib import Path
import os
import subprocess

# Mock eel before importing main
class MockEel:
    def expose(self, func):
        return func

sys.modules['eel'] = MockEel()

# Add src to path
project_root = Path("/home/xc/#Coding/gui_media_web_viewer")
sys.path.append(str(project_root))

# Mock other imports
sys.modules['src.core.env_handler'] = type('Mock', (), {'validate_safe_startup': lambda: None})

import src.core.main as main

def test_run_tests():
    print("Testing run_tests with recursive path...")
    # Use a file that definitely has tests
    test_file = "basic/env/test_min_python_version.py"
    
    print(f"Running test: {test_file}")
    
    result = main.run_tests([test_file])
    print(f"Result type: {type(result)}")
    if isinstance(result, dict):
        if "error" in result:
            print(f"Error Result: {result.get('error')}")
        else:
            print(f"Exit Code: {result.get('exit_code')}")
            print(f"Summary: {result.get('summary')}")
            print(f"Output snippet: {result.get('output')[:200]}...")
    else:
        print("Unexpected result type.")

if __name__ == "__main__":
    test_run_tests()
