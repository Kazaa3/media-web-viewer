# Logbuch: Scraping-Features für Media-Metadaten (Playwright)

## Ziel
Automatisiertes Scraping von Media-Metadaten (Cover, Tags, Beschreibungen) aus dynamischen Webquellen wie TMDB, IMDB, Amazon, Spotify, MusicBrainz – direkt integriert in die Media-Library. Playwright ermöglicht robuste, Anti-Bot-resistente Browser-Automation, auch in Docker/venv.

---

## 1. Setup & Tools
- **Python venv/Docker:**
  - `pip install playwright beautifulsoup4 parsel jmespath`
  - `playwright install chromium`
- **Docker:**
  - Basierend auf `mcr.microsoft.com/playwright/python:v1.47.0`
  - Pakete offline via `--find-links ./packages/`

---

## 2. Beispiel: TMDB/IMDB Scraper
```python
from playwright.sync_api import sync_playwright
import json
from bs4 import BeautifulSoup

def scrape_tmdb(title):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.themoviedb.org/search?query={title}")
        page.wait_for_selector("a.results-group-item")
        meta = page.locator("a.results-group-item").first
        poster = meta.locator("img").get_attribute("src")
        details = meta.inner_text()
        soup = BeautifulSoup(page.content(), "html.parser")
        overview = soup.select_one(".overview").text if soup.select_one(".overview") else ""
        browser.close()
        return {"poster": poster, "details": details, "overview": overview}
```
- **Nutzung:**
  - `meta = scrape_tmdb("Inception")`
  - Ergebnisse als JSON speichern oder in Supabase/DB ablegen

---

## 3. Erweiterte Features
| Feature           | Code-Snippet                                               |
|-------------------|-----------------------------------------------------------|
| Infinite Scroll   | `page.mouse.wheel(0, 1000); page.wait_for_selector(...)`   |
| Login (IMDB)      | `page.fill(...); page.click(...)`                          |
| API Intercept     | `page.route("**/api/**", lambda r: print(r.fetch().json()))` |
| Stealth/Anti-Bot  | `args=["--disable-blink-features=AutomationControlled"]`   |
| Parallel Scraping | `[context.new_page() for _ in range(5)]`                   |
| Rate-Limit        | `import asyncio; await asyncio.sleep(2)`                   |

---

## 4. Media-spezifische Scraping-Strategien
- **Amazon:** Cover-Suche, Screenshot, ggf. OCR (Tesseract)
- **Spotify/MusicBrainz:** Playlist- und Album-Scraping
- **TMDB/IMDB:** Titel, Jahr, Poster, Beschreibung, Rating
- **Fallback:** robots.txt beachten, nur öffentliche Daten scrapen

---

## 5. Integration in Media-Workflow
- Beim Scan unbekannter Medien (z.B. MKV ohne Metadaten):
  - Automatisch Scraper starten, Cover/Tags holen, Ergebnis cachen
  - Optional: Ergebnisse in Supabase/DB speichern
- In Docker/CI lauffähig, parallelisierbar

---

## 6. Legal & Best Practices
- Nur öffentliche Daten scrapen, robots.txt respektieren
- Rate-Limits und Captcha-Bypass beachten
- API-Intercept für strukturierte Daten bevorzugen

---

## Fazit
Mit Playwright und Scraping-Tools lassen sich Media-Metadaten automatisiert, robust und flexibel aus dem Web extrahieren – ideal für Cover, Tags und Zusatzinfos in der Media-Library. Erweiterbar für neue Quellen und Features (z.B. OCR, Parallelisierung, Stealth).
