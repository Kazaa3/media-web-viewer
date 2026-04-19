# Logbuch – v1.41.08 Safe-Boot & Handshake-Schutz

Ich habe das ausfallsichere Boot-Konzept für die GUI spezifiziert und in vier Phasen gegliedert, um Backend-Hänger und schwarze Bildschirme endgültig zu verhindern.

---

## Maßnahmen & Phasen

### Phase 1: Safe-Init Logic (JS)
- **2s Timeout:** eel.get_ui_settings in ui_core.js wird mit einem 2-Sekunden-Timeout versehen. Bleibt die Antwort aus, startet die GUI im Safe-Mode mit Standard-Header und Untermenü.
- **5s Emergency Reveal:** Ein Watchdog-Timer entfernt nach spätestens 5 Sekunden alle Lade-Overlays und erzwingt die Sichtbarkeit der Hauptcontainer.

### Phase 2: Navigation Redundancy (JS)
- **Fallbacks:** updateGlobalSubNav in ui_nav_helpers.js erhält eine zuverlässige Fallback-Logik, die das Untermenü auch bei DOM-Problemen nachbefüllt.
- **Status-Mapping:** Die Zuordnung der STATUS-Kategorie und ihrer Pills wird finalisiert.

### Phase 3: Structural Lockdown (CSS)
- **Kein display: none:** Die Regel body.mwv-hide-subnav #sub-nav-container wird so angepasst, dass nur noch height: 0 und overflow: hidden gesetzt werden. Das Layout bleibt stabil, auch wenn das Untermenü temporär ausgeblendet ist.

### Phase 4: Verification
- **Boot-Test:** Start mit absichtlich verzögertem Backend – die GUI muss nach 2s im Safe-Mode erscheinen.
- **Sub-Menu-Test:** Wechsel durch alle Kategorien, das Untermenü bleibt sichtbar und aktualisiert sich korrekt.

---

Mit diesem Konzept ist die GUI gegen Backend-Ausfälle und Ladefehler abgesichert. Die Sichtbarkeit und Bedienbarkeit ist jederzeit gewährleistet.
