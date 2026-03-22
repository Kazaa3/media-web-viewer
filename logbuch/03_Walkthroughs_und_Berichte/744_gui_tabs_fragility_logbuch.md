---

# Logbuch-Eintrag: Instabile Tab-Panels – Parser, Debug & Tests (März 2026)

## Problemstellung

Die Tabs „Parser“, „Debug“ und „Tests“ im GUI brechen regelmäßig, sobald an anderer Stelle im HTML strukturelle Änderungen vorgenommen werden. Die Funktionalität dieser Tabs ist extrem fragil und reagiert empfindlich auf jede Änderung an Containern, Panels oder der DOM-Hierarchie.

---

## Symptome
- Nach Änderungen an anderen Panels (z.B. Options, Tools, Environment) funktionieren die Tabs nicht mehr oder verschwinden komplett.
- Die Tab-Contents sind im DOM nicht mehr sichtbar oder werden falsch verschachtelt.
- Tab-Switching per JS funktioniert nicht mehr zuverlässig.

---

## Ursachen (Vermutung)
- Zu frühes oder fehlerhaftes Schließen von Containern (z.B. </div>), wodurch die Tab-Contents nicht mehr auf derselben Hierarchieebene liegen.
- Verschachtelung der Tab-Contents in Panels, die nicht für sie vorgesehen sind.
- Fehlerhafte DOM-Struktur führt dazu, dass die Tab-Initialisierung/Tab-Switch-Logik ins Leere läuft.
- i18n- oder dynamische JS-Initialisierung wird nach DOM-Änderungen nicht erneut getriggert.

---

## Maßnahmen & Empfehlungen
- Nach jeder strukturellen Änderung gui_validator.py ausführen, um Container-Fehler sofort zu erkennen.
- Sicherstellen, dass alle Tab-Contents (Parser, Debug, Tests, ...) direkte Geschwister (siblings) im DOM sind.
- Tab-Initialisierung und -Switch-Logik im JS nach DOM-Änderungen erneut triggern.
- Automatisierte Tests für Sichtbarkeit und Aktivierung aller Tabs etablieren.
- Nach jeder Änderung gezielt die Funktionalität aller Tabs manuell prüfen.

---

## Fazit

Die Tab-Panels „Parser“, „Debug“ und „Tests“ sind besonders anfällig für strukturelle Fehler im HTML. Eine saubere, flache DOM-Struktur und konsequente Validierung sind essenziell, um die Stabilität dieser GUI-Elemente zu gewährleisten.

---
