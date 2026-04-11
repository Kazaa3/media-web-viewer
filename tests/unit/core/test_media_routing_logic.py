#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_routing_logic():
    print("[TEST] Initializing Routing Logic Test...")
    from src.parsers.format_utils import is_direct_play_capable, ffprobe_quality_score
    
    # Test Cases: (Extension, Codec, Expected Direct Play)
    cases = [
        (".mp4", "h264", True),
        (".webm", "vp9", True),
        (".mkv", "hevc", False),
        (".iso", "", False),
        (".mp3", "mp3", True)
    ]
    
    success = True
    for ext, codec, expected in cases:
        # Mocking is_chrome_native behavior for rapid testing
        from src.parsers.format_utils import is_chrome_native
        result = is_chrome_native(ext, codec)
        if result == expected:
            print(f"  [PASS] {ext}/{codec} -> {result}")
        else:
            print(f"  [FAIL] {ext}/{codec} -> Expected {expected}, got {result}")
            success = False
            
    print("\n[TEST] Quality Score Validation...")
    # Test Quality Scores
    tags_high = {"width": 1920, "height": 1080, "v_bitrate": "5000000"}
    tags_low = {"width": 640, "height": 480}
    
    score_high = ffprobe_quality_score(tags_high)
    score_low = ffprobe_quality_score(tags_low)
    
    print(f"  High Quality Score: {score_high}")
    print(f"  Low Quality Score: {score_low}")
    
    if score_high > score_low:
        print("  [PASS] Scaling works.")
    else:
        print("  [FAIL] Score scaling is inverted.")
        success = False
        
    if not success:
        sys.exit(1)
    print("\n[SUCCESS] Routing logic units passed.")

if __name__ == "__main__":
    test_routing_logic()
