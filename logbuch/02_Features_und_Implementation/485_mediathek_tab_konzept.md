# Logbuch: Mediathek-Tab – Konzept & UI-Design (2026-03-15)

## 1. Umbenennung & Tab-Struktur
- Der bisherige "Bibliothek"-Tab wird in "File"-Tab umbenannt (Schwerpunkt: Dateiansicht, Dateiexplorer).
- Ein neuer "Mediathek"-Tab wird eingeführt:
  - Fokus: Medienobjekte (Audio, Film, Daten, Bilder etc.)
  - Medientypen werden als eigene Objekte verwaltet und angezeigt.

## 2. Mediathek-Tab: Features & UI
- **Objekttypen:**
  - Audio-Objekte (z.B. Musik, Hörbücher)
  - Film-Objekte (z.B. Spielfilme, Serien)
  - Daten-Objekte (z.B. Dokumente, Archive)
  - Weitere Medientypen (z.B. Bilder, Podcasts, Playlists)
- **Visualisierung:**
  - Filmcover und Audiocover als Slideshow/Carousel
  - Übersichtliche Kachel- oder Listenansicht
- **Filter & Navigation:**
  - Oben rechts: Dropdown-Menü für Display-Filter (z.B. nur Filme, nur Audio, alle)
  - Optional: Reiter/Tabs für verschiedene Medientypen (z.B. "Alle", "Filme", "Audio", "Daten")
  - Suchfeld für schnelle Filterung

## 3. Beispiel-UI (Skizze)

```
+-------------------------------------------------------------+
| Mediathek   | File   | ...                                  |
+-------------------------------------------------------------+
| [Suchfeld]         [Dropdown: Alle/Filme/Audio/Daten] [≡]   |
+-------------------------------------------------------------+
| [ Filmcover  ]  [ Audiocover ]  [ Datenobjekt ]  ...        |
| [ Slideshow  ]  [ Slideshow  ]  [ Kachel      ]             |
+-------------------------------------------------------------+
```

## 4. Technische Hinweise
- Mediathek-Tab nutzt die bestehenden MediaItem-Modelle, erweitert um Typ- und Cover-Attribute.
- Filterlogik und UI-Elemente werden im Frontend (web/app.html, JS) ergänzt.
- Backend liefert gefilterte Listen je nach Typ/Filter.

## 5. ToDo
- File-Tab umbenennen
- Mediathek-Tab mit Objekttypen, Cover-Slideshow und Filter-Dropdown implementieren
- Filterlogik im Backend und Frontend ergänzen
- UI/UX-Tests für neue Mediathek-Ansicht

## 6. Erweiterung: Mediathek-Statistiken (nicht Diagnostik)
- Im Mediathek-Tab werden zusätzlich reine Nutzungs- und Inhaltsstatistiken angezeigt (keine Systemdiagnostik).
- **Beispielhafte Statistiken:**
  - Anzahl Filme, Audios, Datenobjekte, Bilder etc.
  - Gesamtdauer aller Filme/Audios
  - Größte/kleinste Datei
  - Meistgespielte/zuletzt hinzugefügte Medien
  - Verteilung nach Medientyp (z.B. Balkendiagramm)
- **UI-Integration:**
  - Statistikbereich oberhalb oder seitlich der Medienübersicht
  - Optional als Infobox, Balken-/Kreisdiagramm oder kleine Kacheln
- **Technik:**
  - Statistiken werden vom Backend bereitgestellt (z.B. API: `/get_mediathek_stats`)
  - Frontend zeigt die Werte und Diagramme an, aktualisiert bei Filterwechsel
- **Abgrenzung:**
  - Keine System-/Diagnosewerte (CPU, RAM, Fehler etc.), sondern reine Medien- und Nutzungsstatistik

## 7. Erweiterung: Cover Flow für Mediathek
- Im Mediathek-Tab wird ein moderner "Cover Flow" als zentrales UI-Element integriert.
- **Funktion:**
  - Medienobjekte (Filme, Audios, Bilder) werden als große Cover in einer horizontal scrollbaren 3D-Ansicht präsentiert.
  - Nutzer kann per Maus, Touch oder Pfeiltasten durch die Cover "fließen" (ähnlich iTunes Cover Flow).
  - Das aktuell ausgewählte Cover wird hervorgehoben (zentral, größer), flankiert von den nächsten/vorherigen Covern.
- **Features:**
  - Sofortvorschau: Beim Anwählen eines Covers werden Metadaten und ggf. ein Mini-Player angezeigt.
  - Filterintegration: Cover Flow zeigt nur die aktuell gefilterten Medientypen (z.B. nur Filme).
  - Optional: Animationen beim Wechsel, sanftes Ein-/Ausblenden.
- **Technik:**
  - Frontend: Umsetzung mit CSS3/JS (z.B. mit bestehenden Coverflow-Libraries oder eigener Komponente)
  - Backend: Liefert die Metadaten und Cover-URLs für die aktuelle Filterung
- **UI-Integration:**
  - Cover Flow als Hauptbereich im Mediathek-Tab, darunter oder daneben Detailinfos/Statistiken
- **Vorteile:**
  - Intuitive, visuelle Navigation durch große Mediensammlungen
  - Moderne, attraktive Benutzeroberfläche
