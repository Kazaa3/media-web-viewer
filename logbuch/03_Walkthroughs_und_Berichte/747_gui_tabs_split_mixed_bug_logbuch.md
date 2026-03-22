---

# Logbuch-Eintrag: Mischfehler – Tabs & Split-Layout gleichzeitig instabil (März 2026)

## Kontext

Aktuell besteht eine Mischform der beiden zuvor dokumentierten Fehlerbilder:
- Tabs wie „Parser“, „Debug“ und „Tests“ sind instabil oder verschwinden.
- Gleichzeitig rutschen Unterseiten/Subpanels aus dem vertikalen Split in den horizontalen Bereich oder umgekehrt.

---

## Beobachtungen
- Nach strukturellen Änderungen (DIV-Reparatur, Panel-Erweiterung) treten beide Effekte gleichzeitig auf.
- Tabs und Split-Layout beeinflussen sich gegenseitig negativ: Korrektur an einer Stelle verschärft das Problem an der anderen.
- Die Navigation und Panel-Zuordnung ist nicht mehr eindeutig, UI-Elemente erscheinen an falscher Stelle oder verschwinden.

---

## Ursachen (Vermutung)
- Mehrfache oder widersprüchliche Container-Verschachtelungen im Bereich der Hauptpanels und Splits.
- Unklare DOM-Hierarchie: Panels/Tabs und Split-Container sind nicht sauber getrennt.
- CSS- und JS-Logik (z.B. Flexbox, Tab-Switching) greifen ins Leere oder wirken auf falsche Container.

---

## Maßnahmen & Empfehlungen
- DOM-Struktur der Hauptpanels, Tabs und Split-Container gemeinsam als Ganzes prüfen und mit gui_validator.py validieren.
- Panels und Tabs als direkte Geschwister (siblings) auf oberster Ebene anlegen, Split-Container klar abgrenzen.
- Nach jeder Änderung automatisierte und manuelle Tests für beide Bereiche (Tabs & Split) durchführen.
- CSS- und JS-Selektoren auf die neue Struktur anpassen.

---

## Fazit

Die gleichzeitige Instabilität von Tabs und Split-Layout ist ein Hinweis auf grundlegende Strukturprobleme im HTML. Nur eine ganzheitliche, saubere DOM-Struktur und konsequente Validierung können beide Fehlerbilder nachhaltig beheben.

---
