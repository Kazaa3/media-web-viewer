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
    "Roadmap Future",
    "Overview Logbook Gapless",
    "Projekt Genese und Philosophie",
    "The Tech Stack",
    "From Skeleton to Player",
    "Skeleton Baseline",
    "Architektur Entwurf",
    "Status Update"
]

def clean_filename(name):
    # Remove existing IDs (NN_) and Dates (YYYY-MM-DD_)
    name = re.sub(r'^\d{2,3}_', '', name)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', name)
    # Also remove any leftover dates within the name parts if they look like _2026-03-13_
    name = re.sub(r'_\d{4}-\d{2}-\d{2}_', '_', name)
    return name

def curate_logbuch():
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
    
    # Sort others by filename (optional but keeps a stable order)
    others.sort(key=lambda x: x["clean_name"])
    
    # Final List
    final_indexing = story_entries + others
    
    print(f"Renumbering {len(final_indexing)} files (removing dates from names)...")
    for idx, entry in enumerate(final_indexing, 1):
        idx_str = f"{idx:03d}"
        new_name = f"{idx_str}_{entry['clean_name']}"
        new_path = entry["path"].parent / new_name
        
        if entry["path"] != new_path:
            try:
                os.rename(entry["path"], new_path)
            except Exception as e:
                # If target exists, try adding a suffix to make it move
                if os.path.exists(new_path):
                     new_name = f"{idx_str}_v2_{entry['clean_name']}"
                     os.rename(entry["path"], entry["path"].parent / new_name)
                else: print(f"Error: {e}")

if __name__ == "__main__":
    curate_logbuch()
