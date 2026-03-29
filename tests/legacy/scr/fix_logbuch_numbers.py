import os
import re
from pathlib import Path

LOGBUCH_DIR = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

CORE_SERIES = [
    "The Skeleton",
    "Architecture Eel Python",
    "The Modular Heart",
    "Frontend Orchestration",
    "Serving the Content Bottle",
    "Format Diversity",
    "Metadata Pipeline",
    "Real Time Transcoding",
    "Persistence Layer",
    "Environment Hygiene",
    "Project Strategy",
    "Quality Assurance",
    "Roadmap Future Milestones"
]

def get_title(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        # Look for # Title or Title_EN: metadata
        match = re.search(r'# (.*)', content)
        if match: return match.group(1).strip()
        match = re.search(r'Title_EN:\s*(.*)', content)
        if match: return match.group(1).strip()
    except:
        pass
    return ""

def renumber():
    all_files = []
    for f in LOGBUCH_DIR.rglob("*.md"):
        title = get_title(f)
        all_files.append({
            "path": f,
            "title": title,
            "filename": f.name,
            "is_core": any(core in title for core in CORE_SERIES) or any(core in f.name for core in CORE_SERIES)
        })
    
    # Sort files by date (using the YYYY-MM-DD in the filename)
    def sort_key(x):
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', x["filename"])
        date = date_match.group(1) if date_match else "1970-01-01"
        # If it's core, we want it at the very beginning
        # We'll handle core separately or give them priority
        return (date, x["filename"])

    all_files.sort(key=sort_key)
    
    # Separate core and others
    core_files = [f for f in all_files if f["is_core"]]
    # Sort core files by their intended sequence if possible
    def core_sequence(x):
        for i, core in enumerate(CORE_SERIES):
            if core in x["title"] or core in x["filename"]:
                return i
        return 99
    core_files.sort(key=core_sequence)
    
    other_files = [f for f in all_files if not f["is_core"]]
    
    # Final Sequence
    final_list = []
    # 1. Add core files (01-13)
    for i, f in enumerate(core_files[:len(CORE_SERIES)], 1):
        final_list.append((f, f"{i:02d}"))
    
    # 2. Add others starting from len(core)+1
    # But wait, original 13!
    start_idx = 14
    for i, f in enumerate(other_files, start_idx):
        final_list.append((f, f"{i:03d}"))
        
    for f_info, idx in final_list:
        old_path = f_info["path"]
        # Strip old index and date
        new_name_base = re.sub(r'^\d{2,3}_', '', old_path.name)
        new_name_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', new_name_base)
        
        # Get date from old name
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', old_path.name)
        date_str = date_match.group(1) if date_match else "2026-03-13"
        
        new_name = f"{idx}_{date_str}_{new_name_base}"
        new_path = old_path.parent / new_name
        
        if old_path != new_path:
            print(f"Renaming {old_path.name} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    renumber()
