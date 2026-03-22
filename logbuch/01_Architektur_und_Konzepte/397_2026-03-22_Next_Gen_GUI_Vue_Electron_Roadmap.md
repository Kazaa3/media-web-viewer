## Zielsetzung
Ablösung des aktuellen **Vanilla JS, Bottle und Eel**-Frontends durch eine moderne, hochperformante Desktop-Applikation auf Basis von **Vue.js** (v3) und **Electron**. Eine Zwischenlösung mit **NiceGUI** war zwar ursprünglich angedacht, wird aber übersprungen, um direkt auf ein professionelles JS-Framework zu portieren.

## Gründe für den Wechsel
1.  **Performance:** Electron bietet eine bessere Integration von Hardware-Beschleunigung für Video-Wiedergabe (z. B. via `mpv.js` oder native Integrationen).
2.  **UI-Komponenten:** Vue.js ermöglicht ein reaktiveres State-Management und den Einsatz von ausgereiften Komponenten-Bibliotheken (z. B. Vuetify, PrimeVue).
3.  **Standalone-Packaging:** Einfachere Paketierung für Windows/macOS/Linux ohne Abhängigkeiten vom installierten Browser des Nutzers.
4.  **Backend-Entkopplung:** Klare Trennung zwischen der Python-Mediendatenbank (als API/Service) und dem JavaScript-Frontend.

## Geplante Phasen
1.  **Evaluierung:** Prototyp mit `mpv.js` in Electron zur Validierung der Video-Latenz.
2.  **API-Design:** Definition einer stabilen REST- oder WebSocket-Schnittstelle im Python-Backend.
3.  **Migration:** Schrittweise Portierung der Tabs (Bibliothek, Player, Logbuch) in die neue Vue-Oberfläche.

---

*Dieser Eintrag markiert den strategischen Entschluss zur technischen Modernisierung der Benutzeroberfläche.*
