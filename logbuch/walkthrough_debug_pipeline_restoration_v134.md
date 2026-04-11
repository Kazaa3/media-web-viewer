# Walkthrough – v1.34 Debug & Pipeline Restoration

Die "Real Media"-Discovery-Pipeline ist wiederhergestellt und ein robustes On-Screen-Diagnosesystem wurde implementiert.

---

## Key Deliverables

### 1. DOM Debug Console (Real-time Trace)
- **Glasmorphes Overlay:** Sofortige Sichtbarkeit der internen App-Mechanik.
- **Toggle:** Gelber LOGS-Button im Footer-Cluster.
- **Features:** Zeigt Frontend-Navigation (mwv_trace), Backend-Parser-Status und Fehler.
- **Backend Bridge:** Python-Logs werden via `eel.append_debug_log` direkt angezeigt.
- **Tipp:** Clear-Button im Overlay leert das Log für lange Debug-Sessions.

### 2. Real Media Discovery Engine
- **Auto-Scan:** Beim Start prüft die App auf echte Medien. Falls keine gefunden, wird ./media automatisch gescannt.
- **Default Indexing:** "audio" und "video" sind immer als indizierte Kategorien gesetzt.

### 3. Extended Options Panel
- **System & Diagnose:**
  - Automatischer Scan: Schaltet Scan bei Start ein/aus.
  - Debug-Konsole (DOM): Standard-Sichtbarkeit des Trace-Overlays speichern.
  - Mocks ausblenden: Mock-Daten in der Galerie persistent ein-/ausblenden.

---

## Verification Results

### Automated Pipeline Check
- Interne Diagnosesuite bestätigt, dass `append_debug_log` funktioniert und die Library zwischen Mock und Real unterscheidet.

### Manual Verification Steps
- **Toggle Logs:** App öffnen, LOGS klicken, Initialisierungstrace sehen.
- **Trigger Scan:** SCAN im Footer klicken, Fortschritt in Debug-Konsole beobachten.
- **Verify Gallery:** Audio Player > Mediengalerie: Echte .mp3/.m4a aus ./media sind sichtbar und abspielbar.
- **Save Options:** Tools > System & Diagnose: Einstellung ändern, nach Refresh bleibt sie erhalten.
