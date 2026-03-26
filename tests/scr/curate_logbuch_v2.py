import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# The Story of dict (Curated order for the first 20)
STORY_DOCS = [
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
    "Roadmap Future Milestones",
    "Overview Logbook Gapless",
    "Qualitaetstests Test Classification",
    "The Tech Stack",
    "From Skeleton to Player",
    "Skeleton Baseline",
    "Architektur Entwurf",
    "Status Update"
]

def clean_filename(name):
    # Remove existing IDs (NN_) and Dates (YYYY-MM-DD_) multiple times if nested
    # Also remove any starting numbers followed by underscore (e.g. 070_ or 87_)
    while re.match(r'^\d{1,3}_', name):
        name = re.sub(r'^\d{1,3}_', '', name)
    
    # Remove dates YYYY-MM-DD_
    name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', name)
    # Remove any dates inside _2026-03-22_
    name = re.sub(r'_\d{4}-\d{2}-\d{2}_', '_', name)
    # Remove any stray IDs middle of the name like _87_
    name = re.sub(r'_\d{1,3}_', '_', name)
    
    return name

def curate_logbuch_v2():
    all_files = []
    for f in ROOT.rglob("*.md"):
        if f.is_file():
            clean_name = clean_filename(f.name)
            all_files.append({
                "path": f,
                "clean_name": clean_name,
                "folder": f.parent.name
            })
            
    # Identify Story Files
    story_matches = []
    others = []
    
    for entry in all_files:
        is_story = False
        for i, story in enumerate(STORY_DOCS):
            if story.lower().replace(" ", "_") in entry["clean_name"].lower():
                story_matches.append((entry, i))
                is_story = True
                break
        if not is_story:
            others.append(entry)
            
    # Sort Story matches by their intended index
    story_matches.sort(key=lambda x: x[1])
    story_entries = [x[0] for x in story_matches]
    
    # Sort others by original modification date if possible (for chronological order)
    others.sort(key=lambda x: os.path.getmtime(x["path"]))
    
    # Final List
    final_indexing = story_entries + others
    
    target_arch = "01_Architektur_und_Konzepte"
    target_feat = "02_Features_und_Implementation"
    target_walk = "03_Walkthroughs_und_Berichte"

    print(f"Aggressive cleaning and renumbering of {len(final_indexing)} files...")
    for idx, entry in enumerate(final_indexing, 1):
        idx_str = f"{idx:03d}"
        new_name = f"{idx_str}_{entry['clean_name']}"
        
        # Decide folder: first 25 go to architecture (the story part)
        # Others stay in their folders if they were categorized, else stay in current.
        if idx <= 25:
            target_path = ROOT / target_arch / new_name
        else:
            target_path = ROOT / entry["folder"] / new_name
            
        # Ensure target dir exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if entry["path"] != target_path:
            try:
                os.rename(entry["path"], target_path)
            except Exception as e:
                # Use shutil.move for safe cross-dir moves if rename fails
                try:
                    shutil.move(entry['path'], target_path)
                except:
                    print(f"Error moving {entry['path']}: {e}")

if __name__ == "__main__":
    curate_logbuch_v2()
