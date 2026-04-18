# Logbuch: Forensic Category & Hydration Stabilization

## Problemstellung
- "Real"-Library-Items (Audio/Video) fehlen weiterhin, während Mock-Items gelegentlich erscheinen.
- Ursache: Race Condition beim Hydration-Toggle und zu restriktive Kategorisierungslogik, wodurch Items mit unvollständigen Metadaten "geghostet" werden.

## Maßnahmen
### 1. Hydration-Sequence-Fix (JS)
- [MODIFY] bibliothek.js
    - `refreshLibrary()` und `loadLibrary()` geben jetzt ein Promise zurück oder nutzen ein globales "Hydration Busy"-Flag.
    - `syncQueueWithLibrary()` wird erst im `.then()`-Block nach erfolgreichem Laden der Library aufgerufen.
- [MODIFY] common_helpers.js
    - `setHydrationMode(mode)` nutzt die neue asynchrone Library-Loading-Sequenz.

### 2. Medien-Kategorisierungs-Parität (JS)
- [MODIFY] common_helpers.js
    - Neue Funktion `isAudioItem(item)` und verbesserte `isVideoItem(item)`:
        - Einschluss von Items, bei denen die Kategorie fehlt, aber forensische Metadaten (Bitrate, Duration, Extension) vorhanden sind.
        - Fallback für "unknown"-Items: Sie werden zumindest in der Audio-Queue angezeigt, statt zu verschwinden.

### 3. Rendering-Stabilität (JS)
- [MODIFY] audioplayer.js
    - Loops in `renderAudioQueue` und `renderPhotoQueue` so angepasst, dass Medientyp-Kollisionen vermieden werden, aber die "Alle Medien"-Ansicht vollständig bleibt.

## Verifikation
- Durchschalten der M/R/B-Buttons aktualisiert Count und Listen korrekt (kein Race Condition mehr).
- "Real"-Audio-Items (auch ohne explizite Kategorie) erscheinen jetzt in der Queue.
- Im Konsolen-Log erscheinen `[Hydration-Done]`-Meldungen, bevor der UI-Refresh-Pulse startet.

---

*Letztes Update: 18.04.2026*
