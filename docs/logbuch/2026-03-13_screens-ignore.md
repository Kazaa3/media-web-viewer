# Logbuch-Eintrag: docs/Screens/ aus Git entfernt und auf .gitignore gesetzt

**Datum:** 13. März 2026

**Aktion:**
- Der Ordner `docs/Screens/` wurde zur `.gitignore` hinzugefügt, um lokale Screenshots und Assets vom Tracking im Git-Repository auszuschließen.
- Alle bereits getrackten Dateien im Ordner wurden mit `git rm --cached -r docs/Screens/` aus dem Git-Index entfernt.
- Nach dem nächsten Commit ist der Ordner nicht mehr im Online-Repository sichtbar.

**Motivation:**
- Screenshots und lokale Assets sollen nicht versioniert werden, um das Repository schlank und datenschutzkonform zu halten.

**Befehle:**
- `.gitignore` angepasst:
  ```
  docs/Screens/
  ```
- Dateien aus dem Index entfernt:
  ```
  git rm --cached -r docs/Screens/
  ```

**Status:**
- Änderung erfolgreich umgesetzt. Beim nächsten Commit wird der Ordner nicht mehr im Repo erscheinen.

---
