# Ausspielen von Backend-Konfigurationen an die GUI

## Ziel
- Das Backend stellt der Web-GUI (Frontend) die jeweils passende Konfiguration und Systeminformationen bereit.
- So kann die GUI dynamisch auf Umgebungsvariablen, Feature-Flags oder Systemstatus reagieren.

## Mechanismen
- **API-Endpunkte:**
  - Das Backend (Bottle/Eel) bietet Endpunkte wie `/api/config` oder `/api/env`, die aktuelle Einstellungen als JSON liefern.
  - Beispiel:
    ```python
    @eel.expose
    def get_config():
        with open("web/config.json") as f:
            return json.load(f)
    ```
- **Eel-Bridge:**
  - Über Eel können Python-Funktionen direkt aus dem Frontend (JavaScript) aufgerufen werden, um Konfigs oder Statusdaten zu holen.
- **Automatisches Nachladen:**
  - Die GUI kann beim Start oder zyklisch die aktuelle Konfiguration vom Backend abrufen und anwenden.

## Typische Daten
- Feature-Flags (z.B. experimentelle Funktionen)
- Systemstatus (z.B. verfügbare Tools, Versionen)
- Benutzer- und Umgebungsdaten
- Aktive Medienverzeichnisse, Kategorien

## Vorteile
- Zentrale Steuerung der Features und Einstellungen
- Flexibles Umschalten von Features ohne Rebuild der GUI
- Bessere Synchronisation zwischen Backend und Frontend

## Hinweise
- Die API/Bridge sollte nur die nötigen Daten ausspielen (Sicherheitsaspekt)
- Änderungen an der Konfiguration im Backend wirken sich sofort auf die GUI aus
- Für komplexe Szenarien können mehrere Endpunkte (z.B. `/api/config`, `/api/status`, `/api/user`) genutzt werden

---

**Siehe auch:**
- Logbuch: JSON-Konfigs, CI/CD-Ausspielung
- src/core/main.py, web/
- Eel-Doku: https://github.com/ChrisKnott/Eel
