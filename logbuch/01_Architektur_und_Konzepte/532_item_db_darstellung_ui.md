# Logbuch: Item DB (Übersicht) – Darstellungsfehler & UI-Verbesserung

**Datum:** 15.03.2026

## Problem
In der aktuellen Item-DB-Übersicht im UI gibt es einen Darstellungsfehler:
- Die Kategorie steht rechts, die Aufzählung (Item-Liste) aber links.
- Dadurch wirken Kategorie und Item-Liste nicht als zusammengehörige Einheit.
- Die Gesamtanzahl der Items wird korrekt angezeigt und soll erhalten bleiben.

---

## Ziel
- Die Darstellung der Item-DB-Übersicht soll gestrafft werden, sodass Kategorie und Aufzählung klar zusammengehören.
- Die Information soll vollständig erhalten bleiben, aber die Lesbarkeit und Übersicht verbessert werden.

---

## Empfohlene Maßnahmen für die UI
- Kategorie und Item-Liste nebeneinander oder untereinander, aber optisch als Einheit (z.B. Tabelle, Grid, Card).
- Keine leeren Kategorien anzeigen.
- Die Gesamtanzahl der Items weiterhin sichtbar halten (z.B. als Badge oder in der Überschrift).

---

## Beispiel für eine gestraffte Darstellung (HTML/CSS)

```html
<div class="item-db-overview">
  <div class="item-db-header">
    <span class="item-db-title">Kategorie</span>
    <span class="item-db-title">Items <span class="item-db-count">(Gesamt: 123)</span></span>
  </div>
  <div class="item-db-list">
    <div class="item-db-row">
      <span class="item-db-category">Audio</span>
      <ul class="item-db-items">
        <li>Song 1</li>
        <li>Song 2</li>
      </ul>
    </div>
    <div class="item-db-row">
      <span class="item-db-category">Video</span>
      <ul class="item-db-items">
        <li>Film 1</li>
        <li>Film 2</li>
      </ul>
    </div>
    <!-- Nur Kategorien mit Einträgen anzeigen -->
  </div>
</div>
```

```css
.item-db-overview { display: flex; flex-direction: column; gap: 8px; }
.item-db-header { display: flex; justify-content: space-between; font-weight: bold; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
.item-db-list { display: flex; flex-direction: column; gap: 6px; }
.item-db-row { display: flex; gap: 24px; align-items: flex-start; }
.item-db-category { min-width: 100px; font-weight: 500; color: #2a7; }
.item-db-items { margin: 0; padding-left: 18px; }
.item-db-count { color: #888; font-size: 0.95em; margin-left: 6px; }
```

- Kategorien und Item-Listen erscheinen als optische Einheit.
- Leere Kategorien werden nicht gerendert.
- Die Gesamtanzahl bleibt als Badge/Info sichtbar.
- Die Umsetzung kann flexibel an das bestehende UI angepasst werden.

---

## Ergebnis
- Nach Umsetzung sind Kategorie und Item-Liste klar als Einheit erkennbar.
- Die Übersichtlichkeit ist verbessert, ohne dass Informationen verloren gehen.
- Die Gesamtzahl der Items bleibt für den Nutzer sichtbar.

---

**Siehe auch:**
- [Item-Liste straffen & Item-DB Übersicht](2026-03-15_item_liste_und_db_uebersicht.md)
