# 01 Die Evolution von dict: Vom Skelett zum Playback

Dieses Dokument fasst die technische Genese, die Namensphilosophie und die ersten Meilensteine des Projekts zusammen.

## Das Skelett: Der Ursprung
Die Anwendung startete als minimalistisches "Wireframe". Das Ziel war rein technischer Natur: Ein Eel-Fenster öffnen, Verzeichnisse scannen und die bidirektionale Bindung zwischen Python und JavaScript testen. Das heute prägende Glassmorphism-Design wurde bereits in dieser Phase grundgelegt.

### Warum Eel & Python?
Nach dem Wireframe fiel die strategische Entscheidung für **Eel**. Dies ermöglichte uns Frontend-Freiheit durch HTML5/CSS3 bei gleichzeitiger Backend-Power durch Python zur Kontrolle des Dateisystems. Die direkte Kommunikation via `@eel.expose` bildete das Rückgrat der Interaktion.

### Warum "dict"?
Der Name spiegelt unsere Kernphilosophie wider: Die Nutzung von Python-Dictionaries als primäre, flexible Datenstruktur. Diese Wahl ermöglichte eine schnelle Iteration ohne starre Schemata und bildet bis heute das Fundament der gesamten Datenverarbeitung - von Scrapern bis zur GUI-Kommunikation.

## Meilenstein: Das erste Playback via Bottle
Während Eel die Benutzeroberfläche steuert, benötigt der Browser für das Abspielen von Medien einen richtigen Web-Endpunkt.

### Integration von Bottle
In der frühen Phase wurde das **Bottle Web Framework** integriert. Bottle läuft parallel zu Eel im Hintergrund und erfüllt einen spezifischen Zweck:
- **Statische Routen:** Bereitstellung von Mediendateien über dedizierte URLs wie `/media/<path>`.
- **Streaming:** Ermöglicht es dem HTML5-Audio-Element, Musik direkt von der Festplatte zu laden, als käme sie aus dem Internet.

Dies war der Moment, in dem aus einem reinen Verzeichnis-Scanner ein funktionsfähiger **Player** wurde.

## Format-Vielfalt: ALAC, M4A & Co.
Ein einfacher MP3-Player reicht nicht aus. Die nächste Stufe war die Unterstützung von Formaten jenseits des Standards.

### Fokus auf Qualität
Besonderes Augenmerk lag auf **ALAC (Apple Lossless)** und dem **M4A/M4B Container**. Da Browser ALAC oft nicht nativ unterstützen, legte dies den Grundstein für unsere **Metadaten-Pipeline** und spätere Transcoding-Überlegungen. Es zeigte sich schnell, dass eine reine Dateiendungs-Prüfung zu kurz greift und tiefere Header-Analysen notwendig sind.

## Technologie-Schuld & Archäologie
Durch die Analyse der Historie haben wir kritische Versäumnisse aufgearbeitet:
1. **Parser-Pipeline**: Refactoring zu einem robusten Handler-Pattern.
2. **Session-Management**: Behebung von "Stale Session" Bugs.
3. **Umgebungs-Isolation**: Migration zu isolierten Virtual Environments (venv).
