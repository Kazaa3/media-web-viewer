import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# The exact list from the Overview (Foundations)
STORY_MAPPING = [
    ("Genese", "001"),
    ("Skeleton", "002"),
    ("Architecture Eel Python", "003"),
    ("Modular Heart", "004"),
    ("Frontend Orchestration", "005"),
    ("Serving the Content Bottle", "006"),
    ("Format Diversity", "007"),
    ("Metadata Pipeline", "008"),
    ("Real Time Transcoding", "009"),
    ("Persistence", "010"),
    ("Environment Hygiene", "011"),
    ("Project Strategy", "012"),
    ("Quality Assurance", "013"),
    ("Roadmap Future", "014"),
    ("Gapless Series", "015"),
    ("Humor", "016"),
    ("Doku-Messy", "016")
]

def clean_filename(name):
    # Strip all numbers and underscores from the start
    name = re.sub(r'^[0-9_]+', '', name)
    # Remove dates YYYY-MM-DD
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    return name.strip("_").replace("__", "_")

def absolute_restoration_v2():
    all_files = []
    # 1. Collect all and strip current IDs
    for folder in ["01_Architektur_und_Konzepte", "02_Features_und_Implementation", "03_Walkthroughs_und_Berichte"]:
        f_dir = ROOT / folder
        if not f_dir.exists(): continue
        for f in f_dir.rglob("*.md"):
            if f.is_file():
                content = ""
                try: content = f.read_text(encoding='utf-8')
                except: pass
                
                clean_name = clean_filename(f.name)
                
                # Check for story matches
                forced_id = None
                for key, idx in STORY_MAPPING:
                    if key.lower() in clean_name.lower().replace("_", " ") or key.lower() in content.lower():
                        forced_id = idx
                        break
                
                all_files.append({
                    "path": f,
                    "clean_name": clean_name,
                    "forced_id": forced_id,
                    "folder": folder
                })

    # Deduplicate forced
    forced = {}
    others = []
    for x in all_files:
        if x["forced_id"] and x["forced_id"] not in forced:
            forced[x["forced_id"]] = x
        else:
            others.append(x)
            
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    final_list = []
    # 001-020
    for i in range(1, 21):
        idx_str = f"{i:03d}"
        if idx_str in forced:
            final_list.append((forced[idx_str], idx_str))
        else:
            if others: final_list.append((others.pop(0), idx_str))
            
    # others 021+
    counter = 21
    for x in others:
        final_list.append((x, f"{counter:03d}"))
        counter += 1
        
    print(f"Executing FINAL Story Restoration (791 files)...")
    for entry, idx in final_list:
        new_name = f"{idx}_{entry['clean_name']}"
        # Story always to Folder 01
        target_folder = "01_Architektur_und_Konzepte" if int(idx) <= 25 else entry["folder"]
        target_path = ROOT / target_folder / new_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    absolute_restoration_v2()
