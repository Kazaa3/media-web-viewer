# Logbuch: Direct Play Modus & Fallback-Strategie

## Datum
16. März 2026

---

## Konzept: Direct Play
- **Definition:** Server sendet Originaldatei unverändert (kein Remux/Transcode), nur Container/Wrapper ggf. angepasst.
- **Vorteile:**
  - CPU-frei (<1% Last)
  - Sofortiges Seeking (HTTP Range-Requests)
  - Perfekt für kompatible Formate (MP4/WebM, H.264/AAC/VP9)
- **Ablauf:**
  1. Client prüft Kompatibilität (ffprobe, Datei-Header)
  2. Server liefert Datei via HTTP Range (progressiver Download)
  3. Keine Verarbeitung am Server, Client dekodiert selbst

---

## Implementierung
- **Kompatibilitätsprüfung (Python):**
  - ffprobe prüft Codec und Container
  - Nur MP4/WebM (ggf. MKV) und H.264/AAC/VP9 erlaubt
- **Bottle-Route:**
  - /direct/<fname> liefert Datei mit Range- und Cache-Headern
  - Fallback: "Nicht kompatibel – Remux nötig"
- **Eel Frontend:**
  - Modus "Direct Play" prüft Kompatibilität, setzt player.src auf /direct/<file>
  - Bei Inkompatibilität: Hinweis + Remux-Trigger

---

## Vergleich zu anderen Modi
| Modus         | CPU-Last | Seeking | Kompatibilität | Beispiel              |
|--------------|----------|---------|----------------|-----------------------|
| Direct Play  | 0%       | Sofort  | MP4/H.264      | /direct/movie.mp4     |
| cvlc         | 5–10%    | 2–5s    | Alle           | TS-Stream             |
| MediaMTX HLS | 2–5%     | 1–3s    | Alle           | .m3u8                 |
| Remux        | Einmalig | Sofort  | Nach Remux     | MP4                   |

- **ISO:** Nicht möglich (Browser versteht nicht) → MakeMKV/MKV → Remux prüfen
- **MKV:** Oft ja (H.264), sonst 2s Buffering beim Seek
- **Auto-Fallback:** Modus prüft → Direct oder Remux/MediaMTX

---

## Empfehlung
- Direct Play als bevorzugter Modus implementieren
- Fallback zu MediaMTX/Remux bei Inkompatibilität
- ffprobe-Integration für automatische Prüfung
- Test: ffprobe movie.mp4 → H.264? → Direct Play go!

---

## Kommentar
Ctrl+Alt+M

---

*Siehe vorherige Logbuch-Einträge für Backend- und Streaming-Details.*
