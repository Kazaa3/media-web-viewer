<!-- Category: Documentation -->
<!-- Title_DE: E-Book, EPUB & PDF Integration -->
<!-- Title_EN: E-Book, EPUB & PDF Integration -->
<!-- Summary_DE: Erweiterung der Bibliothek um Textmedien: EPUB/PDF-Parsing, Comic-Archive und Calibre-Fallback. -->
<!-- Summary_EN: Expanding the library with text media: EPUB/PDF parsing, comic archives and Calibre-fallback. -->
<!-- Status: ACTIVE -->

# E-Book, EPUB & PDF Integration

## Jenseits von Audio und Video
Ein modernes Medienarchiv ist unvollständig ohne die geschriebene Welt. Deshalb wurde **dict - Web Media Player & Library** um eine leistungsfähige Dokumenten-Pipeline erweitert, die E-Books, Dokumente und Comics nahtlos integriert.

## Technische Umsetzung: Die Buch-Parser
Die Extraktion von Metadaten aus Textmedien folgt dem bewährten **Handler-Pattern**:

1.  **EPUB (`ebooklib` / `fitz`):** Wir extrahieren Titel, Autor, Sprache und vor allem das **Cover-Bild** direkt aus dem EPUB-Container.
2.  **PDF (`fitz` / PyMuPDF):** PDF-Dateien werden auf interne Metadaten gescannt. Falls diese fehlen, nutzt dict fortschrittliche Heuristiken, um den Titel aus der ersten Seite des Dokuments zu extrahieren.
3.  **Comic-Archive (CBR/CBZ):** Diese Formate sind im Grunde Bilder-Archive (RAR/ZIP). Dict öffnet sie, zählt die Seiten und extrahiert das erste Bild als Cover für die Bibliothek.

## Der Calibre-Fallback
Für exotische Formate (z.B. MOBI, AZW3 oder alte Palm-PDBs), für die es keine schlanken Python-Parser gibt, nutzt dict eine optionale Integration von **Calibre**:
- Wenn Calibre auf dem System installiert ist, kann dict dessen Kommandozeilen-Tools nutzen, um Metadaten auszulesen oder Formate für die interne Vorschau zu konvertieren.

## Dokumenten-Vorschau
Im UI von dict werden E-Books wie Audio-Alben behandelt:
- **Metadaten-Grid:** Anzeige von Seitenzahlen anstelle von Titellängen.
- **Schnellansicht:** Integration von Web-Viewern für PDFs und EPUBs direkt im Browser-Frontend.

*Mit der Integration von E-Books wird dict zur zentralen Anlaufstelle für das gesamte digitale Wissen und Entertainment des Nutzers.*

<!-- lang-split -->

# E-Book, EPUB & PDF Integration

## Beyond Audio and Video
A modern media archive is incomplete without the written world. Therefore, **dict - Web Media Player & Library** has been expanded to include a powerful document pipeline that seamlessly integrates e-books, documents, and comics.

## Technical Implementation: The Book Parsers
The extraction of metadata from text media follows the proven **Handler Pattern**:

1.  **EPUB (`ebooklib` / `fitz`):** We extract title, author, language and above all the **cover image** directly from the EPUB container.
2.  **PDF (`fitz` / PyMuPDF):** PDF files are scanned for internal metadata. If it is missing, dict uses advanced heuristics to extract the title from the first page of the document.
3.  **Comic Archives (CBR/CBZ):** These formats are basically image archives (RAR/ZIP). Dict opens them, counts the pages and extracts the first image as a cover for the library.

## The Calibre Fallback
For exotic formats (e.g., MOBI, AZW3 or old Palm PDBs) for which there are no lightweight Python parsers, dict uses an optional integration of **Calibre**:
- If Calibre is installed on the system, dict can use its command line tools to read metadata or convert formats for internal preview.

## Document Preview
In the dict UI, e-books are treated like audio albums:
- **Metadata Grid:** Display of page numbers instead of track lengths.
- **Quick View:** Integration of web viewers for PDFs and EPUBs directly in the browser frontend.

*With the integration of e-books, dict becomes the central hub for the user's entire digital knowledge and entertainment.*
