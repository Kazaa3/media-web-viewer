# Aktualisierung von Werten auf der JavaScript-GUI

## Mechanismen
- Die GUI (Frontend, meist JavaScript/HTML) erhält Werte und Konfigurationen vom Backend über:
  - **API-Calls** (z.B. via fetch/AJAX auf `/api/config`)
  - **Eel-Bridge** (direkter Funktionsaufruf von Python nach JS)
  - **WebSocket-Events** (für Live-Updates, falls implementiert)

## Typische Abläufe
1. **Initiales Laden:**
   - Beim Start der GUI wird die Konfiguration (z.B. `config.json` oder API-Response) geladen und in JS-Variablen gespeichert.
   - Beispiel:
     ```js
     fetch('/api/config')
       .then(response => response.json())
       .then(config => {
         window.appConfig = config;
         updateUIWithConfig(config);
       });
     ```
2. **Aktualisierung durch Backend:**
   - Das Backend kann per Eel oder API neue Werte liefern, die dann in der GUI übernommen werden.
   - Beispiel (Eel):
     ```js
     eel.get_config()(config => {
       window.appConfig = config;
       updateUIWithConfig(config);
     });
     ```
3. **Live-Update (optional):**
   - Bei Änderungen (z.B. durch User-Action oder Backend-Event) kann die GUI gezielt einzelne Werte aktualisieren und die betroffenen UI-Elemente neu rendern.
   - Beispiel:
     ```js
     function updateFeatureFlag(flag, value) {
       window.appConfig.feature_flags[flag] = value;
       updateUIWithConfig(window.appConfig);
     }
     ```

## Hinweise
- Änderungen an JS-Objekten wirken sich erst nach explizitem Render/Update auf die UI aus
- Für komplexe GUIs empfiehlt sich ein Framework (z.B. Vue, React), das Datenbindung und automatische Updates unterstützt
- Bei Eel: Python kann direkt JS-Funktionen triggern (und umgekehrt)

---

**Siehe auch:**
- Logbuch: Backend-GUI-Ausspielung, JSON-Konfigs
- web/, src/core/main.py
- Eel-Doku: https://github.com/ChrisKnott/Eel
