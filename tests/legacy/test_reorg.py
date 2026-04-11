import re
from pathlib import Path

files = [
    "4_Venv_Konzept_Planung_Umsetzung_Validierung.md",
    "52_FFmpeg_Transcoding_Fix_and_Optimization.md",
    "54_Build_Recursion_Fix_Monitoring_System.md",
    "Abschluss_Code_Quality_Cleanup_Milestone7.md"
]

processed = []
for fname in files:
    match = re.match(r"^(\d+)_", fname)
    index = int(match.group(1)) if match else 999
    processed.append({"name": fname, "index": index})

processed.sort(key=lambda x: x["index"])

changes = []
for i, item in enumerate(processed, 1):
    original_name = item["name"]
    clean_name = re.sub(r"^\d+_", "", original_name)
    new_name = f"{i:02d}_{clean_name}"
    if original_name != new_name:
        changes.append((original_name, new_name))

print(f"Plan: {changes}")
