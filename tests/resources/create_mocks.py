#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def create_mocks():
    media_dir = Path("media")
    media_dir.mkdir(exist_ok=True)
    
    # Subdirectories
    (media_dir / "Bilder").mkdir(exist_ok=True)
    (media_dir / "Videos").mkdir(exist_ok=True)
    (media_dir / "Music").mkdir(exist_ok=True)
    (media_dir / "Series" / "Staffel_1").mkdir(parents=True, exist_ok=True)

    try:
        from PIL import Image, ImageDraw
        print("PIL found, creating real mock images...")
        
        def create_img(p, text, color):
            img = Image.new('RGB', (400, 400), color=color)
            d = ImageDraw.Draw(img)
            d.text((10, 10), text, fill=(255, 255, 255))
            img.save(p)

        create_img(media_dir / "Bilder" / "test1.jpg", "JPG Test", (200, 0, 0))
        create_img(media_dir / "Bilder" / "test2.png", "PNG Test", (0, 200, 0))
        create_img(media_dir / "Bilder" / "test3.bmp", "BMP Test", (0, 0, 200))
        
    except ImportError:
        print("PIL missing, creating empty files for images as fallback...")
        for ext in ['jpg', 'png', 'bmp']:
            (media_dir / "Bilder" / f"empty.{ext}").touch()

    # MKV & Video mocks
    for name in ["film.mkv", "clip.mp4", "movie.avi"]:
        (media_dir / "Videos" / name).touch()
    
    # Series
    (media_dir / "Series" / "Staffel_1" / "S01E01.mkv").touch()
    
    # Other formats
    (media_dir / "archives").mkdir(exist_ok=True)
    for ext in ["zip", "7z", "tar.gz"]:
        (media_dir / "archives" / f"backup.{ext}").touch()
    
    (media_dir / "disks").mkdir(exist_ok=True)
    for ext in ["iso", "img", "bin"]:
        (media_dir / "disks" / f"game_disk.{ext}").touch()

    print("Mocks created in 'media/' directory.")

if __name__ == "__main__":
    create_mocks()
