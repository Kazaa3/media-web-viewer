

# GitHub Actions: Geckodriver/Firefox Fehler auf Ubuntu

## Problemstellung
Bei der Ausführung von UI- oder End-to-End-Tests mit Selenium und Firefox (geckodriver) auf GitHub Actions (Ubuntu-Runner) treten häufig Fehler auf, z.B.:
- `geckodriver not found`
- `Firefox binary not found`
- `SessionNotCreatedException: Unable to find a matching set of capabilities`
- Headless- oder Display-Probleme (z.B. Xvfb)

## Ursachen
- Geckodriver oder Firefox ist nicht vorinstalliert oder nicht im $PATH
- Versionen von Firefox und geckodriver sind inkompatibel
- Headless-Umgebung benötigt Xvfb oder spezielle Flags
- CI-Runner ist minimal und enthält keine Browser

## Lösungsmöglichkeiten
1. **Installation sicherstellen:**
	- Geckodriver und Firefox explizit im Workflow installieren, z.B. mit `apt-get install firefox-geckodriver` oder via Download.
2. **Versionen prüfen:**
	- Kompatible Versionen von Firefox und geckodriver verwenden (Release Notes beachten).
3. **Headless-Modus korrekt konfigurieren:**
	- Selenium mit `options.headless = True` starten
	- Falls nötig: Xvfb starten (`xvfb-run` vor den Testbefehl setzen)
4. **PATH anpassen:**
	- Sicherstellen, dass die Binaries im $PATH liegen (`which geckodriver`, `which firefox` prüfen)
5. **Beispiel für GitHub Actions Workflow-Step:**
	```yaml
	- name: Install Firefox and Geckodriver
	  run: |
		 sudo apt-get update
		 sudo apt-get install -y firefox geckodriver
	- name: Run Selenium Tests
	  run: |
		 xvfb-run pytest tests/e2e/
	```

## Hinweise
- Bei Problemen: Log-Ausgaben von Selenium, geckodriver und GitHub Actions prüfen
- Alternativen: Chromium/Chrome + chromedriver verwenden, falls Firefox nicht zwingend nötig
- Siehe auch: [GitHub Actions Runner Images](https://github.com/actions/runner-images)

---

**Letzte Aktualisierung:** 15.03.2026


# GitHub Actions: Geckodriver/Firefox Fehler auf Ubuntu

## Problemstellung
Bei der Ausführung von UI- oder End-to-End-Tests mit Selenium und Firefox (geckodriver) auf GitHub Actions (Ubuntu-Runner) treten häufig Fehler auf, z.B.:
- `geckodriver not found`
- `Firefox binary not found`
- `SessionNotCreatedException: Unable to find a matching set of capabilities`
- Headless- oder Display-Probleme (z.B. Xvfb)

## Ursachen
- Geckodriver oder Firefox ist nicht vorinstalliert oder nicht im $PATH
- Versionen von Firefox und geckodriver sind inkompatibel
- Headless-Umgebung benötigt Xvfb oder spezielle Flags
- CI-Runner ist minimal und enthält keine Browser

## Lösungsmöglichkeiten
1. **Installation sicherstellen:**
	- Geckodriver und Firefox explizit im Workflow installieren, z.B. mit `apt-get install firefox-geckodriver` oder via Download.
2. **Versionen prüfen:**
	- Kompatible Versionen von Firefox und geckodriver verwenden (Release Notes beachten).
3. **Headless-Modus korrekt konfigurieren:**
	- Selenium mit `options.headless = True` starten
	- Falls nötig: Xvfb starten (`xvfb-run` vor den Testbefehl setzen)
4. **PATH anpassen:**
	- Sicherstellen, dass die Binaries im $PATH liegen (`which geckodriver`, `which firefox` prüfen)
5. **Beispiel für GitHub Actions Workflow-Step:**
	```yaml
	- name: Install Firefox and Geckodriver
	  run: |
		 sudo apt-get update
		 sudo apt-get install -y firefox geckodriver
	- name: Run Selenium Tests
	  run: |
		 xvfb-run pytest tests/e2e/
	```

## Hinweise
- Bei Problemen: Log-Ausgaben von Selenium, geckodriver und GitHub Actions prüfen
- Alternativen: Chromium/Chrome + chromedriver verwenden, falls Firefox nicht zwingend nötig
- Siehe auch: [GitHub Actions Runner Images](https://github.com/actions/runner-images)

---

**Letzte Aktualisierung:** 15.03.2026
