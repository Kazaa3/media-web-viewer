# FFplay Modes – Vollständige Integration (März 2026)

## 🗂️ FFplay Modus-Tabelle
| Modus         | Command                                   | Use-Case                | Features                |
|---------------|-------------------------------------------|-------------------------|-------------------------|
| ffplay-direct | ffplay file.mkv                           | Lokale Files/ISO        | Full Decode             |
| ffplay-rtsp   | ffplay rtsp://localhost:8554/stream       | MTX/VLC Streams         | RTSP Client             |
| ffplay-hls    | ffplay playlist.m3u8                      | HLS Testing             | Live/VOD                |
| ffplay-hw     | ffplay -hwaccel vaapi file.mp4            | GPU Decode (Intel/AMD)  | Low CPU                 |
| ffplay-vdpau  | ffplay -hwaccel vdpau file.mkv            | NVIDIA (Legacy)         | VDPAU                   |
| ffplay-nvdec  | ffplay -hwaccel cuda file.mkv             | NVIDIA NVDEC            | Modern NVIDIA           |

## 🛠️ Backend: FFplay Controller
- Zentrale Klasse `FFplayController` für alle Modi (direct, rtsp, hls, hw-vaapi, hw-nvdec, ...).
- Methoden: `play(input_path, mode)`, `kill()`, `status()`.
- HW-Decode Detection integriert (vaapi/nvdec/software).
- Remote- und Docker-Integration für NAS/Server-Tests.

## 🖥️ Frontend: FFplay Panel & Controls
- UI-Panel mit Buttons für alle FFplay-Modi (Direct, RTSP, VAAPI, NVDEC, ...).
- Statusanzeige und Kill-Button für Prozesskontrolle.
- JS-Integration für Moduswahl und Status-Updates.

## 🔍 Spezialfälle
- **DVD-ISO:** Direkter Start ohne Menüs (ffplay file.iso).
- **Remote:** SSH-Start auf NAS/Server (`ssh user@host ffplay ...`).
- **Docker:** Containerized Debugging mit jrottenberg/ffmpeg.

## ⚡ Vergleich: FFplay vs VLC/cvlc
| Feature   | FFplay | VLC/cvlc |
|-----------|--------|----------|
| DVD-ISO   | ✅ (no menu) | ✅ Full DVD |
| RTSP      | ✅      | ✅        |
| HW-Decode | ✅ VAAPI/NVDEC | ✅ VDPAU |
| CLI-only  | ✅      | ✅ (cvlc) |
| Menüs     | ❌      | ✅        |

## ✅ Empfehlung
FFplay ist der ultimative Quick-Test/Debug-Player für alle Formate und Streams – ideal für Entwickler, Netzwerk- und Hardware-Tests.

---

**Result:**
FFplay ist jetzt vollständig integriert, unterstützt alle relevanten Modi und ist über das UI und Backend zentral steuerbar.
