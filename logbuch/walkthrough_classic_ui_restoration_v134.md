# Walkthrough – Classic UI Restoration (v1.3.4)

Wir haben das klassische Media Player Layout exakt nach deinem Screenshot wiederhergestellt. Die experimentelle "iPad OS"-Navigation wurde entfernt und durch ein stabiles, hochdichtes Desktop-Design ersetzt.

---

## Key Changes

### 1. Persistent Top Navigation
- Minimalistischer Header ersetzt durch eine vollbreite Navigationsleiste mit allen gewünschten Modulen:
  - **Core:** Player, Library, Browser, Edit, Options, Parser
  - **Diagnostics:** Debug & DB, Tests, Logbook
  - **Extensions:** Video Player, Flags, Features
  - **Global Actions:** Scan Media, Theme Toggle

### 2. Duo-View 'Deck & Queue' Player
- Klassischer Zwei-Spalten-Player:
  - **Linke Spalte (Deck):** Großes Artwork, Metadaten, Tech Specs (Codec, Bitrate, etc.), Dateipfad
  - **Rechte Spalte (Queue):** Scrollbare, kontrastreiche Track-Liste mit Titel, Artist, Album/Track

### 3. Fixed Horizontal Player Footer
- Die schwebende "Pill" wurde durch eine feste Bottom-Bar ersetzt:
  - **Track Info:** Titel/Artist/Artwork links, synchronisiert in Echtzeit
  - **Progress Control:** Breiter Seek-Slider mit Zeitangaben
  - **Pipeline Integration:** HTML5 Audio Controller rechts

### 4. Logic & Interactivity
- **Click-to-Play:** Klick auf eine Track-Card startet sofort die Wiedergabe und aktualisiert das Deck
- **Seeker Sync:** Fortschrittsregler bewegt sich automatisch und erlaubt manuelles Springen
- **Legacy Status Bar:** Schmale Leiste ganz unten mit Version (v1.3.4-Legacy) und Sync-Status

---

## How to use
- **Tabs wechseln:** Über die Buttons in der Top-Navigation
- **Playback:** Items zur Queue hinzufügen (Library/Drag&Drop), im rechten Bereich anklicken
- **Seeking:** Slider im Footer ziehen, um im Track zu springen

> **Tipp:**
> Die Sidebar ist standardmäßig ausgeblendet für maximale Arbeitsfläche, kann aber über das Hamburger-Icon neben dem Audio-Controller im Footer eingeblendet werden.
