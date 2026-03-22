# Logbuch: Session-Management & Automatisierung

## Zweck
Dokumentiert die Möglichkeiten und Best Practices zur Session-Verwaltung und Automatisierung in Media Web Viewer, inkl. Batch-Remux-Tools und User-State-Handling.

---

## Batch-Remux Automatisierung
- **Tdarr (Docker, Synology):** Automatisiertes Scannen und Remuxen von Medien (HEVC-Optimierung) auf NAS.
- **Handbrake (pyhandbrake):** GUI/CLI-Remux, manuell oder skriptgesteuert.
- **MKVToolNix:** Für Batch-Remux via CLI oder UI.
- **GitHub mkv2mp4/mkv2mp4ui:** Einfache Skriptlösungen für Stapelverarbeitung.

**Empfehlung:** Tdarr für große, automatisierte Workflows; MKVToolNix/Handbrake für manuelle Jobs.
