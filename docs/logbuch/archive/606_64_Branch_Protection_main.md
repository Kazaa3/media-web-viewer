<!--
Category: infrastructure
Title_DE: Branch Protection für main-Branch
Title_EN: Branch Protection for main Branch
Summary_DE: Lokaler Git-Hook und GitHub Branch Protection Rules zum Schutz des stabilen main-Branches vor versehentlichen M2-Pushes
Summary_EN: Local Git hook and GitHub branch protection rules to protect stable main branch from accidental M2 pushes
Status: active
Related: 61_Branching_Entscheidung_M2_und_Agent_Workflow.md, 63_M2_Branch_Integration_und_main_Schutz.md
-->

# Branch Protection für main-Branch

**Status:** Implementiert  
**Datum:** 2026-03-09  
**Version:** 1.3.4

## Problem

Nach der Trennung von M1 (main) und M2 (milestone/2-medienbibliothek) besteht das Risiko, dass:
- Versehentlich M2-Arbeit direkt zu main gepusht wird
- Force-Pushes main überschreiben
- Unstabile Features ohne Review in main gelangen

GitHub zeigte die Warnung:
> Your main branch isn't protected. Protect this branch from force pushing or deletion, or require status checks before merging.

## Lösung

### 1. Lokaler Git Pre-Push Hook

**Datei:** `.git/hooks/pre-push`

**Funktionalität:**
- Erkennt Pushes zu `refs/heads/main`
- Zeigt farbige Warnung mit Branch-Info
- Fragt nach expliziter Bestätigung (`yes` erforderlich)
- Schlägt korrekte M2-Workflow-Alternative vor
- Kann mit `--no-verify` umgangen werden

**Installation:**
```bash
chmod +x .git/hooks/pre-push
```

**Test:**
```bash
# Von einem Feature-Branch aus
git checkout -b test-protection
git commit --allow-empty -m "test"
git push origin main  # → Warnung + Abfrage

# Umgehen (falls nötig)
git push origin main --no-verify
```

**Ausgabe bei verbotenem Push:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  WARNUNG: Push zu main-Branch!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Aktueller Branch:  test-protection
  Ziel:              main
  Remote:            origin

Hinweis:
  - main ist für stabile Releases (M1 - AudioPlayer)
  - M2-Arbeit gehört in: milestone/2-medienbibliothek
  - Feature-Branches: m2/feature-name

Zum Überspringen: git push --no-verify
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wirklich zu main pushen? (yes/NO): █
```

### 2. GitHub Branch Protection Rules

**URL:** https://github.com/Kazaa3/media-web-viewer/settings/rules

#### Empfohlene Einstellungen:

##### **Branch name pattern:** `main`

##### **Rules:**

**☑ Require a pull request before merging**
- ☑ Require approvals: 1 (kann später auf 0 für Solo-Arbeit, aber PR-Workflow bleibt)
- ☑ Dismiss stale pull request approvals when new commits are pushed
- ☐ Require review from Code Owners (optional, wenn `CODEOWNERS` Datei existiert)

**☑ Require status checks to pass before merging**
- ☑ Require branches to be up to date before merging
- Status checks to require:
  - `build` (wenn GitHub Actions CI läuft)
  - `test` (wenn automatische Tests konfiguriert sind)

**☑ Require conversation resolution before merging**
- Alle PR-Kommentare müssen resolved sein

**☑ Require linear history**
- Verhindert Merge-Commits, erlaubt nur Rebase/Squash
- Alternative: ☐ deaktivieren und Merge-Commits mit `--no-ff` erlauben

**☑ Require deployments to succeed before merging**
- Optional, nur wenn Deployment-Pipeline existiert

**☑ Do not allow bypassing the above settings**
- Selbst Admins können Rules nicht überspringen (streng)
- Alternative: ☐ deaktivieren für Solo-Entwicklung mit gelegentlichem Admin-Override

**☑ Restrict who can push to matching branches**
- Nur bestimmte User/Teams erlauben
- Liste: `kazaa3` (oder leer lassen für "alle Collaborators via PR")

**☑ Block force pushes**
- Verhindert `git push --force` zu main

**☑ Prevent deletion**
- main-Branch kann nicht gelöscht werden

#### Setup-Schritte:

1. **Navigiere zu:** https://github.com/Kazaa3/media-web-viewer/settings/rules
2. **Klicke:** "New ruleset" oder "Add rule"
3. **Wähle:** "Branch protection rule"
4. **Branch name pattern:** `main`
5. **Aktiviere alle oben empfohlenen Rules**
6. **Save changes**

#### Alternative: Ruleset API (für Scripting)

```bash
# GitHub CLI (gh) benötigt
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/Kazaa3/media-web-viewer/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1}' \
  -f restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

### 3. Workflow mit Branch Protection

#### **Korrekte M2-Entwicklung:**

```bash
# 1. Feature-Branch erstellen
git checkout milestone/2-medienbibliothek
git pull origin milestone/2-medienbibliothek
git checkout -b m2/new-feature

# 2. Entwickeln + committen
# ... work work work ...
git add .
git commit -m "feat(m2): implement new feature"

# 3. Pushen zu Feature-Branch
git push origin m2/new-feature

# 4. Pull Request erstellen
# → GitHub: m2/new-feature → milestone/2-medienbibliothek

# 5. Nach Merge: lokale Branches aufräumen
git checkout milestone/2-medienbibliothek
git pull origin milestone/2-medienbibliothek
git branch -d m2/new-feature
```

#### **Release zu main (nur wenn M2 Release-Ready):**

```bash
# 1. Erstelle Release-PR
git checkout milestone/2-medienbibliothek
git push origin milestone/2-medienbibliothek

# 2. GitHub: Pull Request
#    milestone/2-medienbibliothek → main
#    Title: "Release v1.4.0 - Medienbibliothek"
#    Body: Release Notes aus logbuch/...

# 3. PR-Checks laufen
# 4. PR Review + Approval
# 5. Merge PR (GitHub UI)

# 6. Tag Release
git checkout main
git pull origin main
git tag -a v1.4.0 -m "Release v1.4.0: Medienbibliothek"
git push origin v1.4.0
```

#### **Hotfix für main (Notfall):**

```bash
# 1. Hotfix-Branch von main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Fix entwickeln
# ... fix ...
git commit -m "fix: critical bug in production"

# 3. PR direkt zu main
git push origin hotfix/critical-bug
# → GitHub PR: hotfix/critical-bug → main

# 4. Nach Merge: Hotfix zurück zu M2
git checkout milestone/2-medienbibliothek
git merge main --no-ff -m "chore(m2): integrate hotfix from main"
git push origin milestone/2-medienbibliothek
```

### 4. Bypass-Mechanismen (Notfall)

**Lokaler Hook:**
```bash
git push --no-verify origin main
```

**GitHub Protection (nur wenn "Do not allow bypassing" deaktiviert):**
- Temporär Rule deaktivieren: Settings → Rules → Edit → Disable
- Nach Push wieder aktivieren

**Force-Push trotz Protection (gefährlich):**
```bash
# Nur wenn GitHub-Regeln Admin-Override erlauben
git push --force-with-lease origin main
```

⚠️ **Diese Bypasses sollten nur in echten Notfällen verwendet werden!**

## Validierung

### Lokaler Hook:

```bash
# Test 1: Push zu main verhindern
git checkout -b test-push-protection
git commit --allow-empty -m "test"
git push origin main  # → Warnung, Abfrage "yes/NO"
# Eingabe: NO → Abort ✅

# Test 2: Push zu M2 erlauben
git push origin milestone/2-medienbibliothek  # → Kein Hook, direkter Push ✅

# Test 3: Bypass funktioniert
git push --no-verify origin main  # → Push ohne Warnung ✅
git push origin :refs/heads/main  # Löschen rückgängig falls nötig
```

### GitHub Protection:

1. Settings → Rules → main → Check "Enabled" ✅
2. Versuche Force-Push: `git push -f origin main` → 403 Forbidden ✅
3. Versuche Branch löschen: `git push origin --delete main` → 403 Forbidden ✅
4. Erstelle PR zu main ohne Status-Checks → "Merge"-Button disabled ✅

## Checkliste

- [x] `.git/hooks/pre-push` erstellt
- [x] Hook ausführbar: `chmod +x .git/hooks/pre-push`
- [x] Hook getestet: Push zu main verhindern
- [x] Hook getestet: M2-Push erlauben
- [ ] GitHub Branch Protection Rule für `main` aktiviert
- [ ] Status Checks konfiguriert (optional, wenn CI vorhanden)
- [ ] Force-Push blockiert
- [ ] Branch-Deletion blockiert
- [ ] Team informiert über Workflow-Änderung

## Siehe auch

- [logbuch/61 - Branching-Regeln M2](61_Branching_Entscheidung_M2_und_Agent_Workflow.md)
- [logbuch/63 - M2 Branch Integration](63_M2_Branch_Integration_und_main_Schutz.md)
- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

## Zusammenfassung

**Lokaler Schutz:** ✅ Implementiert (Pre-Push Hook)  
**GitHub Schutz:** ⏳ Manuell aktivieren über GitHub UI  
**M2-Workflow:** ✅ Dokumentiert  
**Release-Prozess:** ✅ Via PRs definiert

**Nächste Schritte:**
1. GitHub Branch Protection Rules über UI aktivieren (siehe Setup-Schritte oben)
2. Optional: CI/CD Status Checks hinzufügen
3. Optional: `CODEOWNERS` Datei für Auto-Review-Assignment
