<!-- Category: Documentation -->
<!-- Title_DE: Projekt-Genese & Philosophie -->
<!-- Title_EN: Project Genesis & Philosophy -->
<!-- Summary_DE: Die Entstehungsgeschichte von "dict", die Wahl des Tech-Stacks und die Namensphilosophie. -->
<!-- Summary_EN: The origin story of "dict", the technology stack choice, and the naming philosophy. -->
<!-- Status: ACTIVE -->

# Projekt-Genese & Philosophie

## Die Vision hinter "dict"
Die Anwendung startete nicht als fertiges Produkt, sondern als Experiment: Wie lässt sich die Power von Python zur Medienverwaltung mit der Flexibilität moderner Web-Technologien kombinieren? 

### Warum der Name "dict"?
Der Name ist eine Hommage an die Python-Datenstruktur `dict` (Dictionary). Er spiegelt unsere Philosophie wider: **Flexibilität durch Schema-Freiheit.** Alle Medien-Metadaten werden im System als hochgradig anpassbare Dictionaries behandelt, was uns erlaubt, neue Felder für Audio, Video oder E-Books hinzuzufügen, ohne die Grundstruktur zu brechen.

## Der Tech-Stack: Eel & Bottle
Die Entscheidung für den Tech-Stack war strategischer Natur:

1.  **Eel (Frontend-Brücke):** Ermöglicht die Nutzung von HTML5/CSS3/JS für das UI, während das Backend in Python bleibt. Die bidirektionale Bindung (`@eel.expose`) ist das Nervenzentrum.
2.  **Bottle (Streaming Engine):** Da Browser für den Zugriff auf lokale Dateien einen HTTP-Kontext benötigen, wurde Bottle parallel zu Eel integriert. Bottle verwaltet die statischen Routen und ermöglicht das Streaming von Mediendateien direkt von der Festplatte.

## Vom Skelett zum Player
Was als minimalistisches Wireframe begann, entwickelte sich schnell weiter:
- **Phase 1:** Verzeichnisse scannen und Pfade anzeigen.
- **Phase 2:** Integration der HTML5-Audio-API und Playback via Bottle.
- **Phase 3:** Einführung des Glassmorphism-Designs für eine premium User-Experience.

*Diese Phase legte den Grundstein für alles, was folgte – von der Metadaten-Extraktion bis hin zum komplexen Transcoding.*

<!-- lang-split -->

# Project Genesis & Philosophy

## The Vision behind "dict"
The application did not start as a finished product, but as an experiment: how can the power of Python for media management be combined with the flexibility of modern web technologies?

### Why the name "dict"?
The name is an homage to the Python data structure `dict` (dictionary). It reflects our philosophy: **Flexibility through schema freedom.** All media metadata is treated in the system as highly customizable dictionaries, allowing us to add new fields for audio, video or e-books without breaking the basic structure.

## The Tech-Stack: Eel & Bottle
The decision for the tech stack was of a strategic nature:

1.  **Eel (Frontend Bridge):** Enables the use of HTML5/CSS3/JS for the UI, while the backend remains in Python. The bidirectional binding (`@eel.expose`) is the nerve center.
2.  **Bottle (Streaming Engine):** Since browsers require an HTTP context to access local files, Bottle was integrated parallel to Eel. Bottle manages the static routes and enables the streaming of media files directly from the hard drive.

## From Skeleton to Player
What began as a minimalistic wireframe quickly evolved:
- **Phase 1:** Scan directories and display paths.
- **Phase 2:** Integration of the HTML5 Audio API and playback via Bottle.
- **Phase 3:** Introduction of Glassmorphism design for a premium user experience.

*This phase laid the foundation for everything that followed – from metadata extraction to complex transcoding.*
