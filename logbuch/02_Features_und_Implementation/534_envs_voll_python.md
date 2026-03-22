# Logbuch: Python-Umgebungen – Jede ENV mit vollem Python

**Datum:** 15.03.2026

## Übersicht
Jede virtuelle Umgebung (ENV) im Projekt – z.B. `.venv_run`, `.venv_testbed`, `.venv_selenium` – enthält eine vollständige, eigene Python-Installation.

---

## Details
- Jede venv ist unabhängig vom System-Python und bringt ihren eigenen Interpreter mit.
- Alle benötigten Pakete werden pro Umgebung installiert und verwaltet.
- Das garantiert:
  - Saubere Trennung der Abhängigkeiten (z.B. Laufzeit, Test, Selenium)
  - Reproduzierbarkeit und weniger Konflikte
  - Keine Abhängigkeit von global installierten Paketen
- Die Umgebungen werden per `python -m venv` oder vergleichbare Tools erzeugt.

---

## Overhead durch eigene Interpreter
- Jede venv bringt einen eigenen Python-Interpreter und eigene Pakete mit.
- Das erhöht den Speicherplatzbedarf (typisch: 50–150 MB pro ENV inkl. Pakete).
- Vorteile überwiegen meist:
  - Maximale Isolierung, keine Konflikte zwischen Abhängigkeiten
  - Reproduzierbare Builds und Tests
  - Unabhängigkeit vom System-Python
- Für moderne SSDs und typische Projektgrößen ist der Overhead meist unkritisch.
- Bei sehr vielen ENVs oder extrem begrenztem Speicher kann eine Konsolidierung sinnvoll sein.

---

## Ressourcenverbrauch zur Laufzeit (RAM/CPU/SSD)
- **RAM:**
  - Jede aktive venv (eigener Python-Prozess) belegt RAM für Interpreter, geladene Pakete und Daten.
  - Typisch: 30–100 MB RAM pro laufender Instanz, je nach Nutzung und Modulen.
- **CPU:**
  - Kein signifikanter Mehrverbrauch durch mehrere ENVs – entscheidend ist die Anzahl paralleler Prozesse, nicht die ENV-Struktur.
  - CPU-Last entsteht durch die eigentliche Anwendung, nicht durch die venv selbst.
- **SSD:**
  - Während der Laufzeit werden venv-Dateien (Interpreter, Pakete) nur gelesen, nicht ständig neu geschrieben.
  - SSD-Belastung ist minimal, außer bei Installation/Update von Paketen.
- **Fazit:**
  - Der Haupt-Overhead entsteht beim Speicherplatzbedarf und beim parallelen Betrieb mehrerer Instanzen.
  - Für typische Desktop-/Server-SSDs und RAM-Größen ist das meist unkritisch.

---

## Paralleler Einsatz mehrerer ENVs und Systemressourcen
- Werden mehrere ENVs gleichzeitig genutzt (z.B. Backend, Testbed, Selenium parallel), startet jeder Prozess mit eigenem Interpreter und eigenen Paketen.
- **RAM:**
  - Der Speicherbedarf steigt linear mit der Anzahl der parallel laufenden Python-Prozesse.
  - Beispiel: 3 parallele ENVs à 80 MB → ca. 240 MB RAM nur für Interpreter, plus Anwendungsdaten.
- **CPU:**
  - Die CPU-Last verteilt sich auf die Prozesse. Bei CPU-intensiven Tasks (z.B. gleichzeitige Tests, Medienverarbeitung) kann es zu Lastspitzen kommen.
  - Moderne Mehrkern-CPUs profitieren von echter Parallelität.
- **SSD:**
  - Keine zusätzliche Belastung durch parallele ENVs im Normalbetrieb, da Pakete/Interpreter nur gelesen werden.
- **Netzwerk/IO:**
  - Parallele Prozesse können zu mehr gleichzeitigen Datei- oder Netzwerkzugriffen führen.
- **Fazit:**
  - Paralleler Einsatz ist problemlos möglich, solange genügend RAM und CPU-Kapazität vorhanden sind.
  - Für ressourcenarme Systeme empfiehlt sich ggf. sequentieller Betrieb oder gezieltes Beenden nicht benötigter ENVs.

---

## Vorteile
- Isolierte, sichere Entwicklungs- und Testumgebungen
- Klare Zuordnung von Paketen zu Use-Cases (z.B. Test vs. Produktion)
- Einfaches Updaten, Löschen oder Ersetzen einzelner ENVs

---

**Siehe auch:**
- [SYSTEM_VENVS_EXPLAINED.md](../docs/SYSTEM_VENVS_EXPLAINED.md)
- [env_handler.py](../src/core/env_handler.py)
