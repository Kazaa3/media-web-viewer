# Logbuch: parent_id – Hierarchie und Verknüpfung von Medienobjekten

## Ziel
Dokumentation der Bedeutung, Nutzung und Best Practices des Feldes `parent_id` in der Media-Datenbank. `parent_id` ermöglicht die Abbildung von Hierarchien und logischen Verknüpfungen zwischen Medienobjekten (z.B. Album → Track, Boxset → Disc, Image → Einzelbild).

---

## 1. Motivation
- Viele Medienobjekte stehen in einer logischen Beziehung zueinander (z.B. ein Album besteht aus Tracks, eine DVD-Box aus mehreren Discs).
- Mit `parent_id` lassen sich solche Hierarchien und Gruppierungen sauber abbilden und abfragen.

---

## 2. Anwendungsfälle
- **Album/Track**: Jeder Track verweist mit `parent_id` auf das zugehörige Album.
- **Boxset/Disc**: Jede Disc eines Boxsets hat als `parent_id` die ID des Boxsets.
- **Image/Einzelbild**: Einzelbilder in einem Image (z.B. Photo-CD) referenzieren das übergeordnete Image.
- **Sammlungen**: Beliebige Gruppierungen (z.B. Compilation, Multi-Disc-Set) können über `parent_id` abgebildet werden.

---

## 3. Beispiel
```json
{
  "id": 123,
  "media_type": "album",
  "name": "Abbey Road"
}
{
  "id": 456,
  "media_type": "track",
  "name": "Come Together",
  "parent_id": 123
}
```

---

## 4. Vorteile
- **Hierarchische Abfragen**: Ermöglicht das Traversieren und Anzeigen von Medienstrukturen (z.B. alle Tracks eines Albums).
- **Flexibilität**: Beliebige Tiefe und Typen von Beziehungen möglich.
- **UI/UX**: Darstellung von Alben, Boxsets, Sammlungen, Playlists etc. wird erleichtert.

---

## 5. Best Practices
- Beim Einfügen von Objekten immer prüfen, ob ein `parent_id` gesetzt werden muss.
- Für Top-Level-Objekte (z.B. Album, Boxset) bleibt `parent_id` leer oder `null`.
- Bei Löschvorgängen: Kindobjekte mitbehandeln (z.B. alle Tracks eines Albums löschen, wenn das Album entfernt wird).
- Abfragen und UI sollten rekursiv/baumartig auf `parent_id` reagieren können.

---

## 6. Erweiterungen
- **group_id**: Für komplexere Gruppierungen (z.B. Multi-Album-Boxsets, Playlists).
- **parent_type**: Optional zur Typabsicherung (z.B. nur Album → Track zulassen).

---

## Fazit
Das Feld `parent_id` ist essenziell für die Abbildung von Hierarchien und Beziehungen in der Media-Datenbank. Es ermöglicht flexible, skalierbare und logisch nachvollziehbare Strukturen für alle Medientypen und ist Grundlage für viele UI- und Backend-Operationen.

---

## Aktueller Stand: Offenheit und Implementierung von `parent_id`

**Im Code und Schema aktuell offen/genutzt:**
- **Datenbankschema:** `parent_id` ist als INTEGER mit Fremdschlüssel auf `media(id)` definiert (siehe db.py).
- **Insert/Update:** Beim Einfügen und Aktualisieren von Medienobjekten wird `parent_id` aus dem item_dict übernommen und gespeichert.
- **Modelle:** In models.py wird `parent_id` aus den Tags extrahiert und beim Serialisieren ausgegeben.
- **Import/Scan:** Beim Medienimport wird `parent_id` aus Mapping-Tabellen gesetzt und an die Datenbank übergeben.
- **Objektstruktur:** In der Medienobjekt-Logik (siehe logbuch_objekt_rework.md) wird `parent_id` für Hierarchien wie Album→Track, Boxset→Disc, Image→Einzelbild genutzt.
- **Beispielobjekte:** parent_id ist null für Top-Level-Objekte und verweist auf die ID des Elternobjekts für untergeordnete Items.

**Fazit:**

---

## Aktuelle Typen im Projekt (media_type, subtype, file_type, category, type)

**media_type (Obertypen):**
- image
- album
- track
- video
- collection
- container
- file
- playlist
- ebook
- document
- disk
- folder
- unknown

**subtype (Feintypen):**
- dvd
- bluray
- iso
- photo_album
- boxset
- audio_album
- audio_track
- book
- unknown

**file_type (technische Typen):**
- iso
- mkv
- flac
- hoerbuch-m4b
- audio-file
- video-file
- ebook-file
- document-file
- disk-file

**category (Kategorien):**
- Audio
- Album
- Hörbuch
- Klassik
- Compilation
- Single
- Podcast
- Radio
- Video
- Film
- Serie
- Bilder
- Dokument
- E-Book
- Abbild
- ISO/Image
- Disk Image
- PAL DVD
- NTSC DVD
- Blu-ray
- PAL DVD (Abbild)
- NTSC DVD (Abbild)
- DVD (Abbild)
- Blu-ray (Abbild)
- Audio-CD (Abbild)
- CD-ROM (Abbild)
- Disk-Abbild
- PC Spiel
- PC Spiel (Index)
- Digitales Spiel (Steam)
- Spiel
- Supplement
- Beigabe
- Software
- Ordner
- Buch

**type (Logik/Mapping):**
- audio
- video
- image
- ebook
- document
- disk
- folder
- playlist
- unknown

H