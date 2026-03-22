<!-- Category: Documentation -->
<!-- Title_DE: Quality Gates, Benchmarking & CI/CD -->
<!-- Title_EN: Quality Gates, Benchmarking & CI/CD -->
<!-- Summary_DE: Professionalisierung des Release-Prozesses: GitHub Actions Pipelines, automatisierte Quality Gates und Performance-Benchmarking. -->
<!-- Summary_EN: Professionalization of the release process: GitHub Actions pipelines, automated quality gates and performance benchmarking. -->
<!-- Status: ACTIVE -->

# Quality Gates, Benchmarking & CI/CD

## Der Weg zur Release-Reife
Vom Hobby-Projekt zum stabilen Produkt: **dict - Web Media Player & Library** hat eine signifikante Professionalisierung seiner DevOps-Prozesse durchlaufen. Das Ziel: Jedes Release muss 100% stabil und performant sein.

## GitHub Actions & Pipelines
Unser CI/CD-System basiert auf GitHub Actions und ist in drei Hauptstränge unterteilt:
1.  **`backend-integration.yml`:** Führt bei jedem Push alle technischen und Basis-Tests in der `testbed`-Umgebung aus.
2.  **`ui-tests.yml`:** Startet die Selenium-Suite in einem Headless-Browser, um Frontend-Regresse zu verhindern.
3.  **`release.yml`:** Die "Königs-Pipeline". Sie baut automatisch Binärpakete für Linux (Debian) und Windows, sobald ein neuer Git-Tag erstellt wird.

## Die "Validation Engine" (Quality Gates)
Ein zentraler Meilenstein war die Einführung eines mandatory **Validation-Jobs** in der Release-Pipeline.
- **Kein Build ohne Test:** Erst wenn alle 240+ Tests (Unit, Integration, E2E) im CI-System grün sind, werden die Build-Server für Windows und Linux gestartet.
- **Transcoding-Checks:** Automatisierte Prüfung, ob die FFmpeg-Engine auf den Zielsystemen korrekt arbeitet.

## Benchmarking & Performance-Audits
Um sicherzustellen, dass dict nicht nur stabil, sondern auch schnell bleibt, wurde ein Benchmarking-System eingeführt:
- **Parser-Optimum:** Messung der Zeit, die die Pipeline benötigt, um tausende Dateien zu scannen.
- **Memory-Profiles:** Überwachung des RAM-Verbrauchs während intensiver Scan-Vorgänge.
- **Version-Vergleich:** Jedes neue Release wird gegen den "Baseline-Snapshot" der Vorversion gemessen, um Performance-Einbrüche sofort zu erkennen.

## Release Protection
Durch die strikte Nutzung von Branch Protection auf dem `main`-Branch und die automatisierten Gates in CI/CD ist dict gegen "unbemerkte" Bugs in der Produktion geschützt. 

*DevOps bei dict bedeutet: Vertrauen in den Code durch unerbittliche Automatisierung.*
