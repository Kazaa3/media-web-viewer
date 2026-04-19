import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from src.core.config_master import PROGRAM_REGISTRY
print(f"FFMPEG: {PROGRAM_REGISTRY.get('ffmpeg')}")
print(f"VLC: {PROGRAM_REGISTRY.get('vlc')}")
