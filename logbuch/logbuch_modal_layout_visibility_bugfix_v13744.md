# Logbuch v1.37.44 – Modal Layout & Visibility Bugfix

**Datum:** 2026-04-06

## Problemstellung
Die Buttons "Neuer Eintrag" (Logbuch) und "✏️ Bearbeiten" (Tests & Logbuch) öffneten ihre Pop-up-Modals nicht korrekt. Wurden sie geöffnet, waren die Formulare oft abgeschnitten oder die Buttons "Abbrechen" und "Speichern" auf kleinen Bildschirmen nicht sichtbar, sodass keine Änderungen gespeichert oder verworfen werden konnten.

## Ursachenanalyse
- **Unvollständiger HTML-Container:** Das feature-status-modal ("Projekt-Status & Features") fehlte ein schließendes </div> (Zeile 1232 in app.html). Dadurch wurden alle nachfolgenden Modals zu DOM-Kindern dieses Modals und erbten dessen display: none.
- **CSS-Konflikt:** Die Modals in web/app.html hatten sowohl display: none; als auch display: flex; in den Inline-Styles, was zu Konflikten beim Umschalten führte.
- **JavaScript-Logik:** Die Funktion openTestEditModal setzte style.display = 'block', was das Flexbox-Layout zerstörte.
- **Viewport-Overflow:** Es fehlte eine max-height-Beschränkung, sodass die Action-Bar (Speichern/Abbrechen) aus dem sichtbaren Bereich rutschte.

## Lösungen
1. **HTML-Fix:** Fehlendes </div> an Zeile 1232 ergänzt, sodass alle Modals wieder korrekt im DOM platziert sind.
2. **CSS-Bereinigung:** display: flex; aus den Inline-Styles entfernt, Modals starten jetzt sauber mit display: none;.
3. **JS-Korrektur:** openTestEditModal setzt jetzt style.display = 'flex', damit das Flexbox-Layout erhalten bleibt.
4. **Viewport-Constraint:** max-height: 80vh; für Modals eingeführt, damit sie nie mehr als 80% der Bildschirmhöhe einnehmen.
5. **Scrollbare Inhalte:** overflow-y: auto; für die Content-Wrapper, damit Felder scrollbar bleiben und Action-Bar immer sichtbar ist.
6. **Python-Bugfix:** Typo in main.py (Zeile 518) von @eel.exposes zu @eel.expose korrigiert.
7. **Logbuch-Speicher-Fix:** saveLogbookEntry übergibt jetzt den echten Dateinamen (currentLogbookEditFilename) statt des UI-Anzeigenamens an das Backend. Korrupte Dateien wurden entfernt.

## Verifikation
- Logbuch-Tab öffnen, "➕ Neuer Eintrag" testen: Modal öffnet korrekt, Action-Bar sichtbar.
- "✏️ Bearbeiten" bei Logbuch- und Test-Einträgen testen: Modal öffnet, Buttons sichtbar.
- Modals auf kleinen Bildschirmen prüfen: Inhalte scrollbar, Action-Bar bleibt sichtbar.

---
**Status:** Modal-Layout- und Sichtbarkeits-Bug behoben, manuelle Verifikation empfohlen (v1.37.44)
