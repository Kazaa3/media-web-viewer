# Nützliche Befehle & KI-Tricks für die Entwicklung

## 1. Häufig genutzte Shell-Befehle

- **Virtuelle Umgebung aktivieren:**
  ```bash
  source .venv_run/bin/activate
  ```
- **App starten:**
  ```bash
  python src/core/main.py
  ```
- **Selenium-Tests ausführen:**
  ```bash
  pytest tests/gui/
  ```
- **HTML-Abschnitt mit Zeilennummern anzeigen:**
  ```bash
  cat -n web/app.html | sed -n '3900,3950p' | head -n 50
  ```
- **Abhängigkeiten installieren:**
  ```bash
  pip install -r requirements.txt
  ```
- **Linter & Typprüfung:**
  ```bash
  python infra/build_system.py --lint --type-check
  ```

## 2. KI-gestützte Entwicklungs-Tricks

- **Automatisierte Testgenerierung:**
  - Nutze KI, um gezielt für neue UI-Elemente oder i18n-Attribute Testdateien vorzuschlagen und zu erstellen.
- **HTML-Struktur-Analyse:**
  - Lass dir mit `grep` oder KI alle relevanten Klassen/IDs für Tabs, Buttons, Filterchips etc. extrahieren, um Testabdeckung zu prüfen.
- **Logbuch-Automatisierung:**
  - Lasse KI automatisch Markdown-Logbuch-Einträge zu Bugfixes, Testabdeckung oder Architekturentscheidungen generieren.
- **Code-Vervollständigung & Refactoring:**
  - Nutze KI für Vorschläge zu Docstrings, Typannotationen, Umbenennungen und zur Erkennung von Redundanzen.
- **Schnelle Kontextsuche:**
  - Mit `grep`, `rg` oder KI-gestützter Suche lassen sich relevante Codebereiche und fehlende Tests schnell finden.
- **Testlücken erkennen:**
  - KI kann systematisch alle UI-Elemente mit i18n-Attributen auflisten und mit vorhandenen Tests abgleichen.

## 3. Tipps für effiziente Zusammenarbeit mit KI

- **Präzise Fragen stellen:**
  - Je klarer das Ziel (z.B. "Erstelle Test für alle Buttons mit data-i18n im Playlist-Tab"), desto besser die KI-Antwort.
- **Kontext bereitstellen:**
  - Workspace-Struktur, relevante Dateien und aktuelle Todos helfen der KI, gezielt zu unterstützen.
- **Automatisierte Dokumentation:**
  - Nutze KI, um nach jedem größeren Schritt automatisch Logbuch-Einträge zu erzeugen.
- **Iteratives Vorgehen:**
  - Komplexe Aufgaben in kleine, prüfbare Schritte aufteilen und die KI jeweils gezielt einsetzen.

---

**Hinweis:**
Diese Datei kann laufend um weitere nützliche Befehle, KI-Workflows und Best Practices ergänzt werden.
