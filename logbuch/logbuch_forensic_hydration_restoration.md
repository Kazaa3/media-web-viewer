# Logbuch: Forensic Hydration Restoration (v1.46.003)

## Ziel
Die mehrstufige Hydration-Handshake-Logik wird wiederhergestellt, sodass die UI niemals leer bleibt – auch nicht vor vollständigem DB-Load. Die Übergänge erfolgen von 0 Items zu 12 Mock-Items und schließlich zu echten Daten (oder einer Kombination).

---

## Maßnahmen

### 1. Web Infrastructure
- **forensic_hydration_bridge.js:**
  - Stage 1: Emergency Injection befüllt jetzt sowohl `window.allLibraryItems` als auch `window.currentPlaylist` mit 12 diversen Mock-Assets.
  - Mode Steering: Logik für `window.__mwv_hydration_mode` integriert ("mock", "real", "both").
  - Both Mode: Merge-Strategie implementiert, bei der Mock-Items beim Eintreffen echter Daten oben erhalten bleiben.
  - Handshake Hardening: Stage 0 triggert sofort bei fehlenden Daten, Übergänge erfolgen konfigurationsbasiert.
- **common_helpers.js:**
  - `setHydrationMode` aktualisiert, um den Audit-Loop der Bridge sofort neu zu triggern und die UI instant zu aktualisieren.
- **bibliothek.js:**
  - `loadLibrary` respektiert jetzt den FHB-Status und löscht keine Mock-Items, wenn der Modus auf "mock" oder "both" steht.
- **test_injection.js:**
  - Datei entfernt, da die Logik nun vollständig in der ForensicHydrationBridge konsolidiert ist.

---

## Offene Fragen
- Sollen Mock-Items im "both"-Modus klar gelabelt werden (z.B. "[MOCK] Asset Name")?
- Sollen Mock-Items die gesamte Session über bestehen bleiben oder ist Stage 1 nur ein temporärer Proof-of-Life?

---

## Verifikation
- **Cold Boot Test:** Nach Start erscheinen innerhalb von 2 Sekunden exakt 12 Items in Bibliothek und Queue.
- **Mode Switching:** Umschalten zwischen M, R und B im Footer aktualisiert Item-Count und Listeninhalt korrekt.
- **Empty DB Test:** DB temporär umbenennen → UI zeigt weiterhin 12 Mock-Items.

---

*Status: Multi-Stage Hydration-Handshake wiederhergestellt, UI bleibt immer befüllt und reaktiv.*
