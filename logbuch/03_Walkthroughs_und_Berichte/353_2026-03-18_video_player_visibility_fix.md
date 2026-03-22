# Logbuch – 18. März 2026

## Fixing Video Player Visibility

### Problem
Der Nutzer meldete, dass der Video-Player im Tab nur einen schwarzen Bildschirm zeigt, während Picture-in-Picture funktioniert. Das Video wird also gerendert, ist aber im GUI verdeckt oder unsichtbar.

### Analyse
- Die Video-Komponente (`#native-html5-video-resource-node`) war per `display: none` im HTML/CSS initial versteckt.
- Das Platzhalter-Icon war immer sichtbar, auch wenn ein Video geladen wurde.
- Die Sichtbarkeit wurde nicht korrekt umgeschaltet, wenn ein Video geladen oder gestoppt wurde.

### Lösungsschritte
1. **CSS/HTML geprüft:**
    - `display: none` aus dem `<video>`-Tag entfernt.
    - Platzhalter-Icon (`#idle-state-media-icon-symbol`) standardmäßig auf `display: none` gesetzt.
2. **JS-Logik ergänzt:**
    - Neue Funktionen `showVideoPlayer()` und `showIdlePlaceholder()` implementiert.
    - Nach dem Laden/Abspielen eines Videos wird `showVideoPlayer()` aufgerufen, beim Stoppen/Leeren `showIdlePlaceholder()`.
3. **Empfohlene Integration:**
    - Nach erfolgreichem Video-Load/Play: `showVideoPlayer();`
    - Nach Stoppen/Clearing: `showIdlePlaceholder();`

### Beispiel-Code
```js
function showVideoPlayer() {
    const video = document.getElementById('native-html5-video-resource-node');
    const idle = document.getElementById('idle-state-media-icon-symbol');
    if (video) video.style.display = '';
    if (idle) idle.style.display = 'none';
}
function showIdlePlaceholder() {
    const video = document.getElementById('native-html5-video-resource-node');
    const idle = document.getElementById('idle-state-media-icon-symbol');
    if (video) video.style.display = 'none';
    if (idle) idle.style.display = '';
}
```

### Ergebnis
- Video-Player ist nach dem Laden/Abspielen sichtbar.
- Platzhalter verschwindet korrekt.
- Picture-in-Picture und Tab-Playback funktionieren wie erwartet.

**Status:** Gefixt & getestet (18.03.2026)
