# Logbuch: GUI-Überarbeitung & Bandbreiten-/Desktop-Modus

## Datum
16. März 2026

---

## GUI-Überarbeitung
- Die Oberfläche wurde überarbeitet, alle Playback-Modi und Hardware-Erkennung sind integriert.
- Drag & Drop Playlist, Toasts, und Kontextmenü sind implementiert.
- Modus-Auswahl und Player-Switch funktionieren wie vorgesehen.

---

## Fehlende Info: Low Bandwidth & Desktop-Modi
- Es gibt aktuell keine Anzeige oder Info im GUI über den Low Bandwidth Mode (20MB/s).
- Desktop-Modus zeigt keinen Datendurchsatz zu Datenträger 1, 2, 3 oder SMB-Freigabe.
- Hardware-Erkennung funktioniert, aber GUI zeigt keine Bandbreiten- oder Durchsatzwerte.

---

## Empfehlung
- Ergänze im GUI eine Info-Box oder Statuszeile:
  - Zeigt aktuellen Modus (Low Bandwidth, Desktop, etc.)
  - Zeigt Datendurchsatz zu den erkannten Datenträgern (HDD/SSD/NVMe/SMB)
  - Zeigt Warnung bei Netzwerkpfaden (z.B. SMB/NFS) mit ressourcenschonendem Scan
- Backend: Liefere Datendurchsatz und Modus-Status als API für das Frontend.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe logbuch/2026-03-16_walkthrough_advanced_playback_ui_debugging.md für Details zur bisherigen GUI-Integration.*
