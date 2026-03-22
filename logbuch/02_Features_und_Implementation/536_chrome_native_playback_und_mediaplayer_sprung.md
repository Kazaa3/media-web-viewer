# Logbuch: Chrome Native Video/Audio Playback & Mediaplayer-Sprung

**Datum:** 2026-03-15

## Übersicht
Dieses Logbuch dokumentiert die Integration und das Verhalten von Chrome (bzw. Chromium-basierten Browsern) beim nativen Abspielen von Medien (z.B. MP4, WebM, MP3) sowie die Möglichkeit, Medienitems direkt im Browser zu öffnen und gezielt in den eigenen Mediaplayer zu springen.

---

## 1. Chrome Native Playback
- **Beschreibung:**
  - Chrome unterstützt nativ viele Medienformate (z.B. MP4/H.264, WebM, MP3, AAC).
  - Medien, die im nativen Format vorliegen, werden direkt im Browser abgespielt, ohne dass eine Transkodierung oder ein spezieller Embed-Player notwendig ist.
  - Vorteil: Schneller Start, keine zusätzliche Serverlast, volle Browser-Integration (z.B. Picture-in-Picture, Download, Timeline).
- **Technische Umsetzung:**
  - Backend erkennt Dateityp (z.B. .mp4, .webm, .mp3) und liefert die Datei mit passendem MIME-Type aus.
  - Frontend kann einen Direktlink generieren oder das Video/Audio-Tag verwenden.
- **Grenzen:**
  - Nicht alle Formate werden von allen Browsern unterstützt (z.B. kein ALAC/WMA in Chrome).
  - Für inkompatible Formate erfolgt Transkodierung (siehe separates Logbuch).

## 2. Medienitems direkt im Browser öffnen
- **Feature:**
  - Nutzer kann aus der Medienbibliothek heraus ein Item direkt im Browser öffnen (z.B. Rechtsklick → "In neuem Tab öffnen").
  - Alternativ: Button "Im Browser öffnen" neben jedem Item.
- **Vorteile:**
  - Nutzung nativer Browserfunktionen (z.B. Kontextmenü, Download, PiP).
  - Kein Medienplayer-Overhead, ideal für schnelle Vorschau.
- **Technische Hinweise:**
  - Direktlink verweist auf /media/<pfad> oder /video-stream/<pfad> (je nach Dateityp und Modus).
  - Bei unterstütztem Format wird das File direkt angezeigt, sonst erfolgt Fallback auf eigenen Player/Transcoding.

## 3. Sprung in eigenen Mediaplayer
- **Feature:**
  - Aus dem Browser (z.B. nach Vorschau) kann der Nutzer gezielt in den eigenen Mediaplayer zurückspringen (z.B. Button "Im Mediaplayer öffnen").
  - Optional: Automatischer Wechsel, wenn ein Format nicht nativ unterstützt wird.
- **Technische Umsetzung:**
  - Frontend-Event/Callback, das das Item im eigenen Player öffnet (z.B. via Eel-API oder Tab-Switch).
  - Kontext wird erhalten (z.B. aktuelle Position, Metadaten).

## 4. UX/Edge Cases
- **Fallback:**
  - Wenn ein Format nicht nativ unterstützt wird, wird automatisch der eigene Player mit Transcoding/Embed gestartet.
- **Download:**
  - Download-Link für Medien immer anbieten, unabhängig vom Player.
- **Mobile:**
  - Verhalten auf mobilen Browsern testen (z.B. iOS Safari, Android Chrome).

---

## Referenzen
- [web/app_bottle.py](/web/app_bottle.py): Medienausspielung, Transcoding, MIME-Type-Handling
- [web/app.html](/web/app.html): UI-Integration, Direktlinks, Player-Logik
- [src/core/main.py](/src/core/main.py): App-Mode, Parser-Konfiguration

---

## ToDo / Offene Punkte
- [ ] UI-Button "Im Browser öffnen" für alle nativ unterstützten Formate
- [ ] Rücksprung-Mechanismus in eigenen Player (Tab-Switch, Event)
- [ ] Edge-Case-Tests (Unsupported, Mobile, Download)
- [ ] Dokumentation der unterstützten Formate pro Browser

---

*Letzte Änderung: 2026-03-15*
