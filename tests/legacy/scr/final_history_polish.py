import os
import re
import shutil
from pathlib import Path
from datetime import datetime

TARGET_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

FOLDERS = [
    "01_Architektur_und_Konzepte",
    "02_Features_und_Implementation",
    "03_Walkthroughs_und_Berichte"
]

def get_real_date(filepath):
    d_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if d_match: return d_match.group(1)
    return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d")

def final_polish():
    all_files = []
    for folder in FOLDERS:
        for f in (TARGET_ROOT / folder).rglob("*.md"):
            if f.is_file():
                # Strip old ID/Date
                clean_base = re.sub(r'^\d{2,3}_', '', f.name)
                clean_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', clean_base)
                
                date = get_real_date(f)
                all_files.append({
                    "path": f,
                    "clean_base": clean_base,
                    "date": date,
                    "target_folder": folder
                })
    
    # Sort ALL by date
    all_files.sort(key=lambda x: (x["date"], x["clean_base"]))
    
    # 1. Ensure the first 25 files (history) are in Folder 01
    for idx, entry in enumerate(all_files[:25]):
        entry["target_folder"] = FOLDERS[0]
        
    print(f"Applying final chronological re-indexing to {len(all_files)} records...")
    for idx, entry in enumerate(all_files, 1):
        idx_str = f"{idx:03d}"
        new_name = f"{idx_str}_{entry['date']}_{entry['clean_base']}"
        
        # Ensure target folder exists
        (TARGET_ROOT / entry["target_folder"]).mkdir(parents=True, exist_ok=True)
        
        final_path = TARGET_ROOT / entry["target_folder"] / new_name
        
        # Move if needed
        if entry["path"] != final_path:
            shutil.move(entry["path"], final_path)

if __name__ == "__main__":
    final_polish()
