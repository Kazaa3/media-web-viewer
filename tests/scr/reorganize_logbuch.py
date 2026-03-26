import os
import re
from datetime import datetime
from pathlib import Path
import shutil

LOGBUCH_DIR = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")
TARGET_FOLDERS = [
    "01_Architektur_und_Konzepte",
    "02_Features_und_Implementation",
    "03_Walkthroughs_und_Berichte"
]

def get_file_info(filepath):
    content = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        pass

    # Extract category from header metadata if available
    category_meta = None
    if "<!-- Category:" in content:
        try:
            category_meta = content.split("Category: ")[1].split(" -->")[0]
        except:
            pass

    # 1. Try to find date in filename (YYYY-MM-DD)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if date_match:
        date_str = date_match.group(1)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d"), category_meta, content
        except:
            pass

    # 2. Try to find date in content (**Datum:** DD.MM.YYYY or **Date:** YYYY-MM-DD or **Datum:** YYYY-MM-DD)
    date_match = re.search(r'\*\*Datum:\*\*\s*(\d{2}\.\d{2}\.\d{4})', content)
    if date_match:
        try:
            return datetime.strptime(date_match.group(1), "%d.%m.%Y"), category_meta, content
        except:
            pass
            
    date_match = re.search(r'\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        try:
            return datetime.strptime(date_match.group(1), "%Y-%m-%d"), category_meta, content
        except:
            pass
            
    date_match = re.search(r'\*\*Datum:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        try:
            return datetime.strptime(date_match.group(1), "%Y-%m-%d"), category_meta, content
        except:
            pass

    # 3. Fallback: Modification time
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime), category_meta, content

def get_target_folder(filename, category_meta, content):
    cat_lower = (category_meta or "").lower()
    content_lower = content.lower()
    name_lower = filename.lower()
    
    # Priority 1: Meta-Category
    if any(k in cat_lower for k in ["planung", "planning", "konzept", "concept", "roadmap", "overview", "uebersicht"]):
        return TARGET_FOLDERS[0]
    if any(k in cat_lower for k in ["untersuchungen", "tests", "validation", "audit", "walkthrough", "analyse"]):
        return TARGET_FOLDERS[2]
    if any(k in cat_lower for k in ["parser", "ui/ux", "implementation", "features", "umsetzung", "fix"]):
        return TARGET_FOLDERS[1]

    # Priority 2: Keyword heuristic
    if any(kw in name_lower or kw in content_lower for kw in ["foundations", "roadmap", "genese", "architektur", "planung", "planning", "anforderungen"]):
        return TARGET_FOLDERS[0]
        
    if any(kw in name_lower or kw in content_lower for kw in ["walkthrough", "bericht", "report", "summary", "audit", "verification", "validierung", "analyse", "recherche", "telemetrie", "auswertung", "benchmark"]):
        return TARGET_FOLDERS[2]
        
    # Default
    return TARGET_FOLDERS[1]

files = []
# Only process .md, .mmd files for re-numbering. Leave .py scripts at root for now.
for f in sorted(LOGBUCH_DIR.iterdir()):
    if f.is_file() and (f.suffix in [".md", ".mmd"]):
        # Special check: Skip actual core overview documents if strictly asked for.
        # But "alle durch nummerieren" is strong.
        date, cat_meta, content = get_file_info(f)
        target = get_target_folder(f.name, cat_meta, content)
        files.append({
            "path": f,
            "date": date,
            "cat": target,
            "old_name": f.name
        })

# Sort by date primarily, then by old name
files.sort(key=lambda x: (x["date"], x["old_name"]))

# Create folders
for folder in TARGET_FOLDERS:
    (LOGBUCH_DIR / folder).mkdir(parents=True, exist_ok=True)

# Prepare mapping for debugging/logging
print(f"Total files to reorganize: {len(files)}")

for i, f_info in enumerate(files, 1):
    idx_str = f"{i:03d}"
    date_str = f_info["date"].strftime("%Y-%m-%d")
    
    # Strip existing indices/dates to avoid "001_01_2026-03-14_2026-03-14_..."
    cleaned_name = f_info["old_name"]
    # Remove leading NNN_
    cleaned_name = re.sub(r'^\d{2,3}_', '', cleaned_name)
    # Remove leading YYYY-MM-DD_
    cleaned_name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', cleaned_name)
    
    new_name = f"{idx_str}_{date_str}_{cleaned_name}"
    target_path = LOGBUCH_DIR / f_info["cat"] / new_name
    
    try:
        shutil.move(f_info["path"], target_path)
    except Exception as e:
        print(f"Error moving {f_info['old_name']}: {e}")

print("Reorganization complete.")
