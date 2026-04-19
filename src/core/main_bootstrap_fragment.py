# Unified Forensic Audit Engine - Finalized Integration (v1.47.05) [AI-Anchor]

# --- SHIELDED BOOTSTRAP ---
try:
    # 2. Main Imports
    import psutil
    from unittest.mock import MagicMock
    
    # Dependency Shielding (v1.47)
    try:
        import bottle
    except ImportError:
        log.warning("[Bootstrap] Bottle missing. Mocking bridge active.")
        bottle = MagicMock()
    
    from src.core.eel_shell import eel
    from eel import chrome
    log.info("[Bootstrap] Eel loaded successfully")

    # --- CORE METADATA REGISTRY ---
    from src.core.config_master import (
        GLOBAL_CONFIG, APP_VERSION, APP_VERSION_CORE, APP_VERSION_FULL, BACKEND_VERSION, FRONTEND_VERSION,
        VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, ALL_AUDIO_EXTENSIONS, ALL_VIDEO_EXTENSIONS
    )
    from src.core.models import MASTER_CAT_MAP, TECH_MARKERS, MediaItem, get_allowed_internal_cats
    from src.core.transcoder import TranscoderManager
    from src.core import handbrake_wrapper as handbrake
    from src.core import api_library
    from src.core import api_reporting
    from src.core import mkv_tool_wrapper as mkv_tool
    from src.core.subtitle_processor import SubtitleProcessor
    import requests
    
    VERSION = APP_VERSION
    PROJECT_ROOT = _root
    
    # Initialize Global Managers
    transcode_mgr = TranscoderManager()
    
except ImportError as e:
    log.error(f"[Bootstrap] Required module missing: {e}")
    # Minimal fallback assignment to avoid NameErrors in subsequent code
    if 'eel' not in locals() and 'eel' not in globals():
        from src.core.eel_shell import eel
    sys.exit(1)
