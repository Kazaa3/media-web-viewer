import os
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path("/home/xc/#Coding/gui_media_web_viewer/logbuch")

# Curated Top 20 Candidates
CURATED = [
    "The_Skeleton",
    "Architecture_Eel_Python",
    "The_Modular_Heart",
    "Frontend_Orchestration",
    "Serving_the_Content",
    "Format_Diversity",
    "Metadata_Pipeline",
    "Real_Time_Transcoding",
    "Persistence_Layer",
    "Environment_Hygiene",
    "Project_Strategy",
    "Quality_Assurance",
    "Roadmap",
    "Genese",
    "Genus",
    "Doku-Messy",
    "Overview_Logbook",
    "Series",
    "Milestone",
    "Story"
]

def clean_name(name):
    name = re.sub(r'^[0-9_]+', '', name) # Remove existing ID
    name = re.sub(r'\d{4}-\d{2}-\d{2}', '', name) # Remove dates
    name = name.replace(".md", "").replace(".mmd", "")
    name = name.strip("_")
    return name

def run_master_cleaner():
    all_files = []
    
    # Collect all md files from the 3 sub-folders
    subfolders = ["01_Architektur_und_Konzepte", "02_Features_und_Implementation", "03_Walkthroughs_und_Berichte"]
    for sub in subfolders:
        dir_path = ROOT / sub
        if not dir_path.exists(): continue
        for f in dir_path.rglob("*.md"):
            if f.is_file():
                all_files.append({
                    "path": f,
                    "mtime": os.path.getmtime(f),
                    "name": clean_name(f.name),
                    "is_curated": False,
                    "folder": sub
                })

    # Identify curated items
    curated_items = []
    others = []
    
    # Check current names and content for curation keywords
    for x in all_files:
        is_curated = False
        for key in CURATED:
            if key.lower() in x["name"].lower():
                is_curated = True
                break
        
        if is_curated:
            x["is_curated"] = True
            curated_items.append(x)
        else:
            others.append(x)
            
    # Sort curated by some logic or just mtime for now (but they'll be capped at 20)
    curated_items.sort(key=lambda x: x["mtime"])
    # Sort others by mtime (chronological history)
    others.sort(key=lambda x: x["mtime"])
    
    # Merge into a single list
    final_list = curated_items[:20] + [i for i in others if i not in curated_items]
    
    print(f"Master Cleaner: Processing {len(final_list)} entries...")
    
    # Final sequential rename
    for i, item in enumerate(final_list):
        new_id = f"{i+1:03d}"
        new_filename = f"{new_id}_{item['name']}.md"
        
        # Determine target folder: 1-25 always in concepts, rest keep original or logic
        target_sub = "01_Architektur_und_Konzepte" if i < 25 else item["folder"]
        target_path = ROOT / target_sub / new_filename
        
        print(f"Renaming: {item['path'].name} -> {new_filename}")
        
        # Ensure subfolder exists
        (ROOT / target_sub).mkdir(parents=True, exist_ok=True)
        
        # Rename on disk
        if item["path"] != target_path:
            # If target exists (due to a previous run), we might need to be careful
            if target_path.exists():
                os.remove(target_path)
            shutil.move(item["path"], target_path)

if __name__ == "__main__":
    run_master_cleaner()
