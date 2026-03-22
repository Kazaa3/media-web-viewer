---

# Logbuch-Eintrag: Wireframe-Analyse & Anker-Kommentare für Tab- und Panel-Struktur (März 2026)

## Ziel

Die zunehmende Komplexität und Zeilenzahl in app.html erschwert die Wartung und gezielte Reparatur der Tab- und Panel-Struktur. Um DOM-Fehler und Tab-Instabilitäten nachhaltig zu vermeiden, werden folgende Maßnahmen empfohlen:


## Maßnahmen
  
  - Alle bisher gebrochenen oder fehleranfälligen Stellen im HTML sollten mit auffälligen Kommentaren markiert werden, z.B. <!-- ACHTUNG: Hier war häufig ein DIV-Fehler! -->
  - Hinter jedem schließenden </div> sollte ein kurzer Kommentar stehen, was genau endet (z.B. <!-- END: Optionen-Panel -->, <!-- END: Split-Container -->).
  - Das erleichtert die spätere Fehlersuche und verhindert erneute Strukturfehler an bekannten Problemstellen.
  - Erstellung einer grafischen oder strukturierten Übersicht (Wireframe) der Tab- und Panel-Hierarchie.
  - Visualisierung der wichtigsten Container (Splits, Panels, Tabs, Footer) und ihrer Beziehungen.
  - Markierung aller kritischen DIV-Punkte (Panel-Start/Ende, Split-Container, Tab-Content) mit klaren HTML-Kommentaren, z.B.:
    - <!-- TAB: Parser START -->
    - <!-- TAB: Debug END -->
    - <!-- SPLIT: Vertical START -->
  - So werden Tab-Grenzen und Panel-Zuordnung auch bei vielen Codezeilen schnell auffindbar.
  - Nach jeder strukturellen Änderung gui_validator.py und manuelle Wireframe-Prüfung durchführen.

  - Haupt-Tabs (z.B. Optionen, Parser, Debug, Tests) und Unterreiter/Sub-Tabs (z.B. General, Tools, Environment innerhalb von Optionen) sollten im Code klar durch HTML-Kommentare getrennt werden.
  - Beispiel für Kommentierung:

    <!-- TAB: Optionen START -->
      ...
      <!-- SUBTAB: Optionen-General START -->
        ...
      <!-- SUBTAB: Optionen-General END -->
      <!-- SUBTAB: Optionen-Tools START -->
        ...
      <!-- SUBTAB: Optionen-Tools END -->
    <!-- TAB: Optionen END -->

    <!-- TAB: Parser START -->
      ...
    <!-- TAB: Parser END -->


  - **HTML:**
    - Panels/Sections: Klare Trennung und Kommentierung aller Hauptbereiche (Header, Sidebar, Main, Footer, Modals).
    - Reusable Components: Wiederkehrende UI-Elemente (z.B. Card, Button, Modal) als eigene Templates oder mit Kommentaren kennzeichnen.
    - Formulare: Input-Gruppen, Validierungsbereiche und Submit-Buttons klar trennen.
    - Dynamische Bereiche: Bereiche, die per JS befüllt werden, mit Kommentaren markieren (<!-- DYNAMIC: Media List -->).
  - **JS:**
    - Event-Handler nach Bereich/Funktion gruppieren (z.B. Player-Events, Tab-Events, Form-Events).
    - UI-Logik (DOM-Manipulation) und Datenlogik (API-Calls, Parsing) trennen.
    - i18n-Initialisierung in eigenes Modul/Funktionsblock auslagern.
    - State-Management zentral bündeln (aktiver Tab, aktueller Song, User-Settings).
    - Utility-Funktionen separat halten und nicht mit UI-Logik vermischen.
  - **Allgemein:**
    - Kommentierung aller logischen Blöcke, dynamischen Ein-/Ausblendungen und Schnittstellen.
    - Einheitliche Namenskonventionen für IDs/Klassen (z.B. tab-*, panel-*, btn-*, section-*).


## Fazit

Wireframe-Analyse und Anker-Kommentare sind essenziell, um die Übersicht und Wartbarkeit der Tab- und Panel-Struktur in großen HTML-Dateien zu sichern. Sie helfen, DOM-Fehler frühzeitig zu erkennen und gezielt zu beheben.

## HTML-Stabilisierung und UI-Fixes für app.html

## Walkthrough: HTML-Stabilisierung & UI-Fixes

Ich habe die Stabilisierung von app.html abgeschlossen und mehrere UI-Probleme wie gewünscht behoben.

### Änderungen im Detail
1. **Strukturelle Stabilisierung (Anker-Kommentare)**
  - Detaillierte Anker-Kommentare an allen Hauptbereichen:
    - Navigation Tabs: <!-- TAB BUTTONS START/END -->
    - Sidebar: <!-- SIDEBAR START/END -->
    - Tab Panels: Alle Hauptpanels (Library, Item, Playlist, Edit, Options, Parser, Debug, Tests, Reporting, Video Player, Logbuch) mit <!-- TAB: [Name] START/END -->
  - Kritischen Nesting-Fehler behoben: options-tools-view hatte ein fehlendes </div>, wodurch alle nachfolgenden Tabs unsichtbar wurden.
2. **Options-Tab & Sub-Tabs**
  - Hauptüberschrift: Zentrale Header-Zeile mit ID options-main-header ergänzt, die dynamisch aktualisiert wird.
  - Sub-Tab-Styling: Harte Inline-Styles aus den Buttons "General", "Tools", "Environment" entfernt und stattdessen eine eigene .options-subtab.active CSS-Klasse eingeführt (blaue Unterstreichung bei aktivem Sub-Tab).
  - Funktionalität: switchOptionsView aktualisiert, damit sowohl Header als auch Button-Active-State korrekt gesetzt werden.
  - Redundante lokale Header entfernt.
3. **Audio Player Footer ("Spielt: von")**
  - i18n-Logik in updateMediaSidebar verbessert: Zeigt bei Idle/kein Track korrekt den Placeholder "Wähle ein Lied aus der Liste!" statt "Spielt: von".
4. **Sidebar Transcoding-Tag**
  - [TRANSCODED]-Badge in der Sidebar wiederhergestellt; erscheint korrekt, wenn item.is_transcoded true ist.

### Verifikation
**HTML-Struktur:**
  - gui_validator.py ausgeführt: "SUCCESS: No structural imbalances detected."
**UI-Funktionalität:**
  - Tab-Switching: "Parser", "Debug", "Tests" nutzen eindeutige IDs und werden korrekt angesprochen.
  - Options-Header: Hauptüberschrift wechselt synchron mit Sub-Tab.
  - Transcoding-Tag: [TRANSCODED] wird per JS korrekt angezeigt.

### Hinweise zur Überprüfung
1. App öffnen, zu Optionen wechseln und zwischen den Sub-Tabs klicken – Header muss synchron wechseln.
2. Transkodiertes Medium abspielen und Sidebar auf [TRANSCODED]-Badge prüfen.
3. Footer prüfen: Bei Idle "Wähle ein Lied aus der Liste!" (bzw. englisches Pendant), bei Wiedergabe "Spielt: ... von ...".

Dieses Dokument beschreibt den Plan zur Stabilisierung der HTML-Struktur durch Anker-Kommentare sowie die Behebung von Fehlern in der Tab-Anzeige (Parser, Debug, Tests), dem Audio-Footer und der Sidebar.

### Geplante Änderungen
1. **Struktur-Stabilisierung (Anker-Kommentare) in web/app.html**
   - An allen Haupt-Containern (Tabs, Panels, Splitter) werden Anker-Kommentare eingefügt, z.B.:
     - Navigations-Tabs: <!-- TAB BUTTONS START --> / <!-- TAB BUTTONS END -->
     - Sidebar: <!-- SIDEBAR START --> / <!-- SIDEBAR END -->
     - Tab-Panels:
       - <!-- TAB: Player START --> / <!-- TAB: Player END -->
       - <!-- TAB: Library START --> / <!-- TAB: Library END -->
       - <!-- TAB: Options START --> / <!-- TAB: Options END -->
       - <!-- TAB: Parser START --> / <!-- TAB: Parser END -->
       - <!-- TAB: Debug START --> / <!-- TAB: Debug END -->
       - <!-- TAB: Tests START --> / <!-- TAB: Tests END -->
       - <!-- TAB: Logbuch START --> / <!-- TAB: Logbuch END -->
     - Sub-Views in Optionen:
       - <!-- VIEW: Options General START --> / <!-- VIEW: Options General END -->
       - <!-- VIEW: Options Tools START --> / <!-- VIEW: Options Tools END -->
       - <!-- VIEW: Options Environment START --> / <!-- VIEW: Options Environment END -->
2. **Header-Visibility in "Optionen" (web/app.html)**
   - Überschriften der Unterkapitel ("Advanced Tools", "System-Infrastruktur") immer sichtbar machen.
   - h2-Elemente aus den Unter-Views in einen zentralen Header-Bereich verschieben.
   - Header synchron mit Sub-Tab-Wechsel aktualisieren.
   - Header für "Allgemeine Einstellungen" ergänzen.
3. **Audio-Footer Fix ("Spielt: von") in web/app.html**
   - Container footer-playback-info ausblenden, wenn kein Track aktiv ist.
   - i18n-Tags für "Spielt" und "von" korrekt in der JS-Logik verknüpfen.
   - "Wähle ein Lied aus der Liste!" darf Footer nicht als aktiv markieren.
4. **Sidebar-Fix (Transcoding-Tag) in web/app.html**
   - Transcoding-Tag in der Sidebar wiederherstellen.
   - Logik in updateMediaSidebar prüfen und reparieren (item.is_transcoded).
   - Sicherstellen, dass sb_transcoding_msg korrekt gerendert wird.

### Verifizierungsplan
- **Automatisierte Validierung:**
  - Ausführen von python scripts/gui_validator.py, um die HTML-Struktur zu prüfen (Div-Balance).
- **Manuelle Prüfung:**
  - Wechseln zwischen allen Tabs (Parser, Debug, Tests), um zu prüfen, dass keine Inhalte verschwinden oder falsch verschachtelt sind.
  - Audio-Footer beim Start (leer/ausgeblendet) und während Wiedergabe ("Spielt: [Titel] von [Interpret]").
  - Auswahl eines transkodierten Mediums und Verifizierung des Tags in der Sidebar.
  - Verifizierung der Header-Sichtbarkeit im Optionen-Tab bei jedem Sub-Tab-Wechsel.
---
