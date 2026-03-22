# Logbuch: Ordner Scraper & Indexierer – Vollautomatisch für ALLE Formate

## Datum: 10. März 2026

---

## Features
- ✅ Rekursiv: /music/subfolders
- ✅ Alle Formate: Audio/PDF/EPUB/DOCX/ODT/RTF/CBZ
- ✅ SQLite: schnelle SQL-Suche
- ✅ ChromaDB: semantische RAG-Suche
- ✅ Eel-GUI: dein Style

---

## Installation
```bash
pip install plibflac pymupdf odfpy striprtf rarfile mutagen librosa chromadb sentence-transformers
```

---

## Master-Skript (scraper.py)
- Initialisiert SQLite und ChromaDB
- Scannt Ordner rekursiv
- Extrahiert Metadaten/Features für alle Formate
- Speichert alles in DBs
- Eel-API für GUI/Frontend

---

## Hauptfunktionen
### scrape_folder(folder_path)
- Findet alle relevanten Dateien
- Verarbeitet jede Datei mit process_file()
- Speichert Metadaten/Features in SQLite
- Embeddings/Text in ChromaDB
- Rückgabe: Anzahl Dateien, Formate, Index-Status

### process_file(filepath)
- Format-Handler für Audio, PDF, EPUB, DOCX, ODT, RTF, CBZ, CBR
- Extrahiert Titel, Artist, Dauer/Seiten, Features (z.B. MFCC für Audio)
- Fehlerhandling für unbekannte Formate

### search_library(query)
- SQL-Suche in SQLite
- Semantische Suche in ChromaDB (RAG)
- Kombinierte Ergebnisse für GUI

---

## JS-Frontend (index.html)
- Ordner-Eingabe, SCRAPE-Button
- Suchfeld, Ergebnisse als JSON
- Eel-API für Backend-Kommunikation

---

## Output
- library_index.db: SQL-Index
- rag_db/: ChromaDB Embeddings
- GUI: Vollständige Library-Suche

---

## Use-Cases
- Musik/Docs/Comics/EPUBs indexieren
- Batch-Scan für große Libraries
- SQL- und RAG-Suche parallel
- Erweiterbar für neue Formate

---

## Eel/Bottle Teststrategie: Playwright & pytest

### 1. Playwright für Eel/Bottle-Server
- Playwright installiert Browser automatisch (Chrome, Firefox, Webkit).
- Stabiler als Selenium für UI-Tests.
- Ideal für Eel/NiceGUI-ähnliche Apps.

**Setup:**
```bash
pip install pytest playwright
playwright install  # Installiert Browser
```

**Bottle-Server starten (z.B. Port 8000):**
```python
import eel

eel.init('web')
eel.start('index.html', port=8000)
```

**Playwright-Test (pytest):**
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.asyncio
async def test_eel_ui(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Media Web Viewer"
    # UI-Elemente prüfen
    assert page.query_selector("#thumb")
```

### 2. Async UI-Checks mit pytest
- pytest.mark.asyncio für asynchrone Tests
- Kombinierbar mit Playwright für moderne UI

**Weitere Checks:**
- Button-Klicks, Cover-Upload, Thumbnail-Update
- Screenshot/Visual Regression

### 3. Hinweise
- Playwright ist stabiler und schneller als Selenium
- Browser werden automatisch installiert
- Für Eel/NiceGUI/Bottle-Apps optimal

**Empfohlene Struktur:**
- tests/test_ui_playwright.py
- pytest für alle UI/Integrationstests

---

## OpenCV (cv2) – Image Processing Power-Tool für Media-Library

### Installation
```bash
pip install opencv-python opencv-contrib-python  # + headless: opencv-python-headless
```

### 1. Image Binning mit cv2 (blitzschnell!)
```python
import cv2
import numpy as np
from pathlib import Path
import eel

@eel.expose
def cv2_bin_image(image_path: str, bin_size: int = 4):
    """2x2/4x4 Binning mit OpenCV (blitzschnell!)"""
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_h, new_w = h // bin_size, w // bin_size
    binned = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    thumb_path = f"thumbs/{Path(image_path).stem}_cv2.jpg"
    Path('thumbs').mkdir(exist_ok=True)
    cv2.imwrite(thumb_path, binned, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return {
        'success': True,
        'orig_size': [w, h],
        'binned_size': [new_w, new_h],
        'thumb': thumb_path
    }
```

### 2. Cover-Art Features (Histogram + ORB)
```python
@eel.expose
def cv2_image_features(image_path: str):
    """Histogram + ORB Features für Cover-Matching"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_norm = cv2.normalize(hist, hist).flatten()
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return {
        'success': True,
        'histogram': hist_norm.tolist()[:50],
        'keypoints': len(kp) if kp else 0,
        'features': des.tolist()[:10] if des is not None else []
    }
```

### 3. QR/Barcode Scanner (Album-Art)
```python
@eel.expose
def scan_cover_qr(image_path: str):
    """Finde QR-Codes/Links in Cover-Art"""
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return {'success': True, 'qr_data': data, 'bbox': bbox.tolist()}
    return {'success': False, 'message': 'Kein QR-Code gefunden'}
```

### 4. Vollständiger Image Handler (Scraper-Integration)
```python
def process_image_cv2(filepath: str):
    """cv2 für Media-Library Scraper"""
    path = Path(filepath)
    features = cv2_image_features(filepath)
    thumb = cv2_bin_image(filepath)
    img_pil = Image.open(filepath)
    exif = dict(img_pil._getexif() or {})
    return {
        'success': True, 'format': 'IMAGE',
        'text': f"Cover: {path.stem} ({features['keypoints']} Features)",
        'title': exif.get(0x010E, path.stem),
        'features': {
            'hist': features['histogram'],
            'thumb': thumb['thumb'],
            'size': thumb['orig_size']
        }
    }
```

### 5. Batch Cover Processing (Ordner)
```python
@eel.expose
def process_covers_folder(folder: str):
    """Alle JPG/PNG → Thumbs + Features"""
    images = glob.glob(folder + "/*.{jpg,jpeg,png}", recursive=True)
    results = []
    for img in images[:100]:
        result = process_image_cv2(img)
        results.append(result)
    return json.dumps(results)
```

### 6. Cover Similarity Suche
```python
def cover_similarity(img1_path: str, img2_path: str):
    """Vergleiche 2 Covers (Histogram + ORB)"""
    feat1 = cv2_image_features(img1_path)
    feat2 = cv2_image_features(img2_path)
    hist_sim = cv2.compareHist(
        np.array(feat1['histogram']),
        np.array(feat2['histogram']),
        cv2.HISTCMP_CORREL
    )
    return {'similarity': float(hist_sim), 'match': hist_sim > 0.8}
```

### cv2 vs. Pillow (für deine Library)
| Feature     | cv2      | Pillow   |
|-------------|----------|----------|
| Binning     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Features    | ⭐⭐⭐⭐⭐   | ❌      |
| QR/Barcode  | ⭐⭐⭐⭐⭐   | ❌      |
| Speed       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Batch       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |

### JS Frontend Beispiel
```javascript
async function processCover(file) {
    const features = await eel.cv2_image_features(file.path)();
    const thumb = await eel.cv2_bin_image(file.path, 4)();
    document.getElementById('thumb').src = thumb.thumb;
    console.log('Features:', features.histogram);
}
```

**cv2 = Media-Library Power-Tool! Cover-Matching + QR-Scanning für automatische Tagging.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Complete Multimedia Tools 2026 – Install-Ready

### Audio
- mutagen: Metadata/Tags/Cover (FLAC/MP3/M4A)
- pydub: Audio cut/merge/convert
- tinytag: Fast metadata
- pyacoustid: Audio fingerprint
- aubio: Beat/Onset detection

### Video
- moviepy: Edit/thumbnails/clips
- ffmpeg-python: Convert/extract/subs
- pymediainfo: Metadata (MKV/MP4)
- pymkv2: MKV chapters/tags
- OpenCV: Computer vision

### Container
- pymkv: MKV mux/split
- pyhandbrake: HandBrake encoding
- towebm: WebM/VP9 convert

### Subs
- pysrt: SRT parsing
- subtitle-edit: CLI subs
- pysubs2: Multi-format subs

### Codecs
- parallelencode: H264/H265 batch
- nvenc: NVIDIA hardware encoding

### Player
- python-vlc: Playback/metadata
- mpv: mpv Python bindings

### OCR/Scanner
- easyocr: Text recognition
- pyzbar: Barcode/ISBN
- pytesseract: Tesseract OCR

---

### 1-Klick Mega-Install (Python & System)
```bash
pip install mutagen pydub tinytag pyacoustid aubio moviepy ffmpeg-python pymediainfo pymkv2 opencv-python pysrt pysubs2 pyhandbrake towebm parallelencode python-vlc easyocr pyzbar pytesseract
sudo apt install mkvtoolnix handbrake vlc tesseract-ocr tesseract-ocr-deu
```

**NIX fehlt mehr – alles für Subs, MPEG, MP4, Container, Codecs, VLC, OCR, Player, Scanner, Batch!**

---

## ImgBurn auf Linux – Beste Alternativen & Python-Integration

### 1. TOP Linux-Alternativen (GUI)
| Tool      | Features                | Installation                | Beste für         |
|-----------|-------------------------|-----------------------------|-------------------|
| K3b       | CD/DVD/BluRay, ISO, Audio, Verify | sudo apt install k3b      | Alles (ImgBurn-Äquivalent) |
| Brasero   | Einfach, Data/Audio CD  | sudo apt install brasero    | Anfänger          |
| Xfburn    | Leicht, Data CD         | sudo apt install xfburn     | Minimal           |
| Graveman  | Data/Audio/ISO          | sudo apt install graveman   | Fortgeschritten   |

### 2. CLI Tools (Python-freundlich)
```bash
sudo apt install cdrdao growisofs genisoimage dvd+rw-tools
```

#### ISO erstellen & brennen
```python
import subprocess
import os

def create_iso(folder: str, iso_name: str):
    """Ordner → ISO (genisoimage)"""
    cmd = [
        'genisoimage',
        '-o', iso_name,
        '-J', '-R',  # Joliet + RockRidge
        '-V', 'Media_Library',
        folder
    ]
    subprocess.run(cmd, check=True)
    return iso_name

def burn_iso(device: str, iso_path: str, speed='4x'):
    """ISO → CD/DVD/BluRay"""
    cmd = [
        'growisofs',
        '-speed=' + speed,
        '-dvd-compat',
        f'-Z {device}={iso_path}'
    ]
    subprocess.run(cmd, check=True)
    return True

# Verwendung
iso = create_iso('/music/album', 'album.iso')
burn_iso('/dev/sr0', iso, '8x')  # /dev/sr0 = DVD-Brenner
```

#### Audio CD brennen
```python
def burn_audio_cd(device: str, wav_folder: str):
    """WAVs → Audio CD"""
    cmd = [
        'cdrdao', 'write', '--device', device,
        '--speed', '8x',
        'toc_file.cue'  # CUE-Sheet generieren
    ]
    subprocess.run(cmd, check=True)
```

### 3. Vollständige Python-Klasse (Eel-Integration)
```python
class LinuxBurner:
    def __init__(self, device='/dev/sr0'):
        self.device = device
    def list_drives(self):
        """Finde alle Brenner"""
        result = subprocess.run(['wodim', '--devices'], capture_output=True, text=True)
        return result.stdout
    def burn_data_iso(self, folder: str, label='Media'):
        """Ordner → Data-DVD"""
        iso = f'/tmp/{label}.iso'
        create_iso(folder, iso)
        burn_iso(self.device, iso, '4x')
        os.remove(iso)
        return True
    def burn_audio(self, wav_files: list):
        """Audio CD"""
        cue_content = f"""
FILE "{wav_files[0]}" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
"""
        with open('/tmp/audio.cue', 'w') as f:
            f.write(cue_content)
        subprocess.run(['cdrdao', 'write', f'--device {self.device}', '/tmp/audio.cue'])

burner = LinuxBurner()

@eel.expose
def burn_folder(folder: str):
    return burner.burn_data_iso(folder)

@eel.expose
def list_burners():
    return burner.list_drives()
```

### 4. K3b automatisieren (GUI-Tool)
```python
subprocess.run(['k3b', '--burn', 'data.iso'])  # Nicht perfekt
```

### 5. JS Frontend (Eel)
```javascript
async function burnData() {
    const folder = '/music/album';
    const result = await eel.burn_folder(folder)();
    alert(result ? '✅ Burned!' : '❌ Error');
}

async function listDrives() {
    const drives = await eel.list_burners()();
    console.log('Brenner:', drives);
}
```

### 6. Vollständige Workflow
1. scrape_folder() → Metadaten extrahieren
2. create_iso(library_export/) → ISO generieren
3. burn_iso(/dev/sr0, library.iso) → Brennen
4. validate_burn() → Prüfen

### Beste Setup (MX Linux)
```bash
sudo apt update
sudo apt install k3b cdrdao growisofs genisoimage dvd+rw-tools
wodim --devices  # Zeigt /dev/sr0 etc.
python burner.py
```

**K3b = Linux-ImgBurn (GUI)! growisofs = CLI-Power. Zero-Konfiguration brennen!**

---

## CONTAINER PROCESSING – MKV Mux + HandBrake + WebM

**Perfekte Ergänzung für deine Media-Library!**
- **pymkv** (MKV Mux/Split)
- **pyhandbrake** (Video Encoding)
- **towebm** (WebM/VP9 Streaming)

### 1. Installation
```bash
sudo apt install mkvtoolnix handbrake-cli ffmpeg
pip install pymkv pyhandbrake  # towebm ist Script (siehe unten)
```

### 2. pymkv – MKV Mux/Split (Chapters/Tags)
```python
from pymkv import MKVFile, MKVTrack
import eel

@eel.expose
def mux_mkv(video: str, audio: str, subs: str = None, output: str = "output.mkv"):
    """Video + Audio + Subs → MKV"""
    mkv = MKVFile()
    mkv.add_track(video, track_id=0, track_type='video')
    mkv.add_track(audio, track_id=1, track_type='audio')
    if subs:
        mkv.add_track(subs, track_id=2, track_type='subtitle')
    mkv.chapters = [
        {"start_time": "00:00:00", "end_time": "00:05:00", "name": "Intro"},
        {"start_time": "00:05:00", "name": "Main"}
    ]
    mkv.mux(output)
    return {'success': True, 'output': output}

@eel.expose
def split_mkv(input_mkv: str, chapters: list):
    """MKV splitten (Chapters)"""
    mkv = MKVFile(input_mkv)
    for i, chap in enumerate(chapters):
        mkv.split(f"part_{i}.mkv", chapters=[chap])
    return {'success': True}
```

### 3. pyhandbrake – Video Encoding
```python
from handbrake import HandBrake
import eel

@eel.expose
def encode_video(input_file: str, output_file: str, preset='Fast 1080p30'):
    """HandBrake Encoding mit Progress"""
    def progress(p):
        print(f"Encoding: {p.task_description} {int(p.percent)}%")
    hb = HandBrake()
    hb.rip_title(input_file, output_file, preset, progress_handler=progress)
    return {'success': True, 'output': output_file}

@eel.expose
def list_presets():
    hb = HandBrake()
    return hb.list_presets()
```

### 4. towebm – WebM/VP9 Converter (Streaming)
**towebm.py** ist ein Single-File Script (kein pip):
```bash
wget https://github.com/Kagami/webm.py/raw/master/towebm.py
chmod +x towebm.py
```

```python
import subprocess
import eel

@eel.expose
def to_webm(input_video: str, output_webm: str, crf=30):
    """MP4/AVI → WebM (VP9/Opus)"""
    cmd = [
        'python3', 'towebm.py',
        input_video, '-o', output_webm,
        '--crf', str(crf),
        '--audio-bitrate', '128k'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'error': result.stderr
    }
```

### 5. Vollständige Container Pipeline (Eel)
```python
@eel.expose
def media_pipeline(input_folder: str, output_folder: str):
    """1. Encode → 2. Mux → 3. WebM"""
    videos = glob.glob(input_folder + "/*.{mp4,avi,mkv}", recursive=True)
    for video in videos:
        encoded = video.replace('.mp4', '_h265.mp4')
        encode_video(video, encoded, 'H.265 MKV 1080p30')
    for enc in glob.glob(output_folder + "/*_h265.*"):
        audio = enc.replace('h265.mp4', 'audio.aac')
        subs = enc.replace('h265.mp4', 'subs.srt')
        mkv_out = enc.replace('.mp4', '.mkv')
        mux_mkv(enc, audio, subs, mkv_out)
    for mkv in glob.glob(output_folder + "/*.mkv"):
        webm = mkv.replace('.mkv', '.webm')
        to_webm(mkv, webm)
    return {'success': True, 'webm_count': len(glob.glob('*.webm'))}
```

### 6. JS Frontend
```javascript
async function processMedia() {
    const input = '/raw_videos';
    const output = '/processed';
    const result = await eel.media_pipeline(input, output)();
    console.log('✅', result.webm_count, 'WebM erstellt');
}
```

### Features
```
✅ MKV Mux (Video+Audio+Subs+Chapters)
✅ H.265 Encoding (HandBrake)
✅ WebM/VP9 (Web-Streaming)
✅ Batch-Processing
✅ Progress-Tracking
```

**Deine Library → Streaming-ready (WebM + MKV)! CRF 20-30 = YouTube-Qualität. Preset: Fast 1080p30 oder H.265 MKV HQ.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## SUBTITLES PROCESSING – SRT/ASS/VTT + CLI Tools

**pysrt**, **pysubs2** + **Subtitle Edit CLI** – vollständige Subtitle-Pipeline für MKV-Muxing/Media-Library!

### 1. Installation
```bash
pip install pysrt pysubs2 srt
sudo apt install subtitleeditor  # GUI (optional)
```

### 2. pysrt – SRT Parsing/Editing
```python
import pysrt
import eel

@eel.expose
def process_srt(srt_path: str):
    """SRT laden → bearbeiten → speichern"""
    subs = pysrt.open(srt_path)
    subs.shift(seconds=2)
    for sub in subs:
        sub.text = sub.text.upper()
    mid_subs = subs.slice(starts_after={'minutes': 10}, ends_before={'minutes': 20})
    output = srt_path.replace('.srt', '_edited.srt')
    mid_subs.save(output, encoding='utf-8')
    return {
        'success': True,
        'subs_count': len(subs),
        'edited': len(mid_subs),
        'output': output
    }
```

### 3. pysubs2 – Multi-Format (SRT/ASS/VTT/SMI)
```python
import pysubs2
import eel

@eel.expose
def subs_universal(input_path: str, output_format='srt'):
    """Beliebige Subs → SRT/ASS"""
    subs = pysubs2.load(input_path, encoding='utf-8')
    subs.shift(s=1.5)
    for line in subs:
        line.custom_style = '{\\fs24\\b1\\c&H00FF00&}'
    output = input_path.rsplit('.', 1)[0] + f'_{output_format}.{output_format}'
    subs.save(output)
    return {
        'success': True,
        'input_format': pysubs2.format_from_filename(input_path),
        'output': output
    }
```

### 4. Subtitle Edit CLI (via Python)
```python
import subprocess
import eel

@eel.expose
def subtitle_edit_cli(input_subs: str, output_subs: str, action='fix'):
    """Subtitle Edit Kommandozeile"""
    cmd = [
        'SubtitleEditCLI',
        input_subs,
        '--fixCommonErrors',
        '--autoAnimateCommonErrors',
        '--setMinDisplayTimeBetweenSE:2000',
        '--outputFormat:srt',
        '--outputFile:' + output_subs
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'errors': result.stderr
    }
```

### 5. Vollständige Subtitle Pipeline (MKV-Integration)
```python
@eel.expose
def subs_pipeline(video: str, subs_folder: str):
    """1. SRT fixen → 2. Timing sync → 3. MKV muxen"""
    srts = glob.glob(subs_folder + "/*.srt")
    fixed_srts = []
    for srt in srts:
        fixed = process_srt(srt)
        fixed_srts.append(fixed['output'])
    best_srt = next((s for s in fixed_srts if Path(video).stem in Path(s).stem), fixed_srts[0])
    mkv_out = video.replace('.mp4', '.mkv')
    mux_mkv(video, best_srt, mkv_out)
    return {'success': True, 'mkv': mkv_out, 'subs_used': best_srt}
```

### 6. Batch CLI (pysubs2)
```bash
pysubs2 --shift 0.5s --to srt *.srt *.ass
pysubs2 input.srt --translate de --to output.srt
```

### 7. JS Frontend
```javascript
async function fixSubs(file) {
    const result = await eel.process_srt(file.path)();
    console.log('✅ Fixed:', result.output);
    await eel.subs_pipeline('video.mp4', '/subs');
}
```

### Features
```
✅ SRT/ASS/VTT/SMI parsing
✅ Timing shift/sync
✅ Text bearbeiten (Übersetzen/Style)
✅ Batch-Processing
✅ MKV-Muxing Integration
✅ CLI + GUI
```

**Subtitle Edit CLI = automatische Fixes (Lücken, Kurz-Subs). pysubs2 = Multi-Format Power!**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Unterstützte Formate – Media-Library 2026

### Audio
- FLAC, MP3, M4A, AAC, WAV, OGG, OPUS, WMA

### Video
- MP4, MKV, AVI, MOV, WEBM, MPEG, FLV, WMV, 3GP

### Container
- MKV, MP4, AVI, MOV, WEBM, FLV, MPEG

### Subs
- SRT, ASS, VTT, SUB, SMI, SSA

### Dokumente
- PDF, EPUB, DOCX, ODT, RTF, CBZ, CBR, TXT

### Bilder
- JPG, PNG, BMP, GIF, TIFF, WEBP, FITS

### Scanner/OCR
- Barcode, QR-Code, ISBN, Text (OCR)

### Sonstige
- ChromaDB Embeddings, SQLite DB, Audio Fingerprint (AcoustID)

---

**Alle Formate sind batch- und GUI-fähig, können indexiert, konvertiert und gemuxed werden.**

---

## Eel/Bottle Teststrategie: Playwright & pytest

### 1. Playwright für Eel/Bottle-Server
- Playwright installiert Browser automatisch (Chrome, Firefox, Webkit).
- Stabiler als Selenium für UI-Tests.
- Ideal für Eel/NiceGUI-ähnliche Apps.

**Setup:**
```bash
pip install pytest playwright
playwright install  # Installiert Browser
```

**Bottle-Server starten (z.B. Port 8000):**
```python
import eel

eel.init('web')
eel.start('index.html', port=8000)
```

**Playwright-Test (pytest):**
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.asyncio
async def test_eel_ui(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Media Web Viewer"
    # UI-Elemente prüfen
    assert page.query_selector("#thumb")
```

### 2. Async UI-Checks mit pytest
- pytest.mark.asyncio für asynchrone Tests
- Kombinierbar mit Playwright für moderne UI

**Weitere Checks:**
- Button-Klicks, Cover-Upload, Thumbnail-Update
- Screenshot/Visual Regression

### 3. Hinweise
- Playwright ist stabiler und schneller als Selenium
- Browser werden automatisch installiert
- Für Eel/NiceGUI/Bottle-Apps optimal

**Empfohlene Struktur:**
- tests/test_ui_playwright.py
- pytest für alle UI/Integrationstests

---

## OpenCV (cv2) – Image Processing Power-Tool für Media-Library

### Installation
```bash
pip install opencv-python opencv-contrib-python  # + headless: opencv-python-headless
```

### 1. Image Binning mit cv2 (blitzschnell!)
```python
import cv2
import numpy as np
from pathlib import Path
import eel

@eel.expose
def cv2_bin_image(image_path: str, bin_size: int = 4):
    """2x2/4x4 Binning mit OpenCV (blitzschnell!)"""
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_h, new_w = h // bin_size, w // bin_size
    binned = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    thumb_path = f"thumbs/{Path(image_path).stem}_cv2.jpg"
    Path('thumbs').mkdir(exist_ok=True)
    cv2.imwrite(thumb_path, binned, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return {
        'success': True,
        'orig_size': [w, h],
        'binned_size': [new_w, new_h],
        'thumb': thumb_path
    }
```

### 2. Cover-Art Features (Histogram + ORB)
```python
@eel.expose
def cv2_image_features(image_path: str):
    """Histogram + ORB Features für Cover-Matching"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_norm = cv2.normalize(hist, hist).flatten()
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return {
        'success': True,
        'histogram': hist_norm.tolist()[:50],
        'keypoints': len(kp) if kp else 0,
        'features': des.tolist()[:10] if des is not None else []
    }
```

### 3. QR/Barcode Scanner (Album-Art)
```python
@eel.expose
def scan_cover_qr(image_path: str):
    """Finde QR-Codes/Links in Cover-Art"""
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return {'success': True, 'qr_data': data, 'bbox': bbox.tolist()}
    return {'success': False, 'message': 'Kein QR-Code gefunden'}
```

### 4. Vollständiger Image Handler (Scraper-Integration)
```python
def process_image_cv2(filepath: str):
    """cv2 für Media-Library Scraper"""
    path = Path(filepath)
    features = cv2_image_features(filepath)
    thumb = cv2_bin_image(filepath)
    img_pil = Image.open(filepath)
    exif = dict(img_pil._getexif() or {})
    return {
        'success': True, 'format': 'IMAGE',
        'text': f"Cover: {path.stem} ({features['keypoints']} Features)",
        'title': exif.get(0x010E, path.stem),
        'features': {
            'hist': features['histogram'],
            'thumb': thumb['thumb'],
            'size': thumb['orig_size']
        }
    }
```

### 5. Batch Cover Processing (Ordner)
```python
@eel.expose
def process_covers_folder(folder: str):
    """Alle JPG/PNG → Thumbs + Features"""
    images = glob.glob(folder + "/*.{jpg,jpeg,png}", recursive=True)
    results = []
    for img in images[:100]:
        result = process_image_cv2(img)
        results.append(result)
    return json.dumps(results)
```

### 6. Cover Similarity Suche
```python
def cover_similarity(img1_path: str, img2_path: str):
    """Vergleiche 2 Covers (Histogram + ORB)"""
    feat1 = cv2_image_features(img1_path)
    feat2 = cv2_image_features(img2_path)
    hist_sim = cv2.compareHist(
        np.array(feat1['histogram']),
        np.array(feat2['histogram']),
        cv2.HISTCMP_CORREL
    )
    return {'similarity': float(hist_sim), 'match': hist_sim > 0.8}
```

### cv2 vs. Pillow (für deine Library)
| Feature     | cv2      | Pillow   |
|-------------|----------|----------|
| Binning     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Features    | ⭐⭐⭐⭐⭐   | ❌      |
| QR/Barcode  | ⭐⭐⭐⭐⭐   | ❌      |
| Speed       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Batch       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |

### JS Frontend Beispiel
```javascript
async function processCover(file) {
    const features = await eel.cv2_image_features(file.path)();
    const thumb = await eel.cv2_bin_image(file.path, 4)();
    document.getElementById('thumb').src = thumb.thumb;
    console.log('Features:', features.histogram);
}
```

**cv2 = Media-Library Power-Tool! Cover-Matching + QR-Scanning für automatische Tagging.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Complete Multimedia Tools 2026 – Install-Ready

### Audio
- mutagen: Metadata/Tags/Cover (FLAC/MP3/M4A)
- pydub: Audio cut/merge/convert
- tinytag: Fast metadata
- pyacoustid: Audio fingerprint
- aubio: Beat/Onset detection

### Video
- moviepy: Edit/thumbnails/clips
- ffmpeg-python: Convert/extract/subs
- pymediainfo: Metadata (MKV/MP4)
- pymkv2: MKV chapters/tags
- OpenCV: Computer vision

### Container
- pymkv: MKV mux/split
- pyhandbrake: HandBrake encoding
- towebm: WebM/VP9 convert

### Subs
- pysrt: SRT parsing
- subtitle-edit: CLI subs
- pysubs2: Multi-format subs

### Codecs
- parallelencode: H264/H265 batch
- nvenc: NVIDIA hardware encoding

### Player
- python-vlc: Playback/metadata
- mpv: mpv Python bindings

### OCR/Scanner
- easyocr: Text recognition
- pyzbar: Barcode/ISBN
- pytesseract: Tesseract OCR

---

### 1-Klick Mega-Install (Python & System)
```bash
pip install mutagen pydub tinytag pyacoustid aubio moviepy ffmpeg-python pymediainfo pymkv2 opencv-python pysrt pysubs2 pyhandbrake towebm parallelencode python-vlc easyocr pyzbar pytesseract
sudo apt install mkvtoolnix handbrake vlc tesseract-ocr tesseract-ocr-deu
```

**NIX fehlt mehr – alles für Subs, MPEG, MP4, Container, Codecs, VLC, OCR, Player, Scanner, Batch!**

---

## ImgBurn auf Linux – Beste Alternativen & Python-Integration

### 1. TOP Linux-Alternativen (GUI)
| Tool      | Features                | Installation                | Beste für         |
|-----------|-------------------------|-----------------------------|-------------------|
| K3b       | CD/DVD/BluRay, ISO, Audio, Verify | sudo apt install k3b      | Alles (ImgBurn-Äquivalent) |
| Brasero   | Einfach, Data/Audio CD  | sudo apt install brasero    | Anfänger          |
| Xfburn    | Leicht, Data CD         | sudo apt install xfburn     | Minimal           |
| Graveman  | Data/Audio/ISO          | sudo apt install graveman   | Fortgeschritten   |

### 2. CLI Tools (Python-freundlich)
```bash
sudo apt install cdrdao growisofs genisoimage dvd+rw-tools
```

#### ISO erstellen & brennen
```python
import subprocess
import os

def create_iso(folder: str, iso_name: str):
    """Ordner → ISO (genisoimage)"""
    cmd = [
        'genisoimage',
        '-o', iso_name,
        '-J', '-R',  # Joliet + RockRidge
        '-V', 'Media_Library',
        folder
    ]
    subprocess.run(cmd, check=True)
    return iso_name

def burn_iso(device: str, iso_path: str, speed='4x'):
    """ISO → CD/DVD/BluRay"""
    cmd = [
        'growisofs',
        '-speed=' + speed,
        '-dvd-compat',
        f'-Z {device}={iso_path}'
    ]
    subprocess.run(cmd, check=True)
    return True

# Verwendung
iso = create_iso('/music/album', 'album.iso')
burn_iso('/dev/sr0', iso, '8x')  # /dev/sr0 = DVD-Brenner
```

#### Audio CD brennen
```python
def burn_audio_cd(device: str, wav_folder: str):
    """WAVs → Audio CD"""
    cmd = [
        'cdrdao', 'write', '--device', device,
        '--speed', '8x',
        'toc_file.cue'  # CUE-Sheet generieren
    ]
    subprocess.run(cmd, check=True)
```

### 3. Vollständige Python-Klasse (Eel-Integration)
```python
class LinuxBurner:
    def __init__(self, device='/dev/sr0'):
        self.device = device
    def list_drives(self):
        """Finde alle Brenner"""
        result = subprocess.run(['wodim', '--devices'], capture_output=True, text=True)
        return result.stdout
    def burn_data_iso(self, folder: str, label='Media'):
        """Ordner → Data-DVD"""
        iso = f'/tmp/{label}.iso'
        create_iso(folder, iso)
        burn_iso(self.device, iso, '4x')
        os.remove(iso)
        return True
    def burn_audio(self, wav_files: list):
        """Audio CD"""
        cue_content = f"""
FILE "{wav_files[0]}" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
"""
        with open('/tmp/audio.cue', 'w') as f:
            f.write(cue_content)
        subprocess.run(['cdrdao', 'write', f'--device {self.device}', '/tmp/audio.cue'])

burner = LinuxBurner()

@eel.expose
def burn_folder(folder: str):
    return burner.burn_data_iso(folder)

@eel.expose
def list_burners():
    return burner.list_drives()
```

### 4. K3b automatisieren (GUI-Tool)
```python
subprocess.run(['k3b', '--burn', 'data.iso'])  # Nicht perfekt
```

### 5. JS Frontend (Eel)
```javascript
async function burnData() {
    const folder = '/music/album';
    const result = await eel.burn_folder(folder)();
    alert(result ? '✅ Burned!' : '❌ Error');
}

async function listDrives() {
    const drives = await eel.list_burners()();
    console.log('Brenner:', drives);
}
```

### 6. Vollständige Workflow
1. scrape_folder() → Metadaten extrahieren
2. create_iso(library_export/) → ISO generieren
3. burn_iso(/dev/sr0, library.iso) → Brennen
4. validate_burn() → Prüfen

### Beste Setup (MX Linux)
```bash
sudo apt update
sudo apt install k3b cdrdao growisofs genisoimage dvd+rw-tools
wodim --devices  # Zeigt /dev/sr0 etc.
python burner.py
```

**K3b = Linux-ImgBurn (GUI)! growisofs = CLI-Power. Zero-Konfiguration brennen!**

---

## CONTAINER PROCESSING – MKV Mux + HandBrake + WebM

**Perfekte Ergänzung für deine Media-Library!**
- **pymkv** (MKV Mux/Split)
- **pyhandbrake** (Video Encoding)
- **towebm** (WebM/VP9 Streaming)

### 1. Installation
```bash
sudo apt install mkvtoolnix handbrake-cli ffmpeg
pip install pymkv pyhandbrake  # towebm ist Script (siehe unten)
```

### 2. pymkv – MKV Mux/Split (Chapters/Tags)
```python
from pymkv import MKVFile, MKVTrack
import eel

@eel.expose
def mux_mkv(video: str, audio: str, subs: str = None, output: str = "output.mkv"):
    """Video + Audio + Subs → MKV"""
    mkv = MKVFile()
    mkv.add_track(video, track_id=0, track_type='video')
    mkv.add_track(audio, track_id=1, track_type='audio')
    if subs:
        mkv.add_track(subs, track_id=2, track_type='subtitle')
    mkv.chapters = [
        {"start_time": "00:00:00", "end_time": "00:05:00", "name": "Intro"},
        {"start_time": "00:05:00", "name": "Main"}
    ]
    mkv.mux(output)
    return {'success': True, 'output': output}

@eel.expose
def split_mkv(input_mkv: str, chapters: list):
    """MKV splitten (Chapters)"""
    mkv = MKVFile(input_mkv)
    for i, chap in enumerate(chapters):
        mkv.split(f"part_{i}.mkv", chapters=[chap])
    return {'success': True}
```

### 3. pyhandbrake – Video Encoding
```python
from handbrake import HandBrake
import eel

@eel.expose
def encode_video(input_file: str, output_file: str, preset='Fast 1080p30'):
    """HandBrake Encoding mit Progress"""
    def progress(p):
        print(f"Encoding: {p.task_description} {int(p.percent)}%")
    hb = HandBrake()
    hb.rip_title(input_file, output_file, preset, progress_handler=progress)
    return {'success': True, 'output': output_file}

@eel.expose
def list_presets():
    hb = HandBrake()
    return hb.list_presets()
```

### 4. towebm – WebM/VP9 Converter (Streaming)
**towebm.py** ist ein Single-File Script (kein pip):
```bash
wget https://github.com/Kagami/webm.py/raw/master/towebm.py
chmod +x towebm.py
```

```python
import subprocess
import eel

@eel.expose
def to_webm(input_video: str, output_webm: str, crf=30):
    """MP4/AVI → WebM (VP9/Opus)"""
    cmd = [
        'python3', 'towebm.py',
        input_video, '-o', output_webm,
        '--crf', str(crf),
        '--audio-bitrate', '128k'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'error': result.stderr
    }
```

### 5. Vollständige Container Pipeline (Eel)
```python
@eel.expose
def media_pipeline(input_folder: str, output_folder: str):
    """1. Encode → 2. Mux → 3. WebM"""
    videos = glob.glob(input_folder + "/*.{mp4,avi,mkv}", recursive=True)
    for video in videos:
        encoded = video.replace('.mp4', '_h265.mp4')
        encode_video(video, encoded, 'H.265 MKV 1080p30')
    for enc in glob.glob(output_folder + "/*_h265.*"):
        audio = enc.replace('h265.mp4', 'audio.aac')
        subs = enc.replace('h265.mp4', 'subs.srt')
        mkv_out = enc.replace('.mp4', '.mkv')
        mux_mkv(enc, audio, subs, mkv_out)
    for mkv in glob.glob(output_folder + "/*.mkv"):
        webm = mkv.replace('.mkv', '.webm')
        to_webm(mkv, webm)
    return {'success': True, 'webm_count': len(glob.glob('*.webm'))}
```

### 6. JS Frontend
```javascript
async function processMedia() {
    const input = '/raw_videos';
    const output = '/processed';
    const result = await eel.media_pipeline(input, output)();
    console.log('✅', result.webm_count, 'WebM erstellt');
}
```

### Features
```
✅ MKV Mux (Video+Audio+Subs+Chapters)
✅ H.265 Encoding (HandBrake)
✅ WebM/VP9 (Web-Streaming)
✅ Batch-Processing
✅ Progress-Tracking
```

**Deine Library → Streaming-ready (WebM + MKV)! CRF 20-30 = YouTube-Qualität. Preset: Fast 1080p30 oder H.265 MKV HQ.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## SUBTITLES PROCESSING – SRT/ASS/VTT + CLI Tools

**pysrt**, **pysubs2** + **Subtitle Edit CLI** – vollständige Subtitle-Pipeline für MKV-Muxing/Media-Library!

### 1. Installation
```bash
pip install pysrt pysubs2 srt
sudo apt install subtitleeditor  # GUI (optional)
```

### 2. pysrt – SRT Parsing/Editing
```python
import pysrt
import eel

@eel.expose
def process_srt(srt_path: str):
    """SRT laden → bearbeiten → speichern"""
    subs = pysrt.open(srt_path)
    subs.shift(seconds=2)
    for sub in subs:
        sub.text = sub.text.upper()
    mid_subs = subs.slice(starts_after={'minutes': 10}, ends_before={'minutes': 20})
    output = srt_path.replace('.srt', '_edited.srt')
    mid_subs.save(output, encoding='utf-8')
    return {
        'success': True,
        'subs_count': len(subs),
        'edited': len(mid_subs),
        'output': output
    }
```

### 3. pysubs2 – Multi-Format (SRT/ASS/VTT/SMI)
```python
import pysubs2
import eel

@eel.expose
def subs_universal(input_path: str, output_format='srt'):
    """Beliebige Subs → SRT/ASS"""
    subs = pysubs2.load(input_path, encoding='utf-8')
    subs.shift(s=1.5)
    for line in subs:
        line.custom_style = '{\\fs24\\b1\\c&H00FF00&}'
    output = input_path.rsplit('.', 1)[0] + f'_{output_format}.{output_format}'
    subs.save(output)
    return {
        'success': True,
        'input_format': pysubs2.format_from_filename(input_path),
        'output': output
    }
```

### 4. Subtitle Edit CLI (via Python)
```python
import subprocess
import eel

@eel.expose
def subtitle_edit_cli(input_subs: str, output_subs: str, action='fix'):
    """Subtitle Edit Kommandozeile"""
    cmd = [
        'SubtitleEditCLI',
        input_subs,
        '--fixCommonErrors',
        '--autoAnimateCommonErrors',
        '--setMinDisplayTimeBetweenSE:2000',
        '--outputFormat:srt',
        '--outputFile:' + output_subs
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'errors': result.stderr
    }
```

### 5. Vollständige Subtitle Pipeline (MKV-Integration)
```python
@eel.expose
def subs_pipeline(video: str, subs_folder: str):
    """1. SRT fixen → 2. Timing sync → 3. MKV muxen"""
    srts = glob.glob(subs_folder + "/*.srt")
    fixed_srts = []
    for srt in srts:
        fixed = process_srt(srt)
        fixed_srts.append(fixed['output'])
    best_srt = next((s for s in fixed_srts if Path(video).stem in Path(s).stem), fixed_srts[0])
    mkv_out = video.replace('.mp4', '.mkv')
    mux_mkv(video, best_srt, mkv_out)
    return {'success': True, 'mkv': mkv_out, 'subs_used': best_srt}
```

### 6. Batch CLI (pysubs2)
```bash
pysubs2 --shift 0.5s --to srt *.srt *.ass
pysubs2 input.srt --translate de --to output.srt
```

### 7. JS Frontend
```javascript
async function fixSubs(file) {
    const result = await eel.process_srt(file.path)();
    console.log('✅ Fixed:', result.output);
    await eel.subs_pipeline('video.mp4', '/subs');
}
```

### Features
```
✅ SRT/ASS/VTT/SMI parsing
✅ Timing shift/sync
✅ Text bearbeiten (Übersetzen/Style)
✅ Batch-Processing
✅ MKV-Muxing Integration
✅ CLI + GUI
```

**Subtitle Edit CLI = automatische Fixes (Lücken, Kurz-Subs). pysubs2 = Multi-Format Power!**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Unterstützte Formate – Media-Library 2026

### Audio
- FLAC, MP3, M4A, AAC, WAV, OGG, OPUS, WMA

### Video
- MP4, MKV, AVI, MOV, WEBM, MPEG, FLV, WMV, 3GP

### Container
- MKV, MP4, AVI, MOV, WEBM, FLV, MPEG

### Subs
- SRT, ASS, VTT, SUB, SMI, SSA

### Dokumente
- PDF, EPUB, DOCX, ODT, RTF, CBZ, CBR, TXT

### Bilder
- JPG, PNG, BMP, GIF, TIFF, WEBP, FITS

### Scanner/OCR
- Barcode, QR-Code, ISBN, Text (OCR)

### Sonstige
- ChromaDB Embeddings, SQLite DB, Audio Fingerprint (AcoustID)

---

**Alle Formate sind batch- und GUI-fähig, können indexiert, konvertiert und gemuxed werden.**

---

## Eel/Bottle Teststrategie: Playwright & pytest

### 1. Playwright für Eel/Bottle-Server
- Playwright installiert Browser automatisch (Chrome, Firefox, Webkit).
- Stabiler als Selenium für UI-Tests.
- Ideal für Eel/NiceGUI-ähnliche Apps.

**Setup:**
```bash
pip install pytest playwright
playwright install  # Installiert Browser
```

**Bottle-Server starten (z.B. Port 8000):**
```python
import eel

eel.init('web')
eel.start('index.html', port=8000)
```

**Playwright-Test (pytest):**
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.asyncio
async def test_eel_ui(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Media Web Viewer"
    # UI-Elemente prüfen
    assert page.query_selector("#thumb")
```

### 2. Async UI-Checks mit pytest
- pytest.mark.asyncio für asynchrone Tests
- Kombinierbar mit Playwright für moderne UI

**Weitere Checks:**
- Button-Klicks, Cover-Upload, Thumbnail-Update
- Screenshot/Visual Regression

### 3. Hinweise
- Playwright ist stabiler und schneller als Selenium
- Browser werden automatisch installiert
- Für Eel/NiceGUI/Bottle-Apps optimal

**Empfohlene Struktur:**
- tests/test_ui_playwright.py
- pytest für alle UI/Integrationstests

---

## OpenCV (cv2) – Image Processing Power-Tool für Media-Library

### Installation
```bash
pip install opencv-python opencv-contrib-python  # + headless: opencv-python-headless
```

### 1. Image Binning mit cv2 (blitzschnell!)
```python
import cv2
import numpy as np
from pathlib import Path
import eel

@eel.expose
def cv2_bin_image(image_path: str, bin_size: int = 4):
    """2x2/4x4 Binning mit OpenCV (blitzschnell!)"""
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_h, new_w = h // bin_size, w // bin_size
    binned = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    thumb_path = f"thumbs/{Path(image_path).stem}_cv2.jpg"
    Path('thumbs').mkdir(exist_ok=True)
    cv2.imwrite(thumb_path, binned, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return {
        'success': True,
        'orig_size': [w, h],
        'binned_size': [new_w, new_h],
        'thumb': thumb_path
    }
```

### 2. Cover-Art Features (Histogram + ORB)
```python
@eel.expose
def cv2_image_features(image_path: str):
    """Histogram + ORB Features für Cover-Matching"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_norm = cv2.normalize(hist, hist).flatten()
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return {
        'success': True,
        'histogram': hist_norm.tolist()[:50],
        'keypoints': len(kp) if kp else 0,
        'features': des.tolist()[:10] if des is not None else []
    }
```

### 3. QR/Barcode Scanner (Album-Art)
```python
@eel.expose
def scan_cover_qr(image_path: str):
    """Finde QR-Codes/Links in Cover-Art"""
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return {'success': True, 'qr_data': data, 'bbox': bbox.tolist()}
    return {'success': False, 'message': 'Kein QR-Code gefunden'}
```

### 4. Vollständiger Image Handler (Scraper-Integration)
```python
def process_image_cv2(filepath: str):
    """cv2 für Media-Library Scraper"""
    path = Path(filepath)
    features = cv2_image_features(filepath)
    thumb = cv2_bin_image(filepath)
    img_pil = Image.open(filepath)
    exif = dict(img_pil._getexif() or {})
    return {
        'success': True, 'format': 'IMAGE',
        'text': f"Cover: {path.stem} ({features['keypoints']} Features)",
        'title': exif.get(0x010E, path.stem),
        'features': {
            'hist': features['histogram'],
            'thumb': thumb['thumb'],
            'size': thumb['orig_size']
        }
    }
```

### 5. Batch Cover Processing (Ordner)
```python
@eel.expose
def process_covers_folder(folder: str):
    """Alle JPG/PNG → Thumbs + Features"""
    images = glob.glob(folder + "/*.{jpg,jpeg,png}", recursive=True)
    results = []
    for img in images[:100]:
        result = process_image_cv2(img)
        results.append(result)
    return json.dumps(results)
```

### 6. Cover Similarity Suche
```python
def cover_similarity(img1_path: str, img2_path: str):
    """Vergleiche 2 Covers (Histogram + ORB)"""
    feat1 = cv2_image_features(img1_path)
    feat2 = cv2_image_features(img2_path)
    hist_sim = cv2.compareHist(
        np.array(feat1['histogram']),
        np.array(feat2['histogram']),
        cv2.HISTCMP_CORREL
    )
    return {'similarity': float(hist_sim), 'match': hist_sim > 0.8}
```

### cv2 vs. Pillow (für deine Library)
| Feature     | cv2      | Pillow   |
|-------------|----------|----------|
| Binning     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Features    | ⭐⭐⭐⭐⭐   | ❌      |
| QR/Barcode  | ⭐⭐⭐⭐⭐   | ❌      |
| Speed       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Batch       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |

### JS Frontend Beispiel
```javascript
async function processCover(file) {
    const features = await eel.cv2_image_features(file.path)();
    const thumb = await eel.cv2_bin_image(file.path, 4)();
    document.getElementById('thumb').src = thumb.thumb;
    console.log('Features:', features.histogram);
}
```

**cv2 = Media-Library Power-Tool! Cover-Matching + QR-Scanning für automatische Tagging.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Complete Multimedia Tools 2026 – Install-Ready

### Audio
- mutagen: Metadata/Tags/Cover (FLAC/MP3/M4A)
- pydub: Audio cut/merge/convert
- tinytag: Fast metadata
- pyacoustid: Audio fingerprint
- aubio: Beat/Onset detection

### Video
- moviepy: Edit/thumbnails/clips
- ffmpeg-python: Convert/extract/subs
- pymediainfo: Metadata (MKV/MP4)
- pymkv2: MKV chapters/tags
- OpenCV: Computer vision

### Container
- pymkv: MKV mux/split
- pyhandbrake: HandBrake encoding
- towebm: WebM/VP9 convert

### Subs
- pysrt: SRT parsing
- subtitle-edit: CLI subs
- pysubs2: Multi-format subs

### Codecs
- parallelencode: H264/H265 batch
- nvenc: NVIDIA hardware encoding

### Player
- python-vlc: Playback/metadata
- mpv: mpv Python bindings

### OCR/Scanner
- easyocr: Text recognition
- pyzbar: Barcode/ISBN
- pytesseract: Tesseract OCR

---

### 1-Klick Mega-Install (Python & System)
```bash
pip install mutagen pydub tinytag pyacoustid aubio moviepy ffmpeg-python pymediainfo pymkv2 opencv-python pysrt pysubs2 pyhandbrake towebm parallelencode python-vlc easyocr pyzbar pytesseract
sudo apt install mkvtoolnix handbrake vlc tesseract-ocr tesseract-ocr-deu
```

**NIX fehlt mehr – alles für Subs, MPEG, MP4, Container, Codecs, VLC, OCR, Player, Scanner, Batch!**

---

## ImgBurn auf Linux – Beste Alternativen & Python-Integration

### 1. TOP Linux-Alternativen (GUI)
| Tool      | Features                | Installation                | Beste für         |
|-----------|-------------------------|-----------------------------|-------------------|
| K3b       | CD/DVD/BluRay, ISO, Audio, Verify | sudo apt install k3b      | Alles (ImgBurn-Äquivalent) |
| Brasero   | Einfach, Data/Audio CD  | sudo apt install brasero    | Anfänger          |
| Xfburn    | Leicht, Data CD         | sudo apt install xfburn     | Minimal           |
| Graveman  | Data/Audio/ISO          | sudo apt install graveman   | Fortgeschritten   |

### 2. CLI Tools (Python-freundlich)
```bash
sudo apt install cdrdao growisofs genisoimage dvd+rw-tools
```

#### ISO erstellen & brennen
```python
import subprocess
import os

def create_iso(folder: str, iso_name: str):
    """Ordner → ISO (genisoimage)"""
    cmd = [
        'genisoimage',
        '-o', iso_name,
        '-J', '-R',  # Joliet + RockRidge
        '-V', 'Media_Library',
        folder
    ]
    subprocess.run(cmd, check=True)
    return iso_name

def burn_iso(device: str, iso_path: str, speed='4x'):
    """ISO → CD/DVD/BluRay"""
    cmd = [
        'growisofs',
        '-speed=' + speed,
        '-dvd-compat',
        f'-Z {device}={iso_path}'
    ]
    subprocess.run(cmd, check=True)
    return True

# Verwendung
iso = create_iso('/music/album', 'album.iso')
burn_iso('/dev/sr0', iso, '8x')  # /dev/sr0 = DVD-Brenner
```

#### Audio CD brennen
```python
def burn_audio_cd(device: str, wav_folder: str):
    """WAVs → Audio CD"""
    cmd = [
        'cdrdao', 'write', '--device', device,
        '--speed', '8x',
        'toc_file.cue'  # CUE-Sheet generieren
    ]
    subprocess.run(cmd, check=True)
```

### 3. Vollständige Python-Klasse (Eel-Integration)
```python
class LinuxBurner:
    def __init__(self, device='/dev/sr0'):
        self.device = device
    def list_drives(self):
        """Finde alle Brenner"""
        result = subprocess.run(['wodim', '--devices'], capture_output=True, text=True)
        return result.stdout
    def burn_data_iso(self, folder: str, label='Media'):
        """Ordner → Data-DVD"""
        iso = f'/tmp/{label}.iso'
        create_iso(folder, iso)
        burn_iso(self.device, iso, '4x')
        os.remove(iso)
        return True
    def burn_audio(self, wav_files: list):
        """Audio CD"""
        cue_content = f"""
FILE "{wav_files[0]}" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
"""
        with open('/tmp/audio.cue', 'w') as f:
            f.write(cue_content)
        subprocess.run(['cdrdao', 'write', f'--device {self.device}', '/tmp/audio.cue'])

burner = LinuxBurner()

@eel.expose
def burn_folder(folder: str):
    return burner.burn_data_iso(folder)

@eel.expose
def list_burners():
    return burner.list_drives()
```

### 4. K3b automatisieren (GUI-Tool)
```python
subprocess.run(['k3b', '--burn', 'data.iso'])  # Nicht perfekt
```

### 5. JS Frontend (Eel)
```javascript
async function burnData() {
    const folder = '/music/album';
    const result = await eel.burn_folder(folder)();
    alert(result ? '✅ Burned!' : '❌ Error');
}

async function listDrives() {
    const drives = await eel.list_burners()();
    console.log('Brenner:', drives);
}
```

### 6. Vollständige Workflow
1. scrape_folder() → Metadaten extrahieren
2. create_iso(library_export/) → ISO generieren
3. burn_iso(/dev/sr0, library.iso) → Brennen
4. validate_burn() → Prüfen

### Beste Setup (MX Linux)
```bash
sudo apt update
sudo apt install k3b cdrdao growisofs genisoimage dvd+rw-tools
wodim --devices  # Zeigt /dev/sr0 etc.
python burner.py
```

**K3b = Linux-ImgBurn (GUI)! growisofs = CLI-Power. Zero-Konfiguration brennen!**

---

## CONTAINER PROCESSING – MKV Mux + HandBrake + WebM

**Perfekte Ergänzung für deine Media-Library!**
- **pymkv** (MKV Mux/Split)
- **pyhandbrake** (Video Encoding)
- **towebm** (WebM/VP9 Streaming)

### 1. Installation
```bash
sudo apt install mkvtoolnix handbrake-cli ffmpeg
pip install pymkv pyhandbrake  # towebm ist Script (siehe unten)
```

### 2. pymkv – MKV Mux/Split (Chapters/Tags)
```python
from pymkv import MKVFile, MKVTrack
import eel

@eel.expose
def mux_mkv(video: str, audio: str, subs: str = None, output: str = "output.mkv"):
    """Video + Audio + Subs → MKV"""
    mkv = MKVFile()
    mkv.add_track(video, track_id=0, track_type='video')
    mkv.add_track(audio, track_id=1, track_type='audio')
    if subs:
        mkv.add_track(subs, track_id=2, track_type='subtitle')
    mkv.chapters = [
        {"start_time": "00:00:00", "end_time": "00:05:00", "name": "Intro"},
        {"start_time": "00:05:00", "name": "Main"}
    ]
    mkv.mux(output)
    return {'success': True, 'output': output}

@eel.expose
def split_mkv(input_mkv: str, chapters: list):
    """MKV splitten (Chapters)"""
    mkv = MKVFile(input_mkv)
    for i, chap in enumerate(chapters):
        mkv.split(f"part_{i}.mkv", chapters=[chap])
    return {'success': True}
```

### 3. pyhandbrake – Video Encoding
```python
from handbrake import HandBrake
import eel

@eel.expose
def encode_video(input_file: str, output_file: str, preset='Fast 1080p30'):
    """HandBrake Encoding mit Progress"""
    def progress(p):
        print(f"Encoding: {p.task_description} {int(p.percent)}%")
    hb = HandBrake()
    hb.rip_title(input_file, output_file, preset, progress_handler=progress)
    return {'success': True, 'output': output_file}

@eel.expose
def list_presets():
    hb = HandBrake()
    return hb.list_presets()
```

### 4. towebm – WebM/VP9 Converter (Streaming)
**towebm.py** ist ein Single-File Script (kein pip):
```bash
wget https://github.com/Kagami/webm.py/raw/master/towebm.py
chmod +x towebm.py
```

```python
import subprocess
import eel

@eel.expose
def to_webm(input_video: str, output_webm: str, crf=30):
    """MP4/AVI → WebM (VP9/Opus)"""
    cmd = [
        'python3', 'towebm.py',
        input_video, '-o', output_webm,
        '--crf', str(crf),
        '--audio-bitrate', '128k'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'error': result.stderr
    }
```

### 5. Vollständige Container Pipeline (Eel)
```python
@eel.expose
def media_pipeline(input_folder: str, output_folder: str):
    """1. Encode → 2. Mux → 3. WebM"""
    videos = glob.glob(input_folder + "/*.{mp4,avi,mkv}", recursive=True)
    for video in videos:
        encoded = video.replace('.mp4', '_h265.mp4')
        encode_video(video, encoded, 'H.265 MKV 1080p30')
    for enc in glob.glob(output_folder + "/*_h265.*"):
        audio = enc.replace('h265.mp4', 'audio.aac')
        subs = enc.replace('h265.mp4', 'subs.srt')
        mkv_out = enc.replace('.mp4', '.mkv')
        mux_mkv(enc, audio, subs, mkv_out)
    for mkv in glob.glob(output_folder + "/*.mkv"):
        webm = mkv.replace('.mkv', '.webm')
        to_webm(mkv, webm)
    return {'success': True, 'webm_count': len(glob.glob('*.webm'))}
```

### 6. JS Frontend
```javascript
async function processMedia() {
    const input = '/raw_videos';
    const output = '/processed';
    const result = await eel.media_pipeline(input, output)();
    console.log('✅', result.webm_count, 'WebM erstellt');
}
```

### Features
```
✅ MKV Mux (Video+Audio+Subs+Chapters)
✅ H.265 Encoding (HandBrake)
✅ WebM/VP9 (Web-Streaming)
✅ Batch-Processing
✅ Progress-Tracking
```

**Deine Library → Streaming-ready (WebM + MKV)! CRF 20-30 = YouTube-Qualität. Preset: Fast 1080p30 oder H.265 MKV HQ.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## SUBTITLES PROCESSING – SRT/ASS/VTT + CLI Tools

**pysrt**, **pysubs2** + **Subtitle Edit CLI** – vollständige Subtitle-Pipeline für MKV-Muxing/Media-Library!

### 1. Installation
```bash
pip install pysrt pysubs2 srt
sudo apt install subtitleeditor  # GUI (optional)
```

### 2. pysrt – SRT Parsing/Editing
```python
import pysrt
import eel

@eel.expose
def process_srt(srt_path: str):
    """SRT laden → bearbeiten → speichern"""
    subs = pysrt.open(srt_path)
    subs.shift(seconds=2)
    for sub in subs:
        sub.text = sub.text.upper()
    mid_subs = subs.slice(starts_after={'minutes': 10}, ends_before={'minutes': 20})
    output = srt_path.replace('.srt', '_edited.srt')
    mid_subs.save(output, encoding='utf-8')
    return {
        'success': True,
        'subs_count': len(subs),
        'edited': len(mid_subs),
        'output': output
    }
```

### 3. pysubs2 – Multi-Format (SRT/ASS/VTT/SMI)
```python
import pysubs2
import eel

@eel.expose
def subs_universal(input_path: str, output_format='srt'):
    """Beliebige Subs → SRT/ASS"""
    subs = pysubs2.load(input_path, encoding='utf-8')
    subs.shift(s=1.5)
    for line in subs:
        line.custom_style = '{\\fs24\\b1\\c&H00FF00&}'
    output = input_path.rsplit('.', 1)[0] + f'_{output_format}.{output_format}'
    subs.save(output)
    return {
        'success': True,
        'input_format': pysubs2.format_from_filename(input_path),
        'output': output
    }
```

### 4. Subtitle Edit CLI (via Python)
```python
import subprocess
import eel

@eel.expose
def subtitle_edit_cli(input_subs: str, output_subs: str, action='fix'):
    """Subtitle Edit Kommandozeile"""
    cmd = [
        'SubtitleEditCLI',
        input_subs,
        '--fixCommonErrors',
        '--autoAnimateCommonErrors',
        '--setMinDisplayTimeBetweenSE:2000',
        '--outputFormat:srt',
        '--outputFile:' + output_subs
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'errors': result.stderr
    }
```

### 5. Vollständige Subtitle Pipeline (MKV-Integration)
```python
@eel.expose
def subs_pipeline(video: str, subs_folder: str):
    """1. SRT fixen → 2. Timing sync → 3. MKV muxen"""
    srts = glob.glob(subs_folder + "/*.srt")
    fixed_srts = []
    for srt in srts:
        fixed = process_srt(srt)
        fixed_srts.append(fixed['output'])
    best_srt = next((s for s in fixed_srts if Path(video).stem in Path(s).stem), fixed_srts[0])
    mkv_out = video.replace('.mp4', '.mkv')
    mux_mkv(video, best_srt, mkv_out)
    return {'success': True, 'mkv': mkv_out, 'subs_used': best_srt}
```

### 6. Batch CLI (pysubs2)
```bash
pysubs2 --shift 0.5s --to srt *.srt *.ass
pysubs2 input.srt --translate de --to output.srt
```

### 7. JS Frontend
```javascript
async function fixSubs(file) {
    const result = await eel.process_srt(file.path)();
    console.log('✅ Fixed:', result.output);
    await eel.subs_pipeline('video.mp4', '/subs');
}
```

### Features
```
✅ SRT/ASS/VTT/SMI parsing
✅ Timing shift/sync
✅ Text bearbeiten (Übersetzen/Style)
✅ Batch-Processing
✅ MKV-Muxing Integration
✅ CLI + GUI
```

**Subtitle Edit CLI = automatische Fixes (Lücken, Kurz-Subs). pysubs2 = Multi-Format Power!**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Unterstützte Formate – Media-Library 2026

### Audio
- FLAC, MP3, M4A, AAC, WAV, OGG, OPUS, WMA

### Video
- MP4, MKV, AVI, MOV, WEBM, MPEG, FLV, WMV, 3GP

### Container
- MKV, MP4, AVI, MOV, WEBM, FLV, MPEG

### Subs
- SRT, ASS, VTT, SUB, SMI, SSA

### Dokumente
- PDF, EPUB, DOCX, ODT, RTF, CBZ, CBR, TXT

### Bilder
- JPG, PNG, BMP, GIF, TIFF, WEBP, FITS

### Scanner/OCR
- Barcode, QR-Code, ISBN, Text (OCR)

### Sonstige
- ChromaDB Embeddings, SQLite DB, Audio Fingerprint (AcoustID)

---

**Alle Formate sind batch- und GUI-fähig, können indexiert, konvertiert und gemuxed werden.**

---

## Eel/Bottle Teststrategie: Playwright & pytest

### 1. Playwright für Eel/Bottle-Server
- Playwright installiert Browser automatisch (Chrome, Firefox, Webkit).
- Stabiler als Selenium für UI-Tests.
- Ideal für Eel/NiceGUI-ähnliche Apps.

**Setup:**
```bash
pip install pytest playwright
playwright install  # Installiert Browser
```

**Bottle-Server starten (z.B. Port 8000):**
```python
import eel

eel.init('web')
eel.start('index.html', port=8000)
```

**Playwright-Test (pytest):**
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.asyncio
async def test_eel_ui(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Media Web Viewer"
    # UI-Elemente prüfen
    assert page.query_selector("#thumb")
```

### 2. Async UI-Checks mit pytest
- pytest.mark.asyncio für asynchrone Tests
- Kombinierbar mit Playwright für moderne UI

**Weitere Checks:**
- Button-Klicks, Cover-Upload, Thumbnail-Update
- Screenshot/Visual Regression

### 3. Hinweise
- Playwright ist stabiler und schneller als Selenium
- Browser werden automatisch installiert
- Für Eel/NiceGUI/Bottle-Apps optimal

**Empfohlene Struktur:**
- tests/test_ui_playwright.py
- pytest für alle UI/Integrationstests

---

## OpenCV (cv2) – Image Processing Power-Tool für Media-Library

### Installation
```bash
pip install opencv-python opencv-contrib-python  # + headless: opencv-python-headless
```

### 1. Image Binning mit cv2 (blitzschnell!)
```python
import cv2
import numpy as np
from pathlib import Path
import eel

@eel.expose
def cv2_bin_image(image_path: str, bin_size: int = 4):
    """2x2/4x4 Binning mit OpenCV (blitzschnell!)"""
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_h, new_w = h // bin_size, w // bin_size
    binned = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    thumb_path = f"thumbs/{Path(image_path).stem}_cv2.jpg"
    Path('thumbs').mkdir(exist_ok=True)
    cv2.imwrite(thumb_path, binned, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return {
        'success': True,
        'orig_size': [w, h],
        'binned_size': [new_w, new_h],
        'thumb': thumb_path
    }
```

### 2. Cover-Art Features (Histogram + ORB)
```python
@eel.expose
def cv2_image_features(image_path: str):
    """Histogram + ORB Features für Cover-Matching"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_norm = cv2.normalize(hist, hist).flatten()
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return {
        'success': True,
        'histogram': hist_norm.tolist()[:50],
        'keypoints': len(kp) if kp else 0,
        'features': des.tolist()[:10] if des is not None else []
    }
```

### 3. QR/Barcode Scanner (Album-Art)
```python
@eel.expose
def scan_cover_qr(image_path: str):
    """Finde QR-Codes/Links in Cover-Art"""
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return {'success': True, 'qr_data': data, 'bbox': bbox.tolist()}
    return {'success': False, 'message': 'Kein QR-Code gefunden'}
```

### 4. Vollständiger Image Handler (Scraper-Integration)
```python
def process_image_cv2(filepath: str):
    """cv2 für Media-Library Scraper"""
    path = Path(filepath)
    features = cv2_image_features(filepath)
    thumb = cv2_bin_image(filepath)
    img_pil = Image.open(filepath)
    exif = dict(img_pil._getexif() or {})
    return {
        'success': True, 'format': 'IMAGE',
        'text': f"Cover: {path.stem} ({features['keypoints']} Features)",
        'title': exif.get(0x010E, path.stem),
        'features': {
            'hist': features['histogram'],
            'thumb': thumb['thumb'],
            'size': thumb['orig_size']
        }
    }
```

### 5. Batch Cover Processing (Ordner)
```python
@eel.expose
def process_covers_folder(folder: str):
    """Alle JPG/PNG → Thumbs + Features"""
    images = glob.glob(folder + "/*.{jpg,jpeg,png}", recursive=True)
    results = []
    for img in images[:100]:
        result = process_image_cv2(img)
        results.append(result)
    return json.dumps(results)
```

### 6. Cover Similarity Suche
```python
def cover_similarity(img1_path: str, img2_path: str):
    """Vergleiche 2 Covers (Histogram + ORB)"""
    feat1 = cv2_image_features(img1_path)
    feat2 = cv2_image_features(img2_path)
    hist_sim = cv2.compareHist(
        np.array(feat1['histogram']),
        np.array(feat2['histogram']),
        cv2.HISTCMP_CORREL
    )
    return {'similarity': float(hist_sim), 'match': hist_sim > 0.8}
```

### cv2 vs. Pillow (für deine Library)
| Feature     | cv2      | Pillow   |
|-------------|----------|----------|
| Binning     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Features    | ⭐⭐⭐⭐⭐   | ❌      |
| QR/Barcode  | ⭐⭐⭐⭐⭐   | ❌      |
| Speed       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Batch       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |

### JS Frontend Beispiel
```javascript
async function processCover(file) {
    const features = await eel.cv2_image_features(file.path)();
    const thumb = await eel.cv2_bin_image(file.path, 4)();
    document.getElementById('thumb').src = thumb.thumb;
    console.log('Features:', features.histogram);
}
```

**cv2 = Media-Library Power-Tool! Cover-Matching + QR-Scanning für automatische Tagging.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Complete Multimedia Tools 2026 – Install-Ready

### Audio
- mutagen: Metadata/Tags/Cover (FLAC/MP3/M4A)
- pydub: Audio cut/merge/convert
- tinytag: Fast metadata
- pyacoustid: Audio fingerprint
- aubio: Beat/Onset detection

### Video
- moviepy: Edit/thumbnails/clips
- ffmpeg-python: Convert/extract/subs
- pymediainfo: Metadata (MKV/MP4)
- pymkv2: MKV chapters/tags
- OpenCV: Computer vision

### Container
- pymkv: MKV mux/split
- pyhandbrake: HandBrake encoding
- towebm: WebM/VP9 convert

### Subs
- pysrt: SRT parsing
- subtitle-edit: CLI subs
- pysubs2: Multi-format subs

### Codecs
- parallelencode: H264/H265 batch
- nvenc: NVIDIA hardware encoding

### Player
- python-vlc: Playback/metadata
- mpv: mpv Python bindings

### OCR/Scanner
- easyocr: Text recognition
- pyzbar: Barcode/ISBN
- pytesseract: Tesseract OCR

---

### 1-Klick Mega-Install (Python & System)
```bash
pip install mutagen pydub tinytag pyacoustid aubio moviepy ffmpeg-python pymediainfo pymkv2 opencv-python pysrt pysubs2 pyhandbrake towebm parallelencode python-vlc easyocr pyzbar pytesseract
sudo apt install mkvtoolnix handbrake vlc tesseract-ocr tesseract-ocr-deu
```

**NIX fehlt mehr – alles für Subs, MPEG, MP4, Container, Codecs, VLC, OCR, Player, Scanner, Batch!**

---

## ImgBurn auf Linux – Beste Alternativen & Python-Integration

### 1. TOP Linux-Alternativen (GUI)
| Tool      | Features                | Installation                | Beste für         |
|-----------|-------------------------|-----------------------------|-------------------|
| K3b       | CD/DVD/BluRay, ISO, Audio, Verify | sudo apt install k3b      | Alles (ImgBurn-Äquivalent) |
| Brasero   | Einfach, Data/Audio CD  | sudo apt install brasero    | Anfänger          |
| Xfburn    | Leicht, Data CD         | sudo apt install xfburn     | Minimal           |
| Graveman  | Data/Audio/ISO          | sudo apt install graveman   | Fortgeschritten   |

### 2. CLI Tools (Python-freundlich)
```bash
sudo apt install cdrdao growisofs genisoimage dvd+rw-tools
```

#### ISO erstellen & brennen
```python
import subprocess
import os

def create_iso(folder: str, iso_name: str):
    """Ordner → ISO (genisoimage)"""
    cmd = [
        'genisoimage',
        '-o', iso_name,
        '-J', '-R',  # Joliet + RockRidge
        '-V', 'Media_Library',
        folder
    ]
    subprocess.run(cmd, check=True)
    return iso_name

def burn_iso(device: str, iso_path: str, speed='4x'):
    """ISO → CD/DVD/BluRay"""
    cmd = [
        'growisofs',
        '-speed=' + speed,
        '-dvd-compat',
        f'-Z {device}={iso_path}'
    ]
    subprocess.run(cmd, check=True)
    return True

# Verwendung
iso = create_iso('/music/album', 'album.iso')
burn_iso('/dev/sr0', iso, '8x')  # /dev/sr0 = DVD-Brenner
```

#### Audio CD brennen
```python
def burn_audio_cd(device: str, wav_folder: str):
    """WAVs → Audio CD"""
    cmd = [
        'cdrdao', 'write', '--device', device,
        '--speed', '8x',
        'toc_file.cue'  # CUE-Sheet generieren
    ]
    subprocess.run(cmd, check=True)
```

### 3. Vollständige Python-Klasse (Eel-Integration)
```python
class LinuxBurner:
    def __init__(self, device='/dev/sr0'):
        self.device = device
    def list_drives(self):
        """Finde alle Brenner"""
        result = subprocess.run(['wodim', '--devices'], capture_output=True, text=True)
        return result.stdout
    def burn_data_iso(self, folder: str, label='Media'):
        """Ordner → Data-DVD"""
        iso = f'/tmp/{label}.iso'
        create_iso(folder, iso)
        burn_iso(self.device, iso, '4x')
        os.remove(iso)
        return True
    def burn_audio(self, wav_files: list):
        """Audio CD"""
        cue_content = f"""
FILE "{wav_files[0]}" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
"""
        with open('/tmp/audio.cue', 'w') as f:
            f.write(cue_content)
        subprocess.run(['cdrdao', 'write', f'--device {self.device}', '/tmp/audio.cue'])

burner = LinuxBurner()

@eel.expose
def burn_folder(folder: str):
    return burner.burn_data_iso(folder)

@eel.expose
def list_burners():
    return burner.list_drives()
```

### 4. K3b automatisieren (GUI-Tool)
```python
subprocess.run(['k3b', '--burn', 'data.iso'])  # Nicht perfekt
```

### 5. JS Frontend (Eel)
```javascript
async function burnData() {
    const folder = '/music/album';
    const result = await eel.burn_folder(folder)();
    alert(result ? '✅ Burned!' : '❌ Error');
}

async function listDrives() {
    const drives = await eel.list_burners()();
    console.log('Brenner:', drives);
}
```

### 6. Vollständige Workflow
1. scrape_folder() → Metadaten extrahieren
2. create_iso(library_export/) → ISO generieren
3. burn_iso(/dev/sr0, library.iso) → Brennen
4. validate_burn() → Prüfen

### Beste Setup (MX Linux)
```bash
sudo apt update
sudo apt install k3b cdrdao growisofs genisoimage dvd+rw-tools
wodim --devices  # Zeigt /dev/sr0 etc.
python burner.py
```

**K3b = Linux-ImgBurn (GUI)! growisofs = CLI-Power. Zero-Konfiguration brennen!**

---

## CONTAINER PROCESSING – MKV Mux + HandBrake + WebM

**Perfekte Ergänzung für deine Media-Library!**
- **pymkv** (MKV Mux/Split)
- **pyhandbrake** (Video Encoding)
- **towebm** (WebM/VP9 Streaming)

### 1. Installation
```bash
sudo apt install mkvtoolnix handbrake-cli ffmpeg
pip install pymkv pyhandbrake  # towebm ist Script (siehe unten)
```

### 2. pymkv – MKV Mux/Split (Chapters/Tags)
```python
from pymkv import MKVFile, MKVTrack
import eel

@eel.expose
def mux_mkv(video: str, audio: str, subs: str = None, output: str = "output.mkv"):
    """Video + Audio + Subs → MKV"""
    mkv = MKVFile()
    mkv.add_track(video, track_id=0, track_type='video')
    mkv.add_track(audio, track_id=1, track_type='audio')
    if subs:
        mkv.add_track(subs, track_id=2, track_type='subtitle')
    mkv.chapters = [
        {"start_time": "00:00:00", "end_time": "00:05:00", "name": "Intro"},
        {"start_time": "00:05:00", "name": "Main"}
    ]
    mkv.mux(output)
    return {'success': True, 'output': output}

@eel.expose
def split_mkv(input_mkv: str, chapters: list):
    """MKV splitten (Chapters)"""
    mkv = MKVFile(input_mkv)
    for i, chap in enumerate(chapters):
        mkv.split(f"part_{i}.mkv", chapters=[chap])
    return {'success': True}
```

### 3. pyhandbrake – Video Encoding
```python
from handbrake import HandBrake
import eel

@eel.expose
def encode_video(input_file: str, output_file: str, preset='Fast 1080p30'):
    """HandBrake Encoding mit Progress"""
    def progress(p):
        print(f"Encoding: {p.task_description} {int(p.percent)}%")
    hb = HandBrake()
    hb.rip_title(input_file, output_file, preset, progress_handler=progress)
    return {'success': True, 'output': output_file}

@eel.expose
def list_presets():
    hb = HandBrake()
    return hb.list_presets()
```

### 4. towebm – WebM/VP9 Converter (Streaming)
**towebm.py** ist ein Single-File Script (kein pip):
```bash
wget https://github.com/Kagami/webm.py/raw/master/towebm.py
chmod +x towebm.py
```

```python
import subprocess
import eel

@eel.expose
def to_webm(input_video: str, output_webm: str, crf=30):
    """MP4/AVI → WebM (VP9/Opus)"""
    cmd = [
        'python3', 'towebm.py',
        input_video, '-o', output_webm,
        '--crf', str(crf),
        '--audio-bitrate', '128k'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'error': result.stderr
    }
```

### 5. Vollständige Container Pipeline (Eel)
```python
@eel.expose
def media_pipeline(input_folder: str, output_folder: str):
    """1. Encode → 2. Mux → 3. WebM"""
    videos = glob.glob(input_folder + "/*.{mp4,avi,mkv}", recursive=True)
    for video in videos:
        encoded = video.replace('.mp4', '_h265.mp4')
        encode_video(video, encoded, 'H.265 MKV 1080p30')
    for enc in glob.glob(output_folder + "/*_h265.*"):
        audio = enc.replace('h265.mp4', 'audio.aac')
        subs = enc.replace('h265.mp4', 'subs.srt')
        mkv_out = enc.replace('.mp4', '.mkv')
        mux_mkv(enc, audio, subs, mkv_out)
    for mkv in glob.glob(output_folder + "/*.mkv"):
        webm = mkv.replace('.mkv', '.webm')
        to_webm(mkv, webm)
    return {'success': True, 'webm_count': len(glob.glob('*.webm'))}
```

### 6. JS Frontend
```javascript
async function processMedia() {
    const input = '/raw_videos';
    const output = '/processed';
    const result = await eel.media_pipeline(input, output)();
    console.log('✅', result.webm_count, 'WebM erstellt');
}
```

### Features
```
✅ MKV Mux (Video+Audio+Subs+Chapters)
✅ H.265 Encoding (HandBrake)
✅ WebM/VP9 (Web-Streaming)
✅ Batch-Processing
✅ Progress-Tracking
```

**Deine Library → Streaming-ready (WebM + MKV)! CRF 20-30 = YouTube-Qualität. Preset: Fast 1080p30 oder H.265 MKV HQ.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## SUBTITLES PROCESSING – SRT/ASS/VTT + CLI Tools

**pysrt**, **pysubs2** + **Subtitle Edit CLI** – vollständige Subtitle-Pipeline für MKV-Muxing/Media-Library!

### 1. Installation
```bash
pip install pysrt pysubs2 srt
sudo apt install subtitleeditor  # GUI (optional)
```

### 2. pysrt – SRT Parsing/Editing
```python
import pysrt
import eel

@eel.expose
def process_srt(srt_path: str):
    """SRT laden → bearbeiten → speichern"""
    subs = pysrt.open(srt_path)
    subs.shift(seconds=2)
    for sub in subs:
        sub.text = sub.text.upper()
    mid_subs = subs.slice(starts_after={'minutes': 10}, ends_before={'minutes': 20})
    output = srt_path.replace('.srt', '_edited.srt')
    mid_subs.save(output, encoding='utf-8')
    return {
        'success': True,
        'subs_count': len(subs),
        'edited': len(mid_subs),
        'output': output
    }
```

### 3. pysubs2 – Multi-Format (SRT/ASS/VTT/SMI)
```python
import pysubs2
import eel

@eel.expose
def subs_universal(input_path: str, output_format='srt'):
    """Beliebige Subs → SRT/ASS"""
    subs = pysubs2.load(input_path, encoding='utf-8')
    subs.shift(s=1.5)
    for line in subs:
        line.custom_style = '{\\fs24\\b1\\c&H00FF00&}'
    output = input_path.rsplit('.', 1)[0] + f'_{output_format}.{output_format}'
    subs.save(output)
    return {
        'success': True,
        'input_format': pysubs2.format_from_filename(input_path),
        'output': output
    }
```

### 4. Subtitle Edit CLI (via Python)
```python
import subprocess
import eel

@eel.expose
def subtitle_edit_cli(input_subs: str, output_subs: str, action='fix'):
    """Subtitle Edit Kommandozeile"""
    cmd = [
        'SubtitleEditCLI',
        input_subs,
        '--fixCommonErrors',
        '--autoAnimateCommonErrors',
        '--setMinDisplayTimeBetweenSE:2000',
        '--outputFormat:srt',
        '--outputFile:' + output_subs
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'errors': result.stderr
    }
```

### 5. Vollständige Subtitle Pipeline (MKV-Integration)
```python
@eel.expose
def subs_pipeline(video: str, subs_folder: str):
    """1. SRT fixen → 2. Timing sync → 3. MKV muxen"""
    srts = glob.glob(subs_folder + "/*.srt")
    fixed_srts = []
    for srt in srts:
        fixed = process_srt(srt)
        fixed_srts.append(fixed['output'])
    best_srt = next((s for s in fixed_srts if Path(video).stem in Path(s).stem), fixed_srts[0])
    mkv_out = video.replace('.mp4', '.mkv')
    mux_mkv(video, best_srt, mkv_out)
    return {'success': True, 'mkv': mkv_out, 'subs_used': best_srt}
```

### 6. Batch CLI (pysubs2)
```bash
pysubs2 --shift 0.5s --to srt *.srt *.ass
pysubs2 input.srt --translate de --to output.srt
```

### 7. JS Frontend
```javascript
async function fixSubs(file) {
    const result = await eel.process_srt(file.path)();
    console.log('✅ Fixed:', result.output);
    await eel.subs_pipeline('video.mp4', '/subs');
}
```

### Features
```
✅ SRT/ASS/VTT/SMI parsing
✅ Timing shift/sync
✅ Text bearbeiten (Übersetzen/Style)
✅ Batch-Processing
✅ MKV-Muxing Integration
✅ CLI + GUI
```

**Subtitle Edit CLI = automatische Fixes (Lücken, Kurz-Subs). pysubs2 = Multi-Format Power!**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Unterstützte Formate – Media-Library 2026

### Audio
- FLAC, MP3, M4A, AAC, WAV, OGG, OPUS, WMA

### Video
- MP4, MKV, AVI, MOV, WEBM, MPEG, FLV, WMV, 3GP

### Container
- MKV, MP4, AVI, MOV, WEBM, FLV, MPEG

### Subs
- SRT, ASS, VTT, SUB, SMI, SSA

### Dokumente
- PDF, EPUB, DOCX, ODT, RTF, CBZ, CBR, TXT

### Bilder
- JPG, PNG, BMP, GIF, TIFF, WEBP, FITS

### Scanner/OCR
- Barcode, QR-Code, ISBN, Text (OCR)

### Sonstige
- ChromaDB Embeddings, SQLite DB, Audio Fingerprint (AcoustID)

---

**Alle Formate sind batch- und GUI-fähig, können indexiert, konvertiert und gemuxed werden.**

---

## Eel/Bottle Teststrategie: Playwright & pytest

### 1. Playwright für Eel/Bottle-Server
- Playwright installiert Browser automatisch (Chrome, Firefox, Webkit).
- Stabiler als Selenium für UI-Tests.
- Ideal für Eel/NiceGUI-ähnliche Apps.

**Setup:**
```bash
pip install pytest playwright
playwright install  # Installiert Browser
```

**Bottle-Server starten (z.B. Port 8000):**
```python
import eel

eel.init('web')
eel.start('index.html', port=8000)
```

**Playwright-Test (pytest):**
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.mark.asyncio
async def test_eel_ui(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000")
    assert page.title() == "Media Web Viewer"
    # UI-Elemente prüfen
    assert page.query_selector("#thumb")
```

### 2. Async UI-Checks mit pytest
- pytest.mark.asyncio für asynchrone Tests
- Kombinierbar mit Playwright für moderne UI

**Weitere Checks:**
- Button-Klicks, Cover-Upload, Thumbnail-Update
- Screenshot/Visual Regression

### 3. Hinweise
- Playwright ist stabiler und schneller als Selenium
- Browser werden automatisch installiert
- Für Eel/NiceGUI/Bottle-Apps optimal

**Empfohlene Struktur:**
- tests/test_ui_playwright.py
- pytest für alle UI/Integrationstests

---

## OpenCV (cv2) – Image Processing Power-Tool für Media-Library

### Installation
```bash
pip install opencv-python opencv-contrib-python  # + headless: opencv-python-headless
```

### 1. Image Binning mit cv2 (blitzschnell!)
```python
import cv2
import numpy as np
from pathlib import Path
import eel

@eel.expose
def cv2_bin_image(image_path: str, bin_size: int = 4):
    """2x2/4x4 Binning mit OpenCV (blitzschnell!)"""
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    new_h, new_w = h // bin_size, w // bin_size
    binned = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    thumb_path = f"thumbs/{Path(image_path).stem}_cv2.jpg"
    Path('thumbs').mkdir(exist_ok=True)
    cv2.imwrite(thumb_path, binned, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return {
        'success': True,
        'orig_size': [w, h],
        'binned_size': [new_w, new_h],
        'thumb': thumb_path
    }
```

### 2. Cover-Art Features (Histogram + ORB)
```python
@eel.expose
def cv2_image_features(image_path: str):
    """Histogram + ORB Features für Cover-Matching"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_norm = cv2.normalize(hist, hist).flatten()
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return {
        'success': True,
        'histogram': hist_norm.tolist()[:50],
        'keypoints': len(kp) if kp else 0,
        'features': des.tolist()[:10] if des is not None else []
    }
```

### 3. QR/Barcode Scanner (Album-Art)
```python
@eel.expose
def scan_cover_qr(image_path: str):
    """Finde QR-Codes/Links in Cover-Art"""
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return {'success': True, 'qr_data': data, 'bbox': bbox.tolist()}
    return {'success': False, 'message': 'Kein QR-Code gefunden'}
```

### 4. Vollständiger Image Handler (Scraper-Integration)
```python
def process_image_cv2(filepath: str):
    """cv2 für Media-Library Scraper"""
    path = Path(filepath)
    features = cv2_image_features(filepath)
    thumb = cv2_bin_image(filepath)
    img_pil = Image.open(filepath)
    exif = dict(img_pil._getexif() or {})
    return {
        'success': True, 'format': 'IMAGE',
        'text': f"Cover: {path.stem} ({features['keypoints']} Features)",
        'title': exif.get(0x010E, path.stem),
        'features': {
            'hist': features['histogram'],
            'thumb': thumb['thumb'],
            'size': thumb['orig_size']
        }
    }
```

### 5. Batch Cover Processing (Ordner)
```python
@eel.expose
def process_covers_folder(folder: str):
    """Alle JPG/PNG → Thumbs + Features"""
    images = glob.glob(folder + "/*.{jpg,jpeg,png}", recursive=True)
    results = []
    for img in images[:100]:
        result = process_image_cv2(img)
        results.append(result)
    return json.dumps(results)
```

### 6. Cover Similarity Suche
```python
def cover_similarity(img1_path: str, img2_path: str):
    """Vergleiche 2 Covers (Histogram + ORB)"""
    feat1 = cv2_image_features(img1_path)
    feat2 = cv2_image_features(img2_path)
    hist_sim = cv2.compareHist(
        np.array(feat1['histogram']),
        np.array(feat2['histogram']),
        cv2.HISTCMP_CORREL
    )
    return {'similarity': float(hist_sim), 'match': hist_sim > 0.8}
```

### cv2 vs. Pillow (für deine Library)
| Feature     | cv2      | Pillow   |
|-------------|----------|----------|
| Binning     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Features    | ⭐⭐⭐⭐⭐   | ❌      |
| QR/Barcode  | ⭐⭐⭐⭐⭐   | ❌      |
| Speed       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐     |
| Batch       | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  |

### JS Frontend Beispiel
```javascript
async function processCover(file) {
    const features = await eel.cv2_image_features(file.path)();
    const thumb = await eel.cv2_bin_image(file.path, 4)();
    document.getElementById('thumb').src = thumb.thumb;
    console.log('Features:', features.histogram);
}
```

**cv2 = Media-Library Power-Tool! Cover-Matching + QR-Scanning für automatische Tagging.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest du?
- Weitere Format-Handler oder GUI-Beispiele gewünscht?

---

## Complete Multimedia Tools 2026 – Install-Ready

### Audio
- mutagen: Metadata/Tags/Cover (FLAC/MP3/M4A)
- pydub: Audio cut/merge/convert
- tinytag: Fast metadata
- pyacoustid: Audio fingerprint
- aubio: Beat/Onset detection

### Video
- moviepy: Edit/thumbnails/clips
- ffmpeg-python: Convert/extract/subs
- pymediainfo: Metadata (MKV/MP4)
- pymkv2: MKV chapters/tags
- OpenCV: Computer vision

### Container
- pymkv: MKV mux/split
- pyhandbrake: HandBrake encoding
- towebm: WebM/VP9 convert

### Subs
- pysrt: SRT parsing
- subtitle-edit: CLI subs
- pysubs2: Multi-format subs

### Codecs
- parallelencode: H264/H265 batch
- nvenc: NVIDIA hardware encoding

### Player
- python-vlc: Playback/metadata
- mpv: mpv Python bindings

### OCR/Scanner
- easyocr: Text recognition
- pyzbar: Barcode/ISBN
- pytesseract: Tesseract OCR

---

### 1-Klick Mega-Install (Python & System)
```bash
pip install mutagen pydub tinytag pyacoustid aubio moviepy ffmpeg-python pymediainfo pymkv2 opencv-python pysrt pysubs2 pyhandbrake towebm parallelencode python-vlc easyocr pyzbar pytesseract
sudo apt install mkvtoolnix handbrake vlc tesseract-ocr tesseract-ocr-deu
```

**NIX fehlt mehr – alles für Subs, MPEG, MP4, Container, Codecs, VLC, OCR, Player, Scanner, Batch!**

---

## ImgBurn auf Linux – Beste Alternativen & Python-Integration

### 1. TOP Linux-Alternativen (GUI)
| Tool      | Features                | Installation                | Beste für         |
|-----------|-------------------------|-----------------------------|-------------------|
| K3b       | CD/DVD/BluRay, ISO, Audio, Verify | sudo apt install k3b      | Alles (ImgBurn-Äquivalent) |
| Brasero   | Einfach, Data/Audio CD  | sudo apt install brasero    | Anfänger          |
| Xfburn    | Leicht, Data CD         | sudo apt install xfburn     | Minimal           |
| Graveman  | Data/Audio/ISO          | sudo apt install graveman   | Fortgeschritten   |

### 2. CLI Tools (Python-freundlich)
```bash
sudo apt install cdrdao growisofs genisoimage dvd+rw-tools
```

#### ISO erstellen & brennen
```python
import subprocess
import os

def create_iso(folder: str, iso_name: str):
    """Ordner → ISO (genisoimage)"""
    cmd = [
        'genisoimage',
        '-o', iso_name,
        '-J', '-R',  # Joliet + RockRidge
        '-V', 'Media_Library',
        folder
    ]
    subprocess.run(cmd, check=True)
    return iso_name

def burn_iso(device: str, iso_path: str, speed='4x'):
    """ISO → CD/DVD/BluRay"""
    cmd = [
        'growisofs',
        '-speed=' + speed,
        '-dvd-compat',
        f'-Z {device}={iso_path}'
    ]
    subprocess.run(cmd, check=True)
    return True

# Verwendung
iso = create_iso('/music/album', 'album.iso')
burn_iso('/dev/sr0', iso, '8x')  # /dev/sr0 = DVD-Brenner
```

#### Audio CD brennen
```python
def burn_audio_cd(device: str, wav_folder: str):
    """WAVs → Audio CD"""
    cmd = [
        'cdrdao', 'write', '--device', device,
        '--speed', '8x',
        'toc_file.cue'  # CUE-Sheet generieren
    ]
    subprocess.run(cmd, check=True)
```

### 3. Vollständige Python-Klasse (Eel-Integration)
```python
class LinuxBurner:
    def __init__(self, device='/dev/sr0'):
        self.device = device
    def list_drives(self):
        """Finde alle Brenner"""
        result = subprocess.run(['wodim', '--devices'], capture_output=True, text=True)
        return result.stdout
    def burn_data_iso(self, folder: str, label='Media'):
        """Ordner → Data-DVD"""
        iso = f'/tmp/{label}.iso'
        create_iso(folder, iso)
        burn_iso(self.device, iso, '4x')
        os.remove(iso)
        return True
    def burn_audio(self, wav_files: list):
        """Audio CD"""
        cue_content = f"""
FILE "{wav_files[0]}" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
"""
        with open('/tmp/audio.cue', 'w') as f:
            f.write(cue_content)
        subprocess.run(['cdrdao', 'write', f'--device {self.device}', '/tmp/audio.cue'])

burner = LinuxBurner()

@eel.expose
def burn_folder(folder: str):
    return burner.burn_data_iso(folder)

@eel.expose
def list_burners():
    return burner.list_drives()
```

### 4. K3b automatisieren (GUI-Tool)
```python
subprocess.run(['k3b', '--burn', 'data.iso'])  # Nicht perfekt
```

### 5. JS Frontend (Eel)
```javascript
async function burnData() {
    const folder = '/music/album';
    const result = await eel.burn_folder(folder)();
    alert(result ? '✅ Burned!' : '❌ Error');
}

async function listDrives() {
    const drives = await eel.list_burners()();
    console.log('Brenner:', drives);
}
```

### 6. Vollständige Workflow
1. scrape_folder() → Metadaten extrahieren
2. create_iso(library_export/) → ISO generieren
3. burn_iso(/dev/sr0, library.iso) → Brennen
4. validate_burn() → Prüfen

### Beste Setup (MX Linux)
```bash
sudo apt update
sudo apt install k3b cdrdao growisofs genisoimage dvd+rw-tools
wodim --devices  # Zeigt /dev/sr0 etc.
python burner.py
```

**K3b = Linux-ImgBurn (GUI)! growisofs = CLI-Power. Zero-Konfiguration brennen!**

---

## CONTAINER PROCESSING – MKV Mux + HandBrake + WebM

**Perfekte Ergänzung für deine Media-Library!**
- **pymkv** (MKV Mux/Split)
- **pyhandbrake** (Video Encoding)
- **towebm** (WebM/VP9 Streaming)

### 1. Installation
```bash
sudo apt install mkvtoolnix handbrake-cli ffmpeg
pip install pymkv pyhandbrake  # towebm ist Script (siehe unten)
```

### 2. pymkv – MKV Mux/Split (Chapters/Tags)
```python
from pymkv import MKVFile, MKVTrack
import eel

@eel.expose
def mux_mkv(video: str, audio: str, subs: str = None, output: str = "output.mkv"):
    """Video + Audio + Subs → MKV"""
    mkv = MKVFile()
    mkv.add_track(video, track_id=0, track_type='video')
    mkv.add_track(audio, track_id=1, track_type='audio')
    if subs:
        mkv.add_track(subs, track_id=2, track_type='subtitle')
    mkv.chapters = [
        {"start_time": "00:00:00", "end_time": "00:05:00", "name": "Intro"},
        {"start_time": "00:05:00", "name": "Main"}
    ]
    mkv.mux(output)
    return {'success': True, 'output': output}

@eel.expose
def split_mkv(input_mkv: str, chapters: list):
    """MKV splitten (Chapters)"""
    mkv = MKVFile(input_mkv)
    for i, chap in enumerate(chapters):
        mkv.split(f"part_{i}.mkv", chapters=[chap])
    return {'success': True}
```

### 3. pyhandbrake – Video Encoding
```python
from handbrake import HandBrake
import eel

@eel.expose
def encode_video(input_file: str, output_file: str, preset='Fast 1080p30'):
    """HandBrake Encoding mit Progress"""
    def progress(p):
        print(f"Encoding: {p.task_description} {int(p.percent)}%")
    hb = HandBrake()
    hb.rip_title(input_file, output_file, preset, progress_handler=progress)
    return {'success': True, 'output': output_file}

@eel.expose
def list_presets():
    hb = HandBrake()
    return hb.list_presets()
```

### 4. towebm – WebM/VP9 Converter (Streaming)
**towebm.py** ist ein Single-File Script (kein pip):
```bash
wget https://github.com/Kagami/webm.py/raw/master/towebm.py
chmod +x towebm.py
```

```python
import subprocess
import eel

@eel.expose
def to_webm(input_video: str, output_webm: str, crf=30):
    """MP4/AVI → WebM (VP9/Opus)"""
    cmd = [
        'python3', 'towebm.py',
        input_video, '-o', output_webm,
        '--crf', str(crf),
        '--audio-bitrate', '128k'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        'success': result.returncode == 0,
        'log': result.stdout,
        'error': result.stderr
    }
```

### 5. Vollständige Container Pipeline (Eel)
```python
@eel.expose
def media_pipeline(input_folder: str, output_folder: str):
    """1. Encode → 2. Mux → 3. WebM"""
    videos = glob.glob(input_folder + "/*.{mp4,avi,mkv}", recursive=True)
    for video in videos:
        encoded = video.replace('.mp4', '_h265.mp4')
        encode_video(video, encoded, 'H.265 MKV 1080p30')
    for enc in glob.glob(output_folder + "/*_h265.*"):
        audio = enc.replace('h265.mp4', 'audio.aac')
        subs = enc.replace('h265.mp4', 'subs.srt')
        mkv_out = enc.replace('.mp4', '.mkv')
        mux_mkv(enc, audio, subs, mkv_out)
    for mkv in glob.glob(output_folder + "/*.mkv"):
        webm = mkv.replace('.mkv', '.webm')
        to_webm(mkv, webm)
    return {'success': True, 'webm_count': len(glob.glob('*.webm'))}
```

### 6. JS Frontend
```javascript
async function processMedia() {
    const input = '/raw_videos';
    const output = '/processed';
    const result = await eel.media_pipeline(input, output)();
    console.log('✅', result.webm_count, 'WebM erstellt');
}
```

### Features
```
✅ MKV Mux (Video+Audio+Subs+Chapters)
✅ H.265 Encoding (HandBrake)
✅ WebM/VP9 (Web-Streaming)
✅ Batch-Processing
✅ Progress-Tracking
```

**Deine Library → Streaming-ready (WebM + MKV)! CRF 20-30 = YouTube-Qualität. Preset: Fast 1080p30 oder H.265 MKV HQ.**

---

**Siehe auch:**
- [Playwright Doku](https://playwright.dev/python/docs/intro)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/)

---

**Fragen/Feedback:**
- Wie viele Dateien erwartest