<!-- Category: Process -->
<!-- Title_DE: Branching-Entscheidung: M2-Arbeit in eigenem Branch -->
<!-- Title_EN: Branching decision: keep M2 work in dedicated branch -->
<!-- Summary_DE: Verbindliche Regel, dass laufende KI-/Feature-Arbeit im M2-Branch isoliert bleibt und erst nach Abschluss in main gemergt wird. -->
<!-- Summary_EN: Binding rule that ongoing AI/feature work stays isolated in the M2 branch and is merged into main only after completion. -->
<!-- Status: ACTIVE -->

# Branching-Entscheidung: M2-Arbeit in eigenem Branch

**Version:** 1.3.4  
**Datum:** 9. März 2026  
**Status:** 🟡 ACTIVE  
**Gültig ab:** sofort

## Entscheidung

Alle laufenden Arbeiten, die über den abgeschlossenen M1-Basisplayer hinausgehen,
werden ausschließlich im Branch

`milestone/2-medienbibliothek`

umgesetzt.

Dazu gehören insbesondere:
- KI-Agent-gestützte Refactorings/Fixes
- Bibliotheksfeatures (Tags, Suche, Filter)
- UI- und Stabilitätsarbeit, sofern sie M2-Ziele betrifft
- Dokumentationsupdates, die M2-Inhalte beschreiben

## Ziel der Trennung

- `main` bleibt stabil als M1-Basislinie.
- M2 kann iterativ entwickelt und getestet werden, ohne M1-Releases zu destabilisieren.
- Der Merge nach `main` erfolgt erst nach M2-Abschlusskriterien.

## Praktischer Workflow

```bash
# 1) Von main auf den M2-Branch wechseln
git checkout milestone/2-medienbibliothek

# 2) Für einzelne Themen optional Feature-Branch erstellen
git checkout -b feature/m2-<thema>

# 3) Änderungen umsetzen, testen, committen
python tests/test_version_sync.py

# 4) Feature-Branch zurück in M2 mergen
git checkout milestone/2-medienbibliothek
git merge --no-ff feature/m2-<thema>

# 5) Nach vollständiger M2-Abnahme: M2 -> main
# (separat, bewusst, mit Release-Check)
```

## Merge-Gates (M2 → main)

Vor dem finalen Merge nach `main` müssen mindestens erfüllt sein:
- [ ] M2-Abnahme laut Meilenstein-Dokumentation
- [ ] Relevante Tests grün
- [ ] Versions-Synchronisierung grün (`tests/test_version_sync.py`)
- [ ] Logbuch/Dokumentation auf aktuellem Stand

## Verknüpfung mit Logbuch

- M1-Abschluss: [60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md](60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md)
- M2-Plan/Umsetzung: [59_Milestone_2_Medienbibliothek.md](59_Milestone_2_Medienbibliothek.md)

<!-- lang-split -->

# Branching decision: keep M2 work in dedicated branch

**Version:** 1.3.4  
**Date:** March 9, 2026  
**Status:** 🟡 ACTIVE  
**Effective:** immediately

## Decision

All ongoing work beyond the completed M1 baseline player is implemented only in

`milestone/2-medienbibliothek`

including:
- AI-agent supported refactors/fixes
- Media library features (tags, search, filters)
- UI/stability work related to M2 goals
- Documentation updates describing M2 content

## Why this separation

- `main` remains stable as M1 baseline.
- M2 can evolve iteratively without destabilizing M1 releases.
- Merge into `main` happens only after M2 completion criteria are met.

## Practical workflow

```bash
# 1) Switch from main to M2 branch
git checkout milestone/2-medienbibliothek

# 2) Optionally create feature branch per topic
git checkout -b feature/m2-<topic>

# 3) Implement, test, commit
python tests/test_version_sync.py

# 4) Merge feature branch back to M2
git checkout milestone/2-medienbibliothek
git merge --no-ff feature/m2-<topic>

# 5) After full M2 acceptance: merge M2 -> main
# (separate, intentional, with release checks)
```

## Merge gates (M2 → main)

Before final merge to `main`, at least:
- [ ] M2 acceptance criteria met
- [ ] Relevant tests passing
- [ ] Version sync passing (`tests/test_version_sync.py`)
- [ ] Logbook/documentation updated

## Logbook linkage

- M1 completion: [60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md](60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md)
- M2 plan/execution: [59_Milestone_2_Medienbibliothek.md](59_Milestone_2_Medienbibliothek.md)
