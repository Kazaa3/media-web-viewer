<!-- Category: Process -->
<!-- Title_DE: 10 Code-Konsistenz & Agent-Workflow -->
<!-- Title_EN: 10 Code Consistency & Agent Workflow -->
<!-- Summary_DE: Sicherstellung der Qualität bei der Zusammenarbeit zwischen Mensch und KI in multiplen Umgebungen. -->
<!-- Summary_EN: Ensuring quality in human-AI collaboration across multiple environments. -->
<!-- Status: COMPLETED -->

# 10 Code-Konsistenz & Agent-Workflow

In einem Projekt, in dem KI-Agenten und Menschen Hand in Hand arbeiten, ist **Konsistenz** kein Luxus, sondern eine Überlebensnotiz. Besonders bei multiplen Umgebungen (Conda, Venv, OS-Unterschiede) ist ein klarer Workflow unerlässlich.

### Die "Single Source of Truth"
Um zu verhindern, dass Versionen in verschiedenen Dateien (z. B. `main.py`, `control`, `DOCUMENTATION.md`) auseinanderlaufen, wurde eine zentrale `VERSION`-Datei eingeführt. 
- Ein **automatisierter Test (`tests/test_build_integrity.py`)** prüft bei jedem Build, ob alle Dateien dieselbe Versionsnummer deklarieren.
- Dies verhindert "stille" Inkonsistenzen in den Release-Paketen.

### Agent-Workflow & Dokumentation
KI-Agenten benötigen klare Leitplanken.
1. **Logbuch-Pflicht:** Jede größere Änderung muss im Logbuch dokumentiert werden. Das dient nicht nur dem Menschen als Historie, sondern dem nächsten Agenten als technischer Kontext.
2. **Umgebungs-Validierung:** Das Backend prüft aktiv, ob alle Abhängigkeiten in der aktuellen Umgebung korrekt installiert sind. Ein Agent kann so sofort erkennen, ob ein Fehler am Code oder an der Umgebung liegt.
3. **Automatisierung:** Repetitive Aufgaben (wie das Bauen der `.deb` Pakete) sind in Skripten gekapselt, um menschliche (und künstliche) Fehler zu minimieren.

### Ergebnis
Dieser strukturierte Workflow stellt sicher, dass das Projekt trotz hoher Entwicklungsgeschwindigkeit und wechselnder Bearbeiter stabil und wartbar bleibt. Er ist das "Betriebssystem" hinter dem Code.

<!-- lang-split -->

# 10 Code Consistency & Agent Workflow

In a project where AI agents and humans work hand in hand, **consistency** is not a luxury but a survival requirement. Especially with multiple environments (Conda, Venv, OS differences), a clear workflow is essential.

### The "Single Source of Truth"
To prevent versions in different files (e.g., `main.py`, `control`, `DOCUMENTATION.md`) from diverging, a central `VERSION` file was introduced. 
- An **automated test (`tests/test_build_integrity.py`)** checks during every build whether all files declare the same version number.
- This prevents "silent" inconsistencies in the release packages.

### Agent Workflow & Documentation
AI agents need clear guardrails.
1. **Logbook Requirement:** Every major change must be documented in the logbook. This serves as a history for humans and as technical context for the next agent.
2. **Environment Validation:** The backend actively checks whether all dependencies are correctly installed in the current environment. This allows an agent to immediately identify whether an error is in the code or the environment.
3. **Automation:** Repetitive tasks (such as building `.deb` packages) are encapsulated in scripts to minimize human (and artificial) errors.

### Result
This structured workflow ensures that the project remains stable and maintainable despite high development speed and changing editors. It is the "operating system" behind the code.
