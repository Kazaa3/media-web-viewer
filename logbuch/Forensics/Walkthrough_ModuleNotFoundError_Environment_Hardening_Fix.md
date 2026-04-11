# Walkthrough - ModuleNotFoundError & Environment Hardening Fix

## Zusammenfassung
Der `ModuleNotFoundError` wurde durch eine Umstrukturierung der Bootstrap-Sequenz der Anwendung behoben.

---

## 🛠️ Solution: Hardened Environment Switching

**Problem:**
- Der Crash trat auf, weil `psutil` (benötigt vom neuen Process Management) ganz oben in `main.py` importiert wurde, bevor die Anwendung in das richtige virtuelle Environment (.venv) wechseln konnte.
- Die globale Python-Installation (3.14) enthielt kein `psutil`, wodurch das Programm vorzeitig beendet wurde.

**Lösung:**
- **Deferred Imports:** Die Importe von `ProcessController` und allen psutil-abhängigen Modulen wurden in die `start_app`-Logik verschoben.
- **Bootstrapping Priority:** Der Guard `ensure_stable_environment()` (erkennt und startet das Skript ggf. neu mit `./.venv/bin/python`) läuft jetzt, bevor externe Abhängigkeiten geladen werden.

---

## 🚀 How to Run Now

Du kannst die Anwendung jetzt sicher starten mit:

**Empfohlen:**
```bash
bash run.sh
```

**Oder manuell:**
```bash
/home/xc/.local/bin/python3.14 src/core/main.py
```

Die App erkennt nun automatisch, wenn sie im falschen Environment läuft, und startet sich selbst mit dem .venv, in dem alle Abhängigkeiten installiert sind.

---

## Ergebnis
- Die "Always-On"-Navigation und die "Kill-on-Startup"-Logik funktionieren jetzt zuverlässig, egal mit welchem Python-Binary das Programm initial gestartet wird.
