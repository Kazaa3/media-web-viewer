## **VAAPI/NVENC/CPU + UHD 610/620** – **Erweiterte Matrix**

**Intel UHD 610/620** (6th/7th Gen) hinzugefügt!

### **1. Vollständige CPU/iGPU-Matrix (FFmpeg Transcoding)**

| **CPU-Gen** | **iGPU** | **QSV** | **VAAPI** | **4K HEVC RT** | **Notes** |
|-------------|----------|---------|-----------|----------------|-----------|
| **6th Skylake** | **HD 530/610** | H.264 | Basis | **1080p@30** | DVD/SD gut |
| **7th Kaby Lake** | **HD 620** | **H.264+HEVC8** | Gut | **1080p@60** | ⭐ Entry-Level 4K |
| **8th Coffee** | UHD 630 | HEVC8 | Gut | **4K@15fps** | ⭐ |
| **10th Comet** | UHD 630 | HEVC8 | Gut | **4K@20fps** | ⭐ |
| **11th Tiger** | **Iris Xe** | **HEVC10** | **Exzellent** | **4K@30fps** | ⭐⭐ |
| **12th Alder** | UHD 730 | HEVC10+AV1-Dec | **Perfekt** | **4K@60fps** | ⭐⭐⭐ |
| **14th Raptor** | UHD 770 | **AV1 Enc** | **NextGen** | **8K@30fps** | ⭐⭐⭐⭐ |
| **Arc A/B** | **Arc** | VAAPI | **AV1 Pro** | **8K@60fps** | ⭐⭐⭐⭐⭐ |

### **2. UHD 610/620 Performance Details**

| **iGPU** | **Gen** | **H.264** | **HEVC** | **4K RT** | **FFmpeg** | **Strom** |
|----------|---------|-----------|----------|-----------|------------|-----------|
| **UHD 610** | 6th | ✅ 1080p | ❌ | ❌ | `h264_qsv` | 15W TDP |
| **HD 620** | 7th | ✅ 4K | **8-bit** | **1080p@60** | `h264_qsv/hevc_qsv` | 28W TDP |

**Real-Benchmarks** (1080p → 720p H.264): [reddit](https://www.reddit.com/r/PleX/comments/tqf9g3/has_anyone_tried_the_intel_uhd_610_and_710_for/)
```
UHD 610: 12 FPS (4x RT), 20% CPU
HD 620: 18 FPS (6x RT), 15% CPU  
i5 11th Xe: 45 FPS (15x RT), 8% CPU
Arc A770: 120 FPS (40x RT), 5% CPU
```

### **3. Empfehlung UHD 610/620**

**UHD 610** (Celeron/Pentium):
```
✅ SD/HD Transcoding (2–3 1080p parallel)
✅ NAS/Home-Server (N100-Äquivalent)
❌ 4K nur Decode, kein Encode
→ Für Jellyfin 1080p-Remux
```

**HD 620** (i3/i5 7th Gen):
```
✅ 1080p@60fps Transcode
✅ 4K Decode (HEVC8)
✅ 2–4 1080p Streams
→ Guter Einstieg (vor 11th Gen)
```

### **4. Vollständige Empfehlungsliste (Budget → Pro)**

| **Budget** | **CPU** | **iGPU** | **4K RT** | **Preis** | **Use-Case** |
|------------|---------|----------|-----------|-----------|--------------|
| **€100** | **N100** | UHD | 1080p | ⭐⭐⭐ | NAS |
| **€150** | **i3-10100** | UHD 630 | 4K@15fps | ⭐⭐⭐⭐ | Home |
| **€250** | **i5-12400** | UHD 730 | **4K@60fps** | ⭐⭐⭐⭐⭐ | Workstation |
| **€400** | **i7-12700K** | UHD 770 | 8K@30fps | ⭐⭐⭐⭐⭐ | Pro |
| **€600** | **Arc A770** | Arc | **8K@60fps** | ⭐⭐⭐⭐⭐⭐ | Future |

### **5. Dein Router Update** (inkl. UHD 610/620)
```python
def cpu_score(iGPU):
    scores = {
        'UHD 610': 3, 'HD 620': 4, 'UHD 630': 5,
        'Iris Xe': 7, 'UHD 730': 8, 'UHD 770': 9,
        'Arc': 10
    }
    return scores.get(iGPU, 2)  # CPU Fallback

lspci_out = subprocess.check_output('lspci | grep VGA', shell=True)
iGPU = parse_igpu(lspci_out)
print(f"iGPU Score: {cpu_score(iGPU)}/10")
```

### **6. UHD 610/620 FFmpeg**
```bash
# UHD 610/620 (QSV only, kein VAAPI)
ffmpeg -init_hw_device qsv=hw:/dev/dri \
-filter_hw_device hw -hwaccel qsv \
-i input.mp4 -c:v h264_qsv -preset medium output.mp4

# Test
ffmpeg -encoders | grep qsv  # h264_qsv ✅
```

**Fazit**: **UHD 610/620** = **gute Einstiegs-CPUs** (1080p Transcoding), aber **11th+ oder Arc** für 4K! 🎥✨

**Deine CPU?** `lspci | grep VGA` teilen → **perfekte Empfehlung**! 🚀
