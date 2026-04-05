import sys
import os
from pathlib import Path

# Mock eel
class MockEel:
    def expose(self, func):
        return func

sys.modules['eel'] = MockEel()

# Import main (you might need to mock more)
# Since main.py is huge and has many dependencies, it's better to just copy relevant part or mock things.

def get_test_suites():
    test_dir = Path("/home/xc/#Coding/gui_media_web_viewer/tests")
    if not test_dir.exists():
        return []

    suites = []
    all_files = []
    for root, dirs, filenames in os.walk(str(test_dir)):
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".sh"):
                if not filename.startswith("__") and not filename.startswith("."):
                    all_files.append(Path(root) / filename)
    
    all_files.sort(key=lambda x: str(x.relative_to(test_dir)))

    for f in all_files:
        rel_path = f.relative_to(test_dir)
        display_name = str(rel_path)
        
        suites.append({
            "id": str(rel_path), 
            "name": display_name,
            "folder": str(rel_path.parent) if str(rel_path.parent) != "." else "",
        })
    return suites

suites = get_test_suites()
print(f"Found {len(suites)} suites")
for i, s in enumerate(suites[:10]):
    print(f"{i}: {s['id']} (Folder: '{s['folder']}')")
