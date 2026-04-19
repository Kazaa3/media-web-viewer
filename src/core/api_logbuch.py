import os
import re
import time
import eel
from pathlib import Path
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT, DEFAULT_TIME_FORMAT
from src.core.logger import get_logger

log = get_logger("api_logbuch")

def get_language():
    """Returns the currently selected UI language (v1.46.136 Centralized)."""
    # Note: In a full refactor, this might come from a central state manager
    reg = GLOBAL_CONFIG.get("parser_registry", {})
    return reg.get("language", "de")

@eel.expose
def get_logbook_entry(feature_name, source="logbuch"):
    root_dir = PROJECT_ROOT
    if source == "root":
        allowed_root_files = {"README.md", "DOCUMENTATION.md", "INSTALL.md", "DEPENDENCIES.md", "LICENSE.md"}
        requested = feature_name if feature_name.endswith(".md") else f"{feature_name}.md"
        if requested not in allowed_root_files:
            return f"<h1>Error</h1><p>Root entry '{feature_name}' not allowed.</p>"
        log_file = root_dir / requested
    elif feature_name.upper() in ["README", "README.MD"]:
        log_file = root_dir / "README.md"
    else:
        log_dir = Path(GLOBAL_CONFIG["storage_registry"]["logbuch_dir"])
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = None
        if "/" in feature_name:
            candidate = log_dir / feature_name
            if not candidate.name.endswith(".md"): candidate = candidate.with_suffix(".md")
            if candidate.exists(): log_file = candidate
        if not log_file:
            for f in log_dir.rglob("*.md"):
                if f.stem == feature_name or f.name == feature_name or feature_name in f.name:
                    log_file = f
                    break
        if not log_file or not log_file.exists():
            return f"<h1>Error</h1><p>Logbook entry for '{feature_name}' not found.</p>"

    try:
        content = log_file.read_text(encoding='utf-8')
        if "<!-- lang-split -->" in content:
            parts = content.split("<!-- lang-split -->")
            if len(parts) >= 2:
                return parts[1].strip() if get_language().lower() == "en" else parts[0].strip()
        return content
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

def _normalize_status(status_raw):
    s = (status_raw or "").strip().upper()
    if not s: return "ACTIVE"
    if any(k in s for k in ["COMPLETE", "DONE", "FERTIG"]): return "COMPLETED"
    if any(k in s for k in ["PLAN", "IDEA"]): return "PLAN"
    if any(k in s for k in ["DOC", "DOCUMENTATION"]): return "DOCS"
    if any(k in s for k in ["BUG", "ISSUE", "FIXME"]): return "BUG"
    return "ACTIVE"

@eel.expose
def list_logbook_entries():
    log_dir = Path(GLOBAL_CONFIG["storage_registry"]["logbuch_dir"])
    if not log_dir.exists(): return []
    entries = []
    current_lang = get_language().lower()
    
    for f in sorted(list(log_dir.rglob("*.md")) + list(log_dir.rglob("*.mmd")), key=lambda x: x.name):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                lines = [fp.readline() for _ in range(20)]
                category, status, title, pinned = "Sonstiges", "ACTIVE", f.stem, False
                title_de, title_en, summary, summary_de, summary_en = "", "", "", "", ""

                for line in lines:
                    line = line.strip()
                    content = line.split("<!--")[1].split("-->")[0].strip() if "<!--" in line and "-->" in line else line
                    if ":" in content:
                        key, val = [x.strip() for x in content.split(":", 1)]
                        if key == "Category": category = val
                        elif key == "Status": status = val
                        elif key == "Pinned": pinned = val.lower() in ["true", "yes", "1"]
                        elif key == "Title_DE": title_de = val
                        elif key == "Title_EN": title_en = val
                        elif key == "Summary_DE": summary_de = val
                        elif key == "Summary_EN": summary_en = val
                        elif key == "Summary": summary = val
                    if line.startswith("# "): title = line.replace("# ", "").strip()

                final_title = (title_en if current_lang == "en" else title_de) or title
                final_summary = (summary_en if current_lang == "en" else summary_de) or summary
                
                entries.append({
                    "name": f.stem, "filename": f.name, "title": final_title,
                    "category": category, "summary": final_summary,
                    "status": _normalize_status(status), "pinned": pinned,
                    "source": "logbuch", "modified_ts": f.stat().st_mtime,
                    "modified_iso": time.strftime('%Y-%m-%d ' + DEFAULT_TIME_FORMAT, time.localtime(f.stat().st_mtime)),
                })
        except Exception:
            entries.append({"name": f.stem, "filename": f.name, "title": f.stem, "category": "Fehler", "status": "ERROR"})
    return entries

@eel.expose
def save_logbook_entry(filename, content):
    log_dir = Path(GLOBAL_CONFIG["storage_registry"]["logbuch_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)
    if not filename.endswith('.md'): filename += '.md'
    if '/' in filename or '\\' in filename or filename.startswith('.'): return {"error": "Invalid filename"}
    file_path = log_dir / filename
    try:
        if "Status:" not in content and "<!-- Status:" not in content:
            content = f"<!-- Status: ACTIVE -->\n{content}"
        file_path.write_text(content, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"error": str(e)}

@eel.expose
def delete_logbook_entry(filename):
    log_dir = Path(GLOBAL_CONFIG["storage_registry"]["log_dir"]) # Note: main.py used log_dir here, maybe check if it should be logbuch_dir
    if not filename.endswith('.md'): filename += '.md'
    file_path = log_dir / filename
    try:
        if file_path.exists(): file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}
