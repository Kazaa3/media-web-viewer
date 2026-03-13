#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Documentation / Management
# Eingabewerte: logbuch/ Verzeichnis
# Ausgabewerte: Listenansicht, neue Logbuch-Dateien, Validierungsberichte, reorganisierte Dateien
# Testdateien: tests/integration/test_logbook_parsing.py
# ERWEITERUNGEN (TODO): [ ] PDF-Export, [ ] Dokumentations-Webview
# KOMMENTAR: Zentraler Verwalter für die Projekt-Logbücher (Dokumentations-Suite).
# VERWENDUNG: python3 scripts/logbook_manager.py list|create|lint|reorganize

"""
KATEGORIE: Documentation / Management
ZWECK: Zentrales Tool zum Verwalten (Listen, Erstellen, Prüfen, Reorganisieren) der Logbuch-Einträge.
EINGABEWERTE: Pfad zum logbuch/ Ordner
AUSGABEWERTE: Formatiere Terminal-Ausgabe, neue/umbenannte Markdown-Dateien
TESTDATEIEN: tests/integration/test_logbook_parsing.py
ERWEITERUNGEN (TODO): [ ] Integration in CI, [ ] Automatische Git-Commits nach Erstellung
KOMMENTAR: Stellt die Konsistenz der bilingualen Dokumentationsstruktur sicher.
VERWENDUNG: python3 scripts/logbook_manager.py create "Thema" | list | lint | reorganize
"""

import os
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path

# --- Configuration ---
LOGBOOK_DIR = "logbuch"
REQUIRED_SECTIONS = [
    (re.compile(r"##\s*ZIELE?", re.I), "ZIELE/ZIEL"),
    (re.compile(r"##\s*KONZEPTE?", re.I), "KONZEPT"),
    (re.compile(r"##\s*UMSETZUNG", re.I), "UMSETZUNG"),
    (re.compile(r"##\s*STATUS", re.I), "STATUS"),
    (re.compile(r"STAND:", re.I), "STAND")
]

TEMPLATE = """# Logbuch: {title}

## Ziel
{description}

---

## Konzept
- 

---

## Umsetzung
- 

---

## Vorteile
- 

---

## Status
- In Bearbeitung

**Stand:** {date}

---

## Kontext & Verweise
- 
"""

def get_logbook_path(root):
    return Path(root) / LOGBOOK_DIR

def get_next_index(root):
    log_dir = get_logbook_path(root)
    if not log_dir.exists():
        return 1
    
    indices = []
    for file in log_dir.glob("*.md"):
        match = re.match(r"^(\d+)_", file.name)
        if match:
            indices.append(int(match.group(1)))
    
    return max(indices) + 1 if indices else 1

def list_logbooks(root, search=None):
    log_dir = get_logbook_path(root)
    if not log_dir.exists():
        print(f"❌ Verzeichnis {log_dir} nicht gefunden.")
        return

    files = sorted(list(log_dir.glob("*.md")))
    print(f"🔍 Gefundene Logbücher in {log_dir}:")
    print("-" * 80)
    
    count = 0
    for f in files:
        if search and search.lower() not in f.name.lower():
            continue
        
        # Try to extract the first line as a title
        title = ""
        try:
            with open(f, 'r', encoding='utf-8') as content:
                first_line = content.readline().strip()
                if first_line.startswith("#"):
                    title = first_line.replace("#", "").strip()
                elif first_line == "" : # Skip empty first line
                     next_line = content.readline().strip()
                     if next_line.startswith("#"):
                         title = next_line.replace("#", "").strip()
        except:
            pass
            
        print(f" {f.name:<45} | {title[:30]}")
        count += 1
    
    print("-" * 80)
    print(f"Gesamt: {count} Einträge.")

def create_logbook(root, title_input):
    log_dir = get_logbook_path(root)
    if not log_dir.exists():
        log_dir.mkdir(parents=True)
        
    index = get_next_index(root)
    safe_title = title_input.replace(" ", "_").replace("/", "-")
    filename = f"{index:02d}_{safe_title}.md"
    file_path = log_dir / filename
    
    if file_path.exists():
        print(f"❌ Datei {filename} existiert bereits.")
        return

    today = datetime.now().strftime("%d. %B %Y").lstrip("0").replace(" 0", " ")
    
    content = TEMPLATE.format(
        title=title_input,
        description="Dokumentation der Änderungen und Fortschritte.",
        date=today
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ Neues Logbuch erstellt: {file_path}")
    print(f"📝 Öffne die Datei zum Bearbeiten.")

def lint_logbooks(root):
    log_dir = get_logbook_path(root)
    if not log_dir.exists():
        return

    print(f"🔍 Validierung der Logbücher in {log_dir}...")
    print("=" * 80)
    
    failed = 0
    checked = 0
    
    for f in sorted(log_dir.glob("*.md")):
        checked += 1
        try:
            with open(f, 'r', encoding='utf-8') as content:
                text = content.read()
                
            missing = []
            for regex, label in REQUIRED_SECTIONS:
                if not regex.search(text):
                    missing.append(label)
            
            if missing:
                print(f"❌ {f.name:<45} | Fehlend: {', '.join(missing)}")
                failed += 1
        except Exception as e:
            print(f"⚠️  {f.name:<45} | Fehler beim Lesen: {e}")
            failed += 1
            
    print("=" * 80)
    print(f"Geprüft: {checked} | Fehlerhaft: {failed}")

def reorganize_logbooks(root, force=False):
    log_dir = get_logbook_path(root)
    if not log_dir.exists():
        return

    files = []
    for f in log_dir.glob("*.md"):
        if f.name in ["Watchdog_Live_Log.md", "000_Index.md"]:
            continue
        
        match = re.match(r"^(\d+)_", f.name)
        index = int(match.group(1)) if match else 999
        files.append({"path": f, "index": index, "name": f.name})

    # Sort by original index, then by modification time for those without index
    files.sort(key=lambda x: (x["index"], x["path"].stat().st_mtime))

    print(f"🔧 Reorganisiere {len(files)} Logbücher...")
    
    changes = []
    for i, item in enumerate(files, 1):
        original_name = item["name"]
        
        # Strip old index if exists
        clean_name = re.sub(r"^\d+_", "", original_name)
        new_name = f"{i:02d}_{clean_name}"
        
        if original_name != new_name:
            changes.append((item["path"], log_dir / new_name))

    if not changes:
        print("✅ Alles bereits korrekt sortiert.")
        return

    print(f"⚠️  {len(changes)} Umbenennungen geplant:")
    for old, new in changes:
        print(f"  {old.name} -> {new.name}")

    if not force:
        confirm = input("\nFortfahren? (y/N): ")
        if confirm.lower() != 'y':
            print("🛑 Abgebrochen.")
            return

    for old, new in changes:
        try:
            old.rename(new)
        except Exception as e:
            print(f"❌ Fehler beim Umbenennen von {old.name}: {e}")

    print("✅ Reorganisation abgeschlossen.")

def rename_logbook(root, old_name, new_title):
    log_dir = get_logbook_path(root)
    old_path = log_dir / old_name
    if not old_path.exists():
        # Try adding .md
        old_path = log_dir / (old_name + ".md")
        if not old_path.exists():
            print(f"❌ Datei {old_name} nicht gefunden.")
            return

    match = re.match(r"^(\d+)_", old_path.name)
    index_prefix = match.group(0) if match else ""
    
    safe_title = new_title.replace(" ", "_").replace("/", "-")
    if not safe_title.endswith(".md"):
        safe_title += ".md"
        
    new_name = f"{index_prefix}{safe_title}" if index_prefix else safe_title
    new_path = log_dir / new_name

    if new_path.exists():
        print(f"❌ Zielldatei {new_name} existiert bereits.")
        return

    old_path.rename(new_path)
    print(f"✅ Umbenannt: {old_path.name} -> {new_path.name}")

def main():
    parser = argparse.ArgumentParser(description="Media Web Viewer Logbook Manager")
    subparsers = parser.add_subparsers(dest="command", help="Optionen")

    # List
    list_parser = subparsers.add_parser("list", help="Alle Logbücher auflisten")
    list_parser.add_argument("--search", type=str, help="Filter nach Suchbegriff")

    # Create
    create_parser = subparsers.add_parser("create", help="Neues Logbuch erstellen")
    create_parser.add_argument("title", type=str, help="Titel des Logbuchs")

    # Lint
    lint_parser = subparsers.add_parser("lint", help="Logbücher validieren")

    # Reorganize
    reorg_parser = subparsers.add_parser("reorganize", help="Indices neu sortieren und Lücken füllen")
    reorg_parser.add_argument("--force", action="store_true", help="Ohne Bestätigung ausführen")

    # Rename
    rename_parser = subparsers.add_parser("rename", help="Ein Logbuch umbenennen (Titel ändern)")
    rename_parser.add_argument("old_name", type=str, help="Aktueller Dateiname")
    rename_parser.add_argument("new_title", type=str, help="Neuer Titel (Inhalt)")

    args = parser.parse_args()
    root_dir = Path(__file__).parents[1]

    if args.command == "list":
        list_logbooks(root_dir, search=args.search)
    elif args.command == "create":
        create_logbook(root_dir, args.title)
    elif args.command == "lint":
        lint_logbooks(root_dir)
    elif args.command == "reorganize":
        reorganize_logbooks(root_dir, args.force)
    elif args.command == "rename":
        rename_logbook(root_dir, args.old_name, args.new_title)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
