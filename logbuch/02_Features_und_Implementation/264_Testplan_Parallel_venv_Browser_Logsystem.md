# Testplan: Verifikation paralleler venvs und Browser-Fenster

## Ziel
Dieser Testplan beschreibt die Verifikation, dass alle venvs (App-GUI, Selenium-Headless, weitere envs) erfolgreich gleichzeitig laufen und im globalen Logsystem (core) sauber getrennt sind.

---

### Testaufbau
1. **App-GUI**
   - Starte die Hauptanwendung im .venv_core (normale GUI, Browser-Fenster).
   - Log-Ausgaben im globalen Logsystem (core).

2. **Selenium-Headless**
   - Starte Selenium-Tests im .venv_selenium (headless Browser).
   - Log-Ausgaben separat, aber im globalen Logsystem sichtbar.

3. **Weitere envs**
   - Starte z.B. Backend-Tests (.venv_dev), Build-Prozesse (.venv_build), Doku-Builds (.venv_docs).
   - Log-Ausgaben jeweils separat, aber im globalen Logsystem sichtbar.

---

### Testschritte
- Parallelstart aller venvs (App-GUI, Selenium, Dev, Build, Docs).
- Öffne mehrere Browser-Fenster (GUI, Selenium-Headless).
- Führe Aktionen in jedem Fenster/env aus (z.B. Tab-Wechsel, Testlauf, Build).
- Prüfe, ob alle Log-Ausgaben im globalen Logsystem erscheinen und eindeutig zugeordnet sind (z.B. durch Prefix: [core], [selenium], [dev], [build], [docs]).
- Verifiziere, dass keine Log-Konflikte oder Überschneidungen auftreten.
- Beende alle Prozesse und prüfe, ob die Trennung weiterhin erhalten bleibt.

---

### Erfolgskriterien
- Alle venvs und Browser-Fenster laufen gleichzeitig und unabhängig.
- Log-Ausgaben sind sauber getrennt und im globalen Logsystem sichtbar.
- Keine Überschneidungen oder Konflikte.
- Trennung bleibt auch nach Beenden der Prozesse erhalten.

---

**Letzte Aktualisierung:** 12. März 2026
