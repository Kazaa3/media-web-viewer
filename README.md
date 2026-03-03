# GUI Media Web Viewer

A custom media player with an embedded web-based GUI. It is built using Python, Eel, and the Bottle web framework. It supports parsing a wide range of audio formats including MP3, M4A, M4B, ALAC, FLAC, OGG, and WAV.

## Features

- **Web-based GUI:** Powered by [Eel](https://github.com/python-eel/Eel), bringing modern HTML/JS/CSS to a desktop app interface.
- **Micro Backend Server:** Uses the [Bottle](https://bottlepy.org/) WSGI micro web-framework to serve media and cover art seamlessly to the frontend.
- **Smart Metadata Extraction:** Uses multiple parser modules (`pymediainfo`, `mutagen`, and `ffmpeg` fallback) to comprehensively read audio tags (title, artist, album, bit depth, codec, sampling rate).
- **On-the-Fly Transcoding:** Automatically transcodes formats with poor browser compatibility like Apple Lossless (`ALAC`) to `FLAC` in the background utilizing lightweight `ffmpeg` caching, ensuring smooth immediate playback on the frontend.
- **Embedded Cover Art:** Identifies and displays embedded cover images inside MP4/M4A/MP3/FLAC items directly natively in the app.

## Requirements

- `Python 3.11+`
- `eel`
- `bottle`
- `mutagen`
- `pymediainfo`
- A working installation of `ffmpeg` in your PATH.

## Installation / Run

```bash
# Optional: Setup virtual environment
# python -m venv .venv
# source .venv/bin/activate

# Install required python packages
pip install eel bottle mutagen pymediainfo

# Run the media viewer
python main.py
```

## Structure

- `/main.py`: Bootstraps the Eel application and defines the MediaItem models.
- `/web/`: Contains the Bottle server (`app_bottle.py`) and UI markup (`app.html`).
- `/parsers/`: Dedicated sub-modules handling different forms of metadata tag extraction.
- `/tests/`: General test scripts to debug extraction logic.
- `/media/`: Default folder for placing music to scan.
