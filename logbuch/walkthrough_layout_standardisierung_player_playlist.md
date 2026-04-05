# Walkthrough – Layout-Standardisierung: Player & Playlist

## Übersicht
Die visuelle Struktur der Player- und Playlist-Tabs wurde erfolgreich harmonisiert, um ein konsistentes "Links: Sidebar / Rechts: Content"-Erlebnis zu bieten.

---

## Verbesserungen im Detail

### 1. Vereinheitlichte Sidebar-Logik
- **Globale Synchronisierung:** Die globale Sidebar bleibt beim Wechsel zwischen Player- und Playlist-Tab sichtbar und sorgt für ein stabiles UI-Ankergefühl.
- **Konsistente Größe:** Beide Fragmente nutzen jetzt eine Sidebar mit fester Breite (320px) für ihre Listen, was einen nahtlosen Übergang beim Tab-Wechsel ermöglicht.

### 2. Redesign "Big Player"-Erlebnis
- **Queue links:** Die aktive Warteschlange befindet sich jetzt in der linken Sidebar des Player-Tabs.
- **Hero-Content rechts:**
  - Großes, hochauflösendes Artwork zentriert im Hauptbereich.
  - Prominente Titel- und Künstleranzeige.
  - Eigener Bereich für technische Metadaten (Bitrate, Samplerate).

### 3. Optimierter Playlist-Manager
- **Layout-Angleichung:** Der Playlist-Manager folgt exakt demselben Strukturmuster wie der Player.
- **Optimierte Content-Ansicht:** Die rechte Arbeitsfläche für das Playlist-Management ist jetzt aufgeräumter und großzügiger gestaltet.

---

## Verifikation
- **Tab-Wechsel:** Der Wechsel zwischen Player und Playlist fühlt sich durch das identische Layout nahtlos an.
- **Metadaten-Sync:** "Big Player"-Artwork und Infos aktualisieren sich sofort beim Trackwechsel.
- **Sidebar-Interaktion:** Die Queue bleibt in der Sidebar scroll- und interaktiv.

---

**Tipp:**
Der "Big Player"-Modus rechts eignet sich perfekt für entspanntes Zuhören, während die Sidebar links stets die nächsten Titel im Blick hält.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
