# Logbuch: Feature – Low Bandwidth / Heavy-Mode

**Datum:** 13.03.2026
**Autor:** Copilot

## Kontext
Für den Media Web Viewer wird ein adaptiver Modus entwickelt, der sich dynamisch an die verfügbare Bandbreite (QoS) und die Backend-Fähigkeiten anpasst. Ziel ist es, sowohl bei schwachen als auch bei leistungsfähigen Verbindungen optimale Nutzererfahrung zu bieten.

## Feature-Design
- **Low Bandwidth Mode:**
  - Reduzierte Bitrate, Auflösung oder Qualität bei Streaming
  - Adaptive Auswahl von Formaten und Transcoding-Profilen
  - Automatische Umschaltung bei schlechter Verbindung (QoS-Check)
- **Heavy-Mode:**
  - Volle Qualität, High-Bitrate, alle Features aktiv
  - Aktiviert bei starker Verbindung und leistungsfähigem Backend
  - Ermöglicht z.B. Gapless Playback, High-Res Audio, große Videodateien

## Motivation
- Optimale Medienwiedergabe unabhängig von Netzwerk und Hardware
- Vermeidung von Buffering, Abbrüchen und Qualitätsverlusten
- Zukunftssichere Architektur für mobile, Desktop- und Heimnetzwerke

## Technische Überlegungen
- QoS-Detection: Bandbreitenmessung, Latenz, Paketverlust
- Backend-Check: CPU, RAM, Transcoding-Fähigkeit
- Dynamische Umschaltung und User-Feedback im UI
- Konfigurierbare Schwellenwerte und Profile

## Nächste Schritte
- Implementierung der QoS- und Backend-Checks
- Entwicklung adaptiver Streaming- und Transcoding-Profile
- UI-Integration für Modus-Anzeige und Umschaltung
- Tests unter verschiedenen Netzwerkbedingungen

---

**Fazit:**
Der Low Bandwidth / Heavy-Mode sorgt für eine flexible, adaptive Medienwiedergabe und passt sich intelligent an die jeweilige System- und Netzwerksituation an.
