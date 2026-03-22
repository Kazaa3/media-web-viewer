import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# Exact curation for the humorous/foundational story (top 20)
# We match these by partial strings in the content/title if filename fails.
TOP_20_MAP = [
    ("Genesis_und_Philosophie", "001"),
    ("Overview_Logbook_Gapless", "002"),
    ("Doku_Messy_Humor", "003"),
    ("Skeleton", "004"),
    ("Architecture_Eel_Python", "005"),
    ("Modular_Heart", "006"),
    ("Frontend_Orchestration", "007"),
    ("Content_Bottle", "008"),
    ("Format_Diversity", "009"),
    ("Metadata_Pipeline", "010"),
    ("Transcoding_Streaming", "011"),
    ("Persistence_Layer", "012"),
    ("Environment_Hygiene", "013"),
    ("Project_Strategy", "014"),
    ("Qualitaetstests_Test_Classification", "015"),
    ("Roadmap_Future", "016"),
    ("Management_Suite_Walkthrough", "017"),
    ("Garbage_Collector", "018"),
    ("Markdown_File_List", "019"),
    ("status_update", "020")
]

def get_best_match(filepath, title):
    content = ""
    try: content = filepath.read_text(encoding='utf-8').lower()
    except: pass
    fname = filepath.name.lower()
    tname = title.lower()
    
    for key, idx in TOP_20_MAP:
        k = key.lower()
        if k in fname or k in tname or k.replace("_", " ") in content:
            return idx
    return None

def clean_filename(name):
    # Aggressively remove IDs like 001_, 87_, _87_, Dates 2026-03-13_
    # 1. Remove leading number sequences 001_87_...
    while re.match(r'^[\d_]+_', name):
        name = re.sub(r'^[\d_]+_', '', name)
    
    # 2. Remove any date strings YYYY-MM-DD
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    
    # 3. Handle leftover double underscores or leading underscores
    name = name.strip("_").replace("__", "_")
    
    # Avoid extensions like .md.md
    if name.endswith(".md.md"): name = name[:-3]
    return name

def curate_logbuch_v3():
    all_files = []
    for f in ROOT.rglob("*.md"):
        if f.is_file():
            # Get Title
            title = ""
            try:
                c = f.read_text(encoding='utf-8')
                match = re.search(r'# (.*)', c)
                if match: title = match.group(1).strip()
            except: pass
            
            clean_name = clean_filename(f.name)
            forced_idx = get_best_match(f, title)
            
            all_files.append({
                "path": f,
                "clean_name": clean_name,
                "forced_idx": forced_idx,
                "folder": f.parent.name
            })
            
    # Priority sorting
    forced = [x for x in all_files if x["forced_idx"] is not None]
    others = [x for x in all_files if x["forced_idx"] is None]
    
    # Dedup forced (if multiple files match same index, pick one)
    dedup_forced = {}
    for x in forced:
        idx = x["forced_idx"]
        if idx not in dedup_forced: dedup_forced[idx] = x
        else: others.append(x) # treat as other
        
    forced_list = sorted(dedup_forced.values(), key=lambda x: x["forced_idx"])
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    final_indexing = []
    # Fill 001-020 with forced ones in order
    forced_map = {x["forced_idx"]: x for x in forced_list}
    
    current_others_ptr = 0
    for i in range(1, 21):
        idx_str = f"{i:03d}"
        if idx_str in forced_map:
            final_indexing.append((forced_map[idx_str], idx_str))
        else:
            # fill with oldest 'other' if we don't have a forced match for this specific 001-020 slot
            if current_others_ptr < len(others):
                final_indexing.append((others[current_others_ptr], idx_str))
                current_others_ptr += 1

    # Add all remaining others
    for entry in others[current_others_ptr:]:
        final_indexing.append((entry, None)) # will set ID below

    # Target folders
    arch = "01_Architektur_und_Konzepte"
    
    print(f"Executing Absolute Story Curation (791 files)...")
    idx_counter = 1
    for entry, forced_id in final_indexing:
        if forced_id: id_str = forced_id
        else:
            idx_counter = max(idx_counter, 21)
            id_str = f"{idx_counter:03d}"
            idx_counter += 1
            
        new_name = f"{id_str}_{entry['clean_name']}"
        
        # Story files (001-020) always to Architecture
        if int(id_str) <= 20:
             target_path = ROOT / arch / new_name
        else:
             target_path = ROOT / entry["folder"] / new_name
             
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            shutil.move(entry["path"], target_path)

if __name__ == "__main__":
    curate_logbuch_v3()
