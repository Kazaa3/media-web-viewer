# Wie sind venv und Conda-Umgebungen verknüpft?

**Datum:** 12. März 2026

---

## Verknüpfung von venv und Conda

- Eine venv ist grundsätzlich unabhängig von Conda.
- Wenn du eine venv in einer aktiven Conda-Umgebung erstellst, kann sie den Python-Interpreter und ggf. Umgebungsvariablen von Conda übernehmen.
- Die venv bleibt aber isoliert: Sie nutzt nur die Pakete, die in ihr installiert wurden.

---

## Typische Szenarien

- **venv in Conda-Umgebung:**
  - Die venv kann den Python von Conda verwenden, ist aber für Python-Pakete unabhängig.
  - Conda-spezifische Pakete (z.B. systemweite Tools) sind nur in der Conda-Umgebung verfügbar.
- **venv ohne Conda:**
  - Nutzt das System-Python oder einen explizit angegebenen Interpreter.

---

## IDE-Einflüsse

- IDEs (z.B. VS Code, PyCharm) zeigen oft beide Umgebungen im Prompt, können aber nur eine für Python-Befehle nutzen.
- Die IDE kann venv und Conda parallel erkennen, aber Python-Befehle laufen immer in der aktivierten Umgebung.
- Manchmal wird die venv mit der Conda-Umgebung "verknüpft", wenn sie im Conda-Kontext erstellt wurde.

---

## venv_build vs. venv_dev

- Du kannst mehrere venvs (z.B. `.venv_build`, `.venv_dev`) parallel haben.
- Jede venv ist unabhängig und kann mit unterschiedlichen Python-Versionen oder Paketen arbeiten.
- Die Wahl der venv bestimmt, welche Pakete und Python-Version verwendet werden.

---

*Entry created: 12. März 2026*
