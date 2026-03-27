import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# EXACT Mapping based on the 'Gapless Series' Overview
GAPLESS_SERIES = [
    ("The Skeleton", "001"),
    ("Architecture Eel Python", "002"),
    ("Modular Heart", "003"),
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
    ("Genese", "014"), # General project philosophy
    ("Doku-Messy", "015"), # Humor
    ("Overview_Logbook", "000")
]

def clean_filename(name):
    name = re.sub(r'^[0-9_]+', '', name)
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    return name.strip("_").replace("__", "_")

def absolute_restoration_v3():
    all_files = []
    # Collect from 01, 02, 03 folders
    for folder in ["01_Architektur_und_Konzepte", "02_Features_und_Implementation", "03_Walkthroughs_und_Berichte"]:
        f_dir = ROOT / folder
        if not f_dir.exists(): continue
        for f in f_dir.rglob("*.md"):
            if f.is_file():
                content = ""
                try: content = f.read_text(encoding='utf-8').lower()
                except: pass
                
                clean_name = clean_filename(f.name)
                
                forced_id = None
                for key, idx in GAPLESS_SERIES:
                    if key.lower() in clean_name.lower().replace("_", " ") or key.lower() in content:
                        forced_id = idx
                        break
                
                all_files.append({
                    "path": f,
                    "clean_name": clean_name,
                    "forced_id": forced_id,
                    "original_folder": folder
                })

    # Dedup forced matches
    forced = {}
    others = []
    for x in all_files:
        if x["forced_id"] and x["forced_id"] not in forced:
            forced[x["forced_id"]] = x
        else:
            others.append(x)
            
    # Sort others by mtime (chronological creation)
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    # Final sequential list
    final_list = []
    # Fill 000-020
    for i in range(0, 21):
        idx_str = f"{i:03d}"
        if idx_str in forced:
            final_list.append((forced[idx_str], idx_str))
        else:
            if others: final_list.append((others.pop(0), idx_str))
            
    # 021+ for others
    counter = 21
    for x in others:
        final_list.append((x, f"{counter:03d}"))
        counter += 1
        
    arch_folder = "01_Architektur_und_Konzepte"
    
    print(f"Executing MASTER Restoration of 01-13 Foundation (791 files)...")
    for entry, idx in final_list:
        new_name = f"{idx}_{entry['clean_name']}"
        # Story (0-25) stays in Architecture
        target_folder = arch_folder if int(idx) <= 25 else entry["original_folder"]
        target_path = ROOT / target_folder / new_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    absolute_restoration_v3()
