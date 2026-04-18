# Logbuch: Forensic Restoration – Media Visibility & Branch Lock Stabilization

## Problemstellung
- "Audios not playing": Ein Logikrennen im Backend sorgt dafür, dass Items mit Legacy-Kategorien (z.B. 'Musik', 'm4a') von der Branch-Lock-Prüfung gedroppt werden, bevor sie in die Standardkategorie 'audio' normalisiert werden.
- Recovery-Items liefern bei DB-Disconnect keine technische Rückmeldung.

## Maßnahmen
### 1. Filtrationspipeline (Python)
- [MODIFY] main.py
    - Die extension-basierte Kategorisierung (Stage 1.0) wird an den Anfang der Item-Loop verschoben.
    - Die Branch-Lock-Prüfung erfolgt jetzt auf der normalisierten Kategorie.
    - [BRANCH-AUDIT]-Logs zeigen, welche Items warum gedroppt werden.

### 2. Recovery-Orchestrierung (Python)
- [MODIFY] main.py
    - Recovery-Items enthalten jetzt einen Dummy-Pfad (diag.mp3).
    - Im UI wird bei Recovery ein "Service Unavailable"-Toast angezeigt.

### 3. Forensisches Logging (Python)
- [MODIFY] main.py
    - [GHOST-TRACE]-Logs im Drop-Loop für Echtzeit-Audit aller gefilterten Items.

## Verifikation
- [Automatisiert] app.log auf [BRANCH-AUDIT]-Einträge prüfen.
- [Automatisiert] get_library liefert in "Productive"-Mode wieder echte Items.
- [Manuell] Bibliothek öffnen: Echte Audiodateien aus media/ sind sichtbar.
- [Manuell] Play klicken: [PLAY-TRACE] erscheint im Log, Audio startet.

---

*Letztes Update: 18.04.2026*
