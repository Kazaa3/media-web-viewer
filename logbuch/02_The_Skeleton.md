<!-- Category: Architecture -->
<!-- Title_DE: 02 Das Skelett: Der erste Wireframe -->
<!-- Title_EN: 02 The Skeleton: The first wireframe -->
<!-- Summary_DE: Rückblick auf den allerersten funktionsfähigen Stand der Anwendung. -->
<!-- Summary_EN: Retrospective on the very first functional state of the application. -->
<!-- Status: COMPLETED -->

# 02 Das Skelett: Der erste Wireframe

Jedes große Projekt beginnt mit einem ersten Schritt. Beim *Media Web Viewer* war dies der "Wireframe"-Stand (Commit `d09a463`).

### Der minimalistische Anfang
In dieser Phase gab es noch keinen Player, kein Transcoding und keine Datenbank. Das Ziel war rein technischer Natur:
1. **Das Fenster öffnen:** Erstmals ein Eel-Fenster mit einer einfachen HTML-Seite anzeigen.
2. **Die Dateiliste:** Python scannt ein Verzeichnis und übergibt eine flache Liste von Dateinamen an JavaScript.
3. **Die Bindung:** Testen, ob Python-Funktionen zuverlässig vom Browser aus aufgerufen werden können.

### Warum dokumentieren wir das?
Dieser Stand markiert den Moment, in dem die Theorie ("Wir bauen einen Web-Player in Python") zur Realität wurde. Es war das Fundament, auf dem alle folgenden komplexen Schichten (Metadaten, SQL, Streaming) aufgebaut wurden.

*Fun Fact: In dieser frühen Phase wurde bereits die Basis für das Glassmorphism-Design gelegt, das bis heute das Gesicht der App prägt.*

<!-- lang-split -->

# 02 The Skeleton: The first wireframe

Every great project starts with a first step. For the *Media Web Viewer*, this was the "Wireframe" state (Commit `d09a463`).

### The Minimalist Beginning
At this stage, there was no player, no transcoding, and no database. The goal was purely technical:
1. **Opening the Window:** Displaying an Eel window with a simple HTML page for the first time.
2. **The File List:** Python scans a directory and hands a flat list of filenames to JavaScript.
3. **The Binding:** Testing if Python functions can be reliably called from the browser.

### Why document this?
This state marks the moment when theory ("Let's build a web player in Python") became reality. It was the foundation upon which all subsequent complex layers (metadata, SQL, streaming) were built.

*Fun Fact: In this early stage, the basis for the Glassmorphism design was already laid, which still defines the face of the app today.*
