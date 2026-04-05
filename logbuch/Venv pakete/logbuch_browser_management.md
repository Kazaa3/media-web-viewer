# Logbuch: Browser-Management & Multi-Browser-Testintegration

## Ziel
Flexible Verwaltung und Integration verschiedener Browser (Chromium, Chrome, Firefox) für automatisierte Tests, Multi-Session-Support und konfigurierbare Startmodi. Ermöglicht reproduzierbare Testläufe, parallele Sessions und gezielte Steuerung über globale Configs und Session-Parameter (PID, Port).

---

## 1. Unterstützte Browser & Modi
- **Chromium, Chrome, Firefox**: Unterstützung für alle gängigen Engines.
- **Headless/GUI-Modus**: Start im Hintergrund oder mit sichtbarer Oberfläche.
- **Global Config**: Zentrale Steuerung von Standard-Browser, Pfaden, Ports, Headless-Optionen etc.

---

## 2. Session-Management
- **Session-Parameter**: Jeder Testlauf erhält eigene PID, Port und ggf. temporäres Profil.
- **Mehrere Sessions parallel**: Ermöglicht parallele Testläufe (z.B. für CI/CD, Lasttests, Multi-User).
- **Session-Registry**: Verwaltung laufender Instanzen, Zuordnung von PID/Port zu Test-Session.

---

## 3. Testintegration
- **Automatisierte Tests**: Integration in Test-Suites (z.B. pytest, unittest, Selenium, Playwright).
- **Multi-Browser-Tests**: Jeder Test kann gezielt mit verschiedenen Browsern/Versionen ausgeführt werden.
- **Session-Setup/Teardown**: Automatisches Starten/Beenden der Browser-Session pro Testfall.
- **Port- und Profil-Handling**: Isolierte Profile und Ports für jede Session, um Kollisionen zu vermeiden.

---

## 4. Beispiel-Workflow
1. **Globale Konfiguration laden** (z.B. aus `config.json`):
   - Standard-Browser, Pfade, Headless, Default-Ports
2. **Session starten**:
   - Browser-Instanz mit gewünschtem Modus/Profil/Port starten
   - PID und Port registrieren
3. **Test ausführen**:
   - Automatisiert (z.B. Selenium/Playwright) gegen die Session
4. **Session beenden**:
   - Browser sauber terminieren, Ressourcen freigeben

---

## 5. Vorteile
- **Reproduzierbare Tests**: Gleiche Umgebung für jeden Lauf
- **Parallele Sessions**: Skalierbar für CI/CD und Multi-User
- **Flexible Steuerung**: Verschiedene Browser/Versionen/Modi einfach konfigurierbar
- **Fehlerdiagnose**: PID/Port-Tracking erleichtert Debugging

---

## 6. Best Practices
- **Profile isolieren**: Temporäre Profile pro Session, um Seiteneffekte zu vermeiden
- **Ports dynamisch wählen**: Freie Ports für parallele Sessions automatisch finden
- **Cleanup sicherstellen**: Nach jedem Testlauf alle Browser-Instanzen beenden
- **Globale Config versionieren**: Änderungen an Browserpfaden/Optionen nachvollziehbar halten

---

## Fazit
Mit diesem Ansatz lassen sich verschiedene Browser-Engines flexibel und reproduzierbar für automatisierte Tests und Multi-Session-Workflows managen. Globale Konfiguration, Session-Parameter und parallele Instanzen sorgen für maximale Kontrolle und Skalierbarkeit im Testbetrieb.
