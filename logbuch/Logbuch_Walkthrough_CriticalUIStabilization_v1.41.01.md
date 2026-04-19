# Logbuch – v1.41.01 Kritische UI-Stabilisierung

Ich habe die kritischen UI-Fehler in v1.41.01 behoben:

---

## 🚀 Fixes im Überblick

- **Icons Rechts:**
  - Dem Header wurde `display: flex` hinzugefügt. Das Logo und die Navigation bleiben links, und das Icon-Cluster (Pulsar, Split, Trash) wird nun wieder korrekt nach ganz rechts geschoben.

- **Untermenü Fix:**
  - Eine Variablen-Inkonsistenz in der `app.html` wurde behoben. Die Pill-Navigation (Warteschlange, Playlist etc.) nutzt jetzt die dynamische Höhenvariable des Orchestrators und ist wieder sichtbar.

- **Black Screen Fix:**
  - Das Hauptproblem war, dass in der `app.html` noch hartcodierte `style="display: none;"`-Attribute an den Tab-Containern hingen. Diese haben die neuen CSS-Regeln überschrieben. Ich habe alle diese Overrides entfernt.

- **Sync-Trigger:**
  - Der Kategoriewechsel in der `ui_nav_helpers.js` triggert jetzt sofort den Orchestrator (`MWV_UI.apply`), um die Geometrie und Offsets ohne Verzögerung zu aktualisieren.

---

**Details findest du im Abschlussbericht:** walkthrough.md

Die UI ist nun stabil: Das Untermenü ist da, die Icons sitzen rechts und die Inhaltsfenster (z.B. Bibliothek) sind wieder sichtbar.
