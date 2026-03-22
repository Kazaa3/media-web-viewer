---

# Logbuch-Eintrag: Tab-Instabilität nach Erweiterung der Optionen (März 2026)

## Kontext

Seit der Erweiterung und Umstrukturierung des Options-Panels (z.B. Hinzufügen neuer Sub-Tabs wie Tools, Environment, General) treten massive Instabilitäten bei den Tabs „Parser“, „Debug“ und „Tests“ auf.

---

## Beobachtungen
- Nach jeder Änderung oder Erweiterung im Options-Bereich funktionieren die genannten Tabs nicht mehr korrekt.
- Die Tab-Contents verschwinden, werden falsch verschachtelt oder sind nicht mehr anwählbar.
- Die Sub-Navigation im Options-Panel (General, Tools, Environment) beeinflusst die Sichtbarkeit und Funktion der anderen Tabs.

---

## Ursachen (Vermutung)
- Die DOM-Struktur der Options-Sub-Tabs ist zu tief oder falsch verschachtelt, wodurch nachfolgende Tab-Contents (Parser, Debug, Tests) nicht mehr als eigenständige Siblings erkannt werden.
- Ein zu frühes oder mehrfaches Schließen von Containern (<div>) im Options-Bereich führt dazu, dass die nachfolgenden Tabs in den Options-Panel-Bereich „hineinrutschen“.
- Die Tab-Initialisierung im JS wird durch DOM-Fehler oder falsche Hierarchie gestört.

---

## Maßnahmen & Empfehlungen
- Nach jeder Erweiterung des Options-Panels gui_validator.py ausführen, um Container-Fehler sofort zu erkennen.
- Sicherstellen, dass alle Haupt-Tabs (Options, Parser, Debug, Tests, ...) auf derselben DOM-Ebene liegen und nicht in Sub-Tabs verschachtelt werden.
- Die Sub-Navigation im Options-Panel strikt innerhalb des Options-Containers halten und sauber abschließen.
- Nach jeder Änderung automatisierte und manuelle Tab-Tests durchführen.

---

## Fazit

Die Erweiterung des Options-Panels hat die Tab-Panel-Struktur destabilisiert. Eine saubere, flache DOM-Struktur und konsequente Validierung sind essenziell, um die Funktionalität aller Tabs zu gewährleisten.

---
