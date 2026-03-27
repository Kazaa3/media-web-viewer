import os
import re
from pathlib import Path

TARGET_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

CORE_SERIES = {
    "The Skeleton": "01",
    "Architecture Eel Python": "02",
    "The Modular Heart": "03",
    "Frontend Orchestration": "04",
    "Serving the Content Bottle": "05",
    "Diversity or Codecs": "06",
    "Metadata Pipeline": "07",
    "Real Time Transcoding": "08",
    "Persistence Layer": "09",
    "Environment Hygiene": "10",
    "Project Strategy": "11",
    "Quality Assurance": "12",
    "Roadmap Future": "13"
}

def get_title(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        match = re.search(r'# (.*)', content)
        if match: return match.group(1).strip()
    except: pass
    return ""

def force_01_13():
    all_files = list(TARGET_ROOT.rglob("*.md"))
    
    # Track which files were assigned a core number
    assigned_mapping = {} # old_path -> new_num
    
    for f in all_files:
        title = get_title(f)
        for key, num in CORE_SERIES.items():
            if key.lower() in title.lower():
                assigned_mapping[f] = num
                break
                
    # Also search by filename if title not found
    for f in all_files:
        if f in assigned_mapping: continue
        for key, num in CORE_SERIES.items():
            if key.lower().replace(" ", "_") in f.name.lower():
                assigned_mapping[f] = num
                break

    # Now handle the renaming
    # We want to swap the ID prefix of these specific files to 01-13
    for old_path, num in assigned_mapping.items():
        base = re.sub(r'^\d{2,3}_', '', old_path.name)
        new_name = f"{num}_{base}"
        new_path = old_path.parent / new_name
        
        if old_path != new_path:
            print(f"Forcing {old_path.name} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    force_01_13()
