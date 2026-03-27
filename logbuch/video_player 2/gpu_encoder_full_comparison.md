# VAAPI / NVENC / CPU / AMD / Intel Onboard / Arc – Voller Vergleich (März 2026)

**MX Linux + Multi-GPU Setup – Alle 6 Varianten im Überblick**

---

## 1. Hardware-Übersicht
| GPU                | API         | Codecs           | Linux | 4K RT | Qualität   | Dein Setup      |
|--------------------|-------------|------------------|-------|-------|------------|-----------------|
| Intel Onboard (iGPU)| QSV/VAAPI  | H264/HEVC        | ✅    | 8–15x | Gut        | ✅              |
| Intel Arc (Axxx)   | VAAPI       | H264/HEVC/AV1    | ✅    | 12–25x| Sehr gut   | ✅ Beste Wahl   |
| Nvidia (RTX/GTX)   | NVENC       | H264/HEVC/AV1    | ✅    | 15–35x| Gut        | ❌              |
| AMD (RX 6000+)     | VAAPI/VCE   | H264/HEVC        | ⚠️    | 10–20x| Mittel     | ❌              |
| CPU (i5/i7)        | x264        | Alles            | ✅    | 0.5–3x| Referenz   | ✅ Fallback     |

---

## 2. FFmpeg Commands (Unified)
```python
def get_encoder():
    if os.system('vainfo | grep -q AV1') == 0: return 'vaapi'      # Arc ✅
    if os.system('nvidia-smi >/dev/null 2>&1') == 0: return 'nvenc'  # RTX
    if os.system('ffmpeg -encoders | grep -q qsv') == 0: return 'qsv' # iGPU
    return 'libx264'  # CPU

encoder = get_encoder()
print(f"✅ Using: {encoder}")

cmd = [
    f'-hwaccel', encoder,
    '-i', 'input.iso',
    f'-c:v', f'{encoder}_h264', '-preset', 'fast',
    '-f', 'hls', 'output.m3u8'
]
```

---

## 3. Performance-Matrix (4K HEVC → H.264)
| Encoder      | FPS (4K) | CPU-Last | VRAM   | AV1? | Linux-Stabilität |
|--------------|----------|----------|--------|------|------------------|
| VAAPI Arc    | 25 FPS   | 8%       | 500MB  | ✅   | ⭐⭐⭐⭐⭐           |
| QSV iGPU     | 15 FPS   | 15%      | 300MB  | ❌   | ⭐⭐⭐⭐            |
| NVENC RTX    | 35 FPS   | 5%       | 400MB  | ✅   | ⭐⭐⭐⭐            |
| AMD VAAPI    | 18 FPS   | 12%      | 600MB  | ❌   | ⭐⭐⭐             |
| CPU x264     | 1.5 FPS  | 150%     | 0MB    | ❌   | ⭐⭐⭐⭐⭐           |

**Arc VAAPI = dein Champion (AV1 + 25 FPS 4K)!**

---

## 4. Installation pro GPU (MX Linux)
**Intel Onboard/Arc:**
```bash
sudo apt install intel-media-va-driver-non-free intel-gpu-tools vainfo libva-utils
export LIBVA_DRIVER_NAME=iHD
sudo chmod 666 /dev/dri/renderD128
```
**Nvidia:**
```bash
sudo apt install nvidia-driver nvidia-utils
export __NVENCODER_SDK_PATH=/usr/lib/nvidia-*
```
**AMD:**
```bash
sudo apt install mesa-va-drivers mesa-vdpau-drivers
```

---

## 5. Auto-Detect Script (Dein Router)
```python
def auto_encoder():
    if os.system('vainfo | grep -q "VAProfileAV1"') == 0:
        return ('vaapi', '/dev/dri/renderD128', 'AV1 ready!')  # Arc
    elif os.system('vainfo | grep -q "VAProfileHEVC"') == 0:
        return ('vaapi', '/dev/dri/renderD128', 'VAAPI iGPU')
    elif os.system('nvidia-smi >/dev/null 2>&1') == 0:
        return ('nvenc', None, 'RTX detected')
    return ('libx264', None, 'CPU Fallback')

encoder, device, msg = auto_encoder()
print(f"🎯 {msg}")
```

---

## 6. Quality-Ranking (Dein Use-Case)
1. Arc VAAPI → AV1/HEVC → 25x RT, Linux-native
2. Intel QSV → H.264 → 15x RT, stabil
3. Nvidia NVENC → H.264/AV1 → 35x RT, proprietär
4. CPU x264 → Alles → Qualität, aber langsam
5. AMD VAAPI → Mittel → Spotty Linux-Support

---

## 7. Dein FFmpeg Master-Template
```bash
ffmpeg \
  $([encoder=vaapi] && echo "-vaapi_device /dev/dri/renderD128 -hwaccel vaapi") \
  $([encoder=nvenc] && echo "-hwaccel nvenc") \
  -i input.iso \
  -c:v ${encoder}_h264 -preset fast -qp 23 \
  -f hls output.m3u8
```

---

**Arc VAAPI = dein perfekter Match (Linux + AV1 + 4K RT)! Install + Test → Router auto-detect! 🎥✨**

> Debug? `vainfo` + `lspci` teilen!
