# Logbuch – 18. März 2026

## Aggressive Video Player Visibility Fix

### Problem
Der Video-Player zeigte trotz laufender Wiedergabe (PiP funktionierte) einen schwarzen Bildschirm im Tab. Ursache: CSS und State-Management hielten das <video>-Element und die Rendering-Fläche verdeckt oder unsichtbar.

### Implementierte Änderungen
- **Forced Video Tag Visibility:**
    - Initiales `display: none` im <video>-Tag entfernt.
    - Stattdessen `visibility: hidden` als Startwert.
    - Bei Playback: explizit `display: block !important` und `visibility: visible` gesetzt.
- **Redundante Sichtbarkeits-Erzwingung:**
    - Nach dem ersten Sichtbarkeits-Update erfolgt ein zweiter Enforcement-Pass nach 150ms.
    - Dies verhindert, dass Video.js oder Browser-Events das Video versehentlich wieder verstecken.
- **Z-Index & Stacking Restoration:**
    - Der Video.js-Wrapper und das <video>-Element erhalten explizite z-index-Werte.
    - Sie bleiben immer über dem Hintergrund und dem Placeholder gestapelt.
- **Placeholder Suppression:**
    - Das "Kein Video ausgewählt"-Placeholder wird mit `display: none !important` und `visibility: hidden` gleichzeitig ausgeblendet.

### Code-Snippet
```js
function showVideoPlayer() {
    const video = document.getElementById('native-html5-video-resource-node');
    const idle = document.getElementById('idle-state-media-icon-symbol');
    if (video) {
        video.style.setProperty('display', 'block', 'important');
        video.style.setProperty('visibility', 'visible', 'important');
    }
    if (idle) {
        idle.style.setProperty('display', 'none', 'important');
        idle.style.setProperty('visibility', 'hidden', 'important');
    }
    setTimeout(() => {
        if (video) {
            video.style.setProperty('display', 'block', 'important');
            video.style.setProperty('visibility', 'visible', 'important');
        }
        if (idle) {
            idle.style.setProperty('display', 'none', 'important');
            idle.style.setProperty('visibility', 'hidden', 'important');
        }
    }, 150);
}
```

### Ergebnis
- Vortrag.mp4 ist im Video-Player-Tab direkt sichtbar.
- Placeholder verschwindet garantiert.
- PiP und Tab-Playback funktionieren wie erwartet.

**Status:** Gefixt & verifiziert (18.03.2026)
