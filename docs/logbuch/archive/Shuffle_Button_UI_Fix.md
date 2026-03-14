# Logbuch: Shuffle-Button UI-Fix

**Datum:** 11. März 2026

---

## Problem
Der Shuffle-Button ist im Player-Bereich vorhanden, aber das Unicode-Symbol (🔀) ist optisch und technisch nicht optimal. Das i18n-Label ist korrekt, aber das Icon passt nicht zum UI-Rahmen oder wird nicht überall korrekt dargestellt.

---

## Fix-Strategie
- **Icon ersetzen:** Statt Unicode-Symbol ein SVG-Icon oder ein Icon aus einer etablierten Bibliothek (z.B. Material Icons, FontAwesome) verwenden.
- **i18n-Label beibehalten:** Das data-i18n-Attribut bleibt für die Barrierefreiheit und Übersetzbarkeit erhalten.
- **Button-Design anpassen:** Das neue Icon wird im Button eingebettet, sodass es zum UI-Rahmen passt und überall korrekt angezeigt wird.

---

## Beispiel für SVG-Integration
```html
<button id="btn-shuffle" onclick="toggleShuffle()" class="player-btn" data-i18n="[title]player_btn_shuffle" aria-label="player_shuffle">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 4 L20 20" stroke="#333" stroke-width="2"/>
    <path d="M4 20 L20 4" stroke="#333" stroke-width="2"/>
    <path d="M18 4 L20 4 L20 6" stroke="#333" stroke-width="2"/>
    <path d="M18 20 L20 20 L20 18" stroke="#333" stroke-width="2"/>
  </svg>
</button>
```

---

## Vorteile
- Einheitliches Design, keine Unicode-Probleme.
- Besser skalierbar und anpassbar.
- i18n bleibt erhalten.

---

**TODO:**
- SVG-Icon in app.html einbauen.
- Styling ggf. anpassen.
- Testen auf allen Plattformen.
- Logbuch-Eintrag nach Umsetzung aktualisieren.
