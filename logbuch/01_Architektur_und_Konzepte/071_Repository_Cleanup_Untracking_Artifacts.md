# 90 Repository Cleanup – Untracking Generated Artifacts

**Datum:** 09.03.2026  
**Bereich:** Git Hygiene / Build-Artefakte  
**Status:** ✅ umgesetzt

## Ziel
Bereits versionierte, generierte Dateien sollten aus dem Repository entfernt werden, ohne lokale Build-/Staging-Dateien zu löschen.

## Problem
Trotz `.gitignore` blieben Änderungen unter folgenden Pfaden in `git status` sichtbar:
- `packaging/opt/media-web-viewer/**` (Build-Staging-Mirror)
- `__pycache__/main.cpython-314.pyc`
- `media-web-viewer_1.3.3_amd64.deb`

Ursache: `.gitignore` greift nur für **neue/untracked** Dateien, nicht für bereits getrackte Inhalte.

## Umsetzung
Einmaliges Entfernen aus dem Git-Index (lokale Dateien bleiben erhalten):

```bash
git rm -r --cached -- packaging/opt/media-web-viewer
git rm --cached -- __pycache__/main.cpython-314.pyc
git rm --cached -- media-web-viewer_1.3.3_amd64.deb
```

Zusätzlich wurde `.gitignore` bereits so ergänzt, dass diese Pfade künftig nicht erneut getrackt werden.

## Ergebnis
- Die Artefakte sind als staged Deletions im Index markiert (korrekt für den Cleanup-Commit).
- Nach Commit/Pull bleiben die Dateien lokal nutzbar, werden aber nicht mehr vom Repo überwacht.

## Nächster Schritt
Cleanup committen und pushen:

```bash
git status --short
git commit -m "chore: untrack generated packaging/cache artifacts"
git push
```
