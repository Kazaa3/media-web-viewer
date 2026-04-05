# Logbuch: Tools-Tab & Menüstruktur-Redesign

## Ziel
Die Menüstruktur der App wird überarbeitet, um den Tools-Tab als eigenständigen Haupt-Tab zu etablieren, Advanced Tools direkt darin zu integrieren und den Parser-Bereich als Untertab von Tools anzuordnen. Überflüssige oder leere Untermenüs werden entfernt, die Navigation wird klarer und flacher.

---

## Ausgangslage
- Tools/Advanced Tools war bisher als verschachteltes Untermenü realisiert.
- Parser war ein separater Bereich oder zu tief verschachtelt.
- Es gab leere oder doppelte Untermenüs/Splits.

---

## Umsetzungsschritte
1. **Tools-Tab als Haupt-Tab:**
   - Tools erscheint nun als eigenständiger Tab in der Hauptnavigation.
2. **Advanced Tools Integration:**
   - Advanced Tools ist kein Untermenü mehr, sondern direkt im Tools-Tab gelistet.
3. **Parser als Untertab:**
   - Parser wird als Untertab von Tools geführt.
4. **Menüstruktur bereinigen:**
   - Überflüssige Splits und leere Untermenüs werden entfernt.
   - Die Menü- und Tab-Logik in HTML/JS wird entsprechend angepasst.

---

## Vorteile
- Klare, flache Navigation ohne unnötige Verschachtelung.
- Tools und Advanced Tools sind direkt zugänglich.
- Parser ist logisch unter Tools einsortiert.
- Keine leeren oder doppelten Menüs mehr.

---

## Nächste Schritte
- Anpassung der Tab- und Menüstruktur in `app.html` und ggf. zugehörigen JS-Dateien.
- Testen der neuen Navigation auf Funktionalität und Übersichtlichkeit.
- Feedback einholen und ggf. weitere Optimierungen vornehmen.

---

## Status
- Planung und Zieldefinition abgeschlossen.
- Umsetzung der Menüstruktur-Änderungen steht an.

---

*Dieses Logbuch dokumentiert die geplante Umstrukturierung der Tools- und Menü-Navigation für eine klarere, benutzerfreundlichere App-Oberfläche.*
