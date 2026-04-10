# Walkthrough - Audio Player Layout & Sidebar Restoration (v1.35.98)

## Zusammenfassung
Der Dual-Pane-Layout des Audio Players wurde wiederhergestellt, das "Black Screen"-Problem durch einen HTML-Strukturfehler behoben und eine globale Konfiguration zum standardmäßigen Ausblenden der vertikalen Sidebar implementiert.

---

## Key Restoration Measures

### 1. Audio Player Layout & Splitter Restoration
- **Premium Sidebar & Queue:** Das klassische Duo-View-Layout für den Audio Player ist zurück. Die Premium Sidebar (Artwork & Metadaten) ist links fixiert, die Queue/Item-Liste rechts.
- **Interactive Splitter:** Ein vertikaler, resizbarer Splitter trennt Sidebar und Queue. Beide Spalten sind auf `overflow-y: auto` gesetzt und unabhängig scrollbar – auch bei großen Playlists oder viel Metadaten.
- **View Integrity:** Flex-Container-Sizing in `player_queue.html` korrigiert, damit das Layout immer den gesamten Viewport ausfüllt und nicht mehr in ein "schwarzes Loch" kollabiert.

### 2. Root Cause Fix: Header Structural Integrity
- **Repaired Malformed HTML:** Kritischer Strukturfehler im Master-Header (`app.html`) behoben. Mehrere ungeschlossene und redundante `<div>`-Tags führten dazu, dass der Browser den Hauptinhalt als Teil des Headers interpretierte – Ursache für den "alles ist schwarz"-Fehler.

### 3. Global Configuration & Sidebar Persistence
- **Config-Driven Visibility:** `sidebar_visible: False` zur `GLOBAL_CONFIG`-Registry in `src/core/config_master.py` hinzugefügt.
- **Frontend Synchronization:** Die Initialisierungslogik im Frontend (`common_helpers.js`) liest dieses Setting aus. Die vertikale Sidebar bleibt beim Start standardmäßig ausgeblendet und sorgt für ein aufgeräumtes Interface.
- **Header Toggle:** Die Sidebar kann weiterhin per Button im Header oder per Footer-Icon ein- und ausgeblendet werden.

---

## Verification Steps
- **Audio View:** "Player" auswählen, um das Split-View mit Splitter zu sehen.
- **Sidebar:** Die vertikale Sidebar ist beim Start geschlossen.
- **Stability:** Das Hauptlayout ist strukturell stabil und sollte nicht mehr in einen "Black Hole"-Zustand geraten.
