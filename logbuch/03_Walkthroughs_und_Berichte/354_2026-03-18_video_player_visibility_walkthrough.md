# Logbuch – 18. März 2026

## Walkthrough: Video Player Visibility Fix

### Problem
Der Video-Player zeigte einen schwarzen Bildschirm, obwohl das Video (z.B. Vortrag.mp4) abspielte und Picture-in-Picture funktionierte. Ursache: Das "Kein Video ausgewählt"-Placeholder-Icon blieb sichtbar und lag im Layout/z-index über dem Video.

### Lösung
- **Z-Index-Korrektur:**
    - Der Video-Player erhält einen expliziten z-index, sodass er immer über dem Placeholder gestapelt wird.
    - Das Placeholder-Icon wird auf einen niedrigeren z-index gesetzt.
- **Garantiertes Verstecken:**
    - Das Placeholder wird beim Start der Wiedergabe mit `display: none !important` ausgeblendet.
    - Die Video-Komponente wird sichtbar gemacht.
- **Syntax-Fix:**
    - Ein kleiner Syntaxfehler in der Video.js-Initialisierung wurde behoben.

### Ablauf
1. **Vor dem Fix:**
    - Video lädt, aber das Placeholder bleibt sichtbar und verdeckt das Video.
    - PiP funktioniert, aber im Tab bleibt der Player schwarz.
2. **Nach dem Fix:**
    - Beim Start der Wiedergabe wird das Placeholder garantiert ausgeblendet.
    - Der Video-Player ist sichtbar und korrekt gestapelt.
    - PiP funktioniert weiterhin.

### Code-Snippet
```js
function showVideoPlayer() {
    const video = document.getElementById('native-html5-video-resource-node');
    const idle = document.getElementById('idle-state-media-icon-symbol');
    if (video) video.style.display = '';
    if (idle) idle.style.setProperty('display', 'none', 'important');
    // Fallback: re-check after short delay
    setTimeout(() => {
        if (video && idle && video.style.display === 'none') {
            video.style.display = '';
            idle.style.setProperty('display', 'none', 'important');
        }
    }, 200);
}
```

### Test & Verifikation
- Vortrag.mp4 im Video-Player-Tab öffnen.
- Placeholder verschwindet, Video ist sichtbar.
- PiP funktioniert wie erwartet.
- Nach Schließen von PiP bleibt das Video sichtbar.

**Status:** Gefixt & verifiziert (18.03.2026)
