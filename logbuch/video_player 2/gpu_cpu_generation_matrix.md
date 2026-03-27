# VAAPI/NVENC/CPU + CPU-Generationen – Vollständige Matrix (März 2026)

**Intel Onboard/Arc/AMD/Nvidia + CPU-Gen-Performance für FFmpeg**

---

## 1. GPU + CPU-Generations-Matrix
| CPU-Gen                | iGPU         | QSV         | VAAPI      | 4K HEVC RT   | Arc     | AMD      | NVENC      |
|------------------------|--------------|-------------|------------|--------------|---------|----------|------------|
| 6th Skylake (2015)     | HD 530       | H.264       | Basis      | ❌           | -       | VCE 3.0  | GTX 900    |
| 8th Coffee Lake (2017) | UHD 630      | H.264+HEVC  | Gut        | 1080p        | -       | VCN 1.0  | GTX 16     |
| 10th Comet Lake (2019) | UHD 630      | HEVC 8-bit  | Gut        | 4K@15fps     | -       | VCN 2.0  | RTX 20     |
| 11th Tiger Lake (2020) | Iris Xe      | HEVC 10-bit | Sehr gut   | 4K@30fps     | A30M    | RDNA 2   | RTX 30     |
| 12th Alder Lake (2021) | UHD 730/Xe   | HEVC10+AV1D | Exzellent  | 4K@60fps     | A370M   | RDNA 3   | RTX 40     |
| 13th/14th Raptor (22/23)| UHD 770/Xe  | AV1 Encode  | Perfekt    | 8K@30fps     | A770    | RDNA 3   | RTX 40xx   |
| 15th Arrow Lake (2025) | Battlemage   | AV1 Pro     | NextGen    | 8K@60fps     | B580    | RDNA 4   | RTX 50     |

---

## 2. FFmpeg Performance (4K HEVC → H.264)
| Hardware    | Encoder      | FPS   | CPU-Last | VRAM   | AV1? |
|-------------|--------------|-------|----------|--------|------|
| Arc A770    | h264_vaapi   | 35    | 6%       | 2GB    | ✅   |
| i7-12700K   | h264_qsv     | 22    | 12%      | 300MB  | ❌   |
| RTX 3060    | h264_nvenc   | 45    | 4%       | 1GB    | ✅   |
| RX 6700 XT  | h264_amf     | 25    | 10%      | 1.5GB  | ❌   |
| i9-13900K   | libx264      | 2     | 180%     | 0      | ❌   |

---

## 3. Generationen-Entwicklung (Intel QSV)
- 6th Gen (Skylake 2015): H.264 nur → 1080p SD
- 8th Gen (Coffee 2017): +HEVC 8-bit → 4K@15fps
- 11th Gen (Tiger 2020): Iris Xe + HEVC10 → 4K@30fps ⭐
- 12th Gen (Alder 2021): AV1 Decode → 4K@60fps
- 14th Gen (Raptor 2023): AV1 Encode → 8K@30fps
- Arc (2022+): AV1 Pro + XeSS → 8K RT ⭐⭐⭐

---

## 4. Dein Auto-Detect + Router
```python
def detect_full_encoder():
    # 1. Arc VAAPI (Top)
    if os.system('vainfo | grep -q "VAProfileAV1Main"') == 0:
        return ('vaapi', '/dev/dri/renderD128', 'Arc AV1 ⭐')
    # 2. Intel iGPU QSV (11th+)
    if os.system('ffmpeg -encoders | grep -q "h264_qsv"') == 0:
        cpuinfo = open('/proc/cpuinfo').read()
        gen = next((l for l in cpuinfo.splitlines() if 'model name' in l), '').lower()
        if '11th' in gen or '12th' in gen or '13th' in gen:
            return ('qsv', '/dev/dri/renderD128', 'iGPU 11th+ ⭐')
        return ('qsv', None, 'iGPU älter')
    # 3. Nvidia
    if os.system('nvidia-smi >/dev/null 2>&1') == 0:
        return ('nvenc', None, 'RTX ⭐⭐')
    # 4. AMD
    if os.system('vainfo | grep -q "VAProfileH264"') == 0:
        return ('vaapi', '/dev/dri/renderD128', 'AMD')
    return ('libx264', None, 'CPU Fallback')

encoder, device, label = detect_full_encoder()
print(f"🎯 {label}: {encoder}")
```

---

## 5. FFmpeg Commands pro Generation
- **Arc (VAAPI):**
  ```bash
  ffmpeg -vaapi_device /dev/dri/renderD128 -hwaccel vaapi -i input -c:v h264_vaapi
  ```
- **i7 11th+ (QSV):**
  ```bash
  ffmpeg -init_hw_device qsv=hw:/dev/dri -filter_hw_device hw -i input -c:v h264_qsv
  ```
- **RTX (NVENC):**
  ```bash
  ffmpeg -hwaccel nvenc -i input -c:v h264_nvenc
  ```
- **CPU (Fallback):**
  ```bash
  ffmpeg -i input -c:v libx264 -preset fast
  ```

---

## 6. Empfehlung für dein Router
1. Arc VAAPI → 35 FPS 4K, AV1, Linux-nativ ⭐⭐⭐⭐⭐
2. i7 11th+ QSV → 22 FPS 4K, stabil ⭐⭐⭐⭐
3. RTX NVENC → 45 FPS, proprietär ⭐⭐⭐⭐
4. CPU x264 → Qualität, langsam ⭐⭐⭐

**Dein Arc = Generationensieger (AV1 + 35 FPS)! Router auto-detect → perfekte Anpassung! 🎥✨**

> Test: `vainfo` → Arc erkannt? 🚀
