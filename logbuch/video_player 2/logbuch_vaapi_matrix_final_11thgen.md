## VAAPI/NVENC/CPU + AMD + 11th Gen Intel – FINAL MATRIX

**11th Gen (Tiger Lake/Iris Xe) ergänzt!**

### 1. 11th Gen Intel Details

| CPU         | iGPU        | QSV | VAAPI | H.264 | HEVC   | AV1    | 4K RT      | FFmpeg        |
|-------------|-------------|-----|-------|-------|--------|--------|------------|---------------|
| i3-1115G4   | Iris Xe     | ✅  | ✅    | 4K    | 10-bit | Decode | 4K@30fps   | h264_qsv ⭐    |
| i5-1135G7   | Iris Xe     | ✅  | ✅    | 8K    | 10-bit | Decode | 4K@45fps   | ⭐⭐           |
| i7-1165G7   | Iris Xe Max | ✅  | ✅    | 8K    | 10-bit | Decode | 4K@60fps   | ⭐⭐⭐          |

11th Gen = erster "moderne" iGPU – HEVC 10-bit + 4K RT!

### 2. Vollständige Matrix (Intel + AMD + Nvidia)

| Typ        | Modell      | Encoder    | 4K FPS | CPU   | AV1 Enc | Linux   | Preis |
|------------|-------------|------------|--------|-------|---------|---------|-------|
| Arc        | A770        | vaapi      | 60     | 5%    | ✅      | ⭐⭐⭐⭐⭐  | €350  |
| Intel 14th | i9-14900K   | qsv        | 45     | 8%    | ✅      | ⭐⭐⭐⭐⭐  | €550  |
| Intel 11th | i7-1165G7   | qsv        | 35     | 10%   | Decode  | ⭐⭐⭐⭐   | €300 (gebraucht) |
| Intel 7th  | i5-7200U    | qsv        | 18     | 15%   | ❌      | ⭐⭐⭐    | €80   |
| AMD Zen4   | Ryzen 8700G | vaapi      | 50     | 7%    | Decode  | ⭐⭐⭐⭐   | €350  |
| Nvidia     | RTX 4060    | nvenc      | 70     | 3%    | ✅      | ⭐⭐⭐⭐   | €300  |
| CPU        | i9-14900K   | libx264    | 3      | 180%  | ❌      | ⭐⭐⭐⭐⭐  | €600  |

### 3. 11th Gen Performance (Iris Xe)

i7-1165G7 Iris Xe:
- H.264: 4K@60fps (25x RT)
- HEVC 10-bit: 4K@45fps (18x RT)
- CPU-Last: 10–15%
- AV1 Decode: ✅ (kein Encode)
- FFmpeg: -hwaccel qsv -c:v h264_qsv medium

11th Gen = perfekter Einstieg (vor Arc)!

### 4. Budget-Matrix inkl. 11th Gen

| € Budget | Beste Wahl           | 4K FPS | Features    |
|----------|----------------------|--------|-------------|
| €100     | Intel N100           | 1080p  | NAS         |
| €200     | i7-1165G7 (gebraucht)| 4K@45  | ⭐ Sweet-Spot|
| €350     | Arc A770             | 8K@60  | AV1 Pro     |
| €400     | Ryzen 8700G          | 4K@120 | RDNA3       |

### 5. Dein Router (11th Gen erkannt)
```python
def detect_cpu_gen():
    cpuinfo = open('/proc/cpuinfo').read()
    if '11th Gen' in cpuinfo or 'Tiger Lake' in cpuinfo:
        return ('qsv_11thgen', 'Iris Xe ⭐⭐⭐⭐')
    # ... rest wie vorher
```

11th Gen Iris Xe = Upgrade von UHD 610/620 → 4K@45fps! 🎥✨

**Deine CPU? → exakte Position in Matrix! 🚀**
