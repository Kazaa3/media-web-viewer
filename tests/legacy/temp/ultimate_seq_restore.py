import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")
STAGING = Path("/tmp/logbook_staging")

def clean_name(name):
    # Remove all leading numbers and underscores
    name = re.sub(r'^[0-9_]+', '', name)
    # Remove dates like 2026-03-22
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name)
    name = name.strip("_").replace(".md", "").replace(".mmd", "")
    return name

def ultimate_sequential_restore():
    if STAGING.exists(): shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    
    all_files = []
    subfolders = ["01_Architektur_und_Konzepte", "02_Features_und_Implementation", "03_Walkthroughs_und_Berichte"]
    
    # Step 1: Extract everything to staging
    print("Staging all files...")
    for sub in subfolders:
        dir_path = ROOT / sub
        if not dir_path.exists(): continue
        for f in dir_path.rglob("*.md"):
            if f.is_file():
                # Store original mtime
                mtime = os.path.getmtime(f)
                cname = clean_name(f.name)
                # Meta-check for foundation
                is_foundation = any(k in cname.lower() for k in ["skeleton", "genese", "philosophy", "architecture", "modular_heart"])
                
                staging_path = STAGING / f.name
                shutil.copy2(f, staging_path)
                all_files.append({
                    "src": staging_path,
                    "mtime": mtime,
                    "name": cname,
                    "is_foundation": is_foundation,
                    "orig_folder": sub
                })
        # Clear original folder files (to avoid duplicates)
        for f in dir_path.glob("*.md"): os.remove(f)

    # Step 2: Sort
    # Foundations first by mtime, then others by mtime
    foundations = [x for x in all_files if x["is_foundation"]]
    foundations.sort(key=lambda x: x["mtime"])
    
    others = [x for x in all_files if not x["is_foundation"]]
    others.sort(key=lambda x: x["mtime"])
    
    final_ordered = foundations + others
    
    # Step 3: Move back with sequential IDs
    print(f"Restoring {len(final_ordered)} files sequentially...")
    for i, item in enumerate(final_ordered):
        new_id = f"{i+1:03d}"
        new_name = f"{new_id}_{item['name']}.md"
        
        # Determine folder: 1-25 in Architecture, rest in original
        target_sub = "01_Architektur_und_Konzepte" if i < 25 else item["orig_folder"]
        target_dir = ROOT / target_sub
        target_dir.mkdir(parents=True, exist_ok=True)
        
        shutil.move(item["src"], target_dir / new_name)
        
    print("Done. Global Logbook Integrity Restored.")

if __name__ == "__main__":
    ultimate_sequential_restore()
