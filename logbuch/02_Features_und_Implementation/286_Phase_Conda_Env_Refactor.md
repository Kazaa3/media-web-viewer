## Phase 14: Conda Environment Refactor
**Datum:** 12. März 2026

- Im CI und Build-System wurden explizit Conda-Umgebungen erlaubt, insbesondere für Python 3.14 (Testzwecke).
- Diese Sonderregelung muss refactored und sauber dokumentiert werden, um langfristige Kompatibilität und Wartbarkeit zu gewährleisten.

### Aufgaben
- Refactoring der CI-Jobs und Build-Skripte, sodass Conda-Umgebungen explizit und kontrolliert unterstützt werden.
- Dokumentation der Conda-Umgebungslogik im Logbuch und in den Build-Dokumenten.
- Sicherstellen, dass die Umgebungserkennung (env_handler.py) robust und flexibel bleibt.
- Tests für Python 3.14 und andere Versionen in Conda-Umgebungen ergänzen.

*Entry created: 12. März 2026*
---