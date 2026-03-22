<!-- Category: Process -->
<!-- Title_DE: M2-Branch-Integration und main-Schutz -->
<!-- Title_EN: M2 branch integration and main protection -->
<!-- Summary_DE: Zusammenführung der Copilot-Branches in milestone/2-medienbibliothek und Verhinderung versehentlicher main-Pushes. -->
<!-- Summary_EN: Integration of Copilot branches into milestone/2-medienbibliothek and prevention of accidental main pushes. -->
<!-- Status: ACTIVE -->

# M2-Branch-Integration und main-Schutz

**Datum:** 9. März 2026  
**Status:** 🟡 ACTIVE

## Situation

Während der initialen M2-Entwicklung wurden Features in Copilot-Branches entwickelt:
- `copilot/add-database-for-tags` - Tags-Tabelle (v1.3.4) → **bereits in main gemergt via PR #2**
- `copilot/add-tags-database` - Erweiterte Features (releases, multi-disc, multi-language) → **noch nicht gemergt**

**Problem:** Ein Teil der M2-Arbeit ist versehentlich bereits in main gelandet.

## Lösung: Saubere M2-Trennung ab jetzt

### 1. Offizieller M2-Branch

Ab sofort ist `milestone/2-medienbibliothek` der **einzige** offizielle Entwicklungsbranch für M2.

```bash
# Sicherstellen, dass du auf M2 bist
git checkout milestone/2-medienbibliothek

# Niemals direkt in main pushen!
# main ist nur für finale M2-Merges nach Abnahme
```

### 2. Integration ausstehender Copilot-Arbeit

```bash
# Copilot-Branch mit erweiterten Features lokal holen
git fetch origin copilot/add-tags-database

# In M2 integrieren (falls gewünscht)
git checkout milestone/2-medienbibliothek
git merge origin/copilot/add-tags-database --no-ff -m "feat(m2): integrate extended tags features from copilot branch"
```

### 3. main-Schutz (lokale Regel)

**Verbindlich ab sofort:**
- ❌ KEIN direktes Arbeiten in main
- ❌ KEIN Pushen nach main ohne explizite M2-Abnahme
- ✅ Alle M2-Arbeit in `milestone/2-medienbibliothek`
- ✅ Feature-Branches optional von M2 abzweigen

```bash
# Vor jedem Push prüfen!
git rev-parse --abbrev-ref HEAD
# Muss "milestone/2-medienbibliothek" sein, NICHT "main"
```

### 4. Workflow für Agent-Arbeit

```bash
# 1) Auf M2-Branch wechseln
git checkout milestone/2-medienbibliothek

# 2) Mit Agent arbeiten (Code, Tests, Doku)
# Agent macht Änderungen...

# 3) Regelmäßig in M2 committen
git add .
git commit -m "feat(m2): <beschreibung>"

# 4) In M2 pushen (NICHT main!)
git push origin milestone/2-medienbibliothek
```

## Was ist mit den bereits gemergten Änderungen in main?

Die Tags-Datenbank (v1.3.4) ist bereits in main und kann dort bleiben.
- Das ist okay, da es funktionsfähig ist
- M2 baut darauf auf
- Zukünftige M2-Erweiterungen bleiben im M2-Branch bis zur finalen Abnahme

## Nächste Meilensteine (Überblick)

| Meilenstein | Branch | Status |
|---|---|---|
| M1 – AudioPlayer | `main` | ✅ abgeschlossen |
| M2 – Medienbibliothek | `milestone/2-medienbibliothek` | 🟡 aktiv |
| M3 – Erweiterte Bibliotheksfunktionen | `milestone/3-erweiterte-bibliothek` (geplant) | 📋 geplant |
| M4 – Neue GUI | `milestone/4-neue-gui` (geplant) | 📋 geplant |

**Hinweis:** M3/M4 sind noch nicht final definiert und werden später detailliert geplant.

## Verwandte Einträge

- [60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md](60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md)
- [61_Branching_Entscheidung_M2_und_Agent_Workflow.md](61_Branching_Entscheidung_M2_und_Agent_Workflow.md)
- [59_Milestone_2_Medienbibliothek.md](59_Milestone_2_Medienbibliothek.md)

<!-- lang-split -->

# M2 branch integration and main protection

**Date:** March 9, 2026  
**Status:** 🟡 ACTIVE

## Situation

During initial M2 development, features were developed in Copilot branches:
- `copilot/add-database-for-tags` - Tags table (v1.3.4) → **already merged to main via PR #2**
- `copilot/add-tags-database` - Extended features (releases, multi-disc, multi-language) → **not yet merged**

**Problem:** Part of M2 work accidentally ended up in main.

## Solution: Clean M2 separation from now on

### 1. Official M2 branch

From now on, `milestone/2-medienbibliothek` is the **only** official development branch for M2.

```bash
# Ensure you're on M2
git checkout milestone/2-medienbibliothek

# Never push directly to main!
# main is only for final M2 merges after acceptance
```

### 2. Integration of pending Copilot work

```bash
# Fetch Copilot branch with extended features
git fetch origin copilot/add-tags-database

# Integrate into M2 (if desired)
git checkout milestone/2-medienbibliothek
git merge origin/copilot/add-tags-database --no-ff -m "feat(m2): integrate extended tags features from copilot branch"
```

### 3. main protection (local rule)

**Binding from now on:**
- ❌ NO direct work in main
- ❌ NO pushing to main without explicit M2 acceptance
- ✅ All M2 work in `milestone/2-medienbibliothek`
- ✅ Feature branches optionally forked from M2

```bash
# Check before every push!
git rev-parse --abbrev-ref HEAD
# Must be "milestone/2-medienbibliothek", NOT "main"
```

### 4. Workflow for agent work

```bash
# 1) Switch to M2 branch
git checkout milestone/2-medienbibliothek

# 2) Work with agent (code, tests, docs)
# Agent makes changes...

# 3) Commit regularly to M2
git add .
git commit -m "feat(m2): <description>"

# 4) Push to M2 (NOT main!)
git push origin milestone/2-medienbibliothek
```

## What about already merged changes in main?

The tags database (v1.3.4) is already in main and can stay there.
- This is okay since it's functional
- M2 builds on top of it
- Future M2 extensions stay in M2 branch until final acceptance

## Next milestones (overview)

| Milestone | Branch | Status |
|---|---|---|
| M1 – AudioPlayer | `main` | ✅ completed |
| M2 – Media Library | `milestone/2-medienbibliothek` | 🟡 active |
| M3 – Extended Library Features | `milestone/3-erweiterte-bibliothek` (planned) | 📋 planned |
| M4 – New GUI | `milestone/4-neue-gui` (planned) | 📋 planned |

**Note:** M3/M4 are not yet finalized and will be planned in detail later.

## Related entries

- [60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md](60_Milestone_1_AudioPlayer_Abschluss_und_Technische_Nachdoku.md)
- [61_Branching_Entscheidung_M2_und_Agent_Workflow.md](61_Branching_Entscheidung_M2_und_Agent_Workflow.md)
- [59_Milestone_2_Medienbibliothek.md](59_Milestone_2_Medienbibliothek.md)
