---
Debian Helper Scripts (dev workflow)

Folgende Hilfsskripte wurden implementiert, um den Entwicklungs-Workflow zu optimieren:

- ./scripts/purge_deb.sh
  * Entfernt das Debian-Paket und alle zugehörigen Konfigurationen vollständig für einen sauberen Zustand.

- ./scripts/dev_rebuild_deb.sh
  * Automatisiert den gesamten Zyklus: Baut das Paket, entfernt die alte Version und installiert den frischen Build.
  * Option --fast: Überspringt Test-Gates für schnelle Iteration.

Beide Skripte sind im develop-Branch committed und in walkthrough.md dokumentiert.

Schnelle Iteration:
  ./scripts/dev_rebuild_deb.sh --fast

Finalisierte Dokumentation:
- walkthrough.md enthält jetzt Anweisungen zu Environment Awareness, Fast-Build-Skripten, Version Synchronization und den neuen deb-Management-Skripten.

Tipp:
- Mit purge_deb.sh kannst du jederzeit eine neue deb sauber installieren.
---
Empfehlung:
Füge einen kurzen Header (Docstring oder Kommentar) hinzu, der Zweck und Testziel beschreibt.
---
