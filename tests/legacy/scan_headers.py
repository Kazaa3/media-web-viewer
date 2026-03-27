import os
from pathlib import Path

test_dir = Path("/home/xc/#Coding/gui_media_web_viewer/tests")
missing_headers = []

for root, dirs, files in os.walk(test_dir):
    if "__pycache__" in dirs:
        dirs.remove("__pycache__")
    
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            file_path = Path(root) / file
            try:
                content = file_path.read_text(encoding='utf-8')
                if "# Kategorie:" not in content:
                    missing_headers.append(str(file_path))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

print("\nFiles missing '# Kategorie:' header:")
for f in missing_headers:
    print(f)
