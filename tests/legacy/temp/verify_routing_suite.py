
import sys
import os
from pathlib import Path

# Add project root to path
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR

from src.parsers.format_utils import ffprobe_suite, ffprobe_quality_score, is_direct_play_capable
# We can't easily import from main.py because it starts a server usually
# But we can test the logic in format_utils.py which is the core.

def test_ffprobe_suite():
    print("Testing ffprobe_suite...")
    # Find a sample file in the media directory if possible
    media_dir = PROJECT_ROOT / "media"
    samples = list(media_dir.glob("*.mp4")) + list(media_dir.glob("*.mkv"))
    
    if not samples:
        print("No sample media files found in /media/. Skipping deep test.")
        return
        
    sample = samples[0]
    print(f"Analyzing: {sample}")
    res = ffprobe_suite(sample)
    print(f"Result: {res}")
    
    score = ffprobe_quality_score(res)
    print(f"Quality Score: {score}")
    
    direct = is_direct_play_capable(sample, "browser")
    print(f"Direct Play Capable (Browser): {direct}")

if __name__ == "__main__":
    test_ffprobe_suite()
