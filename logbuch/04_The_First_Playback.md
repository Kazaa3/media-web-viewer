<!-- Category: Development -->
<!-- Title_DE: 03 Das erste Playback: Medien-Serving via Bottle -->
<!-- Title_EN: 03 The First Playback: Media serving via Bottle -->
<!-- Summary_DE: Wie die App lernte, Musik abzuspielen – die Integration von Bottle. -->
<!-- Summary_EN: How the app learned to play music – the integration of Bottle. -->
<!-- Status: COMPLETED -->

<!-- Anchor: 04_The_First_Playback -->
<!-- Redundancy: Section covers Bottle integration, media serving, GUI/data separation. -->

# 03 Das erste Playback: Medien-Serving via Bottle

Während Eel die Benutzeroberfläche steuert, reichte es für das Abspielen von Medien nicht aus, einfach nur Dateipfade an JavaScript zu senden. Der Browser benötigt einen richtigen Web-Endpunkt, um Binärdaten zu stkJreamen.

### Der Medien-Server
In Commit `c565084` wurde das **Bottle Web Framework** integriert. Bottle läuft parallel zu Eel im Hintergrund und erfüllt einen spezifischen Zweck:
- **Statische Routen:** Bereitstellung von Mediendateien über dedizierte URLs wie `/media/<path>`.
- **Streaming:** Ermöglicht es dem HTML5-Audio-Element, Musik direkt von der Festplatte zu laden, als käme sie aus dem Internet.

### Der Durchbruch
Dies war der Moment, in dem aus einem reinen Verzeichnis-Scanner ein funktionsfähiger **Player** wurde. Die Trennung zwischen der GUI (Eel) und dem Daten-Provider (Bottle) ist bis heute ein zentraler Pfeiler der Performance und Stabilität der Anwendung.

<!-- lang-split -->

# 03 The First Playback: Media serving via Bottle

While Eel controls the user interface, it wasn't enough to simply send file paths to JavaScript for media playback. The browser needs a proper web endpoint to stream binary data.

### The Media Server
In commit `c565084`, the **Bottle web framework** was integrated. Bottle runs in the background parallel to Eel and serves a specific purpose:
- **Static Routes:** Providing media files via dedicated URLs like `/media/<path>`.
- **Streaming:** Allows the HTML5 audio element to load music directly from the hard drive as if it were coming from the internet.

### The Breakthrough
This was the moment when a simple directory scanner became a functional **player**. The separation between the GUI (Eel) and the data provider (Bottle) remains a central pillar of the application's performance and stability today.
