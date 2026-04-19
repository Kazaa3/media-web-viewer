# Implementation Plan – v1.41.106 Atomic HTML Rebuild

## Ziel
Vollständiger Neuaufbau des HTML-Shells, um alle Altlasten und Komplexitäten zu eliminieren, die zum "Black Screen"-Fehler geführt haben. Die Anwendung erhält eine moderne, forensisch auswertbare UI-Basis.

---

## Phase 1: Core Shell Architecture
- **[NEW] shell_master.html**
  - Semantic Structure: Aufbau mit modernen HTML5-Elementen (<header>, <nav>, <main>).
  - Top Menu (Head): Neuaufbau der Hauptkategorie-Leiste (Player, Bibliothek, Database, etc.) mit High-Density-Styling.
  - Sub Menu (Neck): Dynamische Pillenleiste, die ihr Layout aus der Python-SSOT bezieht.
  - Main Viewport (Body): Sauberer, einspaltiger Container für alle fragmentbasierten Views.
  - Monitoring IDs: Re-Integration aller kritischen Diagnose-IDs (diag-pid, diag-boot, diag-up) in ein fixes "Elite HUD".

## Phase 2: Design System
- **[NEW] shell_master.css**
  - Glassmorphism: Modernes, transparentes Design mit Backdrop-Blur.
  - Responsive Grid: Flexbox-basiertes Layout für maximale Stabilität.
  - High-Density Typography: Professionelles UI mit kuratierten Schriftarten.

## Phase 3: Backend Handshake
- **[MODIFY] main.py**
  - Start Hook: eel.start() wird auf das neue shell_master.html umgeleitet.

---

## Forensic Monitoring
- Die neue Shell enthält dedizierte DOM-Hooks für PID, BOOT-Zeit und UPTIME-Diagnostik. Die Oberfläche ist damit von Grund auf "Forensic Ready".

---

## Verification Plan
- **Bootstrap Check:** App starten und prüfen, ob das neue Atomic Shell geladen wird.
- **Top-Menu Test:** Klick auf "Player" oder "Bibliothek" wechselt korrekt die Hauptkategorie.
- **Sub-Menu Test:** Kontextuelle Pills (Queue, Visualizer, etc.) erscheinen in der neuen "Neck"-Bar.
- **HUD Check:** PID und BOOT-Zeit werden im Header korrekt angezeigt und aktualisiert.

---

**Hinweis:** Die alte app.html bleibt erhalten, wird aber umgangen.

**Review erforderlich nach Umsetzung!**
