import os
import re
from pathlib import Path

LOGBUCH_DIR = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# Exact mappings for the original Gapless Series (01-13)
GAPLESS_SERIES = {
    "The Skeleton": "01",
    "Architecture Eel Python": "02",
    "The Modular Heart": "03",
    "Frontend Orchestration": "04",
    "Serving the Content Bottle": "05",
    "Format Diversity and Codecs": "06",
    "Metadata Pipeline": "07",
    "Real Time Transcoding": "08",
    "Persistence Layer": "09",
    "Environment Hygiene": "10",
    "Project Strategy": "11",
    "Quality Assurance": "12",
    "Roadmap Future": "13"
}

def get_title(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        match = re.search(r'# (.*)', content)
        if match: return match.group(1).strip()
        match = re.search(r'Title_EN:\s*(.*)', content)
        if match: return match.group(1).strip()
    except:
        pass
    return ""

def renumber_global():
    all_files = []
    # Identify all files across subfolders
    for f in LOGBUCH_DIR.rglob("*.md"):
        title = get_title(f)
        filename = f.name
        
        assigned_idx = None
        for key, idx in GAPLESS_SERIES.items():
            if key.lower() in title.lower() or key.lower().replace(" ", "_") in filename.lower():
                assigned_idx = idx
                break
        
        all_files.append({
            "path": f,
            "filename": filename,
            "assigned_idx": assigned_idx
        })
    
    # Sort ALL files by date primarily
    def sort_key(x):
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', x["filename"])
        date = date_match.group(1) if date_match else "1970-01-01"
        # Within the same date, keep alphabetical or use old index
        return (date, x["filename"])

    all_files.sort(key=sort_key)
    
    # Create the final sequence mapping
    # 1. First, handle any core files that have a forced index
    # (Optional: If you want to keep them 01-13 regardless of date)
    
    # Actually, let's just number everyone globally 001 to N to keep it unique.
    # But if it's one of the 1-13 ones, we use that ID.
    
    used_numbers = set()
    final_mapping = []
    
    # Pass 1: Handle forced indices
    for f_info in all_files:
        if f_info["assigned_idx"]:
            num = f_info["assigned_idx"]
            final_mapping.append((f_info, num))
            used_numbers.add(num)
            
    # Pass 2: Handle everyone else
    current_idx = 1
    for f_info in all_files:
        if f_info["assigned_idx"]: continue # already handled
        
        # Find next free number
        while f"{current_idx:03d}" in used_numbers or f"{current_idx:02d}" in used_numbers:
            current_idx += 1
        
        num_str = f"{current_idx:03d}"
        final_mapping.append((f_info, num_str))
        used_numbers.add(num_str)
        current_idx += 1
        
    # Execute renaming
    for f_info, idx in final_mapping:
        old_path = f_info["path"]
        
        # Strip old indices
        clean_name = old_path.name
        clean_name = re.sub(r'^\d{2,3}_', '', clean_name)
        clean_name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', clean_name)
        
        # Get date
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', old_path.name)
        date_str = date_match.group(1) if date_match else "2026-03-13"
        
        new_name = f"{idx}_{date_str}_{clean_name}"
        new_path = old_path.parent / new_name
        
        if old_path != new_path:
            print(f"Renaming {old_path.name} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    renumber_global()
