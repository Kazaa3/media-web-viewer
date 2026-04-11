# Logbuch: Feature – Streaming von lokal, später SMB/NFS

**Datum:** 13.03.2026
**Autor:** Copilot

## Kontext
Im Rahmen der Weiterentwicklung des Media Web Viewer wurde das Streaming-Feature zunächst für lokale Medienquellen implementiert. In einer späteren Ausbaustufe ist die Unterstützung für Netzwerkfreigaben (SMB/NFS) geplant.

## Phase 1: Streaming von lokalen Quellen
- Direkter Zugriff und Streaming von Dateien auf lokalen Festplatten und angeschlossenen Laufwerken
- Optimiert für schnelle Wiedergabe und minimale Latenz
- Keine Netzwerkabhängigkeit, ideal für Einzelplatz- und Desktop-Nutzung

## Phase 2: Streaming von SMB/NFS
- Geplante Erweiterung für Netzwerkfreigaben (Windows SMB, Linux NFS)
- Zugriff auf Medien im LAN, Unterstützung für Home-Server und NAS
- Zusätzliche Authentifizierung und Netzwerkmanagement erforderlich

## Motivation
- Flexibilität für verschiedene Nutzungsszenarien (lokal, Netzwerk, gemischt)
- Zukunftssichere Architektur für Medienwiedergabe im Heimnetzwerk

## Technische Überlegungen
- Backend: Abstraktionsschicht für Dateizugriff (lokal vs. remote)
- Performance- und Latenzoptimierung für beide Modi
- UI: Auswahl und Verwaltung von lokalen und Netzwerkquellen

## Nächste Schritte
- Stabilisierung des lokalen Streamings
- Konzept und Prototyp für SMB/NFS-Integration
- Authentifizierungs- und Verbindungsmanagement
- Tests und User-Feedback

---

**Fazit:**
Das Streaming-Feature startet mit lokalem Zugriff und wird perspektivisch um SMB/NFS erweitert, um maximale Flexibilität und Kompatibilität für verschiedene Medienumgebungen zu bieten.
