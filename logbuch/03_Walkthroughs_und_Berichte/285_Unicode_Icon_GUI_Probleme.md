# Logbuch: Unicode-Icon-Unterstützung in GUI

**Datum:** 11. März 2026

---

## Problem
Unicode-Icons (z.B. ■, 🔀, 🔁, ⏪, ⏩, ⏱️, 🎚️) werden in der GUI nicht überall korrekt angezeigt – weder im Chrome-Browser noch in Python-IDE (VS Code). Ursache sind fehlende oder inkompatible Systemfonts und unterschiedliche Font-Engines.

---

## Analyse
- Viele Unicode-Symbole sind nur in modernen Emoji-Fonts enthalten (z.B. Segoe UI Emoji, Noto Color Emoji).
- Browser und IDE nutzen unterschiedliche Standard-Fonts, die nicht alle Symbole abdecken.
- Python-IDE zeigt Unicode oft nur als Platzhalter oder Rechteck.
- Web-GUI kann Unicode-Icons nur anzeigen, wenn der Font auf dem System vorhanden ist.

---

## Empfehlungen
- **Web:** SVG-Icons oder Icon-Bibliotheken (Material Icons, FontAwesome) verwenden, statt Unicode.
- **Python/CLI:** Fallback-Text oder ASCII-Symbole nutzen, wenn Unicode nicht unterstützt wird.
- **VS Code:** Font-Einstellungen prüfen, ggf. „Noto Color Emoji“ oder „Segoe UI Emoji“ aktivieren.
- **Barrierefreiheit:** i18n-Labels und ARIA-Attribute beibehalten.

---

## Fazit
Unicode-Icons sind praktisch, aber nicht überall zuverlässig. Für professionelle GUI immer SVG/Icon-Bibliothek verwenden. Unicode nur als Fallback.

---

**TODO:**
- Web-GUI auf SVG/Icon-Bibliothek umstellen.
- Python-CLI mit Fallback-Symbolen ausstatten.
- Logbuch-Eintrag nach Umsetzung aktualisieren.
