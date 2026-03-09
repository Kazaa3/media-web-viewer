<!-- Category: ROADMAP -->
<!-- Status: PLANNED -->

# Meilenstein 4 – Plattform- und Release-Qualität

## Ziel
Meilenstein 4 fokussiert die Produktionsreife: reproduzierbare Builds, robuste Release-Pipelines, stabile Laufzeitumgebungen und klare Betriebsprozesse.

## Scope (geplant)
- Vereinheitlichung des Build-/Packaging-Prozesses für lokale und CI-Ausführung
- Verlässliche Versionierung und Artefakt-Nachvollziehbarkeit pro Release
- Verbesserte Install-/Update-Validierung (inkl. Debian-Paket-Flow)
- Härtung der Runtime-Umgebung (Abhängigkeiten, Startverhalten, Fallbacks)
- Klare Release-Checklisten und Rollback-fähige Abläufe

## Abgrenzung
Nicht Teil von M4:
- Große UI-Neuentwicklung (M3)
- Neue datenmodellzentrierte Produktfeatures ohne Release-/Betriebsbezug
- Experimentelle Infrastruktur-Themen ohne direkten Delivery-Nutzen

## Technische Leitlinien
- Build und Release müssen lokal und in CI konsistent reproduzierbar sein
- Versionseinträge bleiben über alle Zielorte synchronisiert
- Fehlerfälle im Packaging/Startup werden früh validiert und dokumentiert
- Änderungen priorisieren Wartbarkeit und Debugbarkeit statt kurzfristiger Workarounds

## Deliverables
- Konsolidierter, dokumentierter Build- und Release-Workflow
- Validierte Paket-Metadaten und Installationspfade
- Erweiterte Release-Gates (Tests, Versionskonsistenz, Artefakt-Prüfungen)
- Betriebsdoku für Hotfix-/Rollback-Szenarien

## Akzeptanzkriterien
- Release kann von sauberem Checkout reproduzierbar gebaut werden
- Versionsstände sind an allen definierten Sync-Positionen konsistent
- Kritische Build-/Install-Pfade sind automatisiert getestet
- Release-Dokumentation deckt Build, Validierung und Rollback vollständig ab

## Status
- Stand 2026-03-09: **PLANNED**
- Umsetzung nach M3-Umsetzung und M2-Stabilisierung
