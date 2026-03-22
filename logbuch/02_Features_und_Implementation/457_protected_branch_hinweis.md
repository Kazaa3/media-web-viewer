# Hinweis: Protected Branch – main (März 2026)

## Problem

Der Push auf den Branch `main` wurde von GitHub abgelehnt:

> remote: error: GH006: Protected branch update failed for refs/heads/main.
> remote: - Changes must be made through a pull request.

**Ursache:**
- Der Branch `main` ist als "protected branch" konfiguriert. Direkte Pushes sind nicht erlaubt, Änderungen müssen per Pull Request (PR) erfolgen.

## Lösung / Vorgehen
1. **Pull Request erstellen:**
   - Auf GitHub einen PR von `meilenstein-1-mediaplayer` nach `main` öffnen.
2. **Review & Merge:**
   - PR reviewen lassen und gemäß den Schutzregeln mergen (z.B. Review, Checks grün).
3. **Weiterarbeiten:**
   - Nach dem Merge ist `main` aktuell. Jetzt kann der Feature-Branch für den Videoplayer erstellt werden.

## Empfehlung
- Protected Branches sind sinnvoll für stabile Releases und verhindern versehentliche Fehler.
- Änderungen an `main` immer über PRs und Reviews einbringen.

---

**Siehe auch:**
- GitHub Doku: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- Projekt-Tutorial: Abschnitt "Merge via Terminal/PR" in SYSTEM_SYNTHESIS.md und logbuch/2026-03-14_pipeline_paketbau_fixes.md
