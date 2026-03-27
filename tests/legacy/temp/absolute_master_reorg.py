import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer")
SOURCES = [
    ROOT / "logbuch",
    ROOT / "docs" / "logbuch",
    ROOT / "docs" / "logbuch" / "archive"
]

TARGET_ROOT = ROOT / "logbuch"
FOLDERS = [
    "01_Architektur_und_Konzepte",
    "02_Features_und_Implementation",
    "03_Walkthroughs_und_Berichte"
]

def get_file_metadata(filepath):
    content = ""
    try: content = filepath.read_text(encoding='utf-8')
    except: pass
    
    title = ""
    match = re.search(r'# (.*)', content)
    if match: title = match.group(1).strip()
    
    date_str = "1970-01-01"
    # Try date in filename
    d_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if d_match: date_str = d_match.group(1)
            
    # Category metadata
    category_meta = None
    if "Category:" in content:
        try: category_meta = content.split("Category: ")[1].split(" -->")[0]
        except: pass

    return title, date_str, category_meta, content

def get_target_folder(filename, title, category_meta, content):
    cat_lower = (category_meta or "").lower()
    content_lower = content.lower()
    name_lower = filename.lower()
    title_lower = title.lower()
    
    # 03_Walkthroughs_und_Berichte
    if any(k in cat_lower for k in ["untersuchungen", "tests", "validation", "audit", "walkthrough", "analyse"]) \
       or any(kw in name_lower or kw in title_lower or kw in content_lower for kw in ["walkthrough", "bericht", "report", "summary", "audit", "verification", "validierung", "analyse", "recherche", "telemetrie", "auswertung", "benchmark", "benchmarking"]):
        return FOLDERS[2]
        
    # 01_Architektur_und_Konzepte
    if any(k in cat_lower for k in ["planung", "planning", "konzept", "concept", "roadmap", "overview", "uebersicht"]) \
       or any(kw in name_lower or kw in title_lower or kw in content_lower for kw in ["foundations", "roadmap", "architecture", "architektur", "planung", "planning", "anforderungen", "uebersicht", "overview", "genese"]):
        return FOLDERS[0]
        
    # Default to 02
    return FOLDERS[1]

# 1. Collect all files across all sources
all_entries = []
seen_identifiers = set()

for src in SOURCES:
    if not src.exists(): continue
    for f in src.rglob("*"):
        if f.is_file() and f.suffix in [".md", ".mmd"]:
            # Strip numbers and dates for deduplication
            clean_base = re.sub(r'^\d{2,3}_', '', f.name)
            clean_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', clean_base)
            
            if clean_base in seen_identifiers: continue
            seen_identifiers.add(clean_base)
            
            title, date, cat_meta, content = get_file_metadata(f)
            target_folder = get_target_folder(f.name, title, cat_meta, content)
            
            all_entries.append({
                "old_path": f,
                "clean_base": clean_base,
                "title": title,
                "date": date,
                "cat": target_folder
            })

# 2. Sort ALL by date primarily, then by name
all_entries.sort(key=lambda x: (x["date"], x["clean_base"]))

# 3. Rename into global target structure
for folder in FOLDERS:
    (TARGET_ROOT / folder).mkdir(parents=True, exist_ok=True)

print(f"Executing global re-indexing of {len(all_entries)} files...")
for idx, entry in enumerate(all_entries, 1):
    # Ensure 3-digit numbering for consistency, or 2-digit for 1-13 if desired.
    # The user wanted 1-13 to stay. If I use 3-digit even for them (001), it's cleaner.
    # But I'll follow the user's lead for 01-13 if possible.
    if idx <= 13:
        idx_str = f"{idx:02d}"
    else:
        idx_str = f"{idx:03d}"
        
    new_name = f"{idx_str}_{entry['date']}_{entry['clean_base']}"
    target_path = TARGET_ROOT / entry["cat"] / new_name
    
    # Avoid moving into itself or overwriting
    if target_path != entry["old_path"]:
        try:
            shutil.move(entry["old_path"], target_path)
        except Exception as e:
            # If move fails, try copying and then delete (more robust across filesystems)
            try:
                shutil.copy2(entry["old_path"], target_path)
                os.remove(entry["old_path"])
            except:
                print(f"Failed to move {entry['old_path']} to {target_path}")

# Delete old folders if they are empty
# (Optional)

print("Global technically unique chronological technical record indexing completed.")
