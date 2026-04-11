# Implementation Plan – Quick Sign-off & Real Media Finalization

## Ziel
Mock-Stage wird in einen dedizierten Startup-Test ausgelagert. Die App indexiert und spielt standardmäßig nur echte Medien aus ./media/. Mock-Daten dienen nur noch expliziten GUI-Tests.

---

## Proposed Changes

### [FRONTEND] Discovery Refactoring

**[MODIFY] audioplayer.js**
- Entferne `setTimeout(bootstrapMockQueue, 2000)` (keine automatische Mock-Injektion mehr).
- Exportiere `bootstrapMockQueue` ans `window`-Objekt für gezielte Test-Aufrufe.

**[MODIFY] bibliothek.js**
- Verfeinere die Auto-Scan-Logik:
  - Priorisiere ./media/-Indexierung bei Kaltstart.
  - Keine Störung bestehender Datenbanken.

---

### [TESTS] Development & Sign-off Tools

**[NEW] scripts/quick_signoff_test.py**
- Playwright-Skript, das:
  - Eine Managed Session startet.
  - Echte Medien aus dem Dateisystem entdeckt und prüft.
  - "Mock Bootstrap" manuell triggert, um GUI-Ästhetik zu testen.
  - Playback für echte und Mock-Items bestätigt.

---

## Verification Plan

### Automated Tests
- **Sign-off Run:** `python3.14 scripts/quick_signoff_test.py`
- **Tab Integrity:** `python3.14 scripts/app_audit_playwright.py` prüft UI-Status.

### Manual Verification
- **Cold Start Check:** `media_library.db` löschen, App starten, ./media/ wird korrekt gescannt.

---

**User Review Required:**
- Mock-Daten werden nur noch für gezielte Tests genutzt.
- Standardmäßig werden echte Medien indexiert und abgespielt.
- Quick Sign-off Script prüft beide Pfade (Real & Mock).
