# Test-Suite & UX-Stabilisierung – Media Web Viewer

## Ziel
Eine robuste Test-Suite und gezielte UX-Stabilisierung für den Media Web Viewer. Alle Kernfunktionen (Playlist, Drag & Drop, Tab-Wechsel, Parser, GUI) werden automatisiert getestet und die Benutzererfahrung kontinuierlich verbessert.

## Test-Suite
- **Startup-Tests:** Prüfen, ob alle Tabs und Kernfunktionen nach dem Start verfügbar sind.
- **Playlist-Tests:** Drag & Drop, Up/Down, Item-Select, Reihenfolge, Edge Cases.
- **Tab-Wechsel:** Mehrfaches Wechseln zwischen Tabs, UI-Integrität, keine State-Verluste.
- **Parser-Tests:** Alle Medienformate, Fehlerfälle, Fallbacks.
- **GUI-Tests:** Selenium/Playwright, Screenshots, Responsive-Checks.
- **Environment-Tests:** Python-Umgebung, venv, Paket-Kompatibilität.

## UX-Stabilisierung
- **Fehlerbilder dokumentieren:** Screenshots, Logbuch-Einträge, Regression-Tracking.
- **UI-Feedback:** Klare Statusanzeigen, Fehlermeldungen, Loading-States.
- **Interaktions-Tests:** Maus, Touch, Tastatur, Action Chains.
- **Performance:** Ladezeiten, Responsiveness, Async-Handling.
- **Accessibility:** Tab-Order, ARIA-Labels, Kontrast.

## Workflow
- Automatisierte Tests laufen bei jedem Build/Release.
- Fehlerbilder und UX-Probleme werden im Logbuch dokumentiert.
- Verbesserungen werden iterativ umgesetzt und getestet.

---
Letzte Aktualisierung: 11. März 2026
