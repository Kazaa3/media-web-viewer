---

# Logbuch-Eintrag: Trennung von Haupt-Tabs und Unterreitern mit Kommentaren (März 2026)

## Ziel

Die klare Trennung zwischen Haupt-Tabs (z.B. Optionen, Parser, Debug, Tests) und Unterreitern/Sub-Tabs (z.B. General, Tools, Environment innerhalb von Optionen) ist essenziell für Übersicht, Wartbarkeit und Fehlervermeidung in app.html.

---

## Maßnahmen
- **HTML-Kommentare als Anker:**
  - Haupt-Tabs und ihre Panel-Container mit eindeutigen Kommentaren kennzeichnen, z.B.:
    - <!-- TAB: Optionen START --> ... <!-- TAB: Optionen END -->
    - <!-- TAB: Parser START --> ... <!-- TAB: Parser END -->
  - Unterreiter/Sub-Tabs innerhalb eines Haupt-Tabs ebenfalls mit Kommentaren abgrenzen, z.B.:
    - <!-- SUBTAB: Optionen-General START --> ... <!-- SUBTAB: Optionen-General END -->
    - <!-- SUBTAB: Optionen-Tools START --> ... <!-- SUBTAB: Optionen-Tools END -->
- **Struktur-Check:**
  - Sicherstellen, dass Unterreiter immer innerhalb des zugehörigen Haupt-Tabs liegen und nicht versehentlich auf derselben Ebene wie die Haupt-Tabs.
- **Wireframe-Visualisierung:**
  - Die Kommentierung im Code kann als Grundlage für eine Wireframe- oder Baumstruktur dienen, um die Panel-Hierarchie zu visualisieren.

---

## Beispiel (HTML-Kommentare)

<!-- TAB: Optionen START -->
  ...
  <!-- SUBTAB: Optionen-General START -->
    ...
  <!-- SUBTAB: Optionen-General END -->
  <!-- SUBTAB: Optionen-Tools START -->
    ...
  <!-- SUBTAB: Optionen-Tools END -->
<!-- TAB: Optionen END -->

<!-- TAB: Parser START -->
  ...
<!-- TAB: Parser END -->

---

## Fazit

Die konsequente Trennung und Kommentierung von Haupt-Tabs und Unterreitern erleichtert die Navigation im Code, verhindert Verschachtelungsfehler und unterstützt die Wartbarkeit bei großen HTML-Dateien.

---
