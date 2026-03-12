import subprocess
import re
from pathlib import Path
from typing import Any


def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight') -> dict[str, Any]:
    """
    @brief Extracts metadata using mkvinfo CLI.
    @details Extrahiert Metadaten mittels mkvinfo CLI.
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if file_type.lower() != '.mkv':
        return tags

    try:
        # We use -v to get more info if needed, but for basic tags, default output is fine.
        cmd = ["mkvinfo", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            return tags
            
        output = result.stdout
        
        # Parse Duration: | + Duration: 01:23:45.678 (5025.678s)
        duration_match = re.search(r"Duration: .*?\((\d+\.\d+)s\)", output)
        if duration_match and not tags.get('duration'):
            try:
                tags['duration'] = int(float(duration_match.group(1)))
            except (ValueError, TypeError):
                pass

        # Parse Title: | + Title: Some Title
        title_match = re.search(r"Title: (.*)", output)
        if title_match and not tags.get('title'):
            tags['title'] = title_match.group(1).strip()

        # Parse Muxing App: | + Multiplexing application: ...
        muxing_app_match = re.search(r"Multiplexing application: (.*)", output)
        if muxing_app_match:
            tags['muxing_app'] = muxing_app_match.group(1).strip()

        # Parse Writing App: | + Writing application: ...
        writing_app_match = re.search(r"Writing application: (.*)", output)
        if writing_app_match:
            tags['writing_app'] = writing_app_match.group(1).strip()

        # Parse Tracks (Basic check)
        if mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            tags['full_tags']['mkvinfo_raw'] = output

    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass

    return tags
