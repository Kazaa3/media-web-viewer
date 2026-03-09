<!-- Category: Architecture -->
<!-- Title_DE: 14 Das Skelett: Der MVP-Ansatz -->
<!-- Title_EN: 14 The Skeleton: The MVP approach -->
<!-- Summary_DE: Rückblick auf den allerersten funktionsfähigen Stand (Eel + Dateiliste). -->
<!-- Summary_EN: Retrospective on the very first functional state (Eel + file list). -->
<!-- Status: COMPLETED -->

# 14 Das Skelett: Der MVP-Ansatz

Jedes große System beginnt mit einem minimalen Skelett. Im Fall des *Media Web Viewer* war das Ziel von Commit `d09a463` denkbar klar: Kann Python eine Web-UI steuern?

### Die Geburtsstunde
In dieser Phase gab es:
- Eine einzelne `main.py`, die ein Eel-Fenster öffnet.
- Ein minimalistisches HTML-File ohne CSS-Schnickschnack.
- Einen trivialen Verzeichnis-Scan, der Namen als String-Liste übergibt.

### Erkenntnis
Trotz der Einfachheit bewies dieser Stand, dass die bidirektionale Kommunikation (Python-Backend <-> JS-Frontend) stabil funktioniert. Es war der Beweis, dass wir auf teure und schwere Frameworks verzichten können, um eine reaktive Desktop-Erfahrung zu schaffen.

<!-- lang-split -->

# 14 The Skeleton: The MVP approach

Every large system begins with a minimal skeleton. In the case of the *Media Web Viewer*, the goal of commit `d09a463` was very clear: Can Python control a web UI?

### The Birth
At this stage there were:
- A single `main.py` opening an Eel window.
- A minimalist HTML file without any CSS fancy.
- A trivial directory scan passing names as a string list.

### Insight
Despite its simplicity, this state proved that bidirectional communication (Python backend <-> JS frontend) works stably. It was proof that we can skip heavy frameworks to create a reactive desktop experience.
