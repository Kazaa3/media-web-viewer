# Digitale HiFi-Formate: Qobuz, Tidal, Streaming & Download
**Datum:** 12. März 2026


### 1. Streaming-Dienste (Qobuz, Tidal, Deezer, Apple Music)
## Digitale Audio-Kauf-Formate: Hi-Res & DSD

- Moderne Download-Portale (Qobuz, HDtracks, Bandcamp, NativeDSD) bieten folgende Formate zum Kauf:
	- FLAC: 24-bit/44.1 kHz bis 24-bit/384 kHz
	- WAV, AIFF: bis 32-bit/384 kHz
	- ALAC: bis 24-bit/192 kHz
	- DSD (DSF, DFF): DSD64, DSD128, DSD256 (je nach Album)
- Alle Formate sind DRM-frei und können direkt archiviert und abgespielt werden.
- Hi-Res-Downloads sind ideal für langfristige Archivierung und maximale Klangqualität.
- Lossless Streaming: FLAC (Qobuz, Tidal HiFi), ALAC (Apple Music), WAV
- HiRes Audio: bis 24-bit/192 kHz (Qobuz, Tidal Masters/MQA)
- Proprietäre Formate: MQA (Tidal Masters), AAC (Apple Music, Deezer)
- DRM: Meist verschlüsselt, nicht direkt als Datei speicherbar

### 2. Download-Portale (Qobuz, HDtracks, Bandcamp)
- Lossless Downloads: FLAC, ALAC, WAV, AIFF, DSD
- HiRes Audio: bis 24-bit/384 kHz, DSD64/DSD128
- Metadaten: Album, Künstler, Cover, Genre, ISRC, oft umfangreicher als bei physischen Medien

### 3. Playability & Integration
- Medienbibliothek kann gekaufte Downloads (FLAC, WAV, DSD) direkt indexieren und abspielen
- Streaming-Links können als Metadaten gespeichert werden, aber nicht direkt abgespielt (DRM)
- UI zeigt HiRes- und Streaming-Formate mit Premium-Label

---

## Archivierungs-Hinweis
- Für maximale Kompatibilität empfiehlt sich die Nutzung und Archivierung offener Formate (FLAC, WAV, ALAC)
- Proprietäre Formate (MQA, DRM-geschützte Streams) sind langfristig riskant

---

*Entry created: 12. März 2026*
---

## Phase 7: Comprehensive CD/DVD Standards (Rainbow Books & DVD Books)
**Datum:** 12. März 2026

- Implementierung und Verifizierung von Phase 7: Unterstützung aller wichtigen optischen Medienstandards (Rainbow Books & DVD Books).
- Unterstützte Standards:
	- Rainbow Books: VCD (White Book), SVCD, CD-i (Green Book), Photo CD (Beige Book), CD-Extra (Blue Book)
	- DVD Standards: DVD-Audio, DVD-VR (Video Recording)
- Logik:
	- VCD, SVCD, DVD-VR und DVD-Audio werden als "playable" markiert.
	- Photo CD und CD-i werden als "Index-Only" eingestuft (gemäß Vorgabe für Datenträger).
- Die Erkennung und Filterung erfolgt über pycdlib und die aktualisierte detect_file_format-Logik.
- Alle Formate wurden erfolgreich mit dem Verifikationsskript /tmp/verify_phase_7.py validiert.
- Walkthrough und Task-Artefakte zu Phase 1-7 sind aktualisiert und dokumentiert.

*Entry created: 12. März 2026*
---
