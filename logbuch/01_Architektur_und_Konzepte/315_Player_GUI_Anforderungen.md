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

Hier ist der Block, den du unten in die Player_GUI_Anforderungen.md einfügen kannst:

GUI-Button-Varianten mit Unicode
Stop: <button id="btn-stop" onclick="stopPlayback()" class="player-btn" aria-label="player_stop">■</button>

Shuffle: <button id="btn-shuffle" onclick="toggleShuffle()" class="player-btn" aria-label="player_shuffle">🔀</button>

Repeat: <button id="btn-repeat" onclick="toggleRepeat()" class="player-btn" aria-label="player_repeat">🔁</button>

Seek (Vor/Zurück): <button id="btn-seek-back" onclick="seekBack()" class="player-btn" aria-label="player_seek_back">⏪</button>
                   <button id="btn-seek-forward" onclick="seekForward()" class="player-btn" aria-label="player_seek_forward">⏩</button>
Speed: <button id="btn-speed" onclick="toggleSpeed()" class="player-btn" aria-label="player_speed">⏱️</button>

EQ: <button id="btn-eq" onclick="openEQ()" class="player-btn" aria-label="player_eq">🎚️</button>

Diese Unicode-Varianten können als schnelle GUI-Erweiterung genutzt werden und später durch SVG-Icons ersetzt werden.


Hier sind die Python Unicode-Zeichen für die GUI-Buttons, die du unten in die Player_GUI_Anforderungen.md einfügen kannst:

Python Unicode-Zeichen für GUI-Buttons

stop_btn = '\u25A0'        # ■shuffle_btn = '\U0001F500' # 🔀repeat_btn = '\U0001F501'  # 🔁seek_back_btn = '\U000023EA'   # ⏪seek_forward_btn = '\U000023E9' # ⏩speed_btn = '\U000023F1'   # ⏱️eq_btn = '\U0001F39A'      # 🎚️# Beispiel für Verwendung:print(stop_btn, shuffle_btn, repeat_btn, seek_back_btn, seek_forward_btn, speed_btn, eq_btn)
Diese Strings kannst du direkt in Python verwenden, z.B. für Button-Labels im Backend oder für Tests.