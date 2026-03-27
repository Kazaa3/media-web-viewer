## **Empfohlene CPUs für FFmpeg + VAAPI** (Linux 2026)

**Für dein Media-Library-Projekt** – **Transcoding/Streaming** mit **VAAPI/QSV** (4K RT, niedrige CPU).

### **🏆 TOP 5 CPUs (März 2026)**

| **Rang** | **CPU** | **iGPU** | **VAAPI RT (4K)** | **Preis** | **Warum?** |
|----------|---------|----------|-------------------|-----------|------------|
| **1** | **i9-14900K** | **UHD 770** | **8K@30fps** | €550 | **QSV AV1 Encode**, 24 Kerne, Workstation |
| **2** | **i7-14700K** | **UHD 770** | **4K@120fps** | €420 | **QSV Pro**, 20 Kerne, Sweet-Spot |
| **3** | **i5-14600K** | **UHD 730** | **4K@60fps** | €320 | **VAAPI Exzellent**, 14 Kerne, Budget-King |
| **4** | **N100** (NAS) | **UHD** | **1080p@60fps** | €120 | **VAAPI NAS**, 24/7, Jellyfin-ready |
| **5** | **Arc A380 + i3** | **Arc** | **8K@30fps** | €250+€100 | **VAAPI AV1**, dedizierte GPU |

### **2. Generationen-Matrix** (Intel QSV/VAAPI)

| **Gen** | **Jahr** | **iGPU** | **H.264** | **HEVC** | **AV1 Decode** | **AV1 Encode** | **4K RT** |
|---------|----------|----------|-----------|----------|----------------|---------------|-----------|
| **8th** | 2017 | UHD 630 | ✅ | 8-bit | ❌ | ❌ | 1080p |
| **11th** | 2020 | **Iris Xe** | ✅ | **10-bit** | ✅ | ❌ | **4K@30** ⭐ |
| **12th** | 2021 | UHD 730 | ✅ | 10-bit | ✅ | ❌ | 4K@60 |
| **13th/14th** | 2022/23 | UHD 770 | ✅ | 10-bit | ✅ | **✅** | **8K@30** ⭐⭐ |
| **Arc A/B** | 2022/25 | **Arc** | ✅ | 10-bit | **✅** | **✅** | **8K@60** ⭐⭐⭐ |

### **3. Performance-Charts** (4K HEVC → H.264)

```
CPU Transcode (x264):     1–3 FPS (150% CPU)
i5 11th Gen (Iris Xe):  20 FPS (12% CPU)
i7 14th Gen (UHD 770): **45 FPS (8% CPU)**
Arc A770:              **60 FPS (5% CPU)** ⭐
```

### **4. Deine Empfehlungen (Budget → High-End)**

**🏠 NAS/Home-Server**:
```
1. Intel N100/N305 (€120) → VAAPI 1080p, 24/7
2. i3-12100 (€150) → QSV 4K, Office-PC
```

**💻 Workstation**:
```
1. i5-14600K (€320) → 4K@60fps, Gaming
2. i7-14700K (€420) → 8K@30fps, Content
```

**⚡ High-End**:
```
1. i9-14900KS (€650) → 8K@60fps, Pro
2. Arc A770 + i5 (€400) → AV1 Monster
```

### **5. Linux MX Setup (Alle CPUs)**

```bash
# Gemeinsam
sudo apt install intel-media-va-driver-non-free vainfo libmfx1

# Arc-spezifisch
sudo apt install mesa-va-drivers-mesa-va-drivers

# Test
ffmpeg -hwaccels  # vaapi qsv ✅
vainfo  # 20+ Profile
```

### **6. Auto-Detect für Multi-CPU**
```python
def recommend_cpu(info):
    if info['resolution'] == '4K':
        return 'i7-14700K (45 FPS) or Arc A770 (60 FPS)'
    return 'i5-14600K (20 FPS) or N100 (NAS)'

print(recommend_cpu({'resolution': '4K', 'use_case': 'streaming'}))
# → "i7-14700K (45 FPS) or Arc A770 (60 FPS)"
```

### **7. Preis/Leistung 2026**
```
⭐⭐⭐⭐⭐ i5-14600K: 4K@60fps → €320 → BEST VALUE
⭐⭐⭐⭐⭐ Arc A770: 8K@60fps → €350 → FUTURE-PROOF
⭐⭐⭐⭐  N100: 1080p NAS → €120 → 24/7 Budget
```

**Für dein Projekt**: **i5-14600K + Arc A770 Combo** → **unbesiegbar** (VAAPI + AV1 + 8K RT)! 🎥✨

**Welche Budget-Klasse**? 🚀
