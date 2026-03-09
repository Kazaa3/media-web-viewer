<!-- Category: ROADMAP -->
<!-- Status: PLANNED -->

# Meilenstein 3 – New GUI

## Ziel
Meilenstein 3 modernisiert die Oberfläche des Media Web Viewer und trennt UI-/UX-Themen klar von der Daten- und Backend-Logik aus M2.

## Scope (geplant)
- Überarbeitung der Hauptnavigation (klarere Informationsarchitektur)
- Einheitliches Komponenten-Layout für Listen, Details und Aktionen
- Verbesserte Discoverability für Medien-Metadaten und Releases
- Saubere Zustandsanzeige für laufende Prozesse (Scans, Tests, Parsing)
- Konsistente i18n-Integration in neuen/überarbeiteten UI-Bereichen

## Abgrenzung
Nicht Teil von M3:
- Neue Datenmodelle als Primärziel (gehört zu M2/M4 je nach Feature)
- Release-/Packaging-Themen ohne direkten UI-Bezug
- Große Infrastruktur-Refactorings ohne sichtbaren UX-Mehrwert

## Technische Leitlinien
- UI-Änderungen bleiben kompatibel zum bestehenden Python/Eel-Backend
- Bestehende Endpunkte werden bevorzugt weiterverwendet statt neu erfunden
- Schrittweise Migration statt Big-Bang-Rewrite
- Regressionen werden mit zielgerichteten UI-/Integrations-Tests abgesichert

## Deliverables
- Überarbeitete GUI-Struktur in `web/app.html` (inkrementell)
- Aktualisierte zugehörige UI-Logik in Frontend-Skripten
- Dokumentierte UX-Entscheidungen und Navigation
- Testabdeckung für kritische UI-Flows

## Akzeptanzkriterien
- Kern-Workflows (Abspielen, Navigieren, Suchen/Filtern, Test-Tab-Aufruf) sind ohne UX-Brüche nutzbar
- Keine Regression in Session-Stabilität und Single-Window-Verhalten
- Sichtbare Konsistenz der UI-Komponenten über die Hauptansichten
- Änderungen sind im Logbuch und in der Hauptdokumentation nachgeführt

## Status
- Stand 2026-03-09: **PLANNED**
- Umsetzung startet nach Stabilisierung/Abnahme der M2-Datenbasis
