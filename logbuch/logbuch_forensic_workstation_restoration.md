# Logbuch: Forensic Workstation Restoration (Legacy Host Protocol)

## Hintergrund
Der User hat den 'rebuild'-Modus explizit abgelehnt, da dieser als Fehlerquelle identifiziert wurde. Ziel ist die Wiederherstellung und Reparatur der klassischen GUI (Legacy Shell app.html), wobei die forensischen Split-Views sichtbar und funktionsfähig bleiben sollen.

---

## Geplante Änderungen (Konzept)

### Backend-Konfiguration
- **config_master.py**
  - Setze `ui_evolution_mode` auf `'stable'` (Zeile 284).
  - Setze das verschachtelte `evolution_mode` unter `ui_registry` auf `'stable'` (Zeile 531).
  - Ergebnis: `app.html` wird als Entry-Point genutzt (wie gewünscht: „in der alten ist schon alles da“).

### UI Proof of Life (Hardcoding)
- **app.html**
  - Harte Identifikations-Tags am Anfang der Haupt-Viewports einfügen:
    - `#player-main-viewport`: `<div id="proof-player" style="background: #ff3366; color: white; font-weight: 900; padding: 5px; font-size: 10px; z-index: 10000;">⚡ PLAYER SPLIT ACTIVE</div>`
    - `#rebuild-stage`: `<div id="proof-stage" style="background: #007aff; color: white; font-weight: 900; padding: 5px; font-size: 10px; z-index: 10000;">⚡ FORENSIC STAGE ACTIVE</div>`

### Frontend-Orchestrierung
- **app_core.js**
  - Fragment-Registrierungen anpassen, um Kompatibilität mit `app.html` sicherzustellen.
  - Sicherstellen, dass `fragments/player_queue.html` (oder bevorzugter Split) korrekt geladen wird.

### Playlist Safety Audit
- **playlists.js**
  - Guard-Clauses in `syncQueueWithLibrary`, um Abstürze bei leeren/fehlerhaften Listen zu verhindern.
  - `renderAudioQueue`-Aufruf in try-catch-Block einbetten.

---

## Offene Fragen
- Soll `rebuild/audioplayer.html` (mit den zwei Mounts) innerhalb von `app.html` bleiben, oder lieber klassisches `player_queue.html`?
- „two splits are black“: Bezieht sich das auf Sidebar vs. Content in `app.html` oder auf die Left/Right-Splits im neuen Audioplayer?

---

## Verifikationsplan
- App starten und prüfen, dass `app.html` geladen wird (Standard: Light Theme).
- Sichtbarkeit der roten/blauen Proof-of-Life-Tags am oberen Rand des Content-Bereichs prüfen.
- Library-Sync auslösen und sicherstellen, dass keine Abstürze im Konsolen-Log auftreten.

---

**Status:**
Konzept archiviert. Umsetzung wurde nicht ausgeführt.
