# Phase 12: Test Organization & Debug Artifacts

**Datum:** 13.03.2026
**Autor:** Copilot

## Ziel
Testskripte werden in logische Unterverzeichnisse gruppiert und Debug-Artefakte (Screenshots, Logs) in einen zentralen, git-ignorierten Ordner ausgelagert. Dies erhöht Übersichtlichkeit und Wartbarkeit der Teststruktur.

## Maßnahmen
- [MODIFY] `tests/`: Aufteilung in `tests/ui/`, `tests/unit/`, `tests/integration/`
- [NEW] `tests/debug_artifacts/`: Zentrale Ablage für Screenshots und Logs (git-ignored)

## Verification Plan
**Automatisierte Tests:**
- `pytest` aus dem Root-Verzeichnis ausführen, um sicherzustellen, dass alle Tests in den Unterverzeichnissen gefunden werden
- Überprüfen, dass Screenshots und Logs in `tests/debug_artifacts/` geschrieben werden

**Manuelle Prüfung:**
- Kontrolle, dass das Projekt-Root sauber bleibt (keine Debug-Artefakte außerhalb von `tests/debug_artifacts/`)
- Sicherstellen, dass `.gitignore` das neue Debug-Verzeichnis korrekt ausschließt
- Nur essentielle Projektdateien (README, .gitignore, src/) im Root

---

**Kommentar:**
Die neue Teststruktur und zentrale Debug-Artefakt-Ablage sorgen für eine saubere, skalierbare Testumgebung und erleichtern die Pflege und Analyse von Testergebnissen.
