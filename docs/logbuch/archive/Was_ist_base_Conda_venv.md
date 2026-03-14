# Was bedeutet "base" bei Python/Conda?

**Datum:** 12. März 2026



## Warum wird "base" angezeigt, wenn eine venv aktiv ist?

- Das Terminal aktiviert oft automatisch die Conda base-Umgebung beim Start (z.B. durch eine Zeile in ~/.bashrc oder ~/.zshrc).
- Wenn danach eine venv aktiviert wird, bleibt "(base)" im Prompt sichtbar, aber Python nutzt die venv.
- Das ist rein kosmetisch und hat keinen Einfluss auf die Python-Umgebung.
- Um das zu ändern, kann die automatische Conda-Aktivierung aus der Shell-Konfiguration entfernt werden. Dann erscheint "(base)" nur, wenn Conda bewusst aktiviert wird.


- **"base"** bezeichnet die Standardumgebung von Conda, die beim Start von Conda immer vorhanden ist.
- Wenn im Terminal `(base)` angezeigt wird, ist die Conda-Basisumgebung aktiv.


## Verbindung von venv und Conda

- Eine venv kann im Kontext einer aktiven Conda-Umgebung erstellt werden und übernimmt dann deren Python-Interpreter.
- Die venv bleibt für Python-Pakete isoliert, Conda beeinflusst nur systemweite Tools und Umgebungsvariablen.
- Es wird immer nur ein Python-Interpreter verwendet – die venv übernimmt die Kontrolle für Python.

## IDE-Hinweis

- IDEs (z.B. VS Code, PyCharm) können venv und Conda automatisch verknüpfen, wenn die venv im Conda-Kontext erstellt wurde.
- Falls dies unerwünscht ist, kann es nötig sein, die venv außerhalb einer aktiven Conda-Umgebung zu erstellen oder die IDE-Einstellungen anzupassen.
- Eine venv (z.B. `.venv_build`) läuft unabhängig von Conda und nutzt nur die darin installierten Python-Pakete.
- Wenn beide Umgebungen aktiviert sind, hat die venv für Python-Befehle Vorrang.

---

## Typische Szenarien

- `(base)` und `.venv_build` gleichzeitig im Prompt:
  - Python nutzt die venv, Conda-Befehle (z.B. `conda install`) wirken auf die base-Umgebung.
- Nur `.venv_build` im Prompt:
  - Vollständig isolierte Python-Umgebung, keine Conda-Einflüsse.

---

## Fazit

- Die venv ist für Python-Projekte meist ausreichend und unabhängig.
- "base" ist nur relevant, wenn Conda-spezifische Pakete oder Umgebungen benötigt werden.

---

*Entry created: 12. März 2026*
