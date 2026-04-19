# Logbuch Eintrag 025: Codec-Kompatibilität und Priority-Routing (V1.36)

## Datum: 2026-03-18
## Status: VERIFIED / OPTIMIZED

### Analyse der Wiedergabe-Prioritäten (Smart-Router)
Nach der Härtung für DVD-Images wurde die Priorisierung für Standardformate (MKV/MP4) feinjustiert, um maximale Qualität im Browser ("Embedded") zu gewährleisten und gleichzeitig robuste Fallbacks für inkompatible Codecs zu bieten.

### Hierarchie-Verifizierung (`test_playback_priority_routing.py`)
Die automatisierten Tests bestätigen nun folgende Kette:
1.  **Direktwiedergabe (Native)**: MP4-Dateien (H264/AAC) verwenden direkt den Native-Pfad (`chrome_direct`).
2.  **MKV-Spezialist (Remux)**: Standard-MKVs nutzen jetzt prioritär das **MKVMerge PIPE-KIT** (`chrome_remux`), sofern mkvtoolnix installiert ist. Dies bietet die beste Bildqualität ohne Transcodierung.
3.  **On-the-fly Fallback (FragMP4)**: Unbekannte oder inkompatible Codecs (z.B. HEVC in Chromium) nutzen FFmpeg-Transmuxing (`chrome_fragmp4`).
4.  **Hard-Fallback (VLC Guard)**: Legacy-Formate (`MPEG-2 PAL` / `4 Könige DVD-Objekt`) werden explizit vom Browser-Routing ausgeschlossen und an den gesicherten VLC-Einzelinstanz-Prozess übergeben.

### Fehlerbehebung: "MKV starten nicht"
Ein Logikfehler in der `auto`-Auflösung von `open_video` wurde behoben. Der Status "Invalid config: auto/auto" wurde durch eine korrekte Auflösung in den jeweils optimalen Chrome-Mode ersetzt.

### System-Stabilität
- **Singleton-Garantie**: `pkill` bereinigt nun zuverlässig verwaiste X-Server-Instanzen von VLC (siehe Logbuch 024).
- **Embedded-Player**: Der `video-placeholder` zeigt nun zuverlässig den korrekten Status an, wenn auf VLC gewechselt wird.

Status: **FINALIZED**
