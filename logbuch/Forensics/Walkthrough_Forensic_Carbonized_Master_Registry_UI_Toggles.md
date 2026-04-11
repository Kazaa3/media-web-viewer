# Walkthrough - Forensic Carbonized Master-Registry & UI Toggles

## Zusammenfassung
Die Master-Registry in der `config_master.py` ist jetzt vollständig "Forensic Carbonized". Jedes kritische Interface-Element besitzt einen eigenen autoritativen Master-Schalter, der tief mit dem Geometrie- und Sichtbarkeitssystem der Anwendung verzahnt ist.

---

## Übersicht der neuen Master-Toggles
Sie können folgende Module jetzt global (anwendungsweit) in der `config_master.py` ein- oder ausschalten:

- **Audio Engine (`audio_engine_enabled`):** Deaktiviert den gesamten Musik-Player.
- **Video Engine (`video_engine_enabled`):** Deaktiviert das Cinema/Video-Modul.
- **Media Queue (`queue_panel_enabled`):** Schaltet die Abspielliste (Queue) global ab.
- **Lyrics & Meta (`lyrics_panel_enabled`):** Entfernt das Panel für Songtexte und Metadaten.
- **Global Search (`global_search_allowed`):** Schaltet die Suche im Header ab.
- **Audio Footer (`footer_visible`):** Steuert die untere Steuerleiste.
- **Mini-Player (`mini_player_allowed`):** Erlaubt oder verbietet den PiP-Modus.

---

## Schutz vor Layout-Stalling
Alle Flags sind tief in das Geometrie-System integriert. Wird ein Modul deaktiviert, gibt die Anwendung den Platz sofort frei – "schwarze Flächen" werden so zuverlässig vermieden. Beispiel: Sind `audio_engine` und `footer` deaktiviert, wächst der Content-Bereich automatisch auf volle Bildschirmhöhe (echter Zen-Mode).

---

## Single Source of Truth (SSOT)
Die Registry ist jetzt das SSOT für die gesamte Forensic-Session. Änderungen an den Master-Toggles wirken sich sofort und global auf das UI aus.

---

## Hinweis
Gibt es noch ein spezifisches Element (z.B. Logbuch-Overlay, Diagnostik-Panel), das ebenfalls als Master-Schalter in die Config aufgenommen werden soll? Ansonsten ist das System jetzt auf einem sehr hohen Stabilitäts- und Kontrollniveau.
