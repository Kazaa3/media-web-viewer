# Implementation Plan: UI Consistency & Theme Restoration (v1.46.024)

## Ziel
Behebung von Layout- und Theme-Regressionsfehlern in der Mediengalerie und Level-2-Navigation. Wiederherstellung des konsistenten Forensik-Dark-Themes und der Menüausrichtung.

## Schritte

### 1. Stylesheets (web/css/main.css)
- **Track-Item-Konsolidierung:**
  - Entferne alle hardcodierten `background: #ffffff`-Definitionen aus `.legacy-track-item`.
  - Ersetze durch `background: var(--bg-secondary)` (bzw. `#000000` für High-Contrast-Dark-Theme).
- **Theme-Inversion-Registry:**
  - Füge `.legacy-track-item` zum `html[data-theme="dark"]`-Block (ca. Zeile 55) hinzu, um "Black Background / White Text"-Parität mit Buttons zu gewährleisten.
- **Level-2-Menü-Feinabstimmung:**
  - Passe Padding und Höhe von `.sub-nav-bar` und `#header-nav-buttons` an, um Layout-Shifts und Überlappungen zu verhindern.
- **Doppelte Selektoren entfernen:**
  - Bereinige Zeilen 1712, 2071, 2085, 2099 und 2522, um CSS-Konflikte zu vermeiden.

### 2. Technical Orchestration (web/app.html)
- **Header-Sync:**
  - Prüfe, dass die Variablen `--active-header-height` und `--active-sub-nav-height` korrekt gesetzt und weitergegeben werden, damit das Level-2-Menü nicht überlappt.

## Verifikationsplan

### Automatisierte Tests
- Anwendung starten: `python3 src/core/main.py --probe`
- Prüfen, dass `.legacy-track-item`-Elemente im Dark Theme den Hintergrund `#000000` (oder die gewünschte Variable) haben.

### Manuelle Überprüfung
- In die "Database" oder "Library"-Ansicht wechseln.
- Sicherstellen, dass das Level-2-Menü korrekt unter dem Haupt-Header ausgerichtet ist.
- Prüfen, dass Listeneinträge (z.B. `[FOLDER] ac3`) schwarzen Hintergrund und weiße Schrift haben.

## Status
- Die Änderungen stellen das konsistente Forensik-Dark-Theme und die Menüausrichtung wieder her.
- Die Mediengalerie und Navigation sind wieder optisch und funktional einheitlich.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob diese Bereinigungen wie beschrieben umgesetzt werden sollen.