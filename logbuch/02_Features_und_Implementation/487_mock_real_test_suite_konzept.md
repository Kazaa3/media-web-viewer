# Konzept: Test-Suite für Mock- und Realdateien

**Datum:** 15.03.2026

## Ziel
- Aufbau einer umfassenden Test-Suite, die sowohl mit Mock-Dateien (synthetisch, minimal) als auch mit echten Mediendateien (real-world samples) arbeitet.

## Aufbau
- **Mock-Dateien:**
  - Kleine, gezielt erzeugte Testdateien (z. B. leere MP3, Dummy-MP4, Mini-ISOs), die bestimmte Randfälle und Fehlerbedingungen abdecken.
  - Vorteil: Schnell, portabel, keine Copyright-Probleme.
- **Realdateien:**
  - Echte Medienbeispiele (z. B. Musikstücke, Videos, ISOs), die typische und komplexe Metadaten enthalten.
  - Vorteil: Testet das System unter realistischen Bedingungen und deckt Parser-/Codec-Probleme auf.

## Test-Suite-Strategie
- Gemeinsames Test-Framework (z. B. pytest, unittest) für beide Dateitypen.
- Trennung der Testfälle in:
  - `tests/unit/mock/` für reine Mock-Tests
  - `tests/integration/real/` für Realdateien
- Automatisierte Checks:
  - Erkennung, Import und Metadaten-Parsing für alle unterstützten Formate
  - Fehlerbehandlung bei ungültigen oder inkompatiblen Dateien
  - UI-Integration: Sichtbarkeit und Abspielbarkeit in der App

## Logbuch-Notiz
- Die Test-Suite wird iterativ aufgebaut und erweitert.
- Mock- und Realdateien werden klar getrennt, um schnelle Unit-Tests und realistische Integrations-Tests zu ermöglichen.
- Ziel: Maximale Testabdeckung und robuste Medienverarbeitung.
