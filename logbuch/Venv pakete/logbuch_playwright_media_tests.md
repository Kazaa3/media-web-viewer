# Logbuch: Playwright für automatisierte Media-App-Browser-Tests

## Ziel
Playwright als Standard für automatisierte End-to-End-Tests der Media-App (Video-Player, JS-Frontend). Ermöglicht Multi-Browser-Tests (Chrome, Firefox), HLS-Playback-Prüfung, Screenshots/Videos bei Fehlern und Integration in CI/CD (Docker, GitHub Actions).

---

## 1. Schnellstart (Python/pytest)
- In venv (offline via packages/):
  ```bash
  pip install playwright pytest-playwright pytest-html
  playwright install chromium  # Browser einmalig downloaden
  ```
- Beispiel-Test (test_media_app.py):
  ```python
  import pytest
  from playwright.sync_api import Page, expect

  @pytest.fixture(scope="session")
  def page(browser):
      page = browser.new_page()
      page.goto("http://localhost:3000")
      return page

  def test_video_playback(page: Page):
      expect(page.locator("#media-list")).to_be_visible()
      page.click("text=video1.mkv")
      expect(page.locator("video")).to_have_attribute("src", expect.anything())
      page.click("button:has-text('Play')")
      expect(page.locator("video")).to_have_js_property("paused", False)
      page.wait_for_timeout(2000)
      page.screenshot(path="test-playback.png")
  ```
- Run: `pytest test_media_app.py --headed --video=retry --html=report.html`

---

## 2. Docker für Tests (CI-ready)
- Dockerfile.test:
  ```dockerfile
  FROM mcr.microsoft.com/playwright/python:v1.47.0-focal
  WORKDIR /app
  COPY requirements.txt packages/ .
  RUN pip install --no-index --find-links packages/ -r requirements.txt
  COPY tests/ .
  CMD ["pytest", "--headed"]
  ```
- Build & Run:
  ```bash
  docker build -f Dockerfile.test -t app-tests .
  docker run --rm -p 3000:3000 -v $(pwd)/media:/media app-tests
  ```
- Testet gegen lokale App + Docker-Media-Tools.

---

## 3. Testfälle für Media-App
| Test                | Code-Snippet                                      |
|---------------------|---------------------------------------------------|
| Login/Media-Scan    | page.fill("#path", "/media"); page.click("#scan") |
| HLS-Stream          | expect(page.locator("video video")).to_play()     |
| Mobile              | page.set_viewport_size({"width": 375, "height": 812}) |
| Subs                | page.click("#sub-toggle"); expect(page.locator(".subtitle")).to_be_visible() |

---

## 4. pytest.ini für Reporting
```ini
[tool:pytest.ini_options]
addopts = -v --html=report.html --self-contained-html --video=retain-on-failure
```
- Generiert Videos/Screenshots bei Fehlern – ideal für Video-Player-Debug.

---

## 5. Vorteile
- Multi-Browser (Chromium, Firefox, WebKit)
- Headless/GUI, Video/Screenshot-Export
- Parallele Tests, Mobile-Emulation
- Perfekt für CI/CD, Docker, GitHub Actions

---

## Fazit
Playwright ist die optimale Lösung für automatisierte, reproduzierbare Media-App-Tests – von HLS-Playback bis UI-Regression. Integration in Docker und CI/CD garantiert stabile, nachvollziehbare Ergebnisse.
