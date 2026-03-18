# Logbuch Eintrag 022: Video Player Visibility & Sidebar Sync

## Datum: 2026-03-18
## Status: In Progress / Execution Finished

### Problemstellung
1. **Video Player Sichtbarkeit**: Das Video wurde im GUI-Tab nicht angezeigt (nur Schwarzbild), obwohl es im PiP-Modus (Picture-in-Picture) korrekt lief. Die Audiowiedergabe funktionierte ebenfalls.
2. **Sidebar Synchronisation**: Bei Videodateien wurde die Sidebar-Metadaten-Anzeige nicht aktualisiert; es blieb das Artwork/Titel des vorangegangenen Audio-Songs stehen.
3. **Player Controls**: Der Player wurde vom User als "unvollständig" empfunden (insb. Spulen und UI-Vollständigkeit).

### Implementierte Fixes
1. **Forced Visibility (z-index & display)**:
    - Der native HTML5 `<video>` Tag wurde von `display: none` auf `visibility: hidden` im Idle-State umgestellt.
    - In der Funktion `startEmbeddedVideo` wird nun explizit `display: block !important` und `visibility: visible` auf das Video-Element (die "Tech" von Video.js) angewendet.
    - Der Video.js Wrapper erhält einen hohen `z-index: 50`, um sicherzustellen, dass er vor dem Placeholder liegt.
    - Der Placeholder (`Kein Video ausgewählt`) wird nun mit `!important` ausgeblendet und in der z-Ebene nach hinten verschoben (`z-index: -1`).

2. **Sidebar Metadata Refactoring**:
    - Die Metadaten-Update-Logik wurde aus der `play()`-Funktion in eine eigenständige Funktion `updateMediaSidebar(item, path)` extrahiert.
    - Diese wird nun für **Audio und Video** gleichermaßen aufgerufen, sodass bei jedem Playback-Start die Sidebar (Titel, Artist, Artwork, Parser-Zeiten, Kapitel) aktualisiert wird.
    - Die Logik wurde robuster gegenüber fehlenden Tags gestaltet (Fallback auf `item.name`).

3. **Player UI Vervollständigung**:
    - (Geplant/In Arbeit) Integration eines dedizierten Seek-Sliders in die Advanced Controls, falls die Video.js Controls nicht ausreichen oder verdeckt sind.

### Verifikation
- [x] Syntax-Fehler in `app.html` behoben.
- [x] Sidebar aktualisiert sich nun bei Video-Start.
- [ ] Test mit `Vortrag.mp4` durch den User steht noch aus.

---
*Erstellt durch Antigravity (AI Assistant)*
