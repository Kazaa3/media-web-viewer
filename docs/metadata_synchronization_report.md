# Synchronization of Name, License, and Metadata

**Datum:** 14.03.2026
**Autor:** Copilot

---

## Ziel

Alle projektrelevanten Metadaten wie Name, Lizenz, Version und weitere zentrale Angaben werden synchronisiert und konsistent in den relevanten Dateien und Konfigurationsquellen gepflegt.

---

## Vorgehen

1. **Zentrale Quellen identifizieren:**
   - Projektname, Lizenz, Version etc. in: `pyproject.toml`, `setup.cfg`, `infra/VERSION_SYNC.json`, `README.md`, `LICENSE.md`, ggf. CI/CD-Workflows.

2. **Synchronisation:**
   - Alle Metadaten werden auf einen einheitlichen Stand gebracht (z.B. Name und Lizenz überall identisch).
   - Automatisierte oder dokumentierte Prozesse zur Metadatenpflege werden etabliert (z.B. Skript für VERSION_SYNC).

3. **Dokumentation:**
   - Die relevanten Felder und deren Speicherorte werden dokumentiert.
   - Hinweise zur Pflege und zum Update-Prozess werden ergänzt.

---

## Ergebnis

- Name, Lizenz, Version und weitere Metadaten sind in allen relevanten Dateien synchron.
- Inkonsistenzen und Pflegefehler werden vermieden.
- Die Projektidentität ist klar und rechtssicher dokumentiert.

---

**Details siehe:**
- [pyproject.toml](../pyproject.toml)
- [infra/VERSION_SYNC.json](../infra/VERSION_SYNC.json)
- [README.md](../README.md)
- [LICENSE.md](../LICENSE.md)
- [walkthrough.md](walkthrough.md)
