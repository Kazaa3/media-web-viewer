# Logbuch: Naming-Konventionen für MPV und MPV-WASM (Phase 10+)

## Status: ToDo / Für spätere Refaktorisierung

---

## Ziel
Für zukünftige Refactorings und bessere Wartbarkeit soll eine klare Unterscheidung zwischen MPV (Native) und MPV-WASM (Embedded) im Dateinamen- und Komponenten-Schema eingeführt werden.

---

## Empfehlungen
- **Dateinamen:**
  - mpv_native.js für die Desktop/Native-Integration
  - mpv_wasm.js für die WASM/Browser-Integration
- **Komponenten/Bridges:**
  - Eindeutige Benennung in app.html, main.js und allen Imports/Exports
  - UI-Elemente und Buttons entsprechend kennzeichnen (z.B. "Play with MPV (Native)" vs. "Play with MPV (WASM)")
- **Dokumentation:**
  - Hinweise in README und Entwicklerdokumentation ergänzen

---

*Dieses Logbuch dient als Reminder und Planungsgrundlage für die spätere, saubere Trennung und Benennung der MPV-Komponenten.*
