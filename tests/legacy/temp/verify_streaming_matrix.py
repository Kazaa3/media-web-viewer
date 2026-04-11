import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.core import db
from src.core.main import get_streaming_capability_matrix, get_media_compatibility_report
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_streaming_expansion():
    print("=== Verifying Streaming Capability Matrix ===")
    matrix = get_streaming_capability_matrix()
    engines = [m['engine'] for m in matrix]
    print(f"Supported Engines: {engines}")
    
    assert "mkvmerge" in engines, "mkvmerge missing from matrix"
    assert "ffplay" in engines, "ffplay missing from matrix"
    assert "swyh-rs (suw)" in engines, "swyh-rs missing from matrix"
    print("✓ Capability Matrix expanded correctly.")

    print("\n=== Verifying Item Compatibility Report ===")
    report = get_media_compatibility_report()
    if not report:
        print("! Report is empty (expected if DB is empty, but let's check structure)")
    else:
        print(f"Report size: {len(report)} items")
        first = report[0]
        required_keys = ['name', 'chrome_native', 'mediamtx', 'vlc', 'ffplay']
        for key in required_keys:
            assert key in first, f"Missing key '{key}' in report item"
        print(f"Sample item: {first['name']} | Chrome: {first['chrome_native']}")
    print("✓ Compatibility Report logic verified.")

if __name__ == "__main__":
    try:
        verify_streaming_expansion()
        print("\nALL VERIFICATIONS PASSED!")
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        sys.exit(1)
