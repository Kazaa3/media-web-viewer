# Logbuch-Eintrag 053: ISO/DVD Support für VLC

## Status
- **Datum:** 2026-03-12
- **Thema:** Native DVD-Wiedergabe von ISO-Dateien
- **Status:** Abgeschlossen

## Problemstellung
ISO-Dateien können nicht direkt im Browser wiedergegeben werden. Nutzer möchten DVD-Abbilder jedoch nahtlos abspielen, idealerweise mit Menü-Support und Kapitelwahl, ohne die Datei manuell in VLC öffnen zu müssen.

## Strategie
Anstatt ISO-Dateien zeitaufwendig zu remuxen oder über eine Pipe zu streamen (was den Menü-Support einschränken würde), wurde die Funktionalität in den "Direct Play"-Workflow integriert.

1. **Dateityp-Erkennung:** Erkennung von `.iso` Dateien im Backend.
2. **Native Ansteuerung:** Start von VLC über das `dvd://` Protokoll (`vlc dvd:///pfad/zu/datei.iso`).
3. **UI-Integration:** Automatische Benachrichtigung im Frontend, dass der native DVD-Modus aktiv ist.

## Implementierung

### Backend (`main.py`)
In der Funktion `stream_to_vlc` wurde eine Weiche für ISO-Dateien implementiert:
```python
if file_path.lower().endswith('.iso'):
    vlc_path = shutil.which('vlc') or 'vlc'
    cmd = [vlc_path, f"dvd://{file_path}"]
    subprocess.Popen(cmd)
    return {"status": "ok", "mode": "vlc_dvd"}
```

### Frontend (`app.html`)
Die `playVideo` Logik verarbeitet nun den `vlc_dvd` Status und informiert den Nutzer mittels Toast-Nachricht und Status-Update im VLC-Ribbon.

## Vorteile
- **Voller Menü-Support:** Nutzer können DVD-Menüs bedienen.
- **Performance:** Kein Overhead durch Remuxing oder Piping.
- **UX:** Konsistenter Workflow über den "Direct Play" Button.

## Nächste Schritte
- Langfristig: Unterstützung für Blu-ray ISOs (`bluray://`).
