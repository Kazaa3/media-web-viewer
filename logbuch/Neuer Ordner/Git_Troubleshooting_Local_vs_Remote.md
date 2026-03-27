# Git Troubleshooting: Local vs Remote

## Problem

Heute wurden keine Änderungen gemerged – alle Änderungen sind nur lokal vorhanden. Git-Funktionen (Push, Merge) funktionieren nicht wie erwartet.

## Ursachen

- Änderungen wurden nur lokal committet, aber nicht gepusht.
- Remote-Repository ist nicht erreichbar oder falsch konfiguriert.
- Merge-Konflikte verhindern das Pushen.
- Netzwerkprobleme oder Firewall blockieren Git.

## Lösungsschritte

1. **Status prüfen**
   ```bash
   git status
   git log --oneline
   ```
2. **Remote prüfen**
   ```bash
   git remote -v
   git fetch
   ```
3. **Push versuchen**
   ```bash
   git push origin <branch>
   ```
4. **Konflikte auflösen**
   - Bei Konflikten: `git pull --rebase` oder `git merge` und Konflikte manuell lösen.

5. **Netzwerk prüfen**
   - Internetverbindung und Firewall-Einstellungen kontrollieren.

6. **Remote-URL prüfen**
   ```bash
   git remote get-url origin
   ```

## Problem mit großen Dateien (.deb, .exe, .whl)

GitHub akzeptiert keine Dateien >100 MB (z.B. .deb, .exe, .whl). Wenn der Push fehlschlägt:

- Prüfe mit `git status` und `git ls-files` ob große Dateien getrackt sind.
- Entferne sie aus dem Git-Index:
  ```bash
  git rm --cached <dateiname>
  git commit -m "Remove large build artifacts from tracking"
  git push
  ```
- Füge build/ und dist/ sowie *.deb, *.exe, *.whl in `.gitignore` ein.
- Wenn die Dateien in der Historie sind, nutze `git filter-repo` oder `BFG Repo-Cleaner`:
  - [BFG Repo-Cleaner Anleitung](https://rtyley.github.io/bfg-repo-cleaner/)
  - [git filter-repo Anleitung](https://github.com/newren/git-filter-repo)

**Hinweis:**
Nur Quellcode und Dokumentation gehören ins Git-Repo. Build-Artefakte werden über CI/CD bereitgestellt.

## Typische Fehler

- `fatal: not a git repository`
- `error: failed to push some refs`
- `merge conflict`
- `permission denied`

## Hinweise

- Änderungen sind erst nach `git push` im Remote sichtbar.
- Lokale Commits können mit `git log` überprüft werden.
- Bei Problemen: GitHub/Remote-URL, Branch und Netzwerk prüfen.

---

**Letzte Änderung:** 2026-03-13

**Autor:** GitHub Copilot
