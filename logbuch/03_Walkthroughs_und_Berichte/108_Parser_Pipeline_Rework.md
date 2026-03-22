<!-- Category: architecture -->
<!-- Title_DE: Parser Pipeline Rework -->
<!-- Title_EN: Parser Pipeline Rework -->
<!-- Summary_DE: Geplante Überarbeitung der Parser-Pipeline für Robustheit, Priorisierung und bessere Fehlertoleranz -->
<!-- Summary_EN: Planned parser pipeline redesign for robustness, prioritization, and better fault tolerance -->
<!-- Status: planned -->
<!-- Date: 2026-03-09 -->

# Parser Pipeline Rework

## Ziel
Die bestehende Metadaten-Verarbeitung soll von einer rein sequentiellen Kette zu einer robusten, priorisierten Pipeline weiterentwickelt werden.

## Problemstellung
- Unterschiedliche Quellen liefern teils widersprüchliche oder unvollständige Metadaten.
- Einzelne Parser-Fehler können den Gesamtfluss unnötig beeinträchtigen.
- Reihenfolge und Vertrauensniveau der Parser sind nicht überall eindeutig dokumentiert.
- Fallback-Strategien und Fehlerdiagnostik sind ausbaubar.

## Rework-Ansatz
- Einführung klarer Parser-Prioritäten (Trust-Level / Source-Weighting).
- Trennung zwischen:
  - **schnellen Basis-Parsern** (Dateiname, Container)
  - **qualitativen Deep-Parsern** (Mutagen, ffmpeg/pymediainfo)
- Standardisierte Merge-Regeln für Konfliktfelder (z. B. Titel, Album, Track, Disc).
- Isolierte Fehlerbehandlung pro Parser (kein globaler Abbruch bei Teilfehlern).
- Verbesserte Logging-Spuren für jede Pipeline-Stufe.

## Geplante Deliverables
- Dokumentierte Parser-Reihenfolge inkl. Prioritätsmatrix.
- Einheitliches Ergebnisobjekt für Parser-Outputs.
- Konsolidierte Merge-/Fallback-Logik in zentralem Modul.
- Regression-Tests für konfliktbehaftete Metadatenfälle.
- Messbare Qualitätsverbesserung bei gemischten Medienbibliotheken.

## Akzeptanzkriterien
- Pipeline läuft stabil weiter, auch wenn einzelne Parser ausfallen.
- Konflikte werden reproduzierbar nach festen Regeln aufgelöst.
- Logging zeigt pro Datei klar: Quelle, Entscheidung, finaler Wert.
- Relevante Parser-Fälle sind automatisiert getestet.

## Schnittstellen zu anderen Einträgen
- Baut auf den frühen Architektur-/Metadaten-Einträgen auf.
- Ergänzt M2 (Medienbibliothek) mit Fokus auf Datenqualität.
- Unterstützt M4-Ziele im Bereich Release-/Betriebsqualität durch bessere Diagnostik.
