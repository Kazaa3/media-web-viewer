# Logbuch: Erweiterte Player-GUI & Button-Anforderungen

**Datum:** 11. März 2026

---

## Anforderungen für die Player-GUI
- **Erweiterte Steuerung:** Zusätzliche Buttons für fortgeschrittene Player-Funktionen (z.B. Stop, Shuffle, Repeat, Seek, Speed, Playlist, EQ).
- **Konsistentes Design:** Alle Icons als SVG oder aus einer etablierten Icon-Bibliothek (Material, FontAwesome).
- **Barrierefreiheit:** i18n-Labels und ARIA-Attribute für alle Buttons.
- **Platzierung:** Buttons unten links im Player-Bereich, gruppiert und mit Abstand.
- **Erweiterbarkeit:** GUI soll einfach um weitere Funktionen ergänzt werden können.

---

## Vorschläge für neue Buttons
- **Stop:**
  - Symbol: Quadrat (■) oder SVG-Icon (z.B. Material "stop")
  - Funktion: Stoppt die Wiedergabe und setzt den Player zurück.
- **Shuffle:**
  - Symbol: Gekreuzte Pfeile (SVG, Material "shuffle")
  - Funktion: Playlist zufällig abspielen.
- **Repeat:**
  - Symbol: Kreis mit Pfeil (SVG, Material "repeat")
  - Funktion: Wiederholt Playlist/Song.
- **Seek:**
  - Symbol: Pfeile links/rechts (SVG, Material "fast_forward", "fast_rewind")
  - Funktion: Vor-/Zurückspulen.
- **Speed:**
  - Symbol: Tachometer (SVG, Material "speed")
  - Funktion: Wiedergabegeschwindigkeit ändern.
- **EQ:**
  - Symbol: Equalizer-Balken (SVG, Material "equalizer")
  - Funktion: Equalizer öffnen.

---

## Beispiel für Stop-Button (SVG)
```html
<button id="btn-stop" onclick="stopPlayback()" class="player-btn" data-i18n="[title]player_btn_stop" aria-label="player_stop">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="6" y="6" width="12" height="12" fill="#333"/>
  </svg>
</button>
```

---

## TODO/FIXME
- Bestehende Shuffle-Button durch besseres Symbol ersetzen.
- Stop-Button und weitere Funktionen ergänzen.
- GUI unten links erweitern und Buttons gruppieren.
- Funktionen im JS/Backend implementieren.
- Logbuch-Eintrag nach Umsetzung aktualisieren.

---

## Anmerkung
- Aktuelle Funktion des Shuffle-Buttons prüfen und ggf. anpassen.
- Stop-Button einführen und mit Funktion belegen.
- GUI modular gestalten für zukünftige Erweiterungen.
