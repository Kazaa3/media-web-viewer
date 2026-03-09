<!-- Category: docs -->
<!-- Title_DE: GUI-Elemente und Wording -->
<!-- Title_EN: GUI Elements and Wording -->
<!-- Summary_DE: Dokumentation der Benutzeroberfläche: Tabs, Bereiche, Buttons und deren Bezeichnungen -->
<!-- Summary_EN: Documentation of user interface: tabs, areas, buttons and their labels -->
<!-- Status: docs -->
<!-- Date: 2026-03-09 -->

# GUI-Elemente und Wording

## Übersicht
Dokumentation der Benutzeroberfläche des MediaWebViewers mit allen Tabs, Bereichen, Buttons und deren deutschen/englischen Bezeichnungen.

## Hauptstruktur

### Header
- **App-Titel**: "Media Player" (de/en)
- **Sprachbutton**: 🇩🇪/🇬🇧 für Sprachwechsel
- **Version-Info**: Anzeige der aktuellen Version

### Tab-Navigation (Hauptmenü)

| Tab-ID | Deutsch | Englisch | Icon | data-i18n Key |
|--------|---------|----------|------|---------------|
| `player` | Player | Player | - | `nav_player` |
| `library` | Bibliothek | Library | - | `nav_library` |
| `browser` | Browser | Browser | - | `nav_browser` |
| `edit` | Edit | Edit | - | `nav_edit` |
| `options` | Optionen | Options | - | `nav_options` |
| `parser` | Parser | Parser | - | `nav_parser` |
| `debug` | Debug DB | Debug DB | - | `nav_debug` |
| `tests` | Tests | Tests | - | `nav_tests` |
| `logbuch` | 📓 Logbuch | 📓 Logbook | 📓 | `nav_logbook` |
| `vlc` | 🎬 Video Player | 🎬 Video Player | 🎬 | `nav_video` |
| - | ⚙️ Flags | ⚙️ Flags | ⚙️ | `nav_flags` |

### Action-Buttons (Header-Bereich)
- **✨ Features**: Feature-Übersicht öffnen (`btn_features`)
- **Scan Media**: Medienverzeichnisse scannen (`btn_scan_media`)

## Tab-Inhalte

### 1. Player-Tab
**Zweck**: Audio-Wiedergabe und Playlist-Verwaltung

**Elemente**:
- Media-Liste mit Cover, Titel, Künstler
- Audio-Player-Element (`<audio>`)
- Status-Anzeige
- Medien-Cover: 50x50px, abgerundet

### 2. Library-Tab (Bibliothek)
**Zweck**: Übersicht der Medienbibliothek mit Kategorisierung

**Filter**:
- Nach Kategorien (Hörbücher, Musik, etc.)
- Such-Funktionalität

### 3. Browser-Tab
**Zweck**: Dateisystem-Browser mit Ordnerverwaltung

**Buttons**:
- **➕ Add Path**: Pfad hinzufügen (`fb_add_path`)
- Ordner-Liste mit Entfernen-Funktion

### 4. Edit-Tab (Metadaten-Editor)
**Zweck**: Metadaten bearbeiten und Dateien umbenennen

**Bereiche**:
- **Titel**: "Metadaten Editor" / "Metadata Editor" (`edit_title`)
- **Untertitel**: Beschreibung (`edit_subtitle`)
- **Such-Feld**: Bibliothek durchsuchen (`edit_search_library_placeholder`)

**Formular**:
- Dateiname bearbeiten
- Metadaten-Felder (Title, Artist, Album, etc.)
- **Buttons**:
  - ✏️ Rename (`edit_btn_rename`)
  - Speichern (`edit_btn_save`)
  - Abbrechen (`edit_btn_cancel`)
  - 🗑️ Löschen (`edit_btn_delete`)

**Placeholder**: "Wähle links ein Element aus..." (`edit_placeholder_text`)

### 5. Options-Tab (Optionen)
**Zweck**: Anwendungseinstellungen

**Bereiche**:
- **Titel**: "Optionen" / "Options" (`options_title`)

**Scan-Verzeichnisse**:
- **Überschrift**: "Scan-Verzeichnisse" (`options_scan_dirs`)
- **Beschreibung**: Erklärung (`options_scan_dirs_desc`)
- **Buttons**:
  - Verzeichnis hinzufügen (`options_add_dir`)
  - Standard-Verzeichnis hinzufügen (`options_add_default_dir`)

**Darstellung**: (`options_appearance`)
- Parser-Zeiten anzeigen (`options_show_parser_times`)
- Beschreibung (`options_show_parser_times_desc`)

### 6. Parser-Tab
**Zweck**: Parser-Konfiguration und Reihenfolge

**Parser-Chain**:
- Drag & Drop Liste
- Parser: filename, container, mutagen, pymediainfo, ffmpeg
- Parser-Mode: lightweight, normal

### 7. Debug-Tab (Debug DB)
**Zweck**: Datenbankinspektion und Debug-Informationen

**Features**:
- DB-Statistiken
- Item-Details anzeigen
- Rohdaten-Inspektion

### 8. Tests-Tab
**Zweck**: Test-Suite ausführen

**Elemente**:
- Test-Suites auswählen
- Test-Output anzeigen
- Exit-Codes

### 9. Logbuch-Tab 📓
**Zweck**: Projekt-Dokumentation und Entwicklungs-Log

**Struktur**:
- **Sidebar**:
  - Filter nach Status (ALL, COMPLETED, ACTIVE, PLANNED, DOCS, BUG)
  - Filter nach Kategorie (Alle, Planung, Development, etc.)
  - Eintragsliste mit Icons
  - Neu-Button

- **Content-Bereich**:
  - Metadata-Tags (Category, Status, Titles, Date)
  - Markdown-Inhalt (rendered mit marked.js)
  - Edit-Button

**Editor-Modal**:
- Filename (editierbar bei Umbenennung)
- Category (Dropdown)
- Status (Dropdown)
- Title_DE, Title_EN
- Summary_DE, Summary_EN
- Date (automatisch)
- Content (Markdown-Textarea)
- Speichern/Abbrechen-Buttons

**Status-Icons**:
- ✅ COMPLETED
- 🟢 ACTIVE
- 🧭 PLAN
- 📘 DOCS
- 🐞 BUG

**Pinned Entries**:
- 📌 Bugs (00_Known_Issues.md)
- 📌 Features (01_Features.md)

### 10. VLC-Tab 🎬
**Zweck**: Video-Wiedergabe und VLC-Integration

**Features**:
- Playlist-Export
- VLC-Nutzungshinweise

## Sidebar (Rechts)

**Bereiche**:
- **Titel**: "Kein Lied gewählt" / "No song selected" (`sb_no_song`)
- Medien-Cover (groß)
- Metadaten-Anzeige:
  - Title
  - Artist
  - Album
  - Duration, Bitrate, Samplerate
  - Format, Codec
  - Channels

## Player-Controls (Footer)

**Elemente**:
- Audio-Player mit Controls
- Status-Anzeige
- Play/Pause, Seek, Volume
- 40px Höhe

## Internationalisierung (i18n)

**System**:
- Alle UI-Elemente haben `data-i18n` Attribute
- Sprachen: Deutsch (de), Englisch (en)
- Sprachwechsel über Flag-Button (🇩🇪/🇬🇧)
- Fallback zu `currentLanguage` (default: 'de')

**Translation-Keys Struktur**:
```
nav_*        - Navigation Tabs
btn_*        - Buttons
edit_*       - Edit Tab
options_*    - Options Tab
sb_*         - Sidebar
logbook_*    - Logbook Tab
vlc_*        - VLC Tab
app_*        - App-weite Elemente
```

## Design-System

### Farben
- **Primary**: `#2a7` (Grün für Aktionen)
- **Secondary**: `#0277bd` (Blau für Logbuch)
- **Background**: `#fafafa`
- **White**: `#ffffff`
- **Text**: `#333`, `#666` (sekundär)
- **Border**: `#ddd`, `#eee`

### Typografie
- **Font**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **H1**: 1.5em
- **H2**: 1.25em
- **Body**: 1em
- **Small**: 0.85-0.9em

### Spacing
- **Padding**: Standard 10-20px
- **Margin**: 8-25px zwischen Elementen
- **Border-Radius**: 4-8px (Buttons, Cards)

### Komponenten
- **Tab-Buttons**: Padding 6px 12px, Border 1px, Rounded 4px
- **Media-Items**: Padding 12px, Rounded 8px, Shadow
- **Buttons**: Primary (#2a7), Secondary (#ddd)
- **Modals**: Overlay mit centered content

## Spezielle Features

### Splitter
- **Vertikaler Splitter**: 6px breit, Drag & Drop
- Hover-Farbe: `#2a7`
- Cursor: `col-resize`

### Drag & Drop
- Parser-Liste: Reihenfolge ändern
- Cursor: `grab` / `grabbing`

### Loading-States
- **Spinner**: Rotating border animation
- Größe: 14x14px
- Farbe: `#2a7`

### Responsive Verhalten
- Flex-Layout für Anpassung
- Sidebar rechts (ca. 420px)
- Main-Content: Flex 1
- Splitter für manuelle Größenanpassung

## Technische Details

**Markup-Struktur**:
```html
<body>
  <div class="header-container">
    <h1> + <div class="tab-buttons">
  </div>
  <div class="layout-container">
    <div class="left-panel"> (Tabs)
    <div class="splitter-v">
    <div id="sidebar"> (rechts)
  </div>
  <div class="player-container">
    <audio id="player">
    <div id="status">
  </div>
</body>
```

**Tab-Switching**:
- Funktion: `switchTab(tabId, buttonElement)`
- Zeigt/Versteckt `.tab-content` Elemente
- Setzt `.active` Klasse

**State-Management**:
- `currentLanguage`: 'de' | 'en'
- `currentLogbuchEntries`: Array von Einträgen
- `currentLogbookEditName`: Aktiver Edit-Name

## Verweise
- Markup: [web/app.html](../web/app.html)
- i18n-System: Inline translations object
- Logbuch-Rendering: marked.js Integration
- Commit: 37029cc

<!-- lang-split -->

# GUI Elements and Wording

## Overview
Documentation of the MediaWebViewer user interface with all tabs, areas, buttons and their German/English labels.

## Main Structure

### Header
- **App Title**: "Media Player" (de/en)
- **Language Button**: 🇩🇪/🇬🇧 for language switch
- **Version Info**: Display of current version

### Tab Navigation (Main Menu)

| Tab-ID | German | English | Icon | data-i18n Key |
|--------|--------|---------|------|---------------|
| `player` | Player | Player | - | `nav_player` |
| `library` | Bibliothek | Library | - | `nav_library` |
| `browser` | Browser | Browser | - | `nav_browser` |
| `edit` | Edit | Edit | - | `nav_edit` |
| `options` | Optionen | Options | - | `nav_options` |
| `parser` | Parser | Parser | - | `nav_parser` |
| `debug` | Debug DB | Debug DB | - | `nav_debug` |
| `tests` | Tests | Tests | - | `nav_tests` |
| `logbuch` | 📓 Logbuch | 📓 Logbook | 📓 | `nav_logbook` |
| `vlc` | 🎬 Video Player | 🎬 Video Player | 🎬 | `nav_video` |
| - | ⚙️ Flags | ⚙️ Flags | ⚙️ | `nav_flags` |

### Action Buttons (Header Area)
- **✨ Features**: Open feature overview (`btn_features`)
- **Scan Media**: Scan media directories (`btn_scan_media`)

## Tab Contents

### 1. Player Tab
**Purpose**: Audio playback and playlist management

**Elements**:
- Media list with cover, title, artist
- Audio player element (`<audio>`)
- Status display
- Media cover: 50x50px, rounded

### 2. Library Tab
**Purpose**: Media library overview with categorization

**Filters**:
- By categories (Audiobooks, Music, etc.)
- Search functionality

### 3. Browser Tab
**Purpose**: Filesystem browser with folder management

**Buttons**:
- **➕ Add Path**: Add path (`fb_add_path`)
- Folder list with remove function

### 4. Edit Tab (Metadata Editor)
**Purpose**: Edit metadata and rename files

**Areas**:
- **Title**: "Metadaten Editor" / "Metadata Editor" (`edit_title`)
- **Subtitle**: Description (`edit_subtitle`)
- **Search Field**: Search library (`edit_search_library_placeholder`)

**Form**:
- Edit filename
- Metadata fields (Title, Artist, Album, etc.)
- **Buttons**:
  - ✏️ Rename (`edit_btn_rename`)
  - Save (`edit_btn_save`)
  - Cancel (`edit_btn_cancel`)
  - 🗑️ Delete (`edit_btn_delete`)

**Placeholder**: "Select an element on the left..." (`edit_placeholder_text`)

### 5. Options Tab
**Purpose**: Application settings

**Areas**:
- **Title**: "Optionen" / "Options" (`options_title`)

**Scan Directories**:
- **Heading**: "Scan-Verzeichnisse" (`options_scan_dirs`)
- **Description**: Explanation (`options_scan_dirs_desc`)
- **Buttons**:
  - Add directory (`options_add_dir`)
  - Add default directory (`options_add_default_dir`)

**Appearance**: (`options_appearance`)
- Show parser times (`options_show_parser_times`)
- Description (`options_show_parser_times_desc`)

### 6. Parser Tab
**Purpose**: Parser configuration and order

**Parser Chain**:
- Drag & Drop list
- Parsers: filename, container, mutagen, pymediainfo, ffmpeg
- Parser mode: lightweight, normal

### 7. Debug Tab (Debug DB)
**Purpose**: Database inspection and debug information

**Features**:
- DB statistics
- Show item details
- Raw data inspection

### 8. Tests Tab
**Purpose**: Run test suite

**Elements**:
- Select test suites
- Show test output
- Exit codes

### 9. Logbook Tab 📓
**Purpose**: Project documentation and development log

**Structure**:
- **Sidebar**:
  - Filter by status (ALL, COMPLETED, ACTIVE, PLANNED, DOCS, BUG)
  - Filter by category (All, Planning, Development, etc.)
  - Entry list with icons
  - New button

- **Content Area**:
  - Metadata tags (Category, Status, Titles, Date)
  - Markdown content (rendered with marked.js)
  - Edit button

**Editor Modal**:
- Filename (editable for rename)
- Category (dropdown)
- Status (dropdown)
- Title_DE, Title_EN
- Summary_DE, Summary_EN
- Date (automatic)
- Content (Markdown textarea)
- Save/Cancel buttons

**Status Icons**:
- ✅ COMPLETED
- 🟢 ACTIVE
- 🧭 PLAN
- 📘 DOCS
- 🐞 BUG

**Pinned Entries**:
- 📌 Bugs (00_Known_Issues.md)
- 📌 Features (01_Features.md)

### 10. VLC Tab 🎬
**Purpose**: Video playback and VLC integration

**Features**:
- Playlist export
- VLC usage instructions

## Sidebar (Right)

**Areas**:
- **Title**: "Kein Lied gewählt" / "No song selected" (`sb_no_song`)
- Media cover (large)
- Metadata display:
  - Title
  - Artist
  - Album
  - Duration, Bitrate, Samplerate
  - Format, Codec
  - Channels

## Player Controls (Footer)

**Elements**:
- Audio player with controls
- Status display
- Play/Pause, Seek, Volume
- 40px height

## Internationalization (i18n)

**System**:
- All UI elements have `data-i18n` attributes
- Languages: German (de), English (en)
- Language switch via flag button (🇩🇪/🇬🇧)
- Fallback to `currentLanguage` (default: 'de')

**Translation Keys Structure**:
```
nav_*        - Navigation Tabs
btn_*        - Buttons
edit_*       - Edit Tab
options_*    - Options Tab
sb_*         - Sidebar
logbook_*    - Logbook Tab
vlc_*        - VLC Tab
app_*        - App-wide Elements
```

## Design System

### Colors
- **Primary**: `#2a7` (Green for actions)
- **Secondary**: `#0277bd` (Blue for logbook)
- **Background**: `#fafafa`
- **White**: `#ffffff`
- **Text**: `#333`, `#666` (secondary)
- **Border**: `#ddd`, `#eee`

### Typography
- **Font**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **H1**: 1.5em
- **H2**: 1.25em
- **Body**: 1em
- **Small**: 0.85-0.9em

### Spacing
- **Padding**: Standard 10-20px
- **Margin**: 8-25px between elements
- **Border-Radius**: 4-8px (Buttons, Cards)

### Components
- **Tab Buttons**: Padding 6px 12px, Border 1px, Rounded 4px
- **Media Items**: Padding 12px, Rounded 8px, Shadow
- **Buttons**: Primary (#2a7), Secondary (#ddd)
- **Modals**: Overlay with centered content

## Special Features

### Splitter
- **Vertical Splitter**: 6px wide, Drag & Drop
- Hover color: `#2a7`
- Cursor: `col-resize`

### Drag & Drop
- Parser list: Change order
- Cursor: `grab` / `grabbing`

### Loading States
- **Spinner**: Rotating border animation
- Size: 14x14px
- Color: `#2a7`

### Responsive Behavior
- Flex layout for adaptation
- Sidebar right (approx. 420px)
- Main content: Flex 1
- Splitter for manual resizing

## Technical Details

**Markup Structure**:
```html
<body>
  <div class="header-container">
    <h1> + <div class="tab-buttons">
  </div>
  <div class="layout-container">
    <div class="left-panel"> (Tabs)
    <div class="splitter-v">
    <div id="sidebar"> (right)
  </div>
  <div class="player-container">
    <audio id="player">
    <div id="status">
  </div>
</body>
```

**Tab Switching**:
- Function: `switchTab(tabId, buttonElement)`
- Shows/Hides `.tab-content` elements
- Sets `.active` class

**State Management**:
- `currentLanguage`: 'de' | 'en'
- `currentLogbuchEntries`: Array of entries
- `currentLogbookEditName`: Active edit name

## References
- Markup: [web/app.html](../web/app.html)
- i18n System: Inline translations object
- Logbook rendering: marked.js integration
- Commit: 37029cc
