# Logbuch: Playlist- und Parser-UI – Unicode-Icon-Revert (Revert auf Emoji/Text)

**Datum:** 2026-03-15

## Übersicht
Dieses Logbuch dokumentiert das gezielte Zurücksetzen (Revert) von SVG-Icons auf Unicode/Emoji-Icons in der Playlist- und Parser-UI. Ziel ist maximale Klarheit, Lesbarkeit und Kompatibilität.

---

## Änderungen (Revert auf Unicode/Emoji)

### Playlist-Item-Buttons
- **Grab Handle:**
  - Revert von SVG auf Unicode ☰ (U+2630)
- **Remove Button:**
  - Revert von SVG auf Unicode ❌ (U+274C)
- **Movement Buttons (Up/Down):**
  - Revert von SVG auf Unicode 🔼 (U+1F53C) und 🔽 (U+1F53D)

### Playlist-Header-Badges
- **Save:** 💾 (U+1F4BE)
- **Load:** 📂 (U+1F4C2)
- **Shuffle:** 🔀 (U+1F500)
- **Clear:** 🗑️ (U+1F5D1)
- **Up:** 🔼 (U+1F53C)
- **Down:** 🔽 (U+1F53D)

### Parser-Tab
- **Grab Handle:**
  - Revert von SVG auf Unicode ☰ (U+2630) in der Parser-Konfigurationsliste

---

## Motivation
- **Klarheit & Lesbarkeit:** Emojis sind sofort verständlich und systemweit konsistent.
- **Kompatibilität:** Unicode-Icons funktionieren in allen modernen Browsern und auf allen Plattformen.
- **Wartbarkeit:** Weniger CSS/Mask-Overhead, einfachere UI-Anpassung.

---

## ToDo
- [ ] Sicherstellen, dass alle betroffenen Buttons wieder Unicode/Emoji verwenden
- [ ] UI-Regressionstest auf allen Plattformen
- [ ] Dokumentation der Unicode-Codes für zukünftige Referenz

---

*Letzte Änderung: 2026-03-15*
