# Review & Kritik: venv-Konzept – Aktuelle Probleme & Verbesserungsbedarf

**Datum:** 15.03.2026

## Kritik am aktuellen venv-Konzept
- Das aktuelle Konzept mit mehreren spezialisierten venvs (z. B. `.venv_run`, `.venv_testbed`, `.venv_build`) führt zu erheblichem Mehraufwand und ist fehleranfällig.
- Ständig fehlen Pakete in der jeweils aktiven Umgebung, was zu wiederkehrenden Problemen bei Build, Test und Entwicklung führt.
- Die Trennung bringt in der Praxis wenig Mehrwert, da ohnehin jede Umgebung separat gepflegt werden muss und die Synchronisation aufwendig ist.
- Die Komplexität steigt, ohne dass die Vorteile (z. B. saubere Trennung) im Alltag wirklich genutzt werden.

## Beobachtete Probleme
- Häufige Fehlermeldungen wie "No module named ..." beim Wechsel zwischen Test, Build und Laufzeit.
- CI/CD und lokale Entwicklung benötigen oft unterschiedliche Workarounds.
- Neue Teammitglieder oder CI-Runner scheitern regelmäßig an fehlenden Paketen oder falsch aktivierten venvs.

## Verbesserungsansatz
- Vereinfachung auf **eine zentrale venv** für Entwicklung, Test und Build (z. B. `.venv` oder `.venv_dev`).
- Alle benötigten Pakete (inkl. Test- und Build-Abhängigkeiten) werden in dieser einen Umgebung installiert.
- Optionale Trennung (z. B. für Release-Builds) kann als Sonderfall dokumentiert werden, ist aber nicht Standard.
- Onboarding und CI werden dadurch robuster und einfacher.

## Ergänzung: Prozess-Isolation durch venvs
- Jede neu gestartete venv-Umgebung erzeugt ohnehin ihren eigenen, isolierten Python-Prozess.
- Die Trennung der venvs bringt daher in Bezug auf Prozess-Isolation keinen zusätzlichen Vorteil gegenüber einer gepflegten zentralen venv.
- Die Komplexität mehrerer venvs steht nicht im Verhältnis zum tatsächlichen Isolationsgewinn im Alltag.

## Fazit
- Das aktuelle Multi-venv-Konzept ist in der Praxis zu komplex und fehleranfällig.
- Eine zentrale, gepflegte venv ist für die meisten Workflows ausreichend und reduziert Fehlerquellen.
