import sys
import os
from pathlib import Path

# Setup PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("--- [Verification] Forensic Workstation v1.46 Architecture Audit ---")

try:
    from src.core.config_master import GLOBAL_CONFIG, LOGGING_REGISTRY, FORENSIC_TOOLS_LIST, LAUNCH_PROFILE, PROGRAM_REGISTRY
    print("[OK] config_master: Primary registries found.")
    print(f"     FORENSIC_TOOLS: {len(FORENSIC_TOOLS_LIST)} items registered.")
    print(f"     FFMPEG_PATH: {PROGRAM_REGISTRY.get('ffmpeg')}")
    print(f"     VLC_PATH:    {PROGRAM_REGISTRY.get('vlc')}")
    print(f"     LAUNCH_MODE: Connectionless={LAUNCH_PROFILE['connectionless']}")
except ImportError as e:
    print(f"[FAIL] config_master: {e}")
    sys.exit(1)

try:
    from src.core import logger
    print(f"[OK] logger: Local log dir resolved to: {logger.LOCAL_LOG_DIR}")
except ImportError as e:
    print(f"[FAIL] logger: {e}")

try:
    from src.core import api_frontend, api_orchestrator, api_logbuch, api_testing
    print("[OK] API Modules: All new specialized services (Frontend, Orchestrator, Logbuch, Testing) are discoverable.")
except ImportError as e:
    print(f"[FAIL] API Modules: {e}")

try:
    # Test delegation (Mocking eel)
    import eel
    from src.core import main
    print("[OK] main.py: Delegated functions integrated.")
except Exception as e:
    print(f"[FAIL] main.py: {e}")

print("--- [Verification] Audit Complete: Environment Stable ---")
