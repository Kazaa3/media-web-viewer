# Logbuch: SVG Library Construction & Application Refactor

## Ziel
Alle System-Icons werden aus Inline-SVGs in eine zentrale SVG-Sprite-Bibliothek ausgelagert und die Anwendung auf die Nutzung von <use xlink:href="#icon-id"> umgestellt.

---

## Phasen & Maßnahmen

### Phase 1: SVG Library Construction
- Alle einzigartigen SVGs aus `app.html` extrahiert.
- Vorbereitung der Symbol-IDs nach Muster `icon-[name]`.

### Phase 2: Application Core Refactor
- **web/icons.svg:**
  - Neue Datei mit `<symbol>`-Definitionen für alle Icons erstellt.
- **app.html:**
  - SVG-Sprite-Loader implementiert: Lädt `icons.svg` und injiziert es als verstecktes `<svg>` am Anfang des `<body>`.
  - Alle Inline-SVGs durch `<svg class="icon"><use xlink:href="#icon-id"></use></svg>` ersetzt.
  - `SVG_PATHS`-Registry im Header-Script auf Symbol-IDs umgestellt.

### Phase 3: CSS Alignment
- **main.css:**
  - `.icon`-Klasse mit Basis-Styles (Größenvererbung, `stroke: currentColor`) ergänzt.

### Phase 4: Final Verification
- Sichtbarkeit aller System-Icons geprüft (Power, Player, Library, Sidebar, HUD etc.).
- Dynamische Header-Injektion und Icon-Farben (inkl. Hover/Active) erfolgreich getestet.
- "STABLE MODE"-Badge und alle dynamischen Icons korrekt referenziert.

---

## Ergebnis
- HTML ist deutlich aufgeräumter, UI-Assets sind zentral steuerbar.
- Icons bleiben visuell konsistent und flexibel orchestrierbar.

---

*Status: SVG-Sprite-Architektur produktiv, weitere Icons können zentral ergänzt werden.*
