# Testabdeckung & Coverage

## Ziel
Die Testabdeckung dokumentiert, welche Bereiche des Projekts durch automatisierte Tests abgedeckt sind und wo Lücken bestehen.

## Bereiche
- Backend: API, Datenbank, Parser, Logging
- Frontend: UI-Komponenten, Eel-Kommunikation, WebSocket, Session
- Medien: Audio, Video, Playlist, Transcoding, Cover-Art
- Infrastruktur: Build, CI/CD, Deployment
- Spezial: Langlaufende Tests (ISO, DVD, Blu-ray), Selenium/UI

## Testgruppen
- basic: Kernfunktionalität, Smoke-Tests
- tech: Technologie-spezifisch (FFmpeg, VLC, Mutagen)
- advanced: Komplexe Szenarien, Integration, Performance
- category: Nach Funktion/Kategorie (Audio, Video, UI, DB)
- iso: Medien-ISO, DVD, Blu-ray

## Coverage-Matrix (Beispiel)
| Bereich         | Testgruppe   | Abdeckung (%) | Bemerkung           |
|-----------------|-------------|--------------|---------------------|
| Backend/API     | basic, tech | 85           | Fast alle Endpunkte |
| Frontend/UI     | selenium    | 70           | UI-Komponenten      |
| Parser         | tech        | 90           | Medienformate       |
| DB             | basic, adv  | 80           | SQLite, Migration   |
| ISO/DVD/Blu-ray| iso         | 60           | Langlaufende Tests  |

## Lücken & Empfehlungen
- UI-Tests (Selenium) ausbauen
- Langlaufende Tests (ISO) optimieren
- Testdaten-Handling verbessern (siehe Teststruktur_Gruppierung.md)
- Coverage regelmäßig reporten (z.B. pytest-cov, CI/CD)

---

**Letzte Änderung:** 12. März 2026
