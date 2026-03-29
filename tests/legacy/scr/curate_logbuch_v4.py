import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# Exact curation with more robust fuzzy matching
STORY_MAPPING = [
    ("Genese", "001"),
    ("Overview_Logbook", "002"),
    ("Messy", "003"),
    ("Skeleton", "004"),
    ("Architecture_Eel", "005"),
    ("Modular_Heart", "006"),
    ("Frontend_Orchestration", "007"),
    ("Bottle", "008"),
    ("Format_Diversity", "009"),
    ("Metadata_Pipeline", "010"),
    ("Transcoding_Streaming", "011"),
    ("Persistence", "012"),
    ("Hygiene", "013"),
    ("Strategy", "014"),
    ("Assurance", "015"),
    ("Roadmap_Future", "016"),
    ("Management_Suite", "017"),
    ("Garbage_Collector", "018"),
    ("File_List", "019"),
    ("status_update", "020")
]

def clean_filename(name):
    name = re.sub(r'^\d{2,3}_', '', name)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', name)
    while re.match(r'^\d+_', name):
        name = re.sub(r'^\d+_', '', name)
    return name

def curate_logbuch_v4():
    all_files = []
    for f in ROOT.rglob("*.md"):
        if f.is_file():
            content = ""
            try: content = f.read_text(encoding='utf-8').lower()
            except: pass
            
            fname_clean = clean_filename(f.name).lower()
            
            found_idx = None
            for key, idx in STORY_MAPPING:
                k = key.lower().replace("_", " ")
                if k in fname_clean.replace("_", " ") or k in content:
                    found_idx = idx
                    break
            
            all_files.append({
                "path": f,
                "clean_name": clean_filename(f.name),
                "forced_idx": found_idx,
                "folder": f.parent.name
            })

    # Separate matches
    matches = {}
    others = []
    for x in all_files:
        if x["forced_idx"] and x["forced_idx"] not in matches:
            matches[x["forced_idx"]] = x
        else:
            others.append(x)
            
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    final_list = []
    for i in range(1, 21):
        idx = f"{i:03d}"
        if idx in matches: final_list.append((matches[idx], idx))
        else:
            if others: final_list.append((others.pop(0), idx))
            
    # Counter for remaining
    counter = 21
    for x in others:
        final_list.append((x, f"{counter:03d}"))
        counter += 1
        
    print(f"Executing Absolute Humorous Story Restoration (791 files)...")
    for entry, idx in final_list:
        new_name = f"{idx}_{entry['clean_name']}"
        # Story to Archive (01)
        target_folder = "01_Architektur_und_Konzepte" if int(idx) <= 25 else entry["folder"]
        target_path = ROOT / target_folder / new_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    curate_logbuch_v4()
