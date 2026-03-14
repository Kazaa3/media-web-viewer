# Branches & Release-Strategie – v1.34 (2026-03-14)

## Plan für den finalen Release von v1.34

- **Branch-Hierarchie:**
  - Der gereinigte Stand (release/v1.34-purified) wird lokal in meilenstein-1-mediaplayer gemergt.
  - Dies ist die Vorstufe für den PR nach main.
  - Meilenstein 2 bleibt wie gewünscht außen vor.

- **Datenbank (DB):**
  - Für den Release-Commit ist eine "Surgical Purge" (Löschen der lokalen database.db) vorgesehen, damit der gereinigte Stand mit einem frischen Index startet.
  - Bitte um Zustimmung.

- **Debug-Flags:**
  - Die ~20 einzelnen Debug-Flags (scan, parser, ui, etc.) werden direkt in die parser_config.json überführt, um sie zentral steuerbar zu machen.

- data/ ist jetzt in .gitignore eingetragen und wird ignoriert.
- Es waren keine Daten im Git-Index, daher musste nichts entfernt werden.
- Das Verzeichnis bleibt lokal, wird aber nicht mehr versioniert.
- Aufgabe erledigt!
- Diverse Logs sind hier.

Bitte schau dir den implementation_plan.md an, Sektion "Release Branch Strategy & DB Policy". Sobald du grünes Licht gibst, setze ich das um.

---

_Comprehensive plan for v1.34 release: consolidate DEBUG_FLAGS into parser_config.json, merge purified prerelease into M1, and execute a clean DB purge. Includes branch strategy and final diagnostic flag homogenization._
