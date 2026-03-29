# Logbuch: Docker-Container mit System-Tools (FFmpeg, VLC, MKVToolNix, Python)

## Ziel
Ein schlanker, GPU-fähiger Docker-Container für Media-Library-Workflows mit FFmpeg, VLC, MKVToolNix, MediaInfo und Python (inkl. venv/offline-Pakete). Perfekt für Medienverarbeitung, Batch-Transcoding und Python-Skripte – auch offline und mit GPU-Beschleunigung.

---

## 1. Dockerfile (Alpine-basiert)
```dockerfile
FROM alpine:3.20

# System-Tools (FFmpeg, VLC, MKVToolNix, MediaInfo)
RUN apk update && apk add --no-cache \
    ffmpeg \
    vlc \
    mkvtoolnix \
    mediainfo \
    python3 py3-pip py3-venv \
    && rm -rf /var/cache/apk/*

WORKDIR /app
VOLUME ["/media", "/packages"]

ENTRYPOINT ["ffmpeg"]
CMD ["-version"]
```

---

## 2. Build & Run
```bash
docker build -t media-tools .
docker run --rm -it \
  -v $(pwd)/media:/media \
  -v $(pwd)/packages:/packages \
  --device /dev/dri:/dev/dri \  # GPU VAAPI/QSV
  media-tools \
  -i /media/input.mkv -c copy /media/output.mp4
```
- Größe: ~200MB, alle Tools sofort einsatzbereit.

---

## 3. Python venv & Offline-Pakete im Container
```bash
docker run --rm -it \
  -v $(pwd)/packages:/packages \
  media-tools /bin/sh

# Im Container:
python3 -m venv /app/.venv
source /app/.venv/bin/activate
pip install --no-index --find-links /packages/ -r /packages/requirements.txt
python /app/your_script.py
```
- So installierst du Python-Pakete offline in der venv.

---

## 4. Fertige Images (Alternativen)
| Image                | Tools                | Beispiel-Run                                    |
|----------------------|----------------------|-------------------------------------------------|
| linuxserver/ffmpeg   | FFmpeg + ffprobe     | docker run linuxserver/ffmpeg -i ...            |
| jlesage/mkvtoolnix   | MKVToolNix GUI (Web) | docker run -p 5800:5800 -v /media:/storage ...  |
| leplusorg/av         | FFmpeg + MKVToolNix  | docker run leplusorg/av mkvmerge ...            |
| sitkevij/ffmpeg      | FFmpeg (Alpine)      | docker run sitkevij/ffmpeg -i ...               |

---

## 5. Docker-Compose (Media-Pipeline)
```yaml
version: '3.8'
services:
  media-tools:
    build: .
    volumes:
      - ./media:/media
      - ./packages:/packages
    devices:
      - /dev/dri:/dev/dri
    stdin_open: true
    tty: true
```
- Start: `docker compose up -d`

---

## 6. Hinweise
- Für weitere Tools (z.B. subtitles-edit): `apk add subtitles-edit`
- GPU Intel Onboard: `/dev/dri` mounten für VAAPI/QSV.
- Python venvs und Pakete bleiben komplett isoliert.
- Offline-Installationen via `pip install --no-index ...` möglich.

---

## Fazit
Mit diesem Container hast du alle wichtigen System-Tools und eine flexible Python-Umgebung für Medienverarbeitung, Transcoding und Analyse – offline, reproduzierbar, GPU-ready und leichtgewichtig.
