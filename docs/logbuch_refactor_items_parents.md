# Logbuch: Refactoring – Eindeutigkeit von Items und Parents

## Ziel

Dokumentation des Refactorings zur eindeutigen Identifikation von Medieneinträgen (Items) und deren Eltern (Parents) in der Datenbank.

---

## 1. Eindeutigkeit von Items

- **Items** (Medieneinträge) werden ab sofort ausschließlich über den vollständigen Dateipfad (`path`) eindeutig identifiziert.
- Vor jedem Insert wird geprüft, ob bereits ein Eintrag mit demselben Pfad existiert. Nur wenn der Pfad noch nicht vorhanden ist, wird ein neuer Eintrag angelegt.
- Damit sind Duplikate (gleicher Name, aber unterschiedlicher Speicherort) möglich und gewollt, solange der Pfad unterschiedlich ist.
- Die bisherige Prüfung über den Namen entfällt.

**Beispiel:**

| Name         | Pfad                        | Wird eingefügt? |
|--------------|-----------------------------|-----------------|
| song.mp3     | /media/music/song.mp3       | Ja              |
| song.mp3     | /media/backup/song.mp3      | Ja              |
| song.mp3     | /media/music/song.mp3       | Nein (Duplikat) |


### 1.1. Einschränkung: is_mock im main-Branch
#### Mock-Stufen (mock_stage)

- Es existieren verschiedene Mock-Stufen, die über das Feld `mock_stage` definiert werden können (z.B. 1 = Basis-Mock, 2 = erweiterter Mock, 3 = Spezial-Mock etc.).
- Diese Stufen dienen der Entwicklung und dem Testen unterschiedlicher Szenarien.
- Im main-Branch sind alle Mock-Stufen grundsätzlich nicht erlaubt.

**Tabelle: Mock-Stufen und Zulässigkeit im main-Branch**

| is_mock | mock_stage | Item erlaubt? |
|---------|------------|---------------|
| False   | beliebig   | Ja            |
| True    | 1          | Nein          |
| True    | 2          | Nein          |
| True    | 3          | Nein          |
| ...     | ...        | Nein          |

- Im main-Branch der Anwendung sind Items, bei denen das Feld `is_mock` auf `True` gesetzt ist, **nicht erlaubt**.
- Mock-Items dienen ausschließlich zu Test- und Entwicklungszwecken und dürfen nicht in die Produktionsdatenbank gelangen.
- Vor jedem Insert in den main-Branch muss geprüft werden, dass `is_mock` entweder nicht gesetzt oder `False` ist.


**Tabelle: Mock-Items im main-Branch**

| is_mock | Item erlaubt? |
|---------|---------------|
| False   | Ja            |
| True    | Nein          |


## 2. Eindeutigkeit von Parents


Die eindeutige Identifikation von Parent-Objekten (z.B. Alben, Serien, Collections) ist noch **unklar**.
Mögliche Ansätze:
    - **Barcode/Identifier:** Nutzung eines eindeutigen Barcodes oder einer externen ID (z.B. ISBN, EAN, Discogs-ID) zur Identifikation.
    - **Name-Cut:** Algorithmische Kürzung/Normalisierung des Namens (z.B. Entfernen von Jahr, Format, Klammern), um Parent-Objekte zu gruppieren.
    - **Pfad:** Nutzung des übergeordneten Verzeichnispfads als Parent-ID.

### 2.1. Umgang mit Editionen und Formaten

- Bei Medien wie Filmen oder Alben gibt es oft verschiedene Editionen (z.B. Director's Cut, Extended, Premium Edition) oder unterschiedliche Audio-/Video-Formate (z.B. ALAC, FLAC, MP3).
- Ziel ist es, diese Varianten logisch zu gruppieren (z.B. als ein "Parent"-Objekt für das Album/den Film), aber dennoch als eigenständige Items in der Datenbank zuzulassen.
- Mögliche Ansätze:
        - **Editionserkennung:** Analyse des Namens oder der Metadaten, um Editionen zu erkennen und zu gruppieren (z.B. Regex auf "Director's Cut", "Extended", "Remastered").
        - **Formatunterscheidung:** Speicherung des Formats (Codec, Container) als separates Feld, sodass verschiedene Formate desselben Werks als eigene Items, aber unter demselben Parent gruppiert werden können.
        - **Flexible Gruppierung:** Kombination aus Name-Cut (ohne Edition/Format) und Metadaten, um Parent-Objekte zu bilden, die alle Varianten eines Werks umfassen.

**Beispiel:**

| Name                | Edition         | Format | Parent-Gruppe         | Item erlaubt? |
|---------------------|----------------|--------|-----------------------|---------------|
| Album X             | Standard       | FLAC   | Album X               | Ja            |
| Album X             | Premium        | ALAC   | Album X               | Ja            |
| Album X             | Standard       | MP3    | Album X               | Ja            |
| Film Y              | Director's Cut | MKV    | Film Y                | Ja            |
| Film Y              | Standard       | MP4    | Film Y                | Ja            |

So können verschiedene Editionen und Formate eines Werks als eigene Items existieren, werden aber logisch unter einem Parent gruppiert.

### 2.2. Reissue, Rerelease, Länder und Plattformen

- Neben Editionen und Formaten gibt es weitere Varianten, die für die Gruppierung und Eindeutigkeit relevant sind:
    - **Reissue/Rerelease:** Neuauflagen oder Wiederveröffentlichungen eines Werks (z.B. Remastered, 20th Anniversary Edition).
    - **Ländervarianten:** Veröffentlichungen in unterschiedlichen Ländern (z.B. Japan-Edition, US-Version, EU-Pressung).
    - **Digitale Plattformen:** Verschiedene digitale Releases auf Plattformen wie Qobuz, Bandcamp, Amazon, iTunes, Spotify usw.
- Ziel ist es, diese Varianten als eigene Items zuzulassen, aber eine Gruppierung unter einem gemeinsamen Parent zu ermöglichen.
- Mögliche Ansätze:
    - **Release- und Plattform-Metadaten:** Speicherung von Release-Typ (Reissue, Rerelease), Land und Plattform als eigene Felder in der Datenbank.
    - **Flexible Parent-Gruppierung:** Parent-Objekte werden anhand des Werks (z.B. Albumtitel) gebildet, während Items sich durch Edition, Format, Land und Plattform unterscheiden können.

**Beispiel:**

| Name                | Edition         | Format | Land   | Plattform | Parent-Gruppe         | Item erlaubt? |
|---------------------|----------------|--------|--------|-----------|-----------------------|---------------|
| Album X             | Standard       | WAV-24 | UK     | Qobuz     | Album X               | Ja            |
| Album X             | Reissue        | FLAC   | JP     | Bandcamp  | Album X               | Ja            |
| Album X             | Rerelease      | MP3    | US     | Amazon    | Album X               | Ja            |
| Album X             | Standard       | ALAC   | EU     | iTunes    | Album X               | Ja            |
| Album X             | Premium        | FLAC   | DE     | Physisch  | Album X               | Ja            |

So können verschiedene Veröffentlichungen desselben Werks (unterschiedliche Editionen, Länder, Plattformen) als eigene Items existieren, werden aber logisch unter einem Parent gruppiert.

Aktuell ist keine dieser Methoden final implementiert. Die Entscheidung steht noch aus.

---

## 3. ToDo & Ausblick

- Implementierung der Pfad-basierten Eindeutigkeit für Items in allen relevanten Import- und Insert-Funktionen.
- Evaluierung und Auswahl einer robusten Methode zur Parent-Identifikation (Barcode, Name-Cut, Pfad, ...).
- Anpassung der Datenbankabfragen und UI, um die neue Logik zu unterstützen.

---

## 4. Historie

- 2026-03-28: Logbuch-Eintrag erstellt, Status dokumentiert.

---

## 5. Referenzen

- Siehe auch: `db.py`, `main.py`, bestehende Insert- und Query-Logik.
- Siehe Logbücher zu Datenbankabfragen und Parent-Handling.
