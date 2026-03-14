<!-- Category: Documentation -->
<!-- Title_DE: Scraping & Artwork-Metadaten -->
<!-- Title_EN: Scraping & Artwork Metadata -->
<!-- Summary_DE: Anreicherung der Bibliothek: Web-Scraper (Discogs, Amazon), lokale Cover-Extraktion und Scapy-Integration. -->
<!-- Summary_EN: Library enrichment: web scrapers (Discogs, Amazon), local cover extraction and Scapy integration. -->
<!-- Status: ACTIVE -->

# Scraping & Artwork-Metadaten

## Das Gesicht der Bibliothek: Covers
Eine Medienbibliothek ohne Bilder wirkt leblos. **dict - Web Media Player & Library** setzt daher auf eine zweigleisige Strategie, um jedem Album, Film und Buch sein Gesicht zurückzugeben.

### 1. Lokale Extraktion
Bevor wir das Internet befragen, sucht dict lokal:
- **Embedded Art:** Unsere Parser (Mutagen, PyMuPDF) extrahieren Cover-Bilder direkt aus den Metadaten-Tags von Dateien (ID3v2, MP4 Covers, EPUB Content).
- **Sidecar-Files:** Dict erkennt Bilder im selben Ordner wie das Medium (z. B. `folder.jpg`, `cover.png`) und ordnet sie automatisch zu.

### 2. Web-Scraping & Enrichment
Wenn lokal nichts gefunden wird, greift die Scraping-Pipeline:
- **Discogs & Amazon Scraper:** Wir nutzen spezialisierte Scraper, um anhand von Titel und Artist nach hochauflösenden Covern und fehlenden Daten (Erscheinungsjahr, Genre) zu suchen.
- **Mapping-Logik:** Intelligente Algorithmen vergleichen die Suchergebnisse und wählen das wahrscheinlichste Match aus, um "Dirty Data" zu vermeiden.

## Netzwerk-Diagnostik mit Scapy
Um sicherzustellen, dass unsere Scraper und die Kommunikation mit Online-Diensten stabil funktionieren, wurde **Scapy** integriert:
- **Verbindungs-Tests:** Automatisiertes Monitoring der Konnektivität zu den Metadaten-Providern.
- **Validierung:** Prüfung, ob Anfragen korrekt geroutet werden und keine Timeouts durch Netzwerk-Blockaden entstehen.

## Status-Tracking
In der Datenbank wird für jedes Item ein **Artwork-Status** gepflegt. So weiß das System immer:
- Hat das Item bereits ein Cover?
- Wurden Online-Quellen bereits erfolglos abgefragt?
- Muss der Nutzer manuell eingreifen?

*Durch das Zusammenspiel von lokaler Extraktion und intelligentem Scraping verwandelt dict eine simple Dateiliste in ein visuell beeindruckendes Medien-Erlebnis.*

<!-- lang-split -->

# Scraping & Artwork Metadata

## The Face of the Library: Covers
A media library without images feels lifeless. **dict - Web Media Player & Library** therefore relies on a two-pronged strategy to give every album, film, and book its face back.

### 1. Local Extraction
Before we ask the internet, dict searches locally:
- **Embedded Art:** Our parsers (Mutagen, PyMuPDF) extract cover images directly from the metadata tags of files (ID3v2, MP4 covers, EPUB content).
- **Sidecar Files:** Dict recognizes images in the same folder as the medium (e.g., `folder.jpg`, `cover.png`) and assigns them automatically.

### 2. Web Scraping & Enrichment
If local search fails, the scraping pipeline takes over:
- **Discogs & Amazon Scraper:** We use specialized scrapers to search for high-resolution covers and missing data (year of release, genre) based on title and artist.
- **Mapping Logic:** Intelligent algorithms compare the search results and select the most likely match to avoid "dirty data".

## Network Diagnostics with Scapy
To ensure that our scrapers and communication with online services function stably, **Scapy** was integrated:
- **Connection Tests:** Automated monitoring of connectivity to metadata providers.
- **Validation:** Checking whether requests are correctly routed and no timeouts occur due to network blockages.

## Status Tracking
An **artwork status** is maintained in the database for each item. This way, the system always knows:
- Does the item already have a cover?
- Have online sources already been queried unsuccessfully?
- Does the user need to intervene manually?

*Through the interplay of local extraction and intelligent scraping, dict transforms a simple file list into a visually stunning media experience.*
