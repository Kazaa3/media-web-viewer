import os
import re
from pathlib import Path
from datetime import datetime

TARGET_ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

FOLDERS = [
    "01_Architektur_und_Konzepte",
    "02_Features_und_Implementation",
    "03_Walkthroughs_und_Berichte"
]

def get_real_date(filepath):
    # 1. Look for YYYY-MM-DD in filename
    d_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if d_match:
        return d_match.group(1)
    
    # 2. Fallback to file modification time (mtime)
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

def get_title(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        match = re.search(r'# (.*)', content)
        if match: return match.group(1).strip()
    except: pass
    return ""

def final_history_reindex():
    all_files = []
    # Collect from our 3 final folders
    for folder in FOLDERS:
        for f in (TARGET_ROOT / folder).rglob("*.md"):
            if f.is_file():
                # Strip old ID and Date for sorting
                clean_base = re.sub(r'^\d{2,3}_', '', f.name)
                clean_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', clean_base)
                
                date = get_real_date(f)
                title = get_title(f).lower()
                
                all_files.append({
                    "path": f,
                    "clean_base": clean_base,
                    "date": date,
                    "title": title,
                    "folder": folder
                })
    
    # Sort ALL files by date primarily
    all_files.sort(key=lambda x: (x["date"], x["clean_base"]))
    
    # Special: The user wants the 'History of dict' (ArchitectureFoundations) as 001-020.
    # We sorted them by date, so the oldest ones are naturally at the top.
    # All I need to do is apply IDs 001-N to the entire list.
    
    print(f"Executing final technical record indexing for {len(all_files)} files...")
    for idx, entry in enumerate(all_files, 1):
        idx_str = f"{idx:03d}"
        
        # New name: [ID]_[DATE]_[CLEAN_BASE]
        new_name = f"{idx_str}_{entry['date']}_{entry['clean_base']}"
        new_path = entry["path"].parent / new_name
        
        if entry["path"] != new_path:
            # We must be careful about overwriting if someone else has the name.
            # But with unique IDs, this shouldn't happen.
            try:
                os.rename(entry["path"], new_path)
            except Exception as e:
                print(f"Error re-indexing {entry['path']}: {e}")

if __name__ == "__main__":
    final_history_reindex()
