import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# The exact list from the Overview
OVERVIEW_KEYS = [
    ("The Skeleton", "001"),
    ("Architecture Eel Python", "002"),
    ("The Modular Heart", "003"),
    ("Frontend Orchestration", "004"),
    ("Serving the Content Bottle", "005"),
    ("Format Diversity", "006"),
    ("Metadata Pipeline", "007"),
    ("Real Time Transcoding", "008"),
    ("Persistence Layer", "009"),
    ("Environment Hygiene", "010"),
    ("Project Strategy", "011"),
    ("Quality Assurance", "012"),
    ("Roadmap Future", "013"),
    ("Doku-Messy", "014"), # The humorous story
    ("Overview_Logbook", "000")
]

def clean_filename(name):
    while re.match(r'^\d+_', name):
        name = re.sub(r'^\d+_', '', name)
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    return name.strip("_").replace("__", "_")

def absolute_restoration():
    all_files = []
    for f in ROOT.rglob("*.md"):
        if f.is_file():
            content = ""
            try: content = f.read_text(encoding='utf-8').lower()
            except: pass
            
            # Find best match from Overview keys
            assigned_idx = None
            for key, idx in OVERVIEW_KEYS:
                if key.lower() in content or key.lower().replace(" ", "_") in f.name.lower():
                    assigned_idx = idx
                    break
            
            all_files.append({
                "path": f,
                "clean_name": clean_filename(f.name),
                "idx": assigned_idx,
                "folder": f.parent.name
            })
            
    # Sort
    forced = {x["idx"]: x for x in all_files if x["idx"] is not None}
    others = [x for x in all_files if x["idx"] is None]
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    final_list = []
    # Force 000-014
    for i in range(0, 15):
        idx_str = f"{i:03d}"
        if idx_str in forced:
            final_list.append((forced[idx_str], idx_str))
        else:
            if others: final_list.append((others.pop(0), idx_str))
            
    # Remainder
    counter = 15
    for x in others:
        final_list.append((x, f"{counter:03d}"))
        counter += 1
        
    print(f"Restoring 01-13 foundational history (791 files)...")
    for entry, idx in final_list:
        new_name = f"{idx}_{entry['clean_name']}"
        # Foundations to Architecture folder
        target_folder = "01_Architektur_und_Konzepte" if int(idx) <= 15 else entry["folder"]
        target_path = ROOT / target_folder / new_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    absolute_restoration()
