import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# The exact list from the Overview (Foundations)
STORY_MAPPING = [
    ("Genese", "001"),
    ("Skeleton", "002"),
    ("Architecture_Eel", "003"),
    ("Modular_Heart", "004"),
    ("Frontend_Orchestration", "005"),
    ("Serving_the_Content_Bottle", "006"),
    ("Format_Diversity", "007"),
    ("Metadata_Pipeline", "008"),
    ("Real_Time_Transcoding", "009"),
    ("Persistence", "010"),
    ("Environment_Hygiene", "011"),
    ("Project_Strategy", "012"),
    ("Assurance", "013"),
    ("Roadmap_Future", "014"),
    ("Overview_Logbook", "015"),
    ("Doku-Messy", "016"), # Humor
    ("Management_Suite", "017"),
    ("Garbage_Collector", "018"),
    ("File_List", "019"),
    ("status_update", "020")
]

def clean_filename(name):
    # Strip IDs and Dates
    while re.match(r'^\d+_', name):
        name = re.sub(r'^\d+_', '', name)
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    name = name.strip("_").replace("__", "_")
    return name

def force_foundational_order():
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
                "idx": found_idx,
                "folder": f.parent.name
            })
            
    # Priority
    found = {}
    remaining = []
    for x in all_files:
        if x["idx"] and x["idx"] not in found:
            found[x["idx"]] = x
        else:
            remaining.append(x)
            
    remaining.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    final_list = []
    # Fill 001-020
    for i in range(1, 21):
        idx_str = f"{i:03d}"
        if idx_str in found:
            final_list.append((found[idx_str], idx_str))
        else:
            if remaining: final_list.append((remaining.pop(0), idx_str))
            
    # 021+ for all others
    counter = 21
    for x in remaining:
        final_list.append((x, f"{counter:03d}"))
        counter += 1
        
    print(f"Force-Renumbering foundational history (001-020) and sequential others (791 files)...")
    for entry, idx in final_list:
        new_name = f"{idx}_{entry['clean_name']}"
        # Foundations to Architecture folder
        target_folder = "01_Architektur_und_Konzepte" if int(idx) <= 25 else entry["folder"]
        target_path = ROOT / target_folder / new_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    force_foundational_order()
