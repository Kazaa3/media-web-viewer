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
        title = get_title(f).lower()
        filename = f.name.lower()
        
        assigned_idx = None
        for key, idx in GAPLESS_SERIES.items():
            if key.lower() in title or key.lower().replace(" ", "_") in filename:
                assigned_idx = idx
                break
        
        all_files.append({
            "path": f,
            "title": title,
            "filename": f.name,
            "assigned_idx": assigned_idx
        })
    
    # Sort files by date (using the YYYY-MM-DD in the filename)
    def sort_key(x):
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', x["filename"])
        date = date_match.group(1) if date_match else "1970-01-01"
        return (date, x["filename"])

    all_files.sort(key=sort_key)
    
    # Counter for non-assigned files
    current_free_idx = 14
    
    for f_info in all_files:
        old_path = f_info["path"]
        
        if f_info["assigned_idx"]:
            idx_str = f_info["assigned_idx"]
        else:
            idx_str = f"{current_free_idx:03d}"
            current_free_idx += 1
            
        # Clean name
        new_name_base = old_path.name
        new_name_base = re.sub(r'^\d{2,3}_', '', new_name_base)
        new_name_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', new_name_base)
        
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', old_path.name)
        date_str = date_match.group(1) if date_match else "2026-03-13"
        
        new_name = f"{idx_str}_{date_str}_{new_name_base}"
        new_path = old_path.parent / new_name
        
        if old_path != new_path:
            print(f"Moving {old_path.name} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    renumber()
