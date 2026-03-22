<!-- Category: Documentation -->
<!-- Title_DE: Frontend, Interface & Design -->
<!-- Title_EN: Frontend, Interface & Design -->
<!-- Summary_DE: Gestaltung der Benutzeroberfläche: NiceGUI-Integration, Glassmorphism-Designsystem und intuitive Bedienbarkeit. -->
<!-- Summary_EN: User interface design: NiceGUI integration, Glassmorphism design system and intuitive usability. -->
<!-- Status: ACTIVE -->

# Frontend, Interface & Design

## Die Ästhetik von "dict"
Ein Kernziel von **dict - Web Media Player & Library** war es, sich von funktionalen, aber trockenen Medien-Verwaltern abzuheben. Das Ergebnis ist ein **Premium-Design**, das auf moderne Webinhalte setzt.

### Designsystem: Glassmorphism
Das visuelle Rückgrat von dict ist der **Glassmorphism-Stil**. 
- **Transparenz:** Halbtransparente Oberflächen lassen den Hintergrund dezent durchscheinen.
- **Blur-Effekte:** Hochwertige Unschärfefilter sorgen für Depth-of-Field und eine klare visuelle Hierarchie.
- **Vibrant Colors:** Akzente in lebendigen Farben (Vibrancy) führen das Auge des Nutzers und heben interaktive Elemente hervor.

## Von Eel zu NiceGUI
Die Entwicklung des Frontends durchlief eine signifikante Transformation:
1.  **Eel & HTML/JS:** Die ersten Versionen nutzten reines HTML5 und JavaScript. Dies bot volle Freiheit, erforderte aber viel manuelles DOM-Management.
2.  **NiceGUI Integration:** Zur Vereinfachung komplexer UI-Zustände wurde NiceGUI integriert. Es ermöglicht eine deklarative Beschreibung der UI in Python, während die Performance und Ästhetik des Webbrowsers erhalten bleiben.

## Interface-Elemente
Die Benutzeroberfläche ist in logische Bereiche unterteilt:
- **Medien-Bibliothek:** Ein Grid-Layout mit dynamischen Cover-Arts und schneller Filterung.
- **Player-Sektion:** Intuitive Controls für Play/Pause, Volume und Seek. Inklusive visueller Feedback-Effekte beim Hover.
- **Einstellungs-Panel:** Ein aufgeräumter Bereich zur Konfiguration von Scan-Verzeichnissen und Transcoding-Optionen.
- **Playlist-Management:** Ein Drag-and-Drop fähiger Bereich zum einfachen Sortieren und Verwalten der Warteschlange.

## UX-Philosophie
- **Reaktionsschnelligkeit:** Fast-Zero-Latency bei Klicks.
- **Visuelles Feedback:** Sanfte Animationen und Transitionen beim Wechsel zwischen Ansichten.
- **Daten-First:** Trotz des Fokus auf Design bleiben die Metadaten (Titel, Artist, Jahr) immer im Vordergrund und sind leicht lesbar.

*Das Frontend von dict ist mehr als nur eine Hülle – es ist das Fenster zur Medienwelt des Nutzers, gestaltet mit maximaler Präzision.*

<!-- lang-split -->

# Frontend, Interface & Design

## The Aesthetics of "dict"
A core goal of **dict - Web Media Player & Library** was to stand out from functional but dry media managers. The result is a **premium design** that focuses on modern web content.

### Design System: Glassmorphism
The visual backbone of dict is the **Glassmorphism style**.
- **Transparency:** Semi-transparent surfaces allow the background to shine through subtly.
- **Blur Effects:** High-quality blur filters provide depth-of-field and a clear visual hierarchy.
- **Vibrant Colors:** Accents in vibrant colors (vibrancy) guide the user's eye and highlight interactive elements.

## From Eel to NiceGUI
The development of the frontend underwent a significant transformation:
1.  **Eel & HTML/JS:** The first versions used pure HTML5 and JavaScript. This offered full freedom but required a lot of manual DOM management.
2.  **NiceGUI Integration:** To simplify complex UI states, NiceGUI was integrated. It allows a declarative description of the UI in Python while maintaining the performance and aesthetics of the web browser.

## Interface Elements
The user interface is divided into logical areas:
- **Media Library:** A grid layout with dynamic cover arts and fast filtering.
- **Player Section:** Intuitive controls for play/pause, volume and seek. Including visual feedback effects on hover.
- **Settings Panel:** A clean area for configuring scan directories and transcoding options.
- **Playlist Management:** A drag-and-drop capable area for easy sorting and management of the queue.

## UX Philosophy
- **Responsiveness:** Fast zero latency on clicks.
- **Visual Feedback:** Smooth animations and transitions when switching between views.
- **Data First:** Despite the focus on design, the metadata (title, artist, year) always remains in the foreground and is easy to read.

*The frontend of dict is more than just a shell – it is the window to the user's media world, designed with maximum precision.*
