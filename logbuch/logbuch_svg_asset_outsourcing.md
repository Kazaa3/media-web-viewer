# Logbuch: SVG Asset Outsourcing & Centralization

## Ziel
Alle Inline-SVGs werden aus `app.html` in eine zentrale `icons.svg`-Sprite-Bibliothek ausgelagert. Das sorgt für sauberen HTML-Code und zentrale UI-Asset-Verwaltung.

---

## Maßnahmen

### 1. SVG Library Construction
- **icons.svg (NEU):**
  - Enthält `<symbol>`-Definitionen für alle Icons aus `app.html`.
  - IDs nach Muster: `icon-[name]` (z.B. `icon-power`, `icon-refresh`, `icon-player`).
  - Lokale Style-Overrides (z.B. `stroke-width: 3`) werden als CSS-Klassen oder symbol-level Attribute übernommen.

### 2. Application Refactor
- **app.html:**
  - Asset Injection: Script fügt `icons.svg` als verstecktes `<svg>` am Anfang des `<body>` ein (für `<use xlink:href="#id">`).
  - Component Refactor: Alle Inline-`<svg>` werden ersetzt durch:
    ```html
    <svg class="icon"><use xlink:href="#icon-name"></use></svg>
    ```
  - `SVG_PATHS`-Registry verweist jetzt auf Symbol-IDs statt auf Rohdaten.

- **css/main.css:**
  - Basis-Styles für `.icon`-Klasse (Größenvererbung, `stroke: currentColor` etc.) für visuelle Parität.

---

## Verifikation
- Alle Icons (Power, Player, Library, Sidebar, HUD) sind sichtbar und korrekt gefärbt.
- Dynamische Header-Orchestrierung rendert Icons für neue Buttons korrekt.
- "STABLE MODE"-Badge zeigt Icons (falls vorhanden) korrekt an.
- Hover- und Active-States der Buttons behalten Icon-Farbe.

---

*Status: SVG-Assets zentralisiert, HTML aufgeräumt, UI-Assets konsistent steuerbar. Weitere Optimierungen jederzeit möglich.*
