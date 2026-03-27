import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.core.mode_router import smart_route
    from src.core.streams import direct_play, mse_stream, hls_fmp4, vlc_bridge
    from src.core.ffprobe_analyzer import ffprobe_analyze
    print("✅ All modular imports successful.")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Dummy test for ffprobe_analyze (expect fail but check for crash)
try:
    res = ffprobe_analyze("/non/existent/file.mkv")
    print(f"✅ Analyzer robustness test passed (error handled: {res.get('error')})")
except Exception as e:
    print(f"❌ Analyzer crashed: {e}")

print("\nBackend Architecture Verification Complete.")
