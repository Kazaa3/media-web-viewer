# PyInstaller Build-Umgebung & Konsolen-Synchronisation

**Datum:** 14.03.2026

## 1. PyInstaller Build-Umgebung
- Das Build-System (`infra/build_system.py`) sucht jetzt automatisch nach der spezialisierten Umgebung `.venv_build` im Projekt-Root.
- Existiert `.venv_build`, wird diese für den Build-Prozess (PyInstaller) verwendet.
- Falls nicht vorhanden, erfolgt ein Fallback auf den aktuell aktiven Python-Interpreter.
- Damit sind Build-Abhängigkeiten sauber von der Laufzeit-Umgebung getrennt.

## 2. GUI Konsole vs. Python Konsole
- Die Diskrepanz zwischen Terminal-Ausgabe und GUI-Konsole wurde behoben.
- **Verbesserungen in `app.html`:**
  - **Auto-Refresh:** Beim Öffnen des Debug & DB Tabs wird alle 2 Sekunden ein Abgleich mit dem Backend durchgeführt.
  - **Performance:** Neue Logs werden nur gerendert, wenn sich der Inhalt geändert hat.
  - **Scroll-Lock:** Die Konsole scrollt automatisch nach unten (Auto-Scroll), außer Sie scrollen manuell nach oben.
  - **Mehrfach-Sitzungen:** Starten Sie das Programm erneut im Terminal, während eine Instanz läuft, beendet sich der neue Prozess sofort. Die GUI-Konsole zeigt die Logs der aktiven Instanz an.
- Die Konsolenausgabe in der GUI entspricht jetzt exakt der Backend-Ausgabe, sobald der Tab aktiv ist.

---

**Ergebnis:**
- Build- und Laufzeit-Umgebungen sind sauber getrennt.
- Die GUI-Konsole ist performant, synchron und entspricht der echten Python-Konsole.
