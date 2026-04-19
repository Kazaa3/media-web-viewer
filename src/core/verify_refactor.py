import sys
import os
from pathlib import Path

# Setup path
_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_root))
sys.path.insert(0, str(_root / "src"))

try:
    from src.core.config_master import PROGRAM_REGISTRY, BROWSER_REGISTRY, MEDIA_RESOURCE_REGISTRY, GLOBAL_CONFIG
    from src.core import api_tools, api_transcoding, api_core_app, api_parsing
    
    print("SUCCESS: All API modules and registries loaded.")
    print(f"FFmpeg Path: {PROGRAM_REGISTRY.get('ffmpeg')}")
    print(f"VLC Path: {PROGRAM_REGISTRY.get('vlc')}")
    print(f"Project Root: {GLOBAL_CONFIG['storage_registry']['project_root']}")
    
    # Test tool health report
    health = api_tools.get_tool_health_report()
    print(f"Tool Health Check: {len(health)} tools registered.")
    
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
