<!-- Category: Architecture -->
<!-- Title_DE: Architektur: Eel & Python Hybrid -->
<!-- Title_EN: Architecture: Eel & Python Hybrid -->
<!-- Summary_DE: Grundlagen der hybriden Architektur mit Eel und Python. -->
<!-- Summary_EN: Foundations of the hybrid architecture using Eel and Python. -->
<!-- Status: COMPLETED -->

# Architektur: Eel & Python Hybrid

Die Grundentscheidung für die Architektur des *Media Web Viewer* fiel auf eine hybride Lösung: ein **HTML/JS Frontend** kombiniert mit einem **Python Backend**, verbunden über das **Eel Framework**.

### Warum diese Wahl?
1. **Frontend-Flexibilität:** Moderne UIs lassen sich mit Web-Technologien (CSS Grid, Flexbox, Glassmorphism) schneller und ansprechender gestalten als mit klassischen Python-GUI-Frameworks wie Tkinter oder PyQt.
2. **Python-Power:** Für rechenintensive Aufgaben wie das Scannen von Verzeichnissen, die Extraktion von Metadaten (Mutagen) und die Interaktion mit System-Tools (FFmpeg) ist Python ideal.
3. **Leichtgewichtig:** Eel nutzt einen installierten Chrome/Chromium-Browser als "Laufzeitumgebung", was das App-Bundle klein hält im Vergleich zu Electron.

### Funktionsweise
Die Kommunikation erfolgt bidirektional über **WebSockets**:
- **Backend -> Frontend:** Python-Funktionen werden als `@eel.expose` markiert und können direkt von JavaScript aufgerufen werden.
- **Frontend -> Backend:** JavaScript-Funktionen können ebenfalls exponiert und von Python getriggert werden (z.B. für Status-Updates während eines Scans).

Diese Struktur bildet das Fundament für die gesamte Reaktionsfähigkeit und Wartbarkeit der Anwendung.

<!-- lang-split -->

# Architecture: Eel & Python Hybrid

The core architectural decision for the *Media Web Viewer* was a hybrid solution: an **HTML/JS frontend** combined with a **Python backend**, connected via the **Eel framework**.

### Why this choice?
1. **Frontend Flexibility:** Modern UIs can be designed much faster and more attractively with web technologies (CSS Grid, Flexbox, Glassmorphism) than with classic Python GUI frameworks like Tkinter or PyQt.
2. **Python Power:** For computationally intensive tasks such as scanning directories, extracting metadata (Mutagen), and interacting with system tools (FFmpeg), Python is ideal.
3. **Lightweight:** Eel uses an installed Chrome/Chromium browser as its "runtime environment," which keeps the app bundle small compared to Electron.

### How it works
Communication is bidirectional via **WebSockets**:
- **Backend -> Frontend:** Python functions are marked with `@eel.expose` and can be called directly from JavaScript.
- **Frontend -> Backend:** JavaScript functions can also be exposed and triggered by Python (e.g., for status updates during a scan).

This structure forms the foundation for the overall responsiveness and maintainability of the application.
