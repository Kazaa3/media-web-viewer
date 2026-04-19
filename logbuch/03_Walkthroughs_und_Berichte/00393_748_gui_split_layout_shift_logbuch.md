---

# Logbuch-Eintrag: Unerwünschte Layout-Verschiebung nach DIV-Reparatur (März 2026)

## Kontext

Nach der Reparatur der DIV-Struktur (z.B. Entfernen/Einfügen von schließenden Containern) tritt teilweise der gegenteilige Effekt auf: Die Unterseiten/Subpanels, die eigentlich im vertikalen Split (linke Navigation) angezeigt werden sollen, rutschen plötzlich in den horizontalen Bereich (z.B. Haupt-Content oder Tab-Panel).

---

## Beobachtungen
- Nach struktureller Korrektur erscheinen alle Unterseiten/Subpanels nicht mehr im linken vertikalen Bereich, sondern werden im horizontalen Hauptbereich angezeigt.
- Die vertikale Navigation verliert ihre Funktion oder zeigt keine Inhalte mehr an.
- Die Panels sind nicht mehr klar getrennt, sondern verschmelzen im Layout.

---

## Ursachen (Vermutung)
- Ein zu weit geöffnetes oder zu früh geschlossenes DIV im Bereich des vertikalen Splits führt dazu, dass die nachfolgenden Panels nicht mehr im vorgesehenen Container landen.
- Die DOM-Hierarchie der Split-Container (vertical/horizontal) ist nicht mehr eindeutig, sodass das CSS-Layout (z.B. Flexbox, Grid) nicht mehr greift.
- Die Panel-Zuordnung (z.B. per JS oder CSS-Selector) funktioniert nicht mehr, weil die Container-Struktur nicht mehr passt.

---

## Maßnahmen & Empfehlungen
- Nach jeder DIV-Reparatur gezielt prüfen, ob die Split-Container (vertical/horizontal) noch korrekt verschachtelt sind.
- gui_validator.py gezielt auf die Bereiche der Splits anwenden und auf Panel-Geschwisterschaft achten.
- Im CSS/JS prüfen, ob die Panel-Zuordnung noch mit der DOM-Struktur übereinstimmt.
- Nach jeder Änderung manuell testen, ob die vertikale Navigation und die zugehörigen Unterseiten korrekt angezeigt werden.

---

## Fazit

DIV-Reparaturen können zu unerwarteten Layout-Verschiebungen führen, wenn die Split-Container nicht exakt verschachtelt sind. Eine saubere Trennung und Validierung der vertikalen und horizontalen Bereiche ist essenziell für ein stabiles UI.

---
