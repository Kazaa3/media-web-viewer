import os
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer")
SOURCES = [
    ROOT / "logbuch",                      # Current active reorganization root
    ROOT / "docs" / "logbuch",             # Old core location
    ROOT / "docs" / "logbuch" / "archive"  # Archive location
]

TARGET_ROOT = ROOT / "logbuch"
FOLDERS = [
    "01_Architektur_und_Konzepte",
    "02_Features_und_Implementation",
    "03_Walkthroughs_und_Berichte"
]

CORE_GAPLESS = {
    "The Skeleton": "01",
    "Architecture Eel Python": "02",
    "The Modular Heart": "03",
    "Frontend Orchestration": "04",
    "Serving the Content Bottle": "05",
    "Format Diversity or Codecs": "06", # Generalized match
    "Metadata Pipeline": "07",
    "Real Time Transcoding": "08",
    "Persistence Layer": "09",
    "Environment Hygiene": "10",
    "Project Strategy": "11",
    "Quality Assurance": "12",
    "Roadmap Future": "13",
    "Overview Logbook Gapless": "00" # Let's keep Overview as 00
}

def get_file_metadata(filepath):
    content = ""
    try:
        content = filepath.read_text(encoding='utf-8')
    except: pass
    
    title = ""
    match = re.search(r'# (.*)', content)
    if match: title = match.group(1).strip()
    else:
        match = re.search(r'Title_EN:\s*(.*)', content)
        if match: title = match.group(1).strip()
        
    date_str = "2026-03-13"
    # Try date in filename
    d_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    if d_match: date_str = d_match.group(1)
    else:
        # Try date in content
        d_match = re.search(r'\*\*Datum:\*\*\s*(\d{2}\.\d{2}\.\d{4})', content)
        if d_match:
            try:
                date_str = datetime.strptime(d_match.group(1), "%d.%m.%Y").strftime("%Y-%m-%d")
            except: pass
            
    # Category metadata
    category_meta = None
    if "<!-- Category:" in content:
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
       or any(kw in name_lower or kw in title_lower or kw in content_lower for kw in ["foundations", "roadmap", "genese", "architektur", "planung", "planning", "anforderungen", "uebersicht", "overview"]):
        return FOLDERS[0]
        
    # Default to 02
    return FOLDERS[1]

# 1. Collect all files from all sources
all_entries = []
seen_identifiers = set()

for src in SOURCES:
    if not src.exists(): continue
    for f in src.rglob("*"):
        if f.is_file() and f.suffix in [".md", ".mmd"]:
            title, date, cat_meta, content = get_file_metadata(f)
            # Create a unique identifier to avoid duplicates between sources
            # Use original filename after stripping existing numbering
            clean_base = re.sub(r'^\d{2,3}_', '', f.name)
            clean_base = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', clean_base)
            
            # Simple deduplication based on clean name
            if clean_base in seen_identifiers: continue
            seen_identifiers.add(clean_base)
            
            # Check for core series
            assigned_idx = None
            for key, idx in CORE_GAPLESS.items():
                if key.lower() in title.lower() or key.lower() in clean_base.lower().replace("_", " "):
                    assigned_idx = idx
                    break
            
            target_folder = get_target_folder(f.name, title, cat_meta, content)
            
            all_entries.append({
                "old_path": f,
                "clean_base": clean_base,
                "title": title,
                "date": date,
                "cat": target_folder,
                "assigned_idx": assigned_idx
            })

# 2. Sort all by date
all_entries.sort(key=lambda x: (x["date"], x["clean_base"]))

# 3. Assign global unique IDs
used_numbers = set()
final_mapping = []

# Pass 1: Forced indices (01-13)
for entry in all_entries:
    if entry["assigned_idx"]:
        final_mapping.append((entry, entry["assigned_idx"]))
        used_numbers.add(entry["assigned_idx"])

# Pass 2: Others starting from 014
current_idx = 14
for entry in all_entries:
    if entry["assigned_idx"]: continue
    num_str = f"{current_idx:03d}"
    final_mapping.append((entry, num_str))
    used_numbers.add(num_str)
    current_idx += 1

# 4. Prepare target folders
for folder in FOLDERS:
    (TARGET_ROOT / folder).mkdir(parents=True, exist_ok=True)

# 5. Move & Rename everything
print(f"Moving {len(final_mapping)} files to global target structure...")
for entry, idx in final_mapping:
    new_name = f"{idx}_{entry['date']}_{entry['clean_base']}"
    target_path = TARGET_ROOT / entry["cat"] / new_name
    
    # Check for name collisions in the same target folder
    if target_path.exists() and target_path != entry["old_path"]:
         new_name = f"{idx}_{entry['date']}_v2_{entry['clean_base']}"
         target_path = TARGET_ROOT / entry["cat"] / new_name
         
    try:
        shutil.move(entry["old_path"], target_path)
    except Exception as e:
        print(f"Error moving {entry['old_path']}: {e}")

# Clean up empty source directories if they were from docs (be careful)
# We won't auto-delete directories for safety.

print("Master reorganization complete.")
