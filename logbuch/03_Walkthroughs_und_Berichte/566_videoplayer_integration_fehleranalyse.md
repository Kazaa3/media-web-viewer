# Logbuch: Videoplayer Integration & Fehleranalyse

## Datum
16. März 2026

## Übersicht
Dieser Eintrag dokumentiert die Integration des Videoplayers, die erweiterten Playback-Modi und die Hardware-Erkennung sowie die Analyse von Abstürzen und Fehlern nach dem Einbau.

---

## Änderungen & Features

### Backend
- Hardware Detection: Echtzeit-Erkennung von SSD/HDD, PCIe-Generationen, Netzwerk-Mounts (SMB/NFS).
- Playback Modes: Unterstützung für chrome_native, ffmpeg, cvlc, mkvmerge, direct.
- Scan-Optimierung: Automatischer Lightweight-Mode für Netzwerkpfade, Skip-Parsen für bereits indexierte Medien.
- Analyse/Write Modes: Feature Flags für Deep Analysis und Metadaten-Schreiben.

### Frontend
- UI-Integration für Playback-Modi und Hardware-Info.
- Dropdown für Wiedergabe-Modus, Bandbreiten-Limit.
- Echtzeit-Anzeige Hardware-Informationen.

---

## Fehleranalyse (Absturz nach Videoplayer-Einbau)

### Hauptprobleme
- Unresolved Imports: pkg_resources, pymkv, FFprobeParser, toggle_pin.
- Falsche Attribute: eel.log_to_debug, eel.set_db_status, eel.append_test_output.
- VLC_INSTANCE: NoneType-Fehler bei media_player_new/media_new.
- DB-Methoden: get_path_by_name, update_media_tags (Argumente stimmen nicht).
- Netzwerk: host/laddr.ip/port nicht korrekt.

### Lösungsvorschläge
- Fehlende Module installieren und Imports prüfen.
- Eel-Funktionen korrekt exposen und im Frontend verfügbar machen.
- VLC_INSTANCE initialisieren und Fehler abfangen.
- DB-Methoden und Argumente anpassen.
- Netzwerk-Attribute korrekt referenzieren.

---

## Verifikation
- Hardware-Logik: test_hardware_detector.py (alle Tests bestanden)
- Playback-Switching: test_playback_modes.py (alle Tests bestanden)
- Manuelle Verifikation: Optionen-Tab, Hardware-Info, Modus-Wechsel, Feature Flags.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
