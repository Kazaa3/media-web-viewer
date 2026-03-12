import subprocess
import json
from pathlib import Path
from typing import Any


def parse(path: Path, file_type: str, tags: dict[str, Any], filename: str = None, mode: str = 'lightweight') -> dict[str, Any]:
    """
    @brief Extracts metadata using mkvmerge JSON identification.
    @details Extrahiert Metadaten mittels mkvmerge JSON-Identifizierung.
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if file_type.lower() != '.mkv':
        return tags

    try:
        # mkvmerge -J provides a nice structured JSON
        cmd = ["mkvmerge", "-J", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
        
        if result.returncode != 0:
            return tags
            
        data = json.loads(result.stdout)
        
        container = data.get('container', {})
        properties = container.get('properties', {})
        
        # Duration: reported in nanoseconds
        if not tags.get('duration') and 'duration' in properties:
            try:
                # nanoseconds -> seconds
                tags['duration'] = int(int(properties['duration']) / 1_000_000_000)
            except (ValueError, TypeError):
                pass

        # Title
        if not tags.get('title') and 'title' in properties:
            tags['title'] = properties['title']

        # Apps
        if 'muxing_application' in properties:
            tags['muxing_app'] = properties['muxing_application']
        if 'writing_application' in properties:
            tags['writing_app'] = properties['writing_application']

        # Tracks
        tracks = data.get('tracks', [])
        if tracks and mode == 'full':
            if 'full_tags' not in tags:
                tags['full_tags'] = {}
            tags['full_tags']['mkvmerge_json'] = data

        # Simple codec/container fallback
        if not tags.get('container') and container.get('type'):
            tags['container'] = container['type'].lower()

    except subprocess.TimeoutExpired:
        pass
    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    return tags
