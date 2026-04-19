# Logbuch: Visual Restoration – 'Perfect' Reference Alignment

## Ziel
Die Forensic Splits (Deck und Queue) werden exakt an das "perfekte" Legacy-Layout aus dem Referenz-Screenshot angepasst. Forensische Marker werden entfernt, das Design wird klar, kontrastreich und aufgeräumt.

---

## Maßnahmen

### 1. Header Renaming
- "Media Queue" wurde in **Mediengalerie** umbenannt (rechte Spalte).

### 2. Visualizer Integration
- Im linken Split (Deck) wurde ein `<canvas id="sidebar-visualizer-canvas">` am unteren Rand eingefügt.
- Die Visualizer-Engine rendert nun dynamische, blaue Balken im Hintergrund (wie im Referenz-Design).

### 3. Metadata Simplification
- Die technische Grid-Box (Codec, Bitrate, etc.) wurde entfernt.
- Stattdessen: Einzeilige Darstellung, z.B. `mp3 | 320kbps | 44.1kHz` unterhalb der Tags.

### 4. Split View Structure
- **Links (Deck):**
  - Breite auf 45% oder fix (z.B. 480px) erhöht.
  - Forensische Proof-Tags entfernt.
- **Rechts (Mediengalerie):**
  - Header `<h3>Mediengalerie</h3>`
  - Count-Badge als cyanfarbene Pill: `33 Titel`
  - Alle forensischen Marker entfernt.

### 5. Hydration & Visuals
- **audioplayer.js:**
  - `updateMediaSidebar` aktualisiert, um die neue Tech-String-Zeile zu befüllen.
  - `drawVisualizer` rendert auf den neuen Canvas im Sidebar-Deck.

### 6. Navigation Parity
- **config_master.py:**
  - Sub-Nav-Labels werden ggf. nach User-Feedback angepasst ("Mediengalerie" vs. "PLAYLIST MANAGER").

---

## Offene Fragen
- Soll die Sub-Nav "Mediengalerie" oder "PLAYLIST MANAGER" heißen?
- Sollen die Visualizer-Balken blau (wie im Referenz) oder in der aktuellen Akzentfarbe erscheinen?

---

## Verifikation
- Splits sind balanciert (links: Artwork/Tags, rechts: Liste).
- Live-Visualizer-Balken erscheinen hinter den Artwork-Infos.
- "Mediengalerie"-Titel und Badge stimmen mit dem Screenshot überein.

---

*Status: Visuelle Wiederherstellung gemäß Referenz abgeschlossen. Feintuning nach User-Feedback möglich.*
