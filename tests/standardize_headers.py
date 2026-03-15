import os
import sys
import time
from pathlib import Path

# Paths configuration
test_dir = Path("/home/xc/#Coding/gui_media_web_viewer/tests")
project_root = Path("/home/xc/#Coding/gui_media_web_viewer")

def clean_and_standardize(file_path):
    """Clean existing headers and apply the standardized template."""
    try:
        file_path = file_path.resolve()
        
        # Read content
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return False, "Encoding error"

        lines = content.splitlines()
        
        # Extract existing metadata
        metadata = {
            "Kategorie": "-",
            "Eingabewerte": "-",
            "Ausgabewerte": "-",
            "Testdateien": "-",
            "Kommentar": "-"
        }
        
        for line in lines[:20]:
            for key in metadata.keys():
                tag = f"# {key}:"
                if tag in line:
                    val = line.split(tag, 1)[1].strip()
                    if val and val != "-":
                        metadata[key] = val
        
        # Fallback for Kategorie
        if metadata["Kategorie"] == "-":
            try:
                rel_parts = file_path.relative_to(test_dir).parent.parts
                if rel_parts:
                    metadata["Kategorie"] = " / ".join(rel_parts).capitalize()
                else:
                    metadata["Kategorie"] = "General"
            except ValueError:
                metadata["Kategorie"] = "Tests"

        # Defaults
        if metadata["Eingabewerte"] == "-":
            metadata["Eingabewerte"] = file_path.name
        if metadata["Testdateien"] == "-":
            metadata["Testdateien"] = file_path.name
        if metadata["Ausgabewerte"] == "-":
            metadata["Ausgabewerte"] = "Test-Ergebnis"
        if metadata["Kommentar"] == "-":
            metadata["Kommentar"] = "Standardisierte Testdatei."

        # Find code start
        source_start = 0
        while source_start < len(lines):
            line = lines[source_start].strip()
            if not line or line.startswith("#!") or line.startswith("# -*- coding:") or \
               any(line.startswith(f"# {k}:") for k in metadata.keys()):
                source_start += 1
                continue
            break

        header = [
            "#!/usr/bin/env python3",
            "# -*- coding: utf-8 -*-",
            f"# Kategorie: {metadata['Kategorie']}",
            f"# Eingabewerte: {metadata['Eingabewerte']}",
            f"# Ausgabewerte: {metadata['Ausgabewerte']}",
            f"# Testdateien: {metadata['Testdateien']}",
            f"# Kommentar: {metadata['Kommentar']}",
            ""
        ]
        
        new_content = "\n".join(header) + "\n".join(lines[source_start:]).lstrip()
        
        # Write and check
        if new_content.strip() != content.strip():
            file_path.write_text(new_content, encoding='utf-8')
            
            # Verification check
            verify_content = file_path.read_text(encoding='utf-8')
            if verify_content.startswith("#!/usr/bin/env python3") and "# Kategorie:" in verify_content:
                return True, "Updated & Verified"
            else:
                return False, "Verification Failed"
        else:
            return True, "Already standardized"

    except Exception as e:
        return False, f"Error: {str(e)}"

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█'):
    """Call in a loop to create terminal progress bar."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total: 
        print()

def run():
    print(f"Standardizing tests in: {test_dir}\n")
    
    files_to_process = []
    for p in test_dir.rglob("*.py"):
        if p.name.startswith("__") or "venv" in str(p) or ".history" in str(p):
            continue
        files_to_process.append(p)

    total = len(files_to_process)
    if total == 0:
        print("No files found.")
        return

    success_count = 0
    fail_count = 0
    
    for i, file_path in enumerate(files_to_process, 1):
        rel_name = file_path.relative_to(project_root)
        success, msg = clean_and_standardize(file_path)
        
        if success:
            success_count += 1
        else:
            fail_count += 1
            # Move bar line up to print error without breaking bar
            print(f"\nERROR: {rel_name} -> {msg}")
            
        print_progress_bar(i, total, prefix='Progress:', suffix=f'Complete ({i}/{total})', length=50)

    print(f"\nHeader Standardization Finished.")
    print(f"Total: {total} | Success: {success_count} | Failed: {fail_count}")

if __name__ == "__main__":
    run()
