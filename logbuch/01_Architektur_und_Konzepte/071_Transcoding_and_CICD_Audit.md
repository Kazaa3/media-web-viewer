# 117 – Professionalisierung der CI/CD-Infrastruktur

**Datum:** 12.03.2026  
**Version:** 1.3.5  
**Status:** ✅ Implementation Completed  

## Kontext / Context
Nach dem erfolgreichen Baseline-Audit ([Logbuch 116](116_Baseline_Audit_and_Roadmap.md)) wurde deutlich, dass die bestehenden CI/CD-Pipelines nicht ausreichten, um die hohe Qualität des Media Web Viewers über verschiedene Umgebungen hinweg zu garantieren. Dieses Logbuch dokumentiert die Migration zu einer robusten, mehrstufigen Test-Infrastruktur.

Following the successful baseline audit, it became clear that the existing CI/CD pipelines were insufficient to guarantee the Media Web Viewer's high quality across various environments. This logbook documents the migration to a robust, multi-stage testing infrastructure.

---

## 🛠️ Environment Integration (vEnvs in CI)
Bisher wurden die spezialisierten virtuellen Umgebungen (`testbed`, `selenium`, `build`) nur lokal genutzt. Wir haben diese Logik nun in GitHub Actions abgebildet.

Previously, specialized virtual environments were only used locally. We have now mirrored this logic in GitHub Actions.

- **Dependency Matching:** Die Runner nutzen nun exakt die `requirements-*.txt` Dateien aus dem `infra/` Ordner, die auch für die lokalen vEnvs verwendet werden.
- **System Parity:** Installation von Binär-Abhängigkeiten (`ffmpeg`, `mediainfo`, `xvfb`) direkt auf den Ubuntu-Runnern, um die `testbed`-Umgebung zu simulieren.

---

## 🚀 Neue Workflow-Architektur / New Workflow Architecture

### 1. Unified Backend Testing (`backend-integration.yml`)
Der Fokus verschob sich von einem isolierten Docker-Smoke-Test hin zu einer vollwertigen Host-Validierung.
- **Jobs:** 
  - `backend-tests`: Führt die kompletten `tests/tech/` (Parser-Logik) und `tests/basic/` (Core-Stabilität) aus.
  - `backend-docker-smoke`: Erhält die Container-Kompatibilität aufrecht.

### 2. Automatisierte UI-Tests (`ui-tests.yml`) [NEW]
Einführung einer dedizierten Pipeline für Frontend-Regressionen.
- **Headless Mode:** Einsatz von `Xvfb` (X Virtual Framebuffer), um Selenium-Tests ohne physisches Display auszuführen.
- **Driver Management:** Automatisierte Bereitstellung von `geckodriver` für Firefox-basierte E2E-Tests.

---

## ⚓ Release Protection (Gatekeeping)
Die kritischste Änderung betrifft den `release.yml` Workflow. Ein Release wird nun durch "Test-Gates" geschützt.

The most critical change affects the `release.yml` workflow. Releases are now protected by "test gates."

- **Validation Phase:** Bevor ein Build startet, müssen alle technischen Tests und UI-Tests in einer neuen `validation` Stage erfolgreich abgeschlossen sein.
- **Needs Mechanism:** `build-linux` und `build-windows` hängen nun explizit von der `validation` ab. Ein Scheitern der Tests verhindert die Generierung von Binär-Artefakten.

---

## 📈 Fazit / Conclusion
Mit der Implementierung dieser Maßnahmen ist die Lücke zwischen lokaler Entwicklung und globalem Deployment geschlossen. Der Media Web Viewer verfügt nun über eine "Enterprise-Grade" CI/CD-Infrastruktur, die Transcoding-Fixes und Format-Diversität bei jedem Commit validiert.

With these measures, the gap between local development and global deployment is closed. The Media Web Viewer now features an "enterprise-grade" CI/CD infrastructure that validates transcoding fixes and format diversity on every commit.

*Dokumentiert von Antigravity (AI Coding Assistant)*
