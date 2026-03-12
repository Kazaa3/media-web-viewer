import os
from pathlib import Path

def create_mock_dvd(target_dir):
    target_path = Path(target_dir).resolve()
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Create a dummy .iso file (just an empty file for detection)
    iso_file = target_path / "mock_movie.iso"
    iso_file.touch()
    print(f"Created mock ISO: {iso_file}")
    
    # 2. Create a DVD folder structure
    dvd_folder = target_path / "DVD_FOLDER_TEST"
    video_ts = dvd_folder / "VIDEO_TS"
    video_ts.mkdir(parents=True, exist_ok=True)
    (video_ts / "VIDEO_TS.IFO").touch()
    (video_ts / "VTS_01_0.IFO").touch()
    (video_ts / "VTS_01_1.VOB").touch()
    print(f"Created mock DVD folder: {dvd_folder}")

if __name__ == "__main__":
    media_dir = Path(__file__).resolve().parent.parent / "media"
    create_mock_dvd(media_dir)
