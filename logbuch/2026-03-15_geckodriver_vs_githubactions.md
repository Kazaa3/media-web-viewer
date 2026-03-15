# Logbuch: Zusammenhang Geckodriver & GitHub Actions Fehler

**Datum:** 15.03.2026

## Frage
Hat der Geckodriver-Fehler direkt mit dem Browser zu tun, oder ist es ein Problem von GitHub Actions?

## Antwort
- **Geckodriver** ist ein separates Binary, das für die Steuerung von Firefox durch automatisierte Test-Frameworks (z.B. Selenium, pytest-selenium) benötigt wird.
- Der Fehler im CI-Log ("Package 'firefox-geckodriver' has no installation candidate") entsteht, weil das Systempaket für Geckodriver in Ubuntu 24.04 nicht mehr verfügbar ist.
- **GitHub Actions** ist nur die Umgebung, in der das Problem sichtbar wird: Das CI-Image versucht, Geckodriver per `apt install` zu installieren, was fehlschlägt.
- Das Problem ist also **nicht durch den Browser selbst verursacht**, sondern durch die Art, wie Geckodriver im CI installiert wird.
- Die Ursache ist eine Paketänderung in der Ubuntu-Distribution, nicht ein Fehler im Browser oder in Geckodriver selbst.

## Fazit
- Geckodriver ist für automatisierte Firefox-Tests zwingend nötig.
- Der Fehler kommt von der CI-Umgebung (GitHub Actions/Ubuntu 24.04), weil das Paket fehlt.
- Lösung: Geckodriver direkt von Mozilla herunterladen und installieren (siehe vorherigen Logbucheintrag).
